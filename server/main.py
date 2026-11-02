import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.agent import retrieve_evidence, verify_and_answer
from src.document_loader import load_documents
from src.vector_store import add_page_documents, collection, search_documents
from server.models import (
    ActivityStep,
    ChatRequest,
    ChatResponse,
    DocumentItem,
    DocumentListResponse,
    ResetResponse,
    SourceItem,
    StatsResponse,
    UploadResponse,
)

app = FastAPI(
    title="Nexa AI Enterprise Intelligence API",
    description="FastAPI Backend for Nexa AI Enterprise Document Intelligence Platform",
    version="2.0.0"
)

# Configure CORS for local development and standard frontend ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store for tracking conversation continuity
chat_sessions: Dict[str, List[Dict[str, str]]] = {}


def get_or_create_session(session_id: Optional[str]) -> str:
    """Returns an existing session ID or registers a new one."""
    s_id = session_id or str(uuid.uuid4())
    if s_id not in chat_sessions:
        chat_sessions[s_id] = []
    return s_id


@app.get("/api/health")
def health_check():
    """Liveness probe returning system status."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model": "Gemini 2.5 Flash",
        "vector_store": "ChromaDB",
        "embeddings": "all-MiniLM-L6-v2",
        "pipeline": "2-Agent Grounded RAG"
    }


@app.get("/api/stats", response_model=StatsResponse)
def get_stats():
    """Retrieve system-wide indexing and architecture metrics."""
    doc_folder = "data/documents"
    doc_count = 0
    if os.path.exists(doc_folder):
        doc_count = len([f for f in os.listdir(doc_folder) if f.lower().endswith(".pdf")])

    try:
        chunks_count = collection.count()
    except Exception:
        chunks_count = 0

    return StatsResponse(
        documents_count=doc_count,
        chunks_count=chunks_count,
        model="Gemini 2.5 Flash",
        vector_store="ChromaDB",
        embeddings="all-MiniLM-L6-v2",
        status="online"
    )


@app.get("/api/documents", response_model=DocumentListResponse)
def list_documents():
    """List all indexed documents with metadata and chunk metrics."""
    doc_folder = "data/documents"
    doc_items: List[DocumentItem] = []
    total_chunks = 0

    try:
        total_chunks = collection.count()
    except Exception:
        total_chunks = 0

    if os.path.exists(doc_folder):
        for fname in sorted(os.listdir(doc_folder)):
            if fname.lower().endswith(".pdf"):
                fpath = os.path.join(doc_folder, fname)
                try:
                    stat = os.stat(fpath)
                    size_mb = round(stat.st_size / (1024 * 1024), 2)
                    mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%b %d, %Y %H:%M")
                except OSError:
                    size_mb = 0.0
                    mod_time = "Unknown"

                # Query chunk count for this specific document
                try:
                    matching = collection.get(where={"source": fname})
                    chunk_count = len(matching["ids"]) if matching and "ids" in matching else 0
                except Exception:
                    chunk_count = 0

                doc_items.append(
                    DocumentItem(
                        id=fname,
                        name=fname,
                        size_mb=size_mb,
                        chunks_count=chunk_count,
                        status="Indexed",
                        updated_at=mod_time
                    )
                )

    return DocumentListResponse(
        documents=doc_items,
        total_documents=len(doc_items),
        total_chunks=total_chunks
    )


@app.post("/api/documents/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document, extract page-level records (with Gemini Vision OCR fallback),
    delete any pre-existing chunks for the file, and index page-aware chunks into ChromaDB.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Unsupported format. Currently only PDF documents are supported."
        )

    doc_folder = "data/documents"
    os.makedirs(doc_folder, exist_ok=True)
    target_path = os.path.join(doc_folder, file.filename)

    try:
        content = await file.read()
        with open(target_path, "wb") as f:
            f.write(content)
        size_mb = round(len(content) / (1024 * 1024), 2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Extract page-level records using load_documents (with OCR fallback for low-text pages)
    try:
        page_docs = load_documents(target_path)
        if not page_docs:
            raise HTTPException(
                status_code=400,
                detail="The uploaded document does not contain readable pages."
            )

        # Reject only if no usable text could be extracted from the entire document
        total_text = "".join(doc.get("text", "") or "" for doc in page_docs).strip()
        if not total_text:
            raise HTTPException(
                status_code=400,
                detail="The uploaded document does not contain usable readable text."
            )

        # Delete any pre-existing chunks for this filename to ensure a clean update
        try:
            collection.delete(where={"source": file.filename})
        except Exception:
            pass

        # Index page-aware chunks into ChromaDB
        chunk_ids = add_page_documents(page_docs)
        if not chunk_ids:
            raise HTTPException(
                status_code=400,
                detail="Failed to create chunks from document."
            )

        return UploadResponse(
            filename=file.filename,
            size_mb=size_mb,
            chunks_added=len(chunk_ids),
            message=f"Successfully indexed {len(chunk_ids)} page-aware chunks into vector knowledge base."
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing document: {str(e)}")


@app.delete("/api/documents/{filename}")
def delete_document(filename: str):
    """Delete a document from filesystem and ChromaDB collection."""
    doc_folder = "data/documents"
    target_path = os.path.join(doc_folder, filename)

    if not os.path.exists(target_path):
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        os.remove(target_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file from disk: {str(e)}")

    try:
        collection.delete(where={"source": filename})
    except Exception as e:
        print(f"Warning: Failed to delete Chroma entries for {filename}: {e}")

    return {
        "status": "success",
        "message": f"Document {filename} deleted successfully.",
        "filename": filename
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Two-Agent Grounded Question Answering Endpoint:
    1. Agent 1 (retrieve_evidence): ChromaDB vector retrieval with document isolation
    2. Agent 2 (verify_and_answer): Strict Gemini 2.5 Flash verification, evidence grounding,
       and calibrated confidence scoring. Returns ONLY verified supporting sources.
    """
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    session_id = get_or_create_session(request.session_id)

    # Activity steps contract for UI visualization
    activity: List[ActivityStep] = [
        ActivityStep(id="received", label="Question received", status="completed", detail=question[:60]),
        ActivityStep(id="retrieval_agent", label="Retrieval Agent", status="running", detail="Searching vector knowledge base"),
        ActivityStep(id="evidence_retrieved", label="Evidence retrieved", status="pending"),
        ActivityStep(id="verification_agent", label="Verification Agent", status="pending"),
        ActivityStep(id="response_generated", label="Response generated", status="pending"),
    ]

    # Step 1: Agent 1 - Retrieval Agent with Document Isolation
    try:
        evidence_result = retrieve_evidence(question, top_k=5)
        evidence_list = evidence_result.get("evidence", [])
    except Exception as e:
        print(f"[Backend Error] Agent 1 retrieval failed: {e}")
        evidence_list = []

    activity[1].status = "completed"
    activity[1].detail = f"Isolated relevant document(s) ({len(evidence_list)} candidates)"
    activity[2].status = "completed"
    activity[2].detail = f"Retrieved {len(evidence_list)} evidence passages"

    # Step 2: Agent 2 - Verification & Grounded Answering Agent
    activity[3].status = "running"
    activity[3].detail = "Verifying factual support & citations"

    try:
        agent2_result = verify_and_answer(question, evidence_list)
        activity[3].status = "completed"
        activity[4].status = "completed"
        activity[4].detail = "Grounded response verified"
    except Exception as e:
        err_msg = str(e)
        print(f"[Backend Error] Agent 2 failed: {err_msg}")
        activity[3].status = "failed"
        activity[4].status = "failed"

        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "Quota" in err_msg:
            friendly_answer = "Gemini is temporarily rate-limited. Please wait a moment and try again."
        else:
            friendly_answer = "Gemini is temporarily unavailable. Please try again."

        return ChatResponse(
            answer=friendly_answer,
            sources=[],
            confidence=0.0,
            evidence_strength="LOW",
            is_low_confidence=True,
            activity=activity,
            session_id=session_id,
            status="error"
        )

    # Handle Agent 2 internal error if reported
    if "error" in agent2_result and not agent2_result.get("supported"):
        err_str = str(agent2_result.get("error", ""))
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "Quota" in err_str:
            friendly_answer = "Gemini is temporarily rate-limited. Please wait a moment and try again."
        else:
            friendly_answer = agent2_result.get("answer", "Gemini is temporarily unavailable. Please try again.")

        return ChatResponse(
            answer=friendly_answer,
            sources=[],
            confidence=0.0,
            evidence_strength="LOW",
            is_low_confidence=True,
            activity=activity,
            session_id=session_id,
            status="error"
        )

    supported = bool(agent2_result.get("supported", False))
    answer = str(agent2_result.get("answer", ""))
    confidence = float(agent2_result.get("confidence", 0.2))
    evidence_strength = str(agent2_result.get("evidence_strength", "LOW"))
    is_low_confidence = (confidence < 0.60) or (not supported)

    # =========================================================
    # STRICT SOURCE FILTERING:
    # Return ONLY the evidence actually verified and used
    # =========================================================
    sources: List[SourceItem] = []

    if supported:
        supporting_passages = agent2_result.get("supporting_passages", [])
        citations = agent2_result.get("citations", [])
        citation_pairs = {
            (str(c.get("source")), int(c.get("page", 1)))
            for c in citations
            if isinstance(c, dict) and "source" in c
        }

        used_items = []
        for idx, item in enumerate(evidence_list, start=1):
            is_passage_matched = idx in supporting_passages
            is_citation_matched = (str(item.get("source")), int(item.get("page", 1))) in citation_pairs
            if is_passage_matched or is_citation_matched:
                used_items.append(item)

        # Fallback: match by source filename if specific passage was not indexed
        if not used_items and citations:
            cited_sources = {str(c.get("source")) for c in citations if isinstance(c, dict) and "source" in c}
            used_items = [item for item in evidence_list if str(item.get("source")) in cited_sources]

        # Safety fallback: if supported but no citation match, include primary passage
        if not used_items and evidence_list:
            used_items = [evidence_list[0]]

        seen_sources = set()
        for item in used_items:
            doc_text = str(item.get("text", "")).strip()
            clean_snippet = " ".join(doc_text.split())[:280] + "..." if len(doc_text) > 280 else doc_text
            src_file = str(item.get("source", "unknown"))
            page_num = int(item.get("page", 1))
            dist = item.get("distance")

            sig = (src_file, page_num, clean_snippet[:60])
            if sig in seen_sources:
                continue
            seen_sources.add(sig)

            if dist is not None:
                rel_score = max(0.05, min(0.99, round(1.0 - (float(dist) / 2.0), 2)))
            else:
                rel_score = 0.85

            sources.append(
                SourceItem(
                    source=src_file,
                    page=page_num,
                    excerpt=clean_snippet,
                    distance=dist,
                    relevance_score=rel_score
                )
            )

    # Record interaction in session history
    chat_sessions[session_id].append({"role": "user", "content": question})
    chat_sessions[session_id].append({"role": "assistant", "content": answer})

    return ChatResponse(
        answer=answer,
        sources=sources,
        confidence=confidence,
        evidence_strength=evidence_strength,
        is_low_confidence=is_low_confidence,
        activity=activity,
        session_id=session_id,
        status="success"
    )


@app.post("/api/chat/reset", response_model=ResetResponse)
def reset_chat_endpoint(session_id: Optional[str] = None):
    """Reset conversation memory for a session or global state."""
    target_id = session_id or "default"
    if target_id in chat_sessions:
        del chat_sessions[target_id]

    new_id = get_or_create_session(target_id)
    return ResetResponse(
        message="Conversation memory reset successfully.",
        session_id=new_id,
        status="success"
    )


# Mount compiled React frontend if dist exists
dist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
if os.path.exists(dist_dir):
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
