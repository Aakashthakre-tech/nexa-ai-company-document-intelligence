import React from 'react';
import { ShieldCheck, AlertTriangle, ShieldAlert } from 'lucide-react';

interface ConfidenceCardProps {
  confidence?: number;
  evidenceStrength?: 'HIGH' | 'MEDIUM' | 'LOW';
  isLowConfidence?: boolean;
}

export const ConfidenceCard: React.FC<ConfidenceCardProps> = ({
  confidence = 0.92,
  evidenceStrength = 'HIGH',
  isLowConfidence = false,
}) => {
  const percentage = Math.round(confidence * 100);

  const getStrengthColor = () => {
    switch (evidenceStrength) {
      case 'HIGH':
        return {
          text: 'text-emerald-400',
          badge: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
          bar: 'bg-gradient-to-r from-emerald-500 to-teal-400',
        };
      case 'MEDIUM':
        return {
          text: 'text-amber-400',
          badge: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
          bar: 'bg-gradient-to-r from-amber-500 to-yellow-400',
        };
      case 'LOW':
      default:
        return {
          text: 'text-rose-400',
          badge: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
          bar: 'bg-gradient-to-r from-rose-500 to-red-400',
        };
    }
  };

  const style = getStrengthColor();

  return (
    <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800/80">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-lg bg-indigo-500/10 border border-indigo-500/25 flex items-center justify-center text-indigo-400">
            <ShieldCheck className="w-3.5 h-3.5" />
          </div>
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Evidence Confidence
          </span>
        </div>
        <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${style.badge}`}>
          {evidenceStrength}
        </span>
      </div>

      <div className="flex items-baseline justify-between mb-2">
        <span className="text-2xl font-black tracking-tight text-white">
          {percentage}%
        </span>
        <span className="text-xs font-medium text-slate-400">
          Grounding Score
        </span>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-2 rounded-full bg-slate-800/90 overflow-hidden mb-3">
        <div 
          className={`h-full rounded-full transition-all duration-500 ${style.bar}`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* Low Evidence Warning Badge */}
      {isLowConfidence ? (
        <div className="p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-start gap-2.5">
          <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
          <div className="text-[11px] text-rose-300 leading-relaxed">
            <b>Low evidence warning:</b> The available documents do not provide enough verified evidence to answer this question.
          </div>
        </div>
      ) : (
        <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
          <span>Strict document grounding verified · Hallucination protected</span>
        </div>
      )}
    </div>
  );
};
