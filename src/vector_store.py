from typing import Any, Dict, List, Optional, Union
import chromadb
from sentence_transformers import SentenceTransformer

from src.document_loader import chunk_text


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="company_documents"
)


def add_page_documents(
    documents: Union[List[Dict[str, Any]], Dict[str, Any]],
    chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:
    """
    Accept page-level document records in the format:
    {
        "source": "filename.pdf",
        "page": 1,
        "text": "...",
        "needs_ocr": False,
        "extraction_method": "text"
    }
    For every page:
    1. Splits text into chunks using chunk_text.
    2. Generates SentenceTransformer embeddings.
    3. Stores chunks in ChromaDB with metadata:
       {"source": ..., "page": ..., "extraction_method": ...}
    4. Produces unique IDs: f"{source}_page_{page}_chunk_{chunk_idx}"
    """
    if isinstance(documents, dict):
        documents = [documents]

    all_chunks: List[str] = []
    all_ids: List[str] = []
    all_metadatas: List[Dict[str, Any]] = []

    for doc in documents:
        source = str(doc.get("source", "unknown"))
        page = int(doc.get("page", 1))
        text = str(doc.get("text", "") or "")
        extraction_method = str(doc.get("extraction_method", "text"))

        if not text.strip():
            continue

        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{source}_page_{page}_chunk_{i}"
            all_chunks.append(chunk)
            all_ids.append(chunk_id)
            all_metadatas.append({
                "source": source,
                "page": page,
                "extraction_method": extraction_method
            })

    if all_chunks:
        embeddings = model.encode(all_chunks).tolist()
        collection.upsert(
            ids=all_ids,
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas
        )

    return all_ids


def add_documents(
    documents_or_chunks: Union[List[Any], Dict[str, Any]],
    source: Optional[str] = None,
    page: int = 1,
    extraction_method: str = "text",
    chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:
    """
    Add documents or pre-chunked strings to the vector store.
    Supports:
    1. List of page-level document records or single document dictionary.
    2. Legacy chunk strings list: add_documents(chunks, source="filename.pdf")
    """
    if not documents_or_chunks:
        return []

    # Case 1: Single page document record
    if isinstance(documents_or_chunks, dict):
        return add_page_documents([documents_or_chunks], chunk_size=chunk_size, overlap=overlap)

    # Case 2: List of page document records
    if (
        isinstance(documents_or_chunks, list)
        and len(documents_or_chunks) > 0
        and isinstance(documents_or_chunks[0], dict)
    ):
        return add_page_documents(documents_or_chunks, chunk_size=chunk_size, overlap=overlap)

    # Case 3: Legacy list of chunk strings: (chunks, source)
    chunks = documents_or_chunks
    src_name = str(source or "unknown")
    ids = [f"{src_name}_page_{page}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "source": src_name,
            "page": int(page),
            "extraction_method": str(extraction_method)
        }
        for _ in chunks
    ]

    embeddings = model.encode(chunks).tolist()
    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
    return ids


def search_documents(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Search ChromaDB for top_k relevant chunks.
    Returns dictionary with 'documents', 'metadatas', and 'distances'.
    """
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return results