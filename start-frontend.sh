#!/bin/bash

# KidSafe Analyzer V2 - Frontend Startup Script
# Auto-setup: Installs dependencies if missing

echo "🌐 Starting KidSafe Analyzer V2 Frontend..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "   Please install Node.js v18 or higher from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "⚠️  Node.js version is too old. Please upgrade to v18 or higher."
    echo "   Current version: $(node -v)"
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies (this may take 1-2 minutes)..."
    npm install
    echo "✅ Dependencies installed successfully"
fi

echo ""
echo "🚀 Starting Vite dev server on http://localhost:3000"
echo ""
echo "   The browser will open automatically"
echo "   Press CTRL+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the Vite dev server
npm run dev

