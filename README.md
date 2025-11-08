# 🍎 KidSafe Food Analyzer - Version 2

An AI-powered application that helps parents make informed decisions about store-bought food products for their children by analyzing ingredient lists and providing detailed safety assessments.

![Tech Stack](https://img.shields.io/badge/React-18.2.0-blue?logo=react)
![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey?logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-0.3.0-orange)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [API Endpoints](#api-endpoints)
- [Advanced Retrieval Strategies](#advanced-retrieval-strategies)
- [Future Roadmap](#future-roadmap)

---

## 🎯 Overview

**KidSafe Food Analyzer V2** is a web application built with React (frontend) and Flask (backend) that leverages AI to analyze food ingredients specifically for children's safety. Parents can select cereal products from a database or input custom ingredient lists to receive detailed, evidence-based analysis powered by RAG (Retrieval-Augmented Generation) technology.

### Problem Statement

Parents struggle to quickly assess whether store-bought food products are safe for their children due to:
- Time constraints when shopping
- Complex ingredient terminology
- Hidden dangerous additives
- Information overload from conflicting sources

### Solution

KidSafe provides:
- **AI-Powered Analysis**: Using LangGraph and RAG with FDA guidelines
- **Clear Verdicts**: Immediate "GOOD ✅", "MODERATE ⚠️", or "BAD ❌" classifications
- **Ingredient Breakdown**: Detailed analysis of each ingredient
- **Evidence-Based**: All recommendations grounded in FDA food labeling guidelines
- **Interactive Chatbot**: Ask follow-up questions about any product

---

## 🌟 Key Features

### Frontend (React)
- ⚡ **Instant Analysis** - Pre-computed results for all cereals (no waiting!)
- ✨ Modern, responsive UI with gradient design
- 🎨 Smooth animations and transitions
- 📱 Mobile-friendly interface
- 💬 Real-time chatbot for ingredient questions
- 🚀 Blazing fast, component-based architecture

### Backend (Flask + LangChain)
- 🤖 Advanced RAG system with multiple retrieval strategies
- 🔍 Vector search using Qdrant
- 📊 LangGraph workflow orchestration
- 🎯 LangSmith integration for observability
- 🔄 Multiple retrieval strategies:
  - Naive Vector Search (baseline)
  - BM25 Keyword Search
  - Multi-Query Expansion
  - Cohere Reranking
  - Ensemble (recommended)

### Analysis Capabilities
- ✅ Clear safety verdicts (GOOD/MODERATE/BAD)
- 📋 Ingredient-by-ingredient breakdown
- ⚠️ Key concerns highlighting
- 💪 Positive aspects identification
- 🎓 Educational explanations based on FDA guidelines

---

## 🛠 Technology Stack

### Frontend
- **React 18.2** - Component-based UI framework
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client for API requests
- **CSS3** - Custom styling with animations

### Backend
- **Python 3.11** - Primary backend language
- **Flask 3.0** - Lightweight web framework
- **Flask-CORS** - Cross-origin resource sharing
- **LangChain 0.3** - AI application framework
- **LangGraph 0.2** - Workflow orchestration
- **OpenAI GPT-4o-mini** - Language model
- **Qdrant** - Vector database for embeddings
- **PyMuPDF** - PDF document processing
- **RAGAS 0.2** - Evaluation framework

### AI & ML
- **OpenAI Embeddings** - text-embedding-3-small
- **Cohere Rerank** - Advanced reranking (optional, improves accuracy)
- **LangSmith** - Observability and tracing

---

## 📁 Project Structure

```
KidSafe-Analyzer-V2/
├── backend/                       # Flask Backend
│   ├── backend/                   # Python package
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration
│   │   ├── vector_store.py        # Qdrant vector store
│   │   ├── rag_engine.py          # LangGraph RAG workflow
│   │   ├── advanced_retrieval.py  # Retrieval strategies
│   │   ├── evaluation.py          # Evaluation utilities
│   │   └── ragas_evaluation.py    # RAGAS evaluation
│   ├── Data/
│   │   ├── cereal.csv            # Cereal database
│   │   └── Input/
│   │       └── Food-Labeling-Guide-(PDF).pdf
│   ├── main.py                    # Flask application
│   ├── requirements.txt           # Python dependencies
│   ├── runtime.txt               # Python version
│   └── render.yaml               # Render deployment config
│
├── frontend/                      # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx         # Banner header
│   │   │   ├── APIConfig.jsx      # System status display
│   │   │   ├── CerealSelector.jsx # Product selector
│   │   │   ├── AnalysisResults.jsx # Results display
│   │   │   └── Chatbot.jsx        # Interactive chatbot
│   │   ├── services/
│   │   │   └── api.js             # API service layer
│   │   ├── App.jsx                # Main app component
│   │   ├── App.css                # App styles
│   │   ├── main.jsx               # React entry point
│   │   └── index.css              # Global styles
│   ├── index.html                 # HTML template
│   ├── vite.config.js             # Vite configuration
│   ├── vercel.json               # Vercel deployment config
│   └── package.json               # Frontend dependencies
│
├── start-app.sh                   # Start both servers
├── start-backend.sh               # Start backend only
├── start-frontend.sh              # Start frontend only
├── README.md                      # This file
├── DEPLOYMENT.md                  # Deployment guide
└── DEVELOPMENT.md                 # Local development guide
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (3.9 or higher) - [Download](https://www.python.org/downloads/)
- **API Keys** (get these first!):
  - OpenAI API Key (Required) - [Get it here](https://platform.openai.com/api-keys)
  - LangSmith API Key (Required) - [Get it here](https://smith.langchain.com/)
  - Cohere API Key (Optional, improves accuracy 20-30%) - [Get it here](https://dashboard.cohere.com/)

### ⚡ Automatic Setup & Start (Recommended)

The application now features **automatic setup** and **instant analysis**!

```bash
# Navigate to the project
cd KidSafe-Analyzer-V2

# Make scripts executable (first time only)
chmod +x *.sh

# Run automatic setup (first time only)
./setup.sh

# Generate pre-computed analyses (first time only, ~2-3 minutes)
cd backend
source venv/bin/activate
python generate_precomputed_analyses.py
cd ..

# Start the application (anytime)
./start-app.sh
```

**That's it!** 🎉 The scripts will:
- ✅ Auto-create Python virtual environment
- ✅ Auto-install all dependencies
- ✅ Create `.env` template for your API keys
- ✅ Generate instant-load analyses (one time)
- ✅ Start both backend and frontend
- ✅ Open your browser automatically

The app will be available at:
- Frontend: `http://localhost:3000` - **Instant results!** ⚡
- Backend: `http://localhost:5001` - For chatbot questions

### 📝 Adding Your API Keys

After running `setup.sh`, edit `backend/.env` with your actual API keys:

```bash
nano backend/.env  # or use your favorite editor
```

Replace the placeholders with your real keys, then run `./start-app.sh`

### 📚 More Information

- **Quick Start**: See [QUICKSTART.md](./QUICKSTART.md) for detailed instructions
- **Manual Setup**: See [DEVELOPMENT.md](./DEVELOPMENT.md) for manual setup
- **Deployment**: See [DEPLOYMENT.md](./DEPLOYMENT.md) for cloud deployment

---

## 📚 Documentation

- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Local development setup and workflow
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Cloud deployment guide (Vercel + Render)

---

## 📡 API Endpoints

### Base URL (Local)
```
http://localhost:5001
```

### Endpoints

#### 1. Health Check
```http
GET /
```

#### 2. System Status
```http
GET /api/status
```

#### 3. Get Cereals List
```http
GET /api/cereals
```

#### 4. Analyze Ingredients
```http
POST /api/analyze
Content-Type: application/json

{
  "cereal_name": "Product Name",
  "ingredients": "Ingredient list..."
}
```

#### 5. Chat with AI
```http
POST /api/chat
Content-Type: application/json

{
  "cereal_name": "Product Name",
  "ingredients": "Ingredient list...",
  "question": "Your question",
  "previous_analysis": "Previous analysis text",
  "chat_history": []
}
```

---

## 🔍 Advanced Retrieval Strategies

The application implements multiple retrieval strategies:

| Strategy | Speed | Accuracy | Best For |
|----------|-------|----------|----------|
| Naive | ⚡⚡⚡ | ⭐⭐⭐ | Simple semantic queries |
| BM25 | ⚡⚡⚡ | ⭐⭐⭐ | Keyword matching |
| Multi-Query | ⚡⚡ | ⭐⭐⭐⭐ | Complex questions |
| Compression | ⚡⚡ | ⭐⭐⭐⭐⭐ | High precision needs |
| Ensemble | ⚡⚡ | ⭐⭐⭐⭐⭐ | Production use (default) |

**Ensemble** (recommended) combines multiple strategies using Reciprocal Rank Fusion for best results.

---

## 🚀 Future Roadmap

### Phase 2: Enhanced Features
- [ ] Mobile app with camera-based ingredient scanning (OCR)
- [ ] Barcode scanning for instant product lookup
- [ ] Personalized profiles for children with allergies
- [ ] Alternative product recommendations
- [ ] Offline mode for in-store use

### Phase 3: Advanced Capabilities
- [ ] Percentage-based safety scoring (0-100%)
- [ ] Multi-factor analysis dashboard
- [ ] Allergen detection with severity levels
- [ ] Nutritional value comparison charts
- [ ] Community ratings and reviews

### Phase 4: Enterprise Features
- [ ] Dietitian/pediatrician recommendations
- [ ] School cafeteria menu analysis
- [ ] Bulk product analysis
- [ ] API for third-party integration

---

## 🙏 Acknowledgments

- **AI Makerspace** - AI Engineering Bootcamp Cohort 8
- **LangChain** - Powerful AI application framework
- **OpenAI** - GPT-4o-mini and embeddings
- **FDA** - Comprehensive food labeling guidelines
- **React & Flask Teams** - Excellent frameworks

---

## 📄 Version History

- **V2 (Current)** - Backup version with core features
  - AI-powered ingredient analysis
  - Interactive chatbot
  - Multiple retrieval strategies
  - Full deployment support

---

## 📞 Support

For issues or questions:
- Create an issue in the repository
- Check documentation in DEVELOPMENT.md and DEPLOYMENT.md

---

**Built with ❤️ for parents who care about their children's health**

*Making food safety analysis accessible, accurate, and actionable.*

