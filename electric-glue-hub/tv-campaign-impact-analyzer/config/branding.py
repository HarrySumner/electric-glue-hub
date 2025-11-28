"""
Electric Glue Branding Configuration
For TV Campaign Impact Analyzer
"""

# Electric Glue Brand Colors
BRAND_COLORS = {
    'primary': '#FF6B35',      # Electric Glue Orange
    'secondary': '#004E89',    # Electric Glue Blue
    'accent': '#F7B801',       # Electric Glue Yellow
    'dark': '#1A1A1D',         # Dark background
    'light': '#F5F5F5',        # Light background
    'success': '#06D6A0',      # Success green
    'warning': '#F7B801',      # Warning yellow
    'danger': '#EF476F',       # Error red
    'text': '#1A1A1D',         # Primary text
    'text_light': '#6C757D'    # Secondary text
}

# Streamlit Custom CSS
CUSTOM_CSS = """
<style>
    /* Electric Glue Brand Styling */
    .main-header {
        background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.05) 0%, rgba(0, 78, 137, 0.05) 100%);
        border-left: 4px solid #FF6B35;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .feature-box:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.15);
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
        background: linear-gradient(135deg, #F7B801 0%, #F7B801 100%);
        color: #1A1A1D;
    }

    .agent-complete {
        background: linear-gradient(135deg, #06D6A0 0%, #06D6A0 100%);
        color: white;
    }

    .agent-waiting {
        background: linear-gradient(135deg, #6C757D 0%, #6C757D 100%);
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
        border-color: #FF6B35;
        box-shadow: 0 6px 12px rgba(255, 107, 53, 0.1);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FF6B35;
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
        color: #06D6A0;
        font-weight: 700;
    }

    .confidence-medium {
        color: #F7B801;
        font-weight: 700;
    }

    .confidence-low {
        color: #EF476F;
        font-weight: 700;
    }

    /* Results section */
    .results-container {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.03) 0%, rgba(0, 78, 137, 0.03) 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35 0%, #F7B801 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 107, 53, 0.3);
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
        color: #FF6B35;
        font-weight: 700;
    }

    /* Data quality indicators */
    .quality-excellent {
        background: #06D6A0;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .quality-good {
        background: #F7B801;
        color: #1A1A1D;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .quality-poor {
        background: #EF476F;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        background-color: #F5F5F5;
        border-bottom: 3px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        background-color: white;
        border-bottom: 3px solid #FF6B35;
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
    <div style="padding: 1rem; background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%); border-radius: 10px; margin-bottom: 1rem;">
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
