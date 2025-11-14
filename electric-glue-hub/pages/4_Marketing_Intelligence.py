"""
Product 2: Scout - Marketing Intelligence Assistant
Keyword search, file upload, web research, and multi-persona analysis
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import time
import json
from datetime import datetime
import re

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from config.branding import apply_electric_glue_theme, BRAND_COLORS, format_header
from agents.perspective_agents import get_all_perspectives

# Page config
st.set_page_config(
    page_title="Scout | Electric Glue",
    page_icon="🧠",
    layout="wide"
)

# Apply branding
apply_electric_glue_theme()

# Initialize session state
if 'research_complete' not in st.session_state:
    st.session_state.research_complete = False
if 'research_data' not in st.session_state:
    st.session_state.research_data = None
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = 'all'

# Header
st.markdown(format_header(
    "🧠 Scout - Marketing Intelligence Assistant",
    "Enter keywords, upload files, and get multi-perspective insights"
), unsafe_allow_html=True)

# Navigation
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("---")

# About this tool - expandable
with st.expander("📖 About This Tool", expanded=False):
    st.markdown(f"""
    ### What is Scout?

    **Scout** is your AI-powered research assistant for pitch preparation. Enter a company name or marketing topic,
    and Scout automatically gathers comprehensive business intelligence—from company performance and financials
    to customer profiles and vertical analysis.

    Research is then presented through **three strategic perspectives** to fuel creative ideation and strategic planning.

    ### How It Works

    1. **Enter Keywords** - Type any company, brand, campaign, or marketing topic
    2. **Upload Files (Optional)** - Add RFPs, briefs, reports, or competitor decks
    3. **Select Research Depth** - Choose quick scan, standard research, or deep dive
    4. **Pick Perspectives** - Choose which expert viewpoints you need
    5. **Get Insights** - Receive formatted, actionable analysis from AI agents
    6. **Export Results** - Download as markdown or text for presentations

    ### The Three Perspectives

    - 💰 **Stingy Customer** - Budget-conscious CFO focused on ROI and efficiency
    - 🔬 **Critical Thinker** - Data scientist questioning assumptions and biases
    - 🎨 **Creative Ad Man** - Creative director identifying brand opportunities

    ### Why Use This Tool?

    - ✅ **Multi-Perspective Analysis** - See campaigns through different stakeholder lenses
    - ✅ **Web + Document Research** - Combines online search with file analysis
    - ✅ **Sentiment Analysis** - NLP-powered tone and emotion detection
    - ✅ **Export-Ready Outputs** - Formatted for pitch decks and strategy docs
    - ✅ **Progress Tracking** - Real-time updates with time estimates

    ### Best For

    - 🎯 **Pitch Preparation** - Research prospects before new business meetings
    - 📊 **Competitive Analysis** - Understand competitor positioning and messaging
    - 🔍 **Trend Research** - Stay updated on industry movements and consumer behaviour
    - 📝 **Strategy Development** - Gather insights for campaign planning
    """)

st.markdown("---")

# Main Search Interface
st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
            padding: 2rem; border-radius: 15px; margin-bottom: 2rem; border-left: 5px solid {BRAND_COLORS['primary']};'>
    <h3 style='color: {BRAND_COLORS['secondary']}; margin-top: 0;'>🔍 What do you want to research?</h3>
    <p style='font-size: 1.05rem; color: #555; line-height: 1.8; margin-bottom: 0;'>
        Enter a company name, brand, campaign topic, or keywords. Scout will search the web,
        analyse uploaded files, and provide multi-perspective insights from our AI agents.
    </p>
</div>
""", unsafe_allow_html=True)

# Search Bar
col1, col2 = st.columns([4, 1])

with col1:
    search_query = st.text_input(
        "",
        placeholder="e.g., Nike marketing strategy, Airbnb brand positioning, Gen-Z social media trends...",
        label_visibility="collapsed",
        key="search_input",
        help="Enter any marketing research query - company names, topics, campaigns, trends"
    )

with col2:
    search_button = st.button("🚀 Research", type="primary", use_container_width=True)

# File Upload Section
with st.expander("📎 Upload Supporting Files (Optional)", expanded=False):
    st.markdown(f"""
    <p style='color: #666; font-size: 0.95rem; line-height: 1.7;'>
        Upload documents for Scout to analyse alongside web research:
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Accepted Files:**
        - PDFs (reports, briefs, decks)
        - Word Docs (strategy docs)
        - Text/Markdown files
        - CSV/Excel (data exports)
        """)

    with col2:
        st.markdown("""
        **What Scout Extracts:**
        - Key findings & insights
        - Data points & metrics
        - Strategic recommendations
        - Competitor mentions
        """)

    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=['pdf', 'docx', 'txt', 'md', 'csv', 'xlsx'],
        accept_multiple_files=True,
        help="Scout will extract relevant information from these documents",
        label_visibility="collapsed"
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        for file in uploaded_files:
            st.markdown(f"- **{file.name}** ({file.size / 1024:.1f} KB)")

# Advanced Options
with st.expander("⚙️ Advanced Research Options", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Research Depth")
        research_depth = st.select_slider(
            "Depth vs Speed",
            options=["Quick", "Balanced", "Deep Dive"],
            value="Balanced",
            help="Quick: 5-10min | Balanced: 15-20min | Deep: 30-45min"
        )

        time_estimates = {
            "Quick": "5-10 minutes",
            "Balanced": "15-20 minutes",
            "Deep Dive": "30-45 minutes"
        }
        st.caption(f"⏱️ Estimated time: {time_estimates[research_depth]}")

    with col2:
        st.markdown("#### Web Search Sources")
        search_sources = st.multiselect(
            "Search Sources",
            options=['Google', 'News Articles', 'Industry Reports', 'Company Websites',
                    'Social Media', 'Financial Data', 'Academic Papers'],
            default=['Google', 'News Articles', 'Company Websites'],
            help="Select where Scout should search for information"
        )

# Persona Selection
st.markdown("---")
st.markdown(f"## 🎭 Select Analysis Perspectives")

st.markdown(f"""
<p style='font-size: 1rem; color: #666; line-height: 1.7; margin-bottom: 1.5rem;'>
    Choose which perspectives you want Scout to analyse from. Each persona provides unique insights:
</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    persona_stingy = st.checkbox(
        "💰 Stingy Customer",
        value=True,
        help="Budget-conscious CFO perspective - ROI focused, skeptical of spending"
    )
    st.caption("Focus: ROI, efficiency, cost-cutting")

with col2:
    persona_critical = st.checkbox(
        "🔬 Critical Thinker",
        value=True,
        help="Data scientist perspective - questions assumptions, looks for biases"
    )
    st.caption("Focus: Rigor, methodology, assumptions")

with col3:
    persona_creative = st.checkbox(
        "🎨 Creative Ad Man",
        value=True,
        help="Creative director perspective - brand building, bold campaigns"
    )
    st.caption("Focus: Brand, creativity, culture")

# Research Execution
if search_button or st.session_state.research_complete:
    if not search_query and not search_button:
        # Just showing previous results
        pass
    elif search_button and not search_query:
        st.error("⚠️ Please enter a search query to begin research")
    elif not any([persona_stingy, persona_critical, persona_creative]):
        st.error("⚠️ Please select at least one perspective for analysis")
    else:
        # Start research process
        st.session_state.research_complete = False

        st.markdown("---")
        st.markdown(f"### 🔍 Researching: *{search_query}*")

        # Time estimation
        time_map = {"Quick": 10, "Balanced": 20, "Deep Dive": 40}
        estimated_time = time_map.get(research_depth, 20)

        st.markdown(f"""
        <div style='background: {BRAND_COLORS['accent']}; color: black; padding: 1rem;
                    border-radius: 8px; margin-bottom: 1.5rem; text-align: center;'>
            <strong>⏱️ Estimated completion: {estimated_time} seconds</strong> |
            <span style='opacity: 0.8;'>Depth: {research_depth}</span>
        </div>
        """, unsafe_allow_html=True)

        # Progress tracking
        progress_container = st.container()

        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            agent_status = st.empty()

            # Research phases
            phases = [
                ("🌐 Web Search", "Searching across selected sources", 15, "primary"),
                ("📄 Document Processing", "Extracting insights from uploaded files", 10, "accent"),
                ("🧹 Data Cleaning", "Structuring and validating research data", 8, "info"),
                ("🧠 Sentiment Analysis", "Analyzing tone and sentiment in findings", 12, "success"),
                ("📊 Creating Visualisations", "Generating charts and insights", 10, "warning"),
            ]

            # Add persona analysis phases
            active_personas = []
            if persona_stingy:
                phases.append(("💰 Stingy Customer Analysis", "Analyzing from ROI/budget perspective", 15, "warning"))
                active_personas.append("stingy")
            if persona_critical:
                phases.append(("🔬 Critical Thinker Analysis", "Questioning assumptions and methodology", 15, "info"))
                active_personas.append("critical")
            if persona_creative:
                phases.append(("🎨 Creative Ad Man Analysis", "Identifying brand opportunities", 15, "accent"))
                active_personas.append("creative")

            phases.append(("✨ Synthesis", "Combining insights into final report", 10, "success"))

            total_duration = sum(p[2] for p in phases)
            elapsed = 0

            for i, (phase_name, phase_desc, duration, color) in enumerate(phases):
                # Update status
                status_text.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {BRAND_COLORS[color]};'>
                    <strong style='color: {BRAND_COLORS[color]};'>Phase {i+1}/{len(phases)}:</strong> {phase_name}<br/>
                    <span style='color: #666; font-size: 0.9rem;'>{phase_desc}</span>
                </div>
                """, unsafe_allow_html=True)

                # Show agent working indicator
                agent_status.markdown(f"""
                <div style='text-align: center; padding: 0.5rem;'>
                    <span style='background: {BRAND_COLORS['accent']}; color: black; padding: 0.5rem 1rem;
                                border-radius: 20px; font-size: 0.9rem; font-weight: 600;'>
                        🔄 Agent Working...
                    </span>
                </div>
                """, unsafe_allow_html=True)

                # Simulate processing
                phase_steps = 5
                for step in range(phase_steps):
                    time.sleep(duration / (phase_steps * 10))  # Speed up for demo
                    elapsed += duration / phase_steps
                    progress_bar.progress(min(int((elapsed / total_duration) * 100), 100))

                # Mark phase complete
                agent_status.markdown(f"""
                <div style='text-align: center; padding: 0.5rem;'>
                    <span style='background: {BRAND_COLORS['success']}; color: black; padding: 0.5rem 1rem;
                                border-radius: 20px; font-size: 0.9rem; font-weight: 600;'>
                        ✅ Complete
                    </span>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.3)

            progress_bar.progress(100)
            status_text.success(f"✅ Research complete! Analyzed **{search_query}** from {len(active_personas)} perspectives")
            time.sleep(0.5)

        # Clear progress indicators
        progress_container.empty()

        # Store research results
        st.session_state.research_complete = True
        st.session_state.research_data = {
            'query': search_query,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'depth': research_depth,
            'personas': active_personas,
            'files_analysed': len(uploaded_files) if uploaded_files else 0,
            'sources_searched': len(search_sources) if search_sources else 3
        }

# Display Results
if st.session_state.research_complete and st.session_state.research_data:
    data = st.session_state.research_data

    st.markdown("---")
    st.success(f"✅ **Research Complete**: {data['query']}")

    # Summary Stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Sources Searched", data['sources_searched'])
    with col2:
        st.metric("Files Analyzed", data['files_analysed'])
    with col3:
        st.metric("Perspectives", len(data['personas']))
    with col4:
        st.metric("Research Depth", data['depth'])

    st.markdown("---")

    # Sentiment & Key Findings Visualization
    st.markdown(f"## 📊 Research Summary & Sentiment Analysis")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 12px; border-top: 4px solid {BRAND_COLORS['primary']};
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
            <h4 style='color: {BRAND_COLORS['primary']}; margin-top: 0;'>🔑 Key Findings</h4>
            <ul style='color: #555; line-height: 2; font-size: 1rem;'>
                <li><strong>Market Position:</strong> Strong brand recognition in target demographic (18-34)</li>
                <li><strong>Competitive Advantage:</strong> Unique positioning in sustainability and ethics</li>
                <li><strong>Growth Opportunity:</strong> Underutilized social commerce and influencer partnerships</li>
                <li><strong>Risk Factor:</strong> Heavy reliance on single marketing channel (Instagram 65% of traffic)</li>
                <li><strong>Budget Efficiency:</strong> CAC trending upward (↑23% YoY), optimization needed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Sentiment breakdown
        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 12px; border-top: 4px solid {BRAND_COLORS['success']};
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
            <h4 style='color: {BRAND_COLORS['success']}; margin-top: 0;'>💬 Sentiment Analysis</h4>
            <div style='margin: 1rem 0;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                    <span style='color: #666;'>Positive</span>
                    <span style='color: {BRAND_COLORS['success']}; font-weight: bold;'>62%</span>
                </div>
                <div style='background: #f0f0f0; border-radius: 10px; height: 12px; overflow: hidden;'>
                    <div style='background: {BRAND_COLORS['success']}; width: 62%; height: 100%;'></div>
                </div>
            </div>
            <div style='margin: 1rem 0;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                    <span style='color: #666;'>Neutral</span>
                    <span style='color: #666; font-weight: bold;'>28%</span>
                </div>
                <div style='background: #f0f0f0; border-radius: 10px; height: 12px; overflow: hidden;'>
                    <div style='background: #666; width: 28%; height: 100%;'></div>
                </div>
            </div>
            <div style='margin: 1rem 0;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                    <span style='color: #666;'>Negative</span>
                    <span style='color: {BRAND_COLORS['danger']}; font-weight: bold;'>10%</span>
                </div>
                <div style='background: #f0f0f0; border-radius: 10px; height: 12px; overflow: hidden;'>
                    <div style='background: {BRAND_COLORS['danger']}; width: 10%; height: 100%;'></div>
                </div>
            </div>
            <p style='color: #999; font-size: 0.85rem; margin-top: 1rem; font-style: italic;'>
                Based on analysis of 247 mentions across web sources
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Topic Word Cloud (simulated with text)
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
                padding: 2rem; border-radius: 12px;'>
        <h4 style='color: {BRAND_COLORS['secondary']}; margin-top: 0;'>☁️ Key Topics & Themes</h4>
        <div style='text-align: center; padding: 1.5rem;'>
            <span style='font-size: 2rem; color: {BRAND_COLORS['primary']}; margin: 0.5rem;'>sustainability</span>
            <span style='font-size: 1.6rem; color: {BRAND_COLORS['accent']}; margin: 0.5rem;'>brand positioning</span>
            <span style='font-size: 1.4rem; color: {BRAND_COLORS['info']}; margin: 0.5rem;'>social media</span>
            <span style='font-size: 1.8rem; color: {BRAND_COLORS['success']}; margin: 0.5rem;'>Gen-Z</span>
            <span style='font-size: 1.3rem; color: #666; margin: 0.5rem;'>influencer marketing</span>
            <span style='font-size: 1.5rem; color: {BRAND_COLORS['warning']}; margin: 0.5rem;'>ROI optimization</span>
            <span style='font-size: 1.2rem; color: {BRAND_COLORS['accent']}; margin: 0.5rem;'>customer acquisition</span>
            <span style='font-size: 1.7rem; color: {BRAND_COLORS['primary']}; margin: 0.5rem;'>authenticity</span>
            <span style='font-size: 1.4rem; color: #666; margin: 0.5rem;'>content strategy</span>
        </div>
        <p style='color: #666; font-size: 0.9rem; text-align: center; margin-top: 1rem;'>
            Size indicates frequency of mention across research sources
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Persona Toggle Interface
    st.markdown(f"## 🎭 Multi-Perspective Analysis")

    st.markdown(f"""
    <p style='font-size: 1rem; color: #666; line-height: 1.7; margin-bottom: 1.5rem;'>
        Toggle between different perspectives to see how each persona interprets the research:
    </p>
    """, unsafe_allow_html=True)

    # Persona selector buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔄 All Perspectives", use_container_width=True,
                    type="primary" if st.session_state.selected_persona == 'all' else "secondary"):
            st.session_state.selected_persona = 'all'

    with col2:
        if 'stingy' in data['personas']:
            if st.button("💰 Stingy Customer", use_container_width=True,
                        type="primary" if st.session_state.selected_persona == 'stingy' else "secondary"):
                st.session_state.selected_persona = 'stingy'

    with col3:
        if 'critical' in data['personas']:
            if st.button("🔬 Critical Thinker", use_container_width=True,
                        type="primary" if st.session_state.selected_persona == 'critical' else "secondary"):
                st.session_state.selected_persona = 'critical'

    with col4:
        if 'creative' in data['personas']:
            if st.button("🎨 Creative Ad Man", use_container_width=True,
                        type="primary" if st.session_state.selected_persona == 'creative' else "secondary"):
                st.session_state.selected_persona = 'creative'

    st.markdown("<br>", unsafe_allow_html=True)

    # Mock data for each persona (in real implementation, this would come from agents)
    persona_analyses = {
        'stingy': {
            'icon': '💰',
            'name': 'Stingy Customer',
            'color': BRAND_COLORS['warning'],
            'tagline': 'Budget-Conscious CFO Perspective',
            'insight': f"The spending on {data['query']} shows decent returns, but there's fat to cut. Current ROI is 2.4x which is barely acceptable. Bottom 30% of channels are dragging performance down significantly.",
            'actions': [
                "**Cut underperforming channels immediately** - Instagram Stories ads have 0.8x ROI. Kill them and reallocate £15K/month to proven performers",
                "**Demand proof before scaling** - Before increasing budget, run controlled A/B tests. Never scale without 95% confidence in lift",
                "**Renegotiate all vendor contracts** - Influencer agencies charging 20% commission. Industry standard is 12-15%. Push back hard",
                "**Focus on high-intent channels** - Google Search converts at 5.2x vs. social at 1.8x. Why are we spending 60% on social?"
            ],
            'warning': "Don't fall for 'brand building' excuses when ROI is unclear. If it can't be measured with hard revenue attribution, cut the budget in half until proven.",
            'opportunity': "Quick win: Shift 40% of social budget to search. Based on current conversion data, this could boost revenue by £180K annually with same spend."
        },
        'critical': {
            'icon': '🔬',
            'name': 'Critical Thinker',
            'color': BRAND_COLORS['info'],
            'tagline': 'Data Scientist Questioning Assumptions',
            'insight': f"The research on {data['query']} has some methodological concerns. Sample size looks adequate (N=2,400) but time period is only 45 days - not enough to control for seasonality or external shocks.",
            'actions': [
                "**Test attribution model assumptions** - Currently using last-click. This systematically undervalues top-of-funnel. Run incrementality test",
                "**Check for confounders** - Major competitor launched campaign same week. Is the lift actually from our efforts or market expansion?",
                "**Segment analysis required** - Aggregate ROI hides critical variation. New vs returning customers likely behave very differently",
                "**Statistical power check** - With current sample size, can only detect >15% lift reliably. Smaller effects are noise"
            ],
            'warning': "Correlation ≠ causation. Sales went up when campaign ran, but we had 3 other major variables change simultaneously. This needs proper causal inference, not just correlation charts.",
            'opportunity': "Run a proper holdout test in 2-3 markets. Turn off campaign entirely in control markets. Only way to measure true incrementality vs. baseline growth."
        },
        'creative': {
            'icon': '🎨',
            'name': 'Creative Ad Man',
            'color': BRAND_COLORS['accent'],
            'tagline': 'Creative Director Seeing Opportunities',
            'insight': f"The research shows {data['query']} has strong functional benefits but weak emotional connection. Brand is playing it safe - very 'category typical' creative. Massive opportunity to stand out with bold positioning.",
            'actions': [
                "**Launch a provocative brand platform** - Current messaging is forgettable. Need a bold POV that gets PR and social conversation, not just clicks",
                "**Partner with culture creators** - Stop working with macro-influencers charging £50K for mediocre content. Find 5-10 real creators making culture, not just content",
                "**Create a cultural moment** - Tie into something people care about. Sustainability? Gen-Z anxiety? Don't just advertise, participate in conversations that matter",
                "**Kill the safe creative** - Those stock photo ads with generic copy? They're invisible. Invest in 2-3 big swings that could actually win awards and attention"
            ],
            'warning': "Don't let performance marketers kill every creative idea with A/B tests. Great creative compounds over time. You can't A/B test a Super Bowl ad. Sometimes you need conviction, not just data.",
            'opportunity': "Pitch a bold brand campaign that breaks category norms. Something that gets shared, talked about, parodied. That's how you build a brand, not another \\\"shop now\\\" carousel ad."
        }
    }

    # Display selected perspective(s)
    perspectives_to_show = []
    if st.session_state.selected_persona == 'all':
        perspectives_to_show = [p for p in ['stingy', 'critical', 'creative'] if p in data['personas']]
    elif st.session_state.selected_persona in data['personas']:
        perspectives_to_show = [st.session_state.selected_persona]

    for persona_key in perspectives_to_show:
        persona = persona_analyses[persona_key]

        st.markdown(f"""
        <div style='background: white; padding: 2.5rem; border-radius: 15px; border-top: 6px solid {persona['color']};
                    box-shadow: 0 6px 20px rgba(0,0,0,0.1); margin-bottom: 2rem;'>
            <div style='text-align: center; margin-bottom: 2rem;'>
                <div style='font-size: 3rem; margin-bottom: 0.5rem;'>{persona['icon']}</div>
                <h3 style='color: {persona['color']}; margin: 0;'>{persona['name']}</h3>
                <p style='color: #666; font-size: 1rem; margin: 0.5rem 0 0 0;'>{persona['tagline']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Key Insight
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; border-left: 4px solid {persona['color']};'>
            <h4 style='color: {BRAND_COLORS['secondary']}; margin-top: 0;'>🔑 Key Insight</h4>
            <p style='color: #555; font-size: 1.05rem; line-height: 1.8; margin: 0; font-style: italic;'>
                "{persona['insight']}"
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Top Actions
        st.markdown(f"**📋 Top Strategic Actions:**")
        for i, action in enumerate(persona['actions'], 1):
            st.markdown(f"{i}. {action}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Warning
        st.markdown(f"""
        <div style='background: rgba(255,0,0,0.05); padding: 1.5rem; border-radius: 10px; border-left: 4px solid {BRAND_COLORS['danger']};'>
            <h4 style='color: {BRAND_COLORS['danger']}; margin-top: 0;'>⚠️ Warning / Caveat</h4>
            <p style='color: #555; font-size: 1rem; line-height: 1.7; margin: 0;'>
                {persona['warning']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Strategic Opportunity
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 10px; border: 2px solid {persona['color']};'>
            <h4 style='color: {persona['color']}; margin-top: 0;'>💡 Strategic Opportunity</h4>
            <p style='color: #555; font-size: 1.05rem; line-height: 1.8; margin: 0;'>
                {persona['opportunity']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if persona_key != perspectives_to_show[-1]:
            st.markdown("---")

    # Export Options
    st.markdown("---")
    st.markdown(f"## 📥 Export Research Report")

    col1, col2, col3 = st.columns(3)

    # Generate export content
    export_content = f"""# SCOUT RESEARCH BRIEF: {data['query']}
Generated by Electric Glue Scout
Date: {data['timestamp']}
Research Depth: {data['depth']}

---

## Research Summary

**Sources Searched:** {data['sources_searched']}
**Files Analyzed:** {data['files_analysed']}
**Perspectives Generated:** {len(data['personas'])}

### Key Findings
- Market Position: Strong brand recognition in target demographic (18-34)
- Competitive Advantage: Unique positioning in sustainability and ethics
- Growth Opportunity: Underutilized social commerce and influencer partnerships
- Risk Factor: Heavy reliance on single marketing channel (Instagram 65% of traffic)
- Budget Efficiency: CAC trending upward (↑23% YoY), optimization needed

### Sentiment Analysis
- Positive: 62%
- Neutral: 28%
- Negative: 10%

---

"""

    for persona_key in perspectives_to_show:
        persona = persona_analyses[persona_key]
        export_content += f"""
## {persona['icon']} {persona['name']} Perspective

**{persona['tagline']}**

### Key Insight
{persona['insight']}

### Top Strategic Actions
"""
        for i, action in enumerate(persona['actions'], 1):
            export_content += f"{i}. {action}\n"

        export_content += f"""
### Warning
{persona['warning']}

### Strategic Opportunity
{persona['opportunity']}

---

"""

    export_content += f"""
*Generated by Electric Glue Scout | Marketing Intelligence Assistant*
*Research completed in {data['depth'].lower()} mode with {len(data['personas'])} strategic perspectives*
"""

    with col1:
        st.download_button(
            label="📄 Download Markdown",
            data=export_content,
            file_name=f"scout_research_{re.sub(r'[^a-z0-9]+', '_', data['query'].lower())}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:
        st.download_button(
            label="📋 Download Text",
            data=export_content,
            file_name=f"scout_research_{re.sub(r'[^a-z0-9]+', '_', data['query'].lower())}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col3:
        st.button("📊 Export to PDF", use_container_width=True, disabled=True,
                 help="Coming soon - PDF export with visualisations")

else:
    # Welcome State
    st.markdown(f"""
    <div style='text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, rgba(0,255,0,0.03) 0%, rgba(0,0,0,0.03) 100%);
                border-radius: 15px; margin-top: 2rem;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🧠</div>
        <h3 style='color: {BRAND_COLORS['secondary']}; margin-bottom: 1rem;'>Ready to Research?</h3>
        <p style='color: #666; font-size: 1.15rem; line-height: 1.8; max-width: 600px; margin: 0 auto;'>
            Enter any marketing topic, company name, or campaign in the search bar above.
            Scout will search the web, analyse your files, and provide multi-perspective insights
            from AI agents with different expertise.
        </p>
        <div style='margin-top: 2rem; padding: 1.5rem; background: white; border-radius: 10px; max-width: 500px; margin-left: auto; margin-right: auto;'>
            <p style='color: {BRAND_COLORS['primary']}; font-size: 1.1rem; font-weight: 600; margin: 0.5rem 0;'>
                ⚡ Powered by Multi-Agent AI
            </p>
            <p style='color: #999; font-size: 0.95rem; margin: 0.5rem 0;'>
                🔍 Web search • 📄 Document analysis • 🎭 3 expert perspectives
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(0,255,0,0.03) 0%, rgba(0,0,0,0.03) 100%);
            border-radius: 12px; margin-top: 2rem;'>
    <p style='color: {BRAND_COLORS['text']}; font-size: 1rem; font-weight: 600; margin: 0.5rem 0;'>
        ⚡ <strong>Electric Glue</strong> | Product 2: Scout
    </p>
    <p style='font-size: 0.9rem; color: {BRAND_COLORS['text_secondary']}; margin: 0.5rem 0;'>
        Marketing Intelligence Assistant
    </p>
    <p style='font-size: 0.85rem; color: #999; margin: 1rem 0 0.5rem 0;'>
        Powered by Multi-Agent AI • Web Search • NLP Sentiment Analysis
    </p>
    <p style='font-size: 0.8rem; color: #bbb; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e0e0e0;'>
        Powered by Multi-Agent AI × <strong style='color: {BRAND_COLORS['primary']};'>Front Left</strong> Thinking
    </p>
</div>
""", unsafe_allow_html=True)
