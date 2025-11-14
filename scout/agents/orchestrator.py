"""
Quality-Enforced Orchestrator - Manages research workflow with mandatory quality gates
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from ..core.data_models import (
    ResearchState,
    QualityGateStatus,
    QualityGateResult,
    ResearchRequest,
    ResearchPlan,
    ResearchBrief
)
from .quality_agent import QualityAgent


class QualityEnforcedOrchestrator:
    """
    Orchestrator that enforces quality standards through mandatory gates

    Key Features:
    - State machine with 8 states (7 stages + completion)
    - Mandatory quality gate after each stage
    - Automatic retry with corrections (max 3 attempts per gate)
    - Cannot proceed without passing current gate
    - Tracks all validation attempts and corrections
    """

    MAX_RETRIES_PER_GATE = 3

    def __init__(self, quality_standards: Optional[Dict] = None):
        """
        Initialize orchestrator with quality enforcement

        Args:
            quality_standards: Optional custom quality standards
        """
        self.quality_agent = QualityAgent(quality_standards)
        self.current_state = ResearchState.PLANNING
        self.state_history: List[Tuple[ResearchState, datetime]] = []
        self.gate_attempts: Dict[int, int] = {i: 0 for i in range(1, 8)}
        self.corrections_applied: Dict[int, List[str]] = {i: [] for i in range(1, 8)}
        self.research_data: Dict = {}

    def get_current_state(self) -> ResearchState:
        """Get current research state"""
        return self.current_state

    def get_current_gate(self) -> int:
        """Get current quality gate number based on state"""
        state_to_gate = {
            ResearchState.PLANNING: 1,
            ResearchState.DATA_GATHERING: 2,
            ResearchState.FACT_EXTRACTION: 3,
            ResearchState.VERIFICATION: 4,
            ResearchState.ANALYSIS: 5,
            ResearchState.BRIEF_GENERATION: 6,
            ResearchState.QUALITY_ASSURANCE: 7,
            ResearchState.COMPLETE: 7,  # Already passed all gates
            ResearchState.FAILED: 0
        }
        return state_to_gate.get(self.current_state, 0)

    def validate_current_stage(self, stage_data: Dict) -> Tuple[QualityGateResult, bool]:
        """
        Validate current stage output against quality gate

        Args:
            stage_data: Output from current stage

        Returns:
            Tuple of (QualityGateResult, can_proceed)
        """
        gate_number = self.get_current_gate()

        if gate_number == 0:
            raise ValueError(f"Cannot validate stage {self.current_state.name} - invalid state")

        # Increment attempt counter
        self.gate_attempts[gate_number] += 1

        # Validate
        result = self.quality_agent.validate_gate(
            gate_number=gate_number,
            data=stage_data,
            stage_name=self.current_state.name
        )

        # Store data for potential retry
        self.research_data[self.current_state.name] = stage_data

        # Check if can proceed
        can_proceed = result.status == QualityGateStatus.PASSED

        return result, can_proceed

    def attempt_correction(self, failed_result: QualityGateResult) -> List[str]:
        """
        Get correction prompts for failed gate

        Args:
            failed_result: Failed QualityGateResult

        Returns:
            List of correction prompts
        """
        gate_number = failed_result.gate_number

        # Check if max retries exceeded
        if self.gate_attempts[gate_number] >= self.MAX_RETRIES_PER_GATE:
            return [
                f"[!] MAX RETRIES EXCEEDED for Gate {gate_number}",
                "Research cannot proceed with current quality level.",
                "Options:",
                "  1. Manual intervention required",
                "  2. Adjust quality standards",
                "  3. Gather additional resources"
            ]

        # Get correction prompts from quality agent
        corrections = self.quality_agent.get_correction_prompts(failed_result)

        # Store corrections
        self.corrections_applied[gate_number].extend(corrections)

        # Add retry count information
        remaining_attempts = self.MAX_RETRIES_PER_GATE - self.gate_attempts[gate_number]
        corrections.insert(0, f"\n[RETRY] Attempt {self.gate_attempts[gate_number]}/{self.MAX_RETRIES_PER_GATE}")
        corrections.insert(1, f"Remaining attempts: {remaining_attempts}\n")

        return corrections

    def advance_to_next_stage(self) -> bool:
        """
        Advance to next research stage

        Returns:
            True if successfully advanced, False if cannot advance
        """
        # Record state transition
        self.state_history.append((self.current_state, datetime.now()))

        # Define stage progression
        progression = {
            ResearchState.PLANNING: ResearchState.DATA_GATHERING,
            ResearchState.DATA_GATHERING: ResearchState.FACT_EXTRACTION,
            ResearchState.FACT_EXTRACTION: ResearchState.VERIFICATION,
            ResearchState.VERIFICATION: ResearchState.ANALYSIS,
            ResearchState.ANALYSIS: ResearchState.BRIEF_GENERATION,
            ResearchState.BRIEF_GENERATION: ResearchState.QUALITY_ASSURANCE,
            ResearchState.QUALITY_ASSURANCE: ResearchState.COMPLETE
        }

        if self.current_state not in progression:
            return False

        self.current_state = progression[self.current_state]
        return True

    def mark_as_failed(self):
        """Mark research as failed"""
        self.state_history.append((self.current_state, datetime.now()))
        self.current_state = ResearchState.FAILED

    def get_progress_summary(self) -> Dict:
        """
        Get summary of research progress

        Returns:
            Dictionary with progress information
        """
        total_gates = 7
        completed_gates = 0

        # Count completed gates (passed with attempts)
        for gate_num in range(1, 8):
            if self.gate_attempts[gate_num] > 0:
                # Check if last attempt passed
                gate_results = [r for r in self.quality_agent.validation_history
                              if r.gate_number == gate_num]
                if gate_results and gate_results[-1].status == QualityGateStatus.PASSED:
                    completed_gates += 1

        progress_percentage = (completed_gates / total_gates) * 100

        return {
            "current_state": self.current_state.name,
            "current_gate": self.get_current_gate(),
            "completed_gates": completed_gates,
            "total_gates": total_gates,
            "progress_percentage": progress_percentage,
            "total_attempts": sum(self.gate_attempts.values()),
            "states_visited": len(self.state_history),
            "quality_summary": self.quality_agent.get_quality_summary()
        }

    def get_stage_report(self) -> str:
        """
        Generate formatted report of current stage

        Returns:
            Formatted string report
        """
        progress = self.get_progress_summary()

        report = "\n" + "="*70 + "\n"
        report += "SCOUT INTELLIGENCE PLATFORM - RESEARCH PROGRESS\n"
        report += "="*70 + "\n\n"

        # Progress bar
        completed = progress['completed_gates']
        total = progress['total_gates']
        bar_length = 40
        filled = int((completed / total) * bar_length)
        bar = "#" * filled + "-" * (bar_length - filled)

        report += f"Progress: [{bar}] {progress['progress_percentage']:.1f}%\n"
        report += f"Completed: {completed}/{total} quality gates\n\n"

        # Current state
        report += f"Current State: {self.current_state.name}\n"
        report += f"Current Gate: Gate {self.get_current_gate()}\n"
        report += f"Total Validation Attempts: {progress['total_attempts']}\n\n"

        # Gate attempts breakdown
        report += "Gate Attempts:\n"
        for gate_num in range(1, 8):
            attempts = self.gate_attempts[gate_num]
            if attempts > 0:
                gate_results = [r for r in self.quality_agent.validation_history
                              if r.gate_number == gate_num]
                if gate_results:
                    latest = gate_results[-1]
                    status_symbol = "[PASS]" if latest.status == QualityGateStatus.PASSED else "[PEND]"
                    report += f"  {status_symbol} Gate {gate_num}: {attempts} attempt(s) - Score: {latest.score:.1f}/100\n"

        report += "\n" + "="*70 + "\n"

        return report

    def execute_research_workflow(self, request: ResearchRequest) -> ResearchBrief:
        """
        Execute complete research workflow with quality enforcement

        This is a placeholder for the full workflow integration.
        When research agents are implemented, this will orchestrate:
        1. Planning with Gate 1 validation
        2. Data gathering with Gate 2 validation
        3. Fact extraction with Gate 3 validation
        4. Verification with Gate 4 validation
        5. Analysis with Gate 5 validation
        6. Brief generation with Gate 6 validation
        7. Quality assurance with Gate 7 validation

        Args:
            request: ResearchRequest from user

        Returns:
            ResearchBrief (high-quality intelligence output)
        """
        raise NotImplementedError(
            "Full workflow execution will be implemented with research agents. "
            "This orchestrator provides the quality enforcement framework."
        )

    def reset(self):
        """Reset orchestrator to initial state"""
        self.current_state = ResearchState.PLANNING
        self.state_history = []
        self.gate_attempts = {i: 0 for i in range(1, 8)}
        self.corrections_applied = {i: [] for i in range(1, 8)}
        self.research_data = {}
        self.quality_agent.reset_history()
