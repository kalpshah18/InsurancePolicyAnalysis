from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class LLMModel:

    def __init__(self):
        pass

    def openai_llm_model(self, temperature=None, model_name=None):

        if temperature is None:
            temperature = 0.2

        if model_name:
            openai_model_name = model_name
        else:
            openai_model_name = 'gpt-4o'

        openai_llm = ChatOpenAI(
            api_key=os.environ.get('OPENAI_API_KEY'),
            model_name=openai_model_name,
            temperature=temperature
        )

        return openai_llm

    def azure_llm_model(self, temperature=None, deployment_name=None):

        if temperature is None:
            temperature = 0.2

        if deployment_name:
            azure_deployment_name = deployment_name
        else:
            azure_deployment_name = 'DEPLOYMENT_NAME_GPT4o'

        azure_llm = AzureChatOpenAI(
            openai_api_base=os.environ.get('API_BASE') + os.environ.get(azure_deployment_name),
            openai_api_version=os.environ.get('API_VERSION'),
            openai_api_key=os.environ.get('API_KEY'),
            openai_api_type=os.environ.get('API_TYPE'),
            temperature=temperature
        )
        return azure_llm
    
    def gemini_llm_model(self, temperature=None, model_name=None):
        if temperature is None:
            temperature = 0.2

        if model_name:
            gemini_model_name = model_name
        else:
            gemini_model_name = 'gemini-2.0-flash-exp'
        
        gemini_llm = ChatGoogleGenerativeAI(
            model=gemini_model_name,
            google_api_key=os.environ.get('GEMINI_API_KEY'),
            temperature=temperature
        )
        return gemini_llm
