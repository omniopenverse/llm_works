import streamlit as st
from os import getenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.vectorstores import FAISS

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Chat with PDF", layout="wide")
st.title("📘 Chat with Your PDF")

# --- Sidebar for PDF Upload ---
pdf_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")

# --- Initialize Session State ---
if "conversation_chain" not in st.session_state:
    st.session_state.conversation_chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Process PDF and Create Knowledge Base ---
if pdf_file and not st.session_state.conversation_chain:
    with st.sidebar:
        with st.spinner("Processing PDF..."):
            # Extract text
            pdf_reader = PdfReader(pdf_file)
            text = "".join(page.extract_text() or "" for page in pdf_reader.pages)

            # Split into chunks
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text)

            # Create embeddings and vector store
            embeddings = OllamaEmbeddings(
                base_url=getenv("OLLAMA_BASE_URL"),
                model="nomic-embed-text:v1.5"
            )
            vectorstore = FAISS.from_texts(chunks, embeddings)

            # Initialize LLM without terminal output
            llm = Ollama(
                base_url=getenv("OLLAMA_BASE_URL"),
                model="llama3.2:1b",
                temperature=0,
                callback_manager=None  # Remove the terminal output callback
            )

            # Set up conversational chain
            st.session_state.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(),
                return_source_documents=True,
                verbose=False
            )
        st.success("PDF processed! Ask your questions below.")

# --- Chat Interface ---
if st.session_state.conversation_chain:
    # Display chat history (oldest to newest)
    if st.session_state.chat_history:
        st.markdown("---")
        for i, (question, answer, sources) in enumerate(st.session_state.chat_history, 1):
            st.markdown(f"**Q{i}:** {question}")
            st.markdown(f"**A{i}:** {answer}")
            if sources:
                with st.expander(f"📄 Sources for Q{i}"):
                    for j, src in enumerate(sources, 1):
                        st.markdown(f"**Source {j}:**")
                        st.code(src.page_content.strip()[:500] + "...", language="markdown")
            st.markdown("---")

    # Input bar for new questions
    with st.form(key="question_form", clear_on_submit=True):
        user_question = st.text_input("Ask a question about the PDF:", key="user_input")
        submit_button = st.form_submit_button("Send")

        if submit_button and user_question:
            with st.spinner("Generating response..."):
                response = st.session_state.conversation_chain({
                    "question": user_question,
                    "chat_history": [(q, a) for q, a, _ in st.session_state.chat_history]
                })
                st.session_state.chat_history.append((
                    user_question,
                    response["answer"],
                    response.get("source_documents", [])
                ))
                st.rerun()  # Refresh to show the new message immediately

# --- Placeholder if no PDF is uploaded ---
if not pdf_file:
    st.info("Please upload a PDF to start chatting.")