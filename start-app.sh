#!/bin/bash

# KidSafe Analyzer V2 - Complete App Startup Script
# Auto-setup: Runs setup automatically if needed, then starts both servers

echo "╔══════════════════════════════════════════════════════════╗"
echo "║        🍎 KidSafe Analyzer V2 - Starting App 🍎         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Quick setup check - run setup if needed
if [ ! -d "$SCRIPT_DIR/backend/venv" ] || [ ! -d "$SCRIPT_DIR/frontend/node_modules" ]; then
    echo "⚠️  First time setup required..."
    echo ""
    "$SCRIPT_DIR/setup.sh"
    echo ""
    echo "Press Enter to continue starting the application..."
    read
fi

# Check if .env file has been configured
if [ -f "$SCRIPT_DIR/backend/.env" ]; then
    if grep -q "your_openai_api_key_here" "$SCRIPT_DIR/backend/.env" 2>/dev/null; then
        echo "⚠️  WARNING: API keys not configured in backend/.env"
        echo "   The backend will not work without valid API keys."
        echo ""
        echo "   Please edit backend/.env and add your keys, then run this script again."
        echo ""
        exit 1
    fi
fi

# Start backend in background
echo "1️⃣  Starting Backend Server..."
osascript -e "tell app \"Terminal\" to do script \"cd '$SCRIPT_DIR' && ./start-backend.sh\""
sleep 3

# Start frontend in background
echo "2️⃣  Starting Frontend Server..."
osascript -e "tell app \"Terminal\" to do script \"cd '$SCRIPT_DIR' && ./start-frontend.sh\""
sleep 3

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              ✅ Application Started!                     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:5001"
echo ""
echo "🌐 Opening browser..."
sleep 1
open http://localhost:3000

echo ""
echo "💡 Tips:"
echo "   - Wait 30-60 seconds for backend to fully initialize"
echo "   - Check the backend terminal for initialization status"
echo "   - To stop: Close terminal windows or press CTRL+C in each"
echo ""

