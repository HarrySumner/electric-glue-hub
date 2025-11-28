"""
Regional Analysis for AV Campaign Analyser
Compares campaign regions vs control regions to measure regional uplift
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class RegionalAnalysisResult:
    """Results of regional vs national analysis"""
    campaign_region_conversions: int
    control_region_conversions: int
    campaign_region_avg: float
    control_region_avg: float
    uplift_pct: float
    is_significant: bool
    interpretation: str
    campaign_dates: Tuple[str, str]
    regions_analyzed: List[str]


class RegionalAnalyzer:
    """
    Analyzes regional campaign performance vs national baseline.

    Use case: AV campaign only aired in specific regions (e.g., London, SW England)
    This compares those regions vs the rest of the country to isolate AV impact.
    """

    def __init__(self, uplift_threshold: float = 10.0):
        """
        Args:
            uplift_threshold: Minimum % uplift to consider significant
        """
        self.uplift_threshold = uplift_threshold

    def extract_postcode_prefix(self, postcode: str, length: int = 2) -> str:
        """
        Extract postcode prefix (first 1-2 characters).

        Args:
            postcode: Full or partial postcode (e.g., "SW1 1AA", "E1", "N")
            length: Number of characters to extract (1 or 2)

        Returns:
            Postcode prefix (uppercase, e.g., "SW", "E")
        """
        if pd.isna(postcode):
            return ""

        postcode = str(postcode).upper().strip()

        # Remove spaces
        postcode = postcode.replace(" ", "")

        # Extract prefix (alpha characters only)
        if length == 1:
            return postcode[0] if len(postcode) >= 1 and postcode[0].isalpha() else ""
        else:
            # Extract up to 2 alpha characters
            prefix = ""
            for char in postcode:
                if char.isalpha():
                    prefix += char
                    if len(prefix) == 2:
                        break
            return prefix

    def parse_region_input(self, region_input: str) -> List[str]:
        """
        Parse comma-separated region input.

        Args:
            region_input: e.g., "SW, E, N, W1, EC"

        Returns:
            List of uppercase region codes
        """
        if not region_input:
            return []

        regions = [r.strip().upper() for r in region_input.split(',')]
        return [r for r in regions if r]  # Remove empty strings

    def segment_data(
        self,
        data: pd.DataFrame,
        campaign_regions: List[str],
        postcode_col: str = 'postcode',
        date_col: str = 'date',
        conversion_col: str = 'bookings'
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Segment data into campaign regions vs control regions.

        Args:
            data: Full dataset
            campaign_regions: List of postcode prefixes for campaign regions
            postcode_col: Name of postcode column
            date_col: Name of date column
            conversion_col: Name of conversion column

        Returns:
            (campaign_data, control_data) tuple
        """
        df = data.copy()

        # Ensure date is datetime
        if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
            df[date_col] = pd.to_datetime(df[date_col])

        # Extract postcode prefix
        df['postcode_prefix'] = df[postcode_col].apply(
            lambda x: self.extract_postcode_prefix(x, length=2)
        )

        # Segment
        campaign_data = df[df['postcode_prefix'].isin(campaign_regions)]
        control_data = df[~df['postcode_prefix'].isin(campaign_regions)]

        return campaign_data, control_data

    def analyze_regional_uplift(
        self,
        data: pd.DataFrame,
        campaign_regions: List[str],
        campaign_start: str,
        campaign_end: str,
        postcode_col: str = 'postcode',
        date_col: str = 'date',
        conversion_col: str = 'bookings'
    ) -> RegionalAnalysisResult:
        """
        Analyze regional uplift during campaign period.

        Args:
            data: Full dataset
            campaign_regions: List of postcode prefixes where campaign ran
            campaign_start: Campaign start date (YYYY-MM-DD)
            campaign_end: Campaign end date (YYYY-MM-DD)
            postcode_col: Name of postcode column
            date_col: Name of date column
            conversion_col: Name of conversion column

        Returns:
            RegionalAnalysisResult object
        """
        # Segment data
        campaign_data, control_data = self.segment_data(
            data, campaign_regions, postcode_col, date_col, conversion_col
        )

        # Filter to campaign period
        campaign_start_dt = pd.to_datetime(campaign_start)
        campaign_end_dt = pd.to_datetime(campaign_end)

        campaign_period = campaign_data[
            (campaign_data[date_col] >= campaign_start_dt) &
            (campaign_data[date_col] <= campaign_end_dt)
        ]

        control_period = control_data[
            (control_data[date_col] >= campaign_start_dt) &
            (control_data[date_col] <= campaign_end_dt)
        ]

        # Calculate metrics
        campaign_total = campaign_period[conversion_col].sum()
        control_total = control_period[conversion_col].sum()

        campaign_days = (campaign_end_dt - campaign_start_dt).days + 1
        campaign_avg = campaign_total / campaign_days if campaign_days > 0 else 0

        control_days = len(control_period[date_col].unique())
        control_avg = control_total / control_days if control_days > 0 else 0

        # Calculate uplift
        if control_avg > 0:
            uplift_pct = ((campaign_avg - control_avg) / control_avg) * 100
        else:
            uplift_pct = 0

        # Determine if significant
        is_significant = abs(uplift_pct) >= self.uplift_threshold

        # Interpretation
        if uplift_pct > self.uplift_threshold:
            interpretation = f"Strong positive regional uplift ({uplift_pct:.1f}%) indicates likely AV campaign impact"
        elif uplift_pct > 5:
            interpretation = f"Moderate regional uplift ({uplift_pct:.1f}%) suggests some AV impact"
        elif uplift_pct > -5:
            interpretation = f"Minimal regional difference ({uplift_pct:.1f}%) - inconclusive"
        else:
            interpretation = f"Negative regional performance ({uplift_pct:.1f}%) - campaign may not be effective"

        return RegionalAnalysisResult(
            campaign_region_conversions=int(campaign_total),
            control_region_conversions=int(control_total),
            campaign_region_avg=float(campaign_avg),
            control_region_avg=float(control_avg),
            uplift_pct=float(uplift_pct),
            is_significant=is_significant,
            interpretation=interpretation,
            campaign_dates=(campaign_start, campaign_end),
            regions_analyzed=campaign_regions
        )

    def get_region_breakdown(
        self,
        data: pd.DataFrame,
        postcode_col: str = 'postcode',
        conversion_col: str = 'bookings'
    ) -> pd.DataFrame:
        """
        Get breakdown of conversions by postcode prefix.

        Args:
            data: Dataset
            postcode_col: Name of postcode column
            conversion_col: Name of conversion column

        Returns:
            DataFrame with region breakdown
        """
        df = data.copy()

        # Extract postcode prefix
        df['postcode_prefix'] = df[postcode_col].apply(
            lambda x: self.extract_postcode_prefix(x, length=2)
        )

        # Group by prefix
        breakdown = df.groupby('postcode_prefix')[conversion_col].agg([
            ('total_conversions', 'sum'),
            ('avg_per_day', 'mean'),
            ('days', 'count')
        ]).reset_index()

        # Sort by total conversions
        breakdown = breakdown.sort_values('total_conversions', ascending=False)

        return breakdown


# Example usage and testing
if __name__ == "__main__":
    # Test data
    dates = pd.date_range('2024-06-01', periods=30, freq='D')

    # Create synthetic data with regional differences
    np.random.seed(42)

    data = []
    for date in dates:
        # Campaign regions (SW, W1) - higher conversions during campaign
        if date >= pd.Timestamp('2024-06-15') and date <= pd.Timestamp('2024-06-25'):
            # Campaign period - uplift in campaign regions
            data.append({'date': date, 'bookings': 35, 'postcode': 'SW1 1AA'})
            data.append({'date': date, 'bookings': 30, 'postcode': 'W1A 1AA'})
            # Control regions - normal
            data.append({'date': date, 'bookings': 20, 'postcode': 'E1 6AN'})
            data.append({'date': date, 'bookings': 18, 'postcode': 'N1 9AG'})
        else:
            # Pre/post campaign - all regions similar
            data.append({'date': date, 'bookings': 20, 'postcode': 'SW1 1AA'})
            data.append({'date': date, 'bookings': 18, 'postcode': 'W1A 1AA'})
            data.append({'date': date, 'bookings': 19, 'postcode': 'E1 6AN'})
            data.append({'date': date, 'bookings': 20, 'postcode': 'N1 9AG'})

    df = pd.DataFrame(data)

    print("="*60)
    print("REGIONAL ANALYSIS TEST")
    print("="*60)
    print("\nSample data:")
    print(df.head(20))

    # Analyze
    analyzer = RegionalAnalyzer(uplift_threshold=10.0)

    campaign_regions = ['SW', 'W1']

    result = analyzer.analyze_regional_uplift(
        data=df,
        campaign_regions=campaign_regions,
        campaign_start='2024-06-15',
        campaign_end='2024-06-25'
    )

    print(f"\n[INFO] REGIONAL ANALYSIS RESULTS:")
    print("="*60)
    print(f"Campaign Regions: {', '.join(result.regions_analyzed)}")
    print(f"Campaign Period: {result.campaign_dates[0]} to {result.campaign_dates[1]}")
    print(f"\nCampaign Region Performance:")
    print(f"  Total Conversions: {result.campaign_region_conversions}")
    print(f"  Avg per Day: {result.campaign_region_avg:.1f}")
    print(f"\nControl Region Performance:")
    print(f"  Total Conversions: {result.control_region_conversions}")
    print(f"  Avg per Day: {result.control_region_avg:.1f}")
    print(f"\nUplift: {result.uplift_pct:+.1f}%")
    print(f"Significant: {'Yes' if result.is_significant else 'No'}")
    print(f"\nInterpretation: {result.interpretation}")

    # Get region breakdown
    breakdown = analyzer.get_region_breakdown(df)
    print(f"\n[INFO] REGION BREAKDOWN:")
    print("="*60)
    print(breakdown)

    print("\n[SUCCESS] Regional analysis test completed")
