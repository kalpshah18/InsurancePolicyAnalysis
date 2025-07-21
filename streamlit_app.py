import os
import tempfile
import streamlit as st
from src.retrieval_qa import get_response
from src.llm_model import LLMModel
from src.document_loader import load_file
from src.embed_and_store import VectorStore

# Configure page settings
st.set_page_config(
    page_title="Policy Analyzer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

vector_store = VectorStore()
llm_models = LLMModel()

error_message = "Sorry, Something Went Wrong!"

# Add title and description
st.title("📋 Policy Analyzer")
st.markdown("Upload a document and ask questions to get intelligent answers using AI models.")

# Check if API keys are configured
def check_api_keys():
    """Check if at least one API key is configured"""
    try:
        openai_key = st.secrets.get("OPENAI_API_KEY", "")
        azure_key = st.secrets.get("API_KEY", "")
        google_key = st.secrets.get("GOOGLE_API_KEY", "")
        
        if not any([openai_key and openai_key != "your_openai_api_key_here",
                   azure_key and azure_key != "your_azure_openai_api_key", 
                   google_key and google_key != "your_google_api_key_here"]):
            st.error("⚠️ Please configure your API keys in Streamlit secrets to use this application.")
            st.info("Go to your Streamlit Cloud dashboard → Settings → Secrets to add your API keys.")
            return False
    except Exception:
        st.error("⚠️ Please configure your API keys in Streamlit secrets to use this application.")
        return False
    return True

if not check_api_keys():
    st.stop()

st.header("Ask Questions About Your Documents")

model_choice = st.sidebar.radio("Choose the LLM Model", ["Azure OpenAI"])

# Set the vector store and LLM model based on the user selection
if model_choice == "Azure OpenAI":
    vector_embed_fn = vector_store.azure_openai_embedding
    llm_model_fn = llm_models.azure_llm_model
else:
    vector_embed_fn = vector_store.openai_embedding
    llm_model_fn = llm_models.openai_llm_model

document_upload = st.sidebar.file_uploader("📁 Upload Document (PDF, DOCX)", type=["pdf", "docx"])

# Add information about supported models
with st.sidebar.expander("ℹ️ Model Information"):
    st.markdown("""
    **OpenAI**: GPT-4o with high accuracy
    **Azure OpenAI**: Enterprise-grade OpenAI models
    **Gemini**: Google's latest AI model
    """)

if 'vector_db' not in st.session_state:
    st.session_state.vector_db = None
    
if 'processing' not in st.session_state:
    st.session_state.processing = False

if st.sidebar.button("🚀 Process Document", disabled=st.session_state.processing):
    if document_upload is not None:
        st.session_state.processing = True

        file_name = document_upload.name
        _, file_extension = os.path.splitext(file_name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            tmp_file.write(document_upload.getvalue())
            tmp_file_path = tmp_file.name

        try:
            with st.spinner('🔄 Processing document and generating embeddings...'):

                loaded_data = load_file(tmp_file_path)
                vector_db = vector_store.create_faiss_db(loaded_data, vector_embed_fn())

                st.session_state.vector_db = vector_db
                st.sidebar.success(f"✅ Successfully processed {file_name}")

        except Exception as exe:
            print(exe)
            st.sidebar.error(f"❌ Error processing document: {str(exe)}")
        finally:
            st.session_state.processing = False
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass
    else:
        st.sidebar.warning("⚠️ Please upload a document first!")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question := st.chat_input("💬 Ask a question about your document:", disabled=not st.session_state.vector_db):

    if not st.session_state.vector_db:
        st.error("⚠️ Please upload a document first and click 'Process Document' to create embeddings.")
        st.stop()

    try:
        # Try to load existing vector database
        vector_db = vector_store.load_faiss_db(vector_embed_fn())
        st.session_state.vector_db = vector_db
    except FileNotFoundError:
        if not st.session_state.vector_db:
            st.error("⚠️ No processed document found. Please upload a document first and click 'Process Document'.")
            st.stop()

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
