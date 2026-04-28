@echo off
REM SEO Content Tool - Windows Helper Scripts
REM Run commands easily from command line

if "%1"=="install" (
    echo Installing dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo Installation complete!
    goto end
)

if "%1"=="setup" (
    echo Setting up project...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    copy .env.example .env
    echo Setup complete! Edit .env with your API key, then run: make run
    goto end
)

if "%1"=="run" (
    echo Starting FastAPI server...
    call venv\Scripts\activate.bat
    python -m app.main
    goto end
)

if "%1"=="streamlit" (
    echo Starting Streamlit dashboard...
    call venv\Scripts\activate.bat
    streamlit run streamlit_app.py
    goto end
)

if "%1"=="test" (
    echo Running tests...
    call venv\Scripts\activate.bat
    python test_setup.py
    goto end
)

if "%1"=="example" (
    echo Running example...
    call venv\Scripts\activate.bat
    python example_usage.py
    goto end
)

if "%1"=="clean" (
    echo Cleaning up...
    rmdir /s /q __pycache__ 2>nul
    rmdir /s /q .pytest_cache 2>nul
    rmdir /s /q app\__pycache__ 2>nul
    rmdir /s /q app\routes\__pycache__ 2>nul
    rmdir /s /q app\services\__pycache__ 2>nul
    del /q *.log 2>nul
    echo Cleanup complete!
    goto end
)

if "%1"=="help" (
    echo SEO Content Tool - Windows Helper
    echo.
    echo Usage: make [command]
    echo.
    echo Commands:
    echo   install     - Install Python dependencies
    echo   setup       - Full setup (venv, deps, .env)
    echo   run         - Start FastAPI server
    echo   streamlit   - Start Streamlit dashboard
    echo   test        - Run setup tests
    echo   example     - Run example script
    echo   clean       - Clean up cache files
    echo   help        - Show this help message
    echo.
    echo Example workflow:
    echo   1. make setup
    echo   2. Edit .env with your API key
    echo   3. make run
    echo   4. (in another terminal) make streamlit
    goto end
)

echo Unknown command. Use 'make help' for usage information.

:end
