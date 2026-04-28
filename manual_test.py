"""
Manual test runner for SEO Content Tool - doesn't require pytest
Useful for quick validation of core functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BLUE}{'=' * 70}")
    print(f"{text.center(70)}")
    print('=' * 70 + Colors.END)


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def test_imports():
    """Test that all modules can be imported."""
    print_header("Testing Imports")
    
    modules = [
        "app.config",
        "app.models", 
        "app.main",
        "app.routes.topics",
        "app.routes.outline",
        "app.routes.content",
        "app.routes.wordpress",
        "app.services.openai_service",
        "app.services.seo_prompts"
    ]
    
    all_passed = True
    for module_name in modules:
        try:
            __import__(module_name)
            print_success(f"Import: {module_name}")
        except Exception as e:
            print_error(f"Failed to import {module_name}: {str(e)}")
            all_passed = False
    
    return all_passed


def test_config():
    """Test configuration loading."""
    print_header("Testing Configuration")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check for test environment
        os.environ["OPENAI_API_KEY"] = "test-key-sk-1234567890"
        
        from app.config import Settings
        settings = Settings()
        
        print_success("Settings initialized")
        print_success(f"OpenAI Model: {settings.OPENAI_MODEL}")
        print_success(f"API Host: {settings.API_HOST}:{settings.API_PORT}")
        print_success(f"Word Count (min/max): {settings.MIN_WORD_COUNT}/{settings.MAX_WORD_COUNT}")
        
        return True
    except Exception as e:
        print_error(f"Config test failed: {str(e)}")
        return False


def test_models():
    """Test data models."""
    print_header("Testing Data Models")
    
    try:
        from app.models import (
            TopicsRequest, TopicsResponse, 
            OutlineRequest, OutlineResponse,
            ContentRequest, ContentResponse,
            HealthResponse
        )
        
        # Test TopicsRequest
        topics_req = TopicsRequest(
            niche="Marketing",
            primary_keyword="SEO",
            target_audience="Business Owners",
            tone="Professional"
        )
        print_success("TopicsRequest created")
        
        # Test TopicsResponse
        topics_resp = TopicsResponse(
            topics=["Topic 1", "Topic 2"],
            keyword="SEO"
        )
        print_success("TopicsResponse created")
        
        # Test HealthResponse
        health = HealthResponse(
            status="healthy",
            message="API running",
            version="1.0.0"
        )
        print_success("HealthResponse created")
        
        print_success("All models working correctly")
        return True
    except Exception as e:
        print_error(f"Model test failed: {str(e)}")
        return False


def test_prompts():
    """Test SEO prompt generation."""
    print_header("Testing SEO Prompts")
    
    try:
        from app.services.seo_prompts import (
            get_topic_generation_prompt,
            get_outline_generation_prompt,
            get_content_generation_prompt
        )
        
        # Test topic prompt
        topic_prompt = get_topic_generation_prompt(
            niche="Tech",
            primary_keyword="AI",
            target_audience="Developers",
            tone="Casual"
        )
        assert len(topic_prompt) > 50
        print_success(f"Topic prompt generated ({len(topic_prompt)} chars)")
        
        # Test outline prompt
        outline_prompt = get_outline_generation_prompt(
            topic="AI Guide",
            depth="detailed",
            sections=5
        )
        assert len(outline_prompt) > 50
        print_success(f"Outline prompt generated ({len(outline_prompt)} chars)")
        
        # Test content prompt
        content_prompt = get_content_generation_prompt(
            topic="AI",
            outline=["Intro", "Body", "Conclusion"],
            word_count=2000,
            tone="Professional",
            seo_keywords=["AI", "ML"]
        )
        assert len(content_prompt) > 50
        print_success(f"Content prompt generated ({len(content_prompt)} chars)")
        
        return True
    except Exception as e:
        print_error(f"Prompt test failed: {str(e)}")
        return False


def test_fastapi():
    """Test FastAPI app initialization."""
    print_header("Testing FastAPI Application")
    
    try:
        from app.main import app
        
        # Check app properties
        assert app.title == "SEO Content Automation Tool"
        print_success(f"App title: {app.title}")
        
        assert app.version == "1.0.0"
        print_success(f"App version: {app.version}")
        
        # Check routes are registered
        routes = [route.path for route in app.routes]
        print_success(f"Routes registered: {len(routes)}")
        
        for path in ["/api/health", "/api/generate-topics", "/api/generate-outline", 
                     "/api/generate-content", "/api/publish-wordpress"]:
            if any(path in route for route in routes):
                print_success(f"  - {path}")
        
        return True
    except Exception as e:
        print_error(f"FastAPI test failed: {str(e)}")
        return False


def main():
    """Run all manual tests."""
    print_header("SEO Content Tool - Manual Test Suite")
    
    results = {
        "Imports": test_imports(),
        "Configuration": test_config(),
        "Data Models": test_models(),
        "SEO Prompts": test_prompts(),
        "FastAPI App": test_fastapi(),
    }
    
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\n{passed}/{total} test suites passed")
    
    if passed == total:
        print_success("\nAll tests passed! Your SEO tool is ready.")
        return 0
    else:
        print_error(f"\n{total - passed} test suite(s) failed. Check errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
