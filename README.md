# Insurance Policy Analysis using LLMs
A powerful document analysis application that leverages Large Language Models (LLMs) to provide intelligent question-answering capabilities for insurance policies and other documents. The application uses RAG (Retrieval-Augmented Generation) to provide accurate, context-aware responses based on uploaded documents.

## Features

- **Multi-LLM Support**: Choose between OpenAI, Azure OpenAI, and Google Gemini models
- **Document Upload**: Support for PDF and DOCX files
- **Vector Search**: FAISS-based vector database for efficient document retrieval
- **Interactive Chat**: Streamlit-powered web interface with chat history
- **RAG Implementation**: Combines document retrieval with LLM generation for accurate responses
- **Persistent Storage**: Embeddings are stored and can be reused across sessions

## Technology Stack

- **Frontend**: Streamlit
- **LLMs**: OpenAI GPT-4o, Azure OpenAI, Google Gemini
- **Vector Database**: FAISS
- **Document Processing**: LangChain, PyPDF, Unstructured
- **Embeddings**: OpenAI text-embedding-3-large, Azure OpenAI, Google Generative AI

## Prerequisites

Before running the application, you'll need API keys for at least one of the following services:

- **OpenAI API Key** (for OpenAI models)
- **Azure OpenAI credentials** (for Azure OpenAI models)
- **Google API Key** (for Gemini models)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kalpshah18/InsurancePolicyAnalysis.git
   cd InsurancePolicyAnalysis/backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the backend directory and add your API keys:

   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Azure OpenAI Configuration (if using Azure)
   API_KEY=your_azure_openai_api_key
   API_BASE=your_azure_openai_endpoint
   EMBEDDING_DEPLOYMENT_NAME=your_embedding_deployment_name
   AZURE_AI_SEARCH_API_VERSION=2023-05-15
   
   # Google Gemini Configuration (if using Gemini)
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

1. **Start the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to `http://localhost:8501`

3. **Using the application**:
   - Select your preferred LLM model from the sidebar (OpenAI, Azure OpenAI, or Gemini)
   - Upload a document (PDF or DOCX) using the file uploader
   - Click "Submit" to process the document and create embeddings
   - Start asking questions about your document in the chat interface

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── document_loader.py      # Document loading and processing
│   ├── embed_and_store.py      # Vector embeddings and FAISS storage
│   ├── llm_model.py           # LLM model configurations
│   └── retrieval_qa.py        # RAG implementation
├── faiss_index/               # Vector database storage
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── testDocument1.pdf        # Sample test document
└── testDocument2.pdf        # Sample test document
```

## How It Works

1. **Document Processing**: Uploaded documents are processed using LangChain loaders (PyPDF for PDFs, Unstructured for DOCX)
2. **Embedding Generation**: Text chunks are converted to vector embeddings using the selected embedding model
3. **Vector Storage**: Embeddings are stored in a FAISS vector database for efficient similarity search
4. **Query Processing**: User questions are embedded and used to retrieve relevant document chunks
5. **Response Generation**: Retrieved context is combined with the user question and sent to the LLM for answer generation

## Use Cases

- **Insurance Policy Analysis**: Analyze complex insurance documents and get quick answers
- **Contract Review**: Upload contracts and ask specific questions about terms and conditions
- **Document Q&A**: General purpose document question-answering for various file types
- **Research Assistant**: Extract specific information from large documents efficiently

## Configuration

### LLM Models
- **OpenAI**: Uses GPT-4o by default with temperature 0.2
- **Azure OpenAI**: Configurable deployment and API version
- **Gemini**: Google's Generative AI models

### Embedding Models
- **OpenAI**: text-embedding-3-large
- **Azure OpenAI**: Configurable embedding deployment
- **Gemini**: Google Generative AI embeddings

## Security Notes

- Store API keys securely in the `.env` file
- Never commit API keys to version control
- The `.env` file should be added to `.gitignore`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

- **"Please upload a document first"**: Make sure to upload a document and click "Submit" before asking questions
- **API Key errors**: Verify your API keys are correctly set in the `.env` file
- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## Support

For support, please open an issue at [kalpshah18/InsurancePolicyAnalysis](https://github.com/kalpshah18/InsurancePolicyAnalysis) or contact @kalpshah18 on GitHub.

