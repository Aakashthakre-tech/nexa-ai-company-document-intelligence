# Nexa AI – Company Document Intelligence System

**An AI-powered platform for intelligent document processing, semantic search, and context-aware question answering.**

Nexa AI helps organizations understand and retrieve information from their company documents using Artificial Intelligence and Retrieval-Augmented Generation (RAG).

Instead of manually searching through lengthy PDF documents, users can upload documents, ask questions in natural language, and receive relevant answers based on the available document content.

---

## 1. Overview

Organizations manage large volumes of documents, including reports, policies, business records, agreements, and internal documentation.

Finding specific information from these documents manually can be time-consuming and inefficient.

Nexa AI addresses this problem by combining document extraction, semantic search, vector databases, and generative AI to provide an intelligent document interaction system.

## 2. Key Features

- **Document Upload:** Upload company documents for processing.
- **Text Extraction:** Extract textual content from PDF documents.
- **Scanned Document Support:** Use Gemini Vision for supported scanned and handwritten document pages.
- **Intelligent Chunking:** Divide extracted content into smaller, manageable text segments.
- **Semantic Search:** Find relevant information based on meaning rather than exact keyword matching.
- **AI-Powered Question Answering:** Ask questions about uploaded documents using natural language.
- **Context-Aware Responses:** Generate answers using relevant retrieved document content.
- **Document References:** Provide relevant source and page references where available.
- **Confidence Indicators:** Display confidence information where supported by the application.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js, Vite |
| Backend | Python, FastAPI |
| AI Model | Google Gemini 2.5 Flash |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Document Processing | PyPDF / PyMuPDF |
| Communication | REST API |

## 4. System Architecture

Nexa AI follows a Retrieval-Augmented Generation (RAG) architecture.

The system combines document processing, vector-based information retrieval, and AI-generated responses.

### Architecture Flow

```text
       USER
         |
         v
    React Frontend
         |
         v
    FastAPI Backend
         |
         v
   Document Upload
         |
         v
  PDF Text Extraction
         |
         v
  Gemini Vision (when
  scanned page support
      is required)
         |
         v
   Text Processing
         |
         v
   Text Chunking
         |
         v
  MiniLM Embeddings
         |
         v
      ChromaDB
         |
         |
    USER QUESTION
         |
         v
  Question Embedding
         |
         v
  Semantic Retrieval
         |
         v
 Relevant Document Chunks
         |
         v
  Gemini 2.5 Flash
         |
         v
   Final AI Response
         |
         v
  Source / Page References
         |
         v
    React Frontend
```

## 5. Working Flow

### Step 1: Document Upload

Users upload company PDF documents through the frontend interface.

The backend receives the uploaded files and starts the document processing pipeline.

### Step 2: Document Extraction

The system extracts text from PDF documents using PyPDF or PyMuPDF.

For supported scanned or handwritten pages, Gemini Vision is used to help extract and understand the content.

### Step 3: Text Processing and Chunking

Extracted text is cleaned and divided into smaller chunks.

Chunking makes it easier to process large documents and retrieve specific information.

### Step 4: Embedding Generation

The all-MiniLM-L6-v2 embedding model converts text chunks into numerical vector representations.

These vectors capture semantic information about the text.

### Step 5: Vector Storage

The generated embeddings and their associated document information are stored in ChromaDB.

This allows the application to perform semantic similarity searches.

### Step 6: User Question

Users ask questions about their uploaded company documents using natural language.

### Step 7: Semantic Retrieval

The user's question is converted into an embedding using the same embedding model.

ChromaDB searches for document chunks that are semantically relevant to the question.

### Step 8: AI Response Generation

The retrieved document content is provided as context to Gemini 2.5 Flash.

The model uses this context to generate a relevant response.

### Step 9: Final Result

The generated response is displayed in the frontend, along with relevant document and page references where available.

---

## 6. Advantages

1. **Time Efficiency:** Reduces the time required to manually search through lengthy documents.
2. **Intelligent Search:** Finds relevant information based on semantic meaning.
3. **Improved Accessibility:** Allows users to interact with documents through natural language questions.
4. **Context-Aware Answers:** Uses retrieved document information to generate relevant responses.
5. **Scalable Architecture:** Uses vector-based retrieval to support document collections.
6. **Scanned Document Support:** Supports processing of eligible scanned and handwritten pages through vision-based extraction.
7. **Better Information Retrieval:** Helps users locate important information across multiple documents.
8. **Centralized Document Interaction:** Provides a unified interface for searching and understanding company documents.

## 7. Applications

Nexa AI can be useful in:

- Corporate document management.
- Business reports and internal documentation.
- Company policy and procedure search.
- Financial and administrative document analysis.
- Research and knowledge management.
- Enterprise information retrieval.

## 8. Project Structure

```text
company_doc_agent/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── server/
│   └── main.py
│
├── src/
│   └── Document processing and AI modules
│
├── data/
│   └── Document storage
│
├── chroma_db/
│   └── Vector database storage
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

*Note: This is a high-level project structure. Individual modules and files may vary with implementation.*

## 9. Installation and Setup

### Prerequisites

- Python 3.11
- Node.js and npm
- Git
- Google Gemini API key

### Step 1: Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd company_doc_agent
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### Step 3: Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root and configure the Gemini API key using the environment variable name expected by the application.

```env
GEMINI_API_KEY=your_gemini_api_key
```

### Step 5: Start the Backend

```bash
python -m uvicorn server.main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Step 6: Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in the terminal.

---

## 10. Future Scope

- Support for additional document formats.
- Advanced document comparison.
- Improved multilingual document understanding.
- Enterprise authentication and role-based access.
- Enhanced document analytics and knowledge management.
- Integration with external business document platforms.

## 11. Conclusion

Nexa AI transforms traditional document searching into an intelligent information retrieval experience.

By combining Gemini 2.5 Flash, MiniLM embeddings, ChromaDB, and Retrieval-Augmented Generation, the system enables users to interact with company documents through natural language and retrieve relevant information efficiently.

**Nexa AI – Turning Company Documents into Actionable Knowledge.**

---

## Author

**Developed as an AI-powered document intelligence project.**

**GitHub:** https://github.com/Aakashthakre-tech