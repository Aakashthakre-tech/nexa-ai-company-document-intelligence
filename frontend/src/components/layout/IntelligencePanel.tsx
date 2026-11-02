import React from 'react';
import { AgentActivityCard } from '../intelligence/AgentActivityCard';
import { ConfidenceCard } from '../intelligence/ConfidenceCard';
import { SourcesCard } from '../intelligence/SourcesCard';
import { RagPipelineCard } from '../intelligence/RagPipelineCard';
import { SystemSpecsCard } from '../intelligence/SystemSpecsCard';
import { ActivityStep, SourceItem, StatsResponse } from '../../types';

interface IntelligencePanelProps {
  activity: ActivityStep[];
  isProcessing: boolean;
  confidence?: number;
  evidenceStrength?: 'HIGH' | 'MEDIUM' | 'LOW';
  isLowConfidence?: boolean;
  sources: SourceItem[];
  stats: StatsResponse | null;
}

export const IntelligencePanel: React.FC<IntelligencePanelProps> = ({
  activity,
  isProcessing,
  confidence,
  evidenceStrength,
  isLowConfidence,
  sources,
  stats,
}) => {
  return (
    <aside className="w-80 lg:w-96 border-l border-slate-800/80 bg-[#070c16]/70 backdrop-blur-xl p-4 overflow-y-auto space-y-4 shrink-0 hidden xl:block">
      <AgentActivityCard activity={activity} isProcessing={isProcessing} />
      <ConfidenceCard
        confidence={confidence}
        evidenceStrength={evidenceStrength}
        isLowConfidence={isLowConfidence}
      />
      <SourcesCard sources={sources} />
      <RagPipelineCard />
      <SystemSpecsCard stats={stats} />
    </aside>
  );
};
