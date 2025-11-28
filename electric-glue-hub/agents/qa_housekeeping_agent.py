"""
QA Housekeeping Agent - Validates AI outputs before showing to users

This agent acts as a quality gate, catching fabricated statistics,
missing citations, invalid references, and other errors that would
damage user trust.

CRITICAL: If this agent fails to catch a fabrication, the entire
project is considered a failure. It must be rigorous and uncompromising.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import models and prompts
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
sys.path.insert(0, str(Path(__file__).parent.parent / "config"))

from qa_models import (
    ValidationResult,
    ValidationIssue,
    ValidationDecision,
    IssueSeverity,
    IssueType,
    QAConfig
)
from qa_prompts import QA_SYSTEM_PROMPT, get_validation_prompt

# Import mathematical validator for TrustCheck
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
try:
    from mathematical_validator import MathematicalValidator, FlagSeverity
    MATH_VALIDATOR_AVAILABLE = True
except ImportError:
    MATH_VALIDATOR_AVAILABLE = False
    logger.warning("Mathematical validator not available. Skipping rules-based validation.")


class QAHousekeepingAgent:
    """
    Quality Assurance agent that validates outputs before user sees them.

    This agent is the last line of defense against hallucinations, fabrications,
    and errors. It validates that all claims are grounded in verified facts,
    properly cited, and logically consistent.
    """

    def __init__(self, config: Optional[QAConfig] = None):
        """
        Initialize QA agent.

        Parameters
        ----------
        config : QAConfig, optional
            Configuration for validation behavior
        """
        self.config = config or QAConfig()
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

        if not self.anthropic_api_key:
            logger.warning("ANTHROPIC_API_KEY not found. QA validation will use fallback mode.")

        # Setup logging directory
        if self.config.log_all_validations:
            self.log_dir = Path(self.config.log_directory)
            self.log_dir.mkdir(parents=True, exist_ok=True)

    def validate_scout_output(
        self,
        output_content: str,
        company_name: str,
        verified_facts: str,
        sources_used: Optional[List[Dict]] = None
    ) -> ValidationResult:
        """
        Validate Scout marketing intelligence output.

        Parameters
        ----------
        output_content : str
            The complete Scout output to validate
        company_name : str
            Company being analyzed
        verified_facts : str
            Numbered list of verified facts with sources
        sources_used : list of dict, optional
            List of sources used in research

        Returns
        -------
        ValidationResult
            Validation decision (APPROVE/BLOCK/WARN) with issues list
        """
        if not self.config.enabled:
            logger.info("QA validation disabled in config. Skipping validation.")
            return ValidationResult(
                decision=ValidationDecision.APPROVE,
                validation_timestamp=datetime.now().isoformat()
            )

        logger.info(f"Validating Scout output for {company_name}")

        try:
            # Get validation prompt
            validation_prompt = get_validation_prompt(
                tool='scout',
                output_content=output_content,
                company_name=company_name,
                verified_facts=verified_facts
            )

            # Call Claude API for validation
            validation_response = self._call_validation_api(validation_prompt)

            # Parse validation response
            result = self._parse_validation_response(validation_response)

            # Log validation
            if self.config.log_all_validations:
                self._log_validation(
                    tool='scout',
                    company_name=company_name,
                    result=result,
                    output_content=output_content
                )

            # Determine final decision based on config
            if self.config.should_block(result):
                result.decision = ValidationDecision.BLOCK
                logger.warning(f"Scout output BLOCKED: {result.severity_counts}")
            elif result.has_warnings():
                result.decision = ValidationDecision.WARN
                logger.info(f"Scout output APPROVED with warnings: {result.severity_counts}")
            else:
                logger.info("Scout output APPROVED - no issues found")

            return result

        except Exception as e:
            logger.error(f"QA validation failed with error: {e}")
            # On error, be conservative - block output
            return ValidationResult(
                decision=ValidationDecision.BLOCK,
                issues=[
                    ValidationIssue(
                        severity=IssueSeverity.CRITICAL,
                        issue_type=IssueType.CODE_ERROR,
                        description=f"QA validation system error: {str(e)}",
                        recommendation="Fix QA validation system before showing outputs to users"
                    )
                ],
                validation_timestamp=datetime.now().isoformat()
            )

    def validate_causal_analysis(
        self,
        output_content: str,
        campaign_name: str,
        time_period: str,
        metric_name: str,
        data_stats: Dict,
        statistical_results: Dict,
        generated_code: Optional[str] = None
    ) -> ValidationResult:
        """
        Validate Causal Impact Analysis output.

        Parameters
        ----------
        output_content : str
            The complete analysis output to validate
        campaign_name : str
            Name of campaign analyzed
        time_period : str
            Time period of analysis (e.g., "2024-01-01 to 2024-03-31")
        metric_name : str
            Metric being analyzed (e.g., "Daily Revenue")
        data_stats : dict
            Statistics about the raw data:
            - sample_size: int
            - date_range: (start, end)
            - metric_values: summary stats
        statistical_results : dict
            Statistical results from analysis:
            - point_estimate: float
            - confidence_interval: (lower, upper)
            - p_value: float
            - effect_size_pct: float
        generated_code : str, optional
            Python/R code generated (if any)

        Returns
        -------
        ValidationResult
            Validation decision (APPROVE/BLOCK/WARN) with issues list
        """
        if not self.config.enabled:
            logger.info("QA validation disabled in config. Skipping validation.")
            return ValidationResult(
                decision=ValidationDecision.APPROVE,
                validation_timestamp=datetime.now().isoformat()
            )

        logger.info(f"Validating Causal Impact analysis for {campaign_name}")

        try:
            # Get validation prompt
            validation_prompt = get_validation_prompt(
                tool='causal_impact',
                output_content=output_content,
                campaign_name=campaign_name,
                time_period=time_period,
                metric_name=metric_name,
                data_stats=json.dumps(data_stats, indent=2),
                statistical_results=json.dumps(statistical_results, indent=2),
                generated_code=generated_code or 'N/A'
            )

            # Call Claude API for validation
            validation_response = self._call_validation_api(validation_prompt)

            # Parse validation response
            result = self._parse_validation_response(validation_response)

            # Log validation
            if self.config.log_all_validations:
                self._log_validation(
                    tool='causal_impact',
                    campaign_name=campaign_name,
                    result=result,
                    output_content=output_content
                )

            # Determine final decision based on config
            if self.config.should_block(result):
                result.decision = ValidationDecision.BLOCK
                logger.warning(f"Causal analysis BLOCKED: {result.severity_counts}")
            elif result.has_warnings():
                result.decision = ValidationDecision.WARN
                logger.info(f"Causal analysis APPROVED with warnings: {result.severity_counts}")
            else:
                logger.info("Causal analysis APPROVED - no issues found")

            return result

        except Exception as e:
            logger.error(f"QA validation failed with error: {e}")
            # On error, be conservative - block output
            return ValidationResult(
                decision=ValidationDecision.BLOCK,
                issues=[
                    ValidationIssue(
                        severity=IssueSeverity.CRITICAL,
                        issue_type=IssueType.CODE_ERROR,
                        description=f"QA validation system error: {str(e)}",
                        recommendation="Fix QA validation system before showing outputs to users"
                    )
                ],
                validation_timestamp=datetime.now().isoformat()
            )

    def validate_campaign_data(
        self,
        campaign_data: Dict,
        output_content: Optional[str] = None
    ) -> ValidationResult:
        """
        Validate campaign data using mathematical validator FIRST, then LLM validation.

        This is part of TrustCheck - catches synthetic/fabricated data before LLM sees it.

        Parameters
        ----------
        campaign_data : dict
            Campaign metrics: impressions, clicks, conversions, CTR, etc.
        output_content : str, optional
            Narrative output to validate against data

        Returns
        -------
        ValidationResult
            Validation decision with mathematical and LLM validation results
        """
        logger.info("Running mathematical validation on campaign data...")

        # PHASE 1: Mathematical validation (rules-based, no LLM)
        math_issues = []
        if MATH_VALIDATOR_AVAILABLE:
            math_validator = MathematicalValidator()
            math_flags = math_validator.validate_report(campaign_data)

            # Convert mathematical flags to ValidationIssues
            for flag in math_flags:
                # Map severity
                if flag.severity == FlagSeverity.RED:
                    severity = IssueSeverity.CRITICAL
                elif flag.severity == FlagSeverity.AMBER:
                    severity = IssueSeverity.HIGH
                else:
                    severity = IssueSeverity.LOW

                math_issues.append(ValidationIssue(
                    severity=severity,
                    issue_type=IssueType.STATISTICAL_INVALID,
                    description=flag.issue,
                    location=flag.field,
                    evidence=f"Expected: {flag.expected}, Actual: {flag.actual}",
                    recommendation=flag.recommendation
                ))

            math_summary = math_validator.get_summary()
            logger.info(f"Mathematical validation: {math_summary['status']}")

            # If critical mathematical errors found, BLOCK immediately
            if not math_summary['passed']:
                logger.error(f"BLOCKED: {math_summary['red_flags']} critical mathematical errors")
                return ValidationResult(
                    decision=ValidationDecision.BLOCK,
                    issues=math_issues,
                    validation_timestamp=datetime.now().isoformat(),
                    fix_recommendations=[
                        "Fix mathematical inconsistencies in campaign data",
                        "Verify data source and calculation methods",
                        "Do not proceed with LLM validation until data is corrected"
                    ]
                )

        # PHASE 2: LLM validation (only if mathematical validation passed or not available)
        if output_content and self.anthropic_api_key:
            logger.info("Running LLM validation on narrative output...")
            try:
                # Create validation prompt with campaign data
                validation_prompt = f"""Validate the following campaign analysis narrative against the source data.

**Source Campaign Data:**
{json.dumps(campaign_data, indent=2)}

**Narrative Output to Validate:**
{output_content}

Check for:
1. Numbers match source data exactly
2. No fabricated metrics or statistics
3. Logical consistency of interpretations
4. Proper attribution of all claims

Provide validation in JSON format with issues array."""

                validation_response = self._call_validation_api(validation_prompt)
                llm_result = self._parse_validation_response(validation_response)

                # Combine mathematical and LLM issues
                all_issues = math_issues + llm_result.issues

                # Determine final decision
                if any(i.severity == IssueSeverity.CRITICAL for i in all_issues):
                    decision = ValidationDecision.BLOCK
                elif len(all_issues) > 0:
                    decision = ValidationDecision.WARN
                else:
                    decision = ValidationDecision.APPROVE

                return ValidationResult(
                    decision=decision,
                    issues=all_issues,
                    validation_timestamp=datetime.now().isoformat(),
                    fix_recommendations=llm_result.fix_recommendations
                )

            except Exception as e:
                logger.error(f"LLM validation failed: {e}")
                # Return mathematical validation result only
                if math_issues:
                    return ValidationResult(
                        decision=ValidationDecision.WARN,
                        issues=math_issues,
                        validation_timestamp=datetime.now().isoformat()
                    )

        # No output content or no API key - return mathematical validation result
        if math_issues:
            decision = ValidationDecision.WARN if all(i.severity != IssueSeverity.CRITICAL for i in math_issues) else ValidationDecision.BLOCK
            return ValidationResult(
                decision=decision,
                issues=math_issues,
                validation_timestamp=datetime.now().isoformat()
            )
        else:
            return ValidationResult(
                decision=ValidationDecision.APPROVE,
                validation_timestamp=datetime.now().isoformat()
            )

    def _call_validation_api(self, validation_prompt: str) -> str:
        """
        Call Claude API to perform validation.

        Parameters
        ----------
        validation_prompt : str
            Formatted validation prompt

        Returns
        -------
        str : JSON string with validation result
        """
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.anthropic_api_key)

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                system=QA_SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": validation_prompt
                }],
                temperature=0.0  # Deterministic validation
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise

    def _parse_validation_response(self, response_text: str) -> ValidationResult:
        """
        Parse JSON validation response from Claude.

        Parameters
        ----------
        response_text : str
            Raw response text from Claude

        Returns
        -------
        ValidationResult
            Parsed validation result
        """
        try:
            # Extract JSON from response (may be wrapped in markdown)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()

            data = json.loads(response_text)

            # Parse issues
            issues = []
            for issue_data in data.get('issues', []):
                issues.append(ValidationIssue(
                    severity=IssueSeverity[issue_data['severity']],
                    issue_type=IssueType[issue_data['type']],
                    description=issue_data['description'],
                    location=issue_data.get('location'),
                    evidence=issue_data.get('evidence'),
                    recommendation=issue_data.get('recommendation')
                ))

            # Create result
            decision = ValidationDecision[data['decision']]

            return ValidationResult(
                decision=decision,
                issues=issues,
                fix_recommendations=data.get('fix_recommendations', []),
                validation_timestamp=datetime.now().isoformat()
            )

        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse validation response: {e}")
            logger.debug(f"Raw response: {response_text[:500]}")

            # Return conservative result on parse failure
            return ValidationResult(
                decision=ValidationDecision.BLOCK,
                issues=[
                    ValidationIssue(
                        severity=IssueSeverity.CRITICAL,
                        issue_type=IssueType.CODE_ERROR,
                        description=f"Failed to parse QA validation response: {str(e)}",
                        recommendation="Check QA prompt format and Claude API response"
                    )
                ]
            )

    def _log_validation(
        self,
        tool: str,
        company_name: str,
        result: ValidationResult,
        output_content: str
    ):
        """Log validation result to file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = self.log_dir / f"qa_{tool}_{company_name}_{timestamp}.json"

            log_data = {
                'timestamp': result.validation_timestamp,
                'tool': tool,
                'company_name': company_name,
                'decision': result.decision.value,
                'severity_counts': result.severity_counts,
                'issues': [
                    {
                        'severity': issue.severity.value,
                        'type': issue.issue_type.value,
                        'description': issue.description,
                        'location': issue.location
                    }
                    for issue in result.issues
                ],
                'fix_recommendations': result.fix_recommendations,
                'output_content_length': len(output_content)
            }

            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)

            logger.debug(f"Validation logged to {log_file}")

        except Exception as e:
            logger.warning(f"Failed to log validation: {e}")


# Example usage
if __name__ == '__main__':
    # Test Scout validation
    qa_agent = QAHousekeepingAgent()

    test_output = """
### 😈 Devil's Advocate Perspective

**Key Insight:**
Revenue grew 45% YoY to reach $50M annually [Fact #1], but this growth is slowing.

**Recommended Actions:**
1. Investigate customer churn rate
2. Assess competitive threats

**Warning:**
⚠️ High customer acquisition cost may not be sustainable

**Data Gaps:**
Missing: Churn rate, CAC trends, competitor spending
"""

    test_facts = """1. Company raised $10M Series A in March 2024 [Source: TechCrunch, 2024-03-15]
2. Based in London with 50 employees [Source: LinkedIn, 2024-11]
3. Serves B2B SaaS customers [Source: Company website, 2024-11]"""

    result = qa_agent.validate_scout_output(
        output_content=test_output,
        company_name="Test Corp",
        verified_facts=test_facts
    )

    print(result.summary())
    print("\n" + "="*80 + "\n")

    if result.issues:
        print("Issues found:")
        for issue in result.issues:
            print(issue)
            print()
