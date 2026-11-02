import React from 'react';
import { Sparkles, Plus, Upload, Database, RefreshCw } from 'lucide-react';
import { NavTab, StatsResponse } from '../../types';

interface TopHeaderProps {
  activeTab: NavTab;
  stats: StatsResponse | null;
  onNewChat: () => void;
  onOpenUpload: () => void;
  isProcessing: boolean;
}

export const TopHeader: React.FC<TopHeaderProps> = ({
  activeTab,
  stats,
  onNewChat,
  onOpenUpload,
  isProcessing,
}) => {
  const getTabTitle = () => {
    switch (activeTab) {
      case 'overview': return 'Executive Intelligence Overview';
      case 'workspace': return 'AI Workspace & Document Agent';
      case 'documents': return 'Knowledge Base & Document Repository';
      case 'analytics': return 'Telemetry & Model Analytics';
      case 'settings': return 'System & Model Configuration';
    }
  };

  return (
    <header className="h-16 border-b border-slate-800/80 bg-[#070c16]/80 backdrop-blur-xl px-6 flex items-center justify-between z-10">
      <div className="flex items-center gap-3">
        <h1 className="text-base font-semibold text-white tracking-tight">
          {getTabTitle()}
        </h1>
        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          Ready
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Knowledge Base stats pill */}
        {stats && (
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300">
            <Database className="w-3.5 h-3.5 text-blue-400" />
            <span>
              <b className="text-white">{stats.documents_count}</b> docs ·{' '}
              <b className="text-white">{stats.chunks_count}</b> chunks
            </span>
          </div>
        )}

        {/* Upload Action */}
        <button
          onClick={onOpenUpload}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-xs font-medium text-slate-200 transition-all shadow-sm"
        >
          <Upload className="w-3.5 h-3.5 text-slate-400" />
          <span>Upload</span>
        </button>

        {/* New Chat Action */}
        <button
          onClick={onNewChat}
          disabled={isProcessing}
          className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-semibold shadow-md shadow-blue-500/20 transition-all disabled:opacity-50"
          title="Start fresh conversation"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>New Chat</span>
        </button>
      </div>
    </header>
  );
};
