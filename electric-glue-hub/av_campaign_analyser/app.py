"""
AV Campaign Analyser - Main Streamlit Application
Analyzes Audio-Visual campaign impact on conversions with anomaly detection and regional analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional

# Import local modules
from config import AVConfig
from anomaly_detection import AnomalyDetector, ConversionAnomaly
from regional_analysis import RegionalAnalyzer, RegionalAnalysisResult
from utils import FileUploader, DataValidator, ChartGenerator, export_to_csv, export_to_excel


# Page configuration
st.set_page_config(
    page_title="AV Campaign Analyser",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light theme CSS
st.markdown("""
<style>
    /* Light theme styling */
    .main {
        background-color: #ffffff;
    }

    .stApp {
        background-color: #f8f9fa;
    }

    /* Headers */
    h1 {
        color: #1f2937;
        font-weight: 600;
    }

    h2, h3 {
        color: #374151;
        font-weight: 500;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1f2937;
    }

    /* Info boxes */
    .info-box {
        background-color: #e0f2fe;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0284c7;
        margin: 1rem 0;
    }

    .warning-box {
        background-color: #fef3c7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }

    .success-box {
        background-color: #d1fae5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }

    .error-box {
        background-color: #fee2e2;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }

    /* Buttons */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
    }

    .stButton>button:hover {
        background-color: #1d4ed8;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 2px dashed #d1d5db;
        border-radius: 0.5rem;
        padding: 1rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f3f4f6;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f3f4f6;
        border-radius: 0.375rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    if 'anomalies' not in st.session_state:
        st.session_state.anomalies = []
    if 'excluded_dates' not in st.session_state:
        st.session_state.excluded_dates = []
    if 'regional_result' not in st.session_state:
        st.session_state.regional_result = None


def render_header():
    """Render application header"""
    st.title("📺 AV Campaign Analyser")
    st.markdown("""
    <div class="info-box">
        <strong>Purpose:</strong> Analyze Audio-Visual (TV, YouTube, etc.) campaign impact on conversions.
        <br><strong>Features:</strong> Anomaly detection, regional uplift analysis, timeline visualization
    </div>
    """, unsafe_allow_html=True)


def render_data_upload():
    """Render data upload section"""
    st.header("1️⃣ Upload Data")

    with st.expander("📋 Data Requirements", expanded=False):
        st.markdown("""
        **Required Columns:**
        - `date` - Date in YYYY-MM-DD, DD/MM/YYYY, or MM/DD/YYYY format
        - `bookings` - Number of conversions/bookings per day

        **Optional Columns:**
        - `postcode` - Customer postcode (for regional analysis)
        - `revenue` - Revenue per day
        - `search_impressions` - Google search impressions
        - `search_clicks` - Google search clicks
        - `brand_searches` - Brand-specific search volume

        **File Formats:** CSV (.csv) or Excel (.xlsx, .xls)
        """)

    uploaded_files = st.file_uploader(
        "Upload one or more files (CSV or XLSX)",
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="You can upload multiple files - they will be merged automatically"
    )

    if uploaded_files:
        all_dataframes = []
        all_errors = []

        for uploaded_file in uploaded_files:
            with st.spinner(f'Loading {uploaded_file.name}...'):
                success, df, errors = FileUploader.load_file(uploaded_file)

                if success:
                    all_dataframes.append(df)
                    if errors:  # Warnings
                        all_errors.extend([f"{uploaded_file.name}: {e}" for e in errors])
                else:
                    st.error(f"**Error in {uploaded_file.name}:**")
                    for error in errors:
                        st.error(f"- {error}")
                    return

        if all_dataframes:
            # Merge dataframes
            merged_df = FileUploader.merge_dataframes(all_dataframes)
            st.session_state.uploaded_data = merged_df

            # Show warnings if any
            if all_errors:
                with st.expander("⚠️ Warnings", expanded=False):
                    for error in all_errors:
                        st.warning(error)

            # Show success message
            st.markdown(f"""
            <div class="success-box">
                ✅ Successfully loaded {len(uploaded_files)} file(s) with {len(merged_df)} rows
            </div>
            """, unsafe_allow_html=True)

            # Show data summary
            summary = DataValidator.get_data_summary(merged_df)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Rows", summary['total_rows'])
            col2.metric("Date Range", f"{summary['total_days']} days")
            col3.metric("Total Bookings", f"{summary['total_bookings']:,}")
            col4.metric("Avg/Day", f"{summary['avg_bookings_per_day']:.1f}")

            # Show data preview
            with st.expander("👀 Data Preview", expanded=False):
                st.dataframe(merged_df.head(20), use_container_width=True)

            # Data capabilities
            st.markdown("**Available Analysis:**")
            capabilities = []
            capabilities.append("✅ Anomaly Detection")
            if summary['has_postcode']:
                capabilities.append(f"✅ Regional Analysis ({summary['unique_postcodes']} unique postcodes)")
            else:
                capabilities.append("❌ Regional Analysis (no postcode data)")
            if summary['has_search_data']:
                capabilities.append("✅ Search Data Analysis")

            for cap in capabilities:
                st.markdown(f"- {cap}")


def render_anomaly_detection():
    """Render anomaly detection section"""
    if st.session_state.uploaded_data is None:
        return

    st.header("2️⃣ Anomaly Detection")
    st.markdown("Identify conversion spikes caused by PR events (e.g., Dragons Den, influencer posts)")

    col1, col2 = st.columns([1, 3])

    with col1:
        threshold = st.slider(
            "Detection Sensitivity",
            min_value=1.5,
            max_value=4.0,
            value=2.5,
            step=0.1,
            help="Lower = more sensitive (more anomalies detected)"
        )

        window = st.slider(
            "Baseline Window (days)",
            min_value=3,
            max_value=14,
            value=7,
            help="Number of days to use for baseline calculation"
        )

        if st.button("🔍 Detect Anomalies", type="primary"):
            with st.spinner("Analyzing conversion patterns..."):
                detector = AnomalyDetector(threshold_std_dev=threshold)
                anomalies = detector.detect_anomalies(
                    st.session_state.uploaded_data,
                    window=window
                )
                st.session_state.anomalies = anomalies

    with col2:
        if st.session_state.anomalies:
            st.markdown(f"""
            <div class="warning-box">
                <strong>🚨 {len(st.session_state.anomalies)} anomalies detected</strong>
                <br>Review these spikes and decide whether to exclude them from campaign analysis
            </div>
            """, unsafe_allow_html=True)

            # Anomaly triage interface
            st.subheader("Anomaly Triage")

            for i, anomaly in enumerate(st.session_state.anomalies):
                with st.container():
                    col_a, col_b, col_c = st.columns([2, 3, 2])

                    with col_a:
                        st.metric("Date", anomaly.date)
                        st.metric("Conversions", f"{anomaly.conversions:,}")

                    with col_b:
                        st.metric("Baseline Avg", f"{anomaly.baseline_avg:.1f}")
                        st.metric("Z-Score", f"{anomaly.z_score:.2f}")
                        st.metric("Increase", f"+{anomaly.increase_pct:.1f}%")

                    with col_c:
                        exclude = st.checkbox(
                            "Exclude from analysis",
                            key=f"exclude_{i}",
                            value=anomaly.date in st.session_state.excluded_dates
                        )

                        if exclude and anomaly.date not in st.session_state.excluded_dates:
                            st.session_state.excluded_dates.append(anomaly.date)
                        elif not exclude and anomaly.date in st.session_state.excluded_dates:
                            st.session_state.excluded_dates.remove(anomaly.date)

                        explanation = st.text_input(
                            "Reason (optional)",
                            key=f"reason_{i}",
                            placeholder="e.g., Dragons Den appearance"
                        )

                    st.divider()

            if st.session_state.excluded_dates:
                st.info(f"📝 {len(st.session_state.excluded_dates)} date(s) marked for exclusion")


def render_regional_analysis():
    """Render regional analysis section with user input prompts"""
    if st.session_state.uploaded_data is None:
        return

    summary = DataValidator.get_data_summary(st.session_state.uploaded_data)

    if not summary['has_postcode']:
        st.header("3️⃣ Regional Analysis")
        st.markdown("""
        <div class="warning-box">
            ⚠️ Regional analysis not available - no postcode data found in uploaded files
        </div>
        """, unsafe_allow_html=True)
        return

    st.header("3️⃣ Regional Analysis")
    st.markdown("Compare campaign regions vs control regions to measure AV campaign impact")

    # Show available postcodes
    with st.expander("📍 Available Postcode Regions", expanded=False):
        df = st.session_state.uploaded_data
        if 'postcode' in df.columns:
            analyzer = RegionalAnalyzer()
            df_temp = df.copy()
            df_temp['postcode_prefix'] = df_temp['postcode'].apply(
                lambda x: analyzer.extract_postcode_prefix(x, length=2)
            )

            breakdown = analyzer.get_region_breakdown(df)
            st.dataframe(breakdown, use_container_width=True)

            top_regions = breakdown.head(10)['postcode_prefix'].tolist()
            st.info(f"**Top regions:** {', '.join(top_regions)}")

    st.subheader("⚙️ Configure Regional Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Campaign regions input
        st.markdown("**Campaign Regions** (where AV campaign aired)")
        campaign_regions_input = st.text_input(
            "Enter postcode prefixes (comma-separated)",
            placeholder="e.g., SW, W1, E, N",
            help="Enter the postcode areas where your AV campaign aired (e.g., London = SW, W1, E, N, EC)"
        )

        if campaign_regions_input:
            analyzer = RegionalAnalyzer()
            campaign_regions = analyzer.parse_region_input(campaign_regions_input)
            st.success(f"✅ Campaign regions: {', '.join(campaign_regions)}")
        else:
            st.warning("👆 Please enter campaign regions to continue")
            return

    with col2:
        # Campaign period
        st.markdown("**Campaign Period**")

        df = st.session_state.uploaded_data
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()

        col_a, col_b = st.columns(2)
        with col_a:
            campaign_start = st.date_input(
                "Start Date",
                value=min_date,
                min_value=min_date,
                max_value=max_date
            )

        with col_b:
            campaign_end = st.date_input(
                "End Date",
                value=max_date,
                min_value=min_date,
                max_value=max_date
            )

        if campaign_start >= campaign_end:
            st.error("End date must be after start date")
            return

    # Analysis parameters
    uplift_threshold = st.slider(
        "Minimum Uplift % to Consider Significant",
        min_value=5.0,
        max_value=25.0,
        value=10.0,
        step=1.0,
        help="Minimum percentage uplift required to flag as significant"
    )

    # Run analysis button
    if st.button("📊 Run Regional Analysis", type="primary"):
        with st.spinner("Analyzing regional performance..."):
            # Get clean data (excluding anomalies if any)
            clean_df = st.session_state.uploaded_data.copy()
            if st.session_state.excluded_dates:
                detector = AnomalyDetector()
                clean_df = detector.get_clean_data(
                    clean_df,
                    st.session_state.excluded_dates
                )

            # Run analysis
            analyzer = RegionalAnalyzer(uplift_threshold=uplift_threshold)
            result = analyzer.analyze_regional_uplift(
                data=clean_df,
                campaign_regions=campaign_regions,
                campaign_start=str(campaign_start),
                campaign_end=str(campaign_end)
            )

            st.session_state.regional_result = result

    # Display results
    if st.session_state.regional_result:
        result = st.session_state.regional_result

        # Determine color based on uplift
        if result.uplift_pct > uplift_threshold:
            box_class = "success-box"
            emoji = "✅"
        elif result.uplift_pct > 0:
            box_class = "info-box"
            emoji = "ℹ️"
        else:
            box_class = "error-box"
            emoji = "❌"

        st.markdown(f"""
        <div class="{box_class}">
            <h3>{emoji} Regional Analysis Results</h3>
            <p><strong>Interpretation:</strong> {result.interpretation}</p>
        </div>
        """, unsafe_allow_html=True)

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Campaign Region Avg", f"{result.campaign_region_avg:.1f}/day")
        col2.metric("Control Region Avg", f"{result.control_region_avg:.1f}/day")
        col3.metric("Uplift", f"{result.uplift_pct:+.1f}%")
        col4.metric("Significant", "Yes" if result.is_significant else "No")

        # Visualization
        chart = ChartGenerator.create_regional_comparison_chart(
            result.campaign_region_avg,
            result.control_region_avg,
            result.uplift_pct
        )
        st.plotly_chart(chart, use_container_width=True)


def render_visualizations():
    """Render visualization section"""
    if st.session_state.uploaded_data is None:
        return

    st.header("4️⃣ Visualizations")

    df = st.session_state.uploaded_data

    # Get clean data
    clean_df = df.copy()
    if st.session_state.excluded_dates:
        detector = AnomalyDetector()
        clean_df = detector.get_clean_data(df, st.session_state.excluded_dates)

    # Timeline chart
    st.subheader("📈 Conversion Timeline")

    anomaly_dates = [a.date for a in st.session_state.anomalies] if st.session_state.anomalies else None

    campaign_start = None
    campaign_end = None
    if st.session_state.regional_result:
        campaign_start, campaign_end = st.session_state.regional_result.campaign_dates

    timeline_chart = ChartGenerator.create_timeline_chart(
        clean_df,
        anomaly_dates=anomaly_dates,
        campaign_start=campaign_start,
        campaign_end=campaign_end
    )
    st.plotly_chart(timeline_chart, use_container_width=True)

    # Regional breakdown (if postcode data exists)
    summary = DataValidator.get_data_summary(df)
    if summary['has_postcode']:
        st.subheader("🗺️ Regional Breakdown")

        analyzer = RegionalAnalyzer()
        breakdown = analyzer.get_region_breakdown(clean_df)

        top_n = st.slider("Number of regions to show", 5, 20, 10)

        breakdown_chart = ChartGenerator.create_postcode_breakdown_chart(breakdown, top_n=top_n)
        st.plotly_chart(breakdown_chart, use_container_width=True)


def render_export():
    """Render export section"""
    if st.session_state.uploaded_data is None:
        return

    st.header("5️⃣ Export Results")

    df = st.session_state.uploaded_data.copy()

    # Add analysis flags to export
    if st.session_state.anomalies:
        anomaly_dates = [a.date for a in st.session_state.anomalies]
        df['is_anomaly'] = df['date'].astype(str).isin(anomaly_dates)

    if st.session_state.excluded_dates:
        df['excluded_from_analysis'] = df['date'].astype(str).isin(st.session_state.excluded_dates)

    col1, col2 = st.columns(2)

    with col1:
        csv_data = export_to_csv(df)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"av_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    with col2:
        excel_data = export_to_excel(df)
        st.download_button(
            label="📥 Download Excel",
            data=excel_data,
            file_name=f"av_analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


def render_sidebar():
    """Render sidebar with configuration and help"""
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/2563eb/ffffff?text=AV+Analyser", use_container_width=True)

        st.markdown("---")

        st.subheader("⚙️ Configuration")

        # Validate config
        is_valid, error = AVConfig.validate()
        if is_valid:
            st.success("✅ API configured")
        else:
            st.error(f"❌ {error}")

        params = AVConfig.get_analysis_params()
        st.info(f"""
        **Default Settings:**
        - Anomaly threshold: {params['anomaly_threshold']} std devs
        - Regional threshold: {params['regional_threshold']}%
        """)

        st.markdown("---")

        st.subheader("📚 Help")

        with st.expander("How to use"):
            st.markdown("""
            1. **Upload Data** - Upload CSV/Excel files with date and bookings
            2. **Detect Anomalies** - Find conversion spikes (PR events)
            3. **Triage Anomalies** - Exclude spikes from campaign analysis
            4. **Regional Analysis** - Compare campaign vs control regions
            5. **Export** - Download results with analysis flags
            """)

        with st.expander("Common Issues"):
            st.markdown("""
            **Q: No anomalies detected?**
            - Lower the detection sensitivity slider
            - Check if you have at least 7 days of data

            **Q: Regional analysis not available?**
            - Ensure your data has a 'postcode' column
            - Postcodes should be UK format (e.g., SW1 1AA)

            **Q: Wrong date format?**
            - Supported: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY
            """)

        st.markdown("---")

        st.caption("AV Campaign Analyser v1.0")
        st.caption("Built with Streamlit + Claude")


def main():
    """Main application entry point"""
    init_session_state()
    render_sidebar()
    render_header()

    # Main content
    render_data_upload()

    if st.session_state.uploaded_data is not None:
        st.markdown("---")
        render_anomaly_detection()

        st.markdown("---")
        render_regional_analysis()

        st.markdown("---")
        render_visualizations()

        st.markdown("---")
        render_export()


if __name__ == "__main__":
    main()
