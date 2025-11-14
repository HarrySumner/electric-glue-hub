# Quick Start Guide - Connected Budget Optimiser

## Installation & Setup

### 1. Install Dependencies

```bash
cd connected-budget-optimiser
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

---

## How to Use

### Step 1: Navigate to Budget Allocation

Click **"Start Budget Allocation →"** on the home page

### Step 2: Input Your Budget

Enter your monthly marketing budget (minimum £15,000)

### Step 3: Select Maturity Stage

Choose from:
- **Nascent** - Just starting
- **Emerging** - Basic tracking (recommended for first-time users)
- **Multi-Moment** - Integrated strategies
- **Connected** - Full optimisation

### Step 4: Answer Business Context Questions

Rate 6 questions on a 1-5 scale:
- Customer journey complexity
- Brand maturity
- Purchase consideration cycle
- Competition intensity
- Historical data availability
- Team capability

### Step 5: Set 4S Behaviour Split

Allocate 100 points across:
- 🔍 **Searching** - Google Search, intent-driven
- 📱 **Scrolling** - Social media, discovery
- 🛒 **Shopping** - Product searches, transactions
- 📺 **Streaming** - Video content, YouTube

**Example:** If your audience is search-heavy, allocate 50% to Searching, 30% Scrolling, 15% Shopping, 5% Streaming

### Step 6: Calculate Allocation

Click **"Calculate Allocation"** and review:
- Recommended budget split
- Estimated ROAS per channel
- Allocation rationale
- Warnings & recommendations

### Step 7: Explore Attribution & MMM

Click **"View Attribution Analysis"** to see:
- Saturation curves (optimal spend points)
- Cross-platform synergies
- 12-week revenue forecast
- Incrementality analysis

### Step 8: Save & Compare Scenarios

Navigate to **"Scenario Modeling"** to:
- Save your allocation with a name
- Compare multiple scenarios side-by-side
- Run what-if analysis (e.g., +20% budget)
- Export to CSV or JSON

---

## Quick Example

**Scenario:** Digital agency with £20,000 monthly budget

1. Budget: £20,000
2. Stage: Emerging
3. Context: Moderate scores (3-4 on most questions)
4. 4S Split: 50% Searching, 30% Scrolling, 15% Shopping, 5% Streaming
5. Calculate → Recommended allocation:
   - SEO: £8,000 (40%)
   - Google Search: £6,000 (30%)
   - Google Shopping: £3,000 (15%)
   - Meta: £2,400 (12%)
   - YouTube: £600 (3%)

6. Save as "Q4 Base Plan"
7. Test what-if: +25% budget → See new allocation
8. Export results

---

## Tips for Best Results

✅ **Start with LOW inputs** - Use conservative estimates for your first run

✅ **Review QA logs** - Check the rationale to understand WHY channels were allocated

✅ **Save scenarios** - Create multiple plans for different quarters/budgets

✅ **Check saturation curves** - Ensure channels aren't oversaturated

✅ **Use what-if analysis** - Test budget changes before committing

---

## Common Issues & Solutions

### Issue: "Budget below minimum viable"
**Solution:** Increase budget to at least £15,000 (£5k SEO + £10k paid)

### Issue: "4S behaviours don't sum to 100%"
**Solution:** Adjust sliders so total equals exactly 100%

### Issue: "Channel below minimum threshold"
**Solution:** System will automatically redistribute. Check warnings.

### Issue: Application won't start
**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade streamlit plotly pandas numpy

# Try running again
streamlit run app.py
```

---

## Next Steps

1. **Test with your actual data** - Input real budget and context
2. **Compare multiple scenarios** - Create Q1, Q2, Q3, Q4 plans
3. **Share with team** - Export CSVs for stakeholder review
4. **Iterate monthly** - Re-run with updated performance data

---

## Support

For issues or questions:
- Check [README.md](README.md) for full documentation
- Review your inputs (most issues are from invalid data)
- Contact: [Company Name]

---

**Pro Tip:** Run the tool quarterly with updated performance data to refine your allocation based on actual ROAS.

**© 2025 [Company Name]**
