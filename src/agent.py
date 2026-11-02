import json
from typing import Any, Dict, List, Optional
from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY
from src.prompts import AGENT2_VERIFICATION_PROMPT
from src.vector_store import search_documents

client = genai.Client(api_key=GEMINI_API_KEY)


# =========================================================
# AGENT 1: RETRIEVAL / RESEARCH AGENT WITH DOCUMENT ISOLATION
# =========================================================
def retrieve_evidence(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Agent 1: Retrieval / Research Agent.
    Queries ChromaDB vector knowledge base and applies document isolation
    to prevent unrelated documents from contaminating the evidence.
    """
    clean_question = (question or "").strip()
    if not clean_question:
        return {"evidence": []}

    # Oversample slightly to evaluate document relevance across candidates
    fetch_k = max(top_k * 2, 8)
    search_res = search_documents(clean_question, top_k=fetch_k)

    if not search_res or "documents" not in search_res or not search_res["documents"]:
        return {"evidence": []}

    doc_list = search_res["documents"][0]
    meta_list = search_res.get("metadatas", [[]])[0]
    dist_list = search_res.get("distances", [[]])[0]

    raw_candidates = []
    for i, doc_text in enumerate(doc_list):
        if not doc_text:
            continue
        cleaned_text = str(doc_text).strip()
        metadata = meta_list[i] if i < len(meta_list) and meta_list[i] else {}
        dist = float(dist_list[i]) if i < len(dist_list) and dist_list[i] is not None else 1.0

        source = str(metadata.get("source", "unknown"))
        raw_page = metadata.get("page")
        page = int(raw_page) if raw_page is not None else None
        extraction_method = str(metadata.get("extraction_method", "text"))

        raw_candidates.append({
            "text": cleaned_text,
            "source": source,
            "page": page,
            "distance": dist,
            "extraction_method": extraction_method,
        })

    if not raw_candidates:
        return {"evidence": []}

    # Prioritize candidates with explicit page numbers and lower distances
    raw_candidates.sort(key=lambda c: (c["page"] is None, c["distance"]))

    # Deduplicate redundant chunks of the same text
    candidates = []
    seen_signatures = set()
    for c in raw_candidates:
        sig = (c["source"], c["text"][:120])
        if sig in seen_signatures:
            continue
        seen_signatures.add(sig)
        # Default page to 1 if not recorded
        c["page"] = c["page"] if c["page"] is not None else 1
        candidates.append(c)

    # Group candidate chunks by source document to evaluate document relevance
    doc_groups: Dict[str, List[Dict[str, Any]]] = {}
    for c in candidates:
        src = c["source"]
        if src not in doc_groups:
            doc_groups[src] = []
        doc_groups[src].append(c)

    # Calculate best distance (min distance) for each document
    doc_min_dist = {
        src: min(item["distance"] for item in items)
        for src, items in doc_groups.items()
    }

    # Sort documents by their strongest relevance (lowest min_dist)
    sorted_docs = sorted(doc_min_dist.keys(), key=lambda s: doc_min_dist[s])
    best_doc = sorted_docs[0]
    best_dist = doc_min_dist[best_doc]

    selected_sources = set()
    selected_sources.add(best_doc)

    # Document Isolation: Keep the best document plus secondary documents
    # whose best chunk is within a reasonable margin of the best document.
    for other_doc in sorted_docs[1:]:
        other_dist = doc_min_dist[other_doc]
        if other_dist <= best_dist + 1.0:
            selected_sources.add(other_doc)

    # Filter chunks to selected relevant documents and discard distant outliers
    filtered_evidence = [
        c for c in candidates
        if c["source"] in selected_sources and c["distance"] < 2.0
    ]

    filtered_evidence.sort(key=lambda x: x["distance"])
    final_evidence = filtered_evidence[:top_k]

    return {"evidence": final_evidence}


# =========================================================
# AGENT 2: STRICT VERIFICATION & ANSWERING AGENT
# =========================================================
def verify_and_answer(question: str, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Agent 2: Verification & Grounding Agent.
    Evaluates evidence sufficiency with Gemini 2.5 Flash, strictly answers from
    verified context, provides citations, and scores confidence grounded in evidence.
    """
    clean_question = (question or "").strip()
    if not clean_question:
        return {
            "answer": "Question cannot be empty.",
            "supported": False,
            "confidence": 0.0,
            "evidence_strength": "LOW",
            "citations": [],
            "supporting_passages": []
        }

    if not evidence:
        return {
            "answer": "The uploaded documents do not contain enough information to answer this question.",
            "supported": False,
            "confidence": 0.15,
            "evidence_strength": "LOW",
            "citations": [],
            "supporting_passages": []
        }

    # Format structured evidence for Agent 2 verification
    evidence_blocks = []
    for idx, item in enumerate(evidence, start=1):
        src = item.get("source", "unknown")
        page = item.get("page", 1)
        method = item.get("extraction_method", "text")
        txt = item.get("text", "").strip()
        evidence_blocks.append(
            f"[Passage {idx}] Source: {src} | Page: {page} | Method: {method}\n{txt}"
        )
    evidence_text = "\n\n".join(evidence_blocks)

    user_content = (
        f"USER QUESTION:\n{clean_question}\n\n"
        f"RETRIEVED EVIDENCE:\n{evidence_text}\n\n"
        f"Evaluate the evidence, verify factual grounding, and respond in the required JSON format:"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[AGENT2_VERIFICATION_PROMPT, user_content],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            )
        )

        raw_text = (response.text or "").strip()
        data = _parse_json_response(raw_text)

        supported = bool(data.get("supported", False))
        answer = str(data.get("answer", "")).strip()

        # Check for refusal phrases in answer text even if supported was mistakenly set to True
        refusal_phrases = [
            "do not contain",
            "does not contain",
            "do not provide",
            "does not provide",
            "not mentioned in",
            "cannot find",
            "not found in",
            "no information",
            "insufficient information",
            "unable to find",
        ]
        is_explicit_refusal = any(phrase in answer.lower() for phrase in refusal_phrases)

        # Parse and calibrate confidence
        try:
            confidence = float(data.get("confidence", 0.2 if not supported else 0.8))
        except (ValueError, TypeError):
            confidence = 0.2 if not supported else 0.8

        if not supported or is_explicit_refusal:
            supported = False
            confidence = min(confidence, 0.30)
            evidence_strength = "LOW"
            citations: List[Dict[str, Any]] = []
            supporting_passages: List[int] = []
        else:
            # Enforce bounded confidence for supported answers (0.40 to 0.95)
            confidence = min(max(confidence, 0.40), 0.95)
            raw_strength = str(data.get("evidence_strength", "HIGH")).upper()
            if raw_strength in ["HIGH", "MEDIUM", "LOW"]:
                evidence_strength = raw_strength
            else:
                evidence_strength = "HIGH" if confidence >= 0.75 else "MEDIUM"

            raw_citations = data.get("citations", [])
            citations = []
            if isinstance(raw_citations, list):
                for c in raw_citations:
                    if isinstance(c, dict) and "source" in c:
                        citations.append({
                            "source": str(c["source"]),
                            "page": int(c.get("page", 1))
                        })

            raw_passages = data.get("supporting_passages", [])
            supporting_passages = []
            if isinstance(raw_passages, list):
                for p in raw_passages:
                    try:
                        p_int = int(p)
                        if 1 <= p_int <= len(evidence):
                            supporting_passages.append(p_int)
                    except (ValueError, TypeError):
                        pass

        return {
            "answer": answer,
            "supported": supported,
            "confidence": round(confidence, 2),
            "evidence_strength": evidence_strength,
            "citations": citations,
            "supporting_passages": supporting_passages,
        }

    except Exception as e:
        return {
            "answer": "Error verifying answer with AI agent. Please try again.",
            "supported": False,
            "confidence": 0.0,
            "evidence_strength": "LOW",
            "citations": [],
            "supporting_passages": [],
            "error": str(e)
        }


def _parse_json_response(raw_text: str) -> Dict[str, Any]:
    """Helper to safely parse JSON from model responses, handling code fence wrappers."""
    if not raw_text:
        return {}

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        clean = raw_text.strip()
        if clean.startswith("```"):
            lines = clean.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            clean = "\n".join(lines).strip()
        return json.loads(clean)


# =========================================================
# LEGACY BACKWARD-COMPATIBLE HELPERS
# =========================================================
def search_company_docs(query: str) -> str:
    """Legacy helper: Search company documents and return concatenated chunks."""
    evidence_data = retrieve_evidence(query, top_k=3)
    chunks = [e["text"] for e in evidence_data.get("evidence", [])]
    return "\n\n".join(chunks) if chunks else "No relevant documents found."


chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [search_company_docs]
    }
)


def generate_answer(question: str) -> str:
    """
    Legacy helper for Streamlit app: executes the 2-agent pipeline
    and returns the verified answer string.
    """
    evidence_data = retrieve_evidence(question, top_k=5)
    result = verify_and_answer(question, evidence_data.get("evidence", []))
    return result.get("answer", "No answer could be generated.")