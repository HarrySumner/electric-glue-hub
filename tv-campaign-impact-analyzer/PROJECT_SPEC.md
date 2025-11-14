# TV Campaign Impact Analyzer
## Agentic Causal Impact Analysis for Television Advertising

**Client:** Electric Glue
**Project Type:** Campaign Measurement & Attribution
**Framework:** Multi-Agent Bayesian Time Series Analysis
**Status:** Development

---

## Executive Summary

An **agentic AI system** for measuring the causal impact of TV advertising campaigns using Bayesian structural time series models, specifically designed to avoid the pitfalls of Difference-in-Differences (DID) methods when regional confounders exist.

### Key Innovation: Why Agentic?

Traditional causal impact tools are **single-purpose calculators**. This system uses **specialized AI agents** that:

1. **Data Agent**: Intelligently ingests, cleans, and validates time series data
2. **Validation Agent**: Checks for confounders, structural breaks, data quality issues
3. **Analysis Agent**: Selects and runs appropriate Bayesian models based on data characteristics
4. **Interpretation Agent**: Generates plain-English explanations and recommendations
5. **Orchestrator Agent**: Coordinates the workflow and handles errors gracefully

This **agent-first architecture** enables:
- Automatic detection of data issues before analysis
- Dynamic model selection based on data properties
- Self-healing when APIs fail or data is malformed
- Natural language interaction ("analyze this campaign")
- Continuous learning from past analyses

---

## Problem Statement: Nielsen Campaign Learnings

### What We Learned

**Campaign:** Nielsen TV campaign (regionally targeted)

**Initial Approach:** Difference-in-Differences (DID)
- Compare targeted regions to control regions
- Measure differential impact

**Critical Issue Discovered:**
Regional controls were **contaminated** by increased flight path availability from airports serving Nielsen customers. This created a **spurious correlation** that invalidated DID assumptions.

**Lesson:** Geographic DID is unreliable when:
- External factors (flight availability, new store openings, infrastructure changes) affect regions differently
- Treatment spillover occurs (TV ads seen in "control" regions via streaming, travel)
- Regional trends diverge for unrelated reasons

### Solution: Bayesian Structural Time Series

Instead of comparing regions, we use:

1. **Synthetic Control via Bayesian Methods**
   - Build counterfactual using pre-intervention time series
   - No geographic controls needed
   - Control for confounders using covariates (seasonality, trends, other marketing)

2. **Robust to Confounders**
   - Model includes flight availability, economic indicators as covariates
   - Automatically adjusts for structural changes
   - Uncertainty quantification via posterior distributions

3. **Flexible Model Specification**
   - Local level + trend components
   - Seasonal patterns (weekly, monthly, yearly)
   - Regression on external predictors
   - Dynamic coefficients

---

## System Architecture: Multi-Agent Design

### Agent Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR AGENT                         │
│  (Coordinates workflow, handles errors, makes decisions)     │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  DATA AGENT   │   │ VALIDATION    │   │  ANALYSIS     │
│               │   │    AGENT      │   │    AGENT      │
│ • Ingest      │   │ • Check       │   │ • Select      │
│ • Clean       │   │   quality     │   │   model       │
│ • Transform   │   │ • Detect      │   │ • Fit BSTS    │
│ • Enrich      │   │   issues      │   │ • Compute     │
│               │   │ • Flag risks  │   │   posteriors  │
└───────────────┘   └───────────────┘   └───────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                  ┌───────────────────┐
                  │ INTERPRETATION    │
                  │      AGENT        │
                  │ • Summarize       │
                  │ • Explain         │
                  │ • Recommend       │
                  │ • Flag caveats    │
                  └───────────────────┘
```

### Agent Specifications

#### 1. Data Agent
**Responsibilities:**
- Parse CSV/Excel uploads
- Auto-detect date columns, metrics, potential covariates
- Handle missing values (interpolation vs flagging)
- Enrich with external data (if available via APIs)
- Create time-aligned dataset for analysis

**Decisions It Makes:**
- Which imputation method to use (forward fill, interpolation, none)
- Whether to aggregate data (daily → weekly if too sparse)
- Which columns are potential covariates vs target metrics

**Tools:**
- Pandas, NumPy
- API integrations (GA4, weather, economic data)
- Data quality libraries

#### 2. Validation Agent
**Responsibilities:**
- Check for structural breaks (CUSUM, Chow test)
- Detect outliers and anomalies
- Validate stationarity assumptions
- Check for confounders (correlation analysis)
- Assess data sufficiency (min periods, coverage)

**Decisions It Makes:**
- Whether data is suitable for Bayesian analysis
- If pre-processing is needed (detrending, differencing)
- Which covariates to include as controls
- Whether to flag high-risk analysis conditions

**Tools:**
- Statsmodels (stationarity tests)
- Scipy (outlier detection)
- Custom confounder detection

#### 3. Analysis Agent
**Responsibilities:**
- Select appropriate BSTS model specification
- Configure priors based on data characteristics
- Fit model via MCMC (PyMC or similar)
- Compute posterior distributions
- Calculate causal effect estimates with credible intervals

**Decisions It Makes:**
- Local level vs local linear trend
- Seasonal period selection (7, 30, 365 days)
- Number of MCMC iterations needed
- Which covariates to include in regression component

**Tools:**
- PyMC3/PyMC4 (Bayesian modeling)
- CausalImpact library (baseline)
- Custom BSTS implementations

#### 4. Interpretation Agent
**Responsibilities:**
- Translate statistical results to plain English
- Generate executive summary
- Create recommendations based on findings
- Flag caveats and limitations
- Produce visualizations with explanations

**Decisions It Makes:**
- How to phrase uncertainty (confidence levels)
- Which visualizations to prioritize
- What recommendations to make based on results

**Tools:**
- LLM (GPT-4 or Claude) for natural language generation
- Template-based reporting
- Visualization libraries (Plotly)

#### 5. Orchestrator Agent
**Responsibilities:**
- Route requests to appropriate agents
- Handle agent failures gracefully
- Manage state across the workflow
- Make high-level decisions (retry, skip, abort)
- Log all actions for reproducibility

**Decisions It Makes:**
- Whether to proceed to next step or request user input
- How to handle conflicting agent recommendations
- When to trigger alerts or warnings

**Tools:**
- LangGraph (agent orchestration)
- State management (Redis or PostgreSQL)
- Error handling and logging

---

## Technical Stack

### Core Components
- **Agent Framework:** LangGraph + LangChain
- **Bayesian Modeling:** PyMC3, CausalImpact (Python port)
- **Time Series:** Statsmodels, Prophet (for comparison)
- **Data Processing:** Pandas, NumPy, Polars
- **LLM Integration:** OpenAI GPT-4 or Anthropic Claude
- **Visualization:** Plotly, Matplotlib
- **Web Interface:** Streamlit
- **Database:** PostgreSQL (analysis history)

### Infrastructure
- **Hosting:** Streamlit Cloud or AWS
- **APIs:** Optional integrations (GA4, weather, economic indicators)
- **Compute:** CPU sufficient (MCMC can be slow, provide progress updates)

---

## Key Features

### 1. Intelligent Data Ingestion
- Upload CSV/Excel with TV campaign data
- Auto-detection of date column, target metric, potential covariates
- Validation checks before proceeding
- Enrichment suggestions ("Do you have weather data? Economic indicators?")

### 2. Automated Confounder Detection
- **Not**: Geographic DID (learned from Nielsen)
- **Instead**: Time series covariates (flight availability, competitor spend, seasonality)
- Correlation analysis to suggest controls
- Flag potential confounders for user review

### 3. Bayesian Structural Time Series
- Local level + trend + seasonal components
- Regression on external predictors
- Posterior distributions for uncertainty
- No need for geographic controls

### 4. Model Selection Intelligence
- Analysis Agent chooses model based on:
  - Data frequency (daily, weekly, monthly)
  - Presence of trend
  - Seasonal patterns detected
  - Number of covariates
- User can override or approve

### 5. Natural Language Explanations
- "Your TV campaign drove an estimated £450K in incremental revenue"
- "There's a 95% probability the effect is between £320K and £580K"
- "Key caveat: Flight availability increased during the campaign, but we controlled for this"

### 6. Interactive Visualizations
- Actual vs counterfactual (what would have happened without TV)
- Pointwise causal effect over time
- Cumulative effect
- Posterior distributions
- Covariate contributions

### 7. Scenario Analysis
- "What if we had spent 20% more on TV?"
- "What if the campaign had run 2 weeks longer?"
- Sensitivity analysis on priors

---

## Workflow: User Journey

### Step 1: Upload Data
User uploads CSV with columns:
- `date`: Daily or weekly timestamps
- `revenue` (or `conversions`, `bookings`): Target metric
- `tv_spend`: TV advertising spend (optional but helpful)
- `[covariates]`: Other marketing channels, external factors

### Step 2: Data Agent Processes
- Detects date column automatically
- Identifies target metric (user confirms)
- Suggests potential covariates
- Shows data preview with quality summary

### Step 3: Validation Agent Reviews
- Checks for structural breaks
- Flags outliers (with option to keep/remove)
- Tests for confounders
- Provides green/amber/red quality score

### Step 4: User Configures Analysis
- Select pre-intervention period (before TV campaign)
- Select post-intervention period (during/after campaign)
- Choose covariates to include as controls
- Review model specification suggested by Analysis Agent

### Step 5: Analysis Agent Runs Model
- Fits Bayesian structural time series
- Shows progress bar (MCMC iterations)
- Computes causal effect estimates
- Generates credible intervals

### Step 6: Interpretation Agent Explains
- Plain-English summary
- Visualizations with annotations
- Recommendations ("Continue this level of TV spend", "Consider increasing")
- Caveats and limitations

### Step 7: Export & Share
- Download PDF report
- Export results to CSV/Excel
- Share link to interactive dashboard
- Save analysis for future comparison

---

## Avoiding DID Pitfalls: Technical Approach

### Why Not DID for Nielsen?

**DID Assumption:**
> Treated and control regions would have followed **parallel trends** absent treatment.

**Nielsen Reality:**
- Flight availability increased → More travel → Different regional trends
- TV ads seen across regions (streaming, travel spillover)
- Economic conditions varied regionally

**Result:** Parallel trends violated → DID estimates biased

### Bayesian Alternative

**BSTS Assumption:**
> We can build a **synthetic control** from pre-intervention data using observable covariates.

**Nielsen Application:**
1. Model pre-campaign revenue using:
   - Historical trend
   - Seasonality (weekly, monthly)
   - Flight availability (covariate)
   - Other marketing spend (covariate)
   - Economic indicators (covariate)

2. Forecast what revenue **would have been** during campaign period

3. Compare actual revenue to forecast → Causal effect

**Advantages:**
- No geographic controls needed
- Explicitly controls for flight availability
- Uncertainty quantification
- Robust to regional heterogeneity

### Model Specification (Technical)

```
y_t = μ_t + β'x_t + ε_t

where:
  μ_t = local level + trend + seasonal components
  β'x_t = regression on covariates (flight availability, other marketing)
  ε_t ~ N(0, σ²)

Priors:
  Local level: random walk
  Trend: random walk or static
  Seasonal: sum-to-zero constraint
  β ~ N(0, prior_sd²)
```

---

## Success Metrics

### Technical Performance
- **Model Convergence:** Rhat < 1.1 for all parameters
- **Predictive Accuracy:** <10% MAPE on held-out pre-period
- **Credible Interval Coverage:** 95% intervals capture truth in simulations

### User Experience
- **Time to Insight:** <5 minutes from upload to results
- **Explanation Quality:** 4.5/5+ rating from EG team
- **Actionability:** 80%+ of analyses lead to clear recommendations

### Business Impact
- **Client Value:** Enable TV ROI measurement for 10+ campaigns per year
- **Service Revenue:** Launch "TV Attribution Analysis" at £3-5K per campaign
- **Competitive Edge:** Only boutique agency with proprietary TV attribution

---

## Roadmap

### Phase 1: MVP (Weeks 1-4)
- Single-agent system (combined functionality)
- Basic BSTS model (local level + trend)
- Streamlit interface for upload and results
- CSV export

**Deliverable:** Working prototype for Nielsen data

### Phase 2: Multi-Agent (Weeks 5-8)
- Split into Data, Validation, Analysis, Interpretation agents
- LangGraph orchestration
- Enhanced model selection
- PDF report generation

**Deliverable:** Production-ready agentic system

### Phase 3: Advanced Features (Weeks 9-12)
- API integrations (GA4, weather, economic data)
- Scenario analysis
- A/B testing (compare BSTS to DID to show superiority)
- Knowledge base (past analyses for learning)

**Deliverable:** Full-featured TV attribution platform

---

## Why This Matters for Electric Glue

### Strategic Alignment

**From EXECUTIVE_SUMMARY_ALL_PROJECTS.md:**
> "These projects are designed to establish competitive differentiation as an AI-first boutique agency"

This project:
- ✅ Demonstrates **agentic AI** (aligned with EG's AI-first positioning)
- ✅ Solves **real client problem** (TV attribution is high-value)
- ✅ Creates **productized service** (sell to other clients)
- ✅ Builds **proprietary IP** (not off-the-shelf tools)

### Productization Opportunity

**New Service:** "TV Campaign Attribution Analysis"
- **Price:** £3-5K per campaign
- **Delivery:** 2-3 days (mostly automated)
- **Value Prop:** "Prove TV ROI with Bayesian rigor, avoid DID pitfalls"

**Potential Clients:**
- Travel brands (Nielsen, competitor brands)
- Retail with TV spend
- Financial services
- Automotive

**Market Size:** 20-30 potential campaigns per year across client base

---

## Next Steps

### Immediate (This Session)
1. Ingest Nielsen TV campaign data
2. Build basic BSTS model (single-agent)
3. Validate against known results
4. Create Streamlit prototype

### Week 1
1. Refactor into multi-agent architecture
2. Add LangGraph orchestration
3. Enhance validation checks
4. Build interpretation agent (LLM-powered)

### Week 2-4
1. Full feature set (scenario analysis, exports)
2. Documentation and user guide
3. Internal testing with EG team
4. Prepare for client deployment

---

**Ready to build! Awaiting Nielsen campaign data.**
