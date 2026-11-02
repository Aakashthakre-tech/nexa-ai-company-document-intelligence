import React from 'react';
import { Sliders, Cpu, Database, Network } from 'lucide-react';
import { StatsResponse } from '../../types';

interface SystemSpecsCardProps {
  stats: StatsResponse | null;
}

export const SystemSpecsCard: React.FC<SystemSpecsCardProps> = ({ stats }) => {
  return (
    <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
      <div className="flex items-center gap-2 pb-3 mb-3 border-b border-slate-800/80">
        <div className="w-6 h-6 rounded-lg bg-cyan-500/10 border border-cyan-500/25 flex items-center justify-center text-cyan-400">
          <Sliders className="w-3.5 h-3.5" />
        </div>
        <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
          Retrieval Stack Specs
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800/70">
          <div className="text-[10px] uppercase font-bold text-slate-500">Foundation LLM</div>
          <div className="font-semibold text-slate-200 mt-0.5">Gemini 2.5 Flash</div>
        </div>
        <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800/70">
          <div className="text-[10px] uppercase font-bold text-slate-500">Vector Engine</div>
          <div className="font-semibold text-slate-200 mt-0.5">ChromaDB Persistent</div>
        </div>
        <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800/70">
          <div className="text-[10px] uppercase font-bold text-slate-500">Embeddings</div>
          <div className="font-semibold text-slate-200 mt-0.5">MiniLM (384-d)</div>
        </div>
        <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800/70">
          <div className="text-[10px] uppercase font-bold text-slate-500">Retrieval Top K</div>
          <div className="font-semibold text-slate-200 mt-0.5">3 Chunks</div>
        </div>
      </div>
    </div>
  );
};
