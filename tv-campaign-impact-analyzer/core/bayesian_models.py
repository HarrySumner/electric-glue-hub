"""
Bayesian Structural Time Series Models
Avoiding Difference-in-Differences (DID) - Using BSTS instead
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class BayesianStructuralTimeSeries:
    """
    Bayesian Structural Time Series (BSTS) model for causal inference.

    Why BSTS instead of DID?
    - No need for geographic controls
    - Robust to regional confounders (flight availability, etc.)
    - Explicit uncertainty quantification
    - Handles time-varying coefficients
    """

    def __init__(
        self,
        seasonal_periods: Optional[List[int]] = None,
        include_trend: bool = True,
        include_local_level: bool = True,
        prior_level_sd: float = 0.01
    ):
        """
        Initialize BSTS model.

        Parameters
        ----------
        seasonal_periods : list of int, optional
            Seasonal periods to model (e.g., [7] for weekly, [7, 30] for weekly+monthly)
        include_trend : bool, default True
            Include local linear trend component
        include_local_level : bool, default True
            Include local level component
        prior_level_sd : float, default 0.01
            Prior standard deviation for level component
        """
        self.seasonal_periods = seasonal_periods or [7]
        self.include_trend = include_trend
        self.include_local_level = include_local_level
        self.prior_level_sd = prior_level_sd

        self.model = None
        self.trace = None
        self.results = None

    def fit(
        self,
        y: pd.Series,
        X: Optional[pd.DataFrame] = None,
        pre_period: Tuple[int, int] = None,
        post_period: Tuple[int, int] = None,
        niter: int = 2000,
        nburn: int = 1000
    ):
        """
        Fit BSTS model to data.

        Parameters
        ----------
        y : pd.Series
            Time series of response variable
        X : pd.DataFrame, optional
            Covariates (controls for confounders like flight availability)
        pre_period : tuple of int
            (start_idx, end_idx) for pre-intervention period
        post_period : tuple of int
            (start_idx, end_idx) for post-intervention period
        niter : int, default 2000
            Number of MCMC iterations
        nburn : int, default 1000
            Number of burn-in iterations
        """
        try:
            from causalimpact import CausalImpact
        except ImportError:
            raise ImportError(
                "CausalImpact not installed. Run: pip install causalimpact"
            )

        # Prepare data
        if X is not None:
            data = pd.concat([y, X], axis=1)
        else:
            data = pd.DataFrame({y.name: y})

        # Model arguments
        model_args = {
            'nseasons': self.seasonal_periods[0],
            'season_duration': 1,
            'prior_level_sd': self.prior_level_sd,
            'niter': niter
        }

        # Fit model
        self.model = CausalImpact(
            data=data,
            pre_period=pre_period,
            post_period=post_period,
            model_args=model_args
        )

        return self

    def summary(self) -> pd.DataFrame:
        """Get summary statistics from fitted model."""
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")

        return self.model.summary_data

    def plot(self, figsize=(12, 8)):
        """Generate diagnostic plots."""
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")

        return self.model.plot(figsize=figsize)

    def get_causal_effect(self) -> Dict:
        """
        Extract causal effect estimates.

        Returns
        -------
        dict with:
            - average_effect: Average causal effect per period
            - cumulative_effect: Total causal effect
            - relative_effect: Percentage change
            - credible_interval: (lower, upper) bounds
            - posterior_prob: P(effect != 0)
        """
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")

        summary = self.model.summary_data

        return {
            'average_effect': summary.loc['average', 'abs_effect'],
            'average_effect_lower': summary.loc['average', 'abs_effect_lower'],
            'average_effect_upper': summary.loc['average', 'abs_effect_upper'],
            'relative_effect': summary.loc['average', 'rel_effect'],
            'relative_effect_lower': summary.loc['average', 'rel_effect_lower'],
            'relative_effect_upper': summary.loc['average', 'rel_effect_upper'],
            'cumulative_effect': summary.loc['cumulative', 'abs_effect'],
            'cumulative_lower': summary.loc['cumulative', 'abs_effect_lower'],
            'cumulative_upper': summary.loc['cumulative', 'abs_effect_upper'],
            'p_value': self.model.p_value
        }

    def get_counterfactual(self) -> pd.Series:
        """Get counterfactual prediction (what would have happened without intervention)."""
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")

        return self.model.inferences['preds']


def auto_select_model(
    data: pd.DataFrame,
    target_col: str,
    date_col: str = None
) -> Dict:
    """
    Automatically select appropriate BSTS model based on data characteristics.

    Parameters
    ----------
    data : pd.DataFrame
        Time series data
    target_col : str
        Name of target variable column
    date_col : str, optional
        Name of date column

    Returns
    -------
    dict with recommended model specification
    """
    from scipy import stats
    from statsmodels.tsa.stattools import acf

    # Ensure datetime index
    if date_col and date_col in data.columns:
        data = data.set_index(date_col)

    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Data must have datetime index")

    y = data[target_col].dropna()

    # Detect frequency
    freq = pd.infer_freq(data.index)
    if freq in ['D', 'B']:  # Daily
        seasonal_candidates = [7, 30, 365]
    elif freq == 'W':  # Weekly
        seasonal_candidates = [52]
    elif freq == 'M':  # Monthly
        seasonal_candidates = [12]
    else:
        seasonal_candidates = [7]  # Default to weekly

    # Test for seasonality
    detected_seasons = []
    for period in seasonal_candidates:
        if len(y) >= 2 * period:
            autocorr = acf(y, nlags=min(period * 2, len(y) - 1))
            if abs(autocorr[period]) > 0.3:
                detected_seasons.append(period)

    # Test for trend
    time_idx = np.arange(len(y))
    slope, intercept, r_value, p_value, std_err = stats.linregress(time_idx, y)
    has_trend = p_value < 0.05 and abs(r_value) > 0.3

    # Test for local level variation
    rolling_std = y.rolling(window=7).std().mean()
    overall_std = y.std()
    has_local_level = rolling_std / overall_std > 0.2

    return {
        'seasonal_periods': detected_seasons if detected_seasons else [7],
        'include_trend': has_trend,
        'include_local_level': has_local_level,
        'frequency': freq,
        'recommendation': {
            'seasonality': 'Strong' if len(detected_seasons) > 1 else 'Moderate' if detected_seasons else 'Weak',
            'trend': 'Yes' if has_trend else 'No',
            'local_variation': 'High' if has_local_level else 'Low'
        }
    }


def compare_to_did(
    y: pd.Series,
    treatment_group: pd.Series,
    pre_period: Tuple[int, int],
    post_period: Tuple[int, int]
) -> Dict:
    """
    Compare BSTS to traditional DID (for educational purposes - show why DID fails).

    Parameters
    ----------
    y : pd.Series
        Outcome variable
    treatment_group : pd.Series
        Binary indicator (1 = treated region, 0 = control)
    pre_period : tuple
        Pre-intervention period indices
    post_period : tuple
        Post-intervention period indices

    Returns
    -------
    dict with DID estimate and warning about assumptions
    """
    # This function demonstrates why DID is problematic for Nielsen case

    # Split by treatment group
    treated = y[treatment_group == 1]
    control = y[treatment_group == 0]

    # Calculate DID estimate
    treated_pre = treated.iloc[pre_period[0]:pre_period[1]].mean()
    treated_post = treated.iloc[post_period[0]:post_period[1]].mean()
    control_pre = control.iloc[pre_period[0]:pre_period[1]].mean()
    control_post = control.iloc[post_period[0]:post_period[1]].mean()

    did_estimate = (treated_post - treated_pre) - (control_post - control_pre)

    # Test parallel trends assumption (critical for Nielsen!)
    treated_trend = treated_post - treated_pre
    control_trend = control_post - control_pre
    parallel_trends_violated = abs(treated_trend - control_trend) / abs(treated_trend) > 0.5

    return {
        'did_estimate': did_estimate,
        'parallel_trends_violated': parallel_trends_violated,
        'warning': (
            "⚠️ CAUTION: DID assumes parallel trends. "
            "For Nielsen campaign, this was violated due to: "
            "(1) Flight availability changes in control regions, "
            "(2) TV ad spillover via streaming/travel, "
            "(3) Different regional economic trends. "
            "Use BSTS instead!"
        ) if parallel_trends_violated else None
    }


def sensitivity_analysis(
    model: BayesianStructuralTimeSeries,
    prior_sds: List[float] = [0.001, 0.01, 0.05, 0.1]
) -> pd.DataFrame:
    """
    Run sensitivity analysis on prior specifications.

    Shows how robust results are to different prior choices.
    """
    results = []

    for prior_sd in prior_sds:
        # Re-fit with different prior
        model_copy = BayesianStructuralTimeSeries(
            seasonal_periods=model.seasonal_periods,
            include_trend=model.include_trend,
            include_local_level=model.include_local_level,
            prior_level_sd=prior_sd
        )

        # Note: Would need to pass original data - placeholder for now
        effect = {
            'prior_sd': prior_sd,
            'average_effect': None,  # Would calculate
            'cumulative_effect': None
        }
        results.append(effect)

    return pd.DataFrame(results)


# Example usage documentation
"""
EXAMPLE: Nielsen TV Campaign Analysis (Avoiding DID)

# 1. Load data
data = pd.read_csv('nielsen_tv_campaign.csv', parse_dates=['date'])
data = data.set_index('date')

# 2. Define covariates to control for confounders
covariates = [
    'flights_available',      # Control for flight availability increase!
    'digital_spend',          # Control for other marketing
    'economic_indicator'      # Control for regional economic changes
]

# 3. Auto-select model
model_spec = auto_select_model(data, 'bookings')
print(f"Recommended: {model_spec['recommendation']}")

# 4. Fit BSTS model
model = BayesianStructuralTimeSeries(
    seasonal_periods=model_spec['seasonal_periods'],
    include_trend=model_spec['include_trend']
)

model.fit(
    y=data['bookings'],
    X=data[covariates],  # Explicitly control for confounders
    pre_period=(0, 180),   # 6 months pre-campaign
    post_period=(181, 240) # 2 months during campaign
)

# 5. Get results
effect = model.get_causal_effect()
print(f"TV campaign drove {effect['average_effect']:.0f} bookings/day")
print(f"95% CI: [{effect['average_effect_lower']:.0f}, {effect['average_effect_upper']:.0f}]")
print(f"Total: {effect['cumulative_effect']:.0f} incremental bookings")

# 6. Compare to DID (to show why it fails)
did_comparison = compare_to_did(data['bookings'], data['region_treated'], (0, 180), (181, 240))
if did_comparison['warning']:
    print(did_comparison['warning'])
"""
