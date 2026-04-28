"""
Directory Guide and File Index
Complete overview of all files and their purposes
"""

import json
from pathlib import Path
from typing import Dict, List


class DirectoryGuide:
    """Guide to the SEO Content Tool project structure."""
    
    def __init__(self):
        self.base_path = Path(".")
    
    def get_structure(self) -> Dict:
        """Get the complete project structure."""
        return {
            "root": {
                "description": "Project root directory",
                "files": {
                    ".env.example": "Environment variables template (COPY THIS TO .env)",
                    ".env": "Your API keys and configuration (DO NOT COMMIT)",
                    "requirements.txt": "Python package dependencies",
                    "README.md": "Main documentation and API reference",
                    "SETUP.md": "Step-by-step setup instructions",
                    "QUICKSTART.md": "5-minute quick start guide",
                    "PRODUCTION.md": "Production deployment guide",
                    "INDEX.md": "This file - complete project overview",
                    "make.bat": "Windows helper script (make install, make run, etc.)",
                    "make": "Linux/macOS helper script",
                    "test_setup.py": "System diagnostics and testing script",
                    "example_usage.py": "Python example showing full workflow",
                    "api_examples.py": "API endpoint examples with cURL/Python",
                }
            },
            "app": {
                "description": "Main application code",
                "structure": {
                    "__init__.py": "Package initialization",
                    "main.py": "FastAPI application entry point",
                    "config.py": "Configuration management and settings",
                    "models.py": "Pydantic models for request/response validation",
                    "routes": {
                        "description": "API endpoint handlers",
                        "files": {
                            "__init__.py": "Routes package initialization",
                            "topics.py": "POST /api/generate-topics endpoint",
                            "outline.py": "POST /api/generate-outline endpoint",
                            "content.py": "POST /api/generate-content endpoint",
                            "wordpress.py": "POST /api/publish & GET /api/wordpress/status endpoints",
                        }
                    },
                    "services": {
                        "description": "Business logic and external service integration",
                        "files": {
                            "__init__.py": "Services package initialization",
                            "openai_service.py": "OpenAI API integration and async wrapper",
                            "seo_prompts.py": "SEO-optimized prompt templates",
                        }
                    },
                    "models": {
                        "description": "Data models package",
                        "files": {
                            "__init__.py": "Models package initialization",
                        }
                    }
                }
            }
        }
    
    def get_file_descriptions(self) -> Dict[str, str]:
        """Get detailed descriptions of important files."""
        return {
            "README.md": """
Main Documentation
- Complete feature overview
- API endpoints documentation
- Usage examples (cURL, Python)
- Configuration reference
- Error handling
- Performance optimization
- Production deployment basics
START HERE for understanding the tool
            """,
            
            "SETUP.md": """
Detailed Setup Instructions
- Windows setup (Python, venv, dependencies)
- macOS/Linux setup
- Environment configuration
- OpenAI API setup
- WordPress setup (optional)
- Verification procedures
- Troubleshooting guide
START HERE for installation
            """,
            
            "QUICKSTART.md": """
5-Minute Quick Start
- Quick prerequisites check
- Setup in 5 commands
- Running the server
- First API call
- Quick troubleshooting
FASTEST WAY TO GET STARTED
            """,
            
            "PRODUCTION.md": """
Production Deployment Guide
- Security best practices
- Performance optimization
- Docker deployment
- Cloud platforms (AWS, GCP, Heroku)
- CI/CD pipeline setup
- Monitoring and logging
- Scaling strategies
USE THIS FOR PRODUCTION DEPLOYMENT
            """,
            
            "app/main.py": """
FastAPI Application
- Initializes FastAPI app
- Configures middleware (CORS)
- Includes all routes
- Error handling
- Startup/shutdown events
- Health check endpoint
CORE APPLICATION FILE
            """,
            
            "app/config.py": """
Configuration Management
- Loads environment variables from .env
- Validates required settings
- Settings classes and properties
- WordPress authentication helpers
- Rate limiting configuration
HANDLES ALL CONFIGURATION
            """,
            
            "app/models.py": """
Pydantic Data Models
- Request validation models
- Response models
- Ensures data consistency
- Type hints for IDE support
- Automatic API documentation
DATA VALIDATION & DOCUMENTATION
            """,
            
            "app/routes/topics.py": """
Topic Generation Endpoint
- POST /api/generate-topics
- Generates 10 SEO topics
- Uses OpenAI API
- Returns list of topics
FIRST STEP IN CONTENT PIPELINE
            """,
            
            "app/routes/outline.py": """
Outline Generation Endpoint
- POST /api/generate-outline
- Creates structured outlines
- Parses H1/H2/H3 structure
- Generates FAQ questions
SECOND STEP IN CONTENT PIPELINE
            """,
            
            "app/routes/content.py": """
Content Generation Endpoint
- POST /api/generate-content
- Generates full articles
- Creates HTML formatted content
- Generates meta tags
- Counts words
THIRD STEP IN CONTENT PIPELINE
            """,
            
            "app/routes/wordpress.py": """
WordPress Integration
- POST /api/publish
- Publishes to WordPress REST API
- Handles authentication
- Returns post ID and link
- GET /api/wordpress/status for connection check
PUBLISHING ENDPOINT
            """,
            
            "app/services/openai_service.py": """
OpenAI API Integration
- Async wrapper for OpenAI
- Handles API calls
- Error handling
- Rate limiting
- Temperature configuration
OPENAI INTEGRATION LAYER
            """,
            
            "app/services/seo_prompts.py": """
SEO Prompt Templates
- High-quality prompt engineering
- Topic generation prompts
- Outline generation prompts
- Content generation prompts
- Customizable for your needs
PROMPT TEMPLATES - CUSTOMIZE HERE
            """,
            
            "test_setup.py": """
System Diagnostics
- Checks Python version
- Verifies dependencies
- Tests project structure
- Tests module imports
- Validates environment config
- Tests API server
- Tests Streamlit
RUN THIS TO VERIFY INSTALLATION
            """,
            
            "example_usage.py": """
Python API Usage Example
- Demonstrates full workflow
- Shows how to use client
- Generates topics, outline, content
- Optional WordPress publishing
- Saves content to file
RUN THIS TO TEST THE WORKFLOW
            """,
            
            "api_examples.py": """
API Endpoint Examples
- cURL-style examples
- Python requests examples
- All endpoints covered
- Full workflow example
- Error handling examples
USE THIS AS API REFERENCE
            """,
            
            "streamlit_app.py": """
Streamlit Dashboard UI
- User-friendly interface
- Step-by-step workflow
- Interactive content preview
- Direct WordPress publishing
- Download generated content
ALTERNATIVE UI TO API
            """,
            
            "requirements.txt": """
Python Dependencies
- FastAPI & Uvicorn
- OpenAI
- httpx & Requests
- Pydantic
- Streamlit
- python-dotenv
INSTALL WITH: pip install -r requirements.txt
            """,
        }
    
    def get_workflow(self) -> str:
        """Get the workflow from start to finish."""
        return """
COMPLETE WORKFLOW
=================

1. SETUP (Do Once)
   - Copy .env.example to .env
   - Add OpenAI API key to .env
   - Run: pip install -r requirements.txt
   - Optional: Add WordPress credentials to .env

2. RUN BACKEND
   - Terminal 1: python -m app.main
   - Runs on http://localhost:8000

3. RUN FRONTEND (OPTIONAL)
   - Terminal 2: streamlit run streamlit_app.py
   - Opens at http://localhost:8501

4. USE THE TOOL - Option A: Streamlit UI
   - Enter niche and keyword
   - Click "Generate Topics"
   - Select a topic
   - Click "Generate Outline"
   - Click "Generate Content"
   - Optional: Click "Publish to WordPress"

5. USE THE TOOL - Option B: API
   - Use curl or Python requests
   - POST /api/generate-topics
   - POST /api/generate-outline
   - POST /api/generate-content
   - POST /api/publish
   - See README.md for examples

6. USE THE TOOL - Option C: Python Script
   - Run: python example_usage.py
   - Or customize for your needs

7. ITERATE
   - Modify prompts in app/services/seo_prompts.py
   - Customize writing tone/audience
   - Generate more content
   - Publish to WordPress
"""
    
    def get_quick_commands(self) -> str:
        """Get quick reference commands."""
        return """
QUICK COMMANDS
==============

WINDOWS:
  Setup:        make setup
  Install:      make install
  Run Backend:  make run
  Run Streamlit: make streamlit
  Test:         make test
  Example:      make example
  Clean:        make clean

macOS/LINUX:
  Setup:        ./make setup
  Install:      ./make install
  Run Backend:  ./make run
  Run Streamlit: ./make streamlit
  Test:         ./make test
  Example:      ./make example
  Clean:        ./make clean

MANUAL:
  Create venv:           python -m venv venv
  Activate (Windows):    venv\\Scripts\\activate
  Activate (Unix):       source venv/bin/activate
  Install deps:          pip install -r requirements.txt
  Run server:            python -m app.main
  Run Streamlit:         streamlit run streamlit_app.py
  Run tests:             python test_setup.py
  Run example:           python example_usage.py

API ENDPOINTS:
  Topics:     POST http://localhost:8000/api/generate-topics
  Outline:    POST http://localhost:8000/api/generate-outline
  Content:    POST http://localhost:8000/api/generate-content
  Publish:    POST http://localhost:8000/api/publish
  Docs:       GET  http://localhost:8000/docs
  Health:     GET  http://localhost:8000/health
"""
    
    def print_guide(self):
        """Print the complete guide."""
        print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║          SEO CONTENT TOOL - COMPLETE PROJECT GUIDE             ║
║                                                                ║
║     AI-Powered Content Generation with WordPress Integration   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """)
        
        # Project Structure
        print("\n" + "="*60)
        print("PROJECT STRUCTURE")
        print("="*60)
        
        structure = self.get_structure()
        
        print("\nROOT FILES:")
        for filename, desc in structure["root"]["files"].items():
            print(f"  • {filename:<25} - {desc}")
        
        print("\nAPP/ DIRECTORY (Main Application):")
        for filename, desc in structure["app"]["structure"].items():
            if isinstance(desc, str):
                print(f"  • {filename:<30} - {desc}")
            else:
                print(f"  • {filename}/")
                for subfile, subdesc in desc.get("files", {}).items():
                    print(f"    - {subfile:<25} - {subdesc}")
        
        # File Descriptions
        print("\n" + "="*60)
        print("IMPORTANT FILES EXPLAINED")
        print("="*60)
        
        descriptions = self.get_file_descriptions()
        for filename, desc in descriptions.items():
            print(f"\n{filename}:")
            print(desc.strip())
        
        # Workflow
        print("\n" + "="*60)
        print("COMPLETE WORKFLOW")
        print("="*60)
        print(self.get_workflow())
        
        # Quick Commands
        print("\n" + "="*60)
        print("QUICK REFERENCE")
        print("="*60)
        print(self.get_quick_commands())
        
        # Usage Examples
        print("\n" + "="*60)
        print("GETTING STARTED")
        print("="*60)
        print("""
1. FIRST TIME SETUP:
   - Read: QUICKSTART.md (5 minutes)
   - Run: python test_setup.py (verify installation)
   - Run: python example_usage.py (test workflow)

2. WANT TO USE THE UI?
   - Run: python -m app.main (Terminal 1)
   - Run: streamlit run streamlit_app.py (Terminal 2)
   - Open: http://localhost:8501

3. WANT TO USE THE API?
   - Run: python -m app.main (Terminal 1)
   - Read: api_examples.py (see examples)
   - Or use cURL/Postman with examples from README.md

4. WANT TO CUSTOMIZE?
   - Edit: app/services/seo_prompts.py
   - Edit: app/config.py for settings
   - Edit: app/routes/*.py for endpoints

5. WANT TO DEPLOY?
   - Read: PRODUCTION.md
   - Choose: Docker, AWS, GCP, Heroku
   - Follow: Deployment instructions

6. NEED HELP?
   - Check: README.md (comprehensive reference)
   - Check: SETUP.md (troubleshooting section)
   - Check: app/ code comments
        """)
        
        # Next Steps
        print("\n" + "="*60)
        print("NEXT STEPS")
        print("="*60)
        print("""
NOW:
  [ ] Copy .env.example to .env
  [ ] Add your OpenAI API key
  [ ] Run: python test_setup.py
  [ ] Run: python example_usage.py

SOON:
  [ ] Try the Streamlit UI
  [ ] Generate some test articles
  [ ] Customize the prompts
  [ ] Configure WordPress (optional)

LATER:
  [ ] Set up production deployment
  [ ] Monitor API usage and costs
  [ ] Optimize performance
  [ ] Scale infrastructure

DOCUMENTATION MAP:
  START HERE ──> QUICKSTART.md (5 min)
         │
         └──> SETUP.md (detailed setup)
         │
         ├──> README.md (full reference)
         │
         ├──> api_examples.py (API examples)
         │
         └──> PRODUCTION.md (deployment)
        """)
        
        print("\n" + "="*60)
        print("✅ SETUP COMPLETE!")
        print("="*60)
        print("\nYou're ready to start. Good luck! 🚀\n")


if __name__ == "__main__":
    guide = DirectoryGuide()
    guide.print_guide()
