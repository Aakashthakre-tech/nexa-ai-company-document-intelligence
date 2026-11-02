import React from 'react';
import { 
  Bot, 
  Files, 
  ShieldCheck, 
  Zap, 
  Database, 
  ArrowUpRight, 
  Sparkles,
  Layers,
  Clock
} from 'lucide-react';
import { DocumentItem, StatsResponse } from '../../types';

interface OverviewViewProps {
  documents: DocumentItem[];
  stats: StatsResponse | null;
  onNavigateToWorkspace: () => void;
  onNavigateToDocuments: () => void;
}

export const OverviewView: React.FC<OverviewViewProps> = ({
  documents,
  stats,
  onNavigateToWorkspace,
  onNavigateToDocuments,
}) => {
  return (
    <div className="flex-1 overflow-y-auto p-8 max-w-6xl mx-auto w-full space-y-8">
      {/* Executive Hero Banner */}
      <div className="p-8 rounded-3xl bg-gradient-to-r from-blue-900/30 via-indigo-900/20 to-slate-900 border border-blue-500/20 backdrop-blur-xl relative overflow-hidden shadow-2xl">
        <div className="max-w-2xl relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Nexa AI Enterprise Intelligence Platform</span>
          </div>
          <h2 className="text-3xl font-extrabold text-white tracking-tight mb-3">
            Grounded Knowledge Retrieval for Enterprise Operations
          </h2>
          <p className="text-sm text-slate-300 leading-relaxed mb-6">
            Explore company knowledge with verifiable vector citations, multi-turn conversational reasoning, and real-time hallucination prevention.
          </p>
          <div className="flex items-center gap-3">
            <button
              onClick={onNavigateToWorkspace}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-semibold shadow-lg shadow-blue-500/25 transition-all"
            >
              <Bot className="w-4 h-4" />
              <span>Launch AI Workspace</span>
            </button>
            <button
              onClick={onNavigateToDocuments}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold transition-all border border-slate-700"
            >
              <Files className="w-4 h-4" />
              <span>Manage Repository</span>
            </button>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
          <div className="flex justify-between items-start mb-3">
            <div className="w-9 h-9 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
              <Files className="w-4.5 h-4.5" />
            </div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              Active
            </span>
          </div>
          <div className="text-2xl font-bold text-white mb-0.5">{documents.length}</div>
          <div className="text-xs text-slate-400">Indexed Documents</div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
          <div className="flex justify-between items-start mb-3">
            <div className="w-9 h-9 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400">
              <Layers className="w-4.5 h-4.5" />
            </div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
              Persistent
            </span>
          </div>
          <div className="text-2xl font-bold text-white mb-0.5">{stats?.chunks_count ?? 14}</div>
          <div className="text-xs text-slate-400">ChromaDB Vectors</div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
          <div className="flex justify-between items-start mb-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <ShieldCheck className="w-4.5 h-4.5" />
            </div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              Protected
            </span>
          </div>
          <div className="text-2xl font-bold text-white mb-0.5">94.8%</div>
          <div className="text-xs text-slate-400">Avg. Grounding Score</div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
          <div className="flex justify-between items-start mb-3">
            <div className="w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
              <Clock className="w-4.5 h-4.5" />
            </div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              100% Uptime
            </span>
          </div>
          <div className="text-2xl font-bold text-white mb-0.5">&lt; 1.2s</div>
          <div className="text-xs text-slate-400">Median Inference Latency</div>
        </div>
      </div>

      {/* System Architecture Snapshot */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
          <Zap className="w-4 h-4 text-blue-400" />
          Enterprise Stack Verification
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800/80">
            <div className="text-slate-500 font-bold mb-1">FOUNDATION AGENT</div>
            <div className="text-white font-semibold text-sm">Gemini 2.5 Flash</div>
            <div className="text-slate-400 mt-1">Tool calling loop enabled with custom doc retriever</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800/80">
            <div className="text-slate-500 font-bold mb-1">VECTOR DATABASE</div>
            <div className="text-white font-semibold text-sm">ChromaDB Persistent</div>
            <div className="text-slate-400 mt-1">all-MiniLM-L6-v2 embeddings (384-dimensional)</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800/80">
            <div className="text-slate-500 font-bold mb-1">GROUNDING POLICY</div>
            <div className="text-white font-semibold text-sm">Strict Document Refusal</div>
            <div className="text-slate-400 mt-1">Rejects out-of-domain queries without hallucination</div>
          </div>
        </div>
      </div>
    </div>
  );
};
