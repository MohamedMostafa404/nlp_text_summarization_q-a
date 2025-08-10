import streamlit as st
from transformers import pipeline
import PyPDF2
import re

# --- Page config ---
st.set_page_config(page_title="AI Summarizer & Q&A", layout="wide")

# --- Load Models ---
@st.cache_resource
def load_models():
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    qa = pipeline("question-answering", model="deepset/roberta-base-squad2")
    return summarizer, qa

# --- Helpers ---
def chunk_text(text, max_chars=2000):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current_chunk = [], ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_text(text, summarizer):
    chunks = chunk_text(text, max_chars=1200)
    summaries = [summarizer(c, max_length=150, min_length=30, truncation=True)[0]['summary_text'] for c in chunks]
    return " ".join(summaries)

def answer_question(question, text, qa_pipeline):
    chunks = chunk_text(text, max_chars=2000)
    results = [qa_pipeline(question=question, context=c) for c in chunks]
    best = max(results, key=lambda x: x['score'])
    return best

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    return "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

# --- App Layout ---
st.title("📝 AI Summarizer & ❓ Q&A Assistant")
st.write("Your all-in-one tool for summarizing long text and asking intelligent questions.")

# Sidebar Input
with st.sidebar:
    st.header("📂 Input Options")
    text_input = st.text_area("Paste your text here", height=200)
    uploaded_file = st.file_uploader("Or upload a file (.txt or .pdf)", type=["txt", "pdf"])
    if uploaded_file and not text_input:
        if uploaded_file.type == "application/pdf":
            text_input = read_pdf(uploaded_file)
        else:
            text_input = uploaded_file.read().decode("utf-8")

    summarizer, qa_pipeline = load_models()

    if st.button("🔍 Summarize"):
        if text_input:
            with st.spinner("Generating summary..."):
                st.session_state.summary = summarize_text(text_input, summarizer)
                st.session_state.original = text_input
        else:
            st.warning("Please provide text or upload a file.")

# Main Output Area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📜 Summary")
    if 'summary' in st.session_state:
        st.success(st.session_state.summary)
    else:
        st.info("No summary yet.")

with col2:
    st.subheader("💬 Ask a Question")
    question = st.text_input("Type your question here")
    if st.button("Get Answer"):
        if question and 'original' in st.session_state:
            with st.spinner("Searching answer..."):
                ans = answer_question(question, st.session_state.original, qa_pipeline)
                st.markdown(f"**Answer:** {ans['answer']}")
                st.caption(f"Confidence: {ans['score']:.2f}")
        else:
            st.warning("You need both text and a question.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Transformers")
