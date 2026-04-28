# SEO Content Automation Tool

**An AI-powered platform for generating SEO-optimized content and publishing directly to WordPress.**

## Overview

This tool leverages OpenAI's GPT-4 to automate the entire content creation pipeline:
- Generate topic ideas based on niche and keywords
- Create detailed content outlines
- Write full, SEO-optimized articles
- Publish directly to WordPress

Built with FastAPI backend and optional Streamlit UI for a complete production-ready solution.

## Features

### 🎯 Core Features

1. **AI Topic Generation**
   - Generate 10 SEO-optimized blog topics
   - Based on niche, keyword, target audience, and tone
   - Supports long-tail keywords and high-intent topics

2. **Content Outline Generation**
   - Hierarchical H1/H2/H3 structure
   - LSI keyword integration
   - FAQ section planning
   - Long-form content optimization

3. **AI Content Generation**
   - Full-length articles (500-5000 words)
   - HTML formatted output
   - Meta title and description generation
   - Multiple writing tones (Professional, Casual, Friendly, etc.)

4. **WordPress Integration**
   - Direct publishing to WordPress via REST API
   - Draft or publish status control
   - Meta tag integration
   - Tag and category support

5. **Streamlit Dashboard**
   - User-friendly interface
   - Step-by-step workflow
   - Content preview
   - Direct publishing from UI

## Tech Stack

- **Backend**: FastAPI with async/await support
- **AI**: OpenAI API (GPT-4-Turbo)
- **CMS**: WordPress REST API
- **Frontend**: Streamlit Dashboard (optional)
- **HTTP Client**: httpx and Requests
- **ORM/Models**: Pydantic

## Project Structure

```
SEOTool/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── topics.py        # Topic generation endpoint
│   │   ├── outline.py       # Outline generation endpoint
│   │   ├── content.py       # Content generation endpoint
│   │   └── wordpress.py     # WordPress publishing endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── openai_service.py    # OpenAI API integration
│   │   └── seo_prompts.py       # Prompt templates
│   └── models/
│       └── __init__.py
├── streamlit_app.py         # Streamlit UI dashboard
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Environment variables (DO NOT commit)
├── README.md               # This file
└── SETUP.md                # Detailed setup instructions
```

## Installation & Setup

### Prerequisites

- Python 3.10+
- OpenAI API Key ([get one here](https://platform.openai.com/api-keys))
- (Optional) WordPress site with REST API enabled

### Quick Start

1. **Clone/Download the project**
```bash
cd C:\Users\wahab.ikram\Desktop\SEOTool
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the template
copy .env.example .env

# Edit .env and add your credentials
# Required:
#   - OPENAI_API_KEY
# Optional:
#   - WORDPRESS_URL
#   - WORDPRESS_USERNAME
#   - WORDPRESS_APP_PASSWORD
```

5. **Run FastAPI backend**
```bash
python -m app.main
```
The API will start at `http://localhost:8000`

6. **(Optional) Run Streamlit dashboard**
```bash
streamlit run streamlit_app.py
```
The dashboard will open at `http://localhost:8501`

## API Endpoints

### Health Check
```
GET /health
GET /
```
Returns application status.

### Generate Topics
```
POST /api/generate-topics
```
**Request:**
```json
{
  "niche": "Digital Marketing",
  "primary_keyword": "SEO Best Practices 2024",
  "target_audience": "Small business owners",
  "tone": "professional"
}
```
**Response:**
```json
{
  "topics": [
    "10 SEO Best Practices That Drive Real Results in 2024",
    "The Complete Guide to Technical SEO for Beginners",
    ...
  ],
  "keyword": "SEO Best Practices 2024"
}
```

### Generate Outline
```
POST /api/generate-outline
```
**Request:**
```json
{
  "topic": "10 SEO Best Practices That Drive Real Results in 2024",
  "primary_keyword": "SEO Best Practices 2024",
  "target_audience": "Small business owners"
}
```
**Response:**
```json
{
  "topic": "...",
  "outline": [
    {
      "heading": "SEO Best Practices 2024",
      "level": 1,
      "description": null
    },
    {
      "heading": "Why SEO Matters in 2024",
      "level": 2,
      "description": null
    },
    ...
  ],
  "faq_questions": [
    "What are the most important SEO factors?",
    "How long does it take to see SEO results?",
    ...
  ]
}
```

### Generate Content
```
POST /api/generate-content
```
**Request:**
```json
{
  "topic": "10 SEO Best Practices That Drive Real Results in 2024",
  "primary_keyword": "SEO Best Practices 2024",
  "outline": [...],
  "word_count": 2000,
  "target_audience": "Small business owners",
  "tone": "professional"
}
```
**Response:**
```json
{
  "topic": "...",
  "content": {
    "html": "<h1>...</h1><p>...</p>...",
    "plain_text": "...",
    "word_count": 2045,
    "meta_title": "10 SEO Best Practices That Drive Real Results in 2024",
    "meta_description": "Learn the 10 most important SEO best practices that will drive real results for your business in 2024."
  },
  "status": "success"
}
```

### Publish to WordPress
```
POST /api/publish
```
**Request:**
```json
{
  "title": "10 SEO Best Practices That Drive Real Results in 2024",
  "content": "<h1>...</h1><p>...</p>...",
  "meta_description": "Learn the 10 most important SEO best practices...",
  "status": "draft",
  "tags": ["SEO", "Marketing"],
  "categories": [1, 2]
}
```
**Response:**
```json
{
  "post_id": 123,
  "title": "10 SEO Best Practices That Drive Real Results in 2024",
  "link": "https://yoursite.com/10-seo-best-practices/",
  "status": "draft",
  "message": "Post published successfully as draft"
}
```

### Check WordPress Connection
```
GET /api/wordpress/status
```

## Configuration

### Environment Variables (.env)

```
# REQUIRED
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo

# OPTIONAL - WordPress Integration
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_app_password

# API Server
API_HOST=0.0.0.0
API_PORT=8000
```

### WordPress Setup (for publishing)

1. **Enable REST API** (usually enabled by default)
2. **Create Application Password**:
   - Go to Users → Your Profile
   - Scroll to "Application Passwords"
   - Create a new application password
   - Copy and save it to `.env`

## Usage Examples

### Using the API with cURL

```bash
# Generate topics
curl -X POST http://localhost:8000/api/generate-topics \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "SaaS",
    "primary_keyword": "Project Management Tools",
    "target_audience": "Developers",
    "tone": "professional"
  }'

# Generate outline
curl -X POST http://localhost:8000/api/generate-outline \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Best Project Management Tools for Developers",
    "primary_keyword": "Project Management Tools"
  }'

# Generate content
curl -X POST http://localhost:8000/api/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Best Project Management Tools for Developers",
    "primary_keyword": "Project Management Tools",
    "outline": [...],
    "word_count": 2000,
    "tone": "professional"
  }'

# Publish to WordPress
curl -X POST http://localhost:8000/api/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Best Project Management Tools for Developers",
    "content": "<h1>...</h1><p>...</p>",
    "meta_description": "...",
    "status": "draft"
  }'
```

### Using Python

```python
import requests

API_URL = "http://localhost:8000/api"

# Generate topics
response = requests.post(
    f"{API_URL}/generate-topics",
    json={
        "niche": "E-commerce",
        "primary_keyword": "Shopify vs WooCommerce",
        "target_audience": "E-commerce store owners",
        "tone": "professional"
    }
)
topics = response.json()["topics"]

# Generate outline
response = requests.post(
    f"{API_URL}/generate-outline",
    json={
        "topic": topics[0],
        "primary_keyword": "Shopify vs WooCommerce"
    }
)
outline = response.json()["outline"]

# Generate content
response = requests.post(
    f"{API_URL}/generate-content",
    json={
        "topic": topics[0],
        "primary_keyword": "Shopify vs WooCommerce",
        "outline": outline,
        "word_count": 2000,
        "tone": "professional"
    }
)
content = response.json()["content"]

# Publish to WordPress
response = requests.post(
    f"{API_URL}/publish",
    json={
        "title": topics[0],
        "content": content["html"],
        "meta_description": content["meta_description"],
        "status": "draft"
    }
)
print(response.json())
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `201`: Created (WordPress post)
- `400`: Bad Request (validation error)
- `401`: Unauthorized (authentication error)
- `500`: Internal Server Error (API errors)

Error responses include detailed messages:

```json
{
  "error": "Error message",
  "detail": "Detailed explanation",
  "status_code": 500
}
```

## Troubleshooting

### "Cannot connect to OpenAI API"
- Verify `OPENAI_API_KEY` is set correctly in `.env`
- Check your OpenAI account has credits
- Ensure you're using a valid API key from [platform.openai.com](https://platform.openai.com/api-keys)

### "WordPress connection failed"
- Verify WordPress is accessible at the configured URL
- Check WordPress username and app password are correct
- Enable REST API in WordPress settings
- Ensure HTTPS is properly configured

### "Streamlit not connecting to backend"
- Make sure FastAPI is running on `localhost:8000`
- Check if ports are not blocked by firewall
- Update `API_BASE_URL` in `.env` if using different host/port

### Content generation times out
- OpenAI API calls can take 1-2 minutes for full articles
- Ensure your internet connection is stable
- Try reducing `word_count` if having issues

## Advanced Configuration

### Custom Model Selection

Edit `config.py` to use different OpenAI models:

```python
OPENAI_MODEL=gpt-4  # Latest GPT-4
OPENAI_MODEL=gpt-4-turbo-preview  # GPT-4 Turbo
OPENAI_MODEL=gpt-3.5-turbo  # Faster, cheaper option
```

### Rate Limiting

Modify in `config.py`:

```python
RATE_LIMIT_CALLS = 10      # Requests per period
RATE_LIMIT_PERIOD = 60     # In seconds
```

### Custom Prompts

Edit `app/services/seo_prompts.py` to customize prompt templates for your specific use case.

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app \
  --bind 0.0.0.0:8000 \
  --log-level info
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t seo-tool .
docker run -p 8000:8000 --env-file .env seo-tool
```

### Environment Variables in Production

Use environment variable management:
- AWS Secrets Manager
- Google Cloud Secret Manager
- HashiCorp Vault
- Docker secrets

**Never commit `.env` file to version control.**

## Security Considerations

1. **API Keys**: Keep OpenAI API key private
2. **WordPress**: Use strong application passwords
3. **Rate Limiting**: Implement in production
4. **Input Validation**: All inputs are validated with Pydantic
5. **HTTPS**: Always use HTTPS in production
6. **CORS**: Configure allowed origins appropriately

## Performance Optimization

1. **Caching**: Implement Redis caching for frequently generated topics
2. **Async Processing**: Use Celery for background jobs
3. **Content Streaming**: Stream large content generation responses
4. **Rate Limiting**: Prevent API abuse

## Monitoring & Logging

Logs are written to:
- `app.log` - Application logs
- Console output - Real-time debugging

Configure log level in `main.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # Verbose logging
```

## API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review FastAPI documentation
3. Consult OpenAI API documentation
4. Check WordPress REST API documentation

## Future Enhancements

- [ ] Image generation integration
- [ ] Multi-language support
- [ ] Content scheduling
- [ ] A/B testing variations
- [ ] SEO analytics dashboard
- [ ] Competitor analysis
- [ ] Content calendar management
- [ ] Bulk content generation

---

**Happy content creation! 🚀**
