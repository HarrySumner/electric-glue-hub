"""
Settings Page - API Key Configuration
Manage API keys for AI models and external services
"""

import streamlit as st
import sys
import os
from pathlib import Path
from dotenv import load_dotenv, set_key, find_dotenv

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from config.branding import apply_electric_glue_theme, BRAND_COLORS, format_header
from core.api_usage_tracker import get_tracker

# Page config
st.set_page_config(
    page_title="Settings | Electric Glue",
    page_icon="⚙️",
    layout="wide"
)

# Apply branding
apply_electric_glue_theme()

# Header
st.markdown(format_header(
    "⚙️ Settings",
    "Configure API Keys and System Settings"
), unsafe_allow_html=True)

# Navigation
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("---")

# Load environment variables
load_dotenv()

# Overview
st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.05) 100%);
            padding: 2rem; border-radius: 12px; border-left: 5px solid {BRAND_COLORS['primary']};'>
    <h3 style='color: {BRAND_COLORS['secondary']}; margin-top: 0;'>🔑 API Key Management</h3>
    <p style='font-size: 1.05rem; line-height: 1.8; color: #555;'>
        Configure API keys for AI models (OpenAI, Anthropic) and external services.
        Your keys are stored securely in a <code>.env</code> file and never transmitted beyond your local environment.
    </p>
    <p style='font-size: 0.95rem; line-height: 1.8; color: #666; margin-top: 1rem;'>
        <strong>⚠️ Security Note:</strong> API keys are sensitive credentials. Never share your <code>.env</code> file
        or commit it to version control. Each team member should configure their own keys.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# API Keys Configuration
st.markdown(f"## 🔐 API Keys")

# Get .env file path
env_path = find_dotenv()
if not env_path:
    env_path = Path(__file__).parent.parent / ".env"
    # Create .env if it doesn't exist
    if not env_path.exists():
        env_path.touch()

# OpenAI Configuration
st.markdown(f"""
<div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border-left: 4px solid {BRAND_COLORS['primary']};'>
    <h4 style='color: {BRAND_COLORS['primary']}; margin-top: 0;'>🤖 OpenAI API Key</h4>
    <p style='color: #666; font-size: 0.95rem; line-height: 1.6;'>
        Used by Product 2 (Scout) for multi-perspective analysis. Get your API key from
        <a href='https://platform.openai.com/api-keys' target='_blank' style='color: {BRAND_COLORS['primary']};'>
            OpenAI Platform
        </a>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Check current OpenAI key status
current_openai_key = os.getenv('OPENAI_API_KEY', '')
openai_status = "✓ Configured" if current_openai_key else "⚠️ Not Configured"
openai_status_color = BRAND_COLORS['success'] if current_openai_key else BRAND_COLORS['warning']

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"**Current Status:** <span style='color: {openai_status_color}; font-weight: 600;'>{openai_status}</span>", unsafe_allow_html=True)
with col2:
    if current_openai_key:
        masked_key = current_openai_key[:8] + "..." + current_openai_key[-4:] if len(current_openai_key) > 12 else "***"
        st.code(masked_key, language=None)

# OpenAI API Key Input
with st.expander("🔧 Configure OpenAI API Key", expanded=not bool(current_openai_key)):
    openai_key_input = st.text_input(
        "Enter OpenAI API Key",
        value="",
        type="password",
        placeholder="sk-...",
        help="Your OpenAI API key (starts with 'sk-')"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 Save OpenAI Key", width='stretch'):
            if openai_key_input:
                try:
                    set_key(env_path, 'OPENAI_API_KEY', openai_key_input)
                    os.environ['OPENAI_API_KEY'] = openai_key_input
                    st.success("✓ OpenAI API key saved successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving API key: {e}")
            else:
                st.warning("Please enter an API key")

    with col2:
        if current_openai_key and st.button("🗑️ Remove OpenAI Key", width='stretch'):
            try:
                set_key(env_path, 'OPENAI_API_KEY', '')
                os.environ.pop('OPENAI_API_KEY', None)
                st.success("✓ OpenAI API key removed")
                st.rerun()
            except Exception as e:
                st.error(f"Error removing API key: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# Anthropic Configuration
st.markdown(f"""
<div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border-left: 4px solid {BRAND_COLORS['accent']};'>
    <h4 style='color: {BRAND_COLORS['accent']}; margin-top: 0;'>🧠 Anthropic API Key (Claude)</h4>
    <p style='color: #666; font-size: 0.95rem; line-height: 1.6;'>
        Alternative AI provider for analysis tasks. Get your API key from
        <a href='https://console.anthropic.com/account/keys' target='_blank' style='color: {BRAND_COLORS['accent']};'>
            Anthropic Console
        </a>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Check current Anthropic key status
current_anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
anthropic_status = "✓ Configured" if current_anthropic_key else "⚠️ Not Configured"
anthropic_status_color = BRAND_COLORS['success'] if current_anthropic_key else BRAND_COLORS['warning']

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"**Current Status:** <span style='color: {anthropic_status_color}; font-weight: 600;'>{anthropic_status}</span>", unsafe_allow_html=True)
with col2:
    if current_anthropic_key:
        masked_key = current_anthropic_key[:8] + "..." + current_anthropic_key[-4:] if len(current_anthropic_key) > 12 else "***"
        st.code(masked_key, language=None)

# Anthropic API Key Input
with st.expander("🔧 Configure Anthropic API Key", expanded=not bool(current_anthropic_key)):
    anthropic_key_input = st.text_input(
        "Enter Anthropic API Key",
        value="",
        type="password",
        placeholder="sk-ant-...",
        help="Your Anthropic API key (starts with 'sk-ant-')"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 Save Anthropic Key", width='stretch'):
            if anthropic_key_input:
                try:
                    set_key(env_path, 'ANTHROPIC_API_KEY', anthropic_key_input)
                    os.environ['ANTHROPIC_API_KEY'] = anthropic_key_input
                    st.success("✓ Anthropic API key saved successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving API key: {e}")
            else:
                st.warning("Please enter an API key")

    with col2:
        if current_anthropic_key and st.button("🗑️ Remove Anthropic Key", width='stretch'):
            try:
                set_key(env_path, 'ANTHROPIC_API_KEY', '')
                os.environ.pop('ANTHROPIC_API_KEY', None)
                st.success("✓ Anthropic API key removed")
                st.rerun()
            except Exception as e:
                st.error(f"Error removing API key: {e}")

st.markdown("<br><br>", unsafe_allow_html=True)

# System Information
st.markdown("---")
st.markdown(f"## 💻 System Information")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"""
    <div style='background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06);'>
        <h4 style='color: {BRAND_COLORS['primary']};'>📁 Environment File</h4>
        <p style='color: #666; font-size: 0.95rem;'>
            <strong>Location:</strong><br/>
            <code style='background: #f5f5f5; padding: 0.3rem 0.5rem; border-radius: 4px; font-size: 0.85rem;'>
                {env_path}
            </code>
        </p>
        <p style='color: #666; font-size: 0.95rem; margin-top: 1rem;'>
            <strong>Status:</strong> {'✓ File exists' if Path(env_path).exists() else '⚠️ File not found'}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06);'>
        <h4 style='color: {BRAND_COLORS['accent']};'>🔌 LLM Availability</h4>
        <p style='color: #666; font-size: 0.95rem;'>
            <strong>OpenAI:</strong> <span style='color: {openai_status_color};'>{'✓ Available' if current_openai_key else '⚠️ Not configured'}</span><br/>
            <strong>Anthropic:</strong> <span style='color: {anthropic_status_color};'>{'✓ Available' if current_anthropic_key else '⚠️ Not configured'}</span>
        </p>
        <p style='color: #666; font-size: 0.85rem; margin-top: 1rem; font-style: italic;'>
            At least one LLM provider is required for AI-powered features.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# API Usage Tracking
st.markdown("---")
st.markdown(f"## 📊 API Usage & Cost Tracking")

st.markdown("""
<div style='background: linear-gradient(135deg, rgba(0,255,255,0.05) 0%, rgba(0,0,0,0.05) 100%);
            padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;'>
    <p style='font-size: 0.95rem; line-height: 1.6; color: #666; margin: 0;'>
        Track API usage and estimated costs across all Electric Glue products.
        Costs are estimated based on current pricing and may vary slightly from actual billing.
    </p>
</div>
""", unsafe_allow_html=True)

# Load usage tracker
tracker = get_tracker()
summary = tracker.get_summary()
daily_stats = tracker.get_daily_summary(days=7)

# Overall Summary
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total API Calls",
        f"{summary['total_calls']:,}",
        help="Total number of API calls made"
    )

with col2:
    st.metric(
        "Total Tokens",
        f"{summary['total_tokens']:,}",
        help="Total tokens processed (input + output)"
    )

with col3:
    st.metric(
        "Estimated Cost",
        f"${summary['total_cost']:.4f}",
        help="Estimated total cost in USD"
    )

with col4:
    avg_cost_per_call = summary['total_cost'] / summary['total_calls'] if summary['total_calls'] > 0 else 0
    st.metric(
        "Avg Cost/Call",
        f"${avg_cost_per_call:.4f}",
        help="Average cost per API call"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Breakdown by Provider
if summary['by_provider']:
    st.markdown("### 🔑 Usage by Provider")

    cols = st.columns(len(summary['by_provider']))

    for idx, (provider, stats) in enumerate(summary['by_provider'].items()):
        with cols[idx]:
            color = BRAND_COLORS['primary'] if provider == 'openai' else BRAND_COLORS['accent']
            icon = "🤖" if provider == 'openai' else "🧠"

            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 12px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.06); border-top: 4px solid {color};'>
                <h4 style='color: {color}; margin: 0 0 1rem 0; font-size: 1.2rem;'>
                    {icon} {provider.upper()}
                </h4>
                <p style='margin: 0.5rem 0; color: #666; font-size: 0.9rem;'>
                    <strong>Calls:</strong> {stats['calls']:,}<br/>
                    <strong>Tokens:</strong> {stats['tokens']:,}<br/>
                    <strong>Cost:</strong> ${stats['cost']:.4f}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# Breakdown by Operation
if summary['by_operation']:
    st.markdown("### ⚡ Usage by Operation")

    operation_names = {
        'qa_validation': '🚦 QA Validation',
        'scout_research': '🧠 Scout Research',
        'perspective_generation': '🎭 Perspective Generation',
        'web_search': '🔍 Web Search'
    }

    for operation, stats in summary['by_operation'].items():
        display_name = operation_names.get(operation, operation.replace('_', ' ').title())

        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            st.markdown(f"**{display_name}**")
        with col2:
            st.caption(f"{stats['calls']:,} calls")
        with col3:
            st.caption(f"{stats['tokens']:,} tokens")
        with col4:
            st.caption(f"${stats['cost']:.4f}")

    st.markdown("<br>", unsafe_allow_html=True)

# Daily Usage Chart
if daily_stats:
    st.markdown("### 📅 Last 7 Days")

    import pandas as pd

    # Convert to DataFrame for display
    daily_data = []
    for date, stats in sorted(daily_stats.items()):
        daily_data.append({
            'Date': date,
            'Calls': stats['calls'],
            'Tokens': stats['tokens'],
            'Cost ($)': round(stats['cost'], 4)
        })

    if daily_data:
        df = pd.DataFrame(daily_data)
        st.dataframe(df, width='stretch', hide_index=True)

        # Simple chart
        st.markdown("**Cost Trend**")
        st.bar_chart(df.set_index('Date')['Cost ($)'])

    st.markdown("<br>", unsafe_allow_html=True)

# Recent API Calls
with st.expander("🔍 Recent API Calls (Last 10)", expanded=False):
    recent = tracker.get_recent_calls(limit=10)

    if recent:
        for call in reversed(recent):  # Show newest first
            timestamp = call['timestamp'].split('T')[1].split('.')[0] if 'T' in call['timestamp'] else call['timestamp']
            date = call['timestamp'].split('T')[0] if 'T' in call['timestamp'] else ''

            status_icon = "✅" if call['success'] else "❌"
            cost_str = f"${call['estimated_cost']:.4f}"

            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid {"#00FF00" if call["success"] else "#FF0000"};'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong>{status_icon} {call['operation'].replace('_', ' ').title()}</strong><br/>
                        <span style='font-size: 0.85rem; color: #666;'>
                            {call['provider']} • {call['model'][:30]}{'...' if len(call['model']) > 30 else ''} • {date} {timestamp}
                        </span>
                    </div>
                    <div style='text-align: right;'>
                        <strong style='color: {BRAND_COLORS["primary"]};'>{cost_str}</strong><br/>
                        <span style='font-size: 0.85rem; color: #999;'>{call['total_tokens']:,} tokens</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No API calls tracked yet. Usage will appear here after you use Scout or QA Validation.")

# Reset button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🔄 Refresh Stats"):
        st.rerun()

with col2:
    if st.button("🗑️ Reset All Stats"):
        tracker.reset_stats()
        st.success("✓ Usage statistics reset")
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Help Section
st.markdown("---")
st.markdown(f"## 💡 Help & Documentation")

st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(0,255,0,0.03) 0%, rgba(0,0,0,0.03) 100%);
            padding: 2rem; border-radius: 12px;'>
    <h4 style='color: {BRAND_COLORS['secondary']};'>❓ Frequently Asked Questions</h4>

    <details style='margin-top: 1rem;'>
        <summary style='cursor: pointer; color: {BRAND_COLORS['primary']}; font-weight: 600; font-size: 1.05rem;'>
            Where are my API keys stored?
        </summary>
        <p style='color: #666; margin-top: 0.5rem; padding-left: 1.5rem; line-height: 1.7;'>
            API keys are stored in a <code>.env</code> file in the root directory of the Electric Glue Hub application.
            This file is never committed to version control (it's listed in <code>.gitignore</code>).
        </p>
    </details>

    <details style='margin-top: 1rem;'>
        <summary style='cursor: pointer; color: {BRAND_COLORS['primary']}; font-weight: 600; font-size: 1.05rem;'>
            Do I need both OpenAI and Anthropic keys?
        </summary>
        <p style='color: #666; margin-top: 0.5rem; padding-left: 1.5rem; line-height: 1.7;'>
            No, you only need at least one. The system will use whichever provider(s) you have configured.
            OpenAI (GPT-4) is currently used by Product 2 (Scout) for multi-perspective analysis.
        </p>
    </details>

    <details style='margin-top: 1rem;'>
        <summary style='cursor: pointer; color: {BRAND_COLORS['primary']}; font-weight: 600; font-size: 1.05rem;'>
            What if I don't have an API key?
        </summary>
        <p style='color: #666; margin-top: 0.5rem; padding-left: 1.5rem; line-height: 1.7;'>
            Some features will fall back to rule-based analysis instead of AI-powered insights.
            For the full experience, we recommend getting an API key from OpenAI or Anthropic.
        </p>
    </details>

    <details style='margin-top: 1rem;'>
        <summary style='cursor: pointer; color: {BRAND_COLORS['primary']}; font-weight: 600; font-size: 1.05rem;'>
            How do I share this with my team?
        </summary>
        <p style='color: #666; margin-top: 0.5rem; padding-left: 1.5rem; line-height: 1.7;'>
            Each team member should configure their own API keys on their local installation.
            <strong>Never share your <code>.env</code> file or API keys directly.</strong> Each person should get their own keys from the provider.
        </p>
    </details>

    <details style='margin-top: 1rem;'>
        <summary style='cursor: pointer; color: {BRAND_COLORS['primary']}; font-weight: 600; font-size: 1.05rem;'>
            Are my API keys secure?
        </summary>
        <p style='color: #666; margin-top: 0.5rem; padding-left: 1.5rem; line-height: 1.7;'>
            Yes. API keys are stored locally on your machine in the <code>.env</code> file and are never transmitted
            beyond your local environment. They are only used to authenticate with OpenAI or Anthropic when making API calls.
        </p>
    </details>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(0,255,0,0.03) 0%, rgba(0,0,0,0.03) 100%);
            border-radius: 12px; margin-top: 2rem;'>
    <p style='color: {BRAND_COLORS['text']}; font-size: 1rem; font-weight: 600; margin: 0.5rem 0;'>
        ⚡ <strong>Electric Glue</strong> | Settings & Configuration
    </p>
    <p style='font-size: 0.85rem; color: #999; margin: 1rem 0 0.5rem 0;'>
        Secure API Key Management
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
