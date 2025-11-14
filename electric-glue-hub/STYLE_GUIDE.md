# Electric Glue - Style Guide & Design Principles

**Version:** 1.0
**Last Updated:** 2025-01-14
**Created by:** Front Left

---

## 🎨 Brand Identity

### Colour Palette

Electric Glue uses a **black, white, and green** colour scheme inspired by the lightning bolt logo.

```python
BRAND_COLORS = {
    'primary': '#00FF00',           # Electric Glue Bright Green (Lightning)
    'secondary': '#000000',         # Electric Glue Black
    'accent': '#39FF14',            # Electric Glue Neon Green (Accent)
    'dark': '#000000',              # Black background
    'light': '#FFFFFF',             # White background
    'background_light': '#F8F9FA',  # Light background variant
    'success': '#00FF00',           # Success green (matches primary)
    'warning': '#39FF14',           # Warning neon green
    'danger': '#FF0000',            # Error red
    'info': '#00CC00',              # Info dark green
    'text': '#000000',              # Primary text (Black)
    'text_light': '#666666',        # Secondary text (Dark grey)
    'text_secondary': '#666666'     # Alias for text_light
}
```

### Gradients

**Primary Gradient (Black to Green):**
```css
background: linear-gradient(135deg, #000000 0%, #00FF00 100%);
```

**Subtle Background Gradient:**
```css
background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
```

**Ultra-Subtle Background:**
```css
background: linear-gradient(135deg, rgba(0,255,0,0.03) 0%, rgba(0,0,0,0.03) 100%);
```

### Shadows

**Green Glow (for buttons, cards):**
```css
box-shadow: 0 8px 24px rgba(0, 255, 0, 0.4);
```

**Subtle Shadow (for elevation):**
```css
box-shadow: 0 4px 12px rgba(0,0,0,0.08);
```

---

## ✍️ Typography & Language

### Spelling
**ALWAYS use UK English spelling:**
- analyse (not analyze)
- optimise (not optimize)
- visualise (not visualize)
- organise (not organize)
- colour (not color)
- centre (not center)
- metre (not meter)
- realise (not realize)

### Tone of Voice
- **Professional but approachable**
- **Data-driven and precise**
- **Action-oriented** (use active voice)
- **Confident without being arrogant**

### Writing Style
- Short, punchy sentences for impact
- Bullet points for scanability
- Numbers for credibility (e.g., "3 agents", "2.4x ROI")
- **Avoid jargon** - explain technical terms in plain English

---

## 🖼️ UI Component Standards

### Headers

```html
<div style='background: linear-gradient(135deg, #000000 0%, #00FF00 100%);
            padding: 2.5rem; border-radius: 12px; margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 255, 0, 0.3);'>
    <h1 style='color: white; font-size: 2.8rem; font-weight: 700;'>Title</h1>
    <p style='color: rgba(255, 255, 255, 0.95); font-size: 1.2rem;'>Subtitle</p>
</div>
```

### Feature Boxes

```html
<div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
            padding: 2rem; border-radius: 12px; border-left: 5px solid #00FF00;'>
    <h3>Feature Title</h3>
    <p>Feature description...</p>
</div>
```

### Agent Status Indicators

**Running:**
```html
<span style='background: #39FF14; color: #000000; padding: 0.5rem 1rem;
            border-radius: 20px; font-weight: 600;'>🔄 Agent Working...</span>
```

**Complete:**
```html
<span style='background: #00FF00; color: #000000; padding: 0.5rem 1rem;
            border-radius: 20px; font-weight: 600;'>✅ Complete</span>
```

**Waiting:**
```html
<span style='background: #666666; color: white; padding: 0.5rem 1rem;
            border-radius: 20px; font-weight: 600;'>⏸️ Waiting</span>
```

### Buttons

```css
.stButton > button {
    background: linear-gradient(135deg, #000000 0%, #00FF00 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 255, 0, 0.5);
}
```

### Metric Cards

```html
<div style='background: white; padding: 2rem; border-radius: 12px;
            border-top: 4px solid #00FF00; box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
    <h4 style='color: #00FF00;'>Metric Label</h4>
    <p style='font-size: 2rem; font-weight: bold; color: #00FF00;'>Value</p>
    <p style='color: #666; font-size: 0.9rem;'>Description</p>
</div>
```

---

## 📐 Spacing & Layout

### Consistent Spacing
- **Section gaps:** `margin-bottom: 3rem;` (48px)
- **Card padding:** `padding: 2rem;` (32px)
- **Small gaps:** `margin: 1rem 0;` (16px)
- **Micro spacing:** `margin: 0.5rem 0;` (8px)

### Border Radius
- **Cards/Containers:** `border-radius: 12px;`
- **Buttons:** `border-radius: 8px;`
- **Pills/Tags:** `border-radius: 20px;`
- **Large hero elements:** `border-radius: 50px;`

### Column Layouts
- **2 columns:** `st.columns(2, gap="large")`
- **3 columns:** `st.columns(3, gap="large")`
- **4 columns (metrics):** `st.columns(4)`

---

## 🏗️ Page Structure Template

Every page should follow this structure:

```python
"""
[Page Name] - [Short Description]
[Longer description of what this page does]
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from config.branding import apply_electric_glue_theme, BRAND_COLORS, format_header

# Page config
st.set_page_config(
    page_title="[Page Title] | Electric Glue",
    page_icon="[emoji]",
    layout="wide"
)

# Apply branding
apply_electric_glue_theme()

# Header
st.markdown(format_header(
    "[Main Title]",
    "[Subtitle]"
), unsafe_allow_html=True)

# Navigation
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("---")

# [PAGE CONTENT HERE]

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem;
            background: linear-gradient(135deg, rgba(0,255,0,0.03) 0%, rgba(0,0,0,0.03) 100%);
            border-radius: 12px; margin-top: 2rem;'>
    <p style='color: {BRAND_COLORS['text']}; font-size: 1rem; font-weight: 600; margin: 0.5rem 0;'>
        ⚡ <strong>Electric Glue</strong> | [Page Name]
    </p>
    <p style='font-size: 0.85rem; color: #999; margin: 1rem 0 0.5rem 0;'>
        [Tagline or description]
    </p>
    <p style='font-size: 0.8rem; color: #bbb; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e0e0e0;'>
        Powered by Multi-Agent AI × <strong style='color: {BRAND_COLORS['primary']};'>Front Left</strong> Thinking
    </p>
</div>
""", unsafe_allow_html=True)
```

---

## 🎭 Multi-Agent System Principles

### Agent Personas

**1. Stingy Customer (💰)**
- **Focus:** ROI, budget efficiency, cost-cutting
- **Tone:** Skeptical, demanding, numbers-focused
- **Colour:** `#39FF14` (neon green/warning)

**2. Critical Thinker (🔬)**
- **Focus:** Methodology, assumptions, statistical rigor
- **Tone:** Analytical, questioning, evidence-based
- **Colour:** `#00CC00` (dark green/info)

**3. Creative Ad Man (🎨)**
- **Focus:** Brand building, bold ideas, cultural moments
- **Tone:** Enthusiastic, provocative, big-picture
- **Colour:** `#39FF14` (neon green/accent)

### Agent Output Structure

Each agent analysis should include:
1. **Key Insight** (2-3 sentences)
2. **Top 3-4 Actions** (specific, actionable)
3. **Warning/Caveat** (what to watch out for)
4. **Strategic Opportunity** (quick win or big idea)

---

## 📊 Data Visualisation Standards

### Sentiment Analysis
Display as horizontal progress bars:
- **Positive:** Green (`#00FF00`)
- **Neutral:** Grey (`#666666`)
- **Negative:** Red (`#FF0000`)

### Progress Tracking
Use Streamlit's `st.progress()` with:
- Percentage-based updates
- Clear phase descriptions
- Time estimates displayed upfront

### Word Clouds / Topic Visualisation
Size indicates frequency:
```html
<span style='font-size: 2rem; color: #00FF00;'>high frequency</span>
<span style='font-size: 1.2rem; color: #666;'>low frequency</span>
```

---

## 🔒 Code Quality Standards

### Python Style
- Follow PEP 8
- Use descriptive variable names
- Add docstrings to all functions
- Type hints where appropriate

### Streamlit Best Practices
- Use `st.session_state` for persistence
- Avoid redundant `st.write()` calls
- Use `unsafe_allow_html=True` for custom styling
- Always include `st.markdown("---")` for section breaks

### File Organisation
```
electric-glue-hub/
├── app.py                    # Homepage
├── config/
│   └── branding.py          # Colours, CSS, utilities
├── agents/
│   └── perspective_agents.py # AI agent logic
├── pages/
│   ├── 1_Product_1_Overview.py
│   ├── 2_Causal_Impact_Analyser.py
│   ├── 3_Product_2_Overview.py
│   ├── 4_Marketing_Intelligence.py
│   ├── 5_Product_3_Overview.py
│   └── 6_Settings.py
├── .env                     # API keys (never commit!)
└── STYLE_GUIDE.md          # This file
```

---

## 🚀 Development Workflow

### Before Committing
1. ✅ Check all UK spellings (analyse, optimise, visualise)
2. ✅ Verify brand colours (no orange/blue from old design)
3. ✅ Test all navigation links
4. ✅ Ensure Front Left attribution in footers
5. ✅ Run quick manual QA of key user flows

### Git Commit Message Format
```
[Component] Brief description

- Detailed change 1
- Detailed change 2

Created by Front Left
```

---

## 📞 Support & Maintenance

**Created by:** Front Left
**Platform:** Streamlit
**Python Version:** 3.9+
**Key Dependencies:** streamlit, pandas, python-dotenv

### Future Maintainers
- All brand colours defined in `config/branding.py`
- Reusable components available via `format_header()`, etc.
- Agent logic centralised in `agents/perspective_agents.py`
- UK spelling is **mandatory** - check before deploying

---

**⚡ Electric Glue** | Where AI Meets Marketing Science
*Created by Front Left*
