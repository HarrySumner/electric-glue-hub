"""
Electric Glue Hub - Unified Agentic Marketing Platform
Main entry point with navigation to all tools
"""

import streamlit as st
import sys
from pathlib import Path

# Add to path
sys.path.append(str(Path(__file__).parent))

from config.branding import apply_electric_glue_theme, BRAND_COLORS
from config.qa_status import render_qa_traffic_light, render_qa_diagnostics

# Page configuration
st.set_page_config(
    page_title="Homepage | Electric Glue",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply branding
apply_electric_glue_theme()

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 2rem;'>
        <div style='background: linear-gradient(135deg, {BRAND_COLORS['secondary']} 0%, {BRAND_COLORS['primary']} 100%);
                    padding: 1rem; border-radius: 15px;'>
            <h2 style='color: white; margin: 0; font-size: 1.5rem; font-weight: 800;'>⚡ ELECTRIC GLUE</h2>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.85rem;'>
                Marketing Intelligence
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Home
    st.page_link("app.py", label="Home", icon="🏠")

    st.markdown("---")

    # Product 1
    st.page_link("pages/2_Causal_Impact_Analyzer.py", label="AV Campaign Analyser", icon="📺")

    st.markdown("---")

    # Product 2
    st.page_link("pages/4_Marketing_Intelligence.py", label="Scout", icon="🧠")

    st.markdown("---")

    # Product 3
    st.page_link("pages/5_Report_QA_Agent.py", label="Report QA Agent", icon="🚦")

    st.markdown("---")

    # Settings
    st.page_link("pages/6_Settings.py", label="Settings", icon="⚙️")

# Render QA traffic light in sidebar
render_qa_traffic_light(location="sidebar")

# Logo and Header
st.markdown(f"""
<div style='text-align: center; margin-bottom: 3rem; padding: 2rem 0;'>
    <div style='display: inline-block; background: linear-gradient(135deg, {BRAND_COLORS['secondary']} 0%, {BRAND_COLORS['primary']} 100%);
                padding: 1.5rem 3rem; border-radius: 50px; margin-bottom: 1.5rem; box-shadow: 0 8px 24px rgba(0, 255, 0, 0.4);'>
        <h1 style='color: white; font-size: 3rem; margin: 0; font-weight: 800; letter-spacing: 3px;'>
            ⚡ ELECTRIC GLUE
        </h1>
    </div>
    <h2 style='color: {BRAND_COLORS['secondary']}; margin-top: 1.5rem; font-size: 2.2rem; font-weight: 600;'>
        Agentic Marketing Intelligence Platform
    </h2>
    <p style='color: #666; font-size: 1.3rem; margin-top: 1rem; font-weight: 300;'>
        Where AI Meets Marketing Science
    </p>
</div>
""", unsafe_allow_html=True)

# Product cards
st.markdown("## 🚀 Our Products")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(f"""
    <div style='background: white; padding: 2rem; border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.08); min-height: 400px;
                border-top: 6px solid {BRAND_COLORS['primary']}; transition: all 0.3s ease;
                display: flex; flex-direction: column;'>
        <div style='text-align: center;'>
            <div style='font-size: 3.5rem; margin-bottom: 0.5rem;'>📺</div>
            <h3 style='color: {BRAND_COLORS['primary']}; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;'>
                AV Campaign Analyser
            </h3>
        </div>
        <p style='color: #333; font-size: 1rem; line-height: 1.6; text-align: center; margin-bottom: 1.5rem; flex-grow: 1;'>
            Advanced Bayesian MCMC analysis for measuring TV/radio campaign impact with proper statistical validation.
        </p>
        <div style='background: #f8f9fa; padding: 1.2rem; border-radius: 10px; margin-top: 1rem;'>
            <p style='font-size: 0.9rem; color: #333; margin: 0.5rem 0;'><strong style='color: {BRAND_COLORS['primary']};'>🔬 Method:</strong> Bayesian MCMC</p>
            <p style='font-size: 0.9rem; color: #333; margin: 0.5rem 0;'><strong style='color: {BRAND_COLORS['primary']};'>⚡ Type:</strong> Statistical validation</p>
            <p style='font-size: 0.9rem; color: #333; margin: 0.5rem 0;'><strong style='color: {BRAND_COLORS['primary']};'>📊 Use:</strong> Campaign analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem; text-align: center;'>", unsafe_allow_html=True)
    st.page_link("pages/2_Causal_Impact_Analyzer.py", label="Launch AV Campaign Analyser", use_container_width=True, icon="📺")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: white; padding: 2rem; border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.08); min-height: 400px;
                border-top: 6px solid {BRAND_COLORS['accent']}; transition: all 0.3s ease;
                display: flex; flex-direction: column;'>
        <div style='text-align: center;'>
            <div style='font-size: 3.5rem; margin-bottom: 0.5rem;'>🧠</div>
            <h3 style='color: {BRAND_COLORS['accent']}; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;'>
                Scout
            </h3>
        </div>
        <p style='color: #333; font-size: 1rem; line-height: 1.6; text-align: center; margin-bottom: 1.5rem; flex-grow: 1;'>
            Multi-perspective analysis with QA validation. Every output verified to prevent fabrications.
        </p>
        <div style='background: #f8f9fa; padding: 1.2rem; border-radius: 10px; margin-top: 1rem;'>
            <p style='font-size: 0.9rem; color: #333; margin: 0.5rem 0;'><strong style='color: {BRAND_COLORS['accent']};'>😈 Devil's Advocate:</strong> Risk analysis</p>
            <p style='font-size: 0.9rem; color: #333; margin: 0.5rem 0;'><strong style='color: {BRAND_COLORS['accent']};'>🌟 Optimist:</strong> Growth opportunities</p>
            <p style='font-size: 0.9rem; color: #333; margin: 0.5rem 0;'><strong style='color: {BRAND_COLORS['accent']};'>⚖️ Realist:</strong> Practical next steps</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem; text-align: center;'>", unsafe_allow_html=True)
    st.page_link("pages/4_Marketing_Intelligence.py", label="Launch Scout", use_container_width=True, icon="🧠")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background: white; padding: 2rem; border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.08); min-height: 400px;
                border-top: 6px solid #FF6B6B; transition: all 0.3s ease;
                display: flex; flex-direction: column;'>
        <div style='text-align: center;'>
            <div style='font-size: 3.5rem; margin-bottom: 0.5rem;'>🚦</div>
            <h3 style='color: #FF6B6B; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;'>
                Report QA Agent
            </h3>
        </div>
        <p style='color: #333; font-size: 1rem; line-height: 1.6; text-align: center; margin-bottom: 1.5rem; flex-grow: 1;'>
            AI validates AI. Automated quality assurance that flags errors, validates analyses, and provides confidence scores for every output.
        </p>
        <div style='background: #f8f9fa; padding: 1.2rem; border-radius: 10px; margin-top: 1rem;'>
            <p style='font-size: 0.9rem; color: #333; margin: 0.5rem 0;'><strong style='color: #FF6B6B;'>✅ Data Quality:</strong> Checks for errors</p>
            <p style='font-size: 0.9rem; color: #333; margin: 0.5rem 0;'><strong style='color: #FF6B6B;'>📊 Statistical:</strong> Validates claims</p>
            <p style='font-size: 0.9rem; color: #333; margin: 0.5rem 0;'><strong style='color: #FF6B6B;'>🎯 Confidence:</strong> Scoring system</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem; text-align: center;'>", unsafe_allow_html=True)
    st.page_link("pages/5_Report_QA_Agent.py", label="View QA Status", use_container_width=True, icon="🚦")
    st.markdown("</div>", unsafe_allow_html=True)

# QA System Health Diagnostics
st.markdown("---")
st.markdown("## 🚦 QA System Health")
st.markdown("<br>", unsafe_allow_html=True)

qa_diagnostics_html = render_qa_diagnostics()
st.markdown(qa_diagnostics_html, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-top: 2rem; padding: 1.5rem; background: rgba(0,255,0,0.03); border-radius: 10px;'>
    <p style='color: #666; margin: 0; font-size: 0.95rem;'>
        <strong>🛡️ Quality Assurance:</strong> The QA Housekeeping Agent validates all Scout outputs with 75 synthetic tests.
        <br><br>
        <strong>Critical Mission:</strong> If the QA agent fails to catch a fabrication, the project is considered a failure.
        <br>
        This system is the foundation of trust and will be deployed across all future Electric Glue products.
    </p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; margin-top: 3rem;'>
    <p style='font-size: 0.85rem; color: #999; margin: 0.5rem 0;'>
        © 2025 Electric Glue | Proprietary AI-Powered Marketing Intelligence Platform
    </p>
    <p style='font-size: 0.8rem; color: #bbb; margin-top: 1rem;'>
        Powered by Multi-Agent AI × <strong style='color: {BRAND_COLORS['primary']};'>Front Left</strong> Thinking
    </p>
    <p style='font-size: 0.85rem; margin-top: 1.5rem;'>
        <a href='https://forms.gle/mXR2nYbJWZ6WzwPX8' target='_blank' style='color: {BRAND_COLORS['primary']}; text-decoration: none; font-weight: 600;'>
            💬 Share Your Feedback
        </a>
    </p>
</div>
""", unsafe_allow_html=True)
