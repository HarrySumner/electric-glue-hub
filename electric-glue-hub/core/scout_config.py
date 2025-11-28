"""
Scout Configuration Management
Handles API keys and environment variables securely for Scout Research Agent
"""

import os
from typing import Optional, Tuple
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)


class ScoutConfig:
    """Configuration class for Scout Research Agent"""

    # Anthropic API Configuration
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    ANTHROPIC_MAX_TOKENS: int = int(os.getenv("ANTHROPIC_MAX_TOKENS", "8000"))
    ANTHROPIC_TIMEOUT: int = int(os.getenv("ANTHROPIC_TIMEOUT", "60"))

    # Research Configuration
    RESEARCH_DEPTH_SETTINGS = {
        "Quick": {
            "search_queries": 15,
            "min_sources": 50,
            "min_facts": 25,
            "estimated_time": "5-10 minutes"
        },
        "Balanced": {
            "search_queries": 25,
            "min_sources": 100,
            "min_facts": 35,
            "estimated_time": "15-20 minutes"
        },
        "Deep Dive": {
            "search_queries": 40,
            "min_sources": 150,
            "min_facts": 50,
            "estimated_time": "30-45 minutes"
        }
    }

    # Quality Standards
    QUALITY_STANDARDS = {
        "minimum_sources": 10,
        "minimum_facts": 30,
        "minimum_verification_rate": 0.5,
        "minimum_insight_ratio": 0.33,
        "minimum_overall_quality": 85,
    }

    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> Tuple[bool, Optional[str]]:
        """
        Validate configuration

        Returns:
            (is_valid, error_message)
        """
        if not cls.ANTHROPIC_API_KEY:
            return False, "ANTHROPIC_API_KEY not set in environment. Please check your .env file."

        if not cls.ANTHROPIC_API_KEY.startswith("sk-ant-"):
            return False, "ANTHROPIC_API_KEY appears to be invalid (should start with 'sk-ant-')"

        return True, None

    @classmethod
    def test_api_connection(cls) -> Tuple[bool, str]:
        """
        Test API connection with a minimal request

        Returns:
            (success, message)
        """
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=cls.ANTHROPIC_API_KEY)

            # Minimal test request
            response = client.messages.create(
                model=cls.ANTHROPIC_MODEL,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )

            return True, "✅ API connection successful"

        except Exception as e:
            return False, f"❌ API connection failed: {str(e)}"

    @classmethod
    def get_research_config(cls, depth: str) -> dict:
        """
        Get research configuration for a given depth level

        Args:
            depth: Research depth ("Quick", "Balanced", or "Deep Dive")

        Returns:
            Configuration dictionary
        """
        return cls.RESEARCH_DEPTH_SETTINGS.get(depth, cls.RESEARCH_DEPTH_SETTINGS["Balanced"])

    @classmethod
    def get_quality_standards(cls) -> dict:
        """Get quality standards for research validation"""
        return cls.QUALITY_STANDARDS.copy()


# Validate configuration on import (but don't fail)
_is_valid, _error = ScoutConfig.validate()
if not _is_valid and ScoutConfig.DEBUG:
    print(f"⚠️  Scout Configuration Warning: {_error}")


# Example usage and testing
if __name__ == "__main__":
    print("="*60)
    print("SCOUT CONFIGURATION TEST")
    print("="*60)

    # Validate configuration
    is_valid, error = ScoutConfig.validate()
    if is_valid:
        print("✅ Configuration valid")
        print(f"   Model: {ScoutConfig.ANTHROPIC_MODEL}")
        print(f"   Max Tokens: {ScoutConfig.ANTHROPIC_MAX_TOKENS}")
        print(f"   Timeout: {ScoutConfig.ANTHROPIC_TIMEOUT}s")

        # Test API connection
        print("\nTesting API connection...")
        success, message = ScoutConfig.test_api_connection()
        print(f"   {message}")

        # Show research configurations
        print("\nResearch Depth Configurations:")
        for depth, config in ScoutConfig.RESEARCH_DEPTH_SETTINGS.items():
            print(f"\n   {depth}:")
            print(f"      - Search Queries: {config['search_queries']}")
            print(f"      - Min Sources: {config['min_sources']}")
            print(f"      - Min Facts: {config['min_facts']}")
            print(f"      - Estimated Time: {config['estimated_time']}")

        # Show quality standards
        print("\nQuality Standards:")
        for key, value in ScoutConfig.get_quality_standards().items():
            print(f"   - {key}: {value}")
    else:
        print(f"❌ Configuration error: {error}")
        print("\nPlease ensure ANTHROPIC_API_KEY is set in your .env file:")
        print("   1. Create/edit .env file in project root")
        print("   2. Add line: ANTHROPIC_API_KEY=sk-ant-...")
        print("   3. Restart the application")
