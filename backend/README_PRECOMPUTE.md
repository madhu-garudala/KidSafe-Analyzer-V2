# Generate Pre-computed Analyses

## Quick Command

```bash
cd backend
source venv/bin/activate
python generate_precomputed_analyses.py
```

## What It Does

This script:
1. Loads all 10 cereals from `Data/cereal.csv`
2. Analyzes each using the full RAG AI pipeline
3. Saves results to `../frontend/public/precomputed-analyses.json`

## Output File Location

```
frontend/public/precomputed-analyses.json
```

This file is automatically loaded by the frontend for instant results!

## When to Run

- ✅ **First time setup** (required)
- ✅ After adding new cereals
- ✅ After changing analysis prompts
- ✅ After updating FDA guidelines document

## Time Required

- ~10-20 seconds per cereal
- **Total: 2-3 minutes for 10 cereals**

## Prerequisites

- Backend virtual environment activated
- `.env` file with API keys configured
- Internet connection (for OpenAI API)

---

See [PRECOMPUTE_INSTRUCTIONS.md](../PRECOMPUTE_INSTRUCTIONS.md) for full details.

