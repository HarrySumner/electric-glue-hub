# ⚡ Electric Glue Hub
## Unified Agentic Marketing Intelligence Platform

**Version:** 2.0.0
**Port:** http://localhost:8505
**Status:** Fully Redesigned | All Products Independent

---

## 🚀 Overview

Electric Glue Hub is a unified platform bringing together three powerful AI-powered marketing tools. Each product is built on multi-agent AI orchestration and designed to solve specific marketing analytics challenges.

### 🎯 Product 1: Causal Impact Analyzer
- **Status:** ✅ **Ready** (integrated in Hub)
- **Purpose:** Measure true causal impact of campaigns using Bayesian BSTS
- **Key Features:**
  - Bayesian structural time series methodology
  - Avoids Difference-in-Differences pitfalls
  - Handles seasonality, trends, and confounders
  - 5 specialized AI agents
  - Client-ready reports with counterfactual analysis
- **Use Cases:** TV, Radio, OOH campaign attribution
- **Access:** Navigate to Product 1 → Run Analysis in sidebar

### 🧠 Product 2: Scout (Marketing Intelligence Assistant)
- **Status:** ✅ **Beta** (integrated in Hub)
- **Purpose:** Multi-perspective analysis of marketing data
- **Key Features:**
  - 💰 **Stingy Customer** - Budget-focused, ROI-obsessed CFO perspective
  - 🔬 **Critical Thinker** - Analytical data scientist questioning assumptions
  - 🎨 **Creative Ad Man** - Visionary creative director seeing brand opportunities
  - Action-oriented one-pagers
  - Customizable perspectives
- **Use Cases:** Strategy reviews, stakeholder presentations, budget planning
- **Access:** Navigate to Product 2 → Run Analysis in sidebar

### 🛡️ Product 3: TrustCheck (Report QA Layer)
- **Status:** ⏳ **In Development** (Q2 2025)
- **Purpose:** Automated quality assurance for marketing reports
- **Key Features:**
  - Data cross-reference validation
  - Hallucination detection
  - Statistical anomaly flagging
  - Source verification
  - Confidence scoring (Green/Amber/Red)
- **Target:** Address #1 AI adoption barrier (quality concerns)
- **Access:** Overview available in sidebar

---

## 🏗️ Platform Architecture

The Electric Glue Hub uses a **unified navigation structure**:

```
Electric Glue Hub (http://localhost:8505)
│
├── 🏠 Home
│   ├── Welcome section
│   ├── Product cards (3 products)
│   └── Why Electric Glue section
│
├── 📊 Product 1: Causal Impact
│   ├── Overview (methodology, use cases, features)
│   └── Run Analysis (upload data, configure, view results)
│
├── 💡 Product 2: Scout
│   ├── Overview (perspectives, use cases, examples)
│   └── Run Analysis (input metrics, select perspectives, download)
│
└── ✓ Product 3: TrustCheck
    └── Overview (problem, solution, timeline)
```

Each product is **independent and self-contained** with its own:
- Overview page explaining methodology
- Analysis interface with dedicated workflow
- Branding consistent with Electric Glue identity

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
cd electric-glue-hub
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2. (Optional) Configure API Keys

For LLM-powered insights in Product 2 (Scout), create `.env`:

```bash
copy .env.example .env
# Edit .env and add your OpenAI or Anthropic API key
```

**Note:** The system works WITHOUT API keys using rule-based logic. LLM just enhances the narrative.

### 3. Run the Hub

```bash
python run_hub.py
```

Browser opens at **http://localhost:8505**

---

## Using Product 2: Marketing Intelligence Assistant

### Workflow

1. **Navigate** to Product 2 from Hub homepage
2. **Input Campaign Metrics:**
   - Total Spend (£)
   - Revenue Generated (£)
   - Sample Size
   - Time Period (days)
   - Brand Awareness (%)
   - Engagement Rate (%)
   - Marketing Channels used

3. **Add Context** (optional):
   - Industry
   - Target Audience
   - Campaign Type
   - Specific Questions

4. **Select Perspectives:**
   - Check which viewpoints you want (1-3)
   - Each provides different angle on same data

5. **Generate Report:**
   - Click "Generate Intelligence Report"
   - View insights from each perspective
   - Download Markdown or Text report

### Example Output

Each perspective provides:
- **Key Insight** (2-3 sentences)
- **Top 3 Actions** (specific, actionable)
- **Warning/Caveat** (what to watch out for)

**Example (Stingy Customer):**
> "Barely breaking even at 2.4x ROAS. We're spending £50,000 to make £120,000. Not good enough."
>
> Actions:
> 1. Cut bottom 20% performers immediately - Reallocate that £10K to proven channels
> 2. Demand proof before any new spend - Pilot test with £5-10K max
> 3. Negotiate all vendor contracts down 15-20%

---

## The Three Perspectives Explained

### 💰 Stingy Customer
**Persona:** Budget-conscious CFO who scrutinizes every pound

**Focus:**
- ROI and efficiency
- Cost-cutting opportunities
- Proof of value
- Eliminating waste

**When to use:**
- Budget reviews
- Stakeholder presentations to finance
- Justifying spend
- Finding cost savings

**Tone:** Skeptical, no-nonsense, data-driven

---

### 🔬 Critical Thinker
**Persona:** Data scientist who questions every assumption

**Focus:**
- Statistical rigor
- Confounders and biases
- Methodology flaws
- Alternative explanations

**When to use:**
- Internal strategy reviews
- Challenging your own assumptions
- Pre-client presentation (sanity check)
- Academic/technical audiences

**Tone:** Analytical, skeptical, intellectually honest

---

### 🎨 Creative Ad Man
**Persona:** Creative director seeing brand opportunities

**Focus:**
- Bold campaign ideas
- Brand building (not just performance)
- Creative opportunities
- Long-term brand equity

**When to use:**
- Creative briefs
- Brand strategy discussions
- Pitching big ideas
- Breaking out of performance marketing rut

**Tone:** Enthusiastic, visionary, bold

---

## Port Configuration

**Why port 8505?**
- Product 1 (TV Campaign): `8501` (standalone)
- Connected Budget Optimizer (other client): `8504`
- **Electric Glue Hub: `8505`** ← Current app
- Future tools: `8506+`

Each tool has dedicated port to avoid conflicts.

---

## Project Structure

```
electric-glue-hub/
├── app.py                      # Main hub homepage
├── pages/
│   └── 1_Marketing_Intelligence.py  # Product 2 interface
├── agents/
│   ├── __init__.py
│   └── perspective_agents.py   # 3 perspective agents
├── config/
│   ├── __init__.py
│   └── branding.py             # Electric Glue branding (shared with Product 1)
├── requirements.txt
├── .env.example
├── run_hub.py                  # Startup script
└── README.md                   # This file
```

---

## LLM Integration (Optional)

Product 2 can use LLMs for enhanced narrative quality:

**With LLM (OpenAI/Anthropic):**
- More natural language
- Context-aware recommendations
- Tailored to your specific situation

**Without LLM (Rule-Based):**
- Fast, deterministic
- No API costs
- Still provides actionable insights

**Setup:**
1. Add API key to `.env`
2. System auto-detects and uses LLM
3. Falls back to rules if unavailable

---

## Roadmap

### Current (v1.0)
- ✅ Hub homepage with navigation
- ✅ Product 2: Marketing Intelligence (3 perspectives)
- ✅ Rule-based + LLM-powered insights
- ✅ Export to Markdown/Text

### Next (v1.1 - Week 2)
- [ ] Product 3: Report QA Layer integration
- [ ] Enhanced perspective: "Data Scientist" view
- [ ] Comparison mode (see all 3 perspectives side-by-side)
- [ ] Historical reports (save past analyses)

### Future (v2.0 - Month 2)
- [ ] Full Scout integration (Company Research, Competitive Analysis)
- [ ] Custom perspective creation (define your own persona)
- [ ] Multi-campaign comparison
- [ ] API access for programmatic use

---

## Differences from Product 1

| Feature | Product 1 (TV Campaign) | Product 2 (Marketing Intelligence) |
|---------|-------------------------|-----------------------------------|
| **Focus** | Causal impact of TV ads | General marketing insights |
| **Methodology** | Bayesian BSTS | Multi-perspective analysis |
| **Agents** | 5 specialized (Data, Validation, Analysis, Interpretation, Orchestrator) | 3 perspectives (Stingy, Critical, Creative) |
| **Output** | Statistical report with causality | Action-oriented one-pagers |
| **Use Case** | Measure specific campaign ROI | Strategic decision-making |
| **Complexity** | High (MCMC, statistical inference) | Low (quick insights) |
| **Runtime** | 2-5 minutes | <30 seconds |

**Both share:** Electric Glue branding, LLM integration patterns, client-ready outputs

---

## Troubleshooting

### "Module not found: config.branding"

**Solution:** Make sure you're running from project root:
```bash
cd C:\Users\harry\OneDrive\Desktop\EG\electric-glue-hub
python run_hub.py
```

### "Port 8505 already in use"

**Solution:** Kill existing process or use different port:
```bash
# Use different port
streamlit run app.py --server.port=8506

# Or kill process
netstat -ano | findstr :8505
taskkill /PID <PID> /F
```

### Perspectives seem generic

**Solution:**
1. Add more context in "Additional Business Context" section
2. Be specific in "Specific Question or Focus"
3. Add API key for LLM-powered insights (more tailored)

---

## Next Steps

1. ✅ **Test Product 2** - Try with your own campaign data
2. ⏳ **Integrate Product 1** - Add TV Campaign tool as Product 1 page
3. ⏳ **Build Product 3** - Report QA Layer
4. ⏳ **Deploy to Cloud** - Make accessible to Electric Glue team

---

## Support

**For Electric Glue Team:**
- Product questions: Contact project lead
- Technical issues: Check GitHub repo or ask dev team
- Feature requests: Submit via internal roadmap process

**Built by Electric Glue | Where AI Meets Marketing Science**

---

**Version History:**
- v1.0 (Current): Hub + Product 2 (Marketing Intelligence)
- v0.9: Product 1 standalone (TV Campaign Impact Analyzer)
