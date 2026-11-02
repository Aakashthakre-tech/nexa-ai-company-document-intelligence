import type { ChatResponse, DocumentListResponse, StatsResponse } from '../types';

const API_BASE = '/api';

export async function sendMessage(question: string, sessionId?: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, session_id: sessionId }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server error (${res.status})`);
  }

  return res.json();
}

export async function resetSession(sessionId?: string): Promise<{ message: string; session_id: string }> {
  const url = sessionId ? `${API_BASE}/chat/reset?session_id=${encodeURIComponent(sessionId)}` : `${API_BASE}/chat/reset`;
  const res = await fetch(url, { method: 'POST' });
  if (!res.ok) {
    throw new Error('Failed to reset session');
  }
  return res.json();
}

export async function getDocuments(): Promise<DocumentListResponse> {
  const res = await fetch(`${API_BASE}/documents`);
  if (!res.ok) {
    throw new Error('Failed to load documents');
  }
  return res.json();
}

export async function uploadDocument(file: File): Promise<{ filename: string; size_mb: number; chunks_added: number; message: string }> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to upload document');
  }

  return res.json();
}

export async function deleteDocument(filename: string): Promise<{ status: string; message: string; filename: string }> {
  const res = await fetch(`${API_BASE}/documents/${encodeURIComponent(filename)}`, {
    method: 'DELETE',
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to delete document');
  }

  return res.json();
}

export async function getStats(): Promise<StatsResponse> {
  const res = await fetch(`${API_BASE}/stats`);
  if (!res.ok) {
    throw new Error('Failed to fetch system stats');
  }
  return res.json();
}

export async function getHealth(): Promise<{ status: string; model: string; vector_store: string; embeddings: string }> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) {
    throw new Error('Health check failed');
  }
  return res.json();
}
