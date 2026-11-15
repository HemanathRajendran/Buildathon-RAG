# AgriSaarthi

## AI-Powered Agricultural Scheme Assistant

AgriSaarthi is a Retrieval-Augmented Generation (RAG) application that helps users query agricultural scheme documents using natural language. Instead of manually searching through lengthy government PDFs, users can upload one or more documents and receive accurate, context-aware answers with source references.

This project was developed as part of a Buildathon to demonstrate practical applications of Generative AI, Vector Databases, Hybrid Search, and Prompt Engineering.

---

## Problem Statement

Agricultural schemes, subsidies, eligibility criteria, and application procedures are often distributed across large government documents and PDFs. Finding relevant information manually can be difficult and time-consuming.

AgriSaarthi simplifies this process by allowing users to upload multiple agricultural scheme PDFs and interact with them conversationally.

---

## Features

### Multi-PDF Support
Upload and search across multiple agricultural scheme documents within a single knowledge base.

### Semantic Search
Uses embeddings and vector similarity search to find contextually relevant information.

### Hybrid Retrieval Ready
Designed to support:
- FAISS Vector Search
- BM25 Keyword Search

Combining semantic and keyword retrieval improves answer quality and retrieval accuracy.

### Source Citation
Every answer includes:
- Source Document
- Page Number

This improves trust, transparency, and explainability.

### Chat History
Maintains previous conversations for a more natural user experience.

### Multi-Language Support
Supports:
- English
- Tamil

Responses are generated in the same language as the user's query.

### Persistent Vector Database
Processed PDFs are stored locally and can be reused without reprocessing.

---

## Architecture

```text
                         +------------------+
                         |    Streamlit UI  |
                         +---------+--------+
                                   |
                                   |
                                   v
                         +------------------+
                         | PDF Upload       |
                         +---------+--------+
                                   |
                                   v
                         +------------------+
                         | PyPDFLoader      |
                         +---------+--------+
                                   |
                                   v
                         +------------------+
                         | Text Chunking    |
                         | 1000 Chars       |
                         | 200 Overlap      |
                         +---------+--------+
                                   |
                                   v
                         +------------------+
                         | Embeddings       |
                         | BGE Small Model  |
                         +---------+--------+
                                   |
                                   v
                         +------------------+
                         | FAISS Vector DB  |
                         +---------+--------+
                                   |
                                   v
                         +------------------+
                         | Similarity Search|
                         +---------+--------+
                                   |
                                   v
                         +------------------+
                         | GPT-4.1 Mini     |
                         +---------+--------+
                                   |
                                   v
                         +------------------+
                         | Answer + Sources |
                         +------------------+
```

---

## Technology Stack

### Frontend
- Streamlit

### LLM
- Azure OpenAI GPT-4.1 Mini

### Embeddings
- HuggingFace Embeddings
- BAAI/bge-small-en-v1.5

### Vector Database
- FAISS

### Retrieval Framework
- LangChain

### Document Processing
- PyPDFLoader

### Language
- Python

---

## RAG Pipeline

```text
PDF Upload
      ↓
Document Loading
      ↓
Chunking
      ↓
Embedding Generation
      ↓
FAISS Storage
      ↓
User Query
      ↓
Similarity Search
      ↓
Relevant Chunks
      ↓
GPT-4.1 Mini
      ↓
Answer + Source Citation
```

---

## Best Practices Implemented

### Prompt Engineering

A custom system prompt is used to:

- Restrict responses to retrieved document context
- Reduce hallucinations
- Return responses in the user's language
- Include subsidy details when available
- Include eligibility information when available
- Handle missing information gracefully

Example:

```text
You are an Agricultural Scheme Expert.

Answer only from context.
Reply in the same language as the user.
Do not make up information.
If information is unavailable, clearly say so.
```

---

### Chunking Strategy

```python
chunk_size = 1000
chunk_overlap = 200
```

Benefits:
- Better retrieval quality
- Preserves context
- Reduces information loss

---

### Metadata Enrichment

Each chunk stores metadata:

```python
{
    "source": "scheme.pdf",
    "page": 12
}
```

Benefits:
- Source citation
- Traceability
- Explainability

---

### Persistent Storage

Vector database files:

```text
vector_db/
├── index.faiss
└── index.pkl
```

Benefits:
- Faster startup
- No need to re-index PDFs
- Reusable knowledge base

---

### Chat History

Uses:

```python
st.session_state.chat_history
```

Benefits:
- Multi-turn conversations
- Context-aware interactions
- Better user experience

---

### Multi-PDF Ingestion

Supports uploading multiple PDFs and building a shared knowledge base.

Benefits:
- Single query across multiple schemes
- Improved coverage
- Better user experience

---

### Source Transparency

Displays:

```text
Document Name
Page Number
Retrieved Chunks
```

Benefits:
- Trustworthy responses
- Easy validation
- Improved explainability

---

## Installation

### Clone Repository

```bash
git clone <repository-url>

cd agri_saarthi
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```cmd
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

### Linux / Mac

```bash
export AZURE_OPENAI_API_KEY="YOUR_KEY"

export AZURE_OPENAI_ENDPOINT="YOUR_ENDPOINT"

export OPENAI_API_VERSION="2024-10-21"
```

### Windows

```cmd
set AZURE_OPENAI_API_KEY=YOUR_KEY

set AZURE_OPENAI_ENDPOINT=YOUR_ENDPOINT

set OPENAI_API_VERSION=2024-10-21
```

---

## Run Application

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

## Usage

### Step 1

Upload one or more scheme PDFs.

Examples:

```text
PM Kisan.pdf
Crop Insurance.pdf
Micro Irrigation.pdf
```

### Step 2

Click:

```text
Process PDFs
```

### Step 3

Ask Questions

Examples:

```text
What is the subsidy amount?

Who is eligible for this scheme?

How can farmers apply?

What documents are required?
```

### Tamil Queries

```text
இந்த திட்டத்திற்கு யார் தகுதியானவர்?

விவசாயிகளுக்கு என்ன மானியம் கிடைக்கும்?

விண்ணப்பிப்பது எப்படி?
```

---

## Sample Questions

### Subsidy Information

```text
What subsidy amount is offered under this scheme?
```

### Eligibility

```text
Who can apply for this scheme?
```

### Application Process

```text
How should farmers apply?
```

### Benefits

```text
What are the benefits of this scheme?
```

### Required Documents

```text
What documents are required for registration?
```

---

## Future Enhancements

- BM25 + FAISS Hybrid Retrieval
- OCR Support for Scanned PDFs
- Cross-Encoder Re-ranking
- Voice-Based Queries
- Speech-to-Text Support
- Scheme Recommendation Engine
- Farmer Profile-Based Recommendations
- Dashboard Analytics
- Advanced Multi-Language Support

---

## Key Learnings

This project provided hands-on experience in:

- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Semantic Search
- Prompt Engineering
- Azure OpenAI
- LangChain
- HuggingFace Embeddings
- FAISS
- Streamlit Application Development
- LLM-Powered Document Intelligence

---

## Project Title

**AgriSaarthi: AI-Powered Agricultural Scheme Discovery and Assistance Platform**

Built as part of a Buildathon to demonstrate how Generative AI can improve access to agricultural knowledge, government welfare schemes, and citizen services through conversational document intelligence.
