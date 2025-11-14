# Connected Budget Optimiser

**Intelligent Channel Allocation Using Google's 4S Behaviours Framework**

Powered by [Company Name] - Marketing Intelligence Solutions

---

## Overview

The Connected Budget Optimiser is a sophisticated Streamlit web application that helps marketing teams allocate budget across paid and organic channels using:

- **Google's 4S Behaviours Framework** (Streaming, Scrolling, Searching, Shopping)
- **E-Matrix™ Methodology** for digital marketing maturity
- **Marketing Mix Modeling (MMM)** with saturation curves and adstock
- **Cross-platform synergy analysis**
- **Scenario planning and comparison**

---

## Features

### 🎯 Budget Allocation Calculator
- Intelligent allocation based on maturity stage, business context, and 4S behaviours
- Minimum threshold enforcement (£5k SEO, £10k paid total)
- Real-time validation and warnings
- Interactive visualizations

### 📈 Attribution & MMM Analysis
- Saturation curve modeling for each channel
- Cross-platform lift factor analysis
- 12-week revenue forecast with adstock carryover
- Incrementality analysis (true incremental vs baseline)
- Channel-specific performance metrics

### 💾 Scenario Modeling & Comparison
- Save multiple budget scenarios
- Side-by-side comparison of up to 3 scenarios
- What-if analysis with budget adjustments
- Export capabilities (CSV, JSON)

---

## Installation

### Requirements
- Python 3.12 or higher
- pip package manager

### Setup

1. **Clone or download the project**
```bash
cd connected-budget-optimiser
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Access in browser**
The app will open automatically at `http://localhost:8501`

---

## Usage Guide

### Quick Start

1. **Open the application** and click "Start Budget Allocation"

2. **Input your budget** (minimum £15,000/month)

3. **Select digital maturity stage**:
   - Nascent (0-25%)
   - Emerging (25-50%)
   - Multi-Moment (50-75%)
   - Connected (75-100%)

4. **Answer 6 business context questions** (1-5 scale):
   - Customer journey complexity
   - Brand maturity
   - Purchase consideration cycle
   - Competition intensity
   - Historical data availability
   - Team capability

5. **Allocate 100 points across 4S behaviours**:
   - 🔍 Searching (Intent-driven)
   - 📱 Scrolling (Discovery)
   - 🛒 Shopping (Transactional)
   - 📺 Streaming (Content consumption)

6. **Calculate allocation** and review recommendations

7. **Navigate to Attribution & MMM** to analyse performance projections

8. **Save scenarios** for comparison and what-if analysis

---

## Business Rules

### Minimum Budget Requirements

- **Total minimum**: £15,000/month
- **SEO minimum**: £5,000/month
- **Paid channels minimum**: £10,000/month total

### Individual Channel Minimums

| Channel | Minimum Spend |
|---------|---------------|
| SEO | £5,000 |
| Google Search | £1,000 |
| Google Shopping | £1,000 |
| Meta (Facebook/Instagram) | £1,000 |
| YouTube | £1,500 |
| TikTok | £1,000 |
| LinkedIn | £1,500 |
| Microsoft Ads | £800 |

### Safety Rails

- No single channel >60% (except Connected stage)
- SEO ≥20% for established brands
- Minimum 3 active channels recommended
- 5% testing reserve

---

## Project Structure

```
connected-budget-optimiser/
├── app.py                          # Main landing page
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
├── pages/
│   ├── 1_Budget_Allocation.py     # Page 1: Budget allocation
│   ├── 2_Attribution_MMM.py       # Page 2: Attribution analysis
│   └── 3_Scenario_Modeling.py     # Page 3: Scenario comparison
├── utils/
│   ├── allocation_engine.py       # Core allocation logic
│   ├── mmm_calculations.py        # MMM & forecasting
│   ├── validation.py              # Validation rules
│   └── visualizations.py          # Plotly charts
├── data/
│   ├── platform_data.json         # Platform performance data
│   └── base_allocations.json      # Maturity stage templates
└── .streamlit/
    └── config.toml                # Streamlit configuration
```

---

## Technical Details

### Tech Stack

- **Python**: 3.12+
- **Streamlit**: 1.51.0 (web framework)
- **Plotly**: 5.24.1 (interactive charts)
- **Pandas**: 2.2.3 (data manipulation)
- **NumPy**: 2.1.3 (numerical calculations)

### Algorithms

- **Hill Equation** for saturation curves
- **Damerau-Levenshtein** principles for similarity
- **Adstock modeling** with exponential decay
- **Cross-platform lift** multiplicative effects
- **Union-find** for efficient clustering

### Data Models

- **Platform Data**: ROAS, saturation points, adstock rates, cross-platform lift
- **Base Allocations**: Templates by maturity stage
- **Session State**: User inputs and calculated scenarios
- **Scenarios**: Saved budget allocations with metadata

---

## Deployment

### Local Development

```bash
streamlit run app.py
```

### Streamlit Cloud

1. Push to GitHub repository
2. Connect Streamlit Cloud to repo
3. Set Python version: 3.12
4. Deploy from main branch
5. App URL: `https://yourapp.streamlit.app`

### Docker (Optional)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## Future Enhancements (v2)

- [ ] API integration (Google Ads, Meta Ads, GA4)
- [ ] Machine learning predictions
- [ ] Multi-currency support
- [ ] Team collaboration features
- [ ] Custom platform addition
- [ ] Seasonality adjustments
- [ ] Competitive benchmarking
- [ ] PDF report generation

---

## Support

For questions, issues, or feature requests, contact:

**[Company Name]**
Marketing Intelligence Solutions

---

## Credits

### Frameworks
- Google 4S Behaviours (Streaming, Scrolling, Searching, Shopping)
- E-Matrix™ Connected Marketing Maturity Model

### Methodologies
- Marketing Mix Modeling best practices
- Econometric attribution principles
- Adstock and saturation curve modeling

---

## License

© 2025 [Company Name]. All rights reserved.

This tool is provided for internal use and client engagements.

---

## Version History

**v1.0** (2025)
- Initial release
- 3-page application
- Core allocation engine
- MMM analysis
- Scenario modeling
- Export capabilities

---

*Built with ❤️ by [Company Name]*
