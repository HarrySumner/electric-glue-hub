# Installation Guide
## TV Campaign Impact Analyzer | Electric Glue

---

## Prerequisites

- **Python 3.9+** (recommended: 3.10 or 3.11)
- **pip** package manager
- **Virtual environment** (recommended)

---

## Quick Start (5 minutes)

### 1. Clone or Navigate to Project

```bash
cd C:\Users\harry\OneDrive\Desktop\EG\tv-campaign-impact-analyzer
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** This will install ~40 packages including:
- PyMC3 (Bayesian modeling)
- CausalImpact
- LangChain & LangGraph (agentic framework)
- Streamlit (UI)
- Plotly (visualizations)

### 4. Configure API Keys (Optional)

The Interpretation Agent can use LLMs for natural language generation. This is optional—the system falls back to rule-based interpretation if no API key is provided.

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your keys
# OPENAI_API_KEY=sk-...
# or
# ANTHROPIC_API_KEY=sk-ant-...
```

**Note:** You only need ONE of these (OpenAI OR Anthropic), not both.

### 5. Run the Application

```bash
python run_app.py
```

This will:
1. Generate sample data (if not exists)
2. Start Streamlit server on http://localhost:8501
3. Open your browser automatically

---

## Platform-Specific Notes

### Windows

**CausalImpact / PyMC3 Warning:**
You may see warnings about missing C compiler (g++) when running MCMC sampling. This is expected on Windows.

```
WARNING: PyTensor is using fallback to slower Python implementation
```

**Impact:** Analysis will work but may be slower (~30% slower than with optimized C backend).

**Solution (optional):**
- Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Or use WSL2 for Linux environment

**For production deployments**, we recommend cloud hosting (Linux) for optimal performance.

### Mac/Linux

No special configuration needed. PyMC3 will use optimized C backend automatically.

---

## Verifying Installation

Run this test script:

```bash
python -c "
from agents import OrchestratorAgent, create_sample_data
print('✅ Agents module loaded')

import streamlit
print('✅ Streamlit installed')

import causalimpact
print('✅ CausalImpact installed')

print('\n🎉 All systems ready!')
"
```

Expected output:
```
✅ Agents module loaded
✅ Streamlit installed
✅ CausalImpact installed

🎉 All systems ready!
```

---

## Troubleshooting

### Import Error: ModuleNotFoundError

**Problem:** `ModuleNotFoundError: No module named 'agents'`

**Solution:** Make sure you're running from the project root directory:

```bash
cd C:\Users\harry\OneDrive\Desktop\EG\tv-campaign-impact-analyzer
python run_app.py
```

### CausalImpact Installation Fails

**Problem:** `ERROR: Could not build wheels for causalimpact`

**Solution:**

1. Upgrade pip and setuptools:
```bash
pip install --upgrade pip setuptools wheel
```

2. Install dependencies separately:
```bash
pip install numpy pandas scipy statsmodels
pip install causalimpact
```

3. If still failing, use conda instead:
```bash
conda install -c conda-forge causalimpact
```

### LangGraph/LangChain Version Conflicts

**Problem:** `ERROR: pip's dependency resolver does not currently take into account all the packages that are installed`

**Solution:** Install specific versions:

```bash
pip install langchain==0.1.0 langgraph==0.0.20 --force-reinstall
```

### OpenAI/Anthropic API Errors

**Problem:** `AuthenticationError: Incorrect API key provided`

**Solution:**

1. Check your `.env` file has correct API key format:
```
OPENAI_API_KEY=sk-proj-...  # Should start with sk-proj- or sk-
ANTHROPIC_API_KEY=sk-ant-... # Should start with sk-ant-
```

2. Set `USE_LLM_AGENT=False` in `.env` to use rule-based interpretation instead

### Streamlit Port Already in Use

**Problem:** `OSError: [Errno 48] Address already in use`

**Solution:**

```bash
# Use different port
streamlit run streamlit_app/app.py --server.port=8502

# Or kill existing process
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8501 | xargs kill
```

---

## Optional: Development Setup

For development and testing:

### Install in Editable Mode

```bash
pip install -e .
```

### Run Tests

```bash
# Test data agent
python agents/data_agent.py

# Test validation agent
python agents/validation_agent.py

# Test analysis agent
python agents/analysis_agent.py

# Test interpretation agent
python agents/interpretation_agent.py

# Test orchestrator
python agents/orchestrator.py
```

### Generate Documentation

```bash
pip install pdoc3
pdoc --html --output-dir docs agents core config
```

---

## Next Steps

1. ✅ Installation complete → Run `python run_app.py`
2. 📊 Try sample data → Check "Use sample data" in sidebar
3. 📁 Upload your own data → CSV/Excel with date + metrics
4. 📧 Configure LLM (optional) → Add API keys to `.env`
5. 📈 Run analysis → Click "Run Analysis" button

---

## Support

**Electric Glue Team:**
- Technical Issues: Check GitHub Issues or contact dev team
- Business Questions: Contact Electric Glue account manager
- Bug Reports: File issue with error logs and data description

**Common Resources:**
- [README.md](README.md) - Full project overview
- [PROJECT_SPEC.md](PROJECT_SPEC.md) - Technical specification
- [.env.example](.env.example) - Configuration template

---

**Built by Electric Glue | Where AI Meets Marketing Science**
