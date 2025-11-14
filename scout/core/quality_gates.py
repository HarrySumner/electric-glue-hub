"""
Quality Gate Validators
Enforces quality standards at each stage of research
"""

import re
from typing import Dict, List
from datetime import datetime, timedelta
from .data_models import QualityGateResult, QualityGateStatus, VerifiedFact


class QualityGateValidator:
    """Base class for quality gate validators"""

    def __init__(self, gate_number: int, gate_name: str, standards: Dict):
        self.gate_number = gate_number
        self.gate_name = gate_name
        self.standards = standards

    def validate(self, data: Dict) -> QualityGateResult:
        """Validate data against quality standards"""
        raise NotImplementedError


class Gate1_PlanningValidator(QualityGateValidator):
    """Gate 1: Planning Phase Validation"""

    def __init__(self, standards: Dict):
        super().__init__(1, "Planning", standards)

    def validate(self, data: Dict) -> QualityGateResult:
        """Validate research plan is complete"""
        checks = {
            "has_company_name": bool(data.get('company_name')),
            "has_research_type": bool(data.get('research_type')),
            "has_focus_areas": bool(data.get('focus_areas')),
            "has_success_metrics": bool(data.get('success_metrics')),
            "has_time_estimate": bool(data.get('estimated_duration'))
        }

        failures = [
            f"Missing: {check.replace('has_', '').replace('_', ' ')}"
            for check, passed in checks.items()
            if not passed
        ]

        score = (sum(checks.values()) / len(checks)) * 100
        threshold = self.standards.get('minimum_score', 80)

        status = QualityGateStatus.PASSED if score >= threshold else QualityGateStatus.FAILED

        recommendations = []
        if not checks["has_company_name"]:
            recommendations.append("Specify target company name")
        if not checks["has_research_type"]:
            recommendations.append("Define research type (pitch_prep, competitive, etc.)")
        if not checks["has_success_metrics"]:
            recommendations.append("Set success criteria for research")

        return QualityGateResult(
            gate_name=self.gate_name,
            gate_number=self.gate_number,
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )


class Gate2_DataGatheringValidator(QualityGateValidator):
    """Gate 2: Data Gathering Validation"""

    def __init__(self, standards: Dict):
        super().__init__(2, "Data Gathering", standards)

    def validate(self, data: Dict) -> QualityGateResult:
        """Validate sufficient diverse fresh data collected"""
        sources = data.get('sources', [])

        # Count metrics
        unique_sources = len(set(s.get('url') for s in sources))
        source_types = set(s.get('source_type') for s in sources)

        # Check freshness
        fresh_sources = [
            s for s in sources
            if self._is_fresh(s.get('date'), days=180)
        ]

        freshness_ratio = len(fresh_sources) / len(sources) if sources else 0

        min_sources = self.standards.get('minimum_sources', 10)
        min_types = self.standards.get('minimum_source_types', 3)
        min_freshness = self.standards.get('data_freshness_ratio', 0.7)

        checks = {
            "minimum_sources": unique_sources >= min_sources,
            "source_diversity": len(source_types) >= min_types,
            "data_freshness": freshness_ratio >= min_freshness,
            "has_company_official": any(s.get('source_type') == 'company_official' for s in sources),
            "has_third_party_data": any(s.get('source_type') == 'data_provider' for s in sources),
        }

        failures = []
        if not checks["minimum_sources"]:
            failures.append(f"Only {unique_sources}/{min_sources} sources gathered")
        if not checks["source_diversity"]:
            failures.append(f"Only {len(source_types)}/{min_types} source types")
        if not checks["data_freshness"]:
            failures.append(f"Only {len(fresh_sources)}/{len(sources)} sources are fresh (<6 months)")

        score = (sum(checks.values()) / len(checks)) * 100
        threshold = self.standards.get('minimum_score', 80)
        status = QualityGateStatus.PASSED if score >= threshold else QualityGateStatus.FAILED

        recommendations = []
        if not checks["minimum_sources"]:
            recommendations.append(f"Query additional sources (need {min_sources - unique_sources} more)")
        if not checks["source_diversity"]:
            recommendations.append("Add sources from: company official, data providers, news, social media")
        if not checks["data_freshness"]:
            recommendations.append("Prioritize recent sources (<6 months old)")

        return QualityGateResult(
            gate_name=self.gate_name,
            gate_number=self.gate_number,
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )

    def _is_fresh(self, date_str: str, days: int = 180) -> bool:
        """Check if data is within freshness threshold"""
        if not date_str:
            return False
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            threshold = datetime.now() - timedelta(days=days)
            return date >= threshold
        except:
            return False


class Gate3_FactExtractionValidator(QualityGateValidator):
    """Gate 3: Fact Extraction Validation"""

    def __init__(self, standards: Dict):
        super().__init__(3, "Fact Extraction", standards)

    def validate(self, data: Dict) -> QualityGateResult:
        """Validate facts are properly structured and categorized"""
        facts = data.get('facts', [])

        required_fields = [
            'category', 'claim', 'source_name', 'confidence',
            'confidence_rationale', 'relevance_score'
        ]

        # Check completeness
        complete_facts = [
            f for f in facts
            if all(field in f for field in required_fields)
        ]

        # Check categories
        categories = set(f.get('category') for f in facts)
        required_categories = set(self.standards.get('required_categories_list', [
            'PROFILE', 'FINANCIAL', 'STRATEGY', 'MARKETING', 'COMPETITIVE'
        ]))

        # Check relevance
        high_relevance = sum(1 for f in facts if f.get('relevance_score', 0) >= 7)

        min_facts = self.standards.get('minimum_facts', 30)
        min_categories = self.standards.get('required_categories', 5)
        min_high_relevance = self.standards.get('minimum_high_relevance', 15)

        checks = {
            "minimum_facts": len(facts) >= min_facts,
            "facts_complete": len(complete_facts) == len(facts) if facts else False,
            "category_diversity": len(categories) >= min_categories,
            "has_required_categories": required_categories.issubset(categories),
            "high_relevance": high_relevance >= min_high_relevance
        }

        failures = []
        if not checks["minimum_facts"]:
            failures.append(f"Only {len(facts)}/{min_facts} facts extracted")
        if not checks["facts_complete"]:
            incomplete = len(facts) - len(complete_facts)
            failures.append(f"{incomplete} facts missing required fields")
        if not checks["has_required_categories"]:
            missing = required_categories - categories
            failures.append(f"Missing categories: {missing}")

        score = (sum(checks.values()) / len(checks)) * 100
        threshold = self.standards.get('minimum_score', 80)
        status = QualityGateStatus.PASSED if score >= threshold else QualityGateStatus.FAILED

        recommendations = []
        if not checks["minimum_facts"]:
            recommendations.append("Extract more facts from existing sources")
        if not checks["facts_complete"]:
            recommendations.append("Re-run extraction ensuring all required fields are captured")
        if not checks["has_required_categories"]:
            missing = required_categories - categories
            recommendations.append(f"Extract facts in missing categories: {missing}")

        return QualityGateResult(
            gate_name=self.gate_name,
            gate_number=self.gate_number,
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )


class Gate4_VerificationValidator(QualityGateValidator):
    """Gate 4: Verification & Cross-Reference Validation"""

    def __init__(self, standards: Dict):
        super().__init__(4, "Verification", standards)

    def validate(self, data: Dict) -> QualityGateResult:
        """Validate facts are verified and conflicts resolved"""
        verified_facts = data.get('verified_facts', [])

        if not verified_facts:
            return QualityGateResult(
                gate_name=self.gate_name,
                gate_number=self.gate_number,
                status=QualityGateStatus.FAILED,
                score=0,
                checks={},
                failures=["No verified facts provided"],
                recommendations=["Run verification process on extracted facts"]
            )

        # Count confidence levels
        high_confidence = sum(1 for f in verified_facts if f.get('confidence_score', 0) >= 80)
        medium_confidence = sum(1 for f in verified_facts if 50 <= f.get('confidence_score', 0) < 80)
        low_confidence = sum(1 for f in verified_facts if f.get('confidence_score', 0) < 50)

        high_ratio = high_confidence / len(verified_facts)
        low_ratio = low_confidence / len(verified_facts)

        # Check conflicts
        conflicts = [f for f in verified_facts if f.get('has_conflict', False)]
        resolved_conflicts = [f for f in conflicts if f.get('conflict_resolution')]

        # Check credibility scoring
        has_credibility = sum(1 for f in verified_facts if 'source_credibility' in f)

        min_high_conf = self.standards.get('minimum_high_confidence_ratio', 0.5)
        max_low_conf = self.standards.get('maximum_low_confidence_ratio', 0.2)

        checks = {
            "minimum_high_confidence": high_ratio >= min_high_conf,
            "not_too_many_low": low_ratio <= max_low_conf,
            "conflicts_resolved": len(resolved_conflicts) == len(conflicts) if conflicts else True,
            "has_credibility_scores": has_credibility == len(verified_facts),
            "confidence_rationale": all('confidence_score' in f for f in verified_facts)
        }

        failures = []
        if not checks["minimum_high_confidence"]:
            failures.append(f"Only {high_ratio:.0%} high confidence (need {min_high_conf:.0%}+)")
        if not checks["conflicts_resolved"]:
            unresolved = len(conflicts) - len(resolved_conflicts)
            failures.append(f"{unresolved} conflicts unresolved")

        score = (sum(checks.values()) / len(checks)) * 100
        threshold = self.standards.get('minimum_score', 80)
        status = QualityGateStatus.PASSED if score >= threshold else QualityGateStatus.FAILED

        recommendations = []
        if not checks["minimum_high_confidence"]:
            recommendations.append("Cross-reference more sources to increase confidence")
        if not checks["conflicts_resolved"]:
            recommendations.append("Resolve all source conflicts with documented rationale")

        return QualityGateResult(
            gate_name=self.gate_name,
            gate_number=self.gate_number,
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )


class Gate5_AnalysisValidator(QualityGateValidator):
    """Gate 5: Analysis & Synthesis Validation"""

    def __init__(self, standards: Dict):
        super().__init__(5, "Analysis & Synthesis", standards)

    def validate(self, data: Dict) -> QualityGateResult:
        """Validate insights generated, not just facts repeated"""
        analysis = data.get('analysis', {})
        facts_count = data.get('facts_count', 0)
        insights = data.get('insights', [])

        # Calculate insight ratio
        insight_ratio = len(insights) / facts_count if facts_count else 0

        # Check insight quality
        supported_insights = [
            i for i in insights
            if len(i.get('supporting_facts', [])) >= 2
        ]

        # Check for implications
        has_implications = [
            i for i in insights
            if 'implication' in i or 'so_what' in i
        ]

        # Check patterns
        patterns = analysis.get('patterns', [])
        cross_insights = analysis.get('cross_section_insights', [])

        min_insight_ratio = self.standards.get('minimum_insight_ratio', 0.33)
        min_patterns = self.standards.get('minimum_patterns', 3)
        min_cross = self.standards.get('minimum_cross_section_insights', 2)

        checks = {
            "minimum_insight_ratio": insight_ratio >= min_insight_ratio,
            "insights_supported": len(supported_insights) == len(insights) if insights else False,
            "has_implications": len(has_implications) / len(insights) >= 0.8 if insights else False,
            "pattern_recognition": len(patterns) >= min_patterns,
            "strategic_connections": len(cross_insights) >= min_cross
        }

        failures = []
        if not checks["minimum_insight_ratio"]:
            failures.append(f"Insight ratio {insight_ratio:.2f} < {min_insight_ratio:.2f} target")
        if not checks["insights_supported"]:
            unsupported = len(insights) - len(supported_insights)
            failures.append(f"{unsupported} insights lack supporting evidence")

        score = (sum(checks.values()) / len(checks)) * 100
        threshold = self.standards.get('minimum_score', 80)
        status = QualityGateStatus.PASSED if score >= threshold else QualityGateStatus.FAILED

        recommendations = []
        if not checks["minimum_insight_ratio"]:
            recommendations.append("Generate more insights by analyzing patterns in facts")
        if not checks["insights_supported"]:
            recommendations.append("Support each insight with 2+ verifiable facts")
        if not checks["has_implications"]:
            recommendations.append("Add 'So what?' implications to each insight")

        return QualityGateResult(
            gate_name=self.gate_name,
            gate_number=self.gate_number,
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )


class Gate6_BriefGenerationValidator(QualityGateValidator):
    """Gate 6: Brief Generation & Formatting Validation"""

    def __init__(self, standards: Dict):
        super().__init__(6, "Brief Generation", standards)

    def validate(self, data: Dict) -> QualityGateResult:
        """Validate professional writing and formatting"""
        brief = data.get('brief', '')

        # Extract exec summary
        exec_summary = self._extract_section(brief, "Executive Summary")
        exec_words = len(exec_summary.split())

        # Count citations
        citations = len(re.findall(r'\[Source:.*?\]', brief))
        claims = len(re.findall(r'\d+[%KMB$£]', brief))
        citation_ratio = citations / claims if claims else 0

        # Check formatting
        has_headers = len(re.findall(r'^##', brief, re.MULTILINE)) >= 5
        has_tables = '|' in brief and '---' in brief
        has_emphasis = '**' in brief

        # Check structure
        required_sections = self.standards.get('required_sections', [
            "Executive Summary", "Strategic Situation", "Analysis", "Opportunities"
        ])
        has_all_sections = all(section in brief for section in required_sections)

        min_exec_words = self.standards.get('exec_summary_min_words', 150)
        max_exec_words = self.standards.get('exec_summary_max_words', 250)
        min_citation_ratio = self.standards.get('minimum_citation_ratio', 0.7)
        min_word_count = self.standards.get('minimum_word_count', 2000)

        checks = {
            "exec_summary_length": min_exec_words <= exec_words <= max_exec_words,
            "adequate_citations": citation_ratio >= min_citation_ratio,
            "professional_formatting": has_headers and has_emphasis,
            "has_tables": has_tables,
            "complete_structure": has_all_sections,
            "minimum_length": len(brief.split()) >= min_word_count
        }

        failures = []
        if not checks["exec_summary_length"]:
            failures.append(f"Executive summary {exec_words} words (need {min_exec_words}-{max_exec_words})")
        if not checks["adequate_citations"]:
            failures.append(f"Only {citation_ratio:.0%} of claims cited (need {min_citation_ratio:.0%})")
        if not checks["complete_structure"]:
            missing = [s for s in required_sections if s not in brief]
            failures.append(f"Missing sections: {missing}")

        score = (sum(checks.values()) / len(checks)) * 100
        threshold = self.standards.get('minimum_score', 80)
        status = QualityGateStatus.PASSED if score >= threshold else QualityGateStatus.FAILED

        recommendations = []
        if not checks["exec_summary_length"]:
            recommendations.append(f"Revise executive summary to {min_exec_words}-{max_exec_words} words")
        if not checks["adequate_citations"]:
            recommendations.append("Add [Source: X] citations to all quantitative claims")
        if not checks["complete_structure"]:
            recommendations.append("Add missing required sections")

        return QualityGateResult(
            gate_name=self.gate_name,
            gate_number=self.gate_number,
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )

    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract specific section from markdown"""
        pattern = f"## {section_name}.*?(?=##|$)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(0) if match else ""


class Gate7_QualityAssuranceValidator(QualityGateValidator):
    """Gate 7: Final Quality Assurance Validation"""

    def __init__(self, standards: Dict):
        super().__init__(7, "Quality Assurance", standards)

    def validate(self, data: Dict) -> QualityGateResult:
        """Final overall quality check"""
        brief = data.get('brief', '')
        quality_metrics = data.get('quality_metrics', {})

        # Get sub-scores
        citation_score = quality_metrics.get('citation_score', 0)
        insight_score = quality_metrics.get('insight_score', 0)
        readability_score = quality_metrics.get('readability_score', 0)
        actionability_score = quality_metrics.get('actionability_score', 0)
        professional_score = quality_metrics.get('professional_score', 0)

        # Calculate overall
        overall_score = (
            citation_score * 0.2 +
            insight_score * 0.2 +
            readability_score * 0.15 +
            actionability_score * 0.25 +
            professional_score * 0.2
        )

        thresholds = self.standards.get('sub_scores', {})

        checks = {
            "citation_quality": citation_score >= thresholds.get('citation_quality', 70),
            "insight_density": insight_score >= thresholds.get('insight_density', 70),
            "readability": readability_score >= thresholds.get('readability', 70),
            "actionability": actionability_score >= thresholds.get('actionability', 80),
            "professional_tone": professional_score >= thresholds.get('professional_tone', 80),
            "overall_threshold": overall_score >= self.standards.get('minimum_score', 85)
        }

        failures = []
        for check_name, passed in checks.items():
            if not passed:
                score_name = check_name.replace('_', ' ')
                failures.append(f"{score_name} below threshold")

        score = overall_score
        status = QualityGateStatus.PASSED if score >= 85 else QualityGateStatus.FAILED

        recommendations = []
        if not checks["citation_quality"]:
            recommendations.append("Add more source citations to factual claims")
        if not checks["insight_density"]:
            recommendations.append("Increase insight-to-fact ratio with deeper analysis")
        if not checks["actionability"]:
            recommendations.append("Make recommendations more specific and time-bound")
        if not checks["professional_tone"]:
            recommendations.append("Improve writing to C-suite professional standard")

        return QualityGateResult(
            gate_name=self.gate_name,
            gate_number=self.gate_number,
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )
