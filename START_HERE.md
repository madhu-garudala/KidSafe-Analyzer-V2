# 🎯 START HERE - KidSafe Analyzer V2

Welcome! This is your backup repository with **automatic setup** features!

---

## ⚡ Quick Start (3 Steps)

### Step 1: Clean Up Old Environment (Important!)
Since files were copied from V1, remove the old venv to let scripts create a fresh one:

```bash
cd /Users/madhugarudala/Desktop/AI_MakerSpace/Code/KidSafe-Analyzer-V2
rm -rf backend/venv
```

### Step 2: Run One-Time Setup
```bash
chmod +x *.sh
./setup.sh
```

This will:
- ✅ Check prerequisites (Python, Node.js)
- ✅ Create fresh virtual environment
- ✅ Install all dependencies
- ✅ Create `.env` template

### Step 3: Add Your API Keys
```bash
nano backend/.env  # or open in your favorite editor
```

Replace placeholders with your actual keys:
```env
OPENAI_API_KEY=sk-your-actual-key-here
LANGCHAIN_API_KEY=your-actual-key-here
COHERE_API_KEY=  # optional
```

### Step 4: Generate Pre-computed Analyses (One Time)
This makes the app **blazing fast** with instant results!

```bash
cd backend
source venv/bin/activate
python generate_precomputed_analyses.py
cd ..
```

This takes ~2-3 minutes but only needs to run once.

### Step 5: Start the App
```bash
./start-app.sh
```

**Done!** 🎉 Your browser will open automatically with **instant analysis results**!

---

## 🎁 What's New?

### No More Manual Setup!
The scripts now handle **everything automatically**:

✅ **Auto-creates** virtual environment  
✅ **Auto-installs** all dependencies  
✅ **Auto-loads** environment variables  
✅ **Auto-validates** API keys  
✅ **Works** in both local and production  

### Just Run and Go!
```bash
# First time
./setup.sh
# Add API keys to backend/.env

# Every other time
./start-app.sh
```

No more:
- ❌ `python3 -m venv venv`
- ❌ `source venv/bin/activate`
- ❌ `pip install -r requirements.txt`
- ❌ `npm install`

The scripts do it all for you! 🚀

---

## 📋 Available Scripts

| Script | Purpose |
|--------|---------|
| `./setup.sh` | One-time setup (creates venv, installs deps) |
| `./start-app.sh` | Start both backend + frontend |
| `./start-backend.sh` | Start backend only |
| `./start-frontend.sh` | Start frontend only |

---

## 🌐 URLs

Once started:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5001
- **Backend API Status**: http://localhost:5001/api/status

---

## 📚 Documentation

- **[QUICKSTART.md](./QUICKSTART.md)** - Detailed quick start guide
- **[README.md](./README.md)** - Full project documentation
- **[CHANGES.md](./CHANGES.md)** - What's new in V2
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deploy to Render/Vercel
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Development workflow

---

## 🔧 Troubleshooting

### "Cereals not loading"
1. Check backend terminal - is it fully initialized?
2. Wait 30-60 seconds on first run (AI system initialization)
3. Check API keys in `backend/.env`
4. Test: `curl http://localhost:5001/api/cereals`

### "Port already in use"
```bash
lsof -ti:5001 | xargs kill -9  # Kill backend
lsof -ti:3000 | xargs kill -9  # Kill frontend
```

### "ModuleNotFoundError"
Your venv wasn't created properly:
```bash
rm -rf backend/venv
./setup.sh
```

### "Node/Python not found"
Install prerequisites:
- Python 3.9+: https://www.python.org/downloads/
- Node.js v18+: https://nodejs.org/

---

## 💡 Pro Tips

1. **Keep both terminal windows open** when running start-app.sh
2. **Wait for "✅ KidSafe Analyzer initialized"** before using frontend
3. **Never commit .env file** - it contains your API keys!
4. **Use `./setup.sh` again** if you add new dependencies

---

## 🎯 What You Asked For - Delivered!

> "Can you modify the code so I don't have to set up virtual environment every time?"

✅ **YES!** Virtual environment setup is now **automatic**:
- Scripts detect if venv exists
- Auto-create if missing
- Auto-install dependencies
- Auto-activate on every run
- Works locally AND in production

You literally never have to manually create venv again! 🎉

---

## 🚀 You're All Set!

Run `./setup.sh` now, add your API keys, then `./start-app.sh`

**Happy coding!** 🍎

