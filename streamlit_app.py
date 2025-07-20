import os
import tempfile
import streamlit as st
from src.retrieval_qa import get_response
from src.llm_model import LLMModel
from src.document_loader import load_file
from src.embed_and_store import VectorStore

vector_store = VectorStore()
llm_models = LLMModel()

error_message = "Sorry, Something Went Wrong!"

st.header("Policy Analyzer Query Application")

model_choice = st.sidebar.radio("Choose the LLM Model", ["OpenAI", "Azure OpenAI", "Gemini"])

# Set the vector store and LLM model based on the user selection
if model_choice == "Azure OpenAI":
    vector_embed_fn = vector_store.azure_openai_embedding
    llm_model_fn = llm_models.azure_llm_model
elif model_choice == "Gemini":
    vector_embed_fn = vector_store.gemini_embedding
    llm_model_fn = llm_models.gemini_llm_model
else:
    vector_embed_fn = vector_store.openai_embedding
    llm_model_fn = llm_models.openai_llm_model

document_upload = st.sidebar.file_uploader("Upload Document (PDF, Word, etc)", type=["pdf", "docx"])

if 'vector_db' not in st.session_state:
    st.session_state.vector_db = None

if st.sidebar.button("Submit"):
    if document_upload is not None:

        file_name = document_upload.name
        _, file_extension = os.path.splitext(file_name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            tmp_file.write(document_upload.getvalue())
            tmp_file_path = tmp_file.name

        try:
            with st.spinner('Generating Embedding...'):

                loaded_data = load_file(tmp_file_path)
                vector_db = vector_store.create_faiss_db(loaded_data, vector_embed_fn())

                st.session_state.vector_db = vector_db
        except Exception as exe:
            print(exe)
            st.error(error_message)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question := st.chat_input("Ask a question related to document:"):

    try:
        vector_db = vector_store.load_faiss_db(vector_embed_fn())
        st.session_state.vector_db = vector_db
    except FileNotFoundError:
        st.error("Please upload a document first and click 'Submit' to create embeddings.")

    if st.session_state.vector_db:

        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            try:
                full_response = get_response(llm_model_fn(), st.session_state.vector_db,
                                                          user_question, st.session_state.chat_history)
            except Exception as exe:
                print(exe)
                full_response = error_message

            message_placeholder.markdown(full_response)

        st.session_state.chat_history.extend([(user_question, full_response)])

        if len(st.session_state.chat_history) >= 5:
            st.session_state.chat_history.pop(0)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
