import React from 'react';
import { CheckCircle2, Clock, Loader2, Zap } from 'lucide-react';
import { ActivityStep } from '../../types';

interface AgentActivityCardProps {
  activity: ActivityStep[];
  isProcessing: boolean;
}

export const AgentActivityCard: React.FC<AgentActivityCardProps> = ({
  activity,
  isProcessing,
}) => {
  const defaultSteps: ActivityStep[] = [
    { id: 'received', label: 'Question received', status: 'completed' },
    { id: 'searching', label: 'Searching knowledge', status: 'completed' },
    { id: 'retrieving', label: 'Retrieving relevant context', status: 'completed' },
    { id: 'analyzing', label: 'Analyzing evidence', status: 'completed' },
    { id: 'generating', label: 'Generating response', status: 'completed' },
  ];

  const steps = activity && activity.length > 0 ? activity : defaultSteps;

  return (
    <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800/80">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-lg bg-blue-500/10 border border-blue-500/25 flex items-center justify-center text-blue-400">
            <Zap className="w-3.5 h-3.5" />
          </div>
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Agent Activity
          </span>
        </div>
        {isProcessing && (
          <span className="flex items-center gap-1.5 text-[11px] text-blue-400 font-medium">
            <Loader2 className="w-3 h-3 animate-spin" />
            Executing
          </span>
        )}
      </div>

      <div className="space-y-2.5">
        {steps.map((step) => {
          const isDone = step.status === 'completed';
          const isRunning = step.status === 'running';

          return (
            <div key={step.id} className="flex items-center gap-2.5 text-xs">
              {isDone ? (
                <div className="w-5 h-5 rounded-full bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                </div>
              ) : isRunning ? (
                <div className="w-5 h-5 rounded-full bg-blue-500/15 border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0">
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                </div>
              ) : (
                <div className="w-5 h-5 rounded-full bg-slate-800/80 border border-slate-700/60 flex items-center justify-center text-slate-500 shrink-0">
                  <Clock className="w-3 h-3" />
                </div>
              )}

              <div className="flex-1 min-w-0">
                <span className={`font-medium truncate block ${isDone ? 'text-slate-200' : isRunning ? 'text-blue-300' : 'text-slate-500'}`}>
                  {step.label}
                </span>
                {step.detail && isDone && (
                  <span className="text-[10px] text-slate-500 truncate block">
                    {step.detail}
                  </span>
                )}
              </div>

              <span className={`text-[10px] font-semibold px-2 py-0.5 rounded ${
                isDone 
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                  : isRunning 
                  ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' 
                  : 'bg-slate-800 text-slate-500'
              }`}>
                {step.status}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
