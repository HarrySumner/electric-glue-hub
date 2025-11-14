# TV Campaign Impact Analyzer
## Agentic AI for Television Advertising Attribution

**Built for Electric Glue** | Proprietary Marketing Intelligence Tool

---

## What This Is

An **intelligent multi-agent system** that measures the causal impact of TV advertising campaigns using Bayesian structural time series analysis.

Unlike traditional attribution tools, this uses **specialized AI agents** that automatically:
- ✅ Clean and validate your data
- ✅ Detect confounders and data quality issues
- ✅ Select the appropriate statistical model
- ✅ Generate plain-English explanations
- ✅ Provide actionable recommendations

**Key Innovation:** Avoids the pitfalls of Difference-in-Differences (DID) methods when regional confounders exist.

---

## Why We Built This

### The Nielsen Problem

**Scenario:** Regional TV campaign for Nielsen
**Initial Approach:** Difference-in-Differences (compare targeted vs control regions)
**Critical Issue:** Control regions were contaminated by:
- Increased flight path availability from local airports
- TV ad spillover via streaming and travel
- Different regional economic trends

**Result:** DID assumptions violated → Unreliable estimates

### The Solution

**Bayesian Structural Time Series (BSTS):**
- No geographic controls needed
- Builds synthetic counterfactual from pre-campaign data
- Explicitly controls for confounders (flight availability, other marketing)
- Quantifies uncertainty via posterior distributions
- Robust to regional heterogeneity

---

## How It Works: Multi-Agent Architecture

### The Agent Team

```
1. DATA AGENT
   └─ Ingests, cleans, validates time series data
   └─ Auto-detects columns and suggests covariates

2. VALIDATION AGENT
   └─ Checks for structural breaks and outliers
   └─ Detects confounders
   └─ Assigns data quality score

3. ANALYSIS AGENT
   └─ Selects appropriate Bayesian model
   └─ Fits BSTS via MCMC
   └─ Computes causal effect estimates

4. INTERPRETATION AGENT
   └─ Translates stats to plain English
   └─ Generates recommendations
   └─ Creates visualizations

5. ORCHESTRATOR AGENT
   └─ Coordinates the workflow
   └─ Handles errors gracefully
   └─ Manages state
```

---

## Quick Start

### Installation

```bash
cd tv-campaign-impact-analyzer
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run streamlit_app/app.py
```

### Upload Your Data

**Required Columns:**
- `date`: Timestamps (daily or weekly)
- `[target_metric]`: Revenue, conversions, bookings, etc.

**Optional (Recommended):**
- `tv_spend`: TV advertising spend
- `[covariates]`: Other marketing channels, external factors

**Example:**
```csv
date,revenue,tv_spend,digital_spend,flights_available
2024-01-01,45000,0,5000,120
2024-01-02,47000,0,5200,122
...
2024-06-01,65000,15000,5500,135  # TV campaign starts
```

### Workflow

1. **Upload** CSV/Excel
2. **Configure** pre/post periods
3. **Select** covariates to control for
4. **Run** analysis (agents work automatically)
5. **Review** results and recommendations
6. **Export** PDF report

---

## Features

### 🤖 Agentic Intelligence
- Automatic data quality assessment
- Smart model selection based on data characteristics
- Self-healing when issues detected
- Natural language explanations

### 📊 Robust Statistical Methods
- Bayesian structural time series (not DID)
- Local level + trend + seasonality
- Regression on covariates
- Posterior distributions for uncertainty

### 🎨 Electric Glue Branding
- Custom orange/blue gradient design
- Agent status indicators
- Interactive visualizations
- Professional client-ready output

### 📈 Comprehensive Results
- Causal effect estimate with credible intervals
- Actual vs counterfactual visualization
- Pointwise and cumulative effects
- Covariate contributions
- ROI calculations

### 📤 Export Options
- PDF report with Executive Summary
- CSV of detailed results
- Interactive HTML dashboard
- Shareable links

---

## Technical Stack

- **Agent Framework:** LangGraph + LangChain
- **Bayesian Modeling:** PyMC3, CausalImpact
- **Time Series:** Statsmodels, Prophet
- **Data Processing:** Pandas, NumPy
- **LLM:** OpenAI GPT-4 or Anthropic Claude (for Interpretation Agent)
- **Visualization:** Plotly, Matplotlib
- **Interface:** Streamlit
- **Database:** PostgreSQL (analysis history)

---

## Project Structure

```
tv-campaign-impact-analyzer/
├── agents/
│   ├── __init__.py
│   ├── data_agent.py           # Data ingestion & cleaning
│   ├── validation_agent.py     # Quality checks & confounder detection
│   ├── analysis_agent.py       # Bayesian model fitting
│   ├── interpretation_agent.py # Natural language explanations
│   └── orchestrator.py         # Workflow coordination
├── core/
│   ├── __init__.py
│   ├── bayesian_models.py      # BSTS implementations
│   ├── validation.py           # Statistical tests
│   └── utils.py                # Helper functions
├── config/
│   ├── branding.py             # Electric Glue styling
│   └── settings.py             # Configuration
├── streamlit_app/
│   ├── app.py                  # Main Streamlit interface
│   ├── components.py           # Reusable UI components
│   └── pages/                  # Multi-page app
├── data/                       # Sample datasets
├── docs/                       # Documentation
├── requirements.txt
├── PROJECT_SPEC.md
└── README.md
```

---

## Use Cases

### 1. TV Campaign ROI Measurement
**Client:** Travel brand (e.g., Nielsen)
**Question:** "Did our TV campaign drive incremental bookings?"
**Output:** "TV campaign drove £450K incremental revenue (95% credible interval: £320K-£580K)"

### 2. Channel Mix Optimization
**Client:** Retail brand
**Question:** "Should we shift budget from digital to TV?"
**Output:** "TV has 3.2x ROAS vs 1.8x for digital when accounting for baseline trends"

### 3. Regional Campaign Analysis
**Client:** Financial services
**Question:** "Which regions showed strongest TV response?"
**Output:** "Scotland: £180K lift, Wales: £95K lift, controlling for regional economic factors"

### 4. Seasonality-Adjusted Attribution
**Client:** E-commerce
**Question:** "What's the true lift excluding Black Friday spike?"
**Output:** "TV drove +18% lift above seasonal baseline, avoiding contamination from holiday shopping"

---

## Advantages Over Traditional Methods

### vs Difference-in-Differences (DID)
- ❌ **DID Problem:** Requires parallel trends assumption (often violated)
- ✅ **BSTS Solution:** No geographic controls needed, robust to regional heterogeneity

### vs Simple Before/After
- ❌ **Before/After Problem:** Confounded by trends, seasonality, other marketing
- ✅ **BSTS Solution:** Explicitly models trends and covariates

### vs Multi-Touch Attribution
- ❌ **MTA Problem:** Assumes additive effects, can't prove causation
- ✅ **BSTS Solution:** Isolates causal effect with uncertainty quantification

### vs Marketing Mix Models (MMM)
- ❌ **MMM Problem:** Requires long historical data, less precise for single campaigns
- ✅ **BSTS Solution:** Works with shorter time series, campaign-specific estimates

---

## Roadmap

### Phase 1: MVP (Current)
- ✅ Single-agent prototype
- ✅ Basic BSTS model
- ✅ Streamlit interface
- ✅ Nielsen data analysis

### Phase 2: Multi-Agent (Weeks 1-2)
- 🔄 LangGraph orchestration
- 🔄 Specialized agents
- 🔄 Enhanced validation
- 🔄 LLM-powered interpretation

### Phase 3: Production (Weeks 3-4)
- ⏸️ API integrations (GA4, weather, economic data)
- ⏸️ Scenario analysis
- ⏸️ A/B testing (BSTS vs DID comparison)
- ⏸️ Knowledge base for learning

### Phase 4: Productization (Month 2+)
- ⏸️ Multi-client deployment
- ⏸️ Automated reporting
- ⏸️ White-label version
- ⏸️ API access

---

## Business Model

### Internal Use (Electric Glue)
- **Value:** Measure TV ROI for 10-20 campaigns per year
- **Time Savings:** 40+ hours per campaign (manual analysis → 30 minutes)
- **Quality:** Statistical rigor + client confidence

### External Service
- **Offering:** "TV Campaign Attribution Analysis"
- **Price:** £3-5K per campaign
- **Delivery:** 2-3 days (mostly automated)
- **Market:** Travel, retail, financial services, automotive

### SaaS Model (Future)
- **Offering:** Self-service platform
- **Price:** £500-1K per month subscription
- **Target:** Mid-size brands with regular TV spend

---

## Support

**Electric Glue Team:**
- Technical Lead: [Your Name]
- Project Sponsor: [Managing Director]
- Client Success: [Account Director]

**For Issues:**
- GitHub: [Repository Link]
- Email: [Support Email]
- Slack: #tv-impact-analyzer

---

## License

© 2025 Electric Glue. Proprietary and Confidential.

This tool is built for internal Electric Glue use and approved client engagements.

---

**Built with Intelligence. Powered by Data. Designed for Impact.**

*Electric Glue - Where AI Meets Marketing Science*
