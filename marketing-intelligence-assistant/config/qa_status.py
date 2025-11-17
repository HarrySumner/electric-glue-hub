"""
QA Status Component - Embeddable traffic light for sidebar
Shows real-time QA agent health status across all pages
"""

import streamlit as st
from pathlib import Path
import sys
from datetime import datetime
import json

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tests"))

from config.branding import BRAND_COLORS


def load_qa_status():
    """Load latest QA test results from session state or cache file."""
    # Try session state first
    if 'qa_test_results' in st.session_state:
        return st.session_state.qa_test_results

    # Try cache file
    cache_file = Path(__file__).parent.parent / "logs" / "qa_last_run.json"
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except:
            pass

    return None


def save_qa_status(results):
    """Save QA test results to session state and cache file."""
    st.session_state.qa_test_results = results

    # Save to cache file
    cache_dir = Path(__file__).parent.parent / "logs"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / "qa_last_run.json"

    try:
        with open(cache_file, 'w') as f:
            json.dump(results, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save QA cache: {e}")


def run_qa_tests():
    """Run QA synthetic tests and return results."""
    try:
        from test_qa_synthetic import SyntheticTestSuite

        suite = SyntheticTestSuite()
        results = suite.run_all_tests()

        # Add timestamp
        results['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save results
        save_qa_status(results)

        return results
    except Exception as e:
        return {
            'error': str(e),
            'pass_rate': 0,
            'status': '🔴',
            'health': 'ERROR'
        }


def render_qa_traffic_light(location="sidebar"):
    """
    Render QA traffic light status widget.

    Parameters
    ----------
    location : str
        Where to render: "sidebar" or "main"
    """
    results = load_qa_status()

    if location == "sidebar":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🚦 QA System Health")

        if results is None:
            # No tests run yet
            st.sidebar.markdown(f"""
            <div style='background: rgba(128,128,128,0.1); padding: 1rem; border-radius: 8px;
                        border: 2px solid #888; text-align: center;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>⚪</div>
                <p style='color: #888; font-size: 0.9rem; margin: 0;'><strong>NOT TESTED</strong></p>
                <p style='color: #666; font-size: 0.8rem; margin: 0.5rem 0 0 0;'>Run tests to verify</p>
            </div>
            """, unsafe_allow_html=True)

            if st.sidebar.button("▶️ Run QA Tests", use_container_width=True, type="primary"):
                with st.spinner("Running 75 tests..."):
                    results = run_qa_tests()
                    st.rerun()

        else:
            # Show status
            pass_rate = results.get('pass_rate', 0)

            if pass_rate >= 95:
                light_color = "#00FF00"
                light_emoji = "🟢"
                status_text = "OPERATIONAL"
                status_bg = "rgba(0,255,0,0.1)"
                border_color = "#00FF00"
            elif pass_rate >= 80:
                light_color = "#FFD700"
                light_emoji = "🟡"
                status_text = "DEGRADED"
                status_bg = "rgba(255,215,0,0.1)"
                border_color = "#FFD700"
            else:
                light_color = "#FF0000"
                light_emoji = "🔴"
                status_text = "CRITICAL"
                status_bg = "rgba(255,0,0,0.1)"
                border_color = "#FF0000"

            st.sidebar.markdown(f"""
            <div style='background: {status_bg}; padding: 1rem; border-radius: 8px;
                        border: 2px solid {border_color}; text-align: center;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{light_emoji}</div>
                <p style='color: {light_color}; font-weight: bold; font-size: 0.95rem; margin: 0;'>{status_text}</p>
                <p style='color: #666; font-size: 1.2rem; font-weight: bold; margin: 0.3rem 0;'>{pass_rate:.0f}%</p>
                <p style='color: #666; font-size: 0.75rem; margin: 0;'>{results.get('passed', 0)}/{results.get('total', 0)} tests</p>
            </div>
            """, unsafe_allow_html=True)

            # Show timestamp
            if 'timestamp' in results:
                st.sidebar.markdown(f"<p style='text-align: center; color: #888; font-size: 0.7rem; margin-top: 0.5rem;'>Last run: {results['timestamp']}</p>", unsafe_allow_html=True)

            # Refresh button
            col1, col2 = st.sidebar.columns(2)
            with col1:
                if st.button("🔄 Refresh", use_container_width=True, key="qa_refresh"):
                    with st.spinner("Testing..."):
                        results = run_qa_tests()
                        st.rerun()

            with col2:
                if results.get('failed', 0) > 0:
                    if st.button("⚠️ Details", use_container_width=True, key="qa_details"):
                        st.session_state.show_qa_details = True

    elif location == "main":
        # Larger version for main content area
        if results is None:
            st.warning("⚪ **QA System Not Tested** - Run synthetic tests to verify system health")
            if st.button("▶️ Run 75 Synthetic Tests", type="primary"):
                with st.spinner("Running comprehensive QA validation tests..."):
                    results = run_qa_tests()
                    st.rerun()
        else:
            pass_rate = results.get('pass_rate', 0)

            if pass_rate >= 95:
                st.success(f"🟢 **QA System Operational** - {pass_rate:.1f}% ({results.get('passed')}/{results.get('total')} tests passing)")
            elif pass_rate >= 80:
                st.warning(f"🟡 **QA System Degraded** - {pass_rate:.1f}% ({results.get('passed')}/{results.get('total')} tests passing)")
            else:
                st.error(f"🔴 **QA System Critical** - {pass_rate:.1f}% ({results.get('passed')}/{results.get('total')} tests passing)")

            # Show failed tests if any
            if results.get('failed', 0) > 0:
                with st.expander(f"⚠️ {results.get('failed')} Failed Tests"):
                    for test in results.get('all_tests', []):
                        if not test.get('passed'):
                            st.markdown(f"- **{test['category']}**: {test['name']}")
                            st.markdown(f"  - Expected: {test['expected']}, Got: {test['actual']}")


def render_qa_diagnostics():
    """Render QA diagnostics for homepage."""
    results = load_qa_status()

    if results is None:
        return f"""
        <div style='background: rgba(128,128,128,0.05); padding: 2rem; border-radius: 15px;
                    border: 2px dashed #888; text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>⚪</div>
            <h3 style='color: #888; margin: 0.5rem 0;'>QA System Status: Unknown</h3>
            <p style='color: #666; margin: 0;'>Run synthetic tests to verify system health</p>
        </div>
        """

    pass_rate = results.get('pass_rate', 0)

    if pass_rate >= 95:
        light_emoji = "🟢"
        status_text = "OPERATIONAL"
        status_color = "#00FF00"
        bg_color = "rgba(0,255,0,0.05)"
        border_color = "#00FF00"
    elif pass_rate >= 80:
        light_emoji = "🟡"
        status_text = "DEGRADED - Investigate"
        status_color = "#FFD700"
        bg_color = "rgba(255,215,0,0.05)"
        border_color = "#FFD700"
    else:
        light_emoji = "🔴"
        status_text = "CRITICAL FAILURE"
        status_color = "#FF0000"
        bg_color = "rgba(255,0,0,0.05)"
        border_color = "#FF0000"

    return f"""
    <div style='background: {bg_color}; padding: 2rem; border-radius: 15px;
                border: 3px solid {border_color}; text-align: center;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>{light_emoji}</div>
        <h3 style='color: {status_color}; margin: 0.5rem 0;'>QA System: {status_text}</h3>
        <p style='color: #666; font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;'>{pass_rate:.1f}% Pass Rate</p>
        <p style='color: #666; margin: 0;'>{results.get('passed', 0)}/{results.get('total', 0)} tests passing</p>
        <p style='color: #888; font-size: 0.85rem; margin-top: 1rem;'>Last tested: {results.get('timestamp', 'Never')}</p>
    </div>
    """
