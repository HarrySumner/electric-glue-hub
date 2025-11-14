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

# Page configuration
st.set_page_config(
    page_title="Electric Glue | Agentic Marketing Intelligence Platform",
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
    st.page_link("app.py", label="🏠 Home")

    st.markdown("---")

    # Product 1
    st.page_link("pages/2_Causal_Impact_Analyzer.py", label="🎯 Causal Impact")

    st.markdown("---")

    # Product 2
    st.page_link("pages/4_Marketing_Intelligence.py", label="🧠 Scout")

    st.markdown("---")

    # Product 3
    st.markdown("<p style='color: #999; font-size: 0.95rem;'>🛡️ TrustCheck</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #999; font-size: 0.75rem; margin-left: 1.5rem; margin-top: -0.5rem;'>⏳ Coming Soon</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Settings
    st.page_link("pages/6_Settings.py", label="⚙️ Settings")

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
    <div style='background: white; padding: 2.5rem; border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.08); height: 520px;
                border-top: 6px solid {BRAND_COLORS['primary']}; transition: all 0.3s ease;'>
        <div style='text-align: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🎯</div>
            <h2 style='color: {BRAND_COLORS['secondary']}; font-size: 1.3rem; margin-bottom: 0.5rem;'>Product 1</h2>
            <h3 style='color: {BRAND_COLORS['primary']}; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem;'>
                Causal Impact Analyser
            </h3>
        </div>
        <p style='color: #555; font-size: 1rem; line-height: 1.6; text-align: center; margin-bottom: 2rem;'>
            Measure the <strong>true causal impact</strong> of your campaigns using Bayesian structural time series.
            Go beyond correlation to understand what actually drives results.
        </p>
        <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-top: auto;'>
            <p style='font-size: 0.95rem; color: #666; margin: 0.5rem 0;'><strong>🔬 Methodology:</strong> Bayesian BSTS</p>
            <p style='font-size: 0.95rem; color: #666; margin: 0.5rem 0;'><strong>🤖 Agents:</strong> 5 specialized AI agents</p>
            <p style='font-size: 0.95rem; color: #666; margin: 0.5rem 0;'><strong>📊 Use Case:</strong> TV, Radio, OOH campaigns</p>
            <p style='font-size: 0.95rem; color: #666; margin: 0.5rem 0;'><strong>⚡ Output:</strong> Client-ready reports</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem; text-align: center;'>", unsafe_allow_html=True)
    st.page_link("pages/2_Causal_Impact_Analyzer.py", label="🚀 Launch Tool", use_container_width=True, icon="🎯")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: white; padding: 2.5rem; border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.08); height: 520px;
                border-top: 6px solid {BRAND_COLORS['accent']}; transition: all 0.3s ease;'>
        <div style='text-align: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🧠</div>
            <h2 style='color: {BRAND_COLORS['secondary']}; font-size: 1.3rem; margin-bottom: 0.5rem;'>Product 2</h2>
            <h3 style='color: {BRAND_COLORS['accent']}; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem;'>
                Scout
            </h3>
        </div>
        <p style='color: #555; font-size: 1rem; line-height: 1.6; text-align: center; margin-bottom: 2rem;'>
            Get <strong>multi-perspective analysis</strong> of your marketing data. See your campaigns through
            the eyes of a CFO, data scientist, and creative director—all at once.
        </p>
        <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-top: auto;'>
            <p style='font-size: 0.95rem; color: #666; margin: 0.5rem 0;'><strong>💰 Perspective:</strong> Stingy Customer (ROI)</p>
            <p style='font-size: 0.95rem; color: #666; margin: 0.5rem 0;'><strong>🔬 Perspective:</strong> Critical Thinker (Rigor)</p>
            <p style='font-size: 0.95rem; color: #666; margin: 0.5rem 0;'><strong>🎨 Perspective:</strong> Creative Ad Man (Brand)</p>
            <p style='font-size: 0.95rem; color: #666; margin: 0.5rem 0;'><strong>⚡ Output:</strong> Actionable one-pagers</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem; text-align: center;'>", unsafe_allow_html=True)
    st.page_link("pages/4_Marketing_Intelligence.py", label="🚀 Launch Tool", use_container_width=True, icon="🧠")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background: white; padding: 2.5rem; border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.08); height: 520px;
                border-top: 6px solid {BRAND_COLORS['info']}; transition: all 0.3s ease; opacity: 0.7;'>
        <div style='text-align: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🛡️</div>
            <h2 style='color: {BRAND_COLORS['secondary']}; font-size: 1.3rem; margin-bottom: 0.5rem;'>Product 3</h2>
            <h3 style='color: {BRAND_COLORS['info']}; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem;'>
                TrustCheck
            </h3>
        </div>
        <p style='color: #555; font-size: 1rem; line-height: 1.6; text-align: center; margin-bottom: 2rem;'>
            <strong>Automated QA</strong> for marketing reports. Validate data, catch errors,
            and ensure quality before client delivery. Never send a bad report again.
        </p>
        <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-top: auto;'>
            <p style='font-size: 0.95rem; color: #999; margin: 0.5rem 0;'><strong>⏳ Status:</strong> In Development</p>
            <p style='font-size: 0.95rem; color: #999; margin: 0.5rem 0;'><strong>🔍 Feature:</strong> Data validation</p>
            <p style='font-size: 0.95rem; color: #999; margin: 0.5rem 0;'><strong>🔍 Feature:</strong> Hallucination detection</p>
            <p style='font-size: 0.95rem; color: #999; margin: 0.5rem 0;'><strong>⚡ Output:</strong> Validated reports</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem; text-align: center;'>", unsafe_allow_html=True)
    st.button("⏳ Coming Soon", key="prod3", use_container_width=True, disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("## 💡 Why Electric Glue?")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"""
    <div style='padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); height: 100%;'>
        <h3 style='color: {BRAND_COLORS['primary']}; margin-top: 0;'>🎯 Built for Marketing Professionals</h3>
        <p style='font-size: 1rem; line-height: 1.7; color: #555;'>
            We're not data scientists trying to understand marketing—we're marketers who understand data science.
            Every tool is designed to answer questions you actually ask, not ones we think you should.
        </p>
        <ul style='font-size: 0.95rem; color: #666; line-height: 1.8;'>
            <li>No PhD required—plain English outputs</li>
            <li>Client-ready reports, not academic papers</li>
            <li>Built on proven methodologies, not hype</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); height: 100%;'>
        <h3 style='color: {BRAND_COLORS['accent']}; margin-top: 0;'>🤖 Multi-Agent AI Architecture</h3>
        <p style='font-size: 1rem; line-height: 1.7; color: #555;'>
            Each product uses specialized AI agents that collaborate like a team of experts.
            One agent handles data validation, another runs analysis, a third interprets results—all orchestrated seamlessly.
        </p>
        <ul style='font-size: 0.95rem; color: #666; line-height: 1.8;'>
            <li>Specialized agents for specialized tasks</li>
            <li>LLM-agnostic (works with or without APIs)</li>
            <li>Transparent, explainable outputs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Final Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; margin-top: 3rem;'>
    <p style='font-size: 0.85rem; color: #999; margin: 0.5rem 0;'>
        © 2025 Electric Glue | Proprietary AI-Powered Marketing Intelligence Platform
    </p>
    <p style='font-size: 0.8rem; color: #bbb; margin-top: 1rem;'>
        Powered by Multi-Agent AI × <strong style='color: {BRAND_COLORS['primary']};'>Front Left</strong> Thinking
    </p>
</div>
""", unsafe_allow_html=True)
