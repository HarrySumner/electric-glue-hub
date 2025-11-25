# Electric Glue Hub - Setup Instructions

## Prerequisites

- Python 3.11 or higher
- Git installed

## Setup Steps

### 1. Clone the Repository

```bash
cd ~
git clone https://github.com/HarrySumner/electric-glue-hub.git
cd electric-glue-hub
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Upgrade pip and Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Create Required Directory Structure

The app needs the following directories that are not in the Git repo:

```bash
mkdir -p electric-glue-hub/config
mkdir -p electric-glue-hub/core
mkdir -p electric-glue-hub/agents
mkdir -p electric-glue-hub/models
mkdir -p electric-glue-hub/pages
```

**IMPORTANT:** You need to copy these files from the shared location:
1. **config/** folder (all Python files inside)
2. **core/** folder (all Python files inside)
3. **agents/** folder (all Python files inside)
4. **models/** folder (if any Python files)
5. **pages/** folder (all page Python files)

These folders contain the core application logic and are not committed to GitHub.

### 5. Configure API Keys (Optional)

Create a `.env` file in the root directory:

```bash
touch .env
```

Add your API keys (optional - some features work without them):

```
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

**Note:** You can configure API keys later through the Settings page in the app.

### 6. Run the Application

**Using the helper script (recommended):**
```bash
python run_hub.py
```

**Or run Streamlit directly:**
```bash
streamlit run electric-glue-hub/app.py
```

**On macOS/Linux:**
```bash
python -m streamlit run electric-glue-hub/app.py
```

The app should now be running at: http://localhost:8501

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'config'"

**Cause:** Missing core application files that aren't in the Git repo.

**Solution:** You need to copy the following folders from a working installation:
- `electric-glue-hub/config/`
- `electric-glue-hub/core/`
- `electric-glue-hub/agents/`
- `electric-glue-hub/pages/`

These folders should be placed inside the `electric-glue-hub/` directory.

### Error: "command not found: python"

**On macOS:** Use `python3` or `python3.11` instead of `python`

**On Windows:** Make sure Python is installed and in your PATH

### Error: "source: no such file or directory: .venv/bin/activate"

**Cause:** Virtual environment not created properly or wrong path.

**Solution:**
1. Make sure you're in the `electric-glue-hub` directory
2. Check that `.venv` folder exists: `ls -la .venv`
3. Recreate the virtual environment: `rm -rf .venv && python3.11 -m venv .venv`

### Port 8501 already in use

**Solution:** Kill the existing Streamlit process or use a different port:
```bash
streamlit run electric-glue-hub/app.py --server.port 8502
```

## Directory Structure

After setup, your directory should look like:

```
electric-glue-hub/
├── .venv/                      # Virtual environment (created during setup)
├── .env                        # API keys (optional)
├── electric-glue-hub/
│   ├── config/                 # ⚠️ Must copy from working installation
│   │   ├── __init__.py
│   │   ├── branding.py
│   │   └── qa_status.py
│   ├── core/                   # ⚠️ Must copy from working installation
│   │   ├── __init__.py
│   │   ├── bayesian_causal_impact.py
│   │   ├── qa_validator.py
│   │   ├── llm_qa_validator.py
│   │   └── api_usage_tracker.py
│   ├── agents/                 # ⚠️ Must copy from working installation
│   │   ├── __init__.py
│   │   ├── scout_research_agent.py
│   │   └── perspective_agents.py
│   ├── pages/                  # ⚠️ Must copy from working installation
│   │   ├── 2_Causal_Impact_Analyzer.py
│   │   ├── 4_Marketing_Intelligence.py
│   │   ├── 5_Report_QA_Agent.py
│   │   └── 6_Settings.py
│   ├── app.py                  # Main app entry point
│   └── README.md
├── requirements.txt
└── run_hub.py
```

## Next Steps

1. Open your browser to http://localhost:8501
2. Configure API keys in Settings (if needed)
3. Start using the tools!

## Support

If you encounter issues:
1. Check that all folders from the working installation are copied
2. Verify Python version: `python --version` (should be 3.11+)
3. Ensure all dependencies installed: `pip list`
4. Check the terminal for specific error messages

## Sharing Files

To share with a colleague, send them:
1. Link to the GitHub repository
2. A zip file containing:
   - `electric-glue-hub/config/` folder
   - `electric-glue-hub/core/` folder
   - `electric-glue-hub/agents/` folder
   - `electric-glue-hub/pages/` folder
3. This SETUP_INSTRUCTIONS.md file
