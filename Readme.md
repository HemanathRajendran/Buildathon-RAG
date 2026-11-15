# Multi-PDF Conversational AI Assistant

## Overview

This project is a Multi-PDF Conversational AI Assistant built using FastAPI, Azure OpenAI, LangChain, FAISS, and BM25-based Hybrid Retrieval. The application allows users to upload multiple PDF documents and ask questions in natural language. Responses are generated based on the uploaded documents, enabling accurate, context-aware, and grounded answers.

The solution leverages Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents before generating responses, significantly reducing hallucinations and improving answer quality.

---

## Features

- Upload and process multiple PDF documents
- Hybrid Retrieval using FAISS and BM25
- Context-aware conversational interface
- Chat history support for follow-up questions
- Document-grounded responses
- Persistent vector database storage
- FastAPI backend APIs
- Streamlit user interface
- Azure OpenAI integration
- Prompt engineering for reliable responses

---

## Architecture

```text
PDF Upload
     ↓
Document Loader
     ↓
Text Chunking
     ↓
Embeddings Generation
     ↓
FAISS Vector Store
     ↓
BM25 Retriever
     ↓
Hybrid Retrieval
     ↓
Azure OpenAI
     ↓
Generated Response
```

---

## Technology Stack

### Backend
- FastAPI
- Python
- LangChain

### AI Components
- Azure OpenAI
- OpenAI Embeddings
- Retrieval-Augmented Generation (RAG)

### Retrieval
- FAISS
- BM25 Retriever
- Hybrid Search

### Frontend
- Streamlit

### Storage
- Local Persistent Vector Database

---

## Project Structure

```text
week2-FASTAPI_buildathon/
│
├── backend/
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── requirements.txt
│   └── vector_db/
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── uploads/
│
├── venv/
│
└── README.md
```

---

## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
cd week2-FASTAPI_buildathon
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Mac/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

### Backend

```bash
cd backend
pip install -r requirements.txt
```

### Frontend

```bash
cd ../frontend
pip install -r requirements.txt
```

---

## Environment Variables

```bash
export AZURE_OPENAI_ENDPOINT=""
export AZURE_OPENAI_API_VERSION="2024-02-01"
export AZURE_OPENAI_API_KEY="<your-api-key>"
```

---

## Running the Backend

```bash
cd backend

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API Documentation:

```text
http://localhost:8000/docs
```

---

## Running the Frontend

```bash
cd frontend

streamlit run app.py --server.port 8501
```

Application URL:

```text
http://localhost:8501
```

---

## How It Works

### Document Processing

1. User uploads one or more PDF documents.
2. PDFs are loaded and parsed.
3. Documents are split into chunks.
4. Embeddings are generated.
5. Chunks are stored in FAISS vector database.

### Question Answering

1. User submits a question.
2. Hybrid Retrieval searches documents using:
   - Semantic Search (FAISS)
   - Keyword Search (BM25)
3. Relevant chunks are retrieved.
4. Retrieved context is sent to Azure OpenAI.
5. Grounded response is returned to the user.

---

## Sample Questions

- Summarize this document.
- What are the key takeaways?
- Explain the main objective.
- List all action items.
- Compare uploaded documents.
- What recommendations are provided?
- Explain this in simple terms.
- Generate an executive summary.
- What challenges are discussed?
- What solutions are proposed?

---

## Key Design Decisions

### Hybrid Retrieval

The application combines vector search and keyword search:

**FAISS**
- Captures semantic similarity
- Handles natural language queries effectively

**BM25**
- Finds exact keyword matches
- Improves retrieval for technical terms and identifiers

Combining both approaches improves retrieval accuracy and relevance.

### Conversation History

User interactions are stored during the session, allowing follow-up questions and context-aware conversations.

### Hallucination Reduction

Responses are generated only from retrieved document content, ensuring answers remain grounded in source documents.

---

## Future Enhancements

- User authentication
- Role-based access control
- Metadata filtering
- Citation and page references
- Cross-encoder reranking
- Feedback collection
- Cloud deployment
- Monitoring and analytics
- Document version management

---

## Learning Outcomes

Through this project, I gained hands-on experience with:

- FastAPI application development
- Retrieval-Augmented Generation (RAG)
- Azure OpenAI integration
- Vector databases and embeddings
- Hybrid Search (FAISS + BM25)
- Prompt Engineering
- Multi-document retrieval systems
- Building end-to-end Generative AI applications

---

## Conclusion

This project demonstrates how Retrieval-Augmented Generation (RAG) can be used to build an intelligent document assistant capable of understanding and answering questions from multiple PDF documents. By combining Azure OpenAI, FastAPI, FAISS, and BM25, the solution delivers accurate, context-aware, and scalable document intelligence capabilities.

---
Built as part of the Week 2 Buildathon.
