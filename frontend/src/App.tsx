import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { TopHeader } from './components/layout/TopHeader';
import { IntelligencePanel } from './components/layout/IntelligencePanel';
import { ChatWorkspace } from './components/chat/ChatWorkspace';
import { DocumentManager } from './components/documents/DocumentManager';
import { UploadModal } from './components/documents/UploadModal';
import { OverviewView } from './components/overview/OverviewView';
import { AnalyticsView } from './components/analytics/AnalyticsView';
import { SettingsView } from './components/settings/SettingsView';
import { 
  NavTab, 
  Message, 
  DocumentItem, 
  StatsResponse, 
  ActivityStep, 
  SourceItem 
} from './types';
import { sendMessage, getDocuments, getStats, resetSession } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState<NavTab>('workspace');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [uploadModalOpen, setUploadModalOpen] = useState(false);

  // Application Data States
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);

  // Intelligence Panel States
  const [latestActivity, setLatestActivity] = useState<ActivityStep[]>([
    { id: 'received', label: 'Question received', status: 'completed' },
    { id: 'searching', label: 'Searching knowledge', status: 'completed' },
    { id: 'retrieving', label: 'Retrieving relevant context', status: 'completed' },
    { id: 'analyzing', label: 'Analyzing evidence', status: 'completed' },
    { id: 'generating', label: 'Generating response', status: 'completed' },
  ]);
  const [latestSources, setLatestSources] = useState<SourceItem[]>([]);
  const [latestConfidence, setLatestConfidence] = useState<number>(0.92);
  const [latestEvidenceStrength, setLatestEvidenceStrength] = useState<'HIGH' | 'MEDIUM' | 'LOW'>('HIGH');
  const [latestIsLowConfidence, setLatestIsLowConfidence] = useState<boolean>(false);

  // Load documents and system stats
  const refreshData = async () => {
    try {
      const [docsRes, statsRes] = await Promise.all([
        getDocuments(),
        getStats().catch(() => null),
      ]);
      setDocuments(docsRes.documents || []);
      if (statsRes) setStats(statsRes);
    } catch (err) {
      console.error('Failed to load initial data:', err);
    }
  };

  useEffect(() => {
    refreshData();
  }, []);

  // Handle Chat Queries
  const handleSendMessage = async (question: string) => {
    if (!question.trim() || isProcessing) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: question,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsProcessing(true);

    // Initial processing activity
    setLatestActivity([
      { id: 'received', label: 'Question received', status: 'completed', detail: question.slice(0, 50) },
      { id: 'searching', label: 'Searching knowledge', status: 'running' },
      { id: 'retrieving', label: 'Retrieving relevant context', status: 'pending' },
      { id: 'analyzing', label: 'Analyzing evidence', status: 'pending' },
      { id: 'generating', label: 'Generating response', status: 'pending' },
    ]);

    try {
      const res = await sendMessage(question, sessionId);

      if (res.session_id) {
        setSessionId(res.session_id);
      }

      setLatestActivity(res.activity || []);
      setLatestSources(res.sources || []);
      setLatestConfidence(res.confidence);
      setLatestEvidenceStrength(res.evidence_strength);
      setLatestIsLowConfidence(res.is_low_confidence);

      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: res.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        sources: res.sources,
        confidence: res.confidence,
        evidence_strength: res.evidence_strength,
        is_low_confidence: res.is_low_confidence,
        status: res.status as 'success' | 'error',
      };

      setMessages((prev) => [...prev, agentMessage]);
    } catch (err: any) {
      console.error('Agent call error:', err);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: err.message || 'Gemini is temporarily unavailable. Please try again.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        confidence: 0,
        evidence_strength: 'LOW',
        is_low_confidence: true,
        status: 'error',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleNewChat = async () => {
    setMessages([]);
    setLatestSources([]);
    try {
      const res = await resetSession(sessionId);
      setSessionId(res.session_id);
    } catch (err) {
      console.error('Failed to reset session:', err);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#070c16] text-[#e2e8f0]">
      {/* Left Collapsible Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
        documents={documents}
        stats={stats}
        onOpenUpload={() => setUploadModalOpen(true)}
      />

      {/* Main Workspace Column */}
      <div className="flex-1 flex flex-col h-full min-w-0 overflow-hidden">
        {/* Top Header */}
        <TopHeader
          activeTab={activeTab}
          stats={stats}
          onNewChat={handleNewChat}
          onOpenUpload={() => setUploadModalOpen(true)}
          isProcessing={isProcessing}
        />

        {/* Dynamic Content Views */}
        <div className="flex-1 flex h-[calc(100vh-4rem)] overflow-hidden">
          {activeTab === 'workspace' && (
            <>
              <ChatWorkspace
                messages={messages}
                onSendMessage={handleSendMessage}
                onOpenUpload={() => setUploadModalOpen(true)}
                isProcessing={isProcessing}
              />
              <IntelligencePanel
                activity={latestActivity}
                isProcessing={isProcessing}
                confidence={latestConfidence}
                evidenceStrength={latestEvidenceStrength}
                isLowConfidence={latestIsLowConfidence}
                sources={latestSources}
                stats={stats}
              />
            </>
          )}

          {activeTab === 'documents' && (
            <DocumentManager
              documents={documents}
              totalChunks={stats?.chunks_count || 14}
              onRefresh={refreshData}
              onOpenUpload={() => setUploadModalOpen(true)}
            />
          )}

          {activeTab === 'overview' && (
            <OverviewView
              documents={documents}
              stats={stats}
              onNavigateToWorkspace={() => setActiveTab('workspace')}
              onNavigateToDocuments={() => setActiveTab('documents')}
            />
          )}

          {activeTab === 'analytics' && (
            <AnalyticsView stats={stats} />
          )}

          {activeTab === 'settings' && (
            <SettingsView onSessionReset={handleNewChat} />
          )}
        </div>
      </div>

      {/* Document Upload Modal */}
      <UploadModal
        isOpen={uploadModalOpen}
        onClose={() => setUploadModalOpen(false)}
        onSuccess={refreshData}
      />
    </div>
  );
}

export default App;
