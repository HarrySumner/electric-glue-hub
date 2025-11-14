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
