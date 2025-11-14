#!/bin/bash

echo "🚀 Initializing Marketing-Assistance GitHub Repository"
echo "=========================================="

# Set repository URL
REPO_URL="https://github.com/HarrySumner/Marketing-assistance.git"

# Navigate to project root
cd "/c/Users/harry/OneDrive/Desktop/EG" || exit

# Check if already a git repo
if [ -d ".git" ]; then
    echo "⚠️  Git repository already exists"
    read -p "Do you want to reinitialize? (y/N): " confirm
    if [ "$confirm" != "y" ]; then
        echo "Aborted."
        exit 0
    fi
    rm -rf .git
fi

# Initialize git
echo "📦 Initializing git repository..."
git init

# Create main branch
git branch -M main

# Add remote
echo "🔗 Adding remote repository..."
git remote add origin "$REPO_URL"

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p docs/prompts
mkdir -p docs/implementation
mkdir -p docs/specifications
mkdir -p docs/guides
mkdir -p docs/examples

# Copy documentation files
echo "📄 Organizing documentation..."
cp scout_enhanced_prompts.md docs/prompts/
cp scout_quality_enforcement_system.md docs/prompts/quality_enforcement.md
cp scout_implementation_guide.md docs/implementation/
cp PROJECT_2_SCOUT_COMPLETE_SPECIFICATION.md docs/specifications/
cp PROJECT_2_MARKETING_INTELLIGENCE_ASSISTANT.md docs/specifications/
cp GITHUB_REPO_STRUCTURE.md docs/

# Create main README
cat > README.md << 'EOL'
# Electric Glue - Marketing Intelligence Platform

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)

Professional-grade marketing intelligence and analytics platform built with multi-agent AI.

## 🎯 Products

### 1. Scout Intelligence Platform
AI-powered competitive intelligence and market research system that generates C-suite ready strategic briefs in minutes.

**Key Features:**
- Multi-agent research system (Company, Competitive, Market Trends agents)
- Quality enforcement with 7 mandatory gates
- Professional analyst-grade output (85+ quality score)
- Full source citation and confidence scoring

[→ View Scout Documentation](docs/specifications/PROJECT_2_SCOUT_COMPLETE_SPECIFICATION.md)

### 2. Causal Impact Analyzer
Bayesian structural time series (BSTS) analysis for measuring true campaign impact.

**Key Features:**
- Counterfactual modeling
- Confidence intervals
- Intervention value estimation
- Professional visualizations

[→ View in Electric Glue Hub](electric-glue-hub/)

### 3. Marketing Intelligence Hub
Unified Streamlit dashboard for all marketing analytics tools.

[→ View Hub](electric-glue-hub/)

## 📚 Documentation

- **Scout Prompts**: [Enhanced Prompt System](docs/prompts/scout_enhanced_prompts.md)
- **Quality System**: [Quality Enforcement](docs/prompts/quality_enforcement.md)
- **Implementation**: [Implementation Guide](docs/implementation/scout_implementation_guide.md)
- **Project Specs**: [Complete Specifications](docs/specifications/)

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/HarrySumner/Marketing-assistance.git
cd Marketing-assistance

# Navigate to Electric Glue Hub
cd electric-glue-hub

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🏗️ Project Structure

```
Marketing-assistance/
├── docs/                    # Documentation
│   ├── prompts/            # Prompt engineering guides
│   ├── implementation/     # Implementation guides
│   ├── specifications/     # Project specifications
│   └── guides/             # User guides
├── electric-glue-hub/      # Main Streamlit application
│   ├── pages/              # Multi-page apps
│   ├── config/             # Configuration & branding
│   └── utils/              # Utility functions
└── scout/                  # Scout Intelligence Platform (coming soon)
    ├── agents/             # AI agents
    ├── core/               # Core functionality
    └── services/           # External services
```

## 📊 Key Features

### Scout Intelligence Platform
- **Quality Enforcement**: 7-stage quality gate system ensures professional output
- **Multi-Agent Architecture**: Specialized agents for different research types
- **Confidence Scoring**: Every fact tagged with confidence level
- **Professional Output**: C-suite ready strategic briefs

### Causal Impact Analyzer
- **Bayesian Analysis**: BSTS for rigorous causal inference
- **No Control Group Needed**: Synthetic control from pre-period data
- **Uncertainty Quantification**: Full confidence intervals
- **Value Estimation**: Calculate monetary impact

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Anthropic Claude 3.7 Sonnet
- **Agent Framework**: LangGraph
- **Data Analysis**: pandas, numpy, scikit-learn
- **Visualization**: matplotlib, plotly

## 📈 Status

- ✅ Causal Impact Analyzer - Production Ready
- ✅ Scout Documentation - Complete
- 🚧 Scout Implementation - In Development
- 🚧 Additional Tools - Planned

## 📝 License

MIT License

## 📞 Contact

**Electric Glue**
- GitHub: [@HarrySumner](https://github.com/HarrySumner)
- Issues: [GitHub Issues](https://github.com/HarrySumner/Marketing-assistance/issues)

---

**Built with** 💚 **by Electric Glue**
*Powered by Multi-Agent AI × Front Left Thinking*
EOL

# Create .gitignore
cat > .gitignore << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.venv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp

# Environment
.env
.env.local

# Data
data/
*.db
*.sqlite

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Test outputs
test_*.png
test_*.py
EOL

# Stage all files
echo "➕ Staging files..."
git add .

# Initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Electric Glue Marketing Intelligence Platform

Features:
- Scout Intelligence Platform documentation
- Enhanced prompt engineering system
- Quality enforcement framework (7-stage gates)
- Implementation guides
- Causal Impact Analyzer (Streamlit app)
- Electric Glue Hub dashboard
- Complete project specifications"

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Repository initialized and pushed successfully!"
echo "🌐 View at: https://github.com/HarrySumner/Marketing-assistance"
echo ""
echo "Next steps:"
echo "1. Visit the repository on GitHub"
echo "2. Add repository description and topics"
echo "3. Enable GitHub Pages (optional)"
echo "4. Review and customize README.md"
