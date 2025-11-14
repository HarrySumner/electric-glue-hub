# Quick Start Guide
## Get Your First TV Campaign Analysis in 5 Minutes

---

## Step 1: Install (2 minutes)

```bash
cd C:\Users\harry\OneDrive\Desktop\EG\tv-campaign-impact-analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 2: Launch (30 seconds)

```bash
python run_app.py
```

Browser opens automatically at http://localhost:8501

---

## Step 3: Run Sample Analysis (2 minutes)

### In the Sidebar:

1. ✅ **Check "Use sample data"** - This loads 365 days of Nielsen TV campaign data

2. **Review the auto-detected settings:**
   - Date column: `date`
   - Target metric: `bookings`
   - Covariates: `tv_spend`, `digital_spend`, `flights_available`

3. **Campaign periods** (pre-filled):
   - Pre-period: Jan 1 - Jul 18, 2024
   - Post-period: Jul 19 - Dec 31, 2024

4. **Business context** (optional):
   - Campaign: "Nielsen Summer TV Campaign"
   - Budget: £450,000
   - Industry: Travel & Leisure

5. 🚀 **Click "Run Analysis"**

### Watch the Agents Work:

```
📊 STEP 1: DATA INGESTION
✅ Data loaded: 365 rows × 5 columns
🔍 Auto-detected: date, bookings, covariates...

✅ STEP 2: DATA VALIDATION
✅ Validation complete: Score 87/100
⚠️  Potential confounder detected: flights_available

🔬 STEP 3: BAYESIAN CAUSAL ANALYSIS
📊 Auto-selecting BSTS model...
🔧 Fitting Bayesian Structural Time Series model...
✅ Model fitting complete!

💬 STEP 4: INTERPRETATION & INSIGHTS
📝 Executive Summary generated

✅ ANALYSIS COMPLETE!
```

---

## Step 4: Review Results (1 minute)

### Tab 1: Summary

**You'll see:**
- ✅ **Executive Summary**: "The campaign drove 48 incremental bookings per day..."
- 📊 **Key Metrics Cards**:
  - Average Effect: 48 [32, 65]
  - Relative Lift: 18.2%
  - Cumulative Impact: 8,520 bookings
  - Statistical Test: ✅ Significant (p = 0.002)

- 💡 **Key Findings** (5 bullet points)
- 🎯 **Recommendations** (actionable next steps)

### Tab 2: Visualizations

- **Actual vs Counterfactual**: Line chart showing what happened vs what would have happened
- **Point-wise Effects**: Daily causal impact
- **Cumulative Impact**: Running total of incremental bookings

### Tab 3: Diagnostics

- **Model Quality**: Excellent (MAPE: 4.2%)
- **Data Quality**: 87/100
- **Validation Checks**: ✅ All passed
- ⚠️ **Warnings**: "Potential confounder detected: flights_available" (correctly handled!)

### Tab 4: Report

Download:
- 📥 Markdown report (client-ready)
- 📥 HTML report (with Electric Glue branding)
- 📥 CSV data (detailed period-by-period results)

---

## Understanding the Sample Data

The sample data simulates a **Nielsen TV campaign** with these characteristics:

### Timeline:
- **Jan 1 - Jul 18**: Pre-campaign period (200 days)
- **Jul 19 - Dec 31**: Campaign active (165 days)

### True Causal Effect (Ground Truth):
- TV campaign drove **+50 bookings/day** on average
- Total incremental bookings: **~8,500**

### The Confounder (Why DID Fails):
- **Day 180 (June 30)**: Flight availability increased by 30 routes
- This caused +8 bookings/day baseline increase
- Traditional DID would attribute this to TV (wrong!)
- Our BSTS model controls for this via `flights_available` covariate ✅

### Other Factors:
- **Trend**: Gradual baseline growth (100 → 150 bookings/day)
- **Seasonality**: Weekly patterns (weekend dips)
- **Digital spend**: Constant at £5K/day (controlled for)

---

## Next Steps: Use Your Own Data

### Data Requirements:

Your CSV or Excel should have:

1. **Date column** (required)
   - Format: `YYYY-MM-DD`, `DD/MM/YYYY`, or any pandas-parseable format
   - Frequency: Daily or weekly (monthly works but less ideal)

2. **Target metric** (required)
   - E.g., `revenue`, `bookings`, `conversions`, `sales`, `orders`
   - Should be numeric
   - No missing values in critical periods (or they'll be interpolated)

3. **TV spend column** (recommended)
   - Your TV advertising spend per period
   - Helps visualize campaign timing

4. **Covariates** (highly recommended!)
   - Other marketing channels: `digital_spend`, `social_spend`, `search_spend`
   - External factors: `flights_available`, `economic_indicator`, `weather`
   - **Why?** Controls for confounders (the Nielsen problem!)

### Example CSV Format:

```csv
date,revenue,tv_spend,digital_spend,flights_available
2024-01-01,45000,0,5000,120
2024-01-02,47000,0,5200,122
2024-01-03,46500,0,5100,121
...
2024-06-01,65000,15000,5500,135  # TV campaign starts
2024-06-02,68000,14500,5600,136
...
```

### Configuration:

1. **Upload your CSV/Excel** (uncheck "Use sample data")
2. **Select columns** from dropdowns
3. **Define periods**:
   - Pre-period: At least 60 days before campaign (more is better!)
   - Post-period: Campaign duration (minimum 14 days)
4. **Add business context** (optional but improves interpretation)
5. **Run analysis!**

---

## Key Insights from Sample Analysis

### What You'll Learn:

1. **BSTS > DID**: Bayesian method correctly identifies +48 bookings/day effect
   - DID would wrongly estimate +58 bookings/day (confounded by flights)

2. **Uncertainty Quantification**: 95% credible interval [32, 65]
   - We're confident the effect is between 32-65 bookings/day
   - Narrow interval = high confidence

3. **Statistical Significance**: p = 0.002
   - Very strong evidence of causal effect
   - Only 0.2% chance this is random noise

4. **ROI Calculation**: £450K budget / 8,520 bookings = £53 per incremental booking
   - Is this profitable? Depends on booking value!
   - If average booking = £500, ROI = 10x ✅

5. **Confounder Detection**: Validation agent correctly flags `flights_available`
   - Without controlling for this, estimate would be biased
   - BSTS explicitly models this as covariate

---

## Common Questions

### Q: How long should my pre-period be?

**A:** Minimum 60 days, ideally 90-180 days. Longer pre-period = better model fit.

### Q: Can I analyze multiple campaigns at once?

**A:** Not yet—this version analyzes one campaign at a time. For multiple campaigns, run separate analyses or use post-period for each campaign.

### Q: What if I don't have covariates?

**A:** Analysis still works, but results may be less reliable if unobserved confounders exist. Try to include at least digital/other marketing spend.

### Q: My p-value is > 0.05. What does that mean?

**A:** No statistically significant effect detected. Could mean:
- Campaign had minimal impact
- Post-period too short (low statistical power)
- High baseline variability masking effect
- Recommendation: Extend campaign duration and re-analyze

### Q: Can this replace Marketing Mix Modeling (MMM)?

**A:** Different use cases:
- **MMM**: Long-term, multi-channel attribution across 2-3 years
- **BSTS**: Single-campaign, short-term causal impact (weeks to months)
- **Use both**: MMM for strategic planning, BSTS for campaign-specific measurement

---

## Troubleshooting

### "No significant effect detected"

**Check:**
1. Is post-period long enough? (Minimum 14 days recommended)
2. Is pre-period stable? (No major shocks before campaign)
3. Are covariates included? (Confounders reduce power)

### "Low data quality score"

**Check:**
1. Missing values? (Tool interpolates but too many = problem)
2. Outliers? (Review data for data entry errors)
3. Structural breaks? (External shocks in pre-period)

### "Model fit is poor"

**Check:**
1. Unusual seasonality? (Try different seasonal_periods)
2. Non-stationary data? (May need log transformation)
3. Sparse data? (Weekly aggregation might help)

---

## Ready for Production?

Once you've tested with sample data and your own data:

1. **Document your methodology**: Use the generated reports
2. **Share with stakeholders**: HTML report has Electric Glue branding
3. **Set up regular reporting**: Re-run analysis monthly/quarterly
4. **Build a knowledge base**: Track ROI across campaigns
5. **Train your team**: This tool is the first of three in Electric Glue's agentic toolkit!

---

## What's Next?

This is **Tool #1** of Electric Glue's three-tool agentic suite:

1. ✅ **TV Campaign Impact Analyzer** (this tool)
2. ⏳ **Multi-Channel Attribution Engine** (coming soon)
3. ⏳ **Budget Optimizer with Causal Constraints** (coming soon)

All three will share:
- Electric Glue branding
- Agentic architecture
- Production-ready code
- Client-facing reports

**Feedback?** Contact Electric Glue team or file GitHub issue.

---

**🎉 Congratulations! You've completed your first Bayesian causal impact analysis.**

**📺 Built by Electric Glue | Where AI Meets Marketing Science**
