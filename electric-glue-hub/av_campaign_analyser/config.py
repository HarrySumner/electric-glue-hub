"""
Configuration for AV Campaign Analyser
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)


class AVConfig:
    """AV Campaign Analyser Configuration"""

    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # Analysis Parameters
    ANOMALY_THRESHOLD_STD_DEV = 2.5  # Conversions >2.5 std devs = anomaly
    REGIONAL_UPLIFT_THRESHOLD = 10  # % uplift to consider significant

    # Data validation
    REQUIRED_FIELDS = ['date', 'bookings']
    OPTIONAL_FIELDS = ['revenue', 'postcode', 'search_impressions', 'search_clicks', 'brand_searches']

    # UI Settings
    THEME = "light"  # light or dark

    @classmethod
    def validate(cls):
        """
        Validate configuration

        Returns:
            (is_valid, error_message)
        """
        if not cls.ANTHROPIC_API_KEY:
            return False, "ANTHROPIC_API_KEY not set in environment"

        if not cls.ANTHROPIC_API_KEY.startswith("sk-ant-"):
            return False, "ANTHROPIC_API_KEY appears to be invalid"

        return True, None

    @classmethod
    def get_analysis_params(cls):
        """Get analysis parameters"""
        return {
            "anomaly_threshold": cls.ANOMALY_THRESHOLD_STD_DEV,
            "regional_threshold": cls.REGIONAL_UPLIFT_THRESHOLD
        }


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("AV CAMPAIGN ANALYSER - CONFIGURATION TEST")
    print("="*60)

    is_valid, error = AVConfig.validate()

    if is_valid:
        print("\n✅ Configuration valid")
        print(f"   API Key: {AVConfig.ANTHROPIC_API_KEY[:20]}...")
        print(f"   Anomaly Threshold: {AVConfig.ANOMALY_THRESHOLD_STD_DEV} std devs")
        print(f"   Regional Threshold: {AVConfig.REGIONAL_UPLIFT_THRESHOLD}%")
    else:
        print(f"\n❌ Configuration error: {error}")
