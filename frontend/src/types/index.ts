export interface SourceItem {
  source: string;
  excerpt: string;
  distance?: number | null;
  relevance_score?: number | null;
}

export interface ActivityStep {
  id: string;
  label: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  detail?: string | null;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  sources?: SourceItem[];
  confidence?: number;
  evidence_strength?: 'HIGH' | 'MEDIUM' | 'LOW';
  is_low_confidence?: boolean;
  activity?: ActivityStep[];
  status?: 'success' | 'error';
}

export interface DocumentItem {
  id: string;
  name: string;
  size_mb: number;
  chunks_count: number;
  status: string;
  updated_at: string;
}

export interface DocumentListResponse {
  documents: DocumentItem[];
  total_documents: number;
  total_chunks: number;
}

export interface StatsResponse {
  documents_count: number;
  chunks_count: number;
  model: string;
  vector_store: string;
  embeddings: string;
  status: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceItem[];
  confidence: number;
  evidence_strength: 'HIGH' | 'MEDIUM' | 'LOW';
  is_low_confidence: boolean;
  activity: ActivityStep[];
  session_id: string;
  status: string;
}

export type NavTab = 'overview' | 'workspace' | 'documents' | 'analytics' | 'settings';
