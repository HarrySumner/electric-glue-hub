"""
Data Agent - Intelligent data ingestion and preprocessing
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class DataAgent:
    """
    Intelligent agent for data ingestion, cleaning, and preprocessing.

    Responsibilities:
    - Parse CSV/Excel uploads
    - Auto-detect date columns and metrics
    - Handle missing values intelligently
    - Suggest potential covariates
    - Prepare time-aligned dataset
    """

    def __init__(self):
        self.raw_data = None
        self.processed_data = None
        self.metadata = {}
        self.suggestions = {}

    def ingest(self, file_path: str) -> Dict:
        """
        Ingest data from file.

        Parameters
        ----------
        file_path : str
            Path to CSV or Excel file

        Returns
        -------
        dict with ingestion results and suggestions
        """
        try:
            # Detect file type and load
            if file_path.endswith('.csv'):
                self.raw_data = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                self.raw_data = pd.read_excel(file_path)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported file format: {Path(file_path).suffix}'
                }

            # Analyze data
            analysis = self._analyze_data()

            return {
                'success': True,
                'shape': self.raw_data.shape,
                'columns': list(self.raw_data.columns),
                'analysis': analysis,
                'suggestions': self.suggestions
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _analyze_data(self) -> Dict:
        """Analyze uploaded data and make intelligent suggestions."""

        # Detect date columns
        date_candidates = self._detect_date_columns()

        # Detect numeric columns (potential metrics)
        numeric_cols = self._detect_numeric_columns()

        # Suggest target metric
        target_suggestion = self._suggest_target_metric(numeric_cols)

        # Suggest covariates
        covariate_suggestions = self._suggest_covariates(numeric_cols, target_suggestion)

        # Store suggestions
        self.suggestions = {
            'date_column': date_candidates[0] if date_candidates else None,
            'target_metric': target_suggestion,
            'covariates': covariate_suggestions,
            'all_date_candidates': date_candidates,
            'all_numeric_columns': numeric_cols
        }

        return {
            'n_rows': len(self.raw_data),
            'n_columns': len(self.raw_data.columns),
            'date_columns_found': len(date_candidates),
            'numeric_columns_found': len(numeric_cols),
            'missing_values': self.raw_data.isnull().sum().sum(),
            'date_range': self._get_date_range(date_candidates[0]) if date_candidates else None
        }

    def _detect_date_columns(self) -> List[str]:
        """Auto-detect date columns."""
        date_cols = []

        for col in self.raw_data.columns:
            # Check column name
            if any(kw in col.lower() for kw in ['date', 'time', 'day', 'week', 'month', 'year', 'period']):
                date_cols.append(col)
                continue

            # Try to parse as datetime
            try:
                pd.to_datetime(self.raw_data[col], errors='raise')
                date_cols.append(col)
            except:
                pass

        return date_cols

    def _detect_numeric_columns(self) -> List[str]:
        """Detect numeric columns that could be metrics."""
        return self.raw_data.select_dtypes(include=[np.number]).columns.tolist()

    def _suggest_target_metric(self, numeric_cols: List[str]) -> Optional[str]:
        """
        Suggest which column is likely the target metric.

        Heuristics:
        - Contains keywords: revenue, bookings, conversions, sales, orders
        - Has reasonable variance
        - No negatives (usually)
        """
        if not numeric_cols:
            return None

        # Keyword matching
        priority_keywords = ['booking', 'revenue', 'conversion', 'sale', 'order', 'transaction']

        for keyword in priority_keywords:
            for col in numeric_cols:
                if keyword in col.lower():
                    return col

        # If no keyword match, suggest column with highest variance
        variances = {col: self.raw_data[col].var() for col in numeric_cols}
        return max(variances, key=variances.get)

    def _suggest_covariates(self, numeric_cols: List[str], target: Optional[str]) -> List[str]:
        """
        Suggest potential covariates (control variables).

        Look for:
        - TV spend, marketing spend columns
        - External factors (flights, weather, economic)
        - Other channels
        """
        if not target:
            return []

        covariate_keywords = [
            'spend', 'budget', 'cost', 'investment',  # Marketing spend
            'digital', 'social', 'search', 'display',  # Other channels
            'flight', 'availability', 'capacity',      # Nielsen-specific confounders!
            'economic', 'gdp', 'unemployment',         # Economic indicators
            'weather', 'temperature', 'rain',          # Weather
            'competitor'                                # Competition
        ]

        suggestions = []
        for col in numeric_cols:
            if col == target:
                continue

            col_lower = col.lower()
            if any(kw in col_lower for kw in covariate_keywords):
                suggestions.append(col)

        return suggestions

    def _get_date_range(self, date_col: str) -> Dict:
        """Get date range from date column."""
        try:
            dates = pd.to_datetime(self.raw_data[date_col])
            return {
                'start': str(dates.min()),
                'end': str(dates.max()),
                'n_periods': len(dates),
                'frequency': pd.infer_freq(dates)
            }
        except:
            return None

    def prepare_for_analysis(
        self,
        date_col: str,
        target_col: str,
        covariate_cols: Optional[List[str]] = None,
        handle_missing: str = 'interpolate'
    ) -> pd.DataFrame:
        """
        Prepare data for Bayesian analysis.

        Parameters
        ----------
        date_col : str
            Date column name
        target_col : str
            Target metric column
        covariate_cols : list of str, optional
            Covariate columns
        handle_missing : str, default 'interpolate'
            How to handle missing values: 'interpolate', 'forward_fill', 'drop'

        Returns
        -------
        pd.DataFrame
            Prepared time series data with datetime index
        """
        # Select columns
        cols = [date_col, target_col]
        if covariate_cols:
            cols.extend(covariate_cols)

        df = self.raw_data[cols].copy()

        # Convert date column
        df[date_col] = pd.to_datetime(df[date_col])

        # Sort by date
        df = df.sort_values(date_col)

        # Set datetime index
        df = df.set_index(date_col)

        # Remove duplicates
        df = df[~df.index.duplicated(keep='first')]

        # Handle missing values
        if handle_missing == 'interpolate':
            df = df.interpolate(method='time', limit_direction='both')
        elif handle_missing == 'forward_fill':
            df = df.fillna(method='ffill').fillna(method='bfill')
        elif handle_missing == 'drop':
            df = df.dropna()

        self.processed_data = df
        self.metadata = {
            'target': target_col,
            'covariates': covariate_cols or [],
            'date_range': (df.index.min(), df.index.max()),
            'n_periods': len(df),
            'frequency': pd.infer_freq(df.index)
        }

        return df

    def get_summary_stats(self) -> Dict:
        """Get summary statistics of processed data."""
        if self.processed_data is None:
            return {}

        return {
            'target_stats': self.processed_data[self.metadata['target']].describe().to_dict(),
            'covariate_stats': {
                col: self.processed_data[col].describe().to_dict()
                for col in self.metadata['covariates']
            } if self.metadata['covariates'] else {},
            'correlation_matrix': self.processed_data.corr().to_dict()
        }

    def check_data_quality(self) -> Dict:
        """
        Check data quality and return score + issues.

        Returns quality score 0-100 and list of issues.
        """
        if self.processed_data is None:
            return {'score': 0, 'issues': ['No data processed']}

        issues = []
        score = 100

        # Check for missing values
        missing_pct = self.processed_data.isnull().sum().sum() / (
            len(self.processed_data) * len(self.processed_data.columns)
        ) * 100

        if missing_pct > 0:
            issues.append(f'{missing_pct:.1f}% missing values (after imputation)')
            score -= min(20, missing_pct * 2)

        # Check for sufficient data
        if len(self.processed_data) < 50:
            issues.append(f'Only {len(self.processed_data)} periods (minimum 50 recommended)')
            score -= 30

        # Check for outliers in target
        target = self.processed_data[self.metadata['target']]
        q1, q3 = target.quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers = ((target < q1 - 3 * iqr) | (target > q3 + 3 * iqr)).sum()

        if outliers > 0:
            outlier_pct = outliers / len(target) * 100
            if outlier_pct > 5:
                issues.append(f'{outliers} outliers detected ({outlier_pct:.1f}%)')
                score -= 15

        # Check for constant values
        if target.std() == 0:
            issues.append('Target metric has zero variance')
            score -= 50

        # Check date gaps
        expected_freq = pd.infer_freq(self.processed_data.index)
        if expected_freq:
            date_range = pd.date_range(
                self.processed_data.index.min(),
                self.processed_data.index.max(),
                freq=expected_freq
            )
            gaps = len(date_range) - len(self.processed_data)
            if gaps > 0:
                issues.append(f'{gaps} gaps in time series')
                score -= min(20, gaps)

        return {
            'score': max(0, score),
            'issues': issues if issues else ['All quality checks passed'],
            'recommendation': (
                'Excellent' if score >= 80 else
                'Good' if score >= 60 else
                'Acceptable' if score >= 40 else
                'Poor - Consider data cleaning'
            )
        }


def create_sample_data() -> pd.DataFrame:
    """
    Create sample TV campaign data for testing.

    Simulates Nielsen-style campaign with:
    - Daily bookings data
    - TV spend (starts mid-period)
    - Digital spend
    - Flight availability (confounder!)
    - Seasonal patterns
    """
    np.random.seed(42)

    # 12 months of daily data
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
    n_days = len(dates)

    # Base components
    trend = np.linspace(100, 150, n_days)
    seasonality_weekly = 20 * np.sin(2 * np.pi * np.arange(n_days) / 7)
    seasonality_monthly = 30 * np.sin(2 * np.pi * np.arange(n_days) / 30)
    noise = np.random.normal(0, 10, n_days)

    # Flight availability (the confounder!)
    flights_base = 150
    flights_increase_day = 180  # Day 180: new routes added
    flights = np.concatenate([
        np.full(flights_increase_day, flights_base) + np.random.normal(0, 5, flights_increase_day),
        np.full(n_days - flights_increase_day, flights_base + 30) + np.random.normal(0, 5, n_days - flights_increase_day)
    ])

    # Digital spend (constant)
    digital_spend = 5000 + np.random.normal(0, 500, n_days)

    # TV spend (campaign starts day 200)
    tv_campaign_start = 200
    tv_spend = np.concatenate([
        np.zeros(tv_campaign_start),
        np.full(n_days - tv_campaign_start, 15000) + np.random.normal(0, 2000, n_days - tv_campaign_start)
    ])

    # Bookings (affected by everything)
    bookings_base = trend + seasonality_weekly + seasonality_monthly + 0.05 * flights + 0.01 * digital_spend + noise

    # TV effect (true causal impact = +50 bookings/day)
    tv_effect = np.concatenate([
        np.zeros(tv_campaign_start),
        np.full(n_days - tv_campaign_start, 50) + np.random.normal(0, 5, n_days - tv_campaign_start)
    ])

    bookings = bookings_base + tv_effect
    bookings = np.maximum(bookings, 50)  # Floor at 50

    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'bookings': np.round(bookings, 0).astype(int),
        'tv_spend': np.round(tv_spend, 0).astype(int),
        'digital_spend': np.round(digital_spend, 0).astype(int),
        'flights_available': np.round(flights, 0).astype(int)
    })

    return df


# Example usage
if __name__ == '__main__':
    # Create sample data
    sample_df = create_sample_data()
    sample_df.to_csv('sample_data/nielsen_tv_sample.csv', index=False)
    print('Sample data created!')

    # Test Data Agent
    agent = DataAgent()

    # Ingest
    result = agent.ingest('sample_data/nielsen_tv_sample.csv')
    print('\nIngestion Result:')
    print(f"Success: {result['success']}")
    print(f"Shape: {result['shape']}")
    print(f"\nSuggestions:")
    print(f"Date column: {result['suggestions']['date_column']}")
    print(f"Target metric: {result['suggestions']['target_metric']}")
    print(f"Covariates: {result['suggestions']['covariates']}")

    # Prepare
    prepared = agent.prepare_for_analysis(
        date_col='date',
        target_col='bookings',
        covariate_cols=['tv_spend', 'digital_spend', 'flights_available']
    )

    print(f'\nPrepared data shape: {prepared.shape}')

    # Quality check
    quality = agent.check_data_quality()
    print(f'\nData Quality Score: {quality["score"]}/100')
    print(f'Recommendation: {quality["recommendation"]}')
    print(f'Issues: {quality["issues"]}')
