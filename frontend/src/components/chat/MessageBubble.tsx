import React from 'react';
import { Bot, User, ShieldCheck, AlertTriangle, FileText, CheckCircle2 } from 'lucide-react';
import { Message } from '../../types';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end mb-6">
        <div className="max-w-2xl rounded-2xl rounded-tr-sm bg-gradient-to-r from-blue-600/30 via-indigo-600/20 to-slate-800/80 border border-blue-500/30 p-4 shadow-lg shadow-black/20">
          <div className="flex items-center gap-2 mb-1 text-[10px] uppercase font-bold tracking-wider text-blue-400">
            <User className="w-3 h-3" />
            <span>You</span>
            <span className="text-slate-500 font-normal ml-auto">{message.timestamp}</span>
          </div>
          <p className="text-sm text-slate-100 leading-relaxed whitespace-pre-wrap">
            {message.content}
          </p>
        </div>
      </div>
    );
  }

  const isLowConf = message.is_low_confidence || message.evidence_strength === 'LOW';

  return (
    <div className="flex justify-start mb-6">
      <div className="max-w-3xl w-full rounded-2xl rounded-tl-sm bg-slate-900/80 border border-slate-800/90 border-l-4 border-l-blue-500 p-5 shadow-xl shadow-black/25">
        {/* Agent Header & Reasoning Tag */}
        <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800/80">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
              <Bot className="w-4 h-4" />
            </div>
            <div>
              <span className="text-xs font-bold text-white tracking-tight">NEXA AI</span>
              <span className="ml-2 text-[10px] text-slate-400">Grounded Agent</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {message.confidence !== undefined && (
              <div className={`flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-semibold border ${
                isLowConf 
                  ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' 
                  : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
              }`}>
                {isLowConf ? <AlertTriangle className="w-3 h-3" /> : <ShieldCheck className="w-3 h-3" />}
                <span>{Math.round(message.confidence * 100)}% Confidence</span>
              </div>
            )}
            <span className="text-[10px] text-slate-500">{message.timestamp}</span>
          </div>
        </div>

        {/* Low Confidence Hallucination Warning Banner */}
        {isLowConf && (
          <div className="mb-3 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
            <div className="text-xs text-rose-300">
              <b>Low evidence alert:</b> The available knowledge documents do not contain direct or conclusive information regarding this question.
            </div>
          </div>
        )}

        {/* Final Grounded Answer */}
        <div className="text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">
          {message.content}
        </div>

        {/* Evidence Sources Pills */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-4 pt-3 border-t border-slate-800/80">
            <div className="text-[10px] uppercase font-bold text-slate-500 mb-2 flex items-center gap-1.5">
              <CheckCircle2 className="w-3 h-3 text-blue-400" />
              <span>Verified Evidence Sources ({message.sources.length})</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {message.sources.map((s, idx) => (
                <span
                  key={idx}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700 text-xs text-slate-300 hover:text-white transition-colors"
                >
                  <FileText className="w-3 h-3 text-blue-400" />
                  <span>{s.source}</span>
                  {s.relevance_score && (
                    <span className="text-[10px] text-slate-500">
                      ({Math.round(s.relevance_score * 100)}%)
                    </span>
                  )}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
