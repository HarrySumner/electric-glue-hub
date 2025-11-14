# UI Restructure Summary - Questions-First Approach

## What Changed

### ✅ **STEP 1: Prescreening Questions (NEW - TOP OF PAGE)**

**7 Smart Questions** in mixed format (binary + scored):

1. **Is this a new brand?** (Binary: Yes/No)
2. **Market competition level?** (Select slider: Low → Hyper-competitive)
3. **Purchase timeframe?** (Select slider: Impulse → Extended)
4. **Team experience?** (Scored 1-5 with labels: Beginner → Expert)
5. **Have 6+ months of data?** (Binary: Yes/No)
6. **Customer journey complexity?** (Scored 1-5: Simple → Very Complex)
7. **Industry vertical?** (Optional dropdown for better 4S suggestions)

### ✅ **STEP 2: Auto-Suggestions with Confidence Score**

**Three auto-calculated metrics:**

1. **Confidence Score (0-100%)**
   - Shows how confident the system is in recommendations
   - Based on completeness of answers
   - 🟢 80%+ = High confidence
   - 🟡 60-79% = Moderate confidence
   - 🟠 <60% = Low confidence

2. **Suggested Maturity Stage**
   - Auto-calculated from prescreening answers
   - Shows reasoning ("Why this stage?")
   - User can override if needed

3. **Suggested 4S Split**
   - Industry-specific defaults when vertical specified
   - Adjusted for purchase timeframe
   - User can adjust with sliders

### ✅ **STEP 3: Budget Input (with action buttons)**

- Budget input field
- **🔄 Reset All** button - Clears everything
- **✨ Use Suggestions** button - Applies all auto-suggestions
- Budget status with metrics
- Maturity stage selector (shows if matches suggestion)

### ✅ **STEP 4: 4S Behaviour Split (pre-filled)**

- Sliders pre-filled with suggested values
- Shows dominant behaviour
- Validation (must sum to 100%)
- Visual chart

### ✅ **Calculate & Results (same as before)**

---

## Key Improvements

### 1. **Questions Drive Everything**
- Prescreening questions are FIRST (top of page)
- They immediately inform all downstream suggestions
- Users see WHY recommendations are made

### 2. **Confidence Scoring**
- Transparent "how sure are we?" metric
- Encourages complete answers
- Builds trust in recommendations

### 3. **Auto-Suggestions**
- Saves time for users
- Shows intelligent reasoning
- Can be overridden (not forced)

### 4. **Industry Intelligence**
- Optional industry selector
- Pre-built 4S splits for common verticals:
  - E-commerce: High Shopping (40%)
  - SaaS: High Searching (45%)
  - Professional Services: High Searching (50%)
  - etc.

---

## How Auto-Suggestion Works

### Maturity Stage Calculation

```
Score = 0

IF new_brand == "No": +2 points
IF team_experience (1-5): +team_experience points
IF has_data == "Yes": +2 points
IF journey_complexity (1-5): +journey_complexity points

Total: 0-14 points

0-4 points   → Nascent
5-8 points   → Emerging (most common)
9-11 points  → Multi-Moment
12-14 points → Connected
```

### 4S Split Calculation

```
1. Load industry defaults (if specified)
   E.g., E-commerce = {Searching: 30%, Scrolling: 25%, Shopping: 40%, Streaming: 5%}

2. Adjust for purchase timeframe
   IF "Extended" → Searching +10%, Shopping -10%
   IF "Impulse" → Shopping +10%, Searching -10%

3. Normalize to 100%
```

### Confidence Score Calculation

```
Start: 100%

Deduct for missing answers:
- No brand age? -20%
- No competition? -15%
- No purchase time? -15%
- No team exp? -20%
- No data answer? -10%

Bonus:
- Industry specified? +10%

Result: 0-100%
```

---

## Mapping to Business Context

Prescreening answers automatically populate `business_context`:

```python
# Binary "new brand?" → brand_maturity score
"Yes" → brand_maturity = 1
"No"  → brand_maturity = 4

# Competition slider → competition_intensity score
"Low" → 1
"Moderate" → 3
"High" → 4
"Hyper-competitive" → 5

# Purchase timeframe → purchase_consideration score
"Impulse (<24h)" → 1
"Quick (1-7 days)" → 2
"Considered (1-4 weeks)" → 3
"Extended (1-6 months)" → 5

# Team slider (1-5) → team_capability directly

# Has data binary → historical_data_months
"Yes" → 4
"No" → 1

# Journey slider (1-5) → journey_complexity directly
```

---

## User Flow Comparison

### OLD FLOW (questions buried):
```
1. Budget → 2. Maturity → 3. Questions → 4. 4S Split → 5. Calculate
```

### NEW FLOW (questions first):
```
1. Prescreening Questions (7 quick ones)
2. See Auto-Suggestions + Confidence Score
3. Confirm/Adjust Budget & Maturity
4. Confirm/Adjust 4S Split
5. Calculate
```

---

## Testing the New Flow

### Correct Path:
```bash
cd "c:\Users\[user]\OneDrive\Desktop\[Client]\connected-budget-optimiser"
streamlit run app.py
```

### Test Scenario:
1. **Answer prescreening:**
   - New brand? **Yes**
   - Competition: **High**
   - Purchase: **Extended (1-6 months)**
   - Team experience: **3 (Intermediate)**
   - Has data: **No**
   - Journey: **4 (Complex)**
   - Industry: **SaaS/Software**

2. **Expected auto-suggestions:**
   - Maturity: **Emerging** (score: 6/14)
   - Confidence: **80%** (all questions answered + industry)
   - 4S Split: **Searching 45%, Scrolling 30%, Shopping 10%, Streaming 15%**
   - Reasoning: "New brand, high competition, long cycle"

3. **Click "Use Suggestions"** → Everything auto-fills

4. **Input budget: £20,000**

5. **Calculate** → See allocation weighted for:
   - New brand (+20% paid channels)
   - High competition (+15% paid defense)
   - Long cycle (+15% SEO)
   - SaaS industry (Search/Content heavy)

---

## Files Changed

### New:
- `pages/1_Budget_Allocation_v2.py` (renamed to `1_Budget_Allocation.py`)

### Backed Up:
- `pages/1_Budget_Allocation_OLD.py` (original version)

### Unchanged:
- `pages/2_Attribution_MMM.py` ✅
- `pages/3_Scenario_Modeling.py` ✅
- All `utils/*.py` ✅
- All `data/*.json` ✅

---

## Next Steps

1. **Test the new flow** - Run streamlit and verify prescreening works
2. **Refine confidence scoring** - Adjust weights if needed
3. **Add more industries** - Expand industry-specific 4S defaults
4. **Implement auto-optimise** - Make "✨ Auto-Optimise" button functional

---

**Result:** Questions now drive the entire experience, with transparent auto-suggestions and confidence scoring!

© 2025 [Company Name]
