import os
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# -----------------------------
# CONFIG
# -----------------------------

VECTOR_DB_PATH = "vector_db"
UPLOAD_PATH = "uploads"

os.makedirs(VECTOR_DB_PATH, exist_ok=True)
os.makedirs(UPLOAD_PATH, exist_ok=True)

st.set_page_config(
    page_title="AgriSaarthi",
    layout="wide"
)

st.title("🌾 AgriSaarthi")
st.caption("AI Powered Agricultural Scheme Assistant")

# -----------------------------
# OPENAI
# -----------------------------

llm = AzureChatOpenAI(
    azure_deployment="gpt-4.1-mini",
    api_version="2024-10-21",
    temperature=0
)

# -----------------------------
# EMBEDDING MODEL
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# -----------------------------
# CHAT HISTORY
# -----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# PDF PROCESSING
# -----------------------------

def process_pdf(file):

    file_path = os.path.join(
        UPLOAD_PATH,
        file.name
    )

    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    loader = PyPDFLoader(file_path)

    pages = loader.load()

    # Add metadata
    for page in pages:
        page.metadata["source"] = file.name

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

    db.save_local(
        VECTOR_DB_PATH
    )

    return len(chunks)


# -----------------------------
# FILE UPLOAD
# -----------------------------

uploaded_files = st.file_uploader(
    "Upload Agricultural PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    if st.button("Process PDFs"):

        total_chunks = 0

        progress = st.progress(0)

        for idx, pdf in enumerate(uploaded_files):

            total_chunks += process_pdf(pdf)

            progress.progress(
                (idx + 1) / len(uploaded_files)
            )

        st.success(
            f"{len(uploaded_files)} PDF(s) processed successfully."
        )

        st.info(
            f"Total Chunks Created: {total_chunks}"
        )

st.divider()

# -----------------------------
# QUICK QUESTIONS
# -----------------------------

st.subheader("Quick Questions")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Subsidy Amount"):
        st.session_state["question"] = \
            "What is the subsidy amount?"

with c2:
    if st.button("Eligibility"):
        st.session_state["question"] = \
            "What is the eligibility criteria?"

with c3:
    if st.button("Application Process"):
        st.session_state["question"] = \
            "How to apply?"

# -----------------------------
# ASK QUESTION
# -----------------------------

question = st.text_input(
    "Ask question about schemes",
    value=st.session_state.get(
        "question",
        ""
    )
)

if st.button("Search"):

    index_file = os.path.join(
        VECTOR_DB_PATH,
        "index.faiss"
    )

    if not os.path.exists(index_file):

        st.error(
            "Please upload PDFs first."
        )

    else:

        db = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        docs = db.similarity_search(
            question,
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
6. If answer not found say:
'I could not find that in the uploaded PDFs.'

Context:
{context}

Question:
{question}
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
                "question": question
            }
        )

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        st.subheader("Answer")

        st.write(answer)

        st.subheader("Sources")

        displayed = set()

        for doc in docs:

            source = (
                doc.metadata.get("source"),
                doc.metadata.get("page")
            )

            if source not in displayed:

                displayed.add(source)

                st.info(
                    f"""
File: {doc.metadata.get('source')}

Page: {doc.metadata.get('page')}
"""
                )

        with st.expander(
            "Retrieved Chunks"
        ):

            for i, doc in enumerate(
                docs,
                start=1
            ):

                st.write(
                    f"### Chunk {i}"
                )

                st.write(
                    doc.page_content
                )

                st.write("---")

st.divider()

# -----------------------------
# CHAT HISTORY
# -----------------------------

st.subheader("Chat History")

for item in reversed(
    st.session_state.chat_history
):

    st.write(
        f"**Q:** {item['question']}"
    )

    st.write(
        f"**A:** {item['answer']}"
    )

    st.write("---")
