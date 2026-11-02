import React from 'react';
import { 
  Bot, 
  Files, 
  BarChart3, 
  Settings, 
  LayoutDashboard, 
  Upload, 
  ChevronLeft, 
  ChevronRight,
  Sparkles,
  FileText,
  Layers,
  Database
} from 'lucide-react';
import { NavTab, DocumentItem, StatsResponse } from '../../types';

interface SidebarProps {
  activeTab: NavTab;
  setActiveTab: (tab: NavTab) => void;
  collapsed: boolean;
  setCollapsed: (collapsed: boolean) => void;
  documents: DocumentItem[];
  stats: StatsResponse | null;
  onOpenUpload: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  collapsed,
  setCollapsed,
  documents,
  stats,
  onOpenUpload,
}) => {
  const navItems = [
    { id: 'overview' as NavTab, label: 'Overview', icon: LayoutDashboard },
    { id: 'workspace' as NavTab, label: 'AI Workspace', icon: Bot },
    { id: 'documents' as NavTab, label: 'Documents', icon: Files, badge: documents.length },
    { id: 'analytics' as NavTab, label: 'Analytics', icon: BarChart3 },
    { id: 'settings' as NavTab, label: 'Settings', icon: Settings },
  ];

  return (
    <aside 
      className={`relative flex flex-col border-r border-slate-800/80 bg-[#090e1a]/95 backdrop-blur-xl transition-all duration-300 z-20 ${
        collapsed ? 'w-20' : 'w-72'
      }`}
    >
      {/* Brand Header */}
      <div className="flex items-center justify-between px-4 py-5 border-b border-slate-800/80">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-violet-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/25 shrink-0 border border-white/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          {!collapsed && (
            <div className="flex flex-col min-w-0">
              <span className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
                NEXA AI
                <span className="text-[10px] uppercase font-bold tracking-widest px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  v2.0
                </span>
              </span>
              <span className="text-[11px] text-slate-400 truncate">Enterprise Intelligence</span>
            </div>
          )}
        </div>

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Main Navigation */}
      <div className="px-3 py-4 flex-1 overflow-y-auto space-y-6">
        <div>
          {!collapsed && (
            <div className="px-3 mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-500">
              Workspace
            </div>
          )}
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-600/20 to-indigo-600/10 text-white border border-blue-500/30 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                  } ${collapsed ? 'justify-center' : ''}`}
                  title={collapsed ? item.label : undefined}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                  {!collapsed && (
                    <span className="flex-1 text-left truncate">{item.label}</span>
                  )}
                  {!collapsed && item.badge !== undefined && (
                    <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Documents Section */}
        {!collapsed && (
          <div>
            <div className="flex items-center justify-between px-3 mb-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                Knowledge Docs ({documents.length})
              </span>
              <button
                onClick={onOpenUpload}
                className="text-[11px] font-medium text-blue-400 hover:text-blue-300 flex items-center gap-1 transition-colors"
              >
                <Upload className="w-3 h-3" />
                Upload
              </button>
            </div>

            <div className="space-y-1.5 max-h-44 overflow-y-auto pr-1">
              {documents.length === 0 ? (
                <div className="p-3 text-center text-xs text-slate-500 border border-dashed border-slate-800 rounded-xl">
                  No documents indexed yet.
                </div>
              ) : (
                documents.slice(0, 5).map((doc) => (
                  <div
                    key={doc.id}
                    className="flex items-center gap-2.5 p-2 rounded-lg bg-slate-900/50 border border-slate-800/60 hover:border-slate-700 transition-colors"
                  >
                    <div className="w-7 h-7 rounded-md bg-blue-500/10 border border-blue-500/20 flex items-center justify-center shrink-0">
                      <FileText className="w-3.5 h-3.5 text-blue-400" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="text-xs font-medium text-slate-200 truncate">{doc.name}</div>
                      <div className="text-[10px] text-slate-500 flex items-center gap-1.5">
                        <span>{doc.size_mb} MB</span>
                        <span>•</span>
                        <span className="text-emerald-400 font-medium">Indexed</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>

      {/* Agent Status Footer */}
      <div className="p-3 border-t border-slate-800/80 bg-slate-950/40">
        <div className={`p-3 rounded-xl bg-slate-900/80 border border-slate-800 ${collapsed ? 'text-center' : ''}`}>
          <div className="flex items-center gap-2 mb-2">
            <div className="relative flex h-2.5 w-2.5 shrink-0">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </div>
            {!collapsed && (
              <span className="text-xs font-semibold text-emerald-400">Agent Online</span>
            )}
          </div>

          {!collapsed && (
            <div className="space-y-1.5 text-[11px] text-slate-400">
              <div className="flex justify-between items-center py-0.5 border-b border-slate-800/60">
                <span className="text-slate-500 flex items-center gap-1">
                  <Bot className="w-3 h-3" /> Model
                </span>
                <span className="font-medium text-slate-300">Gemini 2.5 Flash</span>
              </div>
              <div className="flex justify-between items-center py-0.5 border-b border-slate-800/60">
                <span className="text-slate-500 flex items-center gap-1">
                  <Database className="w-3 h-3" /> Vector DB
                </span>
                <span className="font-medium text-slate-300">ChromaDB</span>
              </div>
              <div className="flex justify-between items-center py-0.5">
                <span className="text-slate-500 flex items-center gap-1">
                  <Layers className="w-3 h-3" /> Embeddings
                </span>
                <span className="font-medium text-slate-300">MiniLM L6</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};
