# Streamlit Cloud Deployment Guide

This guide will help you deploy the Policy Analyzer application to Streamlit Cloud.

## Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **API Keys**: At least one of the following:
   - OpenAI API Key
   - Azure OpenAI credentials
   - Google AI API Key

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository structure looks like this:
```
your-repo/
├── streamlit_app.py          # Main application file (REQUIRED)
├── requirements.txt          # Dependencies (REQUIRED)
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml         # Secrets template (DO NOT COMMIT)
├── src/                     # Source code modules
├── .gitignore              # Git ignore file
└── README.md               # This file
```

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account if needed
4. Select your repository
5. Set the main file path to `streamlit_app.py`
6. Click "Deploy"

### 3. Configure Secrets

After deployment, you need to add your API keys:

1. In your Streamlit Cloud dashboard, click on your app
2. Go to "Settings" → "Secrets"
3. Add your secrets in TOML format:

```toml
# OpenAI Configuration (add if using OpenAI)
OPENAI_API_KEY = "your_openai_api_key_here"

# Azure OpenAI Configuration (add if using Azure OpenAI)
API_KEY = "your_azure_openai_api_key"
API_BASE = "https://your-resource-name.openai.azure.com/"
API_VERSION = "2024-02-15-preview"
API_TYPE = "azure"
DEPLOYMENT_NAME_GPT4o = "/deployments/your-gpt4o-deployment-name/chat/completions?api-version="
DEPLOYMENT_NAME_GPT4o_TURBO = "/deployments/your-gpt4o-turbo-deployment-name/chat/completions?api-version="
EMBEDDING_DEPLOYMENT_NAME = "/deployments/your-embedding-deployment-name/"
AZURE_AI_SEARCH_API_VERSION = "2023-11-01"

# Google API Configuration (add if using Gemini)
GOOGLE_API_KEY = "your_google_api_key_here"
```

4. Save the secrets
5. Your app will automatically restart with the new configuration

### 4. Test Your Deployment

1. Visit your app URL (provided by Streamlit Cloud)
2. Upload a test document
3. Try asking questions to verify everything works

## Important Notes

### Security
- **NEVER** commit secrets to your repository
- Use Streamlit's secrets management for all API keys
- The `.streamlit/secrets.toml` file is in `.gitignore` for this reason

### File Storage
- Streamlit Cloud has ephemeral storage (files are not persistent between app restarts)
- Uploaded documents and vector databases will be recreated as needed
- This is fine for this application as we recreate embeddings when documents are uploaded

### Resource Limits
- Streamlit Cloud has resource limits for free accounts
- Large documents may take longer to process
- Consider upgrading to Streamlit Cloud for Teams for production use

### Troubleshooting

**App won't start:**
- Check that `streamlit_app.py` is in the repository root
- Verify `requirements.txt` has all necessary dependencies

**API errors:**
- Double-check your API keys in the Secrets section
- Ensure the API keys have the correct permissions

**File upload issues:**
- Make sure the file types are supported (PDF, DOCX)
- Check file size limits

**Memory issues:**
- Large documents may cause memory issues on free tier
- Try smaller documents or upgrade your plan

## Getting API Keys

### OpenAI
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an account and add billing information
3. Go to API Keys section and create a new key

### Azure OpenAI
1. Create an Azure account
2. Create an Azure OpenAI resource
3. Deploy the models you want to use
4. Get the endpoint URL and API key

### Google AI (Gemini)
1. Go to [ai.google.dev](https://ai.google.dev)
2. Create a project
3. Enable the Generative AI API
4. Create an API key

## Support

If you encounter issues:
1. Check the Streamlit Cloud logs in your dashboard
2. Verify all secrets are properly configured
3. Test with a small document first
4. Check the GitHub Issues for common problems

## Local Development

To run locally for development:

```bash
# Clone the repository
git clone your-repo-url
cd your-repo

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your actual API keys

# Run the app
streamlit run streamlit_app.py
```
