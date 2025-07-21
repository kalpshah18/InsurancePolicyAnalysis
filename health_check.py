"""
Health check script to verify the application setup.
Run this before deploying to Streamlit Cloud to ensure everything is configured correctly.
"""

import sys
import importlib.util

def check_imports():
    """Check if all required packages can be imported"""
    required_packages = [
        'streamlit',
        'langchain',
        'langchain_openai',
        'langchain_google_genai',
        'langchain_community',
        'faiss',
        'pypdf',
        'unstructured',
        'dotenv',
        'openai'
    ]
    
    print("Checking package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            if package == 'faiss':
                import faiss
            elif package == 'dotenv':
                from dotenv import load_dotenv
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return failed_imports

def check_file_structure():
    """Check if required files exist"""
    import os
    
    print("\nChecking file structure...")
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        'src/__init__.py',
        'src/document_loader.py',
        'src/embed_and_store.py',
        'src/llm_model.py',
        'src/retrieval_qa.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    return missing_files

def check_streamlit_config():
    """Check Streamlit configuration"""
    import os
    
    print("\nChecking Streamlit configuration...")
    
    if os.path.exists('.streamlit/config.toml'):
        print("✅ .streamlit/config.toml exists")
    else:
        print("⚠️ .streamlit/config.toml not found (optional)")
    
    if os.path.exists('.streamlit/secrets.toml'):
        print("✅ .streamlit/secrets.toml exists")
        print("⚠️ Make sure secrets.toml is in .gitignore and not committed!")
    else:
        print("⚠️ .streamlit/secrets.toml not found")
        print("   Create this file locally or configure secrets in Streamlit Cloud")

def main():
    print("🔍 Policy Analyzer Health Check")
    print("=" * 40)
    
    # Check imports
    failed_imports = check_imports()
    
    # Check file structure
    missing_files = check_file_structure()
    
    # Check Streamlit config
    check_streamlit_config()
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 Summary")
    
    if failed_imports:
        print(f"❌ Missing packages: {', '.join(failed_imports)}")
        print("   Run: pip install -r requirements.txt")
    else:
        print("✅ All packages available")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
    else:
        print("✅ All required files present")
    
    if not failed_imports and not missing_files:
        print("\n🎉 Application is ready for deployment!")
        print("\nNext steps:")
        print("1. Commit your changes to GitHub")
        print("2. Deploy to Streamlit Cloud")
        print("3. Configure secrets in Streamlit Cloud dashboard")
    else:
        print("\n⚠️ Please fix the issues above before deploying")
    
    return len(failed_imports) + len(missing_files) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
