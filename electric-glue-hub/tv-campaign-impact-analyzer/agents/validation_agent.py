"""
Validation Agent - Data quality checks and confounder detection
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from scipy import stats
from statsmodels.stats.diagnostic import het_white, acorr_ljungbox
from statsmodels.tsa.stattools import adfuller, kpss
import warnings
warnings.filterwarnings('ignore')


class ValidationAgent:
    """
    Intelligent agent for data validation and quality assessment.

    Responsibilities:
    - Check for structural breaks (critical for Nielsen case!)
    - Detect potential confounders
    - Validate DID assumptions (and flag when violated)
    - Check for data quality issues
    - Provide actionable recommendations
    """

    def __init__(self):
        self.data = None
        self.target_col = None
        self.date_col = None
        self.validation_results = {}
        self.warnings = []
        self.recommendations = []

    def validate(
        self,
        data: pd.DataFrame,
        target_col: str,
        covariate_cols: Optional[List[str]] = None,
        intervention_date: Optional[str] = None
    ) -> Dict:
        """
        Run comprehensive validation checks.

        Parameters
        ----------
        data : pd.DataFrame
            Time series data with datetime index
        target_col : str
            Target metric column name
        covariate_cols : list of str, optional
            Covariate columns to validate
        intervention_date : str, optional
            Date when intervention occurred (for structural break tests)

        Returns
        -------
        dict with validation results, warnings, and recommendations
        """
        self.data = data
        self.target_col = target_col
        self.warnings = []
        self.recommendations = []

        # Reset validation results
        self.validation_results = {
            'overall_score': 0,
            'checks': {}
        }

        # Run validation checks
        self._check_completeness()
        self._check_stationarity()
        self._check_outliers()
        self._check_heteroscedasticity()
        self._check_autocorrelation()

        if intervention_date:
            self._check_structural_break(intervention_date)

        if covariate_cols:
            self._check_confounders(covariate_cols)
            self._check_multicollinearity(covariate_cols)

        # Calculate overall quality score
        self._calculate_overall_score()

        return {
            'success': True,
            'score': self.validation_results['overall_score'],
            'checks': self.validation_results['checks'],
            'warnings': self.warnings,
            'recommendations': self.recommendations
        }

    def _check_completeness(self):
        """Check for missing values and gaps."""
        target = self.data[self.target_col]

        # Missing values
        missing_pct = target.isnull().sum() / len(target) * 100

        # Date gaps
        date_diff = self.data.index.to_series().diff()
        expected_freq = date_diff.mode()[0] if len(date_diff) > 0 else None
        gaps = (date_diff > expected_freq * 1.5).sum() if expected_freq else 0

        passed = missing_pct < 5 and gaps == 0
        score = 100 if passed else max(0, 100 - missing_pct * 10 - gaps * 5)

        self.validation_results['checks']['completeness'] = {
            'passed': passed,
            'score': score,
            'missing_pct': missing_pct,
            'gaps': gaps
        }

        if missing_pct > 5:
            self.warnings.append(f"⚠️ {missing_pct:.1f}% missing values detected")
            self.recommendations.append("Consider imputation or removing incomplete periods")

        if gaps > 0:
            self.warnings.append(f"⚠️ {gaps} gaps in time series detected")
            self.recommendations.append("Check for data collection issues or holidays")

    def _check_stationarity(self):
        """
        Test for stationarity using ADF and KPSS tests.

        Non-stationary series can violate BSTS assumptions.
        """
        target = self.data[self.target_col].dropna()

        # Augmented Dickey-Fuller test (H0: non-stationary)
        adf_stat, adf_pvalue, _, _, adf_critical, _ = adfuller(target, autolag='AIC')
        adf_stationary = adf_pvalue < 0.05

        # KPSS test (H0: stationary)
        kpss_stat, kpss_pvalue, _, kpss_critical = kpss(target, regression='ct', nlags='auto')
        kpss_stationary = kpss_pvalue > 0.05

        # Both tests should agree for confidence
        passed = adf_stationary and kpss_stationary
        score = 100 if passed else 70 if (adf_stationary or kpss_stationary) else 40

        self.validation_results['checks']['stationarity'] = {
            'passed': passed,
            'score': score,
            'adf_pvalue': adf_pvalue,
            'kpss_pvalue': kpss_pvalue,
            'likely_stationary': adf_stationary or kpss_stationary
        }

        if not passed:
            if not adf_stationary and not kpss_stationary:
                self.warnings.append("⚠️ Time series appears non-stationary (strong trend/drift)")
                self.recommendations.append("Consider differencing or detrending before analysis")
            else:
                self.warnings.append("⚠️ Stationarity tests show mixed results")
                self.recommendations.append("Visual inspection recommended - check for regime changes")

    def _check_outliers(self):
        """Detect outliers using IQR and Z-score methods."""
        target = self.data[self.target_col].dropna()

        # IQR method
        q1, q3 = target.quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers_iqr = ((target < q1 - 3 * iqr) | (target > q3 + 3 * iqr)).sum()

        # Z-score method
        z_scores = np.abs(stats.zscore(target))
        outliers_z = (z_scores > 3).sum()

        outlier_pct = max(outliers_iqr, outliers_z) / len(target) * 100

        passed = outlier_pct < 5
        score = 100 if outlier_pct < 2 else max(0, 100 - outlier_pct * 10)

        self.validation_results['checks']['outliers'] = {
            'passed': passed,
            'score': score,
            'n_outliers_iqr': outliers_iqr,
            'n_outliers_z': outliers_z,
            'outlier_pct': outlier_pct
        }

        if outlier_pct > 5:
            self.warnings.append(f"⚠️ {outlier_pct:.1f}% outliers detected")
            self.recommendations.append("Review outliers - could indicate data quality issues or special events")

    def _check_heteroscedasticity(self):
        """
        Test for heteroscedasticity (non-constant variance).

        Heteroscedasticity can affect credible interval accuracy.
        """
        target = self.data[self.target_col].dropna()
        time_idx = np.arange(len(target)).reshape(-1, 1)

        try:
            # White's test for heteroscedasticity
            # Regress target on time, then test residuals
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(time_idx, target)
            residuals = target - model.predict(time_idx)

            # Split into first and second half
            mid = len(residuals) // 2
            var1 = residuals[:mid].var()
            var2 = residuals[mid:].var()

            # F-test for variance ratio
            f_stat = var2 / var1 if var1 > 0 else np.inf
            # Critical value at 0.05 significance
            passed = 0.5 < f_stat < 2.0  # Roughly constant variance

            score = 100 if passed else max(0, 100 - abs(np.log2(f_stat)) * 20)

            self.validation_results['checks']['heteroscedasticity'] = {
                'passed': passed,
                'score': score,
                'variance_ratio': f_stat,
                'likely_homoscedastic': passed
            }

            if not passed:
                self.warnings.append("⚠️ Variance changes over time (heteroscedasticity detected)")
                self.recommendations.append("Consider log transformation or weighted regression")

        except Exception as e:
            self.validation_results['checks']['heteroscedasticity'] = {
                'passed': None,
                'score': 50,
                'error': str(e)
            }

    def _check_autocorrelation(self):
        """
        Test for autocorrelation using Ljung-Box test.

        Strong autocorrelation is expected in time series but excessive
        autocorrelation in residuals indicates model misspecification.
        """
        target = self.data[self.target_col].dropna()

        # Ljung-Box test for autocorrelation
        lb_result = acorr_ljungbox(target, lags=[7, 14, 30], return_df=True)

        # Check if significant autocorrelation exists
        significant_lags = (lb_result['lb_pvalue'] < 0.05).sum()

        # Some autocorrelation is expected, but not at all lags
        passed = significant_lags >= 1 and significant_lags <= 2
        score = 100 if passed else max(0, 100 - abs(significant_lags - 1.5) * 20)

        self.validation_results['checks']['autocorrelation'] = {
            'passed': passed,
            'score': score,
            'significant_lags': int(significant_lags),
            'lb_pvalues': lb_result['lb_pvalue'].to_dict()
        }

        if significant_lags == 0:
            self.warnings.append("⚠️ No autocorrelation detected - unusual for time series")
            self.recommendations.append("Verify data is truly time series and not cross-sectional")
        elif significant_lags > 2:
            self.recommendations.append("Strong autocorrelation detected - BSTS will model this")

    def _check_structural_break(self, intervention_date: str):
        """
        Test for structural breaks using CUSUM test.

        CRITICAL for Nielsen case: Flight availability caused structural break!
        """
        target = self.data[self.target_col].dropna()

        # Convert intervention date
        intervention_idx = self.data.index.get_loc(pd.to_datetime(intervention_date))

        # Split data
        pre = target.iloc[:intervention_idx]
        post = target.iloc[intervention_idx:]

        if len(pre) < 10 or len(post) < 10:
            self.validation_results['checks']['structural_break'] = {
                'passed': None,
                'score': 50,
                'error': 'Insufficient data before or after intervention'
            }
            return

        # CUSUM test
        pre_mean = pre.mean()
        pre_std = pre.std()

        # Standardized cumulative sum
        cusum = np.cumsum((target - pre_mean) / pre_std)
        cusum_pre = cusum[:intervention_idx]
        cusum_post = cusum[intervention_idx:]

        # Check for break at intervention point
        break_magnitude = abs(cusum_post.iloc[0] - cusum_pre.iloc[-1]) if len(cusum_post) > 0 else 0

        # Also check for breaks BEFORE intervention (the Nielsen problem!)
        pre_cusum_range = cusum_pre.max() - cusum_pre.min()
        early_break_detected = pre_cusum_range > 3 * np.sqrt(len(pre))

        passed = not early_break_detected
        score = 100 if passed else 30

        self.validation_results['checks']['structural_break'] = {
            'passed': passed,
            'score': score,
            'break_magnitude': float(break_magnitude),
            'early_break_detected': early_break_detected,
            'pre_cusum_range': float(pre_cusum_range)
        }

        if early_break_detected:
            self.warnings.append("🚨 CRITICAL: Structural break detected BEFORE intervention!")
            self.warnings.append("This violates the stable pre-period assumption")
            self.recommendations.append("⚠️ DO NOT use Difference-in-Differences (DID)")
            self.recommendations.append("✅ Use BSTS with covariates to control for the break")
            self.recommendations.append("🔍 Investigate what changed (e.g., flight availability, economic shock)")

    def _check_confounders(self, covariate_cols: List[str]):
        """
        Check for potential confounders by analyzing covariate behavior.

        Look for covariates that:
        1. Change around intervention time (like Nielsen flight availability!)
        2. Correlate with target metric
        """
        target = self.data[self.target_col]

        confounder_analysis = {}

        for col in covariate_cols:
            if col not in self.data.columns:
                continue

            covariate = self.data[col].dropna()

            # Correlation with target
            correlation = target.corr(covariate)

            # Check for changes in covariate over time
            rolling_mean = covariate.rolling(window=30, min_periods=10).mean()
            mean_change = abs(rolling_mean.iloc[-1] - rolling_mean.iloc[0]) / rolling_mean.iloc[0] if rolling_mean.iloc[0] != 0 else 0

            # Flag as potential confounder if:
            # - Moderate to strong correlation (|r| > 0.3)
            # - Changed significantly over time (>20%)
            is_confounder = abs(correlation) > 0.3 and mean_change > 0.2

            confounder_analysis[col] = {
                'correlation': float(correlation),
                'mean_change_pct': float(mean_change * 100),
                'is_potential_confounder': is_confounder
            }

            if is_confounder:
                self.warnings.append(f"🔍 Potential confounder detected: {col}")
                self.warnings.append(f"   Correlation: {correlation:.2f}, Changed by {mean_change*100:.1f}%")
                self.recommendations.append(f"✅ Include '{col}' as covariate in BSTS model")

        n_confounders = sum(1 for v in confounder_analysis.values() if v['is_potential_confounder'])

        # Score based on whether confounders are identified
        passed = n_confounders > 0  # Good to identify confounders!
        score = 100 if n_confounders <= 3 else max(60, 100 - (n_confounders - 3) * 10)

        self.validation_results['checks']['confounders'] = {
            'passed': passed,
            'score': score,
            'n_potential_confounders': n_confounders,
            'analysis': confounder_analysis
        }

        if n_confounders == 0:
            self.recommendations.append("No obvious confounders detected - but include key business drivers as covariates")

    def _check_multicollinearity(self, covariate_cols: List[str]):
        """
        Check for multicollinearity among covariates using VIF.

        High multicollinearity makes coefficient interpretation difficult.
        """
        from statsmodels.stats.outliers_influence import variance_inflation_factor

        # Select only numeric covariates that exist
        available_cols = [col for col in covariate_cols if col in self.data.columns]
        if len(available_cols) < 2:
            return

        X = self.data[available_cols].dropna()

        if len(X) < 10:
            return

        try:
            # Calculate VIF for each covariate
            vif_data = {}
            for i, col in enumerate(X.columns):
                vif = variance_inflation_factor(X.values, i)
                vif_data[col] = float(vif)

            max_vif = max(vif_data.values())

            # VIF > 10 indicates high multicollinearity
            passed = max_vif < 10
            score = 100 if max_vif < 5 else max(0, 100 - (max_vif - 5) * 10)

            self.validation_results['checks']['multicollinearity'] = {
                'passed': passed,
                'score': score,
                'vif_scores': vif_data,
                'max_vif': max_vif
            }

            if max_vif > 10:
                high_vif_vars = [k for k, v in vif_data.items() if v > 10]
                self.warnings.append(f"⚠️ High multicollinearity detected: {', '.join(high_vif_vars)}")
                self.recommendations.append("Consider removing highly correlated covariates")

        except Exception as e:
            self.validation_results['checks']['multicollinearity'] = {
                'passed': None,
                'score': 50,
                'error': str(e)
            }

    def _calculate_overall_score(self):
        """Calculate weighted overall quality score."""
        checks = self.validation_results['checks']

        # Weights for each check
        weights = {
            'completeness': 0.25,
            'stationarity': 0.15,
            'outliers': 0.15,
            'heteroscedasticity': 0.10,
            'autocorrelation': 0.10,
            'structural_break': 0.20,  # High weight - critical!
            'confounders': 0.15,
            'multicollinearity': 0.10
        }

        total_score = 0
        total_weight = 0

        for check, weight in weights.items():
            if check in checks and checks[check].get('score') is not None:
                total_score += checks[check]['score'] * weight
                total_weight += weight

        # Normalize to 0-100
        self.validation_results['overall_score'] = round(total_score / total_weight if total_weight > 0 else 0, 1)

    def check_did_assumptions(
        self,
        treatment_data: pd.Series,
        control_data: pd.Series,
        intervention_date: str
    ) -> Dict:
        """
        Check Difference-in-Differences assumptions.

        CRITICAL: Show why DID fails for Nielsen!

        Parameters
        ----------
        treatment_data : pd.Series
            Time series from treatment group
        control_data : pd.Series
            Time series from control group
        intervention_date : str
            Date of intervention

        Returns
        -------
        dict with DID assumption tests and violations
        """
        intervention_idx = treatment_data.index.get_loc(pd.to_datetime(intervention_date))

        # Pre-period data
        treat_pre = treatment_data.iloc[:intervention_idx]
        control_pre = control_data.iloc[:intervention_idx]

        # Test 1: Parallel trends
        # Regress both series on time, compare slopes
        time_idx = np.arange(len(treat_pre))
        treat_slope = np.polyfit(time_idx, treat_pre, 1)[0]
        control_slope = np.polyfit(time_idx, control_pre, 1)[0]

        slope_diff_pct = abs(treat_slope - control_slope) / abs(treat_slope) * 100 if treat_slope != 0 else np.inf
        parallel_trends_passed = slope_diff_pct < 20  # Slopes within 20%

        # Test 2: Common shocks
        # Check correlation of first differences
        treat_diff = treat_pre.diff().dropna()
        control_diff = control_pre.diff().dropna()
        shock_correlation = treat_diff.corr(control_diff)
        common_shocks_passed = shock_correlation > 0.5

        # Test 3: No compositional changes
        # Check for structural breaks in control group (Nielsen problem!)
        control_cusum = np.cumsum((control_pre - control_pre.mean()) / control_pre.std())
        control_break_detected = (control_cusum.max() - control_cusum.min()) > 3 * np.sqrt(len(control_pre))
        no_composition_changes = not control_break_detected

        # Overall DID validity
        did_valid = parallel_trends_passed and common_shocks_passed and no_composition_changes

        return {
            'did_valid': did_valid,
            'assumptions': {
                'parallel_trends': {
                    'passed': parallel_trends_passed,
                    'treat_slope': float(treat_slope),
                    'control_slope': float(control_slope),
                    'slope_diff_pct': float(slope_diff_pct)
                },
                'common_shocks': {
                    'passed': common_shocks_passed,
                    'correlation': float(shock_correlation)
                },
                'no_composition_changes': {
                    'passed': no_composition_changes,
                    'control_break_detected': control_break_detected
                }
            },
            'warning': (
                "🚨 DID ASSUMPTIONS VIOLATED! 🚨\n\n"
                "The control group is not a valid counterfactual because:\n"
                f"{'❌ Parallel trends violated (slopes differ by ' + f'{slope_diff_pct:.1f}%)' if not parallel_trends_passed else '✅ Parallel trends OK'}\n"
                f"{'❌ Shocks not common (correlation: ' + f'{shock_correlation:.2f})' if not common_shocks_passed else '✅ Common shocks OK'}\n"
                f"{'❌ Control group has structural break (e.g., flight availability change)' if control_break_detected else '✅ No compositional changes'}\n\n"
                "📊 RECOMMENDED APPROACH: Bayesian Structural Time Series (BSTS)\n"
                "✅ No geographic controls needed\n"
                "✅ Models confounders explicitly as covariates\n"
                "✅ Robust to violations of parallel trends\n"
            ) if not did_valid else None
        }


# Example usage
if __name__ == '__main__':
    # Create sample data with structural break
    from agents.data_agent import create_sample_data

    df = create_sample_data()

    # Initialize validation agent
    agent = ValidationAgent()

    # Run validation
    result = agent.validate(
        data=df.set_index('date'),
        target_col='bookings',
        covariate_cols=['tv_spend', 'digital_spend', 'flights_available'],
        intervention_date='2024-07-20'  # TV campaign start
    )

    print('=' * 60)
    print('VALIDATION RESULTS')
    print('=' * 60)
    print(f"\nOverall Quality Score: {result['score']}/100")

    print('\n' + '=' * 60)
    print('CHECK RESULTS')
    print('=' * 60)
    for check_name, check_result in result['checks'].items():
        status = '✅' if check_result.get('passed') else '⚠️'
        score = check_result.get('score', 'N/A')
        print(f"{status} {check_name.upper()}: {score}/100")

    if result['warnings']:
        print('\n' + '=' * 60)
        print('WARNINGS')
        print('=' * 60)
        for warning in result['warnings']:
            print(warning)

    if result['recommendations']:
        print('\n' + '=' * 60)
        print('RECOMMENDATIONS')
        print('=' * 60)
        for rec in result['recommendations']:
            print(f"• {rec}")
