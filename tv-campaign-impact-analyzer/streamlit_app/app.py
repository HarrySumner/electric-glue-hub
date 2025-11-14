"""
Electric Glue TV Campaign Impact Analyzer
Streamlit Web Interface
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.branding import (
    BRAND_COLORS,
    CUSTOM_CSS,
    apply_electric_glue_theme,
    format_header,
    format_metric_card
)
from agents import (
    OrchestratorAgent,
    create_sample_data,
    WorkflowState
)

# Page configuration
st.set_page_config(
    page_title="TV Campaign Impact Analyzer | Electric Glue",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Electric Glue branding
apply_electric_glue_theme()

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False


def main():
    """Main application."""

    # Header
    st.markdown(format_header(
        "📺 TV Campaign Impact Analyzer",
        "Agentic AI for Television Advertising Attribution"
    ), unsafe_allow_html=True)

    st.markdown("""
    <div class="subtitle">
    Built by <strong>Electric Glue</strong> | Powered by Bayesian Causal Inference & Multi-Agent AI
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {BRAND_COLORS['primary']} 0%, {BRAND_COLORS['secondary']} 100%);
                    padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0;'>⚙️ Configuration</h2>
        </div>
        """, unsafe_allow_html=True)

        # Data upload
        st.subheader("📊 1. Data Input")

        use_sample = st.checkbox("Use sample data", value=True, help="Use built-in TV campaign sample data")

        uploaded_file = None
        if not use_sample:
            uploaded_file = st.file_uploader(
                "Upload CSV or Excel",
                type=['csv', 'xlsx', 'xls'],
                help="Upload your time series data with date, target metric, and optional covariates"
            )

        # Analysis configuration
        st.subheader("🎯 2. Analysis Settings")

        if use_sample or uploaded_file:
            # Load data preview
            if use_sample:
                sample_df = create_sample_data()
                st.caption(f"Sample data: {len(sample_df)} days of TV campaign data")

                # Set defaults for sample data
                date_col = 'date'
                target_col = 'bookings'
                covariate_cols = ['tv_spend', 'digital_spend', 'flights_available']

                # Show column names
                st.write("**Available columns:**")
                st.code(', '.join(sample_df.columns))

            else:
                # Load uploaded file
                if uploaded_file.name.endswith('.csv'):
                    sample_df = pd.read_csv(uploaded_file)
                else:
                    sample_df = pd.read_excel(uploaded_file)

                st.caption(f"Uploaded: {len(sample_df)} rows × {len(sample_df.columns)} columns")

                # Column selection
                date_col = st.selectbox("Date column", sample_df.columns, index=0)
                target_col = st.selectbox("Target metric", sample_df.columns,
                                         index=1 if len(sample_df.columns) > 1 else 0)

                # Covariate selection
                remaining_cols = [c for c in sample_df.columns if c not in [date_col, target_col]]
                covariate_cols = st.multiselect(
                    "Covariates (control variables)",
                    remaining_cols,
                    default=remaining_cols[:3] if len(remaining_cols) >= 3 else remaining_cols,
                    help="Select variables to control for confounders (e.g., other marketing, external factors)"
                )

            # Period selection
            st.subheader("📅 3. Campaign Periods")

            if use_sample:
                # Defaults for sample data
                pre_start = pd.to_datetime('2024-01-01')
                pre_end = pd.to_datetime('2024-07-18')
                post_start = pd.to_datetime('2024-07-19')
                post_end = pd.to_datetime('2024-12-31')
            else:
                # Convert date column to datetime
                sample_df[date_col] = pd.to_datetime(sample_df[date_col])
                min_date = sample_df[date_col].min()
                max_date = sample_df[date_col].max()

                col1, col2 = st.columns(2)
                with col1:
                    pre_start = st.date_input("Pre-period start", value=min_date)
                    pre_end = st.date_input("Pre-period end",
                                           value=min_date + timedelta(days=180))
                with col2:
                    post_start = st.date_input("Post-period start",
                                              value=min_date + timedelta(days=181))
                    post_end = st.date_input("Post-period end", value=max_date)

            # Business context
            st.subheader("💼 4. Business Context (Optional)")

            campaign_name = st.text_input("Campaign name", value="Nielsen Summer TV Campaign" if use_sample else "")
            campaign_budget = st.number_input("Campaign budget (£)", value=450000 if use_sample else 0, step=10000)
            industry = st.text_input("Industry", value="Travel & Leisure" if use_sample else "")

            # Run analysis button
            st.markdown("---")

            if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
                st.session_state.analysis_run = False  # Reset

                with st.spinner("Initializing agents..."):
                    # Initialize orchestrator
                    st.session_state.orchestrator = OrchestratorAgent(llm_provider='openai')

                    # Prepare business context
                    business_context = {
                        'campaign_name': campaign_name,
                        'campaign_budget': campaign_budget,
                        'target_metric_name': target_col,
                        'industry': industry
                    } if campaign_name else None

                    # Run analysis
                    if use_sample:
                        results = st.session_state.orchestrator.run_full_analysis(
                            data=sample_df,
                            target_col=target_col,
                            date_col=date_col,
                            covariate_cols=covariate_cols,
                            pre_period=(str(pre_start), str(pre_end)),
                            post_period=(str(post_start), str(post_end)),
                            intervention_date=str(post_start),
                            business_context=business_context,
                            auto_suggest=False
                        )
                    else:
                        # Save uploaded file temporarily
                        temp_path = f"temp_{uploaded_file.name}"
                        with open(temp_path, 'wb') as f:
                            f.write(uploaded_file.getvalue())

                        results = st.session_state.orchestrator.run_full_analysis(
                            file_path=temp_path,
                            target_col=target_col,
                            date_col=date_col,
                            covariate_cols=covariate_cols,
                            pre_period=(str(pre_start), str(pre_end)),
                            post_period=(str(post_start), str(post_end)),
                            intervention_date=str(post_start),
                            business_context=business_context,
                            auto_suggest=False
                        )

                    st.session_state.results = results
                    st.session_state.analysis_run = True

                st.success("✅ Analysis complete!")
                st.rerun()

    # Main content area
    if st.session_state.analysis_run and st.session_state.results:
        display_results(st.session_state.results, st.session_state.orchestrator)
    else:
        display_welcome()


def display_welcome():
    """Display welcome screen."""

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">🤖</div>
            <h3>Multi-Agent AI</h3>
            <p>5 specialized agents work together:</p>
            <ul>
                <li>Data Agent</li>
                <li>Validation Agent</li>
                <li>Analysis Agent</li>
                <li>Interpretation Agent</li>
                <li>Orchestrator</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">📊</div>
            <h3>Bayesian BSTS</h3>
            <p>Robust causal inference that avoids DID pitfalls:</p>
            <ul>
                <li>No geographic controls needed</li>
                <li>Handles confounders explicitly</li>
                <li>Uncertainty quantification</li>
                <li>Trend & seasonality modeling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">💡</div>
            <h3>Actionable Insights</h3>
            <p>Plain-English recommendations:</p>
            <ul>
                <li>Executive summaries</li>
                <li>ROI calculations</li>
                <li>Quality scoring</li>
                <li>Client-ready reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Why BSTS not DID
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Why Bayesian Structural Time Series (BSTS) instead of Difference-in-Differences (DID)?</h3>
        <p><strong>The Nielsen Problem:</strong> Regional TV campaigns often violate DID assumptions due to:</p>
        <ul>
            <li>🚨 <strong>Contaminated controls</strong>: Flight availability changes, economic shocks in "control" regions</li>
            <li>📡 <strong>Ad spillover</strong>: TV ads reach control regions via streaming, travel</li>
            <li>📈 <strong>Parallel trends violations</strong>: Regional differences in baseline trends</li>
        </ul>
        <p><strong>BSTS Solution:</strong> No need for geographic controls — builds synthetic counterfactual from pre-campaign data</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick start
    st.markdown("### 🚀 Quick Start")
    st.markdown("""
    1. **Use sample data** (checkbox in sidebar) or upload your own CSV/Excel
    2. **Configure periods**: Define pre-campaign and campaign periods
    3. **Add context** (optional): Campaign budget, industry
    4. **Run analysis**: Click the button and let the agents work!
    5. **Review results**: Get causal effect estimates, visualizations, and recommendations
    """)


def display_results(results, orchestrator):
    """Display analysis results."""

    if not results['success']:
        st.error(f"❌ Analysis failed: {', '.join(results['errors'])}")
        return

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Summary",
        "📈 Visualizations",
        "🔬 Diagnostics",
        "📄 Report"
    ])

    with tab1:
        display_summary_tab(results)

    with tab2:
        display_visualizations_tab(results, orchestrator)

    with tab3:
        display_diagnostics_tab(results)

    with tab4:
        display_report_tab(results, orchestrator)


def display_summary_tab(results):
    """Display summary tab."""

    interpretation = results['interpretation']
    causal_effect = results['analysis']['causal_effect']

    # Executive summary
    st.markdown("""
    <div class="result-box">
        <h2>📋 Executive Summary</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**{interpretation['executive_summary']}**")

    st.markdown("---")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(format_metric_card(
            "Average Effect",
            f"{causal_effect['average_effect']:,.0f}",
            f"[{causal_effect['average_effect_lower']:,.0f}, {causal_effect['average_effect_upper']:,.0f}]"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(format_metric_card(
            "Relative Lift",
            f"{causal_effect['relative_effect']*100:.1f}%",
            f"[{causal_effect['relative_effect_lower']*100:.1f}%, {causal_effect['relative_effect_upper']*100:.1f}%]"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(format_metric_card(
            "Cumulative Impact",
            f"{causal_effect['cumulative_effect']:,.0f}",
            f"[{causal_effect['cumulative_lower']:,.0f}, {causal_effect['cumulative_upper']:,.0f}]"
        ), unsafe_allow_html=True)

    with col4:
        significance = "✅ Significant" if causal_effect['p_value'] < 0.05 else "⚠️ Not Significant"
        st.markdown(format_metric_card(
            "Statistical Test",
            significance,
            f"p-value: {causal_effect['p_value']:.4f}"
        ), unsafe_allow_html=True)

    # Key findings
    st.markdown("### 💡 Key Findings")
    for finding in interpretation['key_findings']:
        st.markdown(f"- {finding}")

    st.markdown("---")

    # Recommendations
    st.markdown("### 🎯 Recommendations")
    for rec in interpretation['recommendations']:
        st.markdown(f"- {rec}")


def display_visualizations_tab(results, orchestrator):
    """Display visualizations tab."""

    st.markdown("### 📈 Causal Impact Visualization")

    # Get detailed results
    detailed = orchestrator.analysis_agent.get_detailed_results()

    # Create plotly figure
    fig = go.Figure()

    # Actual values
    fig.add_trace(go.Scatter(
        x=detailed['date'],
        y=detailed['actual'],
        name='Actual',
        line=dict(color=BRAND_COLORS['primary'], width=2),
        mode='lines'
    ))

    # Predicted (counterfactual)
    fig.add_trace(go.Scatter(
        x=detailed['date'],
        y=detailed['predicted'],
        name='Counterfactual',
        line=dict(color=BRAND_COLORS['secondary'], width=2, dash='dash'),
        mode='lines'
    ))

    fig.update_layout(
        title='Actual vs Counterfactual',
        xaxis_title='Date',
        yaxis_title='Target Metric',
        hovermode='x unified',
        height=500,
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Point-wise effects
    st.markdown("### 📊 Point-wise Causal Effects")

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=detailed['date'],
        y=detailed['point_effect'],
        name='Point Effect',
        fill='tozeroy',
        line=dict(color=BRAND_COLORS['accent'], width=2),
        fillcolor=f"rgba{tuple(list(int(BRAND_COLORS['accent'][i:i+2], 16) for i in (1, 3, 5)) + [0.3])}"
    ))

    fig2.add_hline(y=0, line_dash="dash", line_color="gray")

    fig2.update_layout(
        title='Causal Effect Over Time',
        xaxis_title='Date',
        yaxis_title='Effect Size',
        hovermode='x',
        height=400,
        template='plotly_white'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Cumulative effect
    st.markdown("### 📈 Cumulative Impact")

    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(
        x=detailed['date'],
        y=detailed['cumulative_effect'],
        name='Cumulative Effect',
        line=dict(color=BRAND_COLORS['success'], width=3),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(list(int(BRAND_COLORS['success'][i:i+2], 16) for i in (1, 3, 5)) + [0.2])}"
    ))

    fig3.update_layout(
        title='Cumulative Causal Impact',
        xaxis_title='Date',
        yaxis_title='Cumulative Effect',
        hovermode='x',
        height=400,
        template='plotly_white'
    )

    st.plotly_chart(fig3, use_container_width=True)


def display_diagnostics_tab(results):
    """Display diagnostics tab."""

    st.markdown("### 🔬 Model Diagnostics")

    diagnostics = results['analysis']['diagnostics']
    validation = results['validation']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Model Quality")
        st.metric("Overall Assessment", diagnostics['model_quality'])
        st.metric("MAPE (Mean Absolute % Error)", f"{diagnostics['pre_period_fit']['mape']:.2f}%")
        st.metric("R-squared", f"{diagnostics['pre_period_fit']['r_squared']:.3f}")
        st.metric("RMSE", f"{diagnostics['pre_period_fit']['rmse']:.2f}")

    with col2:
        st.markdown("#### Data Quality")
        score = validation['score']
        if score >= 80:
            quality_color = BRAND_COLORS['success']
            quality_label = "Excellent"
        elif score >= 60:
            quality_color = BRAND_COLORS['warning']
            quality_label = "Good"
        else:
            quality_color = BRAND_COLORS['danger']
            quality_label = "Needs Improvement"

        st.markdown(f"**Score:** <span style='color: {quality_color}; font-size: 24px; font-weight: bold;'>{score}/100</span> ({quality_label})", unsafe_allow_html=True)

        st.markdown("**Validation Checks:**")
        for check_name, check_result in validation['checks'].items():
            status = "✅" if check_result.get('passed') else "⚠️"
            st.write(f"{status} {check_name.replace('_', ' ').title()}")

    # Warnings
    if validation['warnings']:
        st.markdown("---")
        st.markdown("### ⚠️ Validation Warnings")
        for warning in validation['warnings']:
            st.warning(warning)

    # Recommendations from validation
    if validation['recommendations']:
        st.markdown("---")
        st.markdown("### 💡 Technical Recommendations")
        for rec in validation['recommendations']:
            st.info(rec)


def display_report_tab(results, orchestrator):
    """Display report tab."""

    st.markdown("### 📄 Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Markdown report
        md_report = orchestrator.get_report(format='markdown', include_technical=True)
        st.download_button(
            label="📥 Download Markdown Report",
            data=md_report,
            file_name=f"tv_impact_report_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:
        # HTML report
        html_report = orchestrator.get_report(format='html', include_technical=True)
        st.download_button(
            label="📥 Download HTML Report",
            data=html_report,
            file_name=f"tv_impact_report_{datetime.now().strftime('%Y%m%d')}.html",
            mime="text/html",
            use_container_width=True
        )

    with col3:
        # CSV results
        detailed = orchestrator.analysis_agent.get_detailed_results()
        csv = detailed.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Data",
            data=csv,
            file_name=f"tv_impact_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Preview markdown report
    st.markdown("---")
    st.markdown("### 📋 Report Preview (Markdown)")

    with st.expander("View Full Report", expanded=False):
        st.markdown(orchestrator.get_report(format='markdown', include_technical=True))


if __name__ == '__main__':
    main()
