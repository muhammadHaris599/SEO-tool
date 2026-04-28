# Quick Start Guide

**Get your SEO Content Tool running in 5 minutes!**

## Prerequisites

- Python 3.10+ installed
- OpenAI API key (free at https://platform.openai.com/api-keys)

## Quick Setup

### 1. Navigate to Project

```bash
cd C:\Users\wahab.ikram\Desktop\SEOTool
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

**Windows:**
```bash
copy .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env  # or vim, or code
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-YOUR_KEY_HERE
OPENAI_MODEL=gpt-4-turbo
```

Save the file.

### 5. Start the Server

```bash
python -m app.main
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is running!**

### 6. (Optional) Start Streamlit UI

Open a new terminal in the same project directory:

```bash
# Activate venv again
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

streamlit run streamlit_app.py
```

The UI will open at `http://localhost:8501`

## Usage

### Option A: Use Streamlit Dashboard (Easy)

1. Go to `http://localhost:8501`
2. Enter your niche and keyword
3. Click "Generate Topics"
4. Select a topic
5. Click "Generate Outline"
6. Click "Generate Content"
7. (Optional) Publish to WordPress

### Option B: Use Python Script

```bash
# Activate venv
python example_usage.py
```

### Option C: Use cURL (Advanced)

```bash
# Generate topics
curl -X POST http://localhost:8000/api/generate-topics \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "Technology",
    "primary_keyword": "AI Tools",
    "target_audience": "Developers",
    "tone": "professional"
  }'
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Make sure venv is activated |
| `Invalid API Key` | Check `.env` file has correct key |
| `Cannot connect to API` | Make sure backend is running |
| `Timeout errors` | OpenAI may be slow, try again |

## Next Steps

1. ✅ Complete setup above
2. 🧪 Try the example script: `python example_usage.py`
3. 📝 Generate your first article
4. 🚀 Customize prompts in `app/services/seo_prompts.py`
5. 📤 Set up WordPress integration (optional)

## Full Documentation

- Setup details: See `SETUP.md`
- API reference: See `README.md`
- Code comments: See files in `app/`

## Need Help?

1. Check `SETUP.md` for detailed troubleshooting
2. Review `README.md` for API documentation
3. See comments in source code
4. Check FastAPI docs: https://fastapi.tiangolo.com
5. OpenAI docs: https://platform.openai.com/docs

---

**Happy content creation! 🚀**
