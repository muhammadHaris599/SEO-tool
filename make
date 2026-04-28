#!/bin/bash
# SEO Content Tool - macOS/Linux Helper Scripts

case "$1" in
    install)
        echo "Installing dependencies..."
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        echo "Installation complete!"
        ;;
    
    setup)
        echo "Setting up project..."
        python -m venv venv
        source venv/bin/activate
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        cp .env.example .env
        echo "Setup complete! Edit .env with your API key, then run: ./make run"
        ;;
    
    run)
        echo "Starting FastAPI server..."
        source venv/bin/activate
        python -m app.main
        ;;
    
    streamlit)
        echo "Starting Streamlit dashboard..."
        source venv/bin/activate
        streamlit run streamlit_app.py
        ;;
    
    test)
        echo "Running tests..."
        source venv/bin/activate
        python test_setup.py
        ;;
    
    example)
        echo "Running example..."
        source venv/bin/activate
        python example_usage.py
        ;;
    
    clean)
        echo "Cleaning up..."
        find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
        find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null
        rm -f *.log
        echo "Cleanup complete!"
        ;;
    
    help)
        cat <<EOF
SEO Content Tool - Helper Script

Usage: ./make [command]

Commands:
    install     - Install Python dependencies
    setup       - Full setup (venv, deps, .env)
    run         - Start FastAPI server
    streamlit   - Start Streamlit dashboard
    test        - Run setup tests
    example     - Run example script
    clean       - Clean up cache files
    help        - Show this help message

Example workflow:
    1. chmod +x make  (make executable on first run)
    2. ./make setup
    3. Edit .env with your API key
    4. ./make run
    5. (in another terminal) ./make streamlit
EOF
        ;;
    
    *)
        echo "Unknown command. Use './make help' for usage information."
        ;;
esac
