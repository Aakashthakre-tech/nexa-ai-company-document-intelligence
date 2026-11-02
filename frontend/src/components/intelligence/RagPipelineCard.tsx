import React from 'react';
import { GitBranch, MessageSquare, Bot, Search, Database, FileText, Sparkles, CheckCircle } from 'lucide-react';

export const RagPipelineCard: React.FC = () => {
  const steps = [
    { label: 'User Question', icon: MessageSquare, color: 'text-blue-400' },
    { label: 'AI Agent', icon: Bot, color: 'text-indigo-400' },
    { label: 'Document Search Tool', icon: Search, color: 'text-cyan-400' },
    { label: 'ChromaDB Vectors', icon: Database, color: 'text-violet-400' },
    { label: 'Relevant Context', icon: FileText, color: 'text-amber-400' },
    { label: 'Gemini 2.5 Flash', icon: Sparkles, color: 'text-pink-400' },
    { label: 'Grounded Answer', icon: CheckCircle, color: 'text-emerald-400' },
  ];

  return (
    <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
      <div className="flex items-center gap-2 pb-3 mb-3 border-b border-slate-800/80">
        <div className="w-6 h-6 rounded-lg bg-violet-500/10 border border-violet-500/25 flex items-center justify-center text-violet-400">
          <GitBranch className="w-3.5 h-3.5" />
        </div>
        <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
          RAG Pipeline Architecture
        </span>
      </div>

      <div className="space-y-1">
        {steps.map((s, idx) => {
          const Icon = s.icon;
          return (
            <React.Fragment key={idx}>
              <div className="flex items-center justify-between p-2 rounded-lg bg-slate-900/50 border border-slate-800/60 hover:border-slate-700 transition-colors">
                <div className="flex items-center gap-2">
                  <Icon className={`w-3.5 h-3.5 ${s.color}`} />
                  <span className="text-xs font-medium text-slate-300">{s.label}</span>
                </div>
                <span className="text-[10px] font-bold text-slate-600">0{idx + 1}</span>
              </div>
              {idx < steps.length - 1 && (
                <div className="text-center text-[10px] text-slate-600 leading-none py-0.5">
                  ↓
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
