# Production Deployment Guide

Guide for deploying the SEO Content Tool to production environments.

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Security Considerations](#security-considerations)
3. [Performance Optimization](#performance-optimization)
4. [Monitoring and Logging](#monitoring-and-logging)
5. [Docker Deployment](#docker-deployment)
6. [Cloud Deployment Options](#cloud-deployment-options)

## Environment Setup

### Production Environment Variables

Create a `.env.production` file:

```env
# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# OpenAI Configuration
OPENAI_API_KEY=sk-your-production-key
OPENAI_MODEL=gpt-4-turbo

# WordPress Configuration
WORDPRESS_URL=https://your-production-wordpress.com
WORDPRESS_USERNAME=production_user
WORDPRESS_APP_PASSWORD=your_app_password

# Security
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Rate Limiting
RATE_LIMIT_CALLS=100
RATE_LIMIT_PERIOD=60

# Logging
LOG_LEVEL=info
LOG_FILE=/var/log/seo-content-tool/app.log
```

### Database Configuration (Optional)

For production deployments with caching:

```bash
# PostgreSQL for caching
pip install psycopg2-binary sqlalchemy

# Redis for session management
pip install redis
```

## Security Considerations

### 1. API Keys and Secrets

```python
# Use environment variables, never hardcode
from app.config import settings

# Access from environment
api_key = settings.OPENAI_API_KEY
```

**Production Best Practices:**
- Store secrets in AWS Secrets Manager, Google Secret Manager, or HashiCorp Vault
- Rotate keys regularly
- Use service accounts/IAM roles instead of personal API keys
- Enable API key restrictions in OpenAI dashboard

### 2. CORS Configuration

Update `app/main.py` for production:

```python
from fastapi.middleware.cors import CORSMiddleware

# Specific allowed origins
allowed_origins = [
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # NOT ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 3. Rate Limiting

Implement rate limiting to prevent abuse:

```bash
pip install slowapi
```

### 4. HTTPS/SSL

Always use HTTPS in production:

```bash
# Using Nginx as reverse proxy
# Or use Let's Encrypt for free SSL certificates

certbot certonly --standalone -d yourdomain.com
```

### 5. Input Validation

All inputs are validated with Pydantic (already implemented), but ensure:
- Max lengths are enforced
- Content injection is prevented
- XSS protection is enabled

## Performance Optimization

### 1. Caching

```python
# Add caching for frequently generated topics
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_topics(niche: str, keyword: str):
    # Generate topics once and cache
    pass
```

### 2. Database Indexing

For generated content storage:

```sql
-- PostgreSQL indexes
CREATE INDEX idx_topic_keyword ON content(topic, keyword);
CREATE INDEX idx_created_date ON content(created_date);
```

### 3. Load Balancing

```bash
# Multiple Uvicorn workers with Gunicorn
pip install gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app \
  --bind 127.0.0.1:8000
```

### 4. Content Streaming

For large content responses:

```python
from fastapi.responses import StreamingResponse

@app.get("/stream-content")
async def stream_content():
    return StreamingResponse(generate_content_stream())
```

## Monitoring and Logging

### 1. Structured Logging

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        return json.dumps(log_data)
```

### 2. Error Tracking

Use Sentry for error tracking:

```bash
pip install sentry-sdk

import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

### 3. Metrics Collection

Use Prometheus for metrics:

```bash
pip install prometheus-client
```

### 4. Health Checks

Already implemented at `/health` endpoint. Use for:
- Kubernetes readiness probes
- Load balancer health checks
- Monitoring dashboards

## Docker Deployment

### Dockerfile

```dockerfile
# Multi-stage build
FROM python:3.10-slim as builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - WORDPRESS_URL=${WORDPRESS_URL}
      - WORDPRESS_USERNAME=${WORDPRESS_USERNAME}
      - WORDPRESS_APP_PASSWORD=${WORDPRESS_APP_PASSWORD}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=seo_content_tool
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

## Cloud Deployment Options

### AWS (Elastic Beanstalk)

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.10 seo-content-tool

# Create environment
eb create production-env

# Deploy
eb deploy
```

### Google Cloud Run

```bash
# Build and push Docker image
gcloud builds submit --tag gcr.io/PROJECT_ID/seo-content-tool

# Deploy
gcloud run deploy seo-content-tool \
  --image gcr.io/PROJECT_ID/seo-content-tool \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=${OPENAI_API_KEY}
```

### Heroku

```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Push to Heroku
git push heroku main
```

### AWS Lambda (Serverless)

```bash
pip install mangum

# In app/main.py
from mangum import Mangum

handler = Mangum(app)
```

## CI/CD Pipeline

### GitHub Actions

`.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker image
        run: |
          docker build -t seo-content-tool:latest .
          docker push gcr.io/${{ secrets.GCP_PROJECT }}/seo-content-tool:latest
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy seo-content-tool \
            --image gcr.io/${{ secrets.GCP_PROJECT }}/seo-content-tool:latest
```

## Scaling Strategies

### 1. Horizontal Scaling

Use load balancers with multiple instances:
- AWS ELB/ALB
- Google Cloud Load Balancer
- Nginx

### 2. Vertical Scaling

Increase instance resources:
- CPU cores
- Memory
- GPU (for AI model inference)

### 3. Content Generation Queue

For high volume:

```bash
pip install celery

# async task for long-running content generation
@app.post("/generate-content-async")
async def generate_content_async(request: ContentRequest):
    task = celery_app.send_task(
        'tasks.generate_content',
        args=[request.dict()]
    )
    return {"task_id": task.id}
```

## Database Schema (If Storing Generated Content)

```sql
CREATE TABLE generated_content (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    keyword VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    html_content TEXT,
    meta_title VARCHAR(60),
    meta_description VARCHAR(160),
    word_count INT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_topic_keyword (topic, keyword),
    INDEX idx_created_date (created_at)
);

CREATE TABLE publish_history (
    id SERIAL PRIMARY KEY,
    content_id INT REFERENCES generated_content(id),
    wordpress_post_id INT,
    wordpress_url VARCHAR(255),
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_content_id (content_id)
);
```

## Monitoring Checklist

- [ ] API response times monitored
- [ ] Error rate tracked
- [ ] Database performance optimized
- [ ] OpenAI API costs monitored
- [ ] Disk space monitored
- [ ] CPU/Memory usage tracked
- [ ] SSL certificate expiration monitored
- [ ] Backup system implemented
- [ ] Disaster recovery plan tested
- [ ] Security audit completed

## Maintenance

### Regular Tasks

- [ ] Monthly security updates
- [ ] Weekly log rotation
- [ ] Quarterly dependency updates
- [ ] Annual security audit
- [ ] Monthly cost review

### Rollback Procedure

```bash
# Using Docker tags
docker pull seo-content-tool:v1.0.0
docker run -d seo-content-tool:v1.0.0

# Using Git
git revert commit-hash
git push
```

---

For more information, see README.md and SETUP.md
