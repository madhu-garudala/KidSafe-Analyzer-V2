# 💻 KidSafe Analyzer V2 - Local Development Guide

Complete guide for setting up and running KidSafe Food Analyzer V2 on your local machine.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## 🔑 Quick Answer: Where to Put API Keys Locally

**YES, use a `.env` file!** This is the recommended way for local development.

1. Create a file named `.env` in the `backend/` directory (not in project root)
2. Add your API keys to this file (see example below)
3. The file is already in `.gitignore` so your keys won't be committed to Git
4. `python-dotenv` is already installed via `requirements.txt`

**Example `backend/.env` file:**
```bash
OPENAI_API_KEY=sk-your-actual-key-here
LANGCHAIN_API_KEY=ls__your-actual-key-here
COHERE_API_KEY=your-actual-cohere-key-here
FLASK_ENV=development
```

---

## 🔧 Prerequisites

### Required Software

| Software | Minimum Version | Download |
|----------|----------------|----------|
| Node.js | 18.0.0+ | [nodejs.org](https://nodejs.org/) |
| Python | 3.9+ | [python.org](https://www.python.org/) |
| npm | 9.0.0+ | Comes with Node.js |
| pip | 21.0.0+ | Comes with Python |
| Git | 2.30+ | [git-scm.com](https://git-scm.com/) |

### Required API Keys

You'll need these API keys to run the application:

1. **OpenAI API Key** (Required)
   - Sign up at: https://platform.openai.com/
   - Get your API key from: https://platform.openai.com/api-keys
   - Cost: Pay-as-you-go (~$0.50-$2 per 1000 analyses)

2. **LangSmith API Key** (Required)
   - Sign up at: https://smith.langchain.com/
   - Get your API key from Settings → API Keys
   - Cost: Free tier includes 5K traces/month

3. **Cohere API Key** (Optional, for better retrieval)
   - Sign up at: https://dashboard.cohere.com/
   - Get your API key from API Keys section
   - Cost: Free tier includes 1000 calls/month
   - Used for: Advanced reranking in ensemble retrieval strategy

### Verify Prerequisites

```bash
# Check Node.js version
node --version  # Should be v18.0.0 or higher

# Check npm version
npm --version  # Should be 9.0.0 or higher

# Check Python version
python3 --version  # Should be 3.9.0 or higher

# Check pip version
pip3 --version  # Should be 21.0.0 or higher

# Check Git version
git --version  # Should be 2.30 or higher
```

---

## 🚀 Initial Setup

### 1. Clone or Navigate to Project

```bash
cd /path/to/KidSafe-Analyzer-V2
```

### 2. Project Structure Check

Ensure your project has this structure:

```
KidSafe-Analyzer-V2/
├── backend/
│   ├── backend/          # Python package
│   ├── Data/             # Data files
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── start-app.sh
├── start-backend.sh
├── start-frontend.sh
└── README.md
```

---

## 🖥 Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
```

**On Windows:**
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- LangChain (AI framework)
- LangGraph (workflow orchestration)
- OpenAI libraries
- Qdrant (vector database)
- And more...

**Installation may take 2-5 minutes.**

### Step 5: Set Environment Variables

**Option A: Set in Terminal (Temporary)**

**On macOS/Linux:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
export LANGCHAIN_API_KEY="ls__your-key-here"
export COHERE_API_KEY="your-cohere-key-here"  # Optional but recommended
```

**On Windows:**
```cmd
set OPENAI_API_KEY=sk-your-key-here
set LANGCHAIN_API_KEY=ls__your-key-here
set COHERE_API_KEY=your-cohere-key-here
```

**Option B: Create .env File (Recommended for Development)**

Create a `.env` file in the `backend` directory:

```bash
# backend/.env
# Copy these lines and replace with your actual keys

# Required Keys
OPENAI_API_KEY=sk-your-openai-key-here
LANGCHAIN_API_KEY=ls__your-langsmith-key-here

# Optional Keys (improves retrieval accuracy)
COHERE_API_KEY=your-cohere-key-here

# Flask Configuration
FLASK_ENV=development
```

**Note**: The `.env` file is already in `.gitignore` so your keys won't be committed.

Python-dotenv is already included in `requirements.txt`.

### Step 6: Verify Backend Setup

```bash
python main.py
```

You should see:
```
Starting Flask server on port 5001...
🚀 Initializing KidSafe Analyzer...
📚 Loading vector store...
✅ KidSafe Analyzer initialized successfully!
 * Running on http://0.0.0.0:5001
```

**Note**: First run takes 30-60 seconds to initialize AI models.

Test in browser: `http://localhost:5001` - Should see JSON response.

Press `Ctrl+C` to stop the server.

---

## 🌐 Frontend Setup

### Step 1: Navigate to Frontend Directory

```bash
cd ../frontend  # From backend directory
# OR
cd frontend     # From project root
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install:
- React 18.2
- Vite (dev server & build tool)
- Axios (HTTP client)
- React plugins

**Installation may take 1-2 minutes.**

### Step 3: Configure API URL (Optional)

By default, the frontend uses `http://localhost:5001` for the backend.

To change it, create a `.env` file in the `frontend` directory:

```bash
# frontend/.env
VITE_API_URL=http://localhost:5001
```

### Step 4: Verify Frontend Setup

```bash
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

Open browser: `http://localhost:3000` - Should see the KidSafe app.

Press `Ctrl+C` to stop the server.

---

## 🎮 Running the Application

### Method 1: Using Startup Scripts (Recommended for macOS/Linux)

The easiest way to run both servers:

```bash
# From project root
./start-app.sh
```

This will:
1. Open 2 new terminal windows
2. Start backend on `http://localhost:5001`
3. Start frontend on `http://localhost:3000`
4. Open your browser automatically

**To stop**: Close the terminal windows or press `Ctrl+C` in each.

### Method 2: Manual Startup (Works on All Platforms)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open Browser**: Navigate to `http://localhost:3000`

### Method 3: Individual Server Scripts

**Start Backend Only:**
```bash
./start-backend.sh
```

**Start Frontend Only:**
```bash
./start-frontend.sh
```

---

## 🔧 Development Workflow

### Backend Development

1. **Make code changes** in `backend/` directory

2. **Hot reload is NOT automatic** - Restart server to see changes:
   ```bash
   # Press Ctrl+C to stop
   python main.py  # Start again
   ```

3. **Enable debug mode** for auto-reload (development only):
   ```python
   # In main.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

4. **View logs** in terminal where backend is running

5. **Test API endpoints** using:
   - Browser for GET requests
   - Postman or curl for POST requests
   - Frontend application

### Frontend Development

1. **Make code changes** in `frontend/src/` directory

2. **Hot reload is AUTOMATIC** - Changes appear immediately in browser

3. **Component development**:
   - Edit components in `src/components/`
   - See changes instantly
   - Check browser console for errors

4. **Styling changes**:
   - Edit `src/App.css` or `src/index.css`
   - Changes apply immediately

5. **API integration**:
   - Modify `src/services/api.js` for API changes
   - Update components to use new endpoints

### Code Organization

**Backend:**
```
backend/backend/
├── config.py              # Configuration settings
├── vector_store.py        # Qdrant vector database
├── rag_engine.py          # LangGraph RAG workflow
├── advanced_retrieval.py  # Retrieval strategies
└── evaluation.py          # Evaluation tools
```

**Frontend:**
```
frontend/src/
├── components/            # React components
├── services/              # API service layer
├── App.jsx               # Main app component
└── main.jsx              # Entry point
```

---

## 🧪 Testing

### Manual Testing

1. **Start both servers**

2. **Test System Initialization**:
   - Wait for "System Ready!" message
   - Should take 30-60 seconds first time

3. **Test Analysis**:
   - Select a cereal from dropdown
   - Click "Analyze Ingredients"
   - Verify results appear within 10 seconds

4. **Test Chatbot**:
   - Ask questions after analysis
   - Verify intelligent responses

5. **Test Error Handling**:
   - Try without API keys (should show error)
   - Try with invalid cereal (should handle gracefully)

### API Testing with curl

**Test Health Check:**
```bash
curl http://localhost:5001/
```

**Test Status:**
```bash
curl http://localhost:5001/api/status
```

**Test Analysis:**
```bash
curl -X POST http://localhost:5001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "cereal_name": "Test Cereal",
    "ingredients": "Whole Grain Oats, Sugar, Salt"
  }'
```

### Running RAGAS Evaluation

To evaluate the RAG pipeline:

```bash
cd backend
source venv/bin/activate
python -m backend.ragas_evaluation
```

This will:
- Run test cases through the RAG pipeline
- Evaluate faithfulness, relevancy, precision, recall
- Display detailed metrics

---

## 🐛 Troubleshooting

### Backend Issues

#### ❌ `ModuleNotFoundError: No module named 'flask'`

**Solution**: Virtual environment not activated or dependencies not installed
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### ❌ `Error: OPENAI_API_KEY not set`

**Solution**: Set environment variables
```bash
export OPENAI_API_KEY="your-key-here"
export LANGCHAIN_API_KEY="your-key-here"
```

#### ❌ `Address already in use (port 5001)`

**Solution**: Another process is using the port
```bash
# Find and kill the process (macOS/Linux)
lsof -ti:5001 | xargs kill -9

# Or use a different port
# Edit main.py to use port 5002
```

#### ❌ Slow initialization (>2 minutes)

**Cause**: First-time download of AI models

**Solution**: Wait for completion, subsequent starts will be faster

### Frontend Issues

#### ❌ `Cannot find module 'react'`

**Solution**: Dependencies not installed
```bash
cd frontend
npm install
```

#### ❌ `Network Error` or `Failed to fetch`

**Cause**: Backend not running or wrong URL

**Solution**:
1. Verify backend is running on port 5001
2. Check `VITE_API_URL` in frontend/.env
3. Verify CORS is enabled in backend

#### ❌ Port 3000 already in use

**Solution**: Use a different port
```bash
# Edit vite.config.js
server: {
  port: 3001,  // Change to 3001
  ...
}
```

#### ❌ Blank page in browser

**Solution**: Check browser console for errors
- Press F12 to open developer tools
- Check Console tab for JavaScript errors
- Check Network tab for failed API calls

### Common Issues

#### ❌ System stays "Initializing" forever

**Cause**: Backend initialization failed

**Solution**:
1. Check backend terminal for error messages
2. Verify API keys are set correctly
3. Check PDF file exists: `backend/Data/Input/Food-Labeling-Guide-(PDF).pdf`

#### ❌ Analysis fails with "System not initialized"

**Cause**: Backend didn't fully initialize

**Solution**:
1. Wait full 60 seconds for initialization
2. Check backend logs for errors
3. Restart backend server
4. Verify environment variables

---

## 📝 Additional Development Tips

### Hot Reloading

**Frontend**: ✅ Automatic (Vite)  
**Backend**: ❌ Manual restart required (or use Flask debug mode)

### Debugging

**Frontend**:
- Use React DevTools browser extension
- Check browser console (F12)
- Use `console.log()` for debugging

**Backend**:
- Use `print()` statements
- Check terminal output
- Use LangSmith for RAG pipeline tracing

### Performance

**Local Development**:
- Backend initialization: ~30-60 seconds
- Analysis per cereal: ~5-10 seconds
- Chatbot response: ~3-5 seconds

**First Run**:
- Expect longer times for:
  - Installing dependencies
  - Downloading AI models
  - Creating vector embeddings

---

## 🎉 You're Ready to Develop!

Your local development environment is now set up. Happy coding! 🚀

---

## 📋 Quick Reference

### API Keys Location
```bash
# Create this file with your actual keys
backend/.env
```

### Start Commands
```bash
# Start everything
./start-app.sh

# Start backend only
cd backend && source venv/bin/activate && python main.py

# Start frontend only
cd frontend && npm run dev

# Install backend deps
cd backend && pip install -r requirements.txt

# Install frontend deps
cd frontend && npm install
```

### Required API Keys
- **OPENAI_API_KEY** - Required for AI analysis
- **LANGCHAIN_API_KEY** - Required for tracing/monitoring
- **COHERE_API_KEY** - Optional (improves accuracy by 20-30%)

### Access URLs
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5001
- **LangSmith Traces**: https://smith.langchain.com/

---

For deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

