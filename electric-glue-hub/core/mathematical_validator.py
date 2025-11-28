"""
Mathematical Validation - Rules-based checks that don't rely on LLMs
Catches obviously impossible data before LLM validation
Part of the TrustCheck system to prevent synthetic data issues
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class FlagSeverity(Enum):
    """Severity levels for validation flags"""
    GREEN = "green"
    AMBER = "amber"
    RED = "red"


@dataclass
class ValidationFlag:
    """Represents a validation issue found in the data"""
    severity: FlagSeverity
    field: str
    issue: str
    expected: Optional[str] = None
    actual: Optional[str] = None
    recommendation: Optional[str] = None


class MathematicalValidator:
    """
    Rules-based mathematical validation for campaign data.
    Catches impossible data patterns without relying on LLM.

    This is the FIRST line of defense against synthetic/fabricated data.
    """

    def __init__(self):
        self.flags: List[ValidationFlag] = []

    def validate_report(self, data: Dict[str, Any]) -> List[ValidationFlag]:
        """
        Run all mathematical validation checks on campaign data.

        Args:
            data: Dictionary containing report metrics (impressions, clicks, conversions, etc.)

        Returns:
            List of ValidationFlag objects
        """
        self.flags = []

        # Run all validation checks
        self._validate_funnel_logic(data)
        self._validate_percentages(data)
        self._validate_rates(data)
        self._validate_consistency(data)
        self._validate_ranges(data)
        self._validate_dates(data)

        return self.flags

    def _validate_funnel_logic(self, data: Dict):
        """
        Validate that funnel metrics follow logical order:
        Impressions >= Clicks >= Conversions

        This catches the most obvious fabrications.
        """
        impressions = data.get('impressions', 0)
        clicks = data.get('clicks', 0)
        conversions = data.get('conversions', 0)

        # Clicks cannot exceed impressions
        if clicks > impressions and impressions > 0:
            self.flags.append(ValidationFlag(
                severity=FlagSeverity.RED,
                field="clicks",
                issue="Clicks exceed impressions - mathematically impossible",
                expected=f"<= {impressions:,}",
                actual=f"{clicks:,}",
                recommendation="Verify data source. Clicks cannot exceed impressions."
            ))

        # Conversions cannot exceed clicks
        if conversions > clicks and clicks > 0:
            self.flags.append(ValidationFlag(
                severity=FlagSeverity.RED,
                field="conversions",
                issue="Conversions exceed clicks - mathematically impossible",
                expected=f"<= {clicks:,}",
                actual=f"{conversions:,}",
                recommendation="Verify conversion tracking. Users must click before converting."
            ))

        # Conversions cannot exceed impressions
        if conversions > impressions and impressions > 0:
            self.flags.append(ValidationFlag(
                severity=FlagSeverity.RED,
                field="conversions",
                issue="Conversions exceed impressions - mathematically impossible",
                expected=f"<= {impressions:,}",
                actual=f"{conversions:,}",
                recommendation="Critical data error. Review all metrics."
            ))

    def _validate_percentages(self, data: Dict):
        """
        Validate that percentage fields are between 0-100%
        """
        percentage_fields = [
            'ctr', 'conversion_rate', 'bounce_rate',
            'engagement_rate', 'click_through_rate'
        ]

        for field in percentage_fields:
            if field in data:
                value = data[field]

                # Remove % sign if present
                if isinstance(value, str):
                    value = float(value.strip('%'))

                if value < 0:
                    self.flags.append(ValidationFlag(
                        severity=FlagSeverity.RED,
                        field=field,
                        issue=f"Negative percentage value",
                        expected="0-100%",
                        actual=f"{value}%",
                        recommendation="Percentages cannot be negative."
                    ))

                if value > 100:
                    self.flags.append(ValidationFlag(
                        severity=FlagSeverity.RED,
                        field=field,
                        issue=f"Percentage exceeds 100%",
                        expected="0-100%",
                        actual=f"{value}%",
                        recommendation="Percentages cannot exceed 100%."
                    ))

    def _validate_rates(self, data: Dict):
        """
        Validate calculated rates match raw data.
        E.g., CTR = (Clicks / Impressions) × 100
        """
        impressions = data.get('impressions', 0)
        clicks = data.get('clicks', 0)
        conversions = data.get('conversions', 0)

        # Validate CTR if provided
        if 'ctr' in data and impressions > 0:
            stated_ctr = data['ctr']
            if isinstance(stated_ctr, str):
                stated_ctr = float(stated_ctr.strip('%'))

            calculated_ctr = (clicks / impressions) * 100

            # Allow 0.1% tolerance for rounding
            if abs(stated_ctr - calculated_ctr) > 0.1:
                self.flags.append(ValidationFlag(
                    severity=FlagSeverity.RED,
                    field="ctr",
                    issue="Stated CTR doesn't match calculated value",
                    expected=f"{calculated_ctr:.2f}%",
                    actual=f"{stated_ctr:.2f}%",
                    recommendation=f"CTR should be ({clicks:,} / {impressions:,}) × 100 = {calculated_ctr:.2f}%"
                ))

        # Validate Conversion Rate if provided
        if 'conversion_rate' in data and clicks > 0:
            stated_cvr = data['conversion_rate']
            if isinstance(stated_cvr, str):
                stated_cvr = float(stated_cvr.strip('%'))

            calculated_cvr = (conversions / clicks) * 100

            if abs(stated_cvr - calculated_cvr) > 0.1:
                self.flags.append(ValidationFlag(
                    severity=FlagSeverity.RED,
                    field="conversion_rate",
                    issue="Stated conversion rate doesn't match calculated value",
                    expected=f"{calculated_cvr:.2f}%",
                    actual=f"{stated_cvr:.2f}%",
                    recommendation=f"CVR should be ({conversions:,} / {clicks:,}) × 100 = {calculated_cvr:.2f}%"
                ))

    def _validate_consistency(self, data: Dict):
        """
        Validate internal consistency of metrics
        """
        # Check if cost per click matches spend / clicks
        if all(k in data for k in ['spend', 'clicks', 'cpc']):
            spend = data['spend']
            clicks = data['clicks']
            stated_cpc = data['cpc']

            if clicks > 0:
                calculated_cpc = spend / clicks

                # Allow 1% tolerance
                if abs(stated_cpc - calculated_cpc) / calculated_cpc > 0.01:
                    self.flags.append(ValidationFlag(
                        severity=FlagSeverity.AMBER,
                        field="cpc",
                        issue="CPC inconsistent with spend and clicks",
                        expected=f"£{calculated_cpc:.2f}",
                        actual=f"£{stated_cpc:.2f}",
                        recommendation="Verify CPC calculation"
                    ))

        # Check if ROAS matches revenue / spend
        if all(k in data for k in ['revenue', 'spend', 'roas']):
            revenue = data['revenue']
            spend = data['spend']
            stated_roas = data['roas']

            if spend > 0:
                calculated_roas = revenue / spend

                if abs(stated_roas - calculated_roas) / calculated_roas > 0.01:
                    self.flags.append(ValidationFlag(
                        severity=FlagSeverity.AMBER,
                        field="roas",
                        issue="ROAS inconsistent with revenue and spend",
                        expected=f"{calculated_roas:.2f}",
                        actual=f"{stated_roas:.2f}",
                        recommendation="Verify ROAS calculation"
                    ))

    def _validate_ranges(self, data: Dict):
        """
        Validate that metrics are within plausible ranges
        """
        # CTR should rarely exceed 20% (even for brand search campaigns)
        if 'ctr' in data:
            ctr = data['ctr']
            if isinstance(ctr, str):
                ctr = float(ctr.strip('%'))

            if ctr > 20:
                self.flags.append(ValidationFlag(
                    severity=FlagSeverity.AMBER,
                    field="ctr",
                    issue="CTR unusually high (>20%)",
                    expected="<20% (typical range: 1-10%)",
                    actual=f"{ctr}%",
                    recommendation="Verify CTR is correct. Values >20% are extremely rare."
                ))

        # Conversion rate should rarely exceed 20%
        if 'conversion_rate' in data:
            cvr = data['conversion_rate']
            if isinstance(cvr, str):
                cvr = float(cvr.strip('%'))

            if cvr > 20:
                self.flags.append(ValidationFlag(
                    severity=FlagSeverity.AMBER,
                    field="conversion_rate",
                    issue="Conversion rate unusually high (>20%)",
                    expected="<20% (typical range: 1-10%)",
                    actual=f"{cvr}%",
                    recommendation="Verify conversion tracking. Values >20% are very rare."
                ))

        # Bounce rate should be 0-100%
        if 'bounce_rate' in data:
            bounce = data['bounce_rate']
            if isinstance(bounce, str):
                bounce = float(bounce.strip('%'))

            if bounce < 0 or bounce > 100:
                self.flags.append(ValidationFlag(
                    severity=FlagSeverity.RED,
                    field="bounce_rate",
                    issue="Bounce rate outside valid range",
                    expected="0-100%",
                    actual=f"{bounce}%",
                    recommendation="Bounce rate must be between 0% and 100%"
                ))

    def _validate_dates(self, data: Dict):
        """
        Validate date fields are properly formatted and logical
        """
        from datetime import datetime

        # Check campaign start/end dates
        if 'campaign_start' in data and 'campaign_end' in data:
            try:
                start = datetime.fromisoformat(str(data['campaign_start']))
                end = datetime.fromisoformat(str(data['campaign_end']))

                if end < start:
                    self.flags.append(ValidationFlag(
                        severity=FlagSeverity.RED,
                        field="campaign_dates",
                        issue="Campaign end date before start date",
                        expected=f"End date after {start.date()}",
                        actual=f"End date: {end.date()}",
                        recommendation="Verify campaign dates are correct"
                    ))
            except (ValueError, TypeError):
                # Date parsing failed - not critical
                pass

    def get_summary(self) -> Dict:
        """Get validation summary with traffic light status"""
        red_count = sum(1 for f in self.flags if f.severity == FlagSeverity.RED)
        amber_count = sum(1 for f in self.flags if f.severity == FlagSeverity.AMBER)

        if red_count > 0:
            status = "RED - Critical errors found"
            color = "🔴"
        elif amber_count > 0:
            status = "AMBER - Warnings present"
            color = "🟡"
        else:
            status = "GREEN - No mathematical errors detected"
            color = "🟢"

        return {
            "status": status,
            "color": color,
            "red_flags": red_count,
            "amber_flags": amber_count,
            "total_flags": len(self.flags),
            "passed": red_count == 0
        }


# Example usage and testing
if __name__ == "__main__":
    print("="*60)
    print("MATHEMATICAL VALIDATOR TEST")
    print("="*60)

    # Test case 1: Obviously impossible data
    print("\n TEST 1: Impossible data (synthetic/fabricated)")
    print("="*60)

    impossible_data = {
        'impressions': 1000,
        'clicks': 5000,  # IMPOSSIBLE - more clicks than impressions
        'conversions': 10000,  # IMPOSSIBLE - more conversions than clicks
        'ctr': 0.5,  # INCONSISTENT - should be 500% if clicks=5000
    }

    validator = MathematicalValidator()
    flags = validator.validate_report(impossible_data)

    print(f"\nFound {len(flags)} issues:\n")
    for flag in flags:
        print(f"[{flag.severity.value.upper()}] {flag.field}")
        print(f"  Issue: {flag.issue}")
        print(f"  Expected: {flag.expected}")
        print(f"  Actual: {flag.actual}")
        print(f"  Recommendation: {flag.recommendation}")
        print()

    summary = validator.get_summary()
    print(f"{summary['color']} {summary['status']}")
    print(f"Red flags: {summary['red_flags']}, Amber flags: {summary['amber_flags']}")

    # Test case 2: Valid data
    print("\n\nTEST 2: Valid data")
    print("="*60)

    valid_data = {
        'impressions': 10000,
        'clicks': 500,
        'conversions': 25,
        'ctr': 5.0,  # Correct: (500/10000)*100 = 5%
        'conversion_rate': 5.0,  # Correct: (25/500)*100 = 5%
    }

    validator2 = MathematicalValidator()
    flags2 = validator2.validate_report(valid_data)

    if flags2:
        print(f"\nFound {len(flags2)} issues")
        for flag in flags2:
            print(f"[{flag.severity.value.upper()}] {flag.field}: {flag.issue}")
    else:
        print("\n✅ No issues found - data is mathematically valid")

    summary2 = validator2.get_summary()
    print(f"\n{summary2['color']} {summary2['status']}")

    # Test case 3: Inconsistent calculations
    print("\n\nTEST 3: Inconsistent calculations")
    print("="*60)

    inconsistent_data = {
        'impressions': 10000,
        'clicks': 500,
        'ctr': 10.0,  # WRONG - should be 5%, not 10%
        'spend': 1000,
        'cpc': 5.0,  # WRONG - should be 1000/500 = £2.00
    }

    validator3 = MathematicalValidator()
    flags3 = validator3.validate_report(inconsistent_data)

    print(f"\nFound {len(flags3)} issues:\n")
    for flag in flags3:
        print(f"[{flag.severity.value.upper()}] {flag.field}")
        print(f"  Issue: {flag.issue}")
        print(f"  Expected: {flag.expected}")
        print(f"  Actual: {flag.actual}")
        print()

    summary3 = validator3.get_summary()
    print(f"{summary3['color']} {summary3['status']}")
