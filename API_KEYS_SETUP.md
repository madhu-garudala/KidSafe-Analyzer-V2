# 🔑 API Keys Setup Guide - KidSafe Analyzer V2

Quick reference for setting up your API keys locally.

---

## 📍 Where to Put API Keys Locally

**Use a `.env` file in the `backend/` directory** - This is the recommended best practice!

```
KidSafe-Analyzer-V2/
└── backend/
    └── .env  ← Create this file here
```

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Copy the Template

```bash
cd KidSafe-Analyzer-V2
cp backend/.env.template backend/.env
```

### Step 2: Edit the `.env` File

Open `backend/.env` in your text editor and replace the placeholder values with your actual API keys:

```bash
# Required Keys
OPENAI_API_KEY=sk-your-actual-openai-key-here
LANGCHAIN_API_KEY=ls__your-actual-langsmith-key-here

# Optional Keys (recommended)
COHERE_API_KEY=your-actual-cohere-key-here

# Flask Config
FLASK_ENV=development
```

### Step 3: Start the Application

```bash
./start-app.sh
```

That's it! The backend will automatically load your API keys from the `.env` file.

---

## 🔐 Security Notes

✅ **Safe:**
- The `.env` file is already in `.gitignore`
- Your keys won't be committed to Git
- Keys are loaded at runtime, not hardcoded

❌ **Never:**
- Don't commit `.env` files to Git
- Don't share your API keys
- Don't hardcode keys in source code

---

## 🔑 Which API Keys Do I Need?

### Required (Application Won't Work Without These)

1. **OPENAI_API_KEY** ✅ Required
   - **Purpose**: Powers the AI analysis (GPT-4o-mini) and embeddings
   - **Get it**: https://platform.openai.com/api-keys
   - **Cost**: Pay-as-you-go (~$0.50-$2 per 1000 analyses)
   - **Sign up**: Free account with $5 credit for new users

2. **LANGCHAIN_API_KEY** ✅ Required
   - **Purpose**: Enables tracing and monitoring of RAG pipeline
   - **Get it**: https://smith.langchain.com/ (Settings → API Keys)
   - **Cost**: Free tier includes 5K traces/month
   - **Sign up**: Free account

### Optional (But Recommended)

3. **COHERE_API_KEY** ⚠️ Optional
   - **Purpose**: Advanced reranking for better retrieval accuracy
   - **Benefit**: Improves analysis accuracy by 20-30%
   - **Get it**: https://dashboard.cohere.com/
   - **Cost**: Free tier includes 1000 API calls/month
   - **Sign up**: Free account
   - **Recommendation**: ⭐ **Highly recommended for production use**

---

## 🧪 Testing Your Setup

After setting up your `.env` file:

```bash
# Start the backend
cd backend
source venv/bin/activate
python main.py
```

You should see:
```
🚀 Initializing KidSafe Analyzer...
📚 Loading vector store...
✅ KidSafe Analyzer initialized successfully!
```

If you see errors about missing API keys, double-check your `.env` file.

---

## 🆘 Troubleshooting

### Problem: "OPENAI_API_KEY not set"

**Solution**: 
1. Make sure the `.env` file is in `backend/` directory (not project root)
2. Check that your key starts with `sk-`
3. Make sure there are no spaces around the `=` sign
4. Verify the file is named exactly `.env` (not `.env.txt`)

### Problem: "System initialization failed"

**Solutions**:
- Verify both OPENAI_API_KEY and LANGCHAIN_API_KEY are set
- Check that your OpenAI account has credits
- Ensure you have internet connection (for API calls)

### Problem: Keys working in terminal but not in .env file

**Solution**:
- Make sure `python-dotenv` is installed: `pip install python-dotenv`
- It's already in `requirements.txt`, so run: `pip install -r requirements.txt`

---

## 🌐 For Cloud Deployment

When deploying to Render/Vercel, you DON'T use `.env` files. Instead:

1. **Render (Backend)**:
   - Go to your service dashboard
   - Click "Environment" tab
   - Add each key as a separate environment variable

2. **Vercel (Frontend)**:
   - Go to your project settings
   - Click "Environment Variables"
   - Add `VITE_API_URL` with your backend URL

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete cloud deployment instructions.

---

## 📋 Summary

| API Key | Required? | Purpose | Cost |
|---------|-----------|---------|------|
| OPENAI_API_KEY | ✅ Yes | AI analysis & embeddings | Pay-per-use |
| LANGCHAIN_API_KEY | ✅ Yes | RAG pipeline tracing | Free tier |
| COHERE_API_KEY | ⚠️ Optional | Better retrieval accuracy (+20-30%) | Free tier |

---

## 💡 Pro Tips

1. **Get all three keys** - Even though Cohere is optional, it significantly improves accuracy
2. **Monitor usage** - Check your OpenAI dashboard to track API usage
3. **Use LangSmith** - View traces at https://smith.langchain.com/ to debug issues
4. **Rotate keys periodically** - For security, regenerate keys every few months

---

Need help? Check [DEVELOPMENT.md](./DEVELOPMENT.md) for full setup instructions!

