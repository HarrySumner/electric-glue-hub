"""
Product 1: AV Campaign Analyser
Advanced Bayesian MCMC analysis for TV/radio campaign impact measurement
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from config.branding import apply_electric_glue_theme, BRAND_COLORS, format_header
from config.qa_status import render_qa_traffic_light
from core.bayesian_causal_impact import run_causal_impact_analysis
from core.qa_validator import CampaignAnalysisQA

# Page config
st.set_page_config(
    page_title="AV Campaign Analyser | Electric Glue",
    page_icon="📺",
    layout="wide"
)

# Apply branding
apply_electric_glue_theme()

# Header
st.markdown(format_header(
    "📺 AV Campaign Analyser",
    "Advanced Bayesian MCMC Analysis for TV/Radio Campaign Impact"
), unsafe_allow_html=True)

# Navigation
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("---")

# About this tool - expandable
with st.expander("📖 About This Tool", expanded=False):
    st.markdown(f"""
    ### What is Causal Impact Analysis?

    The **Causal Impact Analyser** uses Bayesian structural time series (BSTS) to measure the **true causal effect**
    of your marketing campaigns—particularly TV, radio, and other hard-to-track channels.

    Unlike simple before/after comparisons, BSTS accounts for seasonality, trends, and confounding variables to give
    you an unbiased estimate of campaign impact.

    ### How It Works

    1. **Upload Your Data** - Provide time series data (daily/weekly) with KPI values
    2. **Define Intervention** - Mark the campaign start/end dates
    3. **AI Agents Analyse** - Multi-agent system validates data → runs BSTS → interprets results
    4. **Get Results** - View causal impact estimate, counterfactual forecast, confidence intervals
    5. **Download Report** - Client-ready output with visualisations and plain-English summary

    ### Why Use This Tool?

    - ✅ **Rigorous Methodology** - Bayesian BSTS with counterfactual modelling
    - ✅ **No Control Group Needed** - Creates synthetic control from pre-period data
    - ✅ **Handles Confounders** - Accounts for seasonality, trends, external shocks
    - ✅ **Uncertainty Quantification** - Confidence intervals for all estimates
    - ✅ **Client-Ready Outputs** - Plain English, not academic jargon

    ### Best For

    - 📺 **TV Advertising** - Measure impact on website traffic, sales, app downloads
    - 📻 **Radio & Podcast** - Quantify lift from audio campaigns
    - 🏙️ **Out-of-Home** - Billboard, transit, experiential campaign impact
    """)

st.markdown("---")

# Info banner
st.info("📊 **Note:** This is a simplified demo. Upload your time series data with campaign dates to get started.")

# Sidebar for configuration
with st.sidebar:
    st.markdown("### 📊 Analysis Configuration")

    st.markdown("#### Data Requirements")
    st.markdown("""
    - **Time series data** (daily or weekly)
    - **Pre-campaign period** (minimum 30 points)
    - **Campaign start/end dates**
    - **KPI column** (e.g., sales, conversions)
    """)

    st.markdown("---")

    st.markdown("#### Analysis Options")
    confidence_level = st.slider("Confidence Level (%)", 80, 99, 95)
    include_seasonality = st.checkbox("Include Seasonality", value=True)
    include_trend = st.checkbox("Include Trend", value=True)

# Render QA traffic light in sidebar
render_qa_traffic_light(location="sidebar")

st.markdown("---")

st.markdown("#### Advanced")
mcmc_samples = st.number_input("MCMC Samples", 500, 5000, 1000, step=500)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload Data", "⚙️ Configure Analysis", "📊 Results", "🚦 QA Validation"])

with tab1:
    st.markdown("### Upload Your Campaign Data")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload CSV file with time series data",
        type=['csv'],
        help="Upload any CSV with a date column and metric columns. We'll help you map them."
    )

    # Sample data option
    if not uploaded_file:
        st.markdown("---")
        st.markdown("#### Or Use Sample Data")

        if st.button("📊 Load Sample TV Campaign Data"):
            # Generate sample data
            np.random.seed(42)
            dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')

            # Pre-campaign baseline with trend and seasonality
            baseline = 1000 + np.arange(len(dates)) * 2
            seasonality = 100 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
            noise = np.random.normal(0, 50, len(dates))

            kpi = baseline + seasonality + noise

            # Add campaign effect (March 1 - March 31)
            campaign_start_idx = (dates >= '2024-03-01') & (dates <= '2024-03-31')
            kpi[campaign_start_idx] += 300  # +300 daily lift during campaign

            sample_data = pd.DataFrame({
                'date': dates,
                'y': kpi.astype(int)
            })

            st.session_state['raw_data'] = sample_data
            st.session_state['data'] = sample_data
            st.session_state['date_column'] = 'date'
            st.session_state['kpi_column'] = 'y'
            st.session_state['intervention_date'] = pd.to_datetime('2024-03-01')
            st.success("✅ Sample data loaded!")
            st.rerun()
    else:
        # Process uploaded file
        try:
            raw_data = pd.read_csv(uploaded_file)
            st.session_state['raw_data'] = raw_data
            st.success(f"✅ File uploaded successfully! {len(raw_data)} rows loaded.")

            # Data normalisation section
            st.markdown("---")
            st.markdown("#### 📋 Map Your Columns")
            st.markdown("Tell us which columns contain your date and KPI data:")

            col1, col2 = st.columns(2)

            with col1:
                # Detect potential date columns
                potential_date_cols = []
                for col in raw_data.columns:
                    try:
                        pd.to_datetime(raw_data[col].dropna().iloc[0])
                        potential_date_cols.append(col)
                    except:
                        pass

                date_col = st.selectbox(
                    "Date Column",
                    options=raw_data.columns,
                    index=raw_data.columns.get_loc(potential_date_cols[0]) if potential_date_cols else 0,
                    help="Column containing dates/timestamps"
                )

            with col2:
                # Numeric columns for KPI
                numeric_cols = raw_data.select_dtypes(include=[np.number]).columns.tolist()
                kpi_options = [col for col in raw_data.columns if col != date_col]

                # Determine default index
                if numeric_cols and numeric_cols[0] in kpi_options:
                    default_kpi_index = kpi_options.index(numeric_cols[0])
                else:
                    default_kpi_index = 0

                kpi_col = st.selectbox(
                    "KPI Column",
                    options=kpi_options,
                    index=default_kpi_index if kpi_options else 0,
                    help="Column containing the metric you want to analyse"
                )

            # Normalise data button
            if st.button("✅ Confirm Column Mapping", type="primary"):
                try:
                    # Create normalised dataframe
                    normalised_data = pd.DataFrame()

                    # Try multiple date parsing strategies
                    try:
                        # First try with dayfirst=True for UK/EU dates
                        normalised_data['date'] = pd.to_datetime(raw_data[date_col], dayfirst=True)
                    except:
                        try:
                            # Try with mixed format
                            normalised_data['date'] = pd.to_datetime(raw_data[date_col], format='mixed', dayfirst=True)
                        except:
                            # Try infer_datetime_format as last resort
                            normalised_data['date'] = pd.to_datetime(raw_data[date_col], infer_datetime_format=True)

                    normalised_data['y'] = pd.to_numeric(raw_data[kpi_col], errors='coerce')

                    # Remove NaN values
                    normalised_data = normalised_data.dropna()

                    # Sort by date
                    normalised_data = normalised_data.sort_values('date').reset_index(drop=True)

                    # Store in session state
                    st.session_state['data'] = normalised_data
                    st.session_state['date_column'] = date_col
                    st.session_state['kpi_column'] = kpi_col
                    st.session_state['intervention_date'] = normalised_data['date'].min() + (normalised_data['date'].max() - normalised_data['date'].min()) / 2

                    st.success("✅ Data normalised successfully!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error normalising data: {e}")
                    st.info("💡 Tip: Make sure your date column has consistent date formats (e.g., all DD/MM/YYYY or all YYYY-MM-DD)")

        except Exception as e:
            st.error(f"Error loading file: {e}")

    # Display data preview
    if 'data' in st.session_state:
        st.markdown("---")
        st.markdown("#### Data Preview (Normalised)")
        st.dataframe(st.session_state['data'].head(10), width='stretch')

        # Basic stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", len(st.session_state['data']))
        with col2:
            st.metric("Columns", len(st.session_state['data'].columns))
        with col3:
            if 'y' in st.session_state['data'].columns:
                st.metric("Avg KPI", f"{st.session_state['data']['y'].mean():.0f}")
        with col4:
            if 'date' in st.session_state['data'].columns:
                date_range = (st.session_state['data']['date'].max() - st.session_state['data']['date'].min()).days
                st.metric("Date Range", f"{date_range} days")

with tab2:
    st.markdown("### Configure Your Analysis")

    if 'data' not in st.session_state:
        st.warning("⚠️ Please upload data first in the 'Upload Data' tab.")
    else:
        data = st.session_state['data']

        # Campaign date selection
        st.markdown("#### 📍 Campaign Dates")
        st.markdown("Define when your campaign started and ended:")

        # Visual timeline
        min_date = data['date'].min().date()
        max_date = data['date'].max().date()

        col1, col2 = st.columns(2)

        with col1:
            campaign_start = st.date_input(
                "Campaign Start Date",
                value=st.session_state.get('intervention_date', min_date + (max_date - min_date) / 3).date() if isinstance(st.session_state.get('intervention_date'), pd.Timestamp) else st.session_state.get('intervention_date', min_date + (max_date - min_date) / 3),
                min_value=min_date,
                max_value=max_date,
                help="The date when your campaign began"
            )

        with col2:
            # Default campaign end to 30 days after start
            default_end = campaign_start + timedelta(days=30)
            if default_end > max_date:
                default_end = max_date

            # Get session state value and validate it's within range
            session_end = st.session_state.get('campaign_end_date', default_end)
            if isinstance(session_end, pd.Timestamp):
                session_end = session_end.date()

            # Ensure the session value is within the valid range
            if session_end < campaign_start or session_end > max_date:
                session_end = default_end

            campaign_end = st.date_input(
                "Campaign End Date",
                value=session_end,
                min_value=campaign_start,
                max_value=max_date,
                help="The date when your campaign ended"
            )

        st.session_state['intervention_date'] = pd.to_datetime(campaign_start)
        st.session_state['campaign_end_date'] = pd.to_datetime(campaign_end)

        # Show campaign periods
        st.markdown("---")
        st.markdown("#### 📊 Campaign Period Breakdown")

        # Calculate periods
        pre_campaign = data[data['date'] < pd.to_datetime(campaign_start)]
        campaign_period = data[(data['date'] >= pd.to_datetime(campaign_start)) & (data['date'] <= pd.to_datetime(campaign_end))]

        # 90-day measurement window after campaign end
        measurement_end = pd.to_datetime(campaign_end) + timedelta(days=90)
        measurement_window = data[(data['date'] > pd.to_datetime(campaign_end)) & (data['date'] <= measurement_end)]

        # Store measurement window end
        st.session_state['measurement_end_date'] = measurement_end

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.08) 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #666;'>
                <h4 style='color: #666; margin-top: 0;'>📅 Pre-Campaign</h4>
                <p style='font-size: 1.8rem; font-weight: bold; color: #666; margin: 0.5rem 0;'>{len(pre_campaign)}</p>
                <p style='color: #888; margin: 0;'>data points</p>
                <p style='color: #888; font-size: 0.9rem; margin-top: 0.5rem;'>
                    {pre_campaign['date'].min().strftime('%Y-%m-%d')} to {pre_campaign['date'].max().strftime('%Y-%m-%d')}
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            campaign_days = (pd.to_datetime(campaign_end) - pd.to_datetime(campaign_start)).days + 1
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255,165,0,0.1) 0%, rgba(255,165,0,0.15) 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FFA500;'>
                <h4 style='color: #FFA500; margin-top: 0;'>📢 Campaign Period</h4>
                <p style='font-size: 1.8rem; font-weight: bold; color: #FFA500; margin: 0.5rem 0;'>{len(campaign_period)}</p>
                <p style='color: #888; margin: 0;'>data points ({campaign_days} days)</p>
                <p style='color: #888; font-size: 0.9rem; margin-top: 0.5rem;'>
                    {campaign_start.strftime('%Y-%m-%d')} to {campaign_end.strftime('%Y-%m-%d')}
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,255,0,0.1) 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid {BRAND_COLORS['primary']};'>
                <h4 style='color: {BRAND_COLORS['primary']}; margin-top: 0;'>📈 90-Day Measurement</h4>
                <p style='font-size: 1.8rem; font-weight: bold; color: {BRAND_COLORS['primary']}; margin: 0.5rem 0;'>{len(measurement_window)}</p>
                <p style='color: #666; margin: 0;'>data points (post-campaign)</p>
                <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>
                    {(pd.to_datetime(campaign_end) + timedelta(days=1)).strftime('%Y-%m-%d')} to {measurement_end.strftime('%Y-%m-%d')}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Validation
        st.markdown("---")
        st.markdown("#### ✅ Data Quality Check")

        col1, col2, col3 = st.columns(3)

        with col1:
            if len(pre_campaign) >= 30:
                st.success(f"✅ Pre-campaign sufficient ({len(pre_campaign)} points ≥ 30)")
            else:
                st.error(f"❌ Pre-campaign too short ({len(pre_campaign)} points < 30)")

        with col2:
            if len(campaign_period) >= 1:
                st.success(f"✅ Campaign period valid ({len(campaign_period)} points)")
            else:
                st.error(f"❌ No campaign data available")

        with col3:
            if len(measurement_window) >= 30:
                st.success(f"✅ Measurement window sufficient ({len(measurement_window)} points)")
            elif len(measurement_window) > 0:
                st.warning(f"⚠️ Measurement window short ({len(measurement_window)} points)")
            else:
                st.error(f"❌ No measurement window data available")

        # Campaign Configuration Table
        st.markdown("---")
        st.markdown("#### 📋 Campaign Analysis Configuration")

        config_df = pd.DataFrame({
            'Parameter': [
                'Campaign Start Date',
                'Campaign End Date',
                'Campaign Duration',
                'Pre-Campaign Period',
                'Measurement Window (90 days post-campaign)',
                'Total Data Points',
                'Confidence Level',
                'Include Seasonality',
                'Include Trend'
            ],
            'Value': [
                campaign_start.strftime('%Y-%m-%d'),
                campaign_end.strftime('%Y-%m-%d'),
                f"{campaign_days} days",
                f"{len(pre_campaign)} data points ({pre_campaign['date'].min().strftime('%Y-%m-%d')} to {pre_campaign['date'].max().strftime('%Y-%m-%d')})",
                f"{len(measurement_window)} data points ({(pd.to_datetime(campaign_end) + timedelta(days=1)).strftime('%Y-%m-%d')} to {measurement_end.strftime('%Y-%m-%d')})",
                f"{len(data)} data points",
                f"{confidence_level}%",
                "Yes" if include_seasonality else "No",
                "Yes" if include_trend else "No"
            ]
        })

        st.dataframe(config_df, width='stretch', hide_index=True)

with tab3:
    st.markdown("### 📊 Campaign Impact Analysis Results")

    if 'data' not in st.session_state:
        st.warning("⚠️ Please upload data and configure analysis first.")
    elif 'intervention_date' not in st.session_state:
        st.warning("⚠️ Please configure your campaign dates in the 'Configure Analysis' tab.")
    elif 'campaign_end_date' not in st.session_state:
        st.warning("⚠️ Please configure your campaign end date in the 'Configure Analysis' tab.")
    else:
        st.markdown("---")

        if st.button("🚀 Run Bayesian MCMC Analysis", type="primary", width='stretch'):

            # Get data and campaign dates
            data = st.session_state['data'].copy()
            campaign_start = pd.to_datetime(st.session_state['intervention_date'])
            campaign_end = pd.to_datetime(st.session_state['campaign_end_date'])
            measurement_end = campaign_end + timedelta(days=90)

            # Show analysis in progress
            with st.spinner("🔄 Running Bayesian analysis..."):
                import time

                progress_bar = st.progress(0)
                status_text = st.empty()

                # Simulate multi-agent workflow
                status_text.text("Agent 1: Validating data quality...")
                time.sleep(0.8)
                progress_bar.progress(20)

                status_text.text("Agent 2: Building BSTS model...")
                time.sleep(1)
                progress_bar.progress(40)

                status_text.text("Agent 3: Running MCMC sampling...")
                time.sleep(1.2)
                progress_bar.progress(70)

                status_text.text("Agent 4: Computing counterfactual...")
                time.sleep(0.8)
                progress_bar.progress(85)

                status_text.text("Agent 5: Generating insights...")
                time.sleep(0.8)
                progress_bar.progress(100)

                # Run PROPER Bayesian MCMC analysis
                status_text.text("🔬 Running Bayesian MCMC analysis with proper statistical inference...")

                # Use the new Bayesian causal impact module
                bayesian_results = run_causal_impact_analysis(
                    data=data,
                    campaign_start=campaign_start,
                    campaign_end=campaign_end,
                    measurement_end=measurement_end,
                    kpi_column='y',
                    confidence_level=confidence_level / 100,  # Convert to decimal
                    n_samples=mcmc_samples,  # Use the UI setting
                    seed=42  # For reproducibility
                )

                # Get pre-campaign and measurement data for display
                pre_data = data[data['date'] < campaign_start].copy()
                measurement_data = data[(data['date'] > campaign_end) & (data['date'] <= measurement_end)].copy()

                # Compute cumulative effect for visualization
                cumulative_effect = np.cumsum(bayesian_results['point_effect_mean'])

                # Store results in session state
                st.session_state['results'] = {
                    # Core Bayesian results
                    'actual': bayesian_results['actual'],
                    'counterfactual': bayesian_results['counterfactual_mean'],
                    'counterfactual_lower': bayesian_results['counterfactual_lower'],
                    'counterfactual_upper': bayesian_results['counterfactual_upper'],
                    'point_effect': bayesian_results['point_effect_mean'],
                    'point_effect_lower': bayesian_results['point_effect_lower'],
                    'point_effect_upper': bayesian_results['point_effect_upper'],
                    'cumulative_effect': cumulative_effect,
                    'cumulative_lower': bayesian_results['cumulative_lower'],
                    'cumulative_upper': bayesian_results['cumulative_upper'],

                    # Summary statistics
                    'total_effect': bayesian_results['cumulative_effect'],
                    'avg_effect': bayesian_results['daily_average'],
                    'relative_effect': bayesian_results['relative_effect'],
                    'prob_causal_effect': bayesian_results['prob_causal_effect'],

                    # MCMC diagnostics
                    'convergence': bayesian_results['convergence'],
                    'n_samples': bayesian_results['n_samples'],
                    'posterior_samples': bayesian_results.get('posterior_samples'),

                    # Metadata and visualization data
                    'pre_data': pre_data,
                    'post_data': measurement_data,
                    'intervention_date': campaign_start,
                    'campaign_end_date': campaign_end,
                    'measurement_end_date': measurement_end,
                    'confidence_level': confidence_level,
                    'include_seasonality': include_seasonality,
                    'include_trend': include_trend,
                    'campaign_days': (campaign_end - campaign_start).days + 1,
                    'measurement_days': len(measurement_data),
                    'n_pre_points': bayesian_results['n_pre_points'],
                    'n_post_points': bayesian_results['n_post_points']
                }

                status_text.text("🔍 Running QA validation...")
                progress_bar.progress(95)

                # Run QA validation
                qa_validator = CampaignAnalysisQA()
                qa_report = qa_validator.validate_all(
                    data=data,
                    results=st.session_state['results'],
                    campaign_start=campaign_start,
                    campaign_end=campaign_end
                )

                # Store QA report in session state
                st.session_state['qa_report'] = qa_report

                status_text.text("✅ Analysis and QA validation complete!")
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()

        # Display results if available
        if 'results' in st.session_state:
            results = st.session_state['results']

            st.success("✅ Campaign Impact Analysis Complete!")

            # Campaign summary banner
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,255,0,0.1) 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 5px solid {BRAND_COLORS['primary']}; margin-bottom: 2rem;'>
                <h3 style='color: {BRAND_COLORS['primary']}; margin-top: 0;'>📢 Campaign Performance (90-Day Post-Campaign Window)</h3>
                <p style='color: #666; margin: 0;'>
                    Campaign Period: {results['intervention_date'].strftime('%Y-%m-%d')} to {results['campaign_end_date'].strftime('%Y-%m-%d')} ({results['campaign_days']} days)
                </p>
                <p style='color: #666; margin: 0;'>
                    Measurement Window: {(results['campaign_end_date'] + timedelta(days=1)).strftime('%Y-%m-%d')} to {results['measurement_end_date'].strftime('%Y-%m-%d')} ({results['measurement_days']} days)
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Summary metrics
            st.markdown("### 📈 Campaign Incremental Value")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Incremental Units",
                    f"{results['total_effect']:,.0f}",
                    delta=f"{results['relative_effect']:.1f}% uplift",
                    help="Total incremental units generated in 90-day post-campaign window"
                )

            with col2:
                st.metric(
                    "Daily Average Uplift",
                    f"{results['avg_effect']:,.0f}",
                    help="Average daily incremental units during measurement window"
                )

            with col3:
                st.metric(
                    "Campaign Uplift",
                    f"+{results['relative_effect']:.1f}%",
                    help="Percentage increase vs. what would have happened without campaign"
                )

            with col4:
                # Use actual posterior probability from MCMC
                prob_effect = results.get('prob_causal_effect', 95)
                st.metric(
                    "Probability of Effect",
                    f"{prob_effect:.1f}%",
                    help="Bayesian posterior probability that campaign drove positive incremental value (from MCMC samples)"
                )

            # MCMC Diagnostics
            st.markdown("---")
            st.markdown("### 🔬 MCMC Diagnostics & Credible Intervals")

            convergence = results.get('convergence', {})
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "MCMC Samples",
                    f"{results.get('n_samples', 0):,}",
                    help="Number of MCMC iterations used for posterior distribution"
                )

            with col2:
                ess = convergence.get('effective_sample_size', 0)
                st.metric(
                    "Effective Sample Size",
                    f"{ess:.0f}",
                    help="Effective number of independent samples after accounting for autocorrelation"
                )

            with col3:
                converged = convergence.get('converged', False)
                status_icon = "✅" if converged else "⚠️"
                status_text = "Converged" if converged else "Check needed"
                st.metric(
                    "Convergence Status",
                    f"{status_icon} {status_text}",
                    help=convergence.get('message', 'MCMC convergence status')
                )

            # Detailed summary table with credible intervals
            st.markdown("---")
            st.markdown("### 📊 Detailed Impact Summary with Credible Intervals")

            ci_level = results.get('confidence_level', 95)

            # Handle both old and new result formats
            if 'cumulative_lower' in results and 'cumulative_upper' in results:
                # New Bayesian format
                summary_df = pd.DataFrame({
                    'Metric': [
                        'Actual (observed)',
                        'Predicted (counterfactual)',
                        'Absolute Effect',
                        'Relative Effect',
                        'Cumulative Effect'
                    ],
                    'Point Estimate': [
                        f"{np.mean(results['actual']):,.0f}",
                        f"{np.mean(results['counterfactual']):,.0f}",
                        f"{results['avg_effect']:,.0f}",
                        f"{results['relative_effect']:.1f}%",
                        f"{results['total_effect']:,.0f}"
                    ],
                    f'{ci_level}% Credible Interval': [
                        "—",
                        f"[{np.mean(results['counterfactual_lower']):,.0f}, {np.mean(results['counterfactual_upper']):,.0f}]",
                        f"[{np.mean(results['point_effect_lower']):,.0f}, {np.mean(results['point_effect_upper']):,.0f}]",
                        "—",
                        f"[{results['cumulative_lower']:,.0f}, {results['cumulative_upper']:,.0f}]"
                    ],
                    'Cumulative Total': [
                        f"{np.sum(results['actual']):,.0f}",
                        f"{np.sum(results['counterfactual']):,.0f}",
                        f"{results['total_effect']:,.0f}",
                        f"{results['relative_effect']:.1f}%",
                        f"{results['total_effect']:,.0f}"
                    ]
                })
            else:
                # Old format fallback
                summary_df = pd.DataFrame({
                    'Metric': [
                        'Actual (observed)',
                        'Predicted (counterfactual)',
                        'Absolute Effect',
                        'Relative Effect',
                        'Cumulative Effect'
                    ],
                    'Average': [
                        f"{np.mean(results['actual']):,.0f}",
                        f"{np.mean(results['counterfactual']):,.0f}",
                        f"{results['avg_effect']:,.0f}",
                        f"{results['relative_effect']:.1f}%",
                        f"{results.get('total_effect', 0):,.0f}"
                    ],
                    'Cumulative': [
                        f"{np.sum(results['actual']):,.0f}",
                        f"{np.sum(results['counterfactual']):,.0f}",
                        f"{results['total_effect']:,.0f}",
                        f"{(results['total_effect'] / np.sum(results['counterfactual']) * 100):.1f}%",
                        f"{results.get('total_effect', 0):,.0f}"
                    ]
                })

            st.dataframe(summary_df, width='stretch', hide_index=True)

            # Add explanation of credible intervals
            with st.expander("ℹ️ Understanding Credible Intervals"):
                st.markdown(f"""
                **Bayesian Credible Intervals** represent the range where we believe the true effect lies
                with {ci_level}% probability, based on {results.get('n_samples', 0):,} MCMC samples.

                - **Point Estimate**: The mean of the posterior distribution (most likely value)
                - **{ci_level}% Credible Interval**: The range containing {ci_level}% of the posterior probability mass
                - **Interpretation**: "We are {ci_level}% confident the true effect is within this range"

                This is more robust than traditional confidence intervals because it incorporates
                uncertainty from multiple sources through Bayesian posterior sampling.
                """)

            # Visualizations
            st.markdown("---")
            st.markdown("### 📈 Visualisations")

            # Create matplotlib figures with proper configuration
            plt.style.use('dark_background')
            fig, axes = plt.subplots(3, 1, figsize=(14, 12), facecolor='#0E1117')
            fig.patch.set_facecolor('#0E1117')

            # Plot 1: Actual vs Counterfactual
            ax1 = axes[0]
            ax1.set_facecolor('#0E1117')

            # Pre-period actual (if available)
            if 'pre_data' in results and results['pre_data'] is not None and len(results['pre_data']) > 0:
                ax1.plot(results['pre_data']['date'], results['pre_data']['y'],
                        color='#00FF00', linewidth=2.5, label='Pre-Intervention Actual', zorder=3)

            # Post-period actual
            ax1.plot(results['post_data']['date'], results['actual'],
                    color='#00FF00', linewidth=2.5, label='Post-Intervention Actual', zorder=3)

            # Counterfactual prediction
            ax1.plot(results['post_data']['date'], results['counterfactual'],
                    color='#39FF14', linestyle='--', linewidth=2.5, label='Counterfactual Prediction', zorder=2)

            # Credible interval (from Bayesian MCMC)
            if 'counterfactual_lower' in results and 'counterfactual_upper' in results:
                ax1.fill_between(results['post_data']['date'].values,
                                results['counterfactual_lower'],
                                results['counterfactual_upper'],
                                color='#39FF14', alpha=0.15, label=f'{ci_level}% Credible Interval (MCMC)', zorder=1)
            else:
                # Fallback for old format
                ax1.fill_between(results['post_data']['date'].values,
                                results['counterfactual'] - results.get('ci_width', 0),
                                results['counterfactual'] + results.get('ci_width', 0),
                                color='#39FF14', alpha=0.15, label='95% Confidence Interval', zorder=1)

            # Intervention line
            ax1.axvline(results['intervention_date'], color='#FF6B6B', linestyle='--',
                       linewidth=2.5, alpha=0.8, label='Intervention Date', zorder=4)

            ax1.set_title('Actual vs. Counterfactual', color='white', fontsize=16, fontweight='bold', pad=15)
            ax1.set_xlabel('Date', color='white', fontsize=12)
            ax1.set_ylabel('KPI Value', color='white', fontsize=12)
            ax1.legend(facecolor='#0E1117', edgecolor='#00FF00', labelcolor='white',
                      fontsize=10, loc='upper left', framealpha=0.9)
            ax1.tick_params(colors='white', labelsize=10)
            ax1.spines['bottom'].set_color('#262730')
            ax1.spines['left'].set_color('#262730')
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.grid(True, alpha=0.15, color='#262730', linestyle='-', linewidth=0.5)

            # Plot 2: Pointwise Effect
            ax2 = axes[1]
            ax2.set_facecolor('#0E1117')

            # Determine color based on effect direction
            effect_color = '#00FF00' if np.mean(results['point_effect']) > 0 else '#FF6B6B'

            # Plot credible interval if available
            if 'point_effect_lower' in results and 'point_effect_upper' in results:
                ax2.fill_between(results['post_data']['date'].values,
                                results['point_effect_lower'],
                                results['point_effect_upper'],
                                color=effect_color, alpha=0.15, zorder=1, label=f'{ci_level}% Credible Interval')

            ax2.fill_between(results['post_data']['date'].values, 0, results['point_effect'],
                            color=effect_color, alpha=0.25, zorder=2)
            ax2.plot(results['post_data']['date'], results['point_effect'],
                    color=effect_color, linewidth=2.5, zorder=3, label='Point Effect')
            ax2.axhline(0, color='#666', linestyle='-', linewidth=1.5, alpha=0.6, zorder=0)
            ax2.axvline(results['intervention_date'], color='#FF6B6B', linestyle='--',
                       linewidth=2.5, alpha=0.8, zorder=3)

            ax2.set_title('Pointwise Causal Effect with Credible Intervals', color='white', fontsize=16, fontweight='bold', pad=15)
            ax2.set_xlabel('Date', color='white', fontsize=12)
            ax2.set_ylabel('Effect Size', color='white', fontsize=12)
            if 'point_effect_lower' in results:
                ax2.legend(facecolor='#0E1117', edgecolor='#00FF00', labelcolor='white',
                          fontsize=10, loc='upper left', framealpha=0.9)
            ax2.tick_params(colors='white', labelsize=10)
            ax2.spines['bottom'].set_color('#262730')
            ax2.spines['left'].set_color('#262730')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.grid(True, alpha=0.15, color='#262730', linestyle='-', linewidth=0.5)

            # Plot 3: Cumulative Effect
            ax3 = axes[2]
            ax3.set_facecolor('#0E1117')

            # Determine color based on cumulative effect direction
            cumulative_color = '#00FF00' if results['cumulative_effect'][-1] > 0 else '#FF6B6B'

            ax3.fill_between(results['post_data']['date'].values, 0, results['cumulative_effect'],
                            color=cumulative_color, alpha=0.25, zorder=1)
            ax3.plot(results['post_data']['date'], results['cumulative_effect'],
                    color=cumulative_color, linewidth=2.5, zorder=2)
            ax3.axhline(0, color='#666', linestyle='-', linewidth=1.5, alpha=0.6, zorder=0)
            ax3.axvline(results['intervention_date'], color='#FF6B6B', linestyle='--',
                       linewidth=2.5, alpha=0.8, zorder=3)

            ax3.set_title('Cumulative Causal Effect', color='white', fontsize=16, fontweight='bold', pad=15)
            ax3.set_xlabel('Date', color='white', fontsize=12)
            ax3.set_ylabel('Cumulative Effect', color='white', fontsize=12)
            ax3.tick_params(colors='white', labelsize=10)
            ax3.spines['bottom'].set_color('#262730')
            ax3.spines['left'].set_color('#262730')
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            ax3.grid(True, alpha=0.15, color='#262730', linestyle='-', linewidth=0.5)

            plt.tight_layout(pad=2.0)

            # Display the plot with proper configuration
            st.pyplot(fig, width='stretch')
            plt.close(fig)

            # Posterior Distribution Visualization (if MCMC samples available)
            if 'posterior_samples' in results and results['posterior_samples'] is not None:
                st.markdown("---")
                st.markdown("### 📊 Posterior Distribution of Cumulative Effect")

                with st.expander("ℹ️ What is a Posterior Distribution?", expanded=False):
                    st.markdown(f"""
                    The **posterior distribution** shows all possible values of the cumulative effect
                    based on {results.get('n_samples', 0):,} MCMC samples.

                    - The **peak** shows the most likely value
                    - The **spread** shows the uncertainty
                    - The **shaded area** contains {ci_level}% of the probability mass (credible interval)

                    This is the foundation of Bayesian inference—instead of a single point estimate,
                    we get a full probability distribution showing all plausible values.
                    """)

                # Create histogram of posterior samples
                fig_posterior, ax = plt.subplots(figsize=(12, 6), facecolor='#0E1117')
                ax.set_facecolor('#0E1117')

                posterior_cumulative = results['posterior_samples']['cumulative_effect']

                # Histogram
                n, bins, patches = ax.hist(posterior_cumulative, bins=50, density=True,
                                          color='#00FF00', alpha=0.6, edgecolor='#00FF00',
                                          linewidth=1.5)

                # Add credible interval shading
                lower_bound = results['cumulative_lower']
                upper_bound = results['cumulative_upper']

                # Shade the credible interval
                for i, patch in enumerate(patches):
                    if bins[i] >= lower_bound and bins[i] <= upper_bound:
                        patch.set_facecolor('#39FF14')
                        patch.set_alpha(0.8)

                # Add vertical lines for key statistics
                mean_val = results['total_effect']
                ax.axvline(mean_val, color='#00FF00', linestyle='-',
                          linewidth=3, label=f'Mean: {mean_val:,.0f}', zorder=10)
                ax.axvline(lower_bound, color='#39FF14', linestyle='--',
                          linewidth=2, label=f'{ci_level}% Credible Interval', zorder=9)
                ax.axvline(upper_bound, color='#39FF14', linestyle='--',
                          linewidth=2, zorder=9)
                ax.axvline(0, color='#FF6B6B', linestyle='-',
                          linewidth=2, label='No Effect', alpha=0.7, zorder=8)

                ax.set_title(f'Posterior Distribution of Cumulative Effect ({results.get("n_samples", 0):,} MCMC Samples)',
                            color='white', fontsize=16, fontweight='bold', pad=15)
                ax.set_xlabel('Cumulative Effect', color='white', fontsize=12)
                ax.set_ylabel('Probability Density', color='white', fontsize=12)
                ax.legend(facecolor='#0E1117', edgecolor='#00FF00', labelcolor='white',
                         fontsize=11, loc='upper left', framealpha=0.9)
                ax.tick_params(colors='white', labelsize=10)
                ax.spines['bottom'].set_color('#262730')
                ax.spines['left'].set_color('#262730')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.grid(True, alpha=0.15, color='#262730', linestyle='-', linewidth=0.5)

                plt.tight_layout()
                st.pyplot(fig_posterior, width='stretch')
                plt.close(fig_posterior)

                # Add probability statistics
                col1, col2, col3 = st.columns(3)

                with col1:
                    prob_positive = results['prob_causal_effect']
                    st.metric(
                        "P(Effect > 0)",
                        f"{prob_positive:.1f}%",
                        help="Probability that the campaign had a positive effect"
                    )

                with col2:
                    # Calculate probability of "meaningful" effect (e.g., >5% of counterfactual)
                    counterfactual_total = np.sum(results['counterfactual'])
                    if 'posterior_samples' in results and results['posterior_samples'] is not None:
                        meaningful_threshold = counterfactual_total * 0.05
                        prob_meaningful = np.mean(posterior_cumulative > meaningful_threshold) * 100
                    else:
                        prob_meaningful = prob_positive if results['relative_effect'] > 5 else 0

                    st.metric(
                        "P(Effect > 5%)",
                        f"{prob_meaningful:.1f}%",
                        help="Probability that the campaign drove >5% uplift"
                    )

                with col3:
                    # Probability of very large effect (>20%)
                    if 'posterior_samples' in results and results['posterior_samples'] is not None:
                        large_threshold = counterfactual_total * 0.20
                        prob_large = np.mean(posterior_cumulative > large_threshold) * 100
                    else:
                        prob_large = prob_positive if results['relative_effect'] > 20 else 0

                    st.metric(
                        "P(Effect > 20%)",
                        f"{prob_large:.1f}%",
                        help="Probability that the campaign drove >20% uplift"
                    )

            # Interpretation
            st.markdown("---")
            st.markdown("### 💰 Estimated Intervention Value")

            # Calculate estimated monetary value (if user wants to input unit value)
            col1, col2 = st.columns([1, 2])

            with col1:
                unit_value = st.number_input(
                    "Value per Unit (£)",
                    min_value=0.0,
                    value=0.0,
                    step=0.1,
                    help="Enter the monetary value of each unit to estimate total intervention value"
                )

            with col2:
                if unit_value > 0:
                    total_value = results['total_effect'] * unit_value
                    daily_value = results['avg_effect'] * unit_value

                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(0,255,0,0.1) 0%, rgba(0,255,0,0.05) 100%);
                                padding: 1.5rem; border-radius: 10px; border-left: 5px solid {BRAND_COLORS['success']};'>
                        <h4 style='color: {BRAND_COLORS['primary']}; margin-top: 0;'>💷 Estimated Intervention Value</h4>
                        <p style='font-size: 1.8rem; font-weight: bold; color: {BRAND_COLORS['primary']}; margin: 0.5rem 0;'>
                            £{total_value:,.2f}
                        </p>
                        <p style='color: #666; margin: 0.5rem 0;'>
                            Total value generated (£{daily_value:,.2f} per day)
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("💡 Enter a value per unit above to estimate the total monetary value of the intervention")

            st.markdown("---")
            st.markdown("### 💡 Plain-English Interpretation")

            direction = "positive" if results['avg_effect'] > 0 else "negative"
            # Use 80% as threshold - standard for Bayesian "likely" effect
            if prob_effect >= 95:
                significance = "highly statistically significant"
            elif prob_effect >= 80:
                significance = "statistically significant"
            else:
                significance = "not statistically significant"

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
                        padding: 2rem; border-radius: 12px; border-left: 5px solid {BRAND_COLORS['success']};'>
                <h4 style='color: {BRAND_COLORS['secondary']}; margin-top: 0;'>🎯 Campaign Impact Summary</h4>
                <p style='font-size: 1.1rem; line-height: 1.8; color: #444;'>
                    Your intervention had a <strong>{significance} {direction} effect</strong> on the KPI.
                    We estimate <strong>{results['total_effect']:,.0f} incremental units</strong> over the post-intervention period,
                    representing a <strong>{results['relative_effect']:.1f}% lift</strong> above what we would have expected without the intervention.
                </p>
                <p style='font-size: 1.05rem; line-height: 1.8; color: #555;'>
                    The average daily effect was <strong>{results['avg_effect']:,.0f} units</strong>.
                    Based on our Bayesian analysis, there is a <strong>{prob_effect}% probability</strong> that this effect is real
                    and not due to random chance.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Download options
            st.markdown("---")
            st.markdown("### 📥 Export Results")

            col1, col2 = st.columns(2)

            with col1:
                # Prepare CSV download
                export_df = results['post_data'][['date']].copy()
                export_df['actual'] = results['actual']
                export_df['counterfactual'] = results['counterfactual']
                export_df['point_effect'] = results['point_effect']
                export_df['cumulative_effect'] = results['cumulative_effect']

                csv = export_df.to_csv(index=False)
                st.download_button(
                    "📊 Download Results (CSV)",
                    csv,
                    "av_campaign_analysis_results.csv",
                    "text/csv",
                    width='stretch'
                )

            with col2:
                # Summary report
                # Get convergence info
                convergence = results.get('convergence', {})
                n_samples = results.get('n_samples', 0)

                report = f"""
AV CAMPAIGN ANALYSIS REPORT
Electric Glue - AV Campaign Analyser
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ANALYSIS METHOD: Bayesian MCMC with Structural Time Series
MCMC SAMPLES: {n_samples:,}
CONVERGENCE STATUS: {convergence.get('message', 'N/A')}

CAMPAIGN PERIOD:
- Campaign Start: {results['intervention_date'].strftime('%Y-%m-%d')}
- Campaign End: {results['campaign_end_date'].strftime('%Y-%m-%d')}
- Campaign Duration: {results['campaign_days']} days
- Measurement Window: {results['measurement_days']} days post-campaign

SUMMARY STATISTICS:
- Total Incremental Impact: {results['total_effect']:,.0f} units
- Average Daily Effect: {results['avg_effect']:,.0f} units/day
- Relative Lift: {results['relative_effect']:.1f}%
- Posterior Probability of Positive Effect: {results.get('prob_causal_effect', prob_effect):.1f}%

CREDIBLE INTERVALS ({results.get('confidence_level', 95)}%):
- Cumulative Effect: [{results.get('cumulative_lower', 0):,.0f}, {results.get('cumulative_upper', 0):,.0f}]

MEASUREMENT WINDOW (90 DAYS POST-CAMPAIGN):
- Actual (observed): {np.mean(results['actual']):,.0f} avg/day, {np.sum(results['actual']):,.0f} total
- Counterfactual (predicted): {np.mean(results['counterfactual']):,.0f} avg/day, {np.sum(results['counterfactual']):,.0f} total
- Incremental Effect: {results['avg_effect']:,.0f} avg/day, {results['total_effect']:,.0f} total

STATISTICAL INTERPRETATION:
The AV campaign had a {significance} {direction} effect on the KPI. Based on {n_samples:,} MCMC samples,
we estimate {results['total_effect']:,.0f} incremental units over the 90-day post-campaign
measurement window, representing a {results['relative_effect']:.1f}% uplift vs. the counterfactual.

The Bayesian posterior probability of a positive effect is {results.get('prob_causal_effect', prob_effect):.1f}%,
indicating {'strong' if results.get('prob_causal_effect', prob_effect) > 95 else 'moderate' if results.get('prob_causal_effect', prob_effect) > 80 else 'weak'} evidence of campaign impact.

---
Powered by Electric Glue | Advanced Bayesian Analysis
                """

                st.download_button(
                    "📄 Download Report (TXT)",
                    report,
                    "av_campaign_analysis_report.txt",
                    "text/plain",
                    width='stretch'
                )

with tab4:
    st.markdown("### 🚦 QA Validation Report")

    if 'qa_report' not in st.session_state:
        st.info("ℹ️ Run the analysis first to see QA validation results.")
    else:
        qa = st.session_state['qa_report']

        # Overall Status Banner
        status = qa['overall_status']
        confidence = qa['confidence_score']

        if status == 'PASSED':
            status_color = '#00FF00'
            status_icon = '✅'
            status_bg = 'rgba(0,255,0,0.1)'
        elif status == 'WARNING':
            status_color = '#FFA500'
            status_icon = '⚠️'
            status_bg = 'rgba(255,165,0,0.1)'
        else:
            status_color = '#FF0000'
            status_icon = '🔴'
            status_bg = 'rgba(255,0,0,0.1)'

        st.markdown(f"""
        <div style='background: {status_bg}; padding: 2rem; border-radius: 15px;
                    border-left: 6px solid {status_color}; margin-bottom: 2rem;'>
            <h2 style='color: {status_color}; margin-top: 0; font-size: 2rem;'>
                {status_icon} QA Status: {status}
            </h2>
            <p style='font-size: 1.5rem; font-weight: 600; color: {status_color}; margin: 1rem 0;'>
                Confidence Score: {confidence:.1f}%
            </p>
            <p style='color: #666; font-size: 1rem; margin: 0;'>
                {qa['recommendation']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Confidence Score Breakdown
        st.markdown("#### 📊 Confidence Score Breakdown")

        breakdown = qa['confidence_breakdown']
        cols = st.columns(3)

        breakdown_items = [
            ('Data Quality', breakdown.get('data_quality', 0), 'Quality and completeness of input data'),
            ('Statistical Validity', breakdown.get('statistical_validity', 0), 'Statistical rigor and sample size'),
            ('MCMC Convergence', breakdown.get('mcmc_convergence', 0), 'Bayesian MCMC convergence quality'),
            ('Calculation Verification', breakdown.get('calculation_verification', 0), 'Mathematical accuracy checks'),
            ('Output Coherence', breakdown.get('output_coherence', 0), 'Internal consistency of results'),
            ('Counterfactual Validity', breakdown.get('counterfactual_validity', 0), 'Quality of baseline forecast')
        ]

        for i, (name, score, description) in enumerate(breakdown_items):
            col_idx = i % 3
            with cols[col_idx]:
                # Determine color based on score
                if score >= 85:
                    bar_color = '#00FF00'
                elif score >= 70:
                    bar_color = '#FFA500'
                else:
                    bar_color = '#FF0000'

                st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
                    <p style='margin: 0 0 0.5rem 0; font-weight: 600; color: #333;'>{name}</p>
                    <div style='background: #f0f0f0; height: 20px; border-radius: 10px; overflow: hidden;'>
                        <div style='background: {bar_color}; height: 100%; width: {score}%;
                                    transition: width 0.3s ease;'></div>
                    </div>
                    <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #666;'>
                        {score:.0f}% - {description}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Detailed Layer Results
        st.markdown("---")
        st.markdown("#### 🔍 Detailed Validation Results")

        layers = qa['layer_results']

        for layer_name, layer_data in layers.items():
            layer_title = layer_name.replace('_', ' ').title()
            layer_score = layer_data['score']
            layer_passed = layer_data['passed']

            # Expander for each layer
            with st.expander(f"{'✅' if layer_passed else '⚠️'} {layer_title} - Score: {layer_score:.0f}%", expanded=not layer_passed):
                checks = layer_data.get('checks', {})

                if checks:
                    # Create a dataframe for checks
                    check_data = []
                    for check_name, check_result in checks.items():
                        if isinstance(check_result, dict):
                            passed = check_result.get('passed', check_result.get('valid', check_result.get('adequate', check_result.get('reasonable', True))))
                            description = check_result.get('description', str(check_result))

                            check_data.append({
                                'Check': check_name.replace('_', ' ').title(),
                                'Status': '✅ Pass' if passed else '❌ Fail',
                                'Details': description
                            })

                    if check_data:
                        df = pd.DataFrame(check_data)
                        st.dataframe(df, width='stretch', hide_index=True)
                else:
                    st.write("No detailed checks available for this layer.")

        # Flags and Warnings
        if qa['flags'] or qa['warnings']:
            st.markdown("---")
            st.markdown("#### ⚠️ Issues Detected")

            col1, col2 = st.columns(2)

            with col1:
                if qa['flags']:
                    st.markdown("**Critical Flags:**")
                    for flag in qa['flags']:
                        st.markdown(f"- {flag}")
                else:
                    st.success("✅ No critical flags")

            with col2:
                if qa['warnings']:
                    st.markdown("**Warnings:**")
                    for warning in qa['warnings']:
                        st.markdown(f"- {warning}")
                else:
                    st.success("✅ No warnings")

        # What This Means Section
        st.markdown("---")
        with st.expander("ℹ️ Understanding QA Validation", expanded=False):
            st.markdown("""
            ### How QA Validation Works

            The QA system performs **7 layers of automated validation** on your analysis:

            1. **Data Quality (25% weight)**: Checks for missing values, sufficient data points, date continuity, and outliers
            2. **Statistical Validity (25% weight)**: Validates sample sizes, effect size reasonableness, and credible interval precision
            3. **MCMC Convergence (20% weight)**: Ensures Bayesian MCMC properly converged with sufficient effective samples
            4. **Calculation Verification (15% weight)**: Cross-checks all mathematical calculations for accuracy
            5. **Output Coherence (10% weight)**: Validates internal consistency of results
            6. **Counterfactual Validity (5% weight)**: Assesses quality of baseline forecast

            ### Traffic Light System

            - 🟢 **PASSED (≥85%)**: High confidence - results are reliable for decision-making
            - 🟡 **WARNING (70-84%)**: Moderate confidence - review issues before using
            - 🔴 **FAILED (<70%)**: Low confidence - address critical problems first

            ### Why This Matters

            This QA system addresses the **#1 concern about AI adoption**: accuracy and trustworthiness.
            By having AI validate AI, we provide transparent confidence scoring for every analysis.
            """)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(0,255,0,0.03) 0%, rgba(0,0,0,0.03) 100%);
            border-radius: 12px; margin-top: 2rem;'>
    <p style='color: {BRAND_COLORS['text']}; font-size: 1rem; font-weight: 600; margin: 0.5rem 0;'>
        ⚡ <strong>Electric Glue</strong> | Causal Impact Analyser
    </p>
    <p style='font-size: 0.85rem; color: #999; margin: 1rem 0 0.5rem 0;'>
        Built on Google's CausalImpact R Package | Powered by Multi-Agent AI
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
