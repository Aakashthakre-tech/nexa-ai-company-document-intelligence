from typing import List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., description="User question to the AI Agent")
    session_id: Optional[str] = Field(None, description="Optional session identifier for conversation continuity")


class SourceItem(BaseModel):
    source: str
    excerpt: str
    distance: Optional[float] = None
    relevance_score: Optional[float] = None
    page: Optional[int] = None


class ActivityStep(BaseModel):
    id: str
    label: str
    status: str = Field(..., description="pending, running, completed, or failed")
    detail: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    confidence: float
    evidence_strength: str  # "HIGH", "MEDIUM", "LOW"
    is_low_confidence: bool
    activity: List[ActivityStep]
    session_id: str
    status: str = "success"


class DocumentItem(BaseModel):
    id: str
    name: str
    size_mb: float
    chunks_count: int
    status: str
    updated_at: str


class DocumentListResponse(BaseModel):
    documents: List[DocumentItem]
    total_documents: int
    total_chunks: int


class StatsResponse(BaseModel):
    documents_count: int
    chunks_count: int
    model: str
    vector_store: str
    embeddings: str
    status: str = "online"


class UploadResponse(BaseModel):
    filename: str
    size_mb: float
    chunks_added: int
    message: str
    status: str = "success"


class ResetResponse(BaseModel):
    message: str
    session_id: str
    status: str = "success"
