#!/bin/bash

# KidSafe Analyzer V2 - One-Time Setup Script
# Run this once to set up everything automatically

echo "╔══════════════════════════════════════════════════════════╗"
echo "║      🍎 KidSafe Analyzer V2 - Initial Setup 🍎          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check prerequisites
echo "1️⃣  Checking Prerequisites..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "   Please install Python 3.9 or higher from https://www.python.org/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "   ✅ Python $PYTHON_VERSION found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "   Please install Node.js v18 or higher from https://nodejs.org/"
    exit 1
fi
NODE_VERSION=$(node -v)
echo "   ✅ Node.js $NODE_VERSION found"

echo ""

# Setup Backend
echo "2️⃣  Setting Up Backend..."
echo ""

cd "$SCRIPT_DIR/backend"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "   📝 Creating .env template..."
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
    echo "   ✅ Created .env template"
    echo ""
    echo "   ⚠️  IMPORTANT: You need to add your API keys to backend/.env"
    echo "      - OpenAI API Key: https://platform.openai.com/api-keys"
    echo "      - LangSmith API Key: https://smith.langchain.com/"
    echo "      - Cohere API Key (optional): https://dashboard.cohere.com/"
    echo ""
else
    echo "   ✅ .env file already exists"
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "   📦 Creating Python virtual environment..."
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ✅ Virtual environment already exists"
fi

# Activate and install dependencies
echo "   📦 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
touch venv/.dependencies_installed
echo "   ✅ Python dependencies installed"

cd "$SCRIPT_DIR"
echo ""

# Setup Frontend
echo "3️⃣  Setting Up Frontend..."
echo ""

cd "$SCRIPT_DIR/frontend"

# Install npm dependencies
if [ ! -d "node_modules" ]; then
    echo "   📦 Installing Node.js dependencies..."
    npm install
    echo "   ✅ Node.js dependencies installed"
else
    echo "   ✅ Node.js dependencies already exist"
fi

cd "$SCRIPT_DIR"
echo ""

# Final instructions
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  ✅ Setup Complete!                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo ""
echo "   1. Edit backend/.env and add your API keys"
echo "      (Required: OPENAI_API_KEY, LANGCHAIN_API_KEY)"
echo ""
echo "   2. Start the application:"
echo "      ./start-app.sh"
echo ""
echo "   Or start backend and frontend separately:"
echo "      ./start-backend.sh    (Terminal 1)"
echo "      ./start-frontend.sh   (Terminal 2)"
echo ""
echo "🌐 Once started, the app will be available at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:5001"
echo ""

# Delete the test script if it exists
if [ -f "$SCRIPT_DIR/test-backend.sh" ]; then
    rm "$SCRIPT_DIR/test-backend.sh"
fi

