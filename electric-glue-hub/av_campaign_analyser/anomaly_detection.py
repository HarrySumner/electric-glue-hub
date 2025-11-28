"""
Anomaly Detection for AV Campaign Analyser
Detects conversion spikes and allows user to triage them
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ConversionAnomaly:
    """Represents a detected conversion spike"""
    date: str
    conversions: int
    baseline_avg: float
    baseline_std: float
    z_score: float
    increase_pct: float
    is_excluded: bool = False
    explanation: Optional[str] = None

    def to_dict(self):
        return {
            'date': self.date,
            'conversions': self.conversions,
            'baseline_avg': round(self.baseline_avg, 2),
            'baseline_std': round(self.baseline_std, 2),
            'z_score': round(self.z_score, 2),
            'increase_pct': round(self.increase_pct, 2),
            'is_excluded': self.is_excluded,
            'explanation': self.explanation
        }


class AnomalyDetector:
    """
    Detects anomalous conversion spikes in campaign data.

    Uses rolling statistics to identify dates where conversions are
    significantly higher than baseline (e.g., due to PR events like
    Dragons Den appearances, influencer posts, etc.)
    """

    def __init__(self, threshold_std_dev: float = 2.5):
        """
        Args:
            threshold_std_dev: Number of standard deviations for anomaly detection
        """
        self.threshold = threshold_std_dev
        self.anomalies: List[ConversionAnomaly] = []

    def detect_anomalies(
        self,
        data: pd.DataFrame,
        conversion_col: str = 'bookings',
        date_col: str = 'date',
        window: int = 7
    ) -> List[ConversionAnomaly]:
        """
        Detect conversion anomalies using rolling statistics.

        Args:
            data: DataFrame with conversion data
            conversion_col: Name of conversion column
            date_col: Name of date column
            window: Rolling window size for baseline calculation (days)

        Returns:
            List of ConversionAnomaly objects
        """
        df = data.copy()

        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
            df[date_col] = pd.to_datetime(df[date_col])

        # Sort by date
        df = df.sort_values(date_col)

        # Calculate rolling statistics (backward-looking, excluding current point)
        # This prevents the spike from inflating its own baseline
        df['rolling_mean'] = df[conversion_col].shift(1).rolling(window=window, min_periods=3).mean()
        df['rolling_std'] = df[conversion_col].shift(1).rolling(window=window, min_periods=3).std()

        # Calculate z-scores
        df['z_score'] = (df[conversion_col] - df['rolling_mean']) / df['rolling_std']

        # Calculate percentage increase from baseline
        df['increase_pct'] = ((df[conversion_col] - df['rolling_mean']) / df['rolling_mean']) * 100

        # Identify anomalies
        anomalies = []

        for idx, row in df.iterrows():
            # Skip if not enough data for rolling window
            if pd.isna(row['z_score']):
                continue

            # Flag if z-score exceeds threshold
            if row['z_score'] > self.threshold:
                anomaly = ConversionAnomaly(
                    date=row[date_col].strftime('%Y-%m-%d'),
                    conversions=int(row[conversion_col]),
                    baseline_avg=float(row['rolling_mean']),
                    baseline_std=float(row['rolling_std']),
                    z_score=float(row['z_score']),
                    increase_pct=float(row['increase_pct'])
                )
                anomalies.append(anomaly)

        self.anomalies = anomalies
        return anomalies

    def get_clean_data(
        self,
        data: pd.DataFrame,
        excluded_dates: List[str],
        conversion_col: str = 'bookings',
        date_col: str = 'date'
    ) -> pd.DataFrame:
        """
        Return dataset with excluded anomaly dates removed.

        Args:
            data: Original DataFrame
            excluded_dates: List of dates to exclude (YYYY-MM-DD format)
            conversion_col: Name of conversion column
            date_col: Name of date column

        Returns:
            Cleaned DataFrame
        """
        df = data.copy()

        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
            df[date_col] = pd.to_datetime(df[date_col])

        # Convert excluded_dates to datetime
        excluded_dates_dt = pd.to_datetime(excluded_dates)

        # Filter out excluded dates
        clean_df = df[~df[date_col].isin(excluded_dates_dt)]

        return clean_df

    def get_summary(self) -> Dict:
        """Get anomaly detection summary"""
        if not self.anomalies:
            return {
                "total_anomalies": 0,
                "message": "No anomalies detected"
            }

        excluded_count = sum(1 for a in self.anomalies if a.is_excluded)

        return {
            "total_anomalies": len(self.anomalies),
            "excluded": excluded_count,
            "included": len(self.anomalies) - excluded_count,
            "avg_z_score": np.mean([a.z_score for a in self.anomalies]),
            "max_z_score": max([a.z_score for a in self.anomalies]),
            "dates": [a.date for a in self.anomalies]
        }


# Example usage and testing
if __name__ == "__main__":
    # Test data with obvious spike
    dates = pd.date_range('2024-06-01', periods=30, freq='D')

    # Normal conversions around 20-30
    np.random.seed(42)
    conversions = np.random.randint(20, 30, size=30).astype(float)

    # Add spikes on specific dates (Dragons Den effect)
    conversions[26] = 150.0  # June 27th - massive spike
    conversions[27] = 120.0  # June 28th - continued spike

    # Aggregate by date (sum bookings per day)
    data = pd.DataFrame({
        'date': dates,
        'bookings': conversions
    })

    # Group by date and sum (in case of multiple entries per day)
    data = data.groupby('date', as_index=False).agg({'bookings': 'sum'})

    print("="*60)
    print("ANOMALY DETECTION TEST")
    print("="*60)
    print("\nSample data:")
    print(data.tail(10))

    # Detect anomalies
    detector = AnomalyDetector(threshold_std_dev=2.5)
    anomalies = detector.detect_anomalies(data)

    print(f"\n[INFO] DETECTED {len(anomalies)} ANOMALIES:")
    print("="*60)

    for anomaly in anomalies:
        print(f"\n[RED] Date: {anomaly.date}")
        print(f"   Conversions: {anomaly.conversions}")
        print(f"   Baseline: {anomaly.baseline_avg:.1f} +/- {anomaly.baseline_std:.1f}")
        print(f"   Z-score: {anomaly.z_score:.2f}")
        print(f"   Increase: +{anomaly.increase_pct:.1f}%")

    # Test excluding anomalies
    excluded_dates = [a.date for a in anomalies]
    clean_data = detector.get_clean_data(data, excluded_dates)

    print(f"\n[OK] CLEAN DATA:")
    print(f"Original rows: {len(data)}")
    print(f"Clean rows: {len(clean_data)}")
    print(f"Excluded: {len(data) - len(clean_data)} dates")

    summary = detector.get_summary()
    print(f"\nSummary: {summary}")

    print("\n[SUCCESS] Anomaly detection test completed")
