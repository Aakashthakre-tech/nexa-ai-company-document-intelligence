import os
import streamlit as st
from pypdf import PdfReader

from src.document_loader import load_documents, chunk_text
from src.vector_store import add_documents, search_documents, collection
from src.agent import generate_answer
from src.ui import (
    CSS,
    render_brand_sidebar,
    render_doc_card,
    render_status_card,
    render_top_header,
    render_activity_panel,
    render_pipeline_card,
    render_retrieval_card,
    render_sources_card,
    render_welcome_screen,
    render_user_message,
    render_agent_message,
)

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Nexa AI Agent — Company Document Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Enterprise Modern AI SaaS Styling
st.markdown(CSS, unsafe_allow_html=True)

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_activity" not in st.session_state:
    st.session_state.agent_activity = {
        "received": False,
        "searched": False,
        "retrieved": False,
        "context": False,
        "generated": False,
    }

if "sources" not in st.session_state:
    st.session_state.sources = []

if "active_view" not in st.session_state:
    st.session_state.active_view = "chat"

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# =========================================================
# HELPER: GET LOCAL DOCUMENTS
# =========================================================
def get_local_documents():
    """Retrieve actual PDF documents from data/documents."""
    docs = []
    folder = "data/documents"
    if os.path.exists(folder):
        for fname in sorted(os.listdir(folder)):
            if fname.lower().endswith(".pdf"):
                fpath = os.path.join(folder, fname)
                try:
                    size_mb = os.path.getsize(fpath) / (1024 * 1024)
                except OSError:
                    size_mb = 0.0
                docs.append({"name": fname, "size_mb": size_mb, "path": fpath})
    return docs


# =========================================================
# AGENT EXECUTION PIPELINE
# =========================================================
def run_agent_pipeline(question: str):
    """
    Executes the grounded agent workflow:
    1. Records question receipt
    2. Performs document retrieval in ChromaDB to capture sources
    3. Calls the existing Gemini 2.5 Flash agent tool loop
    4. Records step completions and real retrieved sources
    """
    activity = {
        "received": True,
        "searched": True,
        "retrieved": False,
        "context": False,
        "generated": False,
    }

    # Step 1: Query ChromaDB to extract actual source metadata for the UI
    search_results = search_documents(question, top_k=3)
    sources = []
    if search_results and "metadatas" in search_results and search_results["metadatas"]:
        first_group = search_results["metadatas"][0]
        if first_group:
            for md in first_group:
                if md and "source" in md:
                    s_name = md["source"]
                    if s_name not in sources:
                        sources.append(s_name)

    activity["retrieved"] = True
    activity["context"] = True

    # Step 2: Generate response using the existing Gemini agent
    answer = generate_answer(question)
    activity["generated"] = True

    return answer, sources, activity


# =========================================================
# SIDEBAR NAVIGATION & CONTROLS
# =========================================================
with st.sidebar:
    st.markdown(render_brand_sidebar(), unsafe_allow_html=True)

    # Navigation Tabs
    st.markdown('<div class="sidebar-section-title"><span>🧭</span> NAVIGATION</div>', unsafe_allow_html=True)
    nav_c1, nav_c2, nav_c3 = st.columns(3)
    with nav_c1:
        if st.button("💬 Chat", use_container_width=True, key="btn_nav_chat"):
            st.session_state.active_view = "chat"
            st.rerun()
    with nav_c2:
        if st.button("📄 Docs", use_container_width=True, key="btn_nav_docs"):
            st.session_state.active_view = "documents"
            st.rerun()
    with nav_c3:
        if st.button("⚙️ Stack", use_container_width=True, key="btn_nav_stack"):
            st.session_state.active_view = "settings"
            st.rerun()

    # Documents Section
    st.markdown('<div class="sidebar-section-title"><span>📂</span> DOCUMENTS</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Upload PDF files to index them directly into ChromaDB vector store."
    )

    if uploaded_files:
        os.makedirs("data/documents", exist_ok=True)
        indexed_count = 0
        with st.spinner("Processing & indexing uploaded PDF(s)..."):
            for uploaded_file in uploaded_files:
                target_path = os.path.join("data/documents", uploaded_file.name)
                with open(target_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Extract and chunk text
                try:
                    reader = PdfReader(target_path)
                    text = ""
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"

                    if text.strip():
                        chunks = chunk_text(text)
                        if chunks:
                            try:
                                add_documents(chunks, uploaded_file.name)
                                indexed_count += 1
                            except Exception:
                                # Chunks may already exist in collection
                                pass
                except Exception as e:
                    st.error(f"Error indexing {uploaded_file.name}: {e}")

        st.toast(f"Indexed {len(uploaded_files)} document(s) successfully!", icon="📄")
        st.rerun()

    # Dynamic document listing from real files
    doc_items = get_local_documents()
    if doc_items:
        for doc in doc_items:
            st.markdown(render_doc_card(doc["name"], doc["size_mb"]), unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="font-size:11.5px;color:#64748b;padding:4px 2px;">No documents found in data/documents.</div>',
            unsafe_allow_html=True
        )

    # Agent Status Section
    st.markdown('<div class="sidebar-section-title"><span>⚡</span> AGENT STATUS</div>', unsafe_allow_html=True)
    st.markdown(
        render_status_card(model="Gemini 2.5 Flash", vector_store="ChromaDB", embeddings="MiniLM"),
        unsafe_allow_html=True
    )

    # Reset chat session button
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Reset Conversation", use_container_width=True, help="Clear chat history and reset agent activity"):
        st.session_state.messages = []
        st.session_state.sources = []
        st.session_state.agent_activity = {
            "received": False,
            "searched": False,
            "retrieved": False,
            "context": False,
            "generated": False,
        }
        st.toast("Conversation memory reset.", icon="🧹")
        st.rerun()


# =========================================================
# TOP HEADER BAR
# =========================================================
try:
    total_chunks = collection.count()
except Exception:
    total_chunks = 0

doc_items = get_local_documents()
st.markdown(render_top_header(len(doc_items), total_chunks), unsafe_allow_html=True)


# =========================================================
# VIEW: DOCUMENTS DIRECTORY
# =========================================================
if st.session_state.active_view == "documents":
    st.markdown("### 📄 Indexed Company Documents")
    st.caption("All company documents extracted, chunked, and embedded in ChromaDB for grounded retrieval.")

    docs = load_documents()
    if docs:
        col_a, col_b = st.columns(2)
        for idx, doc in enumerate(docs):
            target_col = col_a if idx % 2 == 0 else col_b
            with target_col:
                fpath = os.path.join("data/documents", doc["source"])
                try:
                    size_mb = os.path.getsize(fpath) / (1024 * 1024)
                except OSError:
                    size_mb = 0.0
                st.markdown(render_doc_card(doc["source"], size_mb), unsafe_allow_html=True)
                char_count = len(doc["text"])
                st.markdown(
                    f"<div style='font-size:11.5px;color:#94a3b8;margin:-4px 0 14px 4px;'>"
                    f"Extraction: <b>{char_count:,}</b> characters extracted & chunked</div>",
                    unsafe_allow_html=True
                )
    else:
        st.info("No documents currently indexed. Drop a PDF into the sidebar to start.")

    st.stop()


# =========================================================
# VIEW: SYSTEM SETTINGS
# =========================================================
if st.session_state.active_view == "settings":
    st.markdown("### ⚙️ Nexa AI Agent Stack Configuration")
    st.caption("Enterprise RAG architecture details and model parameters.")

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown("""
        <div class="right-panel-card">
            <div class="right-card-header">
                <span class="right-card-header-icon">🧠</span>
                <span>LANGUAGE MODEL</span>
            </div>
            <div class="retrieval-grid">
                <div class="retrieval-cell">
                    <div class="retrieval-label">Foundation Model</div>
                    <div class="retrieval-val">Gemini 2.5 Flash</div>
                </div>
                <div class="retrieval-cell">
                    <div class="retrieval-label">Agent Mode</div>
                    <div class="retrieval-val">Tool-Calling RAG</div>
                </div>
                <div class="retrieval-cell">
                    <div class="retrieval-label">Tool Registered</div>
                    <div class="retrieval-val">search_company_docs</div>
                </div>
                <div class="retrieval-cell">
                    <div class="retrieval-label">Conversation Memory</div>
                    <div class="retrieval-val">Active (Stateful)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sc2:
        st.markdown("""
        <div class="right-panel-card">
            <div class="right-card-header">
                <span class="right-card-header-icon">🗄️</span>
                <span>VECTOR DATABASE</span>
            </div>
            <div class="retrieval-grid">
                <div class="retrieval-cell">
                    <div class="retrieval-label">Engine</div>
                    <div class="retrieval-val">ChromaDB</div>
                </div>
                <div class="retrieval-cell">
                    <div class="retrieval-label">Persistence</div>
                    <div class="retrieval-val">./chroma_db</div>
                </div>
                <div class="retrieval-cell">
                    <div class="retrieval-label">Embeddings Model</div>
                    <div class="retrieval-val">all-MiniLM-L6-v2</div>
                </div>
                <div class="retrieval-cell">
                    <div class="retrieval-label">Dimension</div>
                    <div class="retrieval-val">384-d vectors</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sc3:
        st.markdown("""
        <div class="right-panel-card">
            <div class="right-card-header">
                <span class="right-card-header-icon">⚙️</span>
                <span>RETRIEVAL STRATEGY</span>
            </div>
            <div class="retrieval-grid">
                <div class="retrieval-cell">
                    <div class="retrieval-label">Top K Chunks</div>
                    <div class="retrieval-val">3 Chunks</div>
                </div>
                <div class="retrieval-cell">
                    <div class="retrieval-label">Chunk Size</div>
                    <div class="retrieval-val">500 Characters</div>
                </div>
                <div class="retrieval-cell">
                    <div class="retrieval-label">Chunk Overlap</div>
                    <div class="retrieval-val">50 Characters</div>
                </div>
                <div class="retrieval-cell">
                    <div class="retrieval-label">Grounding Policy</div>
                    <div class="retrieval-val">Strict Document Refusal</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# =========================================================
# VIEW: MAIN CHAT WORKSPACE (2-COLUMN DESKTOP SPLIT)
# =========================================================
chat_col, agent_col = st.columns([2.4, 1.1], gap="large")

# ---------------------------------------------------------
# RIGHT PANEL: AGENT ACTIVITY, PIPELINE, RETRIEVAL, SOURCES
# ---------------------------------------------------------
with agent_col:
    st.markdown(render_activity_panel(st.session_state.agent_activity), unsafe_allow_html=True)
    st.markdown(render_pipeline_card(), unsafe_allow_html=True)
    st.markdown(render_retrieval_card(chunk_count=total_chunks, top_k=3), unsafe_allow_html=True)
    st.markdown(render_sources_card(st.session_state.sources), unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN CHAT COLUMN
# ---------------------------------------------------------
with chat_col:
    chat_container = st.container()

    with chat_container:
        # If no conversation exists, display the premium Welcome Screen & Suggestion Chips
        if not st.session_state.messages:
            st.markdown(render_welcome_screen(), unsafe_allow_html=True)

            st.markdown(
                '<div style="font-size:10.5px;font-weight:700;text-transform:uppercase;color:#64748b;letter-spacing:0.1em;text-align:center;margin-bottom:12px;">SUGGESTED QUESTIONS</div>',
                unsafe_allow_html=True
            )

            suggestions = [
                "What are the working hours?",
                "How many employees are there?",
                "What technologies does the company use?",
                "Tell me about the leave policy.",
            ]

            sugg_row1_col1, sugg_row1_col2 = st.columns(2)
            with sugg_row1_col1:
                if st.button(f"👉 {suggestions[0]}", use_container_width=True, key="sugg_0"):
                    st.session_state.pending_question = suggestions[0]
                    st.rerun()
            with sugg_row1_col2:
                if st.button(f"👉 {suggestions[1]}", use_container_width=True, key="sugg_1"):
                    st.session_state.pending_question = suggestions[1]
                    st.rerun()

            sugg_row2_col1, sugg_row2_col2 = st.columns(2)
            with sugg_row2_col1:
                if st.button(f"👉 {suggestions[2]}", use_container_width=True, key="sugg_2"):
                    st.session_state.pending_question = suggestions[2]
                    st.rerun()
            with sugg_row2_col2:
                if st.button(f"👉 {suggestions[3]}", use_container_width=True, key="sugg_3"):
                    st.session_state.pending_question = suggestions[3]
                    st.rerun()

        # If conversation exists, display conversation messages
        else:
            st.markdown('<div class="chat-scroll-container">', unsafe_allow_html=True)
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(render_user_message(msg["content"]), unsafe_allow_html=True)
                else:
                    st.markdown(render_agent_message(msg["content"]), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Handle Question Input (either from suggestion buttons or chat input box)
    active_question = None
    if st.session_state.pending_question:
        active_question = st.session_state.pending_question
        st.session_state.pending_question = None
    else:
        active_question = st.chat_input("Ask something about your company documents...")

    if active_question:
        # Add user message to conversation
        st.session_state.messages.append({"role": "user", "content": active_question})

        # Display progress status while agent is querying ChromaDB and Gemini
        with st.status("Searching company knowledge...", expanded=True) as status_box:
            status_box.write("🔎 Querying ChromaDB vector index...")
            answer, sources, activity = run_agent_pipeline(active_question)
            status_box.write("✨ Generating grounded response with Gemini 2.5 Flash...")
            status_box.update(label="Grounded response ready", state="complete", expanded=False)

        # Update session states with results
        st.session_state.agent_activity = activity
        st.session_state.sources = sources
        st.session_state.messages.append({"role": "assistant", "content": answer})

        st.rerun()
