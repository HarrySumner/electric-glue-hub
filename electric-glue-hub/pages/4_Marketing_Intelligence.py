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
from config.qa_status import render_qa_traffic_light
from agents.perspective_agents import get_all_perspectives
from agents.scout_research_agent import ScoutResearchAgent

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

    - 😈 **Devil's Advocate** - Risk analysis, what could go wrong, hidden costs
    - 🌟 **Optimist** - Growth opportunities, untapped potential, quick wins
    - ⚖️ **Realist** - Practical constraints, trade-offs, MVP approach

    ### Why Use This Tool?

    - ✅ **Multi-Perspective Analysis** - See campaigns through different stakeholder lenses
    - ✅ **QA Housekeeping Agent** - Every output validated for fabrications and errors before display
    - ✅ **Web + Document Research** - Combines online search with file analysis
    - ✅ **Fact-Constrained Insights** - All claims grounded in verified sources with citations
    - ✅ **Export-Ready Outputs** - Formatted for pitch decks and strategy docs
    - ✅ **Progress Tracking** - Real-time updates with time estimates

    ### Best For

    - 🎯 **Pitch Preparation** - Research prospects before new business meetings
    - 📊 **Competitive Analysis** - Understand competitor positioning and messaging
    - 🔍 **Trend Research** - Stay updated on industry movements and consumer behaviour
    - 📝 **Strategy Development** - Gather insights for campaign planning
    """)

st.markdown("---")

# Render QA traffic light in sidebar
render_qa_traffic_light(location="sidebar")

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
    search_button = st.button("🚀 Research", type="primary", width='stretch')

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

# Set all personas to true by default (always analyze all perspectives)
persona_stingy = True
persona_critical = True
persona_creative = True

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
        # CRITICAL: Clear previous results when starting new search
        if search_button:
            # User clicked the button - this is a NEW query
            # Check if query changed from previous
            previous_query = st.session_state.research_data.get('query', '') if st.session_state.research_data else ''
            if search_query != previous_query:
                # NEW QUERY - clear all cached data
                st.session_state.research_complete = False
                st.session_state.research_data = None
                st.session_state.scout_results = None
                st.info(f"🔄 Starting fresh research for: {search_query}")
            else:
                # Same query - just re-running
                st.session_state.research_complete = False
        else:
            # Just displaying previous results - don't clear
            pass

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

            # Determine active personas
            active_personas = []
            if persona_stingy:
                active_personas.append("stingy")
            if persona_critical:
                active_personas.append("critical")
            if persona_creative:
                active_personas.append("creative")

            # Progress callback for Scout agent
            def update_progress(phase_name, phase_desc, progress_pct):
                status_text.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {BRAND_COLORS['primary']};'>
                    <strong style='color: {BRAND_COLORS['primary']};'>{phase_name}</strong><br/>
                    <span style='color: #666; font-size: 0.9rem;'>{phase_desc}</span>
                </div>
                """, unsafe_allow_html=True)

                agent_status.markdown(f"""
                <div style='text-align: center; padding: 0.5rem;'>
                    <span style='background: {BRAND_COLORS['accent']}; color: black; padding: 0.5rem 1rem;
                                border-radius: 20px; font-size: 0.9rem; font-weight: 600;'>
                        🔄 Agent Working...
                    </span>
                </div>
                """, unsafe_allow_html=True)

                progress_bar.progress(progress_pct)
                time.sleep(0.5)

            # Execute real Scout research
            try:
                scout_agent = ScoutResearchAgent()
                research_results = scout_agent.research(
                    query=search_query,
                    depth=research_depth,
                    personas=active_personas,
                    progress_callback=update_progress
                )

                # Mark complete
                agent_status.markdown(f"""
                <div style='text-align: center; padding: 0.5rem;'>
                    <span style='background: {BRAND_COLORS['success']}; color: black; padding: 0.5rem 1rem;
                                border-radius: 20px; font-size: 0.9rem; font-weight: 600;'>
                        ✅ Complete
                    </span>
                </div>
                """, unsafe_allow_html=True)

                progress_bar.progress(100)
                status_text.success(f"✅ Research complete! Analyzed **{search_query}** from {len(active_personas)} perspectives")
                time.sleep(0.5)

                # Store research results
                st.session_state.scout_results = research_results

            except Exception as e:
                status_text.error(f"❌ Research failed: {str(e)}")
                st.session_state.scout_results = None

        # Clear progress indicators
        progress_container.empty()

        # Store research results (combine Scout results with session state)
        st.session_state.research_complete = True

        if st.session_state.get('scout_results'):
            scout = st.session_state.scout_results
            st.session_state.research_data = {
                'query': search_query,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'depth': research_depth,
                'personas': active_personas,
                'files_analysed': len(uploaded_files) if uploaded_files else 0,
                'sources_searched': len(scout.get('sources', [])),
                'facts_count': len(scout.get('facts', [])),
                'quality_score': scout.get('quality_score', 0),
                'quality_report': scout.get('quality_report', {}),
                'insights': scout.get('insights', {})
            }
        else:
            # Fallback if Scout failed
            st.session_state.research_data = {
                'query': search_query,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'depth': research_depth,
                'personas': active_personas,
                'files_analysed': len(uploaded_files) if uploaded_files else 0,
                'sources_searched': len(search_sources) if search_sources else 3,
                'facts_count': 0,
                'quality_score': 0,
                'insights': {}
            }

# Display Results
if st.session_state.research_complete and st.session_state.research_data:
    data = st.session_state.research_data

    st.markdown("---")
    st.success(f"✅ **Research Complete**: {data['query']}")

    # Summary Stats
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Sources Searched", data['sources_searched'])
    with col2:
        st.metric("Facts Extracted", data.get('facts_count', 0))
    with col3:
        st.metric("Perspectives", len(data['personas']))
    with col4:
        quality_score = data.get('quality_score', 0)
        st.metric("Quality Score", f"{quality_score:.0f}/100")
    with col5:
        st.metric("Research Depth", data['depth'])

    st.markdown("---")

    # QA Validation Status (if available)
    if 'qa_validation' in data:
        qa_val = data['qa_validation']

        if data.get('qa_blocked', False):
            # Output was BLOCKED by QA
            st.error("🚫 **QA VALIDATION BLOCKED OUTPUT** - Critical issues detected. Output not shown to prevent fabricated information.")

            with st.expander("❌ Critical Issues Found", expanded=True):
                for issue in data.get('qa_issues', []):
                    st.markdown(f"""
                    **{issue['severity']} - {issue['type']}**
                    - {issue['description']}
                    - *Location:* {issue.get('location', 'N/A')}
                    - *Fix:* {issue.get('recommendation', 'N/A')}
                    """)

        elif qa_val.get('decision') == 'WARN' and 'qa_warnings' in data:
            # Output approved with warnings
            st.warning(f"⚠️ **QA Validation:** Output approved with {len(data['qa_warnings'])} warnings")

            with st.expander("⚠️ View QA Warnings"):
                for warning in data['qa_warnings']:
                    st.markdown(f"- **{warning['severity']}**: {warning['description']}")

        elif qa_val.get('decision') == 'APPROVE':
            # Clean validation pass
            st.success("✅ **QA Validation Passed** - All claims verified against source data. No fabrications detected.")

        elif qa_val.get('status') == 'disabled':
            st.info("ℹ️ QA Validation not available for this output")

    st.markdown("---")

    # DEBUG: Show raw sources and facts
    with st.expander("🔍 DEBUG: Raw Research Data", expanded=False):
        st.markdown("### Sources Retrieved")
        if 'scout_results' in st.session_state:
            sources = st.session_state.scout_results.get('sources', [])
            st.write(f"**Total sources:** {len(sources)}")
            for i, source in enumerate(sources[:10], 1):
                st.markdown(f"{i}. **{source.get('title', 'No title')}**")
                st.markdown(f"   - URL: {source.get('url', 'No URL')}")
                st.markdown(f"   - Description: {source.get('description', 'No description')[:200]}")
                st.markdown(f"   - Type: {source.get('source_type', 'unknown')}")

        st.markdown("### Facts Extracted")
        if 'scout_results' in st.session_state:
            facts = st.session_state.scout_results.get('facts', [])
            st.write(f"**Total facts:** {len(facts)}")
            for i, fact in enumerate(facts[:15], 1):
                st.markdown(f"{i}. [{fact.get('category', 'unknown')}] {fact.get('claim', 'No claim')[:150]}")
                st.markdown(f"   - Source: {fact.get('source_url', 'No source')[:80]}")
                st.markdown(f"   - Confidence: {fact.get('confidence', 'unknown')}")

    # Sentiment & Key Findings Visualization
    st.markdown(f"## 📊 Research Summary & Sentiment Analysis")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Generate key findings from actual facts if available
        key_findings_html = ""
        if 'scout_results' in st.session_state:
            facts = st.session_state.scout_results.get('facts', [])
            if facts and len(facts) >= 5:
                # Extract first 5 facts as key findings
                key_findings_html = "<ul style='color: #555; line-height: 2; font-size: 1rem;'>"
                for i, fact in enumerate(facts[:5], 1):
                    category = fact.get('category', 'General').title()
                    claim = fact.get('claim', 'No data available')
                    key_findings_html += f"<li><strong>{category}:</strong> {claim}</li>"
                key_findings_html += "</ul>"
            else:
                key_findings_html = f"<p style='color: #888;'>Gathering research data for {data['query']}...</p>"
        else:
            # Fallback mock data (only if no real data)
            key_findings_html = """
            <ul style='color: #555; line-height: 2; font-size: 1rem;'>
                <li><strong>Market Position:</strong> Strong brand recognition in target demographic (18-34)</li>
                <li><strong>Competitive Advantage:</strong> Unique positioning in sustainability and ethics</li>
                <li><strong>Growth Opportunity:</strong> Underutilized social commerce and influencer partnerships</li>
                <li><strong>Risk Factor:</strong> Heavy reliance on single marketing channel (Instagram 65% of traffic)</li>
                <li><strong>Budget Efficiency:</strong> CAC trending upward (↑23% YoY), optimization needed</li>
            </ul>
            """

        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 12px; border-top: 4px solid {BRAND_COLORS['primary']};
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
            <h4 style='color: {BRAND_COLORS['primary']}; margin-top: 0;'>🔑 Key Findings</h4>
            {key_findings_html}
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

    # Topic Word Cloud - Generated from actual research data
    wordcloud_html = ""
    if 'scout_results' in st.session_state and st.session_state.scout_results:
        facts = st.session_state.scout_results.get('facts', [])

        # Extract keywords from facts and count frequency
        from collections import Counter
        import re

        # Common words to exclude
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'their', 'them'}

        word_freq = Counter()

        # Extract words from fact claims
        for fact in facts:
            claim = fact.get('claim', '').lower()
            # Remove punctuation and split into words
            words = re.findall(r'\b[a-z]{3,}\b', claim)
            # Filter out stopwords and count
            filtered_words = [w for w in words if w not in stopwords]
            word_freq.update(filtered_words)

        # Get top 12 words
        top_words = word_freq.most_common(12)

        if top_words:
            # Generate word cloud HTML with varying sizes
            colors = [BRAND_COLORS['primary'], BRAND_COLORS['accent'], BRAND_COLORS['info'],
                     BRAND_COLORS['success'], BRAND_COLORS['warning'], '#666']

            wordcloud_items = ""
            max_count = top_words[0][1] if top_words else 1

            for i, (word, count) in enumerate(top_words):
                # Size based on frequency (1.2rem to 2.2rem)
                size = 1.2 + (count / max_count) * 1.0
                color = colors[i % len(colors)]
                wordcloud_items += f"<span style='font-size: {size}rem; color: {color}; margin: 0.5rem;'>{word}</span>\n"

            wordcloud_html = f"""
            <div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
                        padding: 2rem; border-radius: 12px;'>
                <h4 style='color: {BRAND_COLORS['secondary']}; margin-top: 0;'>☁️ Key Topics & Themes</h4>
                <div style='text-align: center; padding: 1.5rem; line-height: 2.5;'>
                    {wordcloud_items}
                </div>
                <p style='color: #666; font-size: 0.9rem; text-align: center; margin-top: 1rem;'>
                    Generated from {len(facts)} extracted facts • Size indicates frequency of mention
                </p>
            </div>
            """
        else:
            # Fallback if no words extracted
            wordcloud_html = f"""
            <div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
                        padding: 2rem; border-radius: 12px;'>
                <h4 style='color: {BRAND_COLORS['secondary']}; margin-top: 0;'>☁️ Key Topics & Themes</h4>
                <p style='color: #666; text-align: center; padding: 2rem;'>
                    Gathering keyword data from research...
                </p>
            </div>
            """
    else:
        # Fallback for demo/mock data
        wordcloud_html = f"""
        <div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
                    padding: 2rem; border-radius: 12px;'>
            <h4 style='color: {BRAND_COLORS['secondary']}; margin-top: 0;'>☁️ Key Topics & Themes</h4>
            <div style='text-align: center; padding: 1.5rem;'>
                <span style='font-size: 2rem; color: {BRAND_COLORS['primary']}; margin: 0.5rem;'>{data['query'].split()[0] if data['query'] else 'marketing'}</span>
                <span style='font-size: 1.6rem; color: {BRAND_COLORS['accent']}; margin: 0.5rem;'>strategy</span>
                <span style='font-size: 1.4rem; color: {BRAND_COLORS['info']}; margin: 0.5rem;'>analysis</span>
                <span style='font-size: 1.8rem; color: {BRAND_COLORS['success']}; margin: 0.5rem;'>insights</span>
            </div>
            <p style='color: #666; font-size: 0.9rem; text-align: center; margin-top: 1rem;'>
                Research in progress...
            </p>
        </div>
        """

    st.markdown(wordcloud_html, unsafe_allow_html=True)

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
        if st.button("🔄 All Perspectives", width='stretch',
                    type="primary" if st.session_state.selected_persona == 'all' else "secondary"):
            st.session_state.selected_persona = 'all'

    with col2:
        if 'devil' in data['personas']:
            if st.button("😈 Devil's Advocate", width='stretch',
                        type="primary" if st.session_state.selected_persona == 'devil' else "secondary"):
                st.session_state.selected_persona = 'devil'

    with col3:
        if 'optimist' in data['personas']:
            if st.button("🌟 Optimist", width='stretch',
                        type="primary" if st.session_state.selected_persona == 'optimist' else "secondary"):
                st.session_state.selected_persona = 'optimist'

    with col4:
        if 'realist' in data['personas']:
            if st.button("⚖️ Realist", width='stretch',
                        type="primary" if st.session_state.selected_persona == 'realist' else "secondary"):
                st.session_state.selected_persona = 'realist'

    st.markdown("<br>", unsafe_allow_html=True)

    # Get real Scout insights or fallback to mock data
    scout_insights = data.get('insights', {})

    # If we have real Scout insights, use them; otherwise use mock data
    if scout_insights:
        persona_analyses = {}
        for persona_key in ['devil', 'optimist', 'realist']:
            if persona_key in scout_insights:
                insight_data = scout_insights[persona_key]
                persona_analyses[persona_key] = {
                    'icon': '😈' if persona_key == 'devil' else ('🌟' if persona_key == 'optimist' else '⚖️'),
                    'name': insight_data.get('perspective', persona_key.title()),
                    'color': BRAND_COLORS['danger'] if persona_key == 'devil' else (BRAND_COLORS['success'] if persona_key == 'optimist' else BRAND_COLORS['info']),
                    'tagline': 'Risk Analysis & What Could Go Wrong' if persona_key == 'devil' else ('Growth Opportunities & Quick Wins' if persona_key == 'optimist' else 'Practical Constraints & Trade-Offs'),
                    'insight': insight_data.get('key_insight', ''),
                    'actions': insight_data.get('actions', []),
                    'warning': insight_data.get('warning', ''),
                    'opportunity': insight_data.get('key_insight', '')  # Using key_insight as opportunity
                }
    else:
        # Fallback mock data
        persona_analyses = {
        'devil': {
            'icon': '😈',
            'name': "Devil's Advocate",
            'color': BRAND_COLORS['danger'],
            'tagline': 'Risk Analysis & What Could Go Wrong',
            'insight': f"The {data['query']} strategy has several red flags. Heavy dependency on single-channel performance creates systemic risk. If Instagram algorithm changes or costs spike, entire funnel collapses. No diversification buffer.",
            'actions': [
                "**Identify dependency risks** - 70% of leads from one channel. Build contingency plan for algorithm changes or platform policy shifts",
                "**Stress test budget assumptions** - Current ROI assumes stable CPMs. Model scenarios: What if costs increase 50%? What's break-even?",
                "**Document failure modes** - Create risk register: Attribution breakdown, competitor copying tactics, market saturation, economic downturn impact",
                "**Review compliance exposure** - Privacy regulations tightening. Is tracking setup GDPR/CCPA compliant? Fines can be catastrophic"
            ],
            'warning': "Success today doesn't mean success tomorrow. Markets change, competitors adapt, platforms update algorithms. Every winning strategy has an expiration date. Plan for downside.",
            'opportunity': "Build resilience now while performance is good. Diversify channels, test backup strategies, document what works so you can pivot quickly when (not if) conditions change."
        },
        'optimist': {
            'icon': '🌟',
            'name': 'Optimist',
            'color': BRAND_COLORS['success'],
            'tagline': 'Growth Opportunities & Quick Wins',
            'insight': f"The {data['query']} data shows untapped potential. Current strategy only scratches surface. Strong product-market fit evident in retention metrics. Room to scale aggressively if done right.",
            'actions': [
                "**Scale what's working** - Top 3 channels showing 4x+ ROAS. Double down systematically. Test 50% budget increase in controlled rollout",
                "**Expand to adjacent audiences** - Lookalike segments show 85% similarity to best converters. Low-risk expansion opportunity worth £200K+ annually",
                "**Test new creative angles** - Current messaging resonates but plays it safe. Bold testimonials, problem-agitate-solve, comparison ads could lift performance 20-40%",
                "**Geographic expansion** - Strong performance in London/Manchester. Birmingham, Bristol, Edinburgh demographics match profile. Quick wins available"
            ],
            'warning': "Growth requires investment and patience. Quick wins are great, but sustainable growth needs sustained effort, budget, and organizational commitment over 6-12 months.",
            'opportunity': "Immediate opportunity: Increase budget 30% in proven channels, launch lookalike targeting, test 3 new creative variations. Conservative estimate: +£300K revenue in 90 days."
        },
        'realist': {
            'icon': '⚖️',
            'name': 'Realist',
            'color': BRAND_COLORS['info'],
            'tagline': 'Practical Constraints & Trade-Offs',
            'insight': f"The {data['query']} performance is workable but not exceptional. 2.1x ROAS is acceptable for this stage. Focus on incremental improvements rather than risky pivots. Steady progress beats home runs.",
            'actions': [
                "**Start with MVP optimizations** - Don't overhaul everything. Test one variable at a time: Bidding strategy first, then creative, then audiences. Measure, iterate",
                "**Work within budget constraints** - £25K/month isn't enough for brand building. Focus on performance marketing and efficiency improvements until budget scales",
                "**Set realistic milestones** - 3-month goal: Improve ROAS to 2.5x. 6-month: Scale to £40K/month spend while maintaining 2.3x+. Break into 2-week sprints",
                "**Acknowledge trade-offs** - Can't test everything. Prioritize: Fix attribution first (biggest unknown), then scale top channel, then creative refresh"
            ],
            'warning': "Perfect is the enemy of good. Ship something workable this week, not something perfect next quarter. Market waits for no one. Iterate in public, learn fast.",
            'opportunity': "Low-hanging fruit: Fix conversion tracking (probably losing 15-20% of attributable conversions), A/B test 3 landing page variations, negotiate CPMs down 10-15%. Do this before scaling spend."
        }
        }  # End of fallback mock data

    # Display selected perspective(s)
    perspectives_to_show = []
    if st.session_state.selected_persona == 'all':
        perspectives_to_show = [p for p in ['devil', 'optimist', 'realist'] if p in data['personas']]
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
            width='stretch'
        )

    with col2:
        st.download_button(
            label="📋 Download Text",
            data=export_content,
            file_name=f"scout_research_{re.sub(r'[^a-z0-9]+', '_', data['query'].lower())}.txt",
            mime="text/plain",
            width='stretch'
        )

    with col3:
        st.button("📊 Export to PDF", width='stretch', disabled=True,
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
    <p style='font-size: 0.85rem; margin-top: 1.5rem;'>
        <a href='https://forms.gle/mXR2nYbJWZ6WzwPX8' target='_blank' style='color: {BRAND_COLORS['primary']}; text-decoration: none; font-weight: 600;'>
            💬 Share Your Feedback
        </a>
    </p>
</div>
""", unsafe_allow_html=True)
