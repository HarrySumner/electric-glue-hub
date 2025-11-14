"""
Connected Budget Optimiser
Main application landing page with navigation

Front Left Consulting - Marketing Intelligence Solutions
"""

import streamlit as st

st.set_page_config(
    page_title="Connected Budget Optimiser",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #00D9FF 0%, #9D4EDD 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }

    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    .main-header p {
        color: white;
        font-size: 1.2rem;
        margin-top: 0;
    }

    .feature-box {
        background: rgba(0, 217, 255, 0.1);
        border: 2px solid #00D9FF;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.3s;
    }

    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 217, 255, 0.3);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .cta-button {
        background: linear-gradient(90deg, #00D9FF 0%, #9D4EDD 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Connected Budget Optimiser</h1>
    <p>Intelligent Channel Allocation Using Google's 4S Behaviours Framework</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">Powered by Front Left Consulting</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
## Welcome to the Connected Budget Optimiser

This advanced tool helps marketing teams allocate budget across paid and organic channels
using **Google's 4S Behaviours framework** (Streaming, Scrolling, Searching, Shopping)
combined with the **E-Matrix™ methodology** for connected marketing maturity.

### Four Powerful Tools in One Platform:
""")

# Feature boxes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">💰</div>
        <h3>1. Budget Allocation</h3>
        <p>Intelligent channel allocation based on your business context, maturity stage,
        and customer behaviour patterns. Get AI-powered recommendations in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Budget Allocation →", key="btn1", use_container_width=True):
        st.switch_page("pages/1_Budget_Allocation.py")

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">📈</div>
        <h3>2. Attribution & MMM</h3>
        <p>Marketing Mix Modeling with saturation curves, cross-platform synergies,
        adstock effects, and incrementality analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View Attribution Analysis →", key="btn2", use_container_width=True):
        st.switch_page("pages/2_Attribution_MMM.py")

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🔄</div>
        <h3>3. Scenario Modeling</h3>
        <p>Save multiple scenarios, compare side-by-side, and run what-if analyses
        to optimise your marketing investment.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Explore Scenarios →", key="btn3", use_container_width=True):
        st.switch_page("pages/3_Scenario_Modeling.py")

with col4:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">📊</div>
        <h3>4. Causal Impact Analysis</h3>
        <p>Measure the true ROI of your campaigns using Bayesian time series analysis.
        Prove incremental impact with statistical rigor.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Measure Campaign ROI →", key="btn4", use_container_width=True):
        st.switch_page("pages/5_Causal_Impact_Analysis.py")

st.divider()

# How It Works
st.markdown("## 🎯 How It Works")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ### The 4S Behaviours Framework

    Google's research identified four dominant consumer behaviours:

    - **🔍 Searching** - Intent-driven exploration (Google Search, research queries)
    - **📱 Scrolling** - Discovery browsing (Social feeds, exploration)
    - **🛒 Shopping** - Direct transaction behaviour (Shopping ads, marketplaces)
    - **📺 Streaming** - Continuous content consumption (YouTube, CTV, podcasts)

    By understanding how your audience splits across these behaviours, we can optimise
    channel allocation for maximum ROI.
    """)

with col2:
    st.markdown("""
    ### The E-Matrix™ Methodology

    Four stages of digital marketing maturity:

    - **Nascent (0-25%)** - Just starting digital marketing
    - **Emerging (25-50%)** - Basic tracking & coordination
    - **Multi-Moment (50-75%)** - Integrated strategies with attribution
    - **Connected (75-100%)** - Full automation & predictive optimisation

    Your maturity stage determines base allocation strategy, which is then refined
    using business context and behavioural data.
    """)

st.divider()

# Key Features
st.markdown("## ✨ Key Features")

features = [
    ("🎯", "Smart Allocation Engine", "Advanced algorithms considering maturity stage, 4S behaviours, and business context"),
    ("⚖️", "Minimum Threshold Enforcement", "Ensures channels meet minimum viable spend (£5k SEO, £10k paid total)"),
    ("📊", "Saturation Curve Analysis", "Identify diminishing returns and optimise marginal ROAS"),
    ("🔗", "Cross-Platform Synergies", "Model how channels lift each other's performance"),
    ("⏰", "Adstock Modeling", "Account for delayed and sustained impact over 12 weeks"),
    ("🎯", "Incrementality Analysis", "Separate truly incremental results from baseline"),
    ("💾", "Scenario Management", "Save, compare, and analyse multiple budget plans"),
    ("📥", "Export Capabilities", "Download allocations as CSV or JSON for further analysis")
]

col1, col2 = st.columns(2)

for i, (icon, title, description) in enumerate(features):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        **{icon} {title}**
        {description}
        """)

st.divider()

# Business Rules
st.markdown("## 📋 Business Rules & Constraints")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Budget Requirements

    - **Minimum viable budget**: £15,000/month
    - **SEO minimum**: £5,000/month
    - **Paid channels minimum**: £10,000/month total
    - **Individual channel minimums**:
        - Google Search: £1,000
        - Google Shopping: £1,000
        - Meta: £1,000
        - YouTube: £1,500
        - TikTok: £1,000
        - LinkedIn: £1,500
        - Microsoft Ads: £800
    """)

with col2:
    st.markdown("""
    ### Safety Rails

    - No single channel >60% (except Connected stage)
    - SEO ≥20% for established brands (3+ months)
    - Testing reserve: 5% of budget
    - Minimum 3 active channels recommended
    - Channels below minimum are zeroed and redistributed
    """)

st.divider()

# Getting Started
st.markdown("## 🚀 Getting Started")

st.info("""
**Ready to optimise your marketing budget?**

1. Click "Start Budget Allocation" above
2. Input your monthly budget (minimum £15,000)
3. Select your digital maturity stage
4. Answer 6 business context questions
5. Allocate 100 points across 4S behaviours
6. Get instant recommendations!

The entire process takes less than 5 minutes.
""")

# CTA
if st.button("🎯 Start Optimising Now", type="primary", use_container_width=True):
    st.switch_page("pages/1_Budget_Allocation.py")

st.divider()

# About
st.markdown("## 📖 About")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Front Left Consulting

    **Marketing Intelligence Solutions**

    We help businesses make data-driven marketing decisions using advanced analytics,
    marketing mix modeling, and strategic frameworks. Our Connected Budget Optimiser
    brings enterprise-level optimisation capabilities to businesses of all sizes.

    **Framework Credits:**
    - Google's 4S Behaviours (Streaming, Scrolling, Searching, Shopping)
    - E-Matrix™ Connected Marketing Maturity Model
    - Marketing Mix Modeling best practices
    - Econometric attribution principles
    """)

with col2:
    st.info("""
    **Tool Version:** 1.0
    **Last Updated:** 2025
    **Tech Stack:**
    - Python 3.12+
    - Streamlit 1.51.0
    - Plotly 5.24.1
    - NumPy & Pandas

    **Support:**
    Contact Front Left Consulting
    """)

st.divider()
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #00D9FF;'>
    <p><strong>© 2025 Front Left Consulting</strong></p>
    <p>Marketing Intelligence Solutions | Connected Budget Optimiser v1.0</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>
        Powered by Google 4S Behaviours & E-Matrix™ Methodology
    </p>
</div>
""", unsafe_allow_html=True)
