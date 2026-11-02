import React, { useState } from 'react';
import { Database, Bot, RefreshCw, CheckCircle2, Shield } from 'lucide-react';
import { resetSession } from '../../services/api';

interface SettingsViewProps {
  onSessionReset: () => void;
}

export const SettingsView: React.FC<SettingsViewProps> = ({ onSessionReset }) => {
  const [resetting, setResetting] = useState(false);
  const [resetMessage, setResetMessage] = useState<string | null>(null);

  const handleReset = async () => {
    setResetting(true);
    setResetMessage(null);
    try {
      await resetSession();
      onSessionReset();
      setResetMessage('Conversation state reset successfully.');
      setTimeout(() => setResetMessage(null), 2500);
    } catch (err: any) {
      setResetMessage('Failed to reset conversation.');
    } finally {
      setResetting(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-8 max-w-4xl mx-auto w-full space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white tracking-tight">System & AI Agent Configuration</h2>
        <p className="text-xs text-slate-400 mt-1">
          Adjust model parameters, review vector store persistence, and manage conversation memory.
        </p>
      </div>

      {/* Model & Agent Settings */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md space-y-4">
        <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
          <Bot className="w-4 h-4 text-blue-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Language Model & Agent Parameters
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800">
            <div className="text-slate-400 font-medium mb-1">Active Model</div>
            <div className="text-white font-semibold text-sm">Gemini 2.5 Flash</div>
            <div className="text-[11px] text-slate-500 mt-1">Managed via Google GenAI SDK</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800">
            <div className="text-slate-400 font-medium mb-1">Tool Calling Hook</div>
            <div className="text-white font-semibold text-sm">search_company_docs</div>
            <div className="text-[11px] text-slate-500 mt-1">Automatic function calling registered</div>
          </div>
        </div>
      </div>

      {/* Vector Database & Retrieval */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md space-y-4">
        <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
          <Database className="w-4 h-4 text-violet-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Vector Database & Embedding Configuration
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800">
            <div className="text-slate-400 font-medium mb-1">Vector DB</div>
            <div className="text-white font-semibold">ChromaDB Persistent</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Path: ./chroma_db</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800">
            <div className="text-slate-400 font-medium mb-1">Embeddings Model</div>
            <div className="text-white font-semibold">all-MiniLM-L6-v2</div>
            <div className="text-[10px] text-slate-500 mt-0.5">384 Dimensions</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800">
            <div className="text-slate-400 font-medium mb-1">Top K Chunks</div>
            <div className="text-white font-semibold">3 Chunks</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Chunk Size: 500 / Overlap: 50</div>
          </div>
        </div>
      </div>

      {/* Hallucination Protection Policy */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md space-y-3">
        <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
          <Shield className="w-4 h-4 text-emerald-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Grounding & Hallucination Guard
          </span>
        </div>
        <p className="text-xs text-slate-400 leading-relaxed">
          Nexa AI Agent enforces strict factual grounding. The agent only formulates answers when relevant facts exist in the indexed ChromaDB collection. When answers are missing from company documents, the system refuses to extrapolate.
        </p>
      </div>

      {/* Conversation Memory Action */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md flex items-center justify-between">
        <div>
          <div className="text-sm font-semibold text-white">Reset Conversation Memory</div>
          <div className="text-xs text-slate-400 mt-0.5">
            Clear multi-turn message history and restart with a clean state.
          </div>
        </div>

        <button
          onClick={handleReset}
          disabled={resetting}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-400 text-xs font-semibold transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${resetting ? 'animate-spin' : ''}`} />
          <span>Reset Session</span>
        </button>
      </div>

      {resetMessage && (
        <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-400 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          <span>{resetMessage}</span>
        </div>
      )}
    </div>
  );
};
