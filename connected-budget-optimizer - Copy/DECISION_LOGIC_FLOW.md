# Decision Logic Flow - How Questions Inform Weighting

## Complete Trace: From Questions → Final Allocation

---

## STEP 1: Questions Are Asked (Page 1, Lines 145-203)

### Location: `pages/1_Budget_Allocation.py`

```python
# STEP 3: Business Context Questions
context_questions = [
    {
        'key': 'journey_complexity',
        'label': 'Customer journey complexity',
        'help': '1 = Linear/Simple → 5 = Multi-touch/Complex'
    },
    {
        'key': 'brand_maturity',
        'label': 'Brand maturity',
        'help': '1 = New Launch → 5 = Established (3+ years)'
    },
    {
        'key': 'purchase_consideration',
        'label': 'Purchase consideration cycle length',
        'help': '1 = Impulse (<24h) → 5 = Extended (6+ months)'
    },
    {
        'key': 'competition_intensity',
        'label': 'Market competition intensity',
        'help': '1 = Low Competition → 5 = Hyper-Competitive'
    },
    {
        'key': 'historical_data_months',
        'label': 'Months of reliable performance data',
        'help': '1 = None (0-2) → 5 = Extensive (12+)'
    },
    {
        'key': 'team_capability',
        'label': 'Team digital marketing maturity',
        'help': '1 = Beginner → 5 = Advanced'
    }
]
```

**UI:** Users answer with sliders (1-5 scale)
**Storage:** Answers stored in `st.session_state.business_context`

---

## STEP 2: Allocation Calculation is Triggered

### Location: `pages/1_Budget_Allocation.py:358-378`

```python
if st.button("Calculate Allocation"):
    result = calculate_allocation(
        total_budget=st.session_state.total_budget,
        maturity_stage=st.session_state.maturity_stage,
        business_context=st.session_state.business_context,  # <-- Questions passed here
        four_s_split=st.session_state.four_s_split,
        historical_data=historical_data
    )
```

---

## STEP 3: Base Allocation Loaded

### Location: `utils/allocation_engine.py:237-245`

```python
# Load base allocation template based on maturity stage
base_allocations = load_base_allocations()
base_allocation = base_allocations[maturity_stage].copy()

# Example for "Emerging" stage:
# {
#   'SEO': 0.40,           # 40%
#   'Google Search': 0.25,  # 25%
#   'Google Shopping': 0.15,# 15%
#   'Meta': 0.12,          # 12%
#   'YouTube': 0.05,       # 5%
#   'Testing_Budget': 0.03 # 3%
# }
```

**Source:** `data/base_allocations.json`

---

## STEP 4: 4S Behaviour Modifiers Applied

### Location: `utils/allocation_engine.py:254-256`

```python
# Step 1: Apply 4S behaviour modifiers
allocation_pct = apply_4s_modifiers(base_allocation, four_s_split, total_budget)
```

### How 4S Modifiers Work:

```python
# If Searching > 50%:
modifiers['SEO'] = 1.20                    # +20%
modifiers['Google Search'] = 1.25          # +25%
modifiers['Microsoft Ads'] = 1.20          # +20%
modifiers['Meta'] = 0.85                   # -15%
modifiers['YouTube'] = 0.90                # -10%

# If Scrolling > 40%:
modifiers['Meta'] = 1.30                   # +30%
modifiers['TikTok'] = 1.40                 # +40%
modifiers['LinkedIn'] = 1.25               # +25%
modifiers['SEO'] = 0.85                    # -15%
modifiers['Google Search'] = 0.85          # -15%

# If Shopping > 50%:
modifiers['Google Shopping'] = 1.40        # +40%
modifiers['Meta'] = 1.20                   # +20%
modifiers['SEO'] = 0.90                    # -10%

# If Streaming > 40%:
modifiers['YouTube'] = 1.50                # +50%
modifiers['Meta'] = 1.10                   # +10%
modifiers['Google Search'] = 0.85          # -15%
```

---

## STEP 5: Business Context Adjustments Applied ⭐ **THIS IS WHERE YOUR QUESTIONS MATTER**

### Location: `utils/allocation_engine.py:258-260`

```python
# Step 2: Apply business context adjustments
allocation_pct, context_reasons = apply_business_context(
    allocation_pct, business_context, total_budget
)
```

### The `apply_business_context()` Function (Lines 108-166)

**THIS IS THE CORE WEIGHTING LOGIC:**

```python
def apply_business_context(allocation, context_scores, total_budget):
    adjustments = {}
    applied_reasons = []

    # 1. PURCHASE CONSIDERATION CYCLE
    if context_scores['purchase_consideration'] >= 4:
        # Long cycle = favor SEO (compounds over time)
        adjustments['SEO'] = 1.15                    # SEO +15%
        adjustments['Google Search'] = 0.95          # Paid Search -5%
        applied_reasons.append("Long consideration cycle (+15% to SEO for compounding)")

    # 2. BRAND MATURITY
    if context_scores['brand_maturity'] <= 2:
        # NEW BRAND = need paid for speed
        adjustments['Google Search'] = 1.20          # Paid Search +20%
        adjustments['Meta'] = 1.15                   # Meta +15%
        adjustments['SEO'] = 0.85                    # SEO -15%
        applied_reasons.append("New brand (+20% paid channels for quick wins)")

    elif context_scores['brand_maturity'] >= 4:
        # ESTABLISHED BRAND = leverage authority
        adjustments['SEO'] = 1.15                    # SEO +15%
        adjustments['Google Search'] = 0.95          # Paid Search -5%
        applied_reasons.append("Established brand (+15% to SEO to leverage authority)")

    # 3. COMPETITION INTENSITY
    if context_scores['competition_intensity'] >= 4:
        # HIGH COMPETITION = paid defense
        adjustments['Google Search'] = 1.20          # Paid Search +20%
        adjustments['Meta'] = 1.10                   # Meta +10%
        applied_reasons.append("High competition (+15% to paid defense)")

    # 4. TEAM CAPABILITY
    if context_scores['team_capability'] <= 2:
        # LOW CAPABILITY = keep it simple (focus on Google/Meta only)
        applied_reasons.append("Limited team capability (recommending focus on core channels)")

    # Apply all adjustments
    adjusted = {}
    for channel, pct in allocation.items():
        adjustment = adjustments.get(channel, 1.0)  # Default 1.0 = no change
        adjusted[channel] = pct * adjustment

    # Normalize to 100%
    total = sum(adjusted.values())
    final = {ch: (pct / total) for ch, pct in adjusted.items()}

    return final, applied_reasons
```

---

## STEP 6: Historical Performance Weighting (Optional)

### Location: `utils/allocation_engine.py:262-266`

```python
# Step 3: Apply historical performance weighting (if available)
if historical_data and business_context.get('historical_data_months', 0) >= 3:
    allocation_pct = apply_historical_weighting(
        allocation_pct, historical_data, total_budget
    )
```

**Only applies if:**
- User has historical data uploaded
- AND `historical_data_months` score >= 3

**How it works:**
- Calculates actual ROAS for each channel
- Weights allocation by relative performance
- Caps adjustments at ±30% to prevent over-reliance

---

## STEP 7: Minimum Thresholds Enforced

### Location: `utils/allocation_engine.py:274-276`

```python
# Step 5: Enforce minimum thresholds
allocation_amounts, zeroed_channels = enforce_minimum_thresholds(
    allocation_amounts, total_budget
)
```

**Removes channels that can't meet minimums:**
- SEO: £5,000
- Google Search: £1,000
- Shopping: £1,000
- Meta: £1,000
- YouTube: £1,500
- etc.

---

## STEP 8: Safety Rails Applied

### Location: `utils/allocation_engine.py:278-280`

```python
# Step 6: Apply safety rails
allocation_amounts, safety_warnings = apply_safety_rails(
    allocation_amounts, maturity_stage, brand_age_months
)
```

**Constraints:**
- No single channel >60% (unless Connected stage)
- SEO ≥20% for established brands
- Minimum 3 active channels

---

## STEP 9: Rationale Generated

### Location: `utils/allocation_engine.py:283-304`

```python
# Build rationale showing what happened
rationale = []
rationale.append(f"✅ {maturity_stage} stage base allocation")

dominant_behaviour = max(four_s_split, key=four_s_split.get)
rationale.append(f"✅ {dominant_behaviour.upper()} behaviour upweight ({four_s_split[dominant_behaviour]}%)")

# Add context reasons from Step 5
rationale.extend([f"✅ {reason}" for reason in context_reasons])

# Add warnings
if zeroed_channels:
    for ch in zeroed_channels:
        rationale.append(f"⚠️ {ch} below minimum threshold - redistributed")

rationale.extend([f"⚠️ {warning}" for warning in safety_warnings])

return {
    'allocation_amounts': allocation_amounts,
    'allocation_percentages': allocation_pct_final,
    'total_allocated': total_allocated,
    'rationale': rationale,              # <-- Shown to user
    'zeroed_channels': zeroed_channels,
    'warnings': safety_warnings,
    'dominant_behaviour': dominant_behaviour
}
```

---

## VISUAL FLOW DIAGRAM

```
USER INPUTS
├─ Budget: £20,000
├─ Maturity: Emerging
├─ Business Context:
│  ├─ journey_complexity: 3
│  ├─ brand_maturity: 2 (NEW BRAND) ⭐
│  ├─ purchase_consideration: 4 (LONG CYCLE) ⭐
│  ├─ competition_intensity: 5 (HIGH) ⭐
│  ├─ historical_data_months: 2
│  └─ team_capability: 3
└─ 4S Split: Searching 50%, Scrolling 30%, Shopping 15%, Streaming 5%

                    ↓

STEP 1: Base Allocation (Emerging)
├─ SEO: 40%
├─ Google Search: 25%
├─ Google Shopping: 15%
├─ Meta: 12%
├─ YouTube: 5%
└─ Testing: 3%

                    ↓

STEP 2: Apply 4S Modifiers (Searching 50% dominant)
├─ SEO: 40% × 1.20 = 48%
├─ Google Search: 25% × 1.25 = 31.25%
├─ Google Shopping: 15% × 1.0 = 15%
├─ Meta: 12% × 0.85 = 10.2%
├─ YouTube: 5% × 0.90 = 4.5%
└─ Testing: 3% × 1.0 = 3%

                    ↓

STEP 3: Apply Business Context Adjustments ⭐⭐⭐
├─ brand_maturity = 2 (New Brand):
│  ├─ Google Search: 31.25% × 1.20 = 37.5% ✅
│  ├─ Meta: 10.2% × 1.15 = 11.73% ✅
│  └─ SEO: 48% × 0.85 = 40.8% ✅
│
├─ purchase_consideration = 4 (Long Cycle):
│  ├─ SEO: 40.8% × 1.15 = 46.92% ✅
│  └─ Google Search: 37.5% × 0.95 = 35.625% ✅
│
└─ competition_intensity = 5 (High):
   ├─ Google Search: 35.625% × 1.20 = 42.75% ✅
   └─ Meta: 11.73% × 1.10 = 12.9% ✅

                    ↓

STEP 4: Normalize to 100%
├─ SEO: 30.5%
├─ Google Search: 35.2%
├─ Google Shopping: 12.3%
├─ Meta: 10.6%
├─ YouTube: 3.7%
└─ Testing: 2.5%

                    ↓

STEP 5: Convert to £ Amounts
├─ SEO: £6,100
├─ Google Search: £7,040
├─ Google Shopping: £2,460
├─ Meta: £2,120
├─ YouTube: £740 (❌ Below £1,500 minimum)
└─ Testing: £500

                    ↓

STEP 6: Enforce Minimums (Zero YouTube, Redistribute)
├─ SEO: £6,350
├─ Google Search: £7,330
├─ Google Shopping: £2,560
├─ Meta: £2,210
├─ YouTube: £0 (Zeroed)
└─ Testing: £550

                    ↓

FINAL ALLOCATION
Total: £19,000 allocated
```

---

## WHERE TO TEST THE FLOW

### Correct Path:
```bash
cd "c:\Users\[user]\OneDrive\Desktop\[Client]\connected-budget-optimiser"
streamlit run app.py
```

### Test Scenario to See All Weightings:
1. **Budget:** £20,000
2. **Stage:** Emerging
3. **Business Context:**
   - Journey complexity: 3
   - Brand maturity: **2** (triggers "New Brand" logic)
   - Purchase consideration: **4** (triggers "Long Cycle" logic)
   - Competition: **5** (triggers "High Competition" logic)
   - Historical data: 2
   - Team: 3
4. **4S Split:** Searching 50%, Scrolling 30%, Shopping 15%, Streaming 5%

**Expected Result:**
- SEO reduced (new brand needs speed)
- Google Search boosted (new brand + high competition + searching dominant)
- Meta boosted (new brand needs awareness)
- Long cycle partially counters the new brand reduction to SEO

---

## Summary

**Q:** Where are prescreening questions asked?
**A:** `pages/1_Budget_Allocation.py` lines 145-203 (STEP 3: Business Context)

**Q:** Where do they inform the weighting?
**A:** `utils/allocation_engine.py:108-166` in the `apply_business_context()` function

**The questions directly modify channel percentages via multiplication factors (0.85x to 1.20x range)**

---

© 2025 [Company Name]
