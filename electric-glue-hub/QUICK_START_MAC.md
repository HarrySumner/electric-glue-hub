# Quick Start Guide for Mac

## Fix for Tim's Error: "ModuleNotFoundError: No module named 'config'"

The issue is now fixed! Follow these steps:

### 1. Remove the old broken clone
```bash
cd ~
rm -rf electric-glue-hub
```

### 2. Clone the updated repository
```bash
git clone https://github.com/HarrySumner/electric-glue-hub.git
cd electric-glue-hub
```

### 3. Navigate to the correct app directory
```bash
cd electric-glue-hub
```

### 4. Create and activate virtual environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 5. Install dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 6. Run the app
```bash
python -m streamlit run app.py
```

The app should now open in your browser at: **http://localhost:8501**

## What Was Fixed?

The GitHub repository was missing the `core/` folder which contains essential modules:
- `bayesian_causal_impact.py` - Causal analysis engine
- `qa_validator.py` - Quality assurance validation
- `llm_qa_validator.py` - LLM-based QA
- `api_usage_tracker.py` - API usage tracking

These have now been pushed to GitHub, so a fresh clone will work perfectly.

## If You Still Get Errors

### "command not found: python3.11"
Try: `python3` or `python` instead

### Port already in use
```bash
python -m streamlit run app.py --server.port 8502
```

### "source: no such file or directory"
Make sure you're in the correct directory:
```bash
pwd  # Should show: /Users/eg/electric-glue-hub/electric-glue-hub
```

## Quick Commands Summary

```bash
# Fresh install (run these in order)
cd ~
rm -rf electric-glue-hub
git clone https://github.com/HarrySumner/electric-glue-hub.git
cd electric-glue-hub/electric-glue-hub
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

## Feedback Link

Every page now has a feedback link at the bottom:
💬 Share Your Feedback → https://forms.gle/mXR2nYbJWZ6WzwPX8

Enjoy!
