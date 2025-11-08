# 🚀 KidSafe Analyzer V2 - Quick Start Guide

This guide will get you up and running in **under 5 minutes**!

---

## 📋 Prerequisites

Before you start, make sure you have:

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Node.js v18+** ([Download](https://nodejs.org/))
- **API Keys** (get these first):
  - OpenAI API Key ([Get it here](https://platform.openai.com/api-keys)) - **Required**
  - LangSmith API Key ([Get it here](https://smith.langchain.com/)) - **Required**
  - Cohere API Key ([Get it here](https://dashboard.cohere.com/)) - Optional (improves accuracy)

---

## ⚡ One-Command Setup & Start

### Option 1: Automatic Everything (Recommended)

```bash
cd KidSafe-Analyzer-V2

# Run setup (only needed first time)
./setup.sh

# After setup, start the app
./start-app.sh
```

That's it! 🎉 The app will open in your browser automatically.

---

### Option 2: Manual Setup (If you prefer control)

#### Step 1: Setup Backend
```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cat > .env << EOF
OPENAI_API_KEY=your_actual_openai_key_here
LANGCHAIN_API_KEY=your_actual_langsmith_key_here
COHERE_API_KEY=
FLASK_ENV=development
PORT=5001
EOF

# Edit .env and add your actual API keys
nano .env  # or use your favorite editor
```

#### Step 2: Setup Frontend
```bash
cd ../frontend

# Install dependencies
npm install
```

#### Step 3: Start the Application

In **Terminal 1** (Backend):
```bash
cd backend
source venv/bin/activate
python main.py
```

In **Terminal 2** (Frontend):
```bash
cd frontend
npm run dev
```

Open your browser to: `http://localhost:3000`

---

## 🔑 Adding API Keys

Edit `backend/.env`:

```bash
# Required
OPENAI_API_KEY=sk-your-actual-openai-key-here
LANGCHAIN_API_KEY=your-actual-langsmith-key-here

# Optional (20-30% better accuracy)
COHERE_API_KEY=your-cohere-key-here

# Configuration
FLASK_ENV=development
PORT=5001
```

**Important:** Never commit the `.env` file to git!

---

## ✅ How to Know It's Working

When the backend starts successfully, you'll see:

```
✅ Loaded environment variables from .env file
🚀 Initializing KidSafe Analyzer...
📚 Loading vector store...
🔍 Initializing advanced retrieval manager...
⚙️  Setting up ensemble retrieval...
🤖 Initializing ingredient analyzer...
✅ KidSafe Analyzer initialized successfully!
Starting Flask server on port 5001...
 * Running on http://0.0.0.0:5001
```

The frontend should display:
- ✅ Green "System Ready" indicator
- A dropdown list of cereals

---

## 🐛 Troubleshooting

### Backend won't start
- **Check API keys**: Make sure you've edited `backend/.env` with real keys
- **Check Python version**: `python3 --version` (must be 3.9+)
- **Activate venv**: `source backend/venv/bin/activate`
- **Reinstall deps**: `pip install -r requirements.txt`

### Frontend won't connect
- **Check backend is running**: Visit `http://localhost:5001` (should see JSON)
- **Check port**: Backend must be on port 5001
- **Check browser console**: Look for CORS or connection errors

### "No cereals found"
- **Backend not fully initialized**: Wait 30-60 seconds for first-time setup
- **Check backend terminal**: Look for any error messages
- **Test API**: `curl http://localhost:5001/api/cereals`

### Port already in use
```bash
# Find and kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

---

## 📂 Project Structure

```
KidSafe-Analyzer-V2/
├── setup.sh              # One-time setup script
├── start-app.sh          # Start both servers
├── start-backend.sh      # Start backend only
├── start-frontend.sh     # Start frontend only
├── backend/
│   ├── .env             # Your API keys (create this!)
│   ├── venv/            # Virtual environment (auto-created)
│   ├── main.py          # Flask server
│   └── requirements.txt # Python dependencies
└── frontend/
    ├── node_modules/    # Dependencies (auto-created)
    └── package.json     # Frontend dependencies
```

---

## 🌐 Production Deployment

For deploying to Render and Vercel, see:
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Full deployment guide
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Development workflow

---

## 🆘 Still Need Help?

1. Check the full [README.md](./README.md)
2. Review [DEVELOPMENT.md](./DEVELOPMENT.md)
3. Check backend terminal for error messages
4. Check browser console for frontend errors

---

**Built with ❤️ for parents who care about their children's health**

