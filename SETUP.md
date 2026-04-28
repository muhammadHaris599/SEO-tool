# Step-by-Step Setup Instructions

Complete guide to setting up the SEO Content Automation Tool from scratch.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Windows Setup](#windows-setup)
3. [macOS/Linux Setup](#macos-linux-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Verification](#verification)
7. [WordPress Setup (Optional)](#wordpress-setup-optional)

## Prerequisites

Before starting, ensure you have:

- **Python 3.10 or higher** - [Download here](https://www.python.org/downloads/)
- **Git** (optional) - [Download here](https://git-scm.com/)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)
- **Text Editor** - VS Code, Sublime, or any code editor
- **Command Line Interface** - Terminal (macOS/Linux) or PowerShell (Windows)

### Verify Python Installation

Open your terminal/PowerShell and run:

```bash
python --version
```

You should see `Python 3.10.x` or higher.

---

## Windows Setup

### Step 1: Navigate to Project Directory

```powershell
cd C:\Users\wahab.ikram\Desktop\SEOTool
```

### Step 2: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal after activation.

### Step 3: Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn (API framework)
- Pydantic (Data validation)
- OpenAI (AI integration)
- httpx (HTTP client)
- python-dotenv (Environment config)
- Streamlit (UI dashboard)

### Step 4: Create Environment File

```powershell
# Copy the template
Copy-Item .env.example -Destination .env

# Open .env in Notepad to edit
notepad .env
```

Or use VS Code:
```powershell
code .env
```

### Step 5: Configure Credentials

Edit `.env` and add your credentials:

```env
# REQUIRED - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-YOUR_API_KEY_HERE

# Model selection (optional)
OPENAI_MODEL=gpt-4-turbo

# Optional - WordPress configuration
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_app_password

# Server configuration (optional)
API_HOST=0.0.0.0
API_PORT=8000
```

**⚠️ Important**: Never share your API keys or push `.env` to version control.

### Step 6: Run FastAPI Backend

```powershell
# Start the API server
python -m app.main
```

You should see:
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 7: (Optional) Run Streamlit Dashboard

Open a **new** PowerShell terminal in the project directory:

```powershell
# Activate virtual environment in new terminal
venv\Scripts\activate

# Run Streamlit app
streamlit run streamlit_app.py
```

Streamlit will open at `http://localhost:8501`

---

## macOS/Linux Setup

### Step 1: Navigate to Project Directory

```bash
cd ~/Desktop/SEOTool
# or wherever you placed the project
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### Step 4: Create Environment File

```bash
# Copy template
cp .env.example .env

# Edit with your editor
nano .env
# or
vim .env
# or
code .env  # if VS Code installed
```

### Step 5: Configure Credentials

Same as Windows (see above).

### Step 6: Run FastAPI Backend

```bash
# Start the API server
python -m app.main
```

### Step 7: (Optional) Run Streamlit Dashboard

Open a new terminal:

```bash
# Navigate to project
cd ~/Desktop/SEOTool

# Activate virtual environment
source venv/bin/activate

# Run Streamlit
streamlit run streamlit_app.py
```

---

## Configuration

### OpenAI API Setup

1. **Create OpenAI Account**
   - Go to [platform.openai.com](https://platform.openai.com)
   - Sign up or log in
   - Navigate to API keys section

2. **Create API Key**
   - Click "Create new secret key"
   - Copy the key (shown once)
   - Paste into `.env` as `OPENAI_API_KEY`

3. **Check Billing**
   - Ensure you have credits
   - Go to Billing → Usage to track costs
   - Set usage limits if desired

### Verify OpenAI Setup

Test your API key:

```bash
# Activate virtual environment first
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run test
python -c "
import openai
from app.config import settings
print('API Key configured:', bool(settings.OPENAI_API_KEY))
print('Model:', settings.OPENAI_MODEL)
"
```

---

## Running the Application

### Start FastAPI Backend

```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run server
python -m app.main
```

### API Endpoints (Backend Only)

Test using curl or Postman:

```bash
# Health check
curl http://localhost:8000/health

# API documentation
curl http://localhost:8000/docs  # Swagger UI
curl http://localhost:8000/redoc # ReDoc
```

### Start Streamlit Dashboard (Optional)

```bash
# In a new terminal, activate venv and run:
streamlit run streamlit_app.py
```

### Full Workflow

1. **Start FastAPI** (Terminal 1)
2. **Start Streamlit** (Terminal 2)
3. Open Streamlit at `http://localhost:8501`
4. Enter your niche and keyword
5. Click "Generate Topics"
6. Select a topic
7. Click "Generate Outline"
8. Click "Generate Content"
9. (Optional) Publish to WordPress

---

## Verification

### Check Installation

Verify all components are working:

```python
# Create test_setup.py
import sys

print("Python:", sys.version)

try:
    import fastapi
    print("✓ FastAPI installed")
except ImportError:
    print("✗ FastAPI not installed")

try:
    import openai
    print("✓ OpenAI installed")
except ImportError:
    print("✗ OpenAI not installed")

try:
    import streamlit
    print("✓ Streamlit installed")
except ImportError:
    print("✗ Streamlit not installed")

try:
    from app.config import settings
    print("✓ Configuration loaded")
    if settings.OPENAI_API_KEY:
        print("✓ OpenAI API Key configured")
    else:
        print("✗ OpenAI API Key NOT configured")
except Exception as e:
    print(f"✗ Configuration error: {e}")
```

Run it:
```bash
python test_setup.py
```

### Test API Endpoints

```bash
# Activate venv and start the server (if not already running)
python -m app.main

# In another terminal:

# Test 1: Health check
curl http://localhost:8000/health

# Test 2: Generate topics
curl -X POST http://localhost:8000/api/generate-topics \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "Technology",
    "primary_keyword": "AI Tools",
    "target_audience": "Developers",
    "tone": "professional"
  }'
```

---

## WordPress Setup (Optional)

### If You Want to Publish Posts to WordPress

#### 1. Prerequisites

- Existing WordPress site (self-hosted or managed)
- Admin access to WordPress dashboard
- WordPress 6.0+ recommended

#### 2. Enable REST API

REST API is usually enabled by default, but verify:

1. Go to WordPress Dashboard
2. Settings → Permalinks
3. Ensure "Post name" or another option is selected (not Plain)
4. Click "Save Changes"

#### 3. Create Application Password

1. Go to WordPress Dashboard
2. Users → Your Profile
3. Scroll to "Application Passwords"
4. Enter App Name: `SEO Content Tool`
5. Click "Add New Application Password"
6. Copy the generated password
7. Add to `.env`:

```env
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=PASSWORD_FROM_STEP_6
```

#### 4. Test WordPress Connection

```bash
# Make sure FastAPI is running

# Test connection
curl http://localhost:8000/api/wordpress/status
```

Expected response:
```json
{
  "status": "connected",
  "wordpress_url": "https://your-site.com",
  "message": "Successfully connected to WordPress"
}
```

---

## Troubleshooting

### Common Issues

#### Python Not Found
```
Error: 'python' is not recognized
```

**Solution**: 
- Windows: Use `python` or `py`
- Add Python to PATH in Windows (Reinstall Python with "Add Python to PATH" checked)

#### Module Not Found (e.g., `ModuleNotFoundError: No module named 'fastapi'`)

**Solution**:
```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### OpenAI API Error

```
Error: OpenAI API error: Invalid API Key
```

**Solution**:
- Verify API key in `.env` is correct
- Check at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Ensure you have available credits

#### Cannot Connect to Backend

```
Cannot connect to API at http://localhost:8000
```

**Solution**:
- Ensure FastAPI is running: `python -m app.main`
- Check port 8000 is not in use: `netstat -an | findstr :8000` (Windows)
- Try different port in `.env`: `API_PORT=8001`

#### WordPress Connection Failed

**Solution**:
- Verify URL is correct and accessible
- Check username and app password are correct
- Ensure REST API is enabled
- Use HTTPS (not HTTP) for WordPress URL

#### OpenAI Timeout

```
Error: Request timed out
```

**Solution**:
- Reduce `word_count` setting
- Try again (API may be temporarily slow)
- Check internet connection

---

## Quick Reference

### Common Commands

```bash
# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Start FastAPI server
python -m app.main

# Start Streamlit dashboard
streamlit run streamlit_app.py

# View API docs
# Browser: http://localhost:8000/docs

# Run tests
python test_setup.py
```

### Key Directories

- **App code**: `app/`
- **Routes**: `app/routes/`
- **Services**: `app/services/`
- **Config**: `app/config.py`
- **Environment**: `.env`
- **Dependencies**: `requirements.txt`

---

## Next Steps

1. ✅ Complete setup from above
2. 🧪 Test API endpoints
3. 🎨 Use Streamlit dashboard or API directly
4. 📝 Generate your first article
5. 🚀 Optimize and customize prompts
6. 📤 (Optional) Publish to WordPress
7. 📊 Monitor and track results

---

## Support

If you encounter issues:

1. **Check logs**: Look at `app.log` or console output
2. **Review configuration**: Verify `.env` is correct
3. **Test components individually**: Start backend, test API
4. **Check dependencies**: `pip list | grep -E "fastapi|openai|streamlit"`
5. **Consult documentation**:
   - FastAPI: https://fastapi.tiangolo.com
   - OpenAI: https://platform.openai.com/docs
   - Streamlit: https://docs.streamlit.io

---

**Ready to generate amazing content! 🚀**
