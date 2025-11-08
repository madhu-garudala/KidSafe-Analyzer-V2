#!/bin/bash

# KidSafe Analyzer V2 - Backend Startup Script
# Auto-setup: Creates venv, installs dependencies, and checks .env

echo "🖥️  Starting KidSafe Analyzer V2 Backend..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Creating .env template..."
    cat > .env << 'EOF'
# KidSafe Analyzer V2 - Environment Variables
# Add your actual API keys below

# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langsmith_api_key_here

# Optional (improves accuracy by 20-30%)
COHERE_API_KEY=

# Flask Configuration
FLASK_ENV=development
PORT=5001
EOF
    echo "✅ Created .env template at backend/.env"
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env and add your API keys!"
    echo "   - Get OpenAI key: https://platform.openai.com/api-keys"
    echo "   - Get LangSmith key: https://smith.langchain.com/"
    echo ""
    read -p "Press Enter after adding your API keys to continue..."
fi

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

# Check if dependencies are installed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo ""
    echo "📦 Installing Python dependencies (this may take 2-3 minutes)..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.dependencies_installed
    echo "✅ Dependencies installed successfully"
fi

echo ""
echo "🚀 Starting Flask server on http://localhost:5001"
echo ""
echo "⏳ Initializing AI system (this may take 30-60 seconds on first run)..."
echo "   Press CTRL+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Load environment variables and start Flask
set -a
source .env
set +a

# Start the Flask server
python main.py

