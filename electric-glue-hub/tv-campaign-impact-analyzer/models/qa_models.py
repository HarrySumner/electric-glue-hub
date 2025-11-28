"""
QA Models - Data structures for quality assurance validation

Defines ValidationResult, ValidationIssue, and related models used by
the QA Housekeeping Agent to validate outputs before showing to users.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class ValidationDecision(Enum):
    """Validation decision outcomes."""
    APPROVE = "APPROVE"  # Output is good, show to user
    BLOCK = "BLOCK"      # Critical issues found, DO NOT show to user
    WARN = "WARN"        # Minor issues found, show with warnings


class IssueSeverity(Enum):
    """Severity levels for validation issues."""
    CRITICAL = "CRITICAL"  # Blocks output (fabrication, invalid citations)
    HIGH = "HIGH"          # Serious concern (missing citations, contradictions)
    MEDIUM = "MEDIUM"      # Notable issue (incomplete sections, weak evidence)
    LOW = "LOW"            # Minor quality issue (style, formatting)


class IssueType(Enum):
    """Categories of validation issues."""
    FABRICATION = "FABRICATION"              # Made-up statistics/facts
    MISSING_CITATION = "MISSING_CITATION"    # Factual claim without source
    INVALID_REFERENCE = "INVALID_REFERENCE"  # Citation to non-existent fact
    CONTRADICTION = "CONTRADICTION"          # Conflicting statements
    DATA_INTEGRITY = "DATA_INTEGRITY"        # Data mismatch (e.g., sample size)
    STATISTICAL_INVALID = "STATISTICAL_INVALID"  # Invalid statistical claim
    INTERPRETATION_ERROR = "INTERPRETATION_ERROR"  # Conclusion doesn't match data
    INCOMPLETE = "INCOMPLETE"                # Missing required sections
    CODE_ERROR = "CODE_ERROR"                # Generated code doesn't work
    LOGICAL_INCONSISTENCY = "LOGICAL_INCONSISTENCY"  # Logic doesn't follow


@dataclass
class ValidationIssue:
    """A single validation issue found in output."""

    severity: IssueSeverity
    issue_type: IssueType
    description: str
    location: Optional[str] = None  # Where in output (e.g., "Devil's Advocate section")
    evidence: Optional[str] = None  # Specific text causing issue
    recommendation: Optional[str] = None  # How to fix it

    def __str__(self) -> str:
        """Human-readable issue description."""
        parts = [f"[{self.severity.value}] {self.issue_type.value}: {self.description}"]
        if self.location:
            parts.append(f"  Location: {self.location}")
        if self.evidence:
            # Truncate long evidence
            evidence_short = self.evidence[:200] + "..." if len(self.evidence) > 200 else self.evidence
            parts.append(f"  Evidence: {evidence_short}")
        if self.recommendation:
            parts.append(f"  Fix: {self.recommendation}")
        return "\n".join(parts)


@dataclass
class ValidationResult:
    """Result of QA validation."""

    decision: ValidationDecision
    issues: List[ValidationIssue] = field(default_factory=list)
    severity_counts: Dict[str, int] = field(default_factory=dict)
    fix_recommendations: List[str] = field(default_factory=list)
    validation_timestamp: Optional[str] = None
    validator_version: str = "1.0"

    def __post_init__(self):
        """Calculate severity counts after initialization."""
        self.severity_counts = {
            'CRITICAL': sum(1 for issue in self.issues if issue.severity == IssueSeverity.CRITICAL),
            'HIGH': sum(1 for issue in self.issues if issue.severity == IssueSeverity.HIGH),
            'MEDIUM': sum(1 for issue in self.issues if issue.severity == IssueSeverity.MEDIUM),
            'LOW': sum(1 for issue in self.issues if issue.severity == IssueSeverity.LOW)
        }

    def should_block(self) -> bool:
        """Determine if output should be blocked based on issues."""
        return self.decision == ValidationDecision.BLOCK

    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.issues) > 0

    def get_critical_issues(self) -> List[ValidationIssue]:
        """Get all CRITICAL severity issues."""
        return [issue for issue in self.issues if issue.severity == IssueSeverity.CRITICAL]

    def get_high_issues(self) -> List[ValidationIssue]:
        """Get all HIGH severity issues."""
        return [issue for issue in self.issues if issue.severity == IssueSeverity.HIGH]

    def summary(self) -> str:
        """Get human-readable validation summary."""
        if self.decision == ValidationDecision.APPROVE and not self.issues:
            return "✅ Validation PASSED - No issues found"

        summary_lines = [
            f"{'🚫 BLOCKED' if self.decision == ValidationDecision.BLOCK else '⚠️ APPROVED WITH WARNINGS' if self.decision == ValidationDecision.WARN else '✅ APPROVED'}",
            f"Total issues: {len(self.issues)}",
            f"  CRITICAL: {self.severity_counts.get('CRITICAL', 0)}",
            f"  HIGH: {self.severity_counts.get('HIGH', 0)}",
            f"  MEDIUM: {self.severity_counts.get('MEDIUM', 0)}",
            f"  LOW: {self.severity_counts.get('LOW', 0)}"
        ]

        if self.decision == ValidationDecision.BLOCK and self.get_critical_issues():
            summary_lines.append("\nCritical issues (must fix):")
            for issue in self.get_critical_issues()[:3]:  # Show first 3
                summary_lines.append(f"  - {issue.description}")

        return "\n".join(summary_lines)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'decision': self.decision.value,
            'issues': [
                {
                    'severity': issue.severity.value,
                    'type': issue.issue_type.value,
                    'description': issue.description,
                    'location': issue.location,
                    'evidence': issue.evidence,
                    'recommendation': issue.recommendation
                }
                for issue in self.issues
            ],
            'severity_counts': self.severity_counts,
            'fix_recommendations': self.fix_recommendations,
            'validation_timestamp': self.validation_timestamp,
            'validator_version': self.validator_version
        }


@dataclass
class QAConfig:
    """Configuration for QA validation."""

    # Enable/disable validation
    enabled: bool = True

    # Blocking thresholds
    block_on_critical: bool = True  # Block if any CRITICAL issues
    block_on_high_count: int = 3    # Block if >= N HIGH issues

    # Validation settings
    check_fabrication: bool = True
    check_citations: bool = True
    check_fact_references: bool = True
    check_contradictions: bool = True
    check_data_integrity: bool = True
    check_completeness: bool = True

    # Logging
    log_all_validations: bool = True
    log_blocked_outputs: bool = True
    log_directory: str = "logs/qa_validation"

    # API settings
    max_retries: int = 1  # How many times to retry if validation fails
    timeout_seconds: int = 30

    def should_block(self, validation_result: ValidationResult) -> bool:
        """Determine if output should be blocked based on config and result."""
        if not self.enabled:
            return False

        if self.block_on_critical and validation_result.severity_counts.get('CRITICAL', 0) > 0:
            return True

        if validation_result.severity_counts.get('HIGH', 0) >= self.block_on_high_count:
            return True

        return False


# Example usage
if __name__ == '__main__':
    # Create some example issues
    issues = [
        ValidationIssue(
            severity=IssueSeverity.CRITICAL,
            issue_type=IssueType.FABRICATION,
            description="Output claims 'Revenue grew 45% YoY' without citing source",
            location="Optimist Perspective, Key Insight section",
            evidence="Revenue grew 45% YoY compared to same period last year",
            recommendation="Remove statistic or cite specific fact number that contains this data"
        ),
        ValidationIssue(
            severity=IssueSeverity.HIGH,
            issue_type=IssueType.MISSING_CITATION,
            description="Market share claim lacks citation",
            location="Devil's Advocate section",
            evidence="Company holds 23% market share in premium segment",
            recommendation="Add [Fact #X] citation or remove claim"
        ),
        ValidationIssue(
            severity=IssueSeverity.MEDIUM,
            issue_type=IssueType.INCOMPLETE,
            description="Data gaps section is empty",
            location="Realist Perspective",
            recommendation="Add explanation of what data is missing"
        )
    ]

    # Create validation result
    result = ValidationResult(
        decision=ValidationDecision.BLOCK,
        issues=issues,
        fix_recommendations=[
            "Remove all fabricated statistics",
            "Add citations for market share claims",
            "Complete data gaps sections"
        ]
    )

    print(result.summary())
    print("\n" + "="*80 + "\n")
    print("Detailed issues:")
    for issue in result.issues:
        print(issue)
        print()
