from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()


class VectorStore:

    def __init__(self):
        self.faiss_folder_name = "faiss_index"
    
    def _get_secret(self, key, default=None):
        """Get secret from Streamlit secrets or environment variables"""
        try:
            return st.secrets.get(key, os.environ.get(key, default))
        except Exception:
            return os.environ.get(key, default)

    def openai_embedding(self):
        """
        Make embedding model call with openai
        langc means Langchain
        :return: embedding model
        """
        embeddings_model = OpenAIEmbeddings(
            api_key=self._get_secret('OPENAI_API_KEY'),
            model="text-embedding-3-large"
        )
        return embeddings_model

    def azure_openai_embedding(self):
        """
        Make embedding model call with openai
        langc means Langchain
        :return: embedding model
        """
        embeddings_model = AzureOpenAIEmbeddings(
            openai_api_base=self._get_secret('API_BASE') + self._get_secret('EMBEDDING_DEPLOYMENT_NAME'),
            openai_api_version=self._get_secret('AZURE_AI_SEARCH_API_VERSION'),
            openai_api_key=self._get_secret('API_KEY'),
        )
        return embeddings_model
    
    def gemini_embedding(self):
        """
        Make embedding model call with Gemini
        :return: embedding model
        """
        embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=self._get_secret('GOOGLE_API_KEY')
        )
        return embeddings_model

    def create_faiss_db(self, document, embedding_model):
        """
        Create embedding on document with embedding model and save it in local driver with name as faiss_index
        :param document: document or a text list on which we like to create embeddings
        :param embedding_model: Embedding model with it api_key which we gonna use to create embedding
        """
        vector_db = FAISS.from_documents(document, embedding_model)
        vector_db.save_local(self.faiss_folder_name)
        return vector_db

    def load_faiss_db(self, embedding_model):
        """
        load existing index to retriv document based on user question
        :return: List of document which is relevant to the user question
        """

        if not os.path.exists(self.faiss_folder_name):
            raise FileNotFoundError(f"FAISS index file not found at {self.faiss_folder_name}")

        vector_db = FAISS.load_local(self.faiss_folder_name,
                                     embedding_model,
                                     allow_dangerous_deserialization=True)
        return vector_db
