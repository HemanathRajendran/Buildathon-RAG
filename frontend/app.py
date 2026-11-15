import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AgriSaarthi",
    layout="wide"
)

st.title("AgriSaarthi")
st.caption(
    "AI Powered Agricultural Scheme Assistant"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_files = st.file_uploader(
    "Upload Agricultural PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    if st.button("Process PDFs"):

        progress = st.progress(0)

        for idx, file in enumerate(uploaded_files):

            response = requests.post(
                f"{API_URL}/upload",
                files={
                    "file":
                    (
                        file.name,
                        file.getvalue(),
                        "application/pdf"
                    )
                }
            )

            progress.progress(
                (idx + 1) /
                len(uploaded_files)
            )

        st.success(
            "Files Processed Successfully"
        )

st.divider()

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

question = st.text_input(
    "Ask Question",
    value=st.session_state.get(
        "question",
        ""
    )
)

if st.button("Search"):

    response = requests.post(
        f"{API_URL}/chat",
        json={
            "question": question
        }
    )

    result = response.json()

    st.subheader("Answer")

    st.write(
        result["answer"]
    )

    st.subheader("Sources")

    for source in result["sources"]:

        st.info(
            f"""
File : {source['file']}

Page : {source['page']}
"""
        )

    st.session_state.chat_history.append(
        {
            "question": question,
            "answer": result["answer"]
        }
    )

st.divider()

st.subheader("Chat History")

for item in reversed(
    st.session_state.chat_history
):

    st.write(
        f"Q: {item['question']}"
    )

    st.write(
        f"A: {item['answer']}"
    )

    st.write("---")