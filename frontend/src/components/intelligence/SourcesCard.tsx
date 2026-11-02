import React, { useState } from 'react';
import { BookOpen, FileText, ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';
import { SourceItem } from '../../types';

interface SourcesCardProps {
  sources: SourceItem[];
}

export const SourcesCard: React.FC<SourcesCardProps> = ({ sources }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const toggleExpand = (idx: number) => {
    setExpandedIndex(expandedIndex === idx ? null : idx);
  };

  return (
    <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800/80">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-lg bg-blue-500/10 border border-blue-500/25 flex items-center justify-center text-blue-400">
            <BookOpen className="w-3.5 h-3.5" />
          </div>
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Sources & Evidence
          </span>
        </div>
        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
          {sources.length} {sources.length === 1 ? 'source' : 'sources'}
        </span>
      </div>

      {sources.length === 0 ? (
        <div className="p-4 text-center text-xs text-slate-500 border border-dashed border-slate-800 rounded-xl">
          No retrieval executed yet. Ask a question to view cited knowledge sources.
        </div>
      ) : (
        <div className="space-y-2">
          {sources.map((src, idx) => {
            const isExpanded = expandedIndex === idx;
            const relScorePct = src.relevance_score ? Math.round(src.relevance_score * 100) : 85;

            return (
              <div
                key={idx}
                className="rounded-xl bg-slate-900/80 border border-slate-800/90 overflow-hidden transition-all"
              >
                <div
                  onClick={() => toggleExpand(idx)}
                  className="flex items-center justify-between p-2.5 cursor-pointer hover:bg-slate-800/40 transition-colors"
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <div className="w-6 h-6 rounded-md bg-blue-500/10 border border-blue-500/20 flex items-center justify-center shrink-0">
                      <FileText className="w-3 h-3 text-blue-400" />
                    </div>
                    <div className="min-w-0">
                      <div className="text-xs font-medium text-slate-200 truncate">
                        {src.source}
                      </div>
                      <div className="text-[10px] text-slate-500">
                        Relevance: <span className="text-blue-400 font-semibold">{relScorePct}%</span>
                      </div>
                    </div>
                  </div>

                  <button className="text-slate-500 hover:text-slate-300 p-1">
                    {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>
                </div>

                {isExpanded && (
                  <div className="px-3 pb-3 pt-1 border-t border-slate-800/60 bg-slate-950/40">
                    <div className="text-[10px] uppercase font-bold text-slate-500 mb-1">
                      Retrieved Excerpt
                    </div>
                    <div className="text-xs text-slate-300 leading-relaxed font-mono bg-slate-900/90 p-2.5 rounded-lg border border-slate-800/80">
                      "{src.excerpt}"
                    </div>
                    {src.distance !== undefined && src.distance !== null && (
                      <div className="mt-2 text-[10px] text-slate-500">
                        Chroma L2 Distance: <span className="text-slate-400">{src.distance.toFixed(4)}</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
