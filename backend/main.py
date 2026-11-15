import os
import shutil

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI(title="AgriSaarthi API")

VECTOR_DB_PATH = "vector_db"
UPLOAD_PATH = "uploads"

os.makedirs(VECTOR_DB_PATH, exist_ok=True)
os.makedirs(UPLOAD_PATH, exist_ok=True)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
print("Embeddings loaded")

llm = AzureChatOpenAI(
    azure_deployment="gpt-4.1-mini",
    api_version="2024-10-21",
    temperature=0
)


@app.get("/")
def health():
    return {"status": "up"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_PATH,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    loader = PyPDFLoader(file_path)

    pages = loader.load()

    for page in pages:
        page.metadata["source"] = file.filename

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(
        pages
    )

    index_file = os.path.join(
        VECTOR_DB_PATH,
        "index.faiss"
    )

    if os.path.exists(index_file):

        db = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        db.add_documents(chunks)

    else:

        db = FAISS.from_documents(
            chunks,
            embeddings
        )

    db.save_local(VECTOR_DB_PATH)

    return {
        "message": "PDF processed successfully",
        "chunks": len(chunks)
    }


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
async def chat(request: ChatRequest):

    db = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(
        request.question,
        k=4
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an Agricultural Scheme Expert.

Rules:
1. Answer only from context.
2. Reply in same language as user.
3. Mention subsidy details if available.
4. Mention eligibility if available.
5. Mention application process if available.

Context:
{context}

Question:
{question}

If answer not found say:
I could not find that in the uploaded PDFs.
"""
    )

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(
        {
            "context": context,
            "question": request.question
        }
    )

    sources = []

    for doc in docs:

        sources.append({
            "file":
            doc.metadata.get(
                "source"
            ),

            "page":
            doc.metadata.get(
                "page"
            )
        })

    return {
        "answer": answer,
        "sources": sources
    }