import React from 'react';
import { Sparkles, FileSearch, ShieldCheck, GitCompare, Clock } from 'lucide-react';

interface EmptyStateProps {
  onSelectSuggestion: (question: string) => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ onSelectSuggestion }) => {
  const suggestions = [
    {
      title: 'What are the working hours?',
      description: 'Check official working times, remote policy, and lunch breaks.',
      icon: Clock,
      color: 'text-blue-400',
    },
    {
      title: 'Tell me about the leave policy.',
      description: 'Review annual, casual, sick leave allowances and notice rules.',
      icon: ShieldCheck,
      color: 'text-emerald-400',
    },
    {
      title: 'Find important company policies.',
      description: 'Extract core HR regulations, attendance rules, and employee guidelines.',
      icon: FileSearch,
      color: 'text-amber-400',
    },
    {
      title: 'Compare documents & technologies.',
      description: 'Analyze technologies, company overview, and technical stack details.',
      icon: GitCompare,
      color: 'text-violet-400',
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center max-w-2xl mx-auto py-12 px-4 text-center">
      {/* Floating AI Orb */}
      <div className="relative mb-6">
        <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-violet-500 flex items-center justify-center text-white shadow-2xl shadow-blue-500/30 border border-white/20 animate-float">
          <Sparkles className="w-10 h-10 text-white" />
        </div>
        <div className="absolute -bottom-2 -right-2 px-2 py-0.5 rounded-full bg-slate-900 border border-slate-700 text-[10px] font-bold text-emerald-400 shadow-md">
          ● Online
        </div>
      </div>

      <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mb-3">
        How can I help you investigate your knowledge?
      </h2>
      <p className="text-sm text-slate-400 max-w-md mb-8 leading-relaxed">
        Ask natural language questions about your company documents and get instant, grounded answers verified against indexed vector evidence.
      </p>

      {/* Suggestion Cards Grid */}
      <div className="w-full grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
        {suggestions.map((item, idx) => {
          const Icon = item.icon;
          return (
            <button
              key={idx}
              onClick={() => onSelectSuggestion(item.title)}
              className="p-4 rounded-xl bg-slate-900/50 hover:bg-slate-800/60 border border-slate-800 hover:border-blue-500/40 transition-all text-left group shadow-sm hover:shadow-md hover:shadow-blue-500/10 hover:-translate-y-0.5"
            >
              <div className="flex items-center gap-3 mb-1.5">
                <div className="w-7 h-7 rounded-lg bg-slate-800 flex items-center justify-center shrink-0 group-hover:bg-blue-500/10 transition-colors">
                  <Icon className={`w-4 h-4 ${item.color}`} />
                </div>
                <span className="text-xs font-semibold text-slate-200 group-hover:text-white transition-colors truncate">
                  {item.title}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed pl-10">
                {item.description}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
