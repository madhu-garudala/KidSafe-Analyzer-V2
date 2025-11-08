# 🌐 KidSafe Analyzer V2 - Cloud Deployment Guide

Complete guide for deploying KidSafe Food Analyzer V2 to production using Vercel (Frontend) and Render (Backend).

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Architecture Overview](#architecture-overview)
- [Backend Deployment (Render)](#backend-deployment-render)
- [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
- [Environment Variables](#environment-variables)
- [Testing Deployment](#testing-deployment)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

Before deploying, ensure you have:

1. **GitHub Account** - To store your code repository
2. **Vercel Account** - For frontend hosting ([Sign up](https://vercel.com/))
3. **Render Account** - For backend hosting ([Sign up](https://render.com/))
4. **API Keys**:
   - OpenAI API Key ([Get it](https://platform.openai.com/api-keys))
   - LangSmith API Key ([Get it](https://smith.langchain.com/))
   - Cohere API Key - Optional ([Get it](https://dashboard.cohere.com/))

---

## 🏗 Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐
│                 │         │                  │
│   User Browser  │ ◄─────► │  Vercel Frontend │
│                 │  HTTPS  │   (React/Vite)   │
└─────────────────┘         └──────────────────┘
                                     │
                                     │ API Calls
                                     │ (HTTPS)
                                     ▼
                            ┌──────────────────┐
                            │                  │
                            │  Render Backend  │
                            │  (Flask/Python)  │
                            │                  │
                            └──────────────────┘
```

---

## 🖥 Backend Deployment (Render)

### Step 1: Push Code to GitHub

```bash
cd KidSafe-Analyzer-V2
git init
git add .
git commit -m "Initial commit for V2"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Create Render Web Service

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Click "New +" → "Web Service"**

3. **Connect Your Repository**:
   - Connect your GitHub account
   - Select the `KidSafe-Analyzer-V2` repository
   - Click "Connect"

4. **Configure the Service**:
   
   | Setting | Value |
   |---------|-------|
   | **Name** | `kidsafe-analyzer-backend-v2` |
   | **Region** | Choose closest to your users |
   | **Branch** | `main` |
   | **Root Directory** | `backend` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `python main.py` |
   | **Plan** | Free (or paid for better performance) |

5. **Add Environment Variables** (See [Environment Variables](#environment-variables) section below)

6. **Click "Create Web Service"**

7. **Wait for Deployment** (3-5 minutes)
   - Render will install dependencies and start your Flask server
   - Once complete, you'll see "Your service is live 🎉"

8. **Copy Your Backend URL**:
   - Example: `https://kidsafe-analyzer-backend-v2.onrender.com`
   - Save this URL for frontend configuration

### Step 3: Test Backend

Visit your backend URL in a browser. You should see:
```json
{
  "status": "running",
  "message": "KidSafe Analyzer API is running!",
  "version": "1.0.0"
}
```

---

## 🌐 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Update API URL** (if needed):
   
   The frontend will automatically use the `VITE_API_URL` environment variable in production.

### Step 2: Deploy to Vercel

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**

2. **Click "Add New..." → "Project"**

3. **Import Your Repository**:
   - Select your `KidSafe-Analyzer-V2` repository
   - Click "Import"

4. **Configure Project**:

   | Setting | Value |
   |---------|-------|
   | **Project Name** | `kidsafe-analyzer-v2` |
   | **Framework Preset** | `Vite` |
   | **Root Directory** | `frontend` |
   | **Build Command** | `npm run build` |
   | **Output Directory** | `dist` |
   | **Install Command** | `npm install` |

5. **Add Environment Variable**:
   - Click "Environment Variables"
   - Add variable:
     - **Name**: `VITE_API_URL`
     - **Value**: Your Render backend URL (e.g., `https://kidsafe-analyzer-backend-v2.onrender.com`)
     - Select all environments (Production, Preview, Development)

6. **Click "Deploy"**

7. **Wait for Deployment** (1-2 minutes)

8. **Your App is Live!**
   - Vercel will provide a URL like: `https://kidsafe-analyzer-v2.vercel.app`
   - Visit it to see your application running

---

## 🔐 Environment Variables

### Backend (Render)

Add these environment variables in Render dashboard:

| Variable Name | Required | Description | Example |
|---------------|----------|-------------|---------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for GPT-4o-mini | `sk-...` |
| `LANGCHAIN_API_KEY` | ✅ Yes | LangSmith API key for tracing | `ls__...` |
| `COHERE_API_KEY` | ⚠️ Optional | Cohere reranking (improves accuracy by 20-30%) | `...` |
| `FLASK_ENV` | ⚠️ Optional | Set to `production` | `production` |
| `PYTHON_VERSION` | ⚠️ Optional | Python version | `3.11.0` |

**How to Add in Render**:
1. Go to your service dashboard
2. Click "Environment" in the left sidebar
3. Click "Add Environment Variable"
4. Enter name and value
5. Click "Save Changes"

### Frontend (Vercel)

Add this environment variable in Vercel dashboard:

| Variable Name | Required | Description | Example |
|---------------|----------|-------------|---------|
| `VITE_API_URL` | ✅ Yes | Backend API URL | `https://kidsafe-analyzer-backend-v2.onrender.com` |

**How to Add in Vercel**:
1. Go to your project dashboard
2. Click "Settings" → "Environment Variables"
3. Add the variable for all environments
4. Redeploy your application

---

## ✅ Testing Deployment

### Test Backend

1. **Health Check**:
   ```bash
   curl https://YOUR_BACKEND_URL.onrender.com/
   ```
   Should return JSON with status "running"

2. **System Status**:
   ```bash
   curl https://YOUR_BACKEND_URL.onrender.com/api/status
   ```
   Should return initialization status

3. **Get Cereals**:
   ```bash
   curl https://YOUR_BACKEND_URL.onrender.com/api/cereals
   ```
   Should return list of cereals

### Test Frontend

1. **Open Your Vercel URL** in a browser

2. **Check System Status**:
   - You should see "Initializing System..." or "System Ready!"
   - Wait up to 60 seconds for initialization

3. **Test Analysis**:
   - Select a cereal from the dropdown
   - Click "Analyze Ingredients"
   - Should see detailed analysis results

4. **Test Chatbot**:
   - After analysis, try asking questions in the chatbot
   - Should receive intelligent responses

### Integration Test

1. **Open browser developer console** (F12)
2. **Check Network tab** - API calls should show 200 status
3. **Try different cereals** - Each should analyze successfully
4. **Test on mobile device** - Should be responsive

---

## 🔧 Troubleshooting

### Backend Issues

#### ❌ "Application Error" or Service Won't Start

**Cause**: Missing dependencies or environment variables

**Solution**:
1. Check Render logs: Dashboard → Logs
2. Ensure all required environment variables are set
3. Verify `requirements.txt` is in the `backend` directory
4. Check Python version matches `runtime.txt`

#### ❌ "System not initialized" Error

**Cause**: Missing API keys

**Solution**:
1. Verify `OPENAI_API_KEY` is set in Render
2. Verify `LANGCHAIN_API_KEY` is set in Render
3. Restart the service after adding keys

#### ❌ Slow Response Times

**Cause**: Render free tier cold starts

**Solution**:
1. Upgrade to paid tier for always-on service
2. Or accept 30-60 second initial load on free tier
3. Consider implementing a keep-alive ping

### Frontend Issues

#### ❌ "Network Error" or "Failed to Fetch"

**Cause**: Frontend can't reach backend

**Solution**:
1. Verify `VITE_API_URL` is set correctly in Vercel
2. Check backend is running (visit backend URL)
3. Check CORS settings in `main.py`
4. Ensure backend URL doesn't have trailing slash

#### ❌ Blank Page or Build Errors

**Cause**: Build configuration issues

**Solution**:
1. Verify root directory is set to `frontend` in Vercel
2. Check build command is `npm run build`
3. Verify output directory is `dist`
4. Check Vercel deployment logs for errors

#### ❌ Environment Variable Not Working

**Cause**: Needs rebuild after adding variables

**Solution**:
1. Go to Vercel dashboard
2. Click "Deployments"
3. Find latest deployment → "..." menu → "Redeploy"
4. Or push a new commit to trigger rebuild

---

## 🔄 Updating Deployment

### Update Backend

```bash
# Make changes to backend code
git add backend/
git commit -m "Update backend"
git push origin main
```

Render will automatically redeploy (webhook-based).

### Update Frontend

```bash
# Make changes to frontend code
git add frontend/
git commit -m "Update frontend"
git push origin main
```

Vercel will automatically redeploy (webhook-based).

---

## 📊 Monitoring

### Render Monitoring

- **Logs**: Dashboard → Your Service → Logs
- **Metrics**: Dashboard → Your Service → Metrics
- **Restart**: Dashboard → Your Service → Manual Deploy → "Clear build cache & deploy"

### Vercel Monitoring

- **Analytics**: Dashboard → Your Project → Analytics
- **Logs**: Dashboard → Your Project → Deployments → View Function Logs
- **Speed Insights**: Dashboard → Your Project → Speed Insights

### LangSmith Monitoring

- **Traces**: [smith.langchain.com](https://smith.langchain.com/)
- **Project**: KidSafe-Food-Analyzer
- View all RAG pipeline traces and performance metrics

---

## 💰 Cost Considerations

### Render (Free Tier)

- ✅ Free web service
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ 30-60 second cold start time
- ⚠️ 750 hours/month free compute

**Upgrade ($7/month)**:
- Always-on service
- No cold starts
- Better performance

### Vercel (Free Tier)

- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Always-on CDN
- ⚠️ Serverless function limits

**Upgrade (Pro $20/month)**:
- More bandwidth
- Advanced analytics
- Team collaboration

### API Costs

- **OpenAI**: Pay per token (~$0.50-$2 per 1000 analyses)
  - GPT-4o-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
  - Embeddings: ~$0.02 per 1M tokens
- **LangSmith**: Free tier includes 5K traces/month (sufficient for development)
- **Cohere**: Free tier includes 1000 API calls/month (reranking operations)

---

## 🎉 Success!

Your KidSafe Analyzer V2 is now deployed and running in the cloud!

**Frontend URL**: `https://kidsafe-analyzer-v2.vercel.app`  
**Backend URL**: `https://kidsafe-analyzer-backend-v2.onrender.com`

Share it with users and gather feedback for future versions! 🚀

