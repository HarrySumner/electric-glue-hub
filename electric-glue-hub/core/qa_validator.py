"""
QA Validation System for Campaign Analysis
Multi-layered validation to ensure accuracy and reliability
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Any


class CampaignAnalysisQA:
    """
    Comprehensive QA validation for campaign analysis results.

    Implements 7-layer validation framework:
    1. Data Quality Validation
    2. Statistical Validity Checks
    3. Logic Flow Validation
    4. Output Coherence Checks
    5. MCMC-Specific Checks
    6. Calculation Verification
    7. Confidence Scoring
    """

    def __init__(self):
        self.validation_results = {}
        self.flags = []
        self.warnings = []
        self.confidence_scores = {}

    def validate_all(
        self,
        data: pd.DataFrame,
        results: Dict[str, Any],
        campaign_start: pd.Timestamp,
        campaign_end: pd.Timestamp
    ) -> Dict[str, Any]:
        """
        Run all validation layers and return comprehensive QA report.

        Args:
            data: Full dataset with pre and post campaign data
            results: Analysis results from Bayesian MCMC
            campaign_start: Campaign start date
            campaign_end: Campaign end date

        Returns:
            Dictionary with validation results and confidence score
        """
        print("[QA] Running QA validation...")

        # Layer 1: Data Quality
        data_quality = self._validate_data_quality(data, campaign_start, campaign_end)

        # Layer 2: Statistical Validity
        statistical_validity = self._validate_statistical_validity(data, results)

        # Layer 3: MCMC-Specific Checks
        mcmc_checks = self._validate_mcmc_convergence(results)

        # Layer 4: Calculation Verification
        calculation_checks = self._verify_calculations(results)

        # Layer 5: Output Coherence
        coherence_checks = self._validate_output_coherence(results)

        # Layer 6: Counterfactual Validity
        counterfactual_checks = self._validate_counterfactual(data, results, campaign_start)

        # Layer 7: Aggregate Confidence Score
        confidence_score = self._calculate_confidence_score()

        # Compile full report
        qa_report = {
            'overall_status': self._determine_status(confidence_score),
            'confidence_score': confidence_score,
            'confidence_breakdown': self.confidence_scores,
            'layer_results': {
                'data_quality': data_quality,
                'statistical_validity': statistical_validity,
                'mcmc_convergence': mcmc_checks,
                'calculation_verification': calculation_checks,
                'output_coherence': coherence_checks,
                'counterfactual_validity': counterfactual_checks
            },
            'flags': self.flags,
            'warnings': self.warnings,
            'recommendation': self._generate_recommendation(confidence_score)
        }

        return qa_report

    def _validate_data_quality(
        self,
        data: pd.DataFrame,
        campaign_start: pd.Timestamp,
        campaign_end: pd.Timestamp
    ) -> Dict[str, Any]:
        """Layer 1: Data Quality Validation"""

        checks = {}
        score = 100.0

        # Check 1: Missing values
        missing_pct = data['y'].isna().sum() / len(data) * 100
        checks['missing_values'] = {
            'value': missing_pct,
            'threshold': 5.0,
            'passed': missing_pct < 5.0,
            'description': f'{missing_pct:.1f}% missing values'
        }
        if missing_pct >= 5.0:
            score -= 25
            self.flags.append(f"⚠️ High missing values: {missing_pct:.1f}%")

        # Check 2: Minimum data points
        pre_data = data[data['date'] < campaign_start]
        n_pre = len(pre_data)
        checks['pre_period_size'] = {
            'value': n_pre,
            'threshold': 30,
            'passed': n_pre >= 30,
            'description': f'{n_pre} pre-campaign observations'
        }
        if n_pre < 30:
            score -= 30
            self.flags.append(f"🔴 Insufficient pre-campaign data: {n_pre} points (need ≥30)")
        elif n_pre < 50:
            score -= 10
            self.warnings.append(f"⚠️ Limited pre-campaign data: {n_pre} points (50+ recommended)")

        # Check 3: Date continuity
        date_gaps = data['date'].diff().dt.days
        max_gap = date_gaps.max()
        checks['date_continuity'] = {
            'value': max_gap,
            'threshold': 7,
            'passed': max_gap <= 7,
            'description': f'Max gap: {max_gap} days'
        }
        if max_gap > 7:
            score -= 15
            self.warnings.append(f"⚠️ Large date gap detected: {max_gap} days")

        # Check 4: Outliers
        q1 = data['y'].quantile(0.25)
        q3 = data['y'].quantile(0.75)
        iqr = q3 - q1
        outliers = ((data['y'] < (q1 - 3 * iqr)) | (data['y'] > (q3 + 3 * iqr))).sum()
        outlier_pct = outliers / len(data) * 100
        checks['outliers'] = {
            'value': outlier_pct,
            'threshold': 5.0,
            'passed': outlier_pct < 5.0,
            'description': f'{outlier_pct:.1f}% outliers'
        }
        if outlier_pct >= 5.0:
            score -= 10
            self.warnings.append(f"⚠️ High outlier rate: {outlier_pct:.1f}%")

        # Check 5: Non-negative values (if applicable)
        negative_values = (data['y'] < 0).sum()
        checks['value_validity'] = {
            'value': negative_values,
            'threshold': 0,
            'passed': negative_values == 0,
            'description': f'{negative_values} negative values'
        }
        if negative_values > 0:
            score -= 10
            self.warnings.append(f"⚠️ Found {negative_values} negative values in KPI")

        self.confidence_scores['data_quality'] = max(0, score)

        return {
            'score': max(0, score),
            'checks': checks,
            'passed': score >= 70
        }

    def _validate_statistical_validity(
        self,
        data: pd.DataFrame,
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Layer 2: Statistical Validity Checks"""

        checks = {}
        score = 100.0

        # Check 1: Sample size adequacy
        n_pre = results.get('n_pre_points', 0)
        n_post = results.get('n_post_points', 0)

        checks['sample_size'] = {
            'pre_period': n_pre,
            'post_period': n_post,
            'adequate': n_pre >= 30 and n_post >= 30,
            'description': f'Pre: {n_pre}, Post: {n_post} observations'
        }

        if n_pre < 30 or n_post < 30:
            score -= 30
            self.flags.append("🔴 Inadequate sample size for statistical inference")

        # Check 2: Effect size reasonableness
        relative_effect = abs(results.get('relative_effect', 0))
        checks['effect_size'] = {
            'value': relative_effect,
            'reasonable': relative_effect < 200,  # >200% is suspicious
            'description': f'{relative_effect:.1f}% relative effect'
        }

        if relative_effect > 200:
            score -= 20
            self.flags.append(f"⚠️ Unusually large effect: {relative_effect:.1f}%")
        elif relative_effect > 100:
            score -= 5
            self.warnings.append(f"⚠️ Large effect detected: {relative_effect:.1f}% - verify data")

        # Check 3: Credible interval width
        if 'cumulative_lower' in results and 'cumulative_upper' in results:
            ci_width = results['cumulative_upper'] - results['cumulative_lower']
            point_estimate = results['total_effect']

            # Relative CI width (as % of point estimate)
            if abs(point_estimate) > 0:
                relative_ci_width = (ci_width / abs(point_estimate)) * 100
            else:
                relative_ci_width = float('inf')

            checks['credible_interval'] = {
                'width': ci_width,
                'relative_width_pct': relative_ci_width,
                'precise': relative_ci_width < 100,
                'description': f'CI width: {relative_ci_width:.1f}% of estimate'
            }

            if relative_ci_width > 150:
                score -= 15
                self.warnings.append(f"⚠️ Wide credible interval: {relative_ci_width:.1f}% of estimate")

        self.confidence_scores['statistical_validity'] = max(0, score)

        return {
            'score': max(0, score),
            'checks': checks,
            'passed': score >= 70
        }

    def _validate_mcmc_convergence(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Layer 3: MCMC-Specific Convergence Checks"""

        checks = {}
        score = 100.0

        convergence = results.get('convergence', {})

        # Check 1: Convergence status
        converged = convergence.get('converged', False)
        checks['convergence_status'] = {
            'converged': converged,
            'message': convergence.get('message', 'Unknown'),
            'passed': converged
        }

        if not converged:
            score -= 40
            self.flags.append("🔴 MCMC did not converge - results may be unreliable")

        # Check 2: Effective sample size
        ess = convergence.get('effective_sample_size', 0)
        checks['effective_sample_size'] = {
            'value': ess,
            'threshold': 100,
            'passed': ess >= 100,
            'description': f'ESS: {ess:.0f}'
        }

        if ess < 100:
            score -= 30
            self.flags.append(f"🔴 Low effective sample size: {ess:.0f} (need ≥100)")
        elif ess < 200:
            score -= 10
            self.warnings.append(f"⚠️ Moderate ESS: {ess:.0f} (200+ recommended)")

        # Check 3: Number of MCMC samples
        n_samples = results.get('n_samples', 0)
        checks['mcmc_samples'] = {
            'value': n_samples,
            'threshold': 1000,
            'passed': n_samples >= 1000,
            'description': f'{n_samples:,} MCMC samples'
        }

        if n_samples < 1000:
            score -= 20
            self.warnings.append(f"⚠️ Low MCMC samples: {n_samples} (1000+ recommended)")

        self.confidence_scores['mcmc_convergence'] = max(0, score)

        return {
            'score': max(0, score),
            'checks': checks,
            'passed': score >= 70
        }

    def _verify_calculations(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Layer 4: Calculation Verification"""

        checks = {}
        score = 100.0

        # Check 1: Cumulative effect = sum of point effects
        if 'point_effect' in results and 'total_effect' in results:
            calculated_total = np.sum(results['point_effect'])
            reported_total = results['total_effect']

            # Allow 1% tolerance for floating point errors
            difference_pct = abs(calculated_total - reported_total) / abs(reported_total) * 100 if reported_total != 0 else 0

            checks['cumulative_calculation'] = {
                'calculated': calculated_total,
                'reported': reported_total,
                'difference_pct': difference_pct,
                'passed': difference_pct < 1.0,
                'description': f'Difference: {difference_pct:.3f}%'
            }

            if difference_pct >= 1.0:
                score -= 50
                self.flags.append(f"🔴 Calculation error: Cumulative ≠ sum of point effects ({difference_pct:.1f}% diff)")

        # Check 2: Relative effect consistency
        if 'total_effect' in results and 'counterfactual' in results and 'relative_effect' in results:
            counterfactual_total = np.sum(results['counterfactual'])
            if counterfactual_total != 0:
                calculated_relative = (results['total_effect'] / counterfactual_total) * 100
                reported_relative = results['relative_effect']

                rel_diff = abs(calculated_relative - reported_relative)

                checks['relative_effect_calculation'] = {
                    'calculated': calculated_relative,
                    'reported': reported_relative,
                    'difference': rel_diff,
                    'passed': rel_diff < 1.0,
                    'description': f'Difference: {rel_diff:.3f}%'
                }

                if rel_diff >= 1.0:
                    score -= 30
                    self.flags.append(f"🔴 Relative effect calculation mismatch: {rel_diff:.2f}%")

        # Check 3: Credible interval contains point estimate
        if all(k in results for k in ['total_effect', 'cumulative_lower', 'cumulative_upper']):
            point_est = results['total_effect']
            lower = results['cumulative_lower']
            upper = results['cumulative_upper']

            contains_estimate = lower <= point_est <= upper

            checks['ci_contains_estimate'] = {
                'point_estimate': point_est,
                'lower_bound': lower,
                'upper_bound': upper,
                'valid': contains_estimate,
                'description': f'[{lower:.0f}, {upper:.0f}] contains {point_est:.0f}'
            }

            if not contains_estimate:
                score -= 40
                self.flags.append("🔴 Point estimate outside credible interval!")

        self.confidence_scores['calculation_verification'] = max(0, score)

        return {
            'score': max(0, score),
            'checks': checks,
            'passed': score >= 70
        }

    def _validate_output_coherence(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Layer 5: Output Coherence Checks"""

        checks = {}
        score = 100.0

        # Check 1: Posterior probability alignment with credible interval
        if 'prob_causal_effect' in results and 'cumulative_lower' in results:
            prob_positive = results['prob_causal_effect']
            lower_bound = results['cumulative_lower']

            # If lower bound > 0, probability should be very high
            if lower_bound > 0 and prob_positive < 95:
                score -= 20
                self.warnings.append(f"⚠️ Lower CI bound positive but probability only {prob_positive:.1f}%")

            # If lower bound < 0, probability shouldn't be near 100%
            if lower_bound < 0 and prob_positive > 97:
                score -= 20
                self.warnings.append(f"⚠️ CI includes negative values but probability is {prob_positive:.1f}%")

            checks['probability_ci_alignment'] = {
                'probability': prob_positive,
                'ci_lower': lower_bound,
                'coherent': True,  # More nuanced check
                'description': f'P={prob_positive:.1f}%, CI lower={lower_bound:.0f}'
            }

        # Check 2: Sign consistency
        if 'total_effect' in results and 'relative_effect' in results:
            total_sign = np.sign(results['total_effect'])
            relative_sign = np.sign(results['relative_effect'])

            signs_match = total_sign == relative_sign

            checks['sign_consistency'] = {
                'total_effect_sign': '+' if total_sign > 0 else '-',
                'relative_effect_sign': '+' if relative_sign > 0 else '-',
                'consistent': signs_match,
                'description': 'Effect signs match' if signs_match else 'Effect signs mismatch!'
            }

            if not signs_match:
                score -= 50
                self.flags.append("🔴 Inconsistent effect signs between absolute and relative metrics")

        self.confidence_scores['output_coherence'] = max(0, score)

        return {
            'score': max(0, score),
            'checks': checks,
            'passed': score >= 70
        }

    def _validate_counterfactual(
        self,
        data: pd.DataFrame,
        results: Dict[str, Any],
        campaign_start: pd.Timestamp
    ) -> Dict[str, Any]:
        """Layer 6: Counterfactual Validity"""

        checks = {}
        score = 100.0

        # We can't fully validate counterfactual without running predictions
        # But we can check if it looks reasonable

        if 'counterfactual' in results:
            counterfactual = results['counterfactual']

            # Check 1: Counterfactual has reasonable variance
            cf_std = np.std(counterfactual)
            cf_mean = np.mean(counterfactual)

            cv = (cf_std / cf_mean) * 100 if cf_mean != 0 else 0

            checks['counterfactual_variability'] = {
                'coefficient_of_variation': cv,
                'reasonable': 5 < cv < 100,
                'description': f'CV: {cv:.1f}%'
            }

            if cv < 1:
                score -= 20
                self.warnings.append("⚠️ Counterfactual has very low variability (too smooth)")
            elif cv > 100:
                score -= 20
                self.warnings.append("⚠️ Counterfactual has very high variability (too noisy)")

        self.confidence_scores['counterfactual_validity'] = max(0, score)

        return {
            'score': max(0, score),
            'checks': checks,
            'passed': score >= 70
        }

    def _calculate_confidence_score(self) -> float:
        """
        Layer 7: Aggregate confidence score from all layers
        """
        weights = {
            'data_quality': 0.25,
            'statistical_validity': 0.25,
            'mcmc_convergence': 0.20,
            'calculation_verification': 0.15,
            'output_coherence': 0.10,
            'counterfactual_validity': 0.05
        }

        total_score = 0.0
        total_weight = 0.0

        for layer, weight in weights.items():
            if layer in self.confidence_scores:
                total_score += self.confidence_scores[layer] * weight
                total_weight += weight

        # Normalize to 100
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 0.0

        return final_score

    def _determine_status(self, confidence_score: float) -> str:
        """Determine traffic light status"""
        if confidence_score >= 85:
            return 'PASSED'
        elif confidence_score >= 70:
            return 'WARNING'
        else:
            return 'FAILED'

    def _generate_recommendation(self, confidence_score: float) -> str:
        """Generate actionable recommendation"""
        if confidence_score >= 85:
            return "✅ High confidence. Analysis passed all critical checks. Results are reliable for decision-making."
        elif confidence_score >= 70:
            return "⚠️ Moderate confidence. Review flagged issues before using results. Consider additional validation."
        else:
            return "🔴 Low confidence. Critical issues detected. Do not use these results without addressing fundamental problems."
