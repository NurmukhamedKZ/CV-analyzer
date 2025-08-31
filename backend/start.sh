echo "🚀 Starting AI CV Checker FastAPI Backend..."

#!/bin/bash
set -e

echo "\033[1;32m🚀 Starting AI CV Checker FastAPI Backend...\033[0m"

# Check for Python 3.8+
if ! command -v python3 &> /dev/null; then
    echo "\033[1;31m❌ Python 3 is not installed.\033[0m"
    exit 1
fi
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "\033[1;31m❌ Python 3.8+ is required. Current version: $PYTHON_VERSION\033[0m"
    exit 1
fi
echo "\033[1;32m✅ Python version: $PYTHON_VERSION\033[0m"

# Create venv if missing
if [ ! -d "venv" ]; then
    echo "\033[1;34m📦 Creating virtual environment...\033[0m"
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate
echo "\033[1;34m🔧 Virtual environment activated.\033[0m"

# Install dependencies with uv
if ! command -v uv &> /dev/null; then
    echo "\033[1;33m⚠️  'uv' not found. Installing with pip...\033[0m"
    pip install uv
fi
echo "\033[1;34m📦 Installing dependencies with uv...\033[0m"
uv pip install -r requirements.txt

# Check for .env
if [ ! -f ".env" ]; then
    echo "\033[1;33m⚠️  No .env file found. Copying from env.example...\033[0m"
    cp env.example .env
    echo "\033[1;33m⚠️  Please edit .env and add your OpenAI API key.\033[0m"
else
    # Check for OPENAI_API_KEY in .env
    if ! grep -q "OPENAI_API_KEY=" .env; then
        echo "\033[1;33m⚠️  .env exists but OPENAI_API_KEY is missing! Please add your key.\033[0m"
    fi
fi

echo "\033[1;32m🚀 Starting FastAPI server...\033[0m"
echo "\033[1;36m📖 API docs: http://localhost:8000/docs\033[0m"
echo "\033[1;36m🔍 Redoc:   http://localhost:8000/redoc\033[0m"
echo "\033[1;36m🏠 API base: http://localhost:8000\033[0m"

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
