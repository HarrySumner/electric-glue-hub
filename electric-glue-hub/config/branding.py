"""
Electric Glue Branding Configuration
For TV Campaign Impact Analyzer
"""

# Electric Glue Brand Colors - Black, White, Green
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

# Streamlit Custom CSS
CUSTOM_CSS = """
<style>
    /* Electric Glue Brand Styling */

    /* True black background */
    .stApp {
        background-color: #000000;
    }

    /* Main content area */
    .main .block-container {
        background-color: #000000;
        padding-top: 2rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
    }

    .main-header {
        background: linear-gradient(135deg, #000000 0%, #00FF00 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 255, 0, 0.3);
    }

    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }

    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2rem;
        margin-top: 0;
    }

    .main-header .tagline {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.95rem;
        font-style: italic;
        margin-top: 0.5rem;
    }

    /* Feature boxes */
    .feature-box {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.05) 0%, rgba(0, 0, 0, 0.05) 100%);
        border-left: 4px solid #00FF00;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .feature-box:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0, 255, 0, 0.3);
        border-left-width: 6px;
    }

    /* Agent status indicators */
    .agent-status {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.3rem;
    }

    .agent-running {
        background: linear-gradient(135deg, #39FF14 0%, #39FF14 100%);
        color: #000000;
    }

    .agent-complete {
        background: linear-gradient(135deg, #00FF00 0%, #00FF00 100%);
        color: #000000;
    }

    .agent-waiting {
        background: linear-gradient(135deg, #666666 0%, #666666 100%);
        color: white;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        border: 2px solid #F5F5F5;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: #00FF00;
        box-shadow: 0 6px 12px rgba(0, 255, 0, 0.3);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00FF00;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.95rem;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Confidence indicators */
    .confidence-high {
        color: #00FF00;
        font-weight: 700;
    }

    .confidence-medium {
        color: #39FF14;
        font-weight: 700;
    }

    .confidence-low {
        color: #FF0000;
        font-weight: 700;
    }

    /* Results section */
    .results-container {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.03) 0%, rgba(0, 0, 0, 0.03) 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
    }

    /* Buttons */
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

    /* Footer */
    .footer {
        text-align: center;
        color: #6C757D;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 2px solid #F5F5F5;
    }

    .footer .brand-name {
        color: #00FF00;
        font-weight: 700;
    }

    /* Data quality indicators */
    .quality-excellent {
        background: #00FF00;
        color: #000000;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .quality-good {
        background: #39FF14;
        color: #000000;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .quality-poor {
        background: #FF0000;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        background-color: #1a1a1a;
        border-bottom: 3px solid transparent;
        color: #00FF00 !important;
        font-weight: 600;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2a2a2a;
        color: #39FF14 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #000000;
        border-bottom: 3px solid #00FF00;
        color: #00FF00 !important;
    }

    /* Tab content panel */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #000000;
        padding-top: 1rem;
    }

    /* Fix text colour on black background */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #FFFFFF;
    }

    .main p, .main li, .main span {
        color: #E0E0E0;
    }

    /* Input fields on black background */
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        color: #FFFFFF;
        border: 1px solid #00FF00;
    }

    .stTextArea > div > div > textarea {
        background-color: #1a1a1a;
        color: #FFFFFF;
        border: 1px solid #00FF00;
    }

    /* File uploader on black background */
    .stFileUploader {
        background-color: #1a1a1a;
        border: 2px dashed #00FF00;
        border-radius: 8px;
        padding: 1rem;
    }

    .stFileUploader label {
        color: #00FF00 !important;
    }
</style>
"""

# Page Configuration
PAGE_CONFIG = {
    "page_title": "TV Campaign Impact Analyzer | Electric Glue",
    "page_icon": "📺",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Header HTML
def get_header_html():
    return """
    <div class="main-header">
        <h1>📺 TV Campaign Impact Analyzer</h1>
        <p>Agentic Bayesian Analysis for Television Advertising ROI</p>
        <p class="tagline">Powered by Electric Glue's Proprietary AI</p>
    </div>
    """

# Footer HTML
def get_footer_html():
    return """
    <div class="footer">
        <p><strong class="brand-name">Electric Glue</strong> | AI-First Marketing Intelligence</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">
            Proprietary TV Attribution Tool | © 2025
        </p>
        <p style="font-size: 0.8rem; color: #9CA3AF; margin-top: 0.5rem;">
            Built with Multi-Agent AI · Bayesian Statistics · Data Science
        </p>
    </div>
    """

# Sidebar branding
def get_sidebar_html():
    return """
    <div style="padding: 1rem; background: linear-gradient(135deg, #000000 0%, #00FF00 100%); border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: white; margin: 0; font-size: 1.3rem;">Electric Glue</h3>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; margin: 0.3rem 0 0 0;">
            TV Campaign Intelligence
        </p>
    </div>
    """

# Agent status display
def get_agent_status_html(agent_name, status):
    """
    Generate HTML for agent status display
    status: 'waiting', 'running', 'complete'
    """
    status_class = f"agent-{status}"
    status_icon = {
        'waiting': '⏸️',
        'running': '🔄',
        'complete': '✅'
    }
    status_text = {
        'waiting': 'Waiting',
        'running': 'Running',
        'complete': 'Complete'
    }

    return f"""
    <span class="agent-status {status_class}">
        {status_icon[status]} {agent_name}: {status_text[status]}
    </span>
    """

# Quality indicator
def get_quality_html(quality_score):
    """
    Generate HTML for data quality indicator
    quality_score: 0-100
    """
    if quality_score >= 80:
        quality_class = "quality-excellent"
        quality_text = "Excellent"
        icon = "🟢"
    elif quality_score >= 60:
        quality_class = "quality-good"
        quality_text = "Good"
        icon = "🟡"
    else:
        quality_class = "quality-poor"
        quality_text = "Needs Attention"
        icon = "🔴"

    return f"""
    <span class="{quality_class}">
        {icon} Data Quality: {quality_text} ({quality_score}%)
    </span>
    """


# Main theme application function
def apply_electric_glue_theme():
    """Apply Electric Glue branding theme to Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Header formatter
def format_header(title: str, subtitle: str = "") -> str:
    """
    Format a branded header.

    Parameters
    ----------
    title : str
        Main header title
    subtitle : str, optional
        Subtitle text

    Returns
    -------
    str : HTML formatted header
    """
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""

    return f"""
    <div class="main-header">
        <h1>{title}</h1>
        {subtitle_html}
    </div>
    """


# Metric card formatter
def format_metric_card(label: str, value: str, detail: str = "") -> str:
    """
    Format a branded metric card.

    Parameters
    ----------
    label : str
        Metric label
    value : str
        Metric value
    detail : str, optional
        Additional detail text

    Returns
    -------
    str : HTML formatted metric card
    """
    detail_html = f"<p style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>{detail}</p>" if detail else ""

    return f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-left: 4px solid {BRAND_COLORS['primary']};'>
        <h4 style='color: {BRAND_COLORS['secondary']}; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>
            {label}
        </h4>
        <p style='font-size: 2rem; font-weight: bold; color: {BRAND_COLORS['primary']}; margin: 0;'>
            {value}
        </p>
        {detail_html}
    </div>
    """
