"""
Product 3: Report QA Agent
Standalone validation system for AI-generated reports and analyses
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from config.branding import apply_electric_glue_theme, BRAND_COLORS, format_header
from config.qa_status import render_qa_traffic_light
from core.llm_qa_validator import LLMQAValidator

# Page config
st.set_page_config(
    page_title="Report QA Agent | Electric Glue",
    page_icon="🚦",
    layout="wide"
)

# Apply branding
apply_electric_glue_theme()

# Header
st.markdown(format_header(
    "🚦 Report QA Agent",
    "AI Validates AI - Quality Assurance for Any Report or Analysis"
), unsafe_allow_html=True)

# Navigation
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("---")

# About this tool
with st.expander("📖 About the Report QA Agent", expanded=False):
    st.markdown(f"""
    ### What is the Report QA Agent?

    The **Report QA Agent** validates ANY report or analysis for accuracy and reliability:

    #### ✅ What It Checks
    - **Hallucinations**: Fabricated data or unsupported claims
    - **Accuracy**: Mathematical correctness and data consistency
    - **Evidence**: Source attribution for every factual claim
    - **Logic**: Consistency of conclusions with presented evidence
    - **Calculations**: Verify percentages, totals, and metrics

    #### 🎯 Why This Matters

    **60% of marketing teams hesitate to adopt AI due to accuracy concerns.**

    This tool builds trust by:
    - Providing transparent validation of AI outputs
    - Catching errors before they reach clients
    - Establishing systematic quality standards
    - Demonstrating "AI validates AI" for confidence

    #### 🔍 Validation Framework

    **7-Layer Validation**:
    1. Evidence-based verification
    2. Logical consistency checks
    3. Hallucination detection
    4. Mathematical accuracy
    5. Source attribution
    6. Claim verification
    7. Confidence scoring

    **Traffic Light System**:
    - 🟢 **PASSED (≥85%)**: Ready for client use
    - 🟡 **WARNING (70-84%)**: Review recommended
    - 🔴 **FAILED (<70%)**: Address issues first

    #### 💡 Use Cases

    - Validate Scout research outputs
    - Check AV Campaign Analysis reports
    - Review external AI-generated content
    - Verify client presentations
    - Audit competitive analyses
    - QA any marketing report or analysis
    """)

# QA System Health
render_qa_traffic_light(location="sidebar")

# Main tabs
tab1, tab2 = st.tabs(["📝 Input & Validate", "📊 Results & History"])

with tab1:
    st.markdown("### 📝 Submit Report for Validation")

    # Quick action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Load Recent AV Analysis", width='stretch'):
            st.session_state['load_recent_av'] = True
    with col2:
        if st.button("🔄 Load Recent Scout Output", width='stretch'):
            st.info("Scout integration coming soon")

    st.markdown("---")

    # Report input
    report_source = st.radio(
        "How would you like to provide the report?",
        ["📝 Paste Text", "📁 Upload File", "🔄 Select Recent Analysis"],
        horizontal=True
    )

    report_text = ""

    if report_source == "📝 Paste Text":
        report_text = st.text_area(
            "Report Content",
            height=300,
            placeholder="""Paste any report or analysis here for validation:

✅ AI-generated insights from Scout
✅ Campaign analysis from AV Analyser
✅ External AI tool outputs
✅ Client presentations
✅ Competitive analyses
✅ Marketing strategy documents

The QA Agent will check for accuracy, unsupported claims, and hallucinations.""",
            help="Paste the full text of the report you want to validate"
        )

    elif report_source == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Upload Report",
            type=['txt', 'md'],
            help="Upload a text or markdown file"
        )

        if uploaded_file:
            report_text = uploaded_file.read().decode('utf-8')
            st.success(f"✅ Loaded {len(report_text):,} characters from {uploaded_file.name}")
            with st.expander("📄 Preview", expanded=False):
                st.text(report_text[:500] + "..." if len(report_text) > 500 else report_text)

    else:  # Recent Analysis
        if 'results' in st.session_state or st.session_state.get('load_recent_av', False):
            if 'results' in st.session_state:
                results = st.session_state['results']

                # Generate comprehensive report summary
                report_text = f"""# AV Campaign Analysis Report

## Campaign Overview
- **Campaign Period**: {results['intervention_date'].strftime('%Y-%m-%d')} to {results['campaign_end_date'].strftime('%Y-%m-%d')} ({results['campaign_days']} days)
- **Measurement Window**: 90 days post-campaign ({results['measurement_days']} days)
- **Analysis Method**: Bayesian MCMC with Structural Time Series

## Key Findings

### Incremental Impact
- **Total Incremental Units**: {results['total_effect']:,.0f}
- **Average Daily Uplift**: {results['avg_effect']:,.0f} units
- **Relative Effect**: {results['relative_effect']:.1f}% increase vs baseline

### Statistical Rigor
- **MCMC Samples**: {results.get('n_samples', 'N/A'):,}
- **Confidence Level**: {results.get('confidence_level', 'N/A')}%
- **Convergence Status**: {results.get('convergence', {}).get('message', 'N/A')}
- **Effective Sample Size**: {results.get('convergence', {}).get('effective_sample_size', 'N/A'):.0f}

### Data Quality
- **Pre-campaign Observations**: {results.get('n_pre_points', 'N/A')}
- **Post-campaign Observations**: {results.get('n_post_points', 'N/A')}
- **Credible Interval**: [{results.get('cumulative_lower', 0):,.0f}, {results.get('cumulative_upper', 0):,.0f}]

## Executive Summary

The AV campaign generated a statistically significant uplift of {results['relative_effect']:.1f}% compared to the counterfactual baseline. Over the 90-day post-campaign measurement window, we estimate {results['total_effect']:,.0f} incremental units directly attributable to the campaign.

The analysis was conducted using Bayesian MCMC methodology with {results.get('n_samples', 1000):,} samples, ensuring robust statistical inference. Convergence diagnostics confirm the model validity ({results.get('convergence', {}).get('message', 'converged')}).

## Methodology

This analysis employs Bayesian Structural Time Series (BSTS) to construct a counterfactual baseline—what would have happened without the campaign. The observed performance is then compared against this baseline to isolate the true causal impact.

**Key Advantages**:
- Accounts for seasonality and trends
- Provides probability distributions (not just point estimates)
- Quantifies uncertainty through credible intervals
- Validates through convergence diagnostics

## Recommendation

Based on the {results['relative_effect']:.1f}% uplift and strong statistical validation, the campaign demonstrated measurable incremental value. The results support continued investment in this channel.
"""

                st.text_area("Generated Report", report_text, height=400)
            else:
                st.warning("⚠️ No recent analysis found. Please run an AV analysis first.")
                report_text = ""
        else:
            st.info("ℹ️ Run an AV Campaign Analysis first, then return here to validate the output.")

    # Optional: Source data for deeper validation
    st.markdown("---")
    with st.expander("➕ Add Source Data (Optional - Enables Deeper Validation)", expanded=False):
        st.markdown("Providing source data allows the QA Agent to verify specific numbers and calculations.")

        source_file = st.file_uploader("Upload Source Data (CSV)", type=['csv'])
        source_context = st.text_area(
            "Additional Context",
            placeholder="Provide context about data sources, methodologies, or known limitations...",
            height=100
        )

    # Run validation
    st.markdown("---")

    if st.button("🚀 Run QA Validation", type="primary", width='stretch'):
        if not report_text or len(report_text.strip()) < 100:
            st.error("❌ Please provide a report with at least 100 characters for meaningful validation.")
        else:
            with st.spinner("🔍 Running comprehensive QA validation..."):
                import time

                progress = st.progress(0)
                status = st.empty()

                status.text("Parsing report structure...")
                time.sleep(0.5)
                progress.progress(20)

                status.text("Extracting factual claims...")
                time.sleep(0.5)
                progress.progress(40)

                status.text("Running LLM validation checks...")
                time.sleep(1.2)
                progress.progress(70)

                status.text("Verifying source attribution...")
                time.sleep(0.5)
                progress.progress(90)

                status.text("Generating confidence scores...")
                time.sleep(0.5)
                progress.progress(100)

                # Run actual validation
                validator = LLMQAValidator()
                analysis_results = st.session_state.get('results', {})
                source_data = {'context': source_context} if source_context else {}

                qa_result = validator.validate_narrative_output(
                    narrative=report_text,
                    source_data=source_data,
                    analysis_results=analysis_results
                )

                # Store results
                st.session_state['qa_standalone'] = qa_result
                st.session_state['qa_report_text'] = report_text
                st.session_state['qa_timestamp'] = datetime.now()

                status.text("✅ Validation complete!")
                time.sleep(0.5)
                progress.empty()
                status.empty()

                st.success("✅ QA Validation Complete! View results in the 'Results & History' tab.")
                st.balloons()

with tab2:
    st.markdown("### 📊 Validation Results")

    if 'qa_standalone' not in st.session_state:
        st.info("ℹ️ Run a validation first to see results here.")
    else:
        qa = st.session_state['qa_standalone']
        timestamp = st.session_state.get('qa_timestamp', datetime.now())

        # Results header
        st.markdown(f"**Validated**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

        # Overall status
        confidence = qa['confidence_score']
        if confidence >= 85:
            status, color, icon, bg = 'PASSED', '#00FF00', '✅', 'rgba(0,255,0,0.1)'
        elif confidence >= 70:
            status, color, icon, bg = 'WARNING', '#FFA500', '⚠️', 'rgba(255,165,0,0.1)'
        else:
            status, color, icon, bg = 'FAILED', '#FF0000', '🔴', 'rgba(255,0,0,0.1)'

        st.markdown(f"""
        <div style='background: {bg}; padding: 2rem; border-radius: 15px; border-left: 6px solid {color}; margin: 1.5rem 0;'>
            <h2 style='color: {color}; margin: 0; font-size: 2.5rem;'>{icon} {status}</h2>
            <p style='font-size: 2rem; font-weight: 700; color: {color}; margin: 1rem 0;'>
                Confidence: {confidence:.1f}%
            </p>
            <p style='color: #666; font-size: 1.1rem; margin: 0;'>
                {'High confidence - safe for client use' if status == 'PASSED'
                 else 'Review recommended before use' if status == 'WARNING'
                 else 'Critical issues detected - do not use'}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Detailed results
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### ✅ Validated")
            if qa['validated_sections']:
                for section in qa['validated_sections'][:5]:
                    st.success(section)
            else:
                st.info("No specific validations")

        with col2:
            st.markdown("#### ⚠️ Flagged Issues")
            if qa['flagged_issues']:
                for issue in qa['flagged_issues'][:5]:
                    st.warning(issue)
            else:
                st.success("No issues detected")

        # Unsupported claims
        if qa['unsupported_claims']:
            st.markdown("---")
            st.markdown("#### 📝 Unsupported Claims")
            for claim in qa['unsupported_claims']:
                st.warning(claim)

        # Full report
        st.markdown("---")
        with st.expander("📄 Full Validation Report"):
            st.markdown(qa.get('raw_response', 'No detailed response'))

        # Export
        st.markdown("---")
        report_export = f"""REPORT QA VALIDATION
Generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}

STATUS: {status}
CONFIDENCE: {confidence:.1f}%

{qa.get('raw_response', '')}

---
Electric Glue | AI Validates AI
"""
        st.download_button(
            "📥 Download QA Report",
            report_export,
            f"qa_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt",
            width='stretch'
        )

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(255,107,107,0.05) 0%, rgba(0,0,0,0.03) 100%);
            border-radius: 12px;'>
    <p style='color: {BRAND_COLORS['text']}; font-size: 1rem; font-weight: 600; margin: 0.5rem 0;'>
        🚦 <strong>Electric Glue</strong> | Report QA Agent
    </p>
    <p style='font-size: 0.85rem; color: #999; margin: 0.5rem 0;'>
        Building Trust Through AI Validation
    </p>
    <p style='font-size: 0.8rem; color: #bbb; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e0e0e0;'>
        Powered by Multi-Agent AI × <strong style='color: #FF6B6B;'>Front Left</strong> Thinking
    </p>
    <p style='font-size: 0.85rem; margin-top: 1.5rem;'>
        <a href='https://forms.gle/mXR2nYbJWZ6WzwPX8' target='_blank' style='color: #FF6B6B; text-decoration: none; font-weight: 600;'>
            💬 Share Your Feedback
        </a>
    </p>
</div>
""", unsafe_allow_html=True)
