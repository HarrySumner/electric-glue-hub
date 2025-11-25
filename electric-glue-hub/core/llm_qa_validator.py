"""
LLM-Powered QA Validator for Narrative Outputs
Uses Claude/OpenAI to validate AI-generated insights for hallucinations and accuracy
"""

import os
from typing import Dict, Any, Optional, List
from pathlib import Path
import anthropic
import openai
from dotenv import load_dotenv

load_dotenv()

# Import usage tracker
try:
    from .api_usage_tracker import get_tracker
    TRACKER_AVAILABLE = True
except ImportError:
    try:
        from api_usage_tracker import get_tracker
        TRACKER_AVAILABLE = True
    except ImportError:
        TRACKER_AVAILABLE = False

# QA System Prompt (Report QA Agent)
QA_SYSTEM_PROMPT = """# Report QA Agent - Accuracy Validation System

You are a specialized QA agent designed to validate AI-generated marketing analyses and reports. Your primary function is to identify potential hallucinations, logical inconsistencies, and accuracy issues.

## Core Validation Framework

### 1. Evidence-Based Verification
- **Source Attribution Check**: Every factual claim must be traceable to provided data/documents
- **Data Consistency**: Cross-reference numbers, metrics, and statistics across the report
- **Flag unsupported claims**: Identify any statement that cannot be directly tied to source material
- **Distinguish between**: Analysis/interpretation (acceptable) vs. fabricated data (unacceptable)

### 2. Logical Consistency Checks
- Verify that conclusions logically follow from presented evidence
- Check for contradictory statements within the report
- Ensure recommendations align with identified problems/opportunities
- Validate that percentages, totals, and calculations are mathematically sound

### 3. Confidence Scoring System
For each major claim or section, assign:
- **HIGH CONFIDENCE (90-100%)**: Direct quote/data from source material with context
- **MEDIUM CONFIDENCE (60-89%)**: Reasonable inference from available data
- **LOW CONFIDENCE (30-59%)**: Extrapolation or assumption with limited support
- **FLAG FOR REVIEW (<30%)**: Insufficient evidence or potential hallucination

### 4. Hallucination Detection Patterns
Actively look for these common AI hallucination indicators:
- Overly specific metrics not present in source data (e.g., "increased by 23.7%" when source says "approximately 25%")
- Named entities (companies, people, tools) not mentioned in provided materials
- Dates, timeframes, or version numbers that seem fabricated
- Technical specifications or features not verifiable in sources
- Competitor comparisons without supporting data

## Validation Protocol

### Step 1: Structural Analysis
- List all factual claims made in the report
- Identify the source/basis for each claim
- Note any claims without clear attribution

### Step 2: Cross-Validation
- Compare related statements for consistency
- Verify numerical data adds up correctly
- Check that trends/patterns are uniformly described

### Step 3: Red Flag Assessment
Mark statements that exhibit:
- Unusual specificity without source data
- Contradictions with other parts of the report
- Claims that seem "too good to be true"
- Industry knowledge that goes beyond provided context

## Output Format

Provide your assessment in this structure:

**OVERALL CONFIDENCE SCORE**: [0-100%]

**VALIDATED SECTIONS**:
- [List sections that pass all checks with confidence scores]

**FLAGGED ISSUES**:
1. **[Severity: HIGH/MEDIUM/LOW]** - [Specific claim or section]
   - **Issue**: [What's potentially wrong]
   - **Evidence**: [Why it's flagged]
   - **Recommendation**: [How to fix]

**UNSUPPORTED CLAIMS**:
- [Bullet list of statements lacking source attribution]

**CONFIDENCE BREAKDOWN**:
- High confidence claims: [X%]
- Medium confidence claims: [Y%]
- Low confidence claims: [Z%]

## Critical Rules

1. **Be specific**: Don't say "some claims lack support" - identify exactly which ones
2. **Provide evidence**: Quote the problematic text and explain why it's flagged
3. **Suggest fixes**: Where possible, indicate what evidence would be needed to validate a claim
4. **Distinguish severity**: Not all issues are equal - prioritize potential fabrications over minor inconsistencies
5. **Context matters**: A claim might be accurate industry knowledge but still should be flagged if not tied to the client's specific data

## When to Escalate to Human Review

Automatically flag for human review if:
- Overall confidence score drops below 70%
- Any HIGH severity issues are detected
- More than 3 unsupported claims in a single report
- Contradictory conclusions that could impact strategy
- Missing or insufficient source data to properly validate

Your goal is to build trust in AI-generated outputs by ensuring only accurate, well-supported analyses reach the team."""


class LLMQAValidator:
    """
    LLM-powered QA validator for narrative content validation.

    Complements statistical validation by checking:
    - Narrative coherence
    - Interpretation accuracy
    - Hallucination detection
    - Claim verification
    """

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize LLM QA validator.

        Args:
            model: LLM model to use (Claude or OpenAI)
        """
        self.model = model
        self.anthropic_client = None
        self.openai_client = None

        # Try to initialize clients
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            except:
                pass

        if os.getenv("OPENAI_API_KEY"):
            try:
                self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except:
                pass

    def validate_narrative_output(
        self,
        narrative: str,
        source_data: Dict[str, Any],
        analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate narrative output against source data for hallucinations.

        Args:
            narrative: The narrative text to validate (insights, interpretations, etc.)
            source_data: Source data used for analysis
            analysis_results: Statistical analysis results

        Returns:
            Dictionary with validation results
        """

        # If no LLM available, return fallback
        if not self.anthropic_client and not self.openai_client:
            return self._fallback_validation(narrative, source_data, analysis_results)

        # Prepare validation prompt
        prompt = self._create_validation_prompt(narrative, source_data, analysis_results)

        # Call LLM for validation
        try:
            if self.anthropic_client:
                response = self._validate_with_claude(prompt)
            else:
                response = self._validate_with_openai(prompt)

            # Parse response
            parsed = self._parse_llm_response(response)

            return {
                'status': 'completed',
                'confidence_score': parsed['overall_confidence'],
                'validated_sections': parsed['validated_sections'],
                'flagged_issues': parsed['flagged_issues'],
                'unsupported_claims': parsed['unsupported_claims'],
                'confidence_breakdown': parsed['confidence_breakdown'],
                'raw_response': response,
                'needs_human_review': parsed['overall_confidence'] < 70 or len(parsed['high_severity_issues']) > 0
            }

        except Exception as e:
            print(f"Error in LLM validation: {e}")
            return self._fallback_validation(narrative, source_data, analysis_results)

    def _create_validation_prompt(
        self,
        narrative: str,
        source_data: Dict[str, Any],
        analysis_results: Dict[str, Any]
    ) -> str:
        """Create the validation prompt with context."""

        # Extract key metrics from results
        metrics_summary = f"""
        Campaign Analysis Results:
        - Total Incremental Effect: {analysis_results.get('total_effect', 'N/A')}
        - Average Daily Effect: {analysis_results.get('avg_effect', 'N/A')}
        - Relative Effect: {analysis_results.get('relative_effect', 'N/A')}%
        - Confidence Level: {analysis_results.get('confidence_level', 'N/A')}%
        - MCMC Samples: {analysis_results.get('n_samples', 'N/A')}
        - Convergence Status: {analysis_results.get('convergence', {}).get('message', 'N/A')}
        - Campaign Days: {analysis_results.get('campaign_days', 'N/A')}
        - Measurement Days: {analysis_results.get('measurement_days', 'N/A')}
        """

        # Data summary
        data_summary = f"""
        Source Data:
        - Pre-campaign observations: {analysis_results.get('n_pre_points', 'N/A')}
        - Post-campaign observations: {analysis_results.get('n_post_points', 'N/A')}
        - Campaign Start: {analysis_results.get('intervention_date', 'N/A')}
        - Campaign End: {analysis_results.get('campaign_end_date', 'N/A')}
        """

        prompt = f"""Please validate the following narrative output for a campaign analysis.

{data_summary}

{metrics_summary}

**NARRATIVE TO VALIDATE**:
{narrative}

**YOUR TASK**:
Validate this narrative against the source data and analysis results provided above. Check for:
1. Accuracy of cited numbers and metrics
2. Logical consistency of interpretations
3. Unsupported claims or potential hallucinations
4. Mathematical accuracy of percentages and calculations

Provide your assessment following the specified output format."""

        return prompt

    def _validate_with_claude(self, prompt: str) -> str:
        """Validate using Claude."""
        try:
            message = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=QA_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )

            # Track usage
            if TRACKER_AVAILABLE:
                try:
                    tracker = get_tracker()
                    usage = message.usage
                    tracker.track_call(
                        provider='anthropic',
                        model=self.model,
                        operation='qa_validation',
                        input_tokens=usage.input_tokens,
                        output_tokens=usage.output_tokens,
                        success=True
                    )
                except Exception as e:
                    print(f"Usage tracking failed: {e}")

            return message.content[0].text
        except Exception as e:
            # Track failed call
            if TRACKER_AVAILABLE:
                try:
                    tracker = get_tracker()
                    tracker.track_call(
                        provider='anthropic',
                        model=self.model,
                        operation='qa_validation',
                        input_tokens=0,
                        output_tokens=0,
                        success=False,
                        error=str(e)
                    )
                except:
                    pass
            raise

    def _validate_with_openai(self, prompt: str) -> str:
        """Validate using OpenAI."""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": QA_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )

            # Track usage
            if TRACKER_AVAILABLE:
                try:
                    tracker = get_tracker()
                    usage = response.usage
                    tracker.track_call(
                        provider='openai',
                        model='gpt-4',
                        operation='qa_validation',
                        input_tokens=usage.prompt_tokens,
                        output_tokens=usage.completion_tokens,
                        success=True
                    )
                except Exception as e:
                    print(f"Usage tracking failed: {e}")

            return response.choices[0].message.content
        except Exception as e:
            # Track failed call
            if TRACKER_AVAILABLE:
                try:
                    tracker = get_tracker()
                    tracker.track_call(
                        provider='openai',
                        model='gpt-4',
                        operation='qa_validation',
                        input_tokens=0,
                        output_tokens=0,
                        success=False,
                        error=str(e)
                    )
                except:
                    pass
            raise

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured format."""

        # Simple parsing - extract confidence score
        import re

        confidence_match = re.search(r'OVERALL CONFIDENCE SCORE.*?(\d+)%', response, re.IGNORECASE)
        overall_confidence = int(confidence_match.group(1)) if confidence_match else 50

        # Extract high severity issues
        high_severity = len(re.findall(r'Severity:\s*HIGH', response, re.IGNORECASE))

        # Parse sections (simplified)
        validated_sections = []
        if 'VALIDATED SECTIONS' in response:
            section_text = response.split('VALIDATED SECTIONS')[1].split('FLAGGED ISSUES')[0] if 'FLAGGED ISSUES' in response else response.split('VALIDATED SECTIONS')[1]
            validated_sections = [line.strip() for line in section_text.split('\n') if line.strip() and line.strip().startswith('-')]

        # Extract flagged issues
        flagged_issues = []
        if 'FLAGGED ISSUES' in response:
            issues_text = response.split('FLAGGED ISSUES')[1].split('UNSUPPORTED CLAIMS')[0] if 'UNSUPPORTED CLAIMS' in response else response.split('FLAGGED ISSUES')[1]
            flagged_issues = [line.strip() for line in issues_text.split('\n') if line.strip() and (line.strip().startswith('1.') or line.strip().startswith('2.') or line.strip().startswith('3.'))]

        # Extract unsupported claims
        unsupported = []
        if 'UNSUPPORTED CLAIMS' in response:
            claims_text = response.split('UNSUPPORTED CLAIMS')[1].split('CONFIDENCE BREAKDOWN')[0] if 'CONFIDENCE BREAKDOWN' in response else response.split('UNSUPPORTED CLAIMS')[1]
            unsupported = [line.strip() for line in claims_text.split('\n') if line.strip() and line.strip().startswith('-')]

        return {
            'overall_confidence': overall_confidence,
            'validated_sections': validated_sections,
            'flagged_issues': flagged_issues,
            'unsupported_claims': unsupported,
            'high_severity_issues': high_severity,
            'confidence_breakdown': {
                'high': 0,  # Would need more sophisticated parsing
                'medium': 0,
                'low': 0
            }
        }

    def _fallback_validation(
        self,
        narrative: str,
        source_data: Dict[str, Any],
        analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback validation when LLM not available.
        Uses rule-based checks.
        """

        flags = []
        warnings = []
        confidence = 85  # Start high, deduct for issues

        # Check 1: Look for specific numbers in narrative
        import re
        numbers_in_narrative = re.findall(r'\b\d+\.?\d*%?\b', narrative)

        # Check 2: Verify key metrics are mentioned if they exist
        total_effect = analysis_results.get('total_effect')
        relative_effect = analysis_results.get('relative_effect')

        if total_effect is not None:
            total_str = f"{total_effect:,.0f}"
            if total_str not in narrative and str(int(total_effect)) not in narrative:
                warnings.append("⚠️ Total effect value not found in narrative")
                confidence -= 10

        if relative_effect is not None:
            relative_str = f"{relative_effect:.1f}%"
            if relative_str not in narrative:
                warnings.append("⚠️ Relative effect percentage not found in narrative")
                confidence -= 10

        return {
            'status': 'fallback',
            'confidence_score': max(0, confidence),
            'validated_sections': ['Fallback validation - LLM not available'],
            'flagged_issues': flags,
            'unsupported_claims': warnings,
            'confidence_breakdown': {'high': 0, 'medium': 100, 'low': 0},
            'raw_response': 'Fallback rule-based validation used (no LLM available)',
            'needs_human_review': False,
            'note': 'LLM validation not available. Install anthropic or openai package and set API key for full validation.'
        }
