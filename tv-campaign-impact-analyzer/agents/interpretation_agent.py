"""
Interpretation Agent - LLM-powered natural language explanations
"""

import os
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv

load_dotenv()


class InterpretationAgent:
    """
    Intelligent agent for translating statistical results into plain English.

    Responsibilities:
    - Generate executive summaries
    - Explain statistical concepts in business language
    - Provide actionable recommendations
    - Flag caveats and limitations
    - Create client-ready narratives

    Uses LLM (OpenAI GPT-4 or Anthropic Claude) for natural language generation.
    """

    def __init__(self, provider: str = 'openai'):
        """
        Initialize Interpretation Agent.

        Parameters
        ----------
        provider : str, default 'openai'
            LLM provider: 'openai' or 'anthropic'
        """
        self.provider = provider
        self.llm_client = None
        self.use_llm = os.getenv('USE_LLM_AGENT', 'True').lower() == 'true'

        if self.use_llm:
            self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LLM client based on provider."""
        try:
            if self.provider == 'openai':
                import openai
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    print("⚠️  No OpenAI API key found - using rule-based interpretation")
                    self.use_llm = False
                    return
                openai.api_key = api_key
                self.llm_client = openai
                print("✅ OpenAI LLM initialized")

            elif self.provider == 'anthropic':
                import anthropic
                api_key = os.getenv('ANTHROPIC_API_KEY')
                if not api_key:
                    print("⚠️  No Anthropic API key found - using rule-based interpretation")
                    self.use_llm = False
                    return
                self.llm_client = anthropic.Anthropic(api_key=api_key)
                print("✅ Anthropic Claude initialized")

        except ImportError:
            print(f"⚠️  {self.provider} library not installed - using rule-based interpretation")
            self.use_llm = False

    def interpret(
        self,
        analysis_results: Dict,
        validation_results: Dict,
        business_context: Optional[Dict] = None
    ) -> Dict:
        """
        Generate comprehensive interpretation of analysis results.

        Parameters
        ----------
        analysis_results : dict
            Results from AnalysisAgent
        validation_results : dict
            Results from ValidationAgent
        business_context : dict, optional
            Additional business context:
            - campaign_name: str
            - campaign_budget: float
            - target_metric_name: str (e.g., "bookings", "revenue")
            - industry: str

        Returns
        -------
        dict with:
            - executive_summary: Plain English summary
            - key_findings: List of bullet points
            - recommendations: Actionable next steps
            - caveats: Limitations to note
            - narrative: Full client-ready report
        """
        if not analysis_results.get('success'):
            return {
                'success': False,
                'error': 'Analysis did not succeed - cannot interpret'
            }

        # Extract key metrics
        causal_effect = analysis_results['causal_effect']
        diagnostics = analysis_results.get('diagnostics', {})
        validation = validation_results

        # Generate interpretation
        if self.use_llm:
            interpretation = self._llm_interpret(
                causal_effect,
                diagnostics,
                validation,
                business_context
            )
        else:
            interpretation = self._rule_based_interpret(
                causal_effect,
                diagnostics,
                validation,
                business_context
            )

        return {
            'success': True,
            **interpretation
        }

    def _llm_interpret(
        self,
        causal_effect: Dict,
        diagnostics: Dict,
        validation: Dict,
        business_context: Optional[Dict]
    ) -> Dict:
        """Generate interpretation using LLM."""

        # Prepare prompt
        prompt = self._build_interpretation_prompt(
            causal_effect,
            diagnostics,
            validation,
            business_context
        )

        try:
            if self.provider == 'openai':
                response = self.llm_client.ChatCompletion.create(
                    model='gpt-4',
                    messages=[
                        {
                            'role': 'system',
                            'content': 'You are an expert marketing analyst specializing in causal inference and TV attribution. Translate statistical results into clear, actionable business insights.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )
                interpretation_text = response['choices'][0]['message']['content']

            elif self.provider == 'anthropic':
                message = self.llm_client.messages.create(
                    model='claude-3-5-sonnet-20241022',
                    max_tokens=2000,
                    temperature=0.3,
                    system='You are an expert marketing analyst specializing in causal inference and TV attribution. Translate statistical results into clear, actionable business insights.',
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                )
                interpretation_text = message.content[0].text

            # Parse LLM response into structured format
            parsed = self._parse_llm_response(interpretation_text)

            return parsed

        except Exception as e:
            print(f"⚠️  LLM interpretation failed: {str(e)}")
            print("   Falling back to rule-based interpretation")
            return self._rule_based_interpret(causal_effect, diagnostics, validation, business_context)

    def _build_interpretation_prompt(
        self,
        causal_effect: Dict,
        diagnostics: Dict,
        validation: Dict,
        business_context: Optional[Dict]
    ) -> str:
        """Build prompt for LLM interpretation."""

        context_str = ""
        if business_context:
            context_str = f"""
BUSINESS CONTEXT:
- Campaign: {business_context.get('campaign_name', 'TV Campaign')}
- Budget: £{business_context.get('campaign_budget', 'Unknown'):,}
- Target Metric: {business_context.get('target_metric_name', 'target metric')}
- Industry: {business_context.get('industry', 'Not specified')}
"""

        prompt = f"""
I ran a Bayesian Structural Time Series (BSTS) causal impact analysis on a TV advertising campaign.
Please interpret these results for a marketing executive (non-technical audience).

{context_str}

CAUSAL EFFECT ESTIMATES:
- Average effect per period: {causal_effect['average_effect']:.0f} [{causal_effect['average_effect_lower']:.0f}, {causal_effect['average_effect_upper']:.0f}]
- Relative effect: {causal_effect['relative_effect']*100:.1f}% [{causal_effect['relative_effect_lower']*100:.1f}%, {causal_effect['relative_effect_upper']*100:.1f}%]
- Cumulative effect: {causal_effect['cumulative_effect']:.0f} [{causal_effect['cumulative_lower']:.0f}, {causal_effect['cumulative_upper']:.0f}]
- P-value: {causal_effect['p_value']:.4f}

MODEL QUALITY:
- Pre-period fit: {diagnostics.get('model_quality', 'Unknown')}
- MAPE: {diagnostics.get('pre_period_fit', {}).get('mape', 'N/A'):.1f}%
- R-squared: {diagnostics.get('pre_period_fit', {}).get('r_squared', 'N/A'):.3f}

DATA QUALITY:
- Overall score: {validation.get('score', 'N/A')}/100
- Warnings: {len(validation.get('warnings', []))}
- Key issues: {', '.join(validation.get('warnings', [])[:3])}

Please provide:

1. **EXECUTIVE SUMMARY** (2-3 sentences): Bottom-line result in plain English

2. **KEY FINDINGS** (3-5 bullet points): Main takeaways

3. **RECOMMENDATIONS** (3-5 bullet points): Actionable next steps for the marketing team

4. **CAVEATS** (2-3 bullet points): Important limitations or considerations

5. **NARRATIVE** (2-3 paragraphs): Full story suitable for client report

Format your response as JSON:
{{
    "executive_summary": "...",
    "key_findings": ["...", "..."],
    "recommendations": ["...", "..."],
    "caveats": ["...", "..."],
    "narrative": "..."
}}
"""
        return prompt

    def _parse_llm_response(self, response_text: str) -> Dict:
        """Parse LLM response into structured format."""
        try:
            # Try to extract JSON from response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1

            if start != -1 and end > start:
                json_str = response_text[start:end]
                parsed = json.loads(json_str)
                return parsed
            else:
                # Fallback: treat as plain text
                return {
                    'executive_summary': response_text[:200],
                    'key_findings': [],
                    'recommendations': [],
                    'caveats': [],
                    'narrative': response_text
                }
        except json.JSONDecodeError:
            return {
                'executive_summary': 'LLM response could not be parsed',
                'key_findings': [],
                'recommendations': [],
                'caveats': [],
                'narrative': response_text
            }

    def _rule_based_interpret(
        self,
        causal_effect: Dict,
        diagnostics: Dict,
        validation: Dict,
        business_context: Optional[Dict]
    ) -> Dict:
        """Generate interpretation using rule-based logic (no LLM)."""

        metric_name = business_context.get('target_metric_name', 'target metric') if business_context else 'target metric'
        campaign_name = business_context.get('campaign_name', 'TV campaign') if business_context else 'TV campaign'

        avg_effect = causal_effect['average_effect']
        rel_effect = causal_effect['relative_effect'] * 100
        cum_effect = causal_effect['cumulative_effect']
        p_value = causal_effect['p_value']

        # Executive Summary
        if p_value < 0.05:
            significance = "statistically significant"
            if avg_effect > 0:
                direction = "increased"
            else:
                direction = "decreased"
                avg_effect = abs(avg_effect)

            exec_summary = (
                f"The {campaign_name} had a {significance} positive impact on {metric_name}. "
                f"The campaign {direction} {metric_name} by an average of {avg_effect:,.0f} per period "
                f"({rel_effect:.1f}% relative increase), resulting in a total of {cum_effect:,.0f} "
                f"incremental units over the campaign period."
            )
        else:
            exec_summary = (
                f"The analysis did not detect a statistically significant effect of the {campaign_name} "
                f"on {metric_name} (p = {p_value:.3f}). This could indicate minimal impact, insufficient "
                f"campaign duration, or high baseline variability."
            )

        # Key Findings
        key_findings = []

        if p_value < 0.05:
            key_findings.append(
                f"✅ Campaign drove {avg_effect:,.0f} incremental {metric_name} per period "
                f"(95% credible interval: [{causal_effect['average_effect_lower']:,.0f}, {causal_effect['average_effect_upper']:,.0f}])"
            )
            key_findings.append(
                f"📊 Relative lift of {rel_effect:.1f}% above baseline trend"
            )
            key_findings.append(
                f"💰 Total incremental impact: {cum_effect:,.0f} units"
            )
        else:
            key_findings.append(
                f"⚠️  No statistically significant effect detected (p = {p_value:.3f})"
            )
            key_findings.append(
                f"📉 Point estimate suggests {avg_effect:,.0f} change, but with high uncertainty"
            )

        # Model quality
        model_quality = diagnostics.get('model_quality', 'Unknown')
        key_findings.append(
            f"🔬 Model fit quality: {model_quality} (MAPE: {diagnostics.get('pre_period_fit', {}).get('mape', 'N/A'):.1f}%)"
        )

        # Data quality
        data_score = validation.get('score', 0)
        if data_score >= 80:
            key_findings.append(f"✅ High data quality (score: {data_score}/100)")
        elif data_score >= 60:
            key_findings.append(f"⚠️  Moderate data quality (score: {data_score}/100)")
        else:
            key_findings.append(f"🚨 Low data quality (score: {data_score}/100) - interpret with caution")

        # Recommendations
        recommendations = []

        if p_value < 0.05 and avg_effect > 0:
            recommendations.append(
                "💡 **Continue investment**: The campaign shows measurable positive impact"
            )
            if business_context and business_context.get('campaign_budget'):
                cost_per_unit = business_context['campaign_budget'] / cum_effect
                recommendations.append(
                    f"💰 **Cost efficiency**: £{cost_per_unit:.2f} per incremental {metric_name}"
                )
            recommendations.append(
                "📈 **Scale opportunity**: Consider increasing budget allocation to TV"
            )
        elif p_value >= 0.05:
            recommendations.append(
                "⏸️  **Hold for more data**: Extend campaign duration to improve statistical power"
            )
            recommendations.append(
                "🔍 **Investigate**: Review creative quality, targeting, and media placement"
            )

        # Always recommend methodology
        recommendations.append(
            "✅ **Methodology**: BSTS approach correctly accounts for trends and confounders (avoiding DID pitfalls)"
        )

        # Warnings-based recommendations
        if validation.get('warnings'):
            for warning in validation['warnings'][:2]:
                if 'confounder' in warning.lower():
                    recommendations.append(
                        "🔧 **Control for confounders**: Analysis correctly includes covariates to isolate TV effect"
                    )
                if 'structural break' in warning.lower():
                    recommendations.append(
                        "🚨 **Structural break detected**: BSTS handles this better than traditional DID"
                    )

        # Caveats
        caveats = []

        caveats.append(
            "📊 **Statistical inference**: Results based on Bayesian credible intervals (not frequentist confidence intervals)"
        )

        if data_score < 80:
            caveats.append(
                f"⚠️  **Data quality**: Moderate data quality issues detected (score: {data_score}/100)"
            )

        if validation.get('warnings'):
            caveats.append(
                f"🔍 **Validation warnings**: {len(validation['warnings'])} data quality warnings flagged"
            )

        # Narrative
        narrative = f"""
{exec_summary}

Our Bayesian Structural Time Series (BSTS) analysis provides a robust estimate of the {campaign_name}'s
causal impact on {metric_name}. Unlike traditional methods like Difference-in-Differences (DID), BSTS
explicitly models trends, seasonality, and external factors, making it ideal for TV attribution where
control groups may be contaminated by confounders.

The analysis {'confirms significant positive impact' if p_value < 0.05 else 'suggests limited measurable impact'},
with {'strong' if model_quality == 'Excellent' else 'acceptable'} model fit to historical data.
The credible intervals quantify our uncertainty: we are 95% confident the true effect lies within
[{causal_effect['average_effect_lower']:,.0f}, {causal_effect['average_effect_upper']:,.0f}] per period.

{'This provides clear evidence to support continued TV investment.' if p_value < 0.05 and avg_effect > 0 else
 'We recommend extending the measurement period to improve statistical power and re-running the analysis.'}
"""

        return {
            'executive_summary': exec_summary,
            'key_findings': key_findings,
            'recommendations': recommendations,
            'caveats': caveats,
            'narrative': narrative.strip()
        }

    def generate_client_report(
        self,
        interpretation: Dict,
        include_technical: bool = False
    ) -> str:
        """
        Generate formatted client-ready report.

        Parameters
        ----------
        interpretation : dict
            Interpretation results
        include_technical : bool, default False
            Include technical details

        Returns
        -------
        str : Formatted markdown report
        """
        report = f"""
# TV Campaign Impact Analysis Report

## Executive Summary

{interpretation['executive_summary']}

---

## Key Findings

"""
        for finding in interpretation['key_findings']:
            report += f"- {finding}\n"

        report += f"""
---

## Recommendations

"""
        for rec in interpretation['recommendations']:
            report += f"- {rec}\n"

        report += f"""
---

## Full Analysis

{interpretation['narrative']}

---

## Important Caveats

"""
        for caveat in interpretation['caveats']:
            report += f"- {caveat}\n"

        if include_technical:
            report += """
---

## Technical Methodology

This analysis uses **Bayesian Structural Time Series (BSTS)**, a state-of-the-art causal inference
method that:

- ✅ Models trends, seasonality, and covariates explicitly
- ✅ Provides probabilistic uncertainty quantification
- ✅ Avoids pitfalls of Difference-in-Differences (violated parallel trends)
- ✅ Handles confounders through regression on control variables
- ✅ Generates counterfactual: "What would have happened without the campaign?"

**Why not DID?** Traditional DID requires parallel trends and clean control groups. In TV attribution,
geographic controls often fail due to:
- Ad spillover (streaming, travel)
- Regional economic differences
- External confounders (e.g., flight availability changes)

**BSTS Solution:** No geographic controls needed - builds counterfactual from pre-campaign data only.
"""

        report += """
---

*Generated by Electric Glue TV Campaign Impact Analyzer*
*Powered by Agentic AI and Bayesian Causal Inference*
"""

        return report


# Example usage
if __name__ == '__main__':
    # Mock results
    mock_analysis = {
        'success': True,
        'causal_effect': {
            'average_effect': 48.5,
            'average_effect_lower': 32.1,
            'average_effect_upper': 65.3,
            'relative_effect': 0.182,
            'relative_effect_lower': 0.121,
            'relative_effect_upper': 0.245,
            'cumulative_effect': 8520,
            'cumulative_lower': 5640,
            'cumulative_upper': 11480,
            'p_value': 0.0023
        },
        'diagnostics': {
            'model_quality': 'Excellent',
            'pre_period_fit': {
                'mape': 4.2,
                'r_squared': 0.89
            }
        }
    }

    mock_validation = {
        'score': 87,
        'warnings': [
            '🔍 Potential confounder detected: flights_available',
            '⚠️  3 outliers detected (2.1%)'
        ]
    }

    mock_context = {
        'campaign_name': 'Nielsen Summer TV Campaign',
        'campaign_budget': 450000,
        'target_metric_name': 'bookings',
        'industry': 'Travel & Leisure'
    }

    # Initialize agent (will use rule-based if no API key)
    agent = InterpretationAgent(provider='openai')

    # Generate interpretation
    interpretation = agent.interpret(
        mock_analysis,
        mock_validation,
        mock_context
    )

    if interpretation['success']:
        print('=' * 80)
        print('INTERPRETATION RESULTS')
        print('=' * 80)
        print('\n' + interpretation['executive_summary'] + '\n')

        print('-' * 80)
        print('KEY FINDINGS:')
        print('-' * 80)
        for finding in interpretation['key_findings']:
            print(finding)

        print('\n' + '-' * 80)
        print('RECOMMENDATIONS:')
        print('-' * 80)
        for rec in interpretation['recommendations']:
            print(rec)

        # Generate client report
        report = agent.generate_client_report(interpretation, include_technical=True)

        print('\n\n' + '=' * 80)
        print('CLIENT REPORT (Markdown)')
        print('=' * 80)
        print(report)
