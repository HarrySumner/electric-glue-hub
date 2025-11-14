"""
Quality Agent - Enforces quality standards through 7 mandatory gates
"""

from typing import Dict, List, Optional
from ..core.data_models import QualityGateResult, QualityGateStatus, ResearchState
from ..core.quality_gates import (
    Gate1_PlanningValidator,
    Gate2_DataGatheringValidator,
    Gate3_FactExtractionValidator,
    Gate4_VerificationValidator,
    Gate5_AnalysisValidator,
    Gate6_BriefGenerationValidator,
    Gate7_QualityAssuranceValidator
)


class QualityAgent:
    """
    Quality Agent enforces standards at each research stage

    Responsibilities:
    - Validate output at each of 7 quality gates
    - Provide specific feedback for improvements
    - Track quality metrics over time
    - Prevent low-quality output from progressing
    """

    def __init__(self, quality_standards: Optional[Dict] = None):
        """
        Initialize Quality Agent with quality standards

        Args:
            quality_standards: Optional custom standards, defaults to industry best practices
        """
        self.standards = quality_standards or self._get_default_standards()

        # Initialize all 7 gate validators
        self.validators = {
            1: Gate1_PlanningValidator(self.standards),
            2: Gate2_DataGatheringValidator(self.standards),
            3: Gate3_FactExtractionValidator(self.standards),
            4: Gate4_VerificationValidator(self.standards),
            5: Gate5_AnalysisValidator(self.standards),
            6: Gate6_BriefGenerationValidator(self.standards),
            7: Gate7_QualityAssuranceValidator(self.standards)
        }

        # Track validation history
        self.validation_history: List[QualityGateResult] = []

    def _get_default_standards(self) -> Dict:
        """Get default quality standards"""
        return {
            "minimum_score": 80,
            "minimum_sources": 10,
            "minimum_facts": 30,
            "minimum_verification_rate": 0.5,
            "minimum_insight_ratio": 0.33,
            "minimum_citation_ratio": 0.7,
            "minimum_overall_quality": 85,
            "source_freshness_days": 180,
            "source_freshness_threshold": 0.7,
            "min_source_types": 3,
            "high_confidence_threshold": 0.5,
            "low_confidence_limit": 0.2,
            "min_fact_categories": 5,
            "high_relevance_threshold": 7,
            "min_high_relevance_facts": 15,
            "insight_support_sources": 2,
            "insight_implication_rate": 0.8,
            "min_patterns": 3,
            "exec_summary_min_words": 150,
            "exec_summary_max_words": 250,
            "min_total_words": 2000,
            "component_quality_threshold": 70,
            "actionability_threshold": 80,
            "professional_tone_threshold": 80
        }

    def validate_gate(self, gate_number: int, data: Dict, stage_name: str = "") -> QualityGateResult:
        """
        Validate data at a specific quality gate

        Args:
            gate_number: Gate number (1-7)
            data: Data to validate
            stage_name: Optional stage name for logging

        Returns:
            QualityGateResult with validation details

        Raises:
            ValueError: If gate_number is invalid
        """
        if gate_number not in self.validators:
            raise ValueError(f"Invalid gate number: {gate_number}. Must be 1-7.")

        validator = self.validators[gate_number]
        result = validator.validate(data)

        # Track in history
        self.validation_history.append(result)

        return result

    def get_gate_feedback(self, result: QualityGateResult) -> str:
        """
        Generate human-readable feedback for a gate result

        Args:
            result: QualityGateResult from validation

        Returns:
            Formatted feedback string
        """
        feedback = f"\n{'='*60}\n"
        feedback += f"QUALITY GATE {result.gate_number}: {result.gate_name.upper()}\n"
        feedback += f"{'='*60}\n\n"

        # Status
        status_symbol = "[PASS]" if result.status == QualityGateStatus.PASSED else "[FAIL]"
        feedback += f"{status_symbol} Status: {result.status.value.upper()}\n"
        feedback += f"Score: {result.score:.1f}/100\n\n"

        # Checks
        feedback += "Checks:\n"
        for check, passed in result.checks.items():
            check_symbol = "[+]" if passed else "[-]"
            check_name = check.replace('_', ' ').title()
            feedback += f"  {check_symbol} {check_name}\n"

        # Failures
        if result.failures:
            feedback += f"\n[!] Issues Found ({len(result.failures)}):\n"
            for failure in result.failures:
                feedback += f"  - {failure}\n"

        # Recommendations
        if result.recommendations:
            feedback += f"\n[*] Recommendations:\n"
            for rec in result.recommendations:
                feedback += f"  - {rec}\n"

        feedback += f"\n{'='*60}\n"

        return feedback

    def get_quality_summary(self) -> Dict:
        """
        Get summary of all quality gate results

        Returns:
            Dictionary with quality metrics
        """
        if not self.validation_history:
            return {
                "total_validations": 0,
                "passed": 0,
                "failed": 0,
                "average_score": 0,
                "gates_completed": 0
            }

        passed = sum(1 for r in self.validation_history if r.status == QualityGateStatus.PASSED)
        failed = sum(1 for r in self.validation_history if r.status == QualityGateStatus.FAILED)
        avg_score = sum(r.score for r in self.validation_history) / len(self.validation_history)

        # Count unique gates completed
        gates_completed = len(set(r.gate_number for r in self.validation_history))

        return {
            "total_validations": len(self.validation_history),
            "passed": passed,
            "failed": failed,
            "average_score": avg_score,
            "gates_completed": gates_completed,
            "latest_gate": self.validation_history[-1].gate_number if self.validation_history else 0
        }

    def reset_history(self):
        """Reset validation history"""
        self.validation_history = []

    def get_failed_checks(self, result: QualityGateResult) -> List[str]:
        """
        Get list of failed check names from result

        Args:
            result: QualityGateResult

        Returns:
            List of failed check names
        """
        return [
            check.replace('_', ' ').title()
            for check, passed in result.checks.items()
            if not passed
        ]

    def can_proceed_to_next_stage(self, current_gate: int) -> bool:
        """
        Check if research can proceed to next stage

        Args:
            current_gate: Current gate number

        Returns:
            True if gate passed and can proceed
        """
        if not self.validation_history:
            return False

        # Get latest result for this gate
        gate_results = [r for r in self.validation_history if r.gate_number == current_gate]
        if not gate_results:
            return False

        latest_result = gate_results[-1]
        return latest_result.status == QualityGateStatus.PASSED

    def get_correction_prompts(self, result: QualityGateResult) -> List[str]:
        """
        Generate specific correction prompts based on failures

        Args:
            result: Failed QualityGateResult

        Returns:
            List of correction prompts to guide improvements
        """
        if result.status == QualityGateStatus.PASSED:
            return []

        prompts = []

        # Gate-specific correction guidance
        if result.gate_number == 1:  # Planning
            prompts.append("Review the research plan and ensure all required components are present:")
            prompts.extend([f"  - {rec}" for rec in result.recommendations])

        elif result.gate_number == 2:  # Data Gathering
            prompts.append("Enhance data gathering to meet quality standards:")
            if "minimum_sources" in [f.lower() for f in result.failures]:
                prompts.append("  - Search for additional authoritative sources")
                prompts.append("  - Target: 10+ high-quality sources")
            if "source_diversity" in [f.lower() for f in result.failures]:
                prompts.append("  - Include diverse source types: company official, data providers, news, industry reports")
            if "source_freshness" in [f.lower() for f in result.failures]:
                prompts.append("  - Prioritize recent sources (< 6 months old)")

        elif result.gate_number == 3:  # Fact Extraction
            prompts.append("Improve fact extraction quality and quantity:")
            if "minimum_facts" in [f.lower() for f in result.failures]:
                prompts.append("  - Extract more facts from gathered sources")
                prompts.append("  - Target: 30+ well-structured facts")
            if "category_diversity" in [f.lower() for f in result.failures]:
                prompts.append("  - Categorize facts into diverse categories (5+ categories)")

        elif result.gate_number == 4:  # Verification
            prompts.append("Strengthen fact verification:")
            prompts.extend([f"  - {rec}" for rec in result.recommendations])

        elif result.gate_number == 5:  # Analysis
            prompts.append("Deepen analysis with more insights:")
            if "insight_ratio" in [f.lower() for f in result.failures]:
                prompts.append("  - Generate 1 insight for every 3 facts")
                prompts.append("  - Connect facts to identify patterns and trends")

        elif result.gate_number == 6:  # Brief Generation
            prompts.append("Enhance brief quality and professionalism:")
            prompts.extend([f"  - {rec}" for rec in result.recommendations])

        elif result.gate_number == 7:  # Quality Assurance
            prompts.append("Final quality improvements needed:")
            prompts.extend([f"  - {rec}" for rec in result.recommendations])

        return prompts
