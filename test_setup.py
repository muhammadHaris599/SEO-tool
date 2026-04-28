"""
Comprehensive Testing Script for SEO Content Tool
Tests all components and provides diagnostic information.
"""

import sys
import subprocess
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text):
    """Print section header."""
    print(f"\n{Colors.BLUE}{'=' * 60}")
    print(f"{text.center(60)}")
    print('=' * 60 + Colors.END)


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_info(text):
    """Print info message."""
    print(f"ℹ {text}")


def test_python_version():
    """Test Python version."""
    print_header("Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"Python: {version_str}")
    
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version_str} is compatible")
        return True
    else:
        print_error(f"Python 3.10+ required, found {version_str}")
        return False


def test_dependencies():
    """Test required dependencies."""
    print_header("Dependencies Check")
    
    dependencies = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "pydantic": "Pydantic",
        "openai": "OpenAI",
        "httpx": "httpx",
        "dotenv": "python-dotenv",
        "streamlit": "Streamlit",
        "requests": "Requests"
    }
    
    all_installed = True
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} NOT installed")
            all_installed = False
    
    return all_installed


def test_environment_file():
    """Test environment file exists."""
    print_header("Environment Configuration")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_example_path.exists():
        print_success(".env.example exists")
    else:
        print_error(".env.example NOT found")
        return False
    
    if env_path.exists():
        print_success(".env file exists")
        
        # Check if API key is configured
        try:
            from dotenv import dotenv_values
            config = dotenv_values(".env")
            
            if config.get("OPENAI_API_KEY"):
                key = config.get("OPENAI_API_KEY")
                key_preview = key[:10] + "..." + key[-4:] if len(key) > 14 else "***"
                print_success(f"OpenAI API Key configured: {key_preview}")
                return True
            else:
                print_warning("OpenAI API Key NOT configured")
                return False
        except Exception as e:
            print_error(f"Error reading .env: {str(e)}")
            return False
    else:
        print_warning(".env file NOT found")
        print_info("Run: cp .env.example .env")
        return False


def test_project_structure():
    """Test project structure."""
    print_header("Project Structure")
    
    required_dirs = [
        "app",
        "app/routes",
        "app/services",
        "app/models"
    ]
    
    required_files = [
        "app/main.py",
        "app/config.py",
        "app/models.py",
        "app/routes/topics.py",
        "app/routes/outline.py",
        "app/routes/content.py",
        "app/routes/wordpress.py",
        "app/services/openai_service.py",
        "app/services/seo_prompts.py",
        "requirements.txt",
        "README.md",
        "SETUP.md",
        "QUICKSTART.md"
    ]
    
    all_exist = True
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print_success(f"Directory: {dir_path}")
        else:
            print_error(f"Directory NOT found: {dir_path}")
            all_exist = False
    
    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"File: {file_path}")
        else:
            print_error(f"File NOT found: {file_path}")
            all_exist = False
    
    return all_exist


def test_imports():
    """Test if all modules can be imported."""
    print_header("Module Imports")
    
    modules_to_test = [
        ("app.config", "Config module"),
        ("app.models", "Models module"),
        ("app.services.openai_service", "OpenAI service"),
        ("app.services.seo_prompts", "SEO prompts"),
        ("app.routes.topics", "Topics routes"),
        ("app.routes.outline", "Outline routes"),
        ("app.routes.content", "Content routes"),
        ("app.routes.wordpress", "WordPress routes"),
        ("app.main", "Main app")
    ]
    
    all_imported = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print_success(f"{description}: {module_name}")
        except Exception as e:
            print_error(f"{description}: {module_name}")
            print_info(f"  Error: {str(e)}")
            all_imported = False
    
    return all_imported


def test_openai_connection():
    """Test OpenAI API connection."""
    print_header("OpenAI API Connection")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from app.config import settings
        
        if not settings.OPENAI_API_KEY:
            print_error("OpenAI API Key not configured")
            return False
        
        print_success("API Key loaded")
        print_info(f"Model: {settings.OPENAI_MODEL}")
        
        # Try to import openai and check if it's configured
        import openai
        openai.api_key = settings.OPENAI_API_KEY
        
        print_success("OpenAI library configured")
        print_info("Note: Full API test requires making an actual API call")
        
        return True
    
    except Exception as e:
        print_error(f"OpenAI configuration error: {str(e)}")
        return False


def test_api_server():
    """Test if API server can start."""
    print_header("API Server Check")
    
    try:
        from app.main import app
        print_success("FastAPI application loaded")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        
        if response.status_code == 200:
            print_success("Health endpoint accessible")
            return True
        else:
            print_error(f"Health endpoint returned: {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"API server error: {str(e)}")
        return False


def test_streamlit():
    """Test Streamlit installation."""
    print_header("Streamlit Check")
    
    try:
        import streamlit
        print_success("Streamlit installed")
        print_info(f"Version: {streamlit.__version__}")
        
        # Check if streamlit app file exists
        if Path("streamlit_app.py").exists():
            print_success("Streamlit app file exists")
            return True
        else:
            print_error("streamlit_app.py NOT found")
            return False
    
    except ImportError:
        print_error("Streamlit NOT installed")
        return False
    except Exception as e:
        print_error(f"Streamlit error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print(f"\n{Colors.BLUE}")
    print("╔" + "=" * 58 + "╗")
    print("║ SEO Content Tool - System Diagnostics".ljust(59) + "║")
    print("╚" + "=" * 58 + "╝")
    print(Colors.END)
    
    results = {
        "Python Version": test_python_version(),
        "Dependencies": test_dependencies(),
        "Project Structure": test_project_structure(),
        "Module Imports": test_imports(),
        "Environment Configuration": test_environment_file(),
        "OpenAI API": test_openai_connection(),
        "API Server": test_api_server(),
        "Streamlit": test_streamlit()
    }
    
    # Summary
    print_header("Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status}{Colors.END} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print(Colors.GREEN + "✓ All systems operational!" + Colors.END)
        print("\nNext steps:")
        print("1. Run: python -m app.main  (FastAPI server)")
        print("2. Open: http://localhost:8000/docs (API documentation)")
        print("3. Run: streamlit run streamlit_app.py  (UI dashboard)")
        return 0
    else:
        print(Colors.RED + "✗ Some tests failed" + Colors.END)
        print("\nPlease fix the issues above and run this test again.")
        print("\nFor help, see:")
        print("- SETUP.md - Detailed setup instructions")
        print("- README.md - Documentation")
        print("- QUICKSTART.md - Quick reference")
        return 1


if __name__ == "__main__":
    sys.exit(main())
