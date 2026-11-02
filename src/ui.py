import html

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* =========================================================
   GLOBAL RESET & THEME
   ========================================================= */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    letter-spacing: -0.01em;
}

.stApp {
    background-color: #070c16;
    background-image: 
        radial-gradient(1200px 600px at 15% -8%, rgba(59, 130, 246, 0.12), transparent 55%),
        radial-gradient(1000px 500px at 85% 5%, rgba(139, 92, 246, 0.10), transparent 50%),
        radial-gradient(900px 700px at 50% 105%, rgba(14, 165, 233, 0.05), transparent 60%);
    background-attachment: fixed;
    color: #e2e8f0;
}

/* Hide default streamlit header decoration */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Top container spacing */
.block-container {
    max-width: 1560px;
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}
::-webkit-scrollbar-track {
    background: rgba(10, 16, 28, 0.5);
}
::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 9999px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}
::-webkit-scrollbar-thumb:hover {
    background: #334155;
}

/* =========================================================
   SIDEBAR STYLING
   ========================================================= */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090e1a 0%, #060a12 100%) !important;
    border-right: 1px solid rgba(30, 41, 59, 0.8) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.25rem;
    padding-left: 1.1rem;
    padding-right: 1.1rem;
}

/* Brand Box */
.brand-container {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 16px 4px;
    margin-bottom: 8px;
    border-bottom: 1px solid rgba(30, 41, 59, 0.7);
}

.brand-logo {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.2);
    flex-shrink: 0;
}

.brand-text-title {
    font-size: 19px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #f8fafc;
    line-height: 1.2;
}

.brand-text-sub {
    font-size: 11px;
    font-weight: 500;
    color: #94a3b8;
    letter-spacing: 0.02em;
    margin-top: 2px;
}

/* Section Title */
.sidebar-section-title {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    margin: 18px 0 10px 2px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Document Item Card */
.doc-item-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(51, 65, 85, 0.5);
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.2s ease;
}
.doc-item-card:hover {
    background: rgba(30, 41, 59, 0.6);
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-1px);
}

.doc-item-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: rgba(59, 130, 246, 0.12);
    border: 1px solid rgba(59, 130, 246, 0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
}

.doc-item-name {
    font-size: 12.5px;
    font-weight: 600;
    color: #e2e8f0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 150px;
}

.doc-item-meta {
    font-size: 11px;
    color: #64748b;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 2px;
}

.doc-item-indexed {
    color: #10b981;
    font-weight: 600;
    font-size: 10.5px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}

/* Sidebar Agent Status Box */
.agent-status-box {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(51, 65, 85, 0.5);
    border-radius: 12px;
    padding: 14px;
    margin-top: 6px;
}

.pulse-beacon {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #10b981;
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    animation: beaconPulse 2s infinite;
    display: inline-block;
}

@keyframes beaconPulse {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
    70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.status-header-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 700;
    color: #10b981;
    margin-bottom: 12px;
}

.status-data-table {
    width: 100%;
    font-size: 11.5px;
}
.status-data-row {
    display: flex;
    justify-content: space-between;
    padding: 5px 0;
    border-bottom: 1px solid rgba(30, 41, 59, 0.6);
}
.status-data-row:last-child {
    border-bottom: none;
}
.status-data-label {
    color: #64748b;
    font-weight: 500;
}
.status-data-val {
    color: #cbd5e1;
    font-weight: 600;
}

/* =========================================================
   TOP HEADER
   ========================================================= */
.top-header-banner {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.4) 100%);
    border: 1px solid rgba(51, 65, 85, 0.6);
    border-radius: 16px;
    padding: 16px 22px;
    margin-bottom: 18px;
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
}

.top-header-title-group {
    display: flex;
    align-items: center;
    gap: 14px;
}

.top-header-icon {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.35);
}

.top-header-main {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 8px;
}

.top-header-sub {
    font-size: 12.5px;
    color: #94a3b8;
    margin-top: 2px;
}

.top-header-badges {
    display: flex;
    align-items: center;
    gap: 10px;
}

.pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(51, 65, 85, 0.8);
    border-radius: 9999px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    color: #cbd5e1;
}
.pill-badge-online {
    background: rgba(16, 185, 129, 0.08);
    border-color: rgba(16, 185, 129, 0.3);
    color: #34d399;
}

/* =========================================================
   RIGHT PANEL: ACTIVITY, PIPELINE, RETRIEVAL, SOURCES
   ========================================================= */
.right-panel-card {
    background: rgba(13, 20, 35, 0.75);
    border: 1px solid rgba(40, 53, 73, 0.7);
    border-radius: 14px;
    padding: 16px 16px 14px 16px;
    margin-bottom: 14px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.right-card-header {
    font-size: 10.5px;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 7px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(30, 41, 59, 0.6);
}

.right-card-header-icon {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    background: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
}

/* Activity Steps */
.activity-step-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0;
    font-size: 12px;
    color: #94a3b8;
}
.activity-step-done {
    color: #e2e8f0;
}
.activity-check-box {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.35);
    color: #10b981;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 700;
    flex-shrink: 0;
}
.activity-idle-box {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(51, 65, 85, 0.5);
    color: #475569;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 9px;
    flex-shrink: 0;
}
.activity-step-label {
    flex-grow: 1;
}
.activity-step-badge {
    font-size: 10px;
    color: #64748b;
    background: rgba(30, 41, 59, 0.5);
    padding: 2px 7px;
    border-radius: 6px;
}
.activity-step-badge.done {
    color: #34d399;
    background: rgba(16, 185, 129, 0.1);
}

/* Pipeline Flow Nodes */
.pipeline-container {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.pipeline-node {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(40, 53, 73, 0.6);
    border-radius: 8px;
    padding: 7px 11px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11.5px;
    font-weight: 600;
    color: #cbd5e1;
    transition: border-color 0.2s;
}
.pipeline-node:hover {
    border-color: rgba(99, 102, 241, 0.4);
}
.pipeline-node-icon {
    font-size: 13px;
    margin-right: 8px;
}
.pipeline-arrow {
    text-align: center;
    font-size: 10px;
    color: #475569;
    line-height: 1;
    margin: -1px 0;
}

/* Retrieval Specs Grid */
.retrieval-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}
.retrieval-cell {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(40, 53, 73, 0.6);
    border-radius: 8px;
    padding: 8px 10px;
}
.retrieval-label {
    font-size: 9.5px;
    font-weight: 600;
    text-transform: uppercase;
    color: #64748b;
    letter-spacing: 0.05em;
}
.retrieval-val {
    font-size: 12px;
    font-weight: 700;
    color: #e2e8f0;
    margin-top: 2px;
}

/* Sources List */
.source-tag-item {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-radius: 8px;
    padding: 8px 12px;
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #93c5fd;
    font-weight: 500;
}
.source-empty-hint {
    font-size: 11.5px;
    color: #64748b;
    text-align: center;
    padding: 14px 10px;
    border: 1px dashed rgba(40, 53, 73, 0.8);
    border-radius: 8px;
    background: rgba(10, 15, 26, 0.3);
}

/* =========================================================
   CHAT MESSAGES
   ========================================================= */
.chat-scroll-container {
    padding-bottom: 20px;
}

.msg-user-bubble {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(20, 30, 46, 0.7) 100%);
    border: 1px solid rgba(71, 85, 105, 0.5);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    margin: 12px 0 12px auto;
    max-width: 85%;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.msg-user-header {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #60a5fa;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.msg-user-text {
    font-size: 14px;
    color: #f1f5f9;
    line-height: 1.6;
    word-break: break-word;
}

.msg-agent-card {
    background: linear-gradient(135deg, rgba(13, 20, 35, 0.9) 0%, rgba(10, 16, 28, 0.9) 100%);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-left: 3.5px solid #6366f1;
    border-radius: 16px 16px 16px 4px;
    padding: 18px 20px;
    margin: 12px 0 16px 0;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.3);
}

.msg-agent-header {
    font-size: 11px;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #a5b4fc;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.agent-badge-icon {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    color: white;
}

.msg-agent-text {
    font-size: 14.5px;
    color: #e2e8f0;
    line-height: 1.7;
    word-break: break-word;
}

/* Welcome / Empty State Screen */
.welcome-hero-box {
    text-align: center;
    padding: 48px 20px 32px 20px;
}

.welcome-floating-badge {
    width: 72px;
    height: 72px;
    margin: 0 auto 20px auto;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
    border: 1px solid rgba(99, 102, 241, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    box-shadow: 0 12px 36px rgba(99, 102, 241, 0.25);
    animation: floatGently 4s ease-in-out infinite;
}

@keyframes floatGently {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

.welcome-headline {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #f8fafc;
    margin-bottom: 10px;
}

.welcome-description {
    font-size: 13.5px;
    color: #94a3b8;
    max-width: 480px;
    margin: 0 auto 26px auto;
    line-height: 1.6;
}

/* =========================================================
   STREAMLIT NATIVE COMPONENT OVERRIDES
   ========================================================= */
/* Chat Input */
[data-testid="stChatInput"] {
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 14px !important;
    background: rgba(13, 20, 35, 0.95) !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
}
[data-testid="stChatInput"] textarea {
    color: #f1f5f9 !important;
    background: transparent !important;
    font-size: 14px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    color: white !important;
    border-radius: 9px !important;
}

/* Suggestion Buttons */
.stButton > button {
    border-radius: 10px !important;
    border: 1px solid rgba(51, 65, 85, 0.6) !important;
    background: rgba(15, 23, 42, 0.7) !important;
    color: #cbd5e1 !important;
    font-weight: 550 !important;
    font-size: 12.5px !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
    padding: 10px 14px !important;
}
.stButton > button:hover {
    border-color: #6366f1 !important;
    background: rgba(30, 41, 59, 0.9) !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2) !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: rgba(13, 20, 35, 0.6) !important;
    border: 1px dashed rgba(51, 65, 85, 0.8) !important;
    border-radius: 12px !important;
    padding: 6px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #3b82f6 !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: rgba(15, 23, 42, 0.3) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploaderDropzone"] small {
    color: #64748b !important;
}

/* Status Widget */
[data-testid="stStatusWidget"] {
    background: rgba(13, 20, 35, 0.9) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}

/* Responsive Media Queries */
@media (max-width: 1024px) {
    .top-header-banner {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }
}
</style>
"""


def render_brand_sidebar():
    return """
    <div class="brand-container">
        <div class="brand-logo">✦</div>
        <div>
            <div class="brand-text-title">NEXA AI</div>
            <div class="brand-text-sub">Company Document Agent</div>
        </div>
    </div>
    """


def render_doc_card(name: str, size_mb: float):
    safe_name = html.escape(name)
    size_str = f"{size_mb:.1f} MB" if size_mb >= 0.1 else f"{size_mb * 1024:.0f} KB"
    return f"""
    <div class="doc-item-card">
        <div class="doc-item-icon">📄</div>
        <div style="min-width: 0; flex-grow: 1;">
            <div class="doc-item-name" title="{safe_name}">{safe_name}</div>
            <div class="doc-item-meta">
                <span>{size_str}</span>
                <span>•</span>
                <span class="doc-item-indexed">✓ Indexed</span>
            </div>
        </div>
    </div>
    """


def render_status_card(model="Gemini 2.5 Flash", vector_store="ChromaDB", embeddings="MiniLM"):
    return f"""
    <div class="agent-status-box">
        <div class="status-header-row">
            <span class="pulse-beacon"></span>
            <span>Agent Online</span>
        </div>
        <div class="status-data-table">
            <div class="status-data-row">
                <span class="status-data-label">Model</span>
                <span class="status-data-val">{html.escape(model)}</span>
            </div>
            <div class="status-data-row">
                <span class="status-data-label">Vector Store</span>
                <span class="status-data-val">{html.escape(vector_store)}</span>
            </div>
            <div class="status-data-row">
                <span class="status-data-label">Embeddings</span>
                <span class="status-data-val">{html.escape(embeddings)}</span>
            </div>
        </div>
    </div>
    """


def render_top_header(doc_count: int, chunk_count: int):
    doc_label = f"{doc_count} document{'s' if doc_count != 1 else ''}"
    chunk_label = f"{chunk_count} chunk{'s' if chunk_count != 1 else ''}"
    return f"""
    <div class="top-header-banner">
        <div class="top-header-title-group">
            <div class="top-header-icon">✦</div>
            <div>
                <div class="top-header-main">
                    NEXA AI AGENT
                </div>
                <div class="top-header-sub">
                    Company Document Intelligence &nbsp;•&nbsp; Grounded AI workspace
                </div>
            </div>
        </div>
        <div class="top-header-badges">
            <div class="pill-badge">
                <span>📚</span>
                <span>{doc_label} ({chunk_label})</span>
            </div>
            <div class="pill-badge pill-badge-online">
                <span class="pulse-beacon"></span>
                <span>Agent Online</span>
            </div>
        </div>
    </div>
    """


def render_activity_panel(activity: dict):
    steps = [
        ("received", "Question received"),
        ("searched", "Searching company documents"),
        ("retrieved", "Retrieved relevant information"),
        ("context", "Context prepared"),
        ("generated", "Gemini response generated"),
    ]
    rows = []
    for key, label in steps:
        is_done = activity.get(key, False)
        if is_done:
            rows.append(f"""
            <div class="activity-step-row activity-step-done">
                <div class="activity-check-box">✓</div>
                <div class="activity-step-label">{label}</div>
                <span class="activity-step-badge done">done</span>
            </div>
            """)
        else:
            rows.append(f"""
            <div class="activity-step-row">
                <div class="activity-idle-box">•</div>
                <div class="activity-step-label">{label}</div>
                <span class="activity-step-badge">idle</span>
            </div>
            """)
    return f"""
    <div class="right-panel-card">
        <div class="right-card-header">
            <span class="right-card-header-icon">⚡</span>
            <span>AGENT ACTIVITY</span>
        </div>
        {"".join(rows)}
    </div>
    """


def render_pipeline_card():
    stages = [
        ("💬", "User Question"),
        ("🤖", "AI Agent"),
        ("🔍", "Document Search Tool"),
        ("🗄️", "ChromaDB"),
        ("📄", "Relevant Context"),
        ("✨", "Gemini"),
        ("🎯", "Grounded Answer"),
    ]
    nodes_html = []
    for i, (ico, name) in enumerate(stages):
        nodes_html.append(f"""
        <div class="pipeline-node">
            <div style="display:flex;align-items:center;">
                <span class="pipeline-node-icon">{ico}</span>
                <span>{name}</span>
            </div>
            <span style="font-size:9.5px;color:#64748b;font-weight:700;">#{i+1}</span>
        </div>
        """)
        if i < len(stages) - 1:
            nodes_html.append('<div class="pipeline-arrow">↓</div>')

    return f"""
    <div class="right-panel-card">
        <div class="right-card-header">
            <span class="right-card-header-icon">🔄</span>
            <span>RAG PIPELINE</span>
        </div>
        <div class="pipeline-container">
            {"".join(nodes_html)}
        </div>
    </div>
    """


def render_retrieval_card(chunk_count: int, top_k: int = 3):
    return f"""
    <div class="right-panel-card">
        <div class="right-card-header">
            <span class="right-card-header-icon">⚙️</span>
            <span>RETRIEVAL</span>
        </div>
        <div class="retrieval-grid">
            <div class="retrieval-cell">
                <div class="retrieval-label">Vector Store</div>
                <div class="retrieval-val">ChromaDB</div>
            </div>
            <div class="retrieval-cell">
                <div class="retrieval-label">Embedding</div>
                <div class="retrieval-val">MiniLM</div>
            </div>
            <div class="retrieval-cell">
                <div class="retrieval-label">Top K</div>
                <div class="retrieval-val">{top_k} Chunks</div>
            </div>
            <div class="retrieval-cell">
                <div class="retrieval-label">Indexed Chunks</div>
                <div class="retrieval-val">{chunk_count} Total</div>
            </div>
        </div>
    </div>
    """


def render_sources_card(sources: list):
    if sources:
        items = "".join([
            f"""
            <div class="source-tag-item">
                <span>📄</span>
                <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                    {html.escape(s)}
                </span>
            </div>
            """
            for s in sources
        ])
    else:
        items = '<div class="source-empty-hint">No sources queried yet. Ask a question to view retrieved document sources.</div>'

    return f"""
    <div class="right-panel-card">
        <div class="right-card-header">
            <span class="right-card-header-icon">📚</span>
            <span>SOURCES</span>
        </div>
        {items}
    </div>
    """


def render_welcome_screen():
    return """
    <div class="welcome-hero-box">
        <div class="welcome-floating-badge">✦</div>
        <div class="welcome-headline">How can I help you?</div>
        <div class="welcome-description">
            Ask questions about your company's documents and get grounded answers instantly.
        </div>
    </div>
    """


def render_user_message(content: str):
    safe_content = html.escape(content)
    return f"""
    <div class="msg-user-bubble">
        <div class="msg-user-header">
            <span>👤</span>
            <span>You</span>
        </div>
        <div class="msg-user-text">{safe_content}</div>
    </div>
    """


def render_agent_message(content: str):
    # Convert newlines to breaks or preserve paragraphs
    safe_content = html.escape(content).replace("\n", "<br/>")
    return f"""
    <div class="msg-agent-card">
        <div class="msg-agent-header">
            <div class="agent-badge-icon">🤖</div>
            <span>NEXA AI</span>
        </div>
        <div class="msg-agent-text">{safe_content}</div>
    </div>
    """
