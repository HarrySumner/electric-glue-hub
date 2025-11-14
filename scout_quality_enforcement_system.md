# SCOUT QUALITY ENFORCEMENT SYSTEM
## Agentic System with Mandatory Quality Gates

---

## 🎯 OVERVIEW

This document defines an **agentic quality enforcement system** that ensures Scout always follows quality steps through:

1. **Mandatory Gate System**: Each stage must pass validation before proceeding
2. **Quality Agent**: Dedicated agent that enforces standards
3. **Feedback Loops**: Automatic revision when quality thresholds not met
4. **State Machine**: Explicit workflow states preventing shortcuts

**Core Principle**: The system should make it **impossible** to produce low-quality output, not just discourage it.

---

## 🏗️ ARCHITECTURE: STATE MACHINE WITH QUALITY GATES

```
┌────────────────────────────────────────────────────────────────┐
│                    RESEARCH REQUEST                             │
│                 (User: "Research Glossier")                     │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│  STATE 1: PLANNING                                              │
│  • Parse request                                               │
│  • Identify research type                                      │
│  • Define success criteria                                     │
│                                                                │
│  QUALITY GATE 1: ✅ Clear research scope defined               │
│                  ✅ Success metrics established                │
└────────────────────────────────────────────────────────────────┘
                            ↓ [GATE PASSED]
┌────────────────────────────────────────────────────────────────┐
│  STATE 2: DATA GATHERING                                        │
│  • Query multiple APIs                                         │
│  • Web scraping                                                │
│  • Source diversity check                                      │
│                                                                │
│  QUALITY GATE 2: ✅ Minimum 10 unique sources                  │
│                  ✅ At least 3 source types                    │
│                  ✅ Data freshness check (<180 days)           │
└────────────────────────────────────────────────────────────────┘
                            ↓ [GATE PASSED]
┌────────────────────────────────────────────────────────────────┐
│  STATE 3: FACT EXTRACTION                                       │
│  • Structured extraction via LLM                               │
│  • Category assignment                                         │
│  • Preliminary confidence scoring                              │
│                                                                │
│  QUALITY GATE 3: ✅ Minimum 30 facts extracted                 │
│                  ✅ All facts have required fields             │
│                  ✅ Facts span 5+ categories                   │
└────────────────────────────────────────────────────────────────┘
                            ↓ [GATE PASSED]
┌────────────────────────────────────────────────────────────────┐
│  STATE 4: VERIFICATION                                          │
│  • Cross-source fact checking                                  │
│  • Conflict resolution                                         │
│  • Final confidence scoring                                    │
│                                                                │
│  QUALITY GATE 4: ✅ 70%+ facts have HIGH confidence            │
│                  ✅ All conflicts documented                   │
│                  ✅ Source credibility scored                  │
└────────────────────────────────────────────────────────────────┘
                            ↓ [GATE PASSED]
┌────────────────────────────────────────────────────────────────┐
│  STATE 5: ANALYSIS & SYNTHESIS                                  │
│  • Pattern recognition                                         │
│  • Insight generation                                          │
│  • Strategic implications                                      │
│                                                                │
│  QUALITY GATE 5: ✅ Insight:Fact ratio ≥ 1:3                   │
│                  ✅ All insights supported by 2+ facts         │
│                  ✅ Strategic implications identified          │
└────────────────────────────────────────────────────────────────┘
                            ↓ [GATE PASSED]
┌────────────────────────────────────────────────────────────────┐
│  STATE 6: BRIEF GENERATION                                      │
│  • Professional writing                                        │
│  • Structured formatting                                       │
│  • Executive summary creation                                  │
│                                                                │
│  QUALITY GATE 6: ✅ Executive summary ≤ 250 words              │
│                  ✅ All quantitative claims cited              │
│                  ✅ Professional formatting verified           │
└────────────────────────────────────────────────────────────────┘
                            ↓ [GATE PASSED]
┌────────────────────────────────────────────────────────────────┐
│  STATE 7: QUALITY ASSURANCE                                     │
│  • Automated quality scoring                                   │
│  • Readability check                                           │
│  • Actionability verification                                  │
│                                                                │
│  QUALITY GATE 7: ✅ Overall quality score ≥ 85/100             │
│                  ✅ All sections pass minimum standards        │
│                  ✅ Recommendations actionable                 │
└────────────────────────────────────────────────────────────────┘
                            ↓ [GATE PASSED]
┌────────────────────────────────────────────────────────────────┐
│  STATE 8: DELIVERY                                              │
│  • Format for output (Google Doc, PDF, Slack)                 │
│  • Metadata attachment                                         │
│  • Archive for future reference                                │
└────────────────────────────────────────────────────────────────┘

                    [IF ANY GATE FAILS]
                            ↓
┌────────────────────────────────────────────────────────────────┐
│  REVISION STATE                                                 │
│  • Identify specific failures                                  │
│  • Re-execute failed stage with corrections                    │
│  • Retry gate validation                                       │
│  • Max 3 retries per gate                                      │
└────────────────────────────────────────────────────────────────┘
```

---

## 🤖 THE QUALITY AGENT

### Dedicated Quality Enforcement Agent

```python
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class QualityGateStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_REVISION = "needs_revision"

@dataclass
class QualityGateResult:
    gate_name: str
    status: QualityGateStatus
    score: float  # 0-100
    checks: Dict[str, bool]
    failures: List[str]
    recommendations: List[str]

class QualityAgent:
    """
    Dedicated agent that enforces quality standards at each stage.
    Acts as a gatekeeper - nothing proceeds without passing quality checks.
    """

    def __init__(self, standards: Dict):
        self.standards = standards
        self.strict_mode = True  # No bypassing gates

    def validate_gate(
        self,
        gate_number: int,
        data: Dict,
        stage_name: str
    ) -> QualityGateResult:
        """
        Validate that data meets quality standards for this gate.

        Returns:
            QualityGateResult with pass/fail status and specific feedback
        """

        gate_validator = getattr(self, f"_validate_gate_{gate_number}")
        return gate_validator(data, stage_name)

    def _validate_gate_1_planning(
        self,
        data: Dict,
        stage_name: str
    ) -> QualityGateResult:
        """
        GATE 1: Planning Phase
        Ensures research scope is clearly defined
        """

        checks = {
            "has_company_name": bool(data.get('company_name')),
            "has_research_type": bool(data.get('research_type')),
            "has_focus_areas": bool(data.get('focus_areas')),
            "has_success_metrics": bool(data.get('success_metrics')),
            "has_time_estimate": bool(data.get('estimated_duration'))
        }

        failures = [
            check_name for check_name, passed in checks.items()
            if not passed
        ]

        score = (sum(checks.values()) / len(checks)) * 100

        if score >= 80:  # Must pass 80% of checks
            status = QualityGateStatus.PASSED
            recommendations = []
        else:
            status = QualityGateStatus.FAILED
            recommendations = [
                f"Missing: {failure.replace('has_', '').replace('_', ' ')}"
                for failure in failures
            ]

        return QualityGateResult(
            gate_name="Gate 1: Planning",
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )

    def _validate_gate_2_data_gathering(
        self,
        data: Dict,
        stage_name: str
    ) -> QualityGateResult:
        """
        GATE 2: Data Gathering
        Ensures sufficient, diverse, fresh data collected
        """

        sources = data.get('sources', [])

        # Count unique sources
        unique_sources = len(set(s['url'] for s in sources))

        # Count source types
        source_types = set(s.get('type') for s in sources)

        # Check data freshness
        from datetime import datetime, timedelta
        fresh_sources = [
            s for s in sources
            if self._is_fresh(s.get('date'), days=180)
        ]

        checks = {
            "minimum_sources": unique_sources >= 10,
            "source_diversity": len(source_types) >= 3,
            "data_freshness": len(fresh_sources) / len(sources) >= 0.7,
            "has_company_official": any(s.get('type') == 'company_official' for s in sources),
            "has_third_party_data": any(s.get('type') == 'data_provider' for s in sources),
        }

        failures = []
        if not checks["minimum_sources"]:
            failures.append(f"Only {unique_sources}/10 sources gathered")
        if not checks["source_diversity"]:
            failures.append(f"Only {len(source_types)}/3 source types")
        if not checks["data_freshness"]:
            failures.append(f"Only {len(fresh_sources)}/{len(sources)} sources are fresh")

        score = (sum(checks.values()) / len(checks)) * 100

        status = QualityGateStatus.PASSED if score >= 80 else QualityGateStatus.FAILED

        recommendations = []
        if not checks["minimum_sources"]:
            recommendations.append("Query additional data sources")
        if not checks["source_diversity"]:
            recommendations.append("Add sources from: news, data providers, social media")
        if not checks["data_freshness"]:
            recommendations.append("Prioritize recent sources (<6 months)")

        return QualityGateResult(
            gate_name="Gate 2: Data Gathering",
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )

    def _validate_gate_3_fact_extraction(
        self,
        data: Dict,
        stage_name: str
    ) -> QualityGateResult:
        """
        GATE 3: Fact Extraction
        Ensures facts are properly structured and categorized
        """

        facts = data.get('facts', [])

        # Required fields for each fact
        required_fields = [
            'category', 'claim', 'source', 'confidence',
            'confidence_rationale', 'relevance'
        ]

        # Check each fact has required fields
        complete_facts = [
            f for f in facts
            if all(field in f for field in required_fields)
        ]

        # Count categories represented
        categories = set(f.get('category') for f in facts)
        required_categories = {
            'PROFILE', 'FINANCIAL', 'STRATEGY',
            'MARKETING', 'COMPETITIVE'
        }

        checks = {
            "minimum_facts": len(facts) >= 30,
            "facts_complete": len(complete_facts) == len(facts),
            "category_diversity": len(categories) >= 5,
            "has_required_categories": required_categories.issubset(categories),
            "high_relevance": sum(1 for f in facts if f.get('relevance', 0) >= 7) >= 15
        }

        failures = []
        if not checks["minimum_facts"]:
            failures.append(f"Only {len(facts)}/30 facts extracted")
        if not checks["facts_complete"]:
            incomplete = len(facts) - len(complete_facts)
            failures.append(f"{incomplete} facts missing required fields")
        if not checks["category_diversity"]:
            failures.append(f"Only {len(categories)}/5 categories represented")

        score = (sum(checks.values()) / len(checks)) * 100
        status = QualityGateStatus.PASSED if score >= 80 else QualityGateStatus.FAILED

        recommendations = []
        if not checks["minimum_facts"]:
            recommendations.append("Extract more facts from existing sources")
        if not checks["facts_complete"]:
            recommendations.append("Re-run extraction with complete field requirements")
        if not checks["has_required_categories"]:
            missing = required_categories - categories
            recommendations.append(f"Extract facts in missing categories: {missing}")

        return QualityGateResult(
            gate_name="Gate 3: Fact Extraction",
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )

    def _validate_gate_4_verification(
        self,
        data: Dict,
        stage_name: str
    ) -> QualityGateResult:
        """
        GATE 4: Verification
        Ensures facts are verified and conflicts resolved
        """

        verified_facts = data.get('verified_facts', [])

        # Count confidence levels
        high_confidence = [f for f in verified_facts if f.get('confidence') == 'HIGH']
        medium_confidence = [f for f in verified_facts if f.get('confidence') == 'MEDIUM']
        low_confidence = [f for f in verified_facts if f.get('confidence') == 'LOW']

        # Check for conflict resolution
        conflicts = [f for f in verified_facts if f.get('has_conflict', False)]
        resolved_conflicts = [
            f for f in conflicts
            if f.get('conflict_resolution')
        ]

        # Check source credibility scoring
        has_credibility_scores = [
            f for f in verified_facts
            if 'source_credibility' in f
        ]

        checks = {
            "minimum_high_confidence": len(high_confidence) / len(verified_facts) >= 0.5,
            "not_too_many_low": len(low_confidence) / len(verified_facts) <= 0.2,
            "conflicts_resolved": len(resolved_conflicts) == len(conflicts),
            "has_credibility_scores": len(has_credibility_scores) == len(verified_facts),
            "confidence_rationale": all(
                'confidence_rationale' in f
                for f in verified_facts
            )
        }

        failures = []
        if not checks["minimum_high_confidence"]:
            pct = len(high_confidence) / len(verified_facts) * 100
            failures.append(f"Only {pct:.0f}% high confidence (need 50%+)")
        if not checks["conflicts_resolved"]:
            unresolved = len(conflicts) - len(resolved_conflicts)
            failures.append(f"{unresolved} conflicts unresolved")

        score = (sum(checks.values()) / len(checks)) * 100
        status = QualityGateStatus.PASSED if score >= 80 else QualityGateStatus.FAILED

        recommendations = []
        if not checks["minimum_high_confidence"]:
            recommendations.append("Cross-reference more sources to increase confidence")
        if not checks["conflicts_resolved"]:
            recommendations.append("Resolve all source conflicts with documented rationale")

        return QualityGateResult(
            gate_name="Gate 4: Verification",
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )

    def _validate_gate_5_analysis(
        self,
        data: Dict,
        stage_name: str
    ) -> QualityGateResult:
        """
        GATE 5: Analysis & Synthesis
        Ensures insights are generated, not just facts repeated
        """

        analysis = data.get('analysis', {})
        facts_used = data.get('facts_count', 0)
        insights = data.get('insights', [])

        # Calculate insight ratio
        insight_ratio = len(insights) / max(facts_used, 1) if facts_used else 0

        # Check insight quality
        supported_insights = [
            i for i in insights
            if len(i.get('supporting_facts', [])) >= 2
        ]

        # Check for strategic implications
        has_implications = [
            i for i in insights
            if 'implication' in i or 'so_what' in i
        ]

        # Check for pattern recognition
        patterns = analysis.get('patterns', [])

        checks = {
            "minimum_insight_ratio": insight_ratio >= 0.33,  # 1 insight per 3 facts
            "insights_supported": len(supported_insights) == len(insights),
            "has_implications": len(has_implications) / len(insights) >= 0.8,
            "pattern_recognition": len(patterns) >= 3,
            "strategic_connections": len(analysis.get('cross_section_insights', [])) >= 2
        }

        failures = []
        if not checks["minimum_insight_ratio"]:
            failures.append(f"Insight ratio {insight_ratio:.2f} < 0.33 target")
        if not checks["insights_supported"]:
            unsupported = len(insights) - len(supported_insights)
            failures.append(f"{unsupported} insights lack supporting evidence")

        score = (sum(checks.values()) / len(checks)) * 100
        status = QualityGateStatus.PASSED if score >= 80 else QualityGateStatus.FAILED

        recommendations = []
        if not checks["minimum_insight_ratio"]:
            recommendations.append("Generate more insights by analyzing patterns in facts")
        if not checks["insights_supported"]:
            recommendations.append("Support each insight with 2+ verifiable facts")
        if not checks["has_implications"]:
            recommendations.append("Add 'So what?' implications to each insight")

        return QualityGateResult(
            gate_name="Gate 5: Analysis & Synthesis",
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )

    def _validate_gate_6_brief_generation(
        self,
        data: Dict,
        stage_name: str
    ) -> QualityGateResult:
        """
        GATE 6: Brief Generation
        Ensures professional writing and formatting standards
        """

        brief = data.get('brief', '')

        # Extract executive summary
        exec_summary = self._extract_section(brief, "Executive Summary")

        # Count citations
        import re
        citations = len(re.findall(r'\[Source:.*?\]', brief))
        quantitative_claims = len(re.findall(r'\d+[%KMB$]', brief))

        # Check formatting
        has_headers = len(re.findall(r'^##', brief, re.MULTILINE)) >= 5
        has_tables = '|' in brief and '---' in brief
        has_emphasis = '**' in brief

        # Check structure
        required_sections = [
            "Executive Summary",
            "Strategic Situation",
            "Analysis",
            "Opportunities"
        ]
        has_all_sections = all(section in brief for section in required_sections)

        checks = {
            "exec_summary_length": 150 <= len(exec_summary.split()) <= 250,
            "adequate_citations": citations / max(quantitative_claims, 1) >= 0.7,
            "professional_formatting": has_headers and has_emphasis,
            "has_tables": has_tables,
            "complete_structure": has_all_sections,
            "minimum_length": len(brief.split()) >= 2000
        }

        failures = []
        if not checks["exec_summary_length"]:
            word_count = len(exec_summary.split())
            failures.append(f"Executive summary {word_count} words (need 150-250)")
        if not checks["adequate_citations"]:
            pct = citations / max(quantitative_claims, 1) * 100
            failures.append(f"Only {pct:.0f}% of claims cited")
        if not checks["complete_structure"]:
            missing = [s for s in required_sections if s not in brief]
            failures.append(f"Missing sections: {missing}")

        score = (sum(checks.values()) / len(checks)) * 100
        status = QualityGateStatus.PASSED if score >= 80 else QualityGateStatus.FAILED

        recommendations = []
        if not checks["exec_summary_length"]:
            recommendations.append("Revise executive summary to 150-250 words")
        if not checks["adequate_citations"]:
            recommendations.append("Add [Source: X] citations to all quantitative claims")
        if not checks["complete_structure"]:
            recommendations.append("Add missing required sections")

        return QualityGateResult(
            gate_name="Gate 6: Brief Generation",
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )

    def _validate_gate_7_quality_assurance(
        self,
        data: Dict,
        stage_name: str
    ) -> QualityGateResult:
        """
        GATE 7: Final Quality Assurance
        Overall quality scoring and actionability check
        """

        brief = data.get('brief', '')
        opportunities = data.get('opportunities', [])

        # Calculate quality sub-scores
        citation_score = self._score_citations(brief)
        insight_score = self._score_insights(brief)
        readability_score = self._score_readability(brief)
        actionability_score = self._score_actionability(opportunities)
        professional_score = self._score_professionalism(brief)

        overall_score = (
            citation_score * 0.2 +
            insight_score * 0.2 +
            readability_score * 0.15 +
            actionability_score * 0.25 +
            professional_score * 0.2
        )

        checks = {
            "citation_quality": citation_score >= 70,
            "insight_density": insight_score >= 70,
            "readability": readability_score >= 70,
            "actionability": actionability_score >= 80,
            "professional_tone": professional_score >= 80,
            "overall_threshold": overall_score >= 85
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
            recommendations.append("Increase insight-to-fact ratio")
        if not checks["actionability"]:
            recommendations.append("Make recommendations more specific and time-bound")
        if not checks["professional_tone"]:
            recommendations.append("Improve writing to C-suite professional standard")

        return QualityGateResult(
            gate_name="Gate 7: Quality Assurance",
            status=status,
            score=score,
            checks=checks,
            failures=failures,
            recommendations=recommendations
        )

    # Helper methods
    def _is_fresh(self, date_str: str, days: int = 180) -> bool:
        """Check if data is within freshness threshold"""
        from datetime import datetime, timedelta

        if not date_str:
            return False

        try:
            date = datetime.fromisoformat(date_str)
            threshold = datetime.now() - timedelta(days=days)
            return date >= threshold
        except:
            return False

    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from markdown text"""
        import re

        pattern = f"## {section_name}.*?(?=##|$)"
        match = re.search(pattern, text, re.DOTALL)

        return match.group(0) if match else ""

    def _score_citations(self, brief: str) -> float:
        """Score citation quality (0-100)"""
        import re

        citations = len(re.findall(r'\[Source:.*?\]', brief))
        claims = len(re.findall(r'\d+[%KMB$]', brief))

        if claims == 0:
            return 100

        ratio = citations / claims
        return min(100, ratio * 100)

    def _score_insights(self, brief: str) -> float:
        """Score insight density (0-100)"""
        # This would use LLM to count facts vs insights
        # Simplified version:
        words = len(brief.split())
        insight_markers = len(re.findall(
            r'(suggests|indicates|reveals|demonstrates|implies)',
            brief,
            re.IGNORECASE
        ))

        density = insight_markers / (words / 100)  # per 100 words
        return min(100, density * 20)

    def _score_readability(self, brief: str) -> float:
        """Score readability (0-100)"""
        # Simplified Flesch-Kincaid-style scoring
        sentences = brief.split('.')
        words = brief.split()

        if len(sentences) == 0:
            return 0

        avg_sentence_length = len(words) / len(sentences)

        # Optimal: 15-20 words per sentence
        if 15 <= avg_sentence_length <= 20:
            return 100
        elif 10 <= avg_sentence_length <= 25:
            return 80
        else:
            return 60

    def _score_actionability(self, opportunities: List[Dict]) -> float:
        """Score how actionable recommendations are (0-100)"""
        if not opportunities:
            return 0

        actionable_count = 0
        for opp in opportunities:
            # Check for actionability markers
            has_specific_value = bool(re.search(r'\$\d+K', str(opp)))
            has_timeframe = bool(re.search(r'\d+ (days|weeks|months)', str(opp)))
            has_specific_action = bool(re.search(
                r'(launch|build|create|implement|partner)',
                str(opp),
                re.IGNORECASE
            ))

            if sum([has_specific_value, has_timeframe, has_specific_action]) >= 2:
                actionable_count += 1

        return (actionable_count / len(opportunities)) * 100

    def _score_professionalism(self, brief: str) -> float:
        """Score professional tone (0-100)"""
        # Check for unprofessional markers
        unprofessional_patterns = [
            r'\b(really|very|pretty|quite|maybe|perhaps)\b',  # Hedging
            r'\b(awesome|cool|nice|great)\b',  # Casual language
            r'!!!',  # Excessive punctuation
            r'\b(I think|I believe|we think)\b'  # First person opinion
        ]

        words = len(brief.split())
        unprofessional_count = sum(
            len(re.findall(pattern, brief, re.IGNORECASE))
            for pattern in unprofessional_patterns
        )

        density = unprofessional_count / (words / 100)

        # Penalty: -5 points per occurrence per 100 words
        score = max(0, 100 - (density * 5))

        return score
```

---

## 🔄 ORCHESTRATOR WITH QUALITY GATES

### Enforced State Machine

```python
from typing import Dict, Optional
from enum import Enum

class ResearchState(Enum):
    PLANNING = 1
    DATA_GATHERING = 2
    FACT_EXTRACTION = 3
    VERIFICATION = 4
    ANALYSIS = 5
    BRIEF_GENERATION = 6
    QUALITY_ASSURANCE = 7
    COMPLETE = 8
    FAILED = 99

class QualityEnforcedOrchestrator:
    """
    Orchestrator that enforces quality gates at each stage.
    Cannot proceed to next stage without passing current gate.
    """

    def __init__(self):
        self.quality_agent = QualityAgent(standards={})
        self.max_retries_per_gate = 3
        self.current_state = ResearchState.PLANNING
        self.state_data = {}
        self.gate_results = {}

    def research_company(
        self,
        company_name: str,
        research_type: str,
        focus_areas: Optional[List[str]] = None
    ) -> Dict:
        """
        Main entry point - enforces quality at each stage
        """

        print(f"🎯 Starting research for {company_name}")
        print(f"   Type: {research_type}")
        print(f"   Quality enforcement: ACTIVE")
        print()

        # STATE 1: PLANNING
        planning_data = self._execute_stage_with_gate(
            stage=ResearchState.PLANNING,
            executor=lambda: self._plan_research(
                company_name,
                research_type,
                focus_areas
            ),
            gate_number=1
        )

        # STATE 2: DATA GATHERING
        data = self._execute_stage_with_gate(
            stage=ResearchState.DATA_GATHERING,
            executor=lambda: self._gather_data(planning_data),
            gate_number=2
        )

        # STATE 3: FACT EXTRACTION
        facts = self._execute_stage_with_gate(
            stage=ResearchState.FACT_EXTRACTION,
            executor=lambda: self._extract_facts(data),
            gate_number=3
        )

        # STATE 4: VERIFICATION
        verified_facts = self._execute_stage_with_gate(
            stage=ResearchState.VERIFICATION,
            executor=lambda: self._verify_facts(facts),
            gate_number=4
        )

        # STATE 5: ANALYSIS
        analysis = self._execute_stage_with_gate(
            stage=ResearchState.ANALYSIS,
            executor=lambda: self._analyze(verified_facts, planning_data),
            gate_number=5
        )

        # STATE 6: BRIEF GENERATION
        brief = self._execute_stage_with_gate(
            stage=ResearchState.BRIEF_GENERATION,
            executor=lambda: self._generate_brief(analysis, verified_facts),
            gate_number=6
        )

        # STATE 7: QUALITY ASSURANCE
        final_result = self._execute_stage_with_gate(
            stage=ResearchState.QUALITY_ASSURANCE,
            executor=lambda: self._final_qa(brief, analysis),
            gate_number=7
        )

        self.current_state = ResearchState.COMPLETE

        print("✅ Research complete - all quality gates passed")
        print()
        print("📊 Quality Gate Summary:")
        for gate_name, result in self.gate_results.items():
            status_icon = "✅" if result.status == QualityGateStatus.PASSED else "❌"
            print(f"   {status_icon} {gate_name}: {result.score:.0f}/100")

        return final_result

    def _execute_stage_with_gate(
        self,
        stage: ResearchState,
        executor: callable,
        gate_number: int
    ) -> Dict:
        """
        Execute a stage and validate through quality gate.
        Retry if gate fails (up to max_retries).
        """

        self.current_state = stage
        stage_name = stage.name.replace('_', ' ').title()

        print(f"{'='*60}")
        print(f"STAGE {gate_number}: {stage_name}")
        print(f"{'='*60}")

        for attempt in range(1, self.max_retries_per_gate + 1):
            print(f"\n🔄 Attempt {attempt}/{self.max_retries_per_gate}")

            # Execute stage
            print(f"   ⚙️  Executing {stage_name}...")
            stage_data = executor()

            # Validate through quality gate
            print(f"   🔍 Validating through Quality Gate {gate_number}...")
            gate_result = self.quality_agent.validate_gate(
                gate_number=gate_number,
                data=stage_data,
                stage_name=stage_name
            )

            # Store result
            self.gate_results[f"Gate {gate_number}"] = gate_result

            # Check result
            if gate_result.status == QualityGateStatus.PASSED:
                print(f"   ✅ PASSED - Score: {gate_result.score:.0f}/100")
                return stage_data

            else:
                print(f"   ❌ FAILED - Score: {gate_result.score:.0f}/100")
                print(f"   Failures:")
                for failure in gate_result.failures:
                    print(f"      • {failure}")

                if attempt < self.max_retries_per_gate:
                    print(f"   🔧 Applying corrections:")
                    for rec in gate_result.recommendations:
                        print(f"      • {rec}")
                    print()

                    # Apply corrections for next attempt
                    stage_data = self._apply_corrections(
                        stage_data,
                        gate_result.recommendations
                    )

        # Max retries exceeded
        print(f"\n❌ Gate {gate_number} failed after {self.max_retries_per_gate} attempts")
        print(f"   Final score: {gate_result.score:.0f}/100")
        print(f"   Cannot proceed to next stage")

        self.current_state = ResearchState.FAILED

        raise QualityGateFailureError(
            f"Gate {gate_number} ({stage_name}) failed quality standards after {self.max_retries_per_gate} attempts. "
            f"Final score: {gate_result.score:.0f}/100"
        )

    def _apply_corrections(
        self,
        stage_data: Dict,
        recommendations: List[str]
    ) -> Dict:
        """
        Apply corrections based on quality gate recommendations.
        This uses LLM to revise the output.
        """

        correction_prompt = f"""
You need to revise this output to meet quality standards.

Current output:
{json.dumps(stage_data, indent=2)}

Quality issues identified:
{chr(10).join(f"- {rec}" for rec in recommendations)}

Revise the output to address all issues. Maintain all existing data,
but add/improve as needed to pass quality checks.

Return revised output in same JSON format.
"""

        # Use LLM to apply corrections
        response = self.llm.generate(correction_prompt)

        revised_data = json.loads(response)
        return revised_data

    # Stage execution methods
    def _plan_research(
        self,
        company_name: str,
        research_type: str,
        focus_areas: Optional[List[str]]
    ) -> Dict:
        """Execute planning stage"""
        # Implementation...
        return {
            "company_name": company_name,
            "research_type": research_type,
            "focus_areas": focus_areas or ["general"],
            "success_metrics": {
                "minimum_sources": 10,
                "minimum_facts": 30,
                "target_quality_score": 85
            },
            "estimated_duration": "25-30 minutes"
        }

    def _gather_data(self, planning_data: Dict) -> Dict:
        """Execute data gathering stage"""
        # Implementation...
        pass

    def _extract_facts(self, data: Dict) -> Dict:
        """Execute fact extraction stage"""
        # Implementation...
        pass

    def _verify_facts(self, facts: Dict) -> Dict:
        """Execute verification stage"""
        # Implementation...
        pass

    def _analyze(self, verified_facts: Dict, planning_data: Dict) -> Dict:
        """Execute analysis stage"""
        # Implementation...
        pass

    def _generate_brief(self, analysis: Dict, verified_facts: Dict) -> Dict:
        """Execute brief generation stage"""
        # Implementation...
        pass

    def _final_qa(self, brief: Dict, analysis: Dict) -> Dict:
        """Execute final QA stage"""
        # Implementation...
        pass


class QualityGateFailureError(Exception):
    """Raised when a quality gate cannot be passed after max retries"""
    pass
```

---

## 📋 QUALITY STANDARDS CONFIGURATION

### Configurable Quality Thresholds

```yaml
# quality_standards.yaml

global:
  strict_mode: true  # Cannot bypass gates
  max_retries_per_gate: 3
  overall_quality_threshold: 85  # Minimum score to pass

gates:
  gate_1_planning:
    minimum_score: 80
    required_fields:
      - company_name
      - research_type
      - success_metrics
      - estimated_duration

  gate_2_data_gathering:
    minimum_score: 80
    thresholds:
      minimum_sources: 10
      minimum_source_types: 3
      data_freshness_ratio: 0.7  # 70% of sources < 180 days
      required_source_types:
        - company_official
        - data_provider
        - news

  gate_3_fact_extraction:
    minimum_score: 80
    thresholds:
      minimum_facts: 30
      required_categories: 5
      minimum_high_relevance: 15  # Facts with relevance ≥ 7
      required_categories_list:
        - PROFILE
        - FINANCIAL
        - STRATEGY
        - MARKETING
        - COMPETITIVE

  gate_4_verification:
    minimum_score: 80
    thresholds:
      minimum_high_confidence_ratio: 0.5  # 50% HIGH confidence
      maximum_low_confidence_ratio: 0.2  # 20% LOW confidence
      conflicts_must_be_resolved: true
      require_credibility_scores: true

  gate_5_analysis:
    minimum_score: 80
    thresholds:
      minimum_insight_ratio: 0.33  # 1 insight per 3 facts
      insights_must_be_supported: true  # 2+ facts each
      minimum_implications_ratio: 0.8  # 80% insights have implications
      minimum_patterns: 3
      minimum_cross_section_insights: 2

  gate_6_brief_generation:
    minimum_score: 80
    thresholds:
      exec_summary_min_words: 150
      exec_summary_max_words: 250
      minimum_citation_ratio: 0.7  # 70% of claims cited
      minimum_word_count: 2000
      required_sections:
        - Executive Summary
        - Strategic Situation
        - Deep Dive Analysis
        - Strategic Implications
        - Opportunities for Electric Glue
        - Recommended Approach

  gate_7_quality_assurance:
    minimum_score: 85  # Higher threshold for final gate
    sub_scores:
      citation_quality: 70
      insight_density: 70
      readability: 70
      actionability: 80
      professional_tone: 80
    weights:
      citation_quality: 0.20
      insight_density: 0.20
      readability: 0.15
      actionability: 0.25
      professional_tone: 0.20
```

---

## 🔍 MONITORING & OBSERVABILITY

### Track Quality Metrics Over Time

```python
class QualityMetricsTracker:
    """Track quality metrics across research requests"""

    def __init__(self, database):
        self.db = database

    def log_gate_result(
        self,
        research_id: str,
        gate_number: int,
        gate_name: str,
        result: QualityGateResult,
        attempt_number: int
    ):
        """Log gate validation result"""

        self.db.insert({
            "research_id": research_id,
            "gate_number": gate_number,
            "gate_name": gate_name,
            "status": result.status.value,
            "score": result.score,
            "checks": result.checks,
            "failures": result.failures,
            "attempt_number": attempt_number,
            "timestamp": datetime.now().isoformat()
        })

    def get_quality_trends(self, days: int = 30) -> Dict:
        """Get quality trends over time"""

        # Average scores by gate
        gate_scores = self.db.query(f"""
            SELECT
                gate_number,
                gate_name,
                AVG(score) as avg_score,
                MIN(score) as min_score,
                MAX(score) as max_score,
                COUNT(*) as total_attempts,
                SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passed_count
            FROM gate_results
            WHERE timestamp >= DATE('now', '-{days} days')
            GROUP BY gate_number, gate_name
            ORDER BY gate_number
        """)

        # First-pass success rate
        first_pass_rate = self.db.query(f"""
            SELECT
                gate_number,
                SUM(CASE WHEN attempt_number = 1 AND status = 'passed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as first_pass_pct
            FROM gate_results
            WHERE timestamp >= DATE('now', '-{days} days')
            GROUP BY gate_number
        """)

        # Common failure patterns
        failure_patterns = self.db.query(f"""
            SELECT
                gate_number,
                failure,
                COUNT(*) as occurrence_count
            FROM gate_results, json_each(failures)
            WHERE timestamp >= DATE('now', '-{days} days')
            GROUP BY gate_number, failure
            ORDER BY occurrence_count DESC
            LIMIT 10
        """)

        return {
            "gate_scores": gate_scores,
            "first_pass_rate": first_pass_rate,
            "failure_patterns": failure_patterns
        }

    def generate_quality_report(self) -> str:
        """Generate human-readable quality report"""

        trends = self.get_quality_trends(days=30)

        report = """
# SCOUT QUALITY REPORT - Last 30 Days

## Quality Gate Performance

| Gate | Avg Score | Pass Rate | First-Pass Rate |
|------|-----------|-----------|-----------------|
"""

        for gate in trends['gate_scores']:
            pass_rate = (gate['passed_count'] / gate['total_attempts']) * 100
            first_pass = trends['first_pass_rate'][gate['gate_number']]

            report += f"| Gate {gate['gate_number']}: {gate['gate_name']} | {gate['avg_score']:.0f}/100 | {pass_rate:.0f}% | {first_pass:.0f}% |\n"

        report += "\n## Common Failure Patterns\n\n"

        for pattern in trends['failure_patterns'][:5]:
            report += f"- **Gate {pattern['gate_number']}**: {pattern['failure']} ({pattern['occurrence_count']} times)\n"

        report += "\n## Recommendations\n\n"

        # Generate recommendations based on data
        low_performing_gates = [
            g for g in trends['gate_scores']
            if g['avg_score'] < 85
        ]

        for gate in low_performing_gates:
            report += f"- Improve **{gate['gate_name']}** (currently {gate['avg_score']:.0f}/100)\n"

        return report
```

---

## 🎯 IMPLEMENTATION CHECKLIST

### Phase 1: Core Quality System (Week 1-2)

- [ ] Implement `QualityAgent` class with all 7 gate validators
- [ ] Implement `QualityEnforcedOrchestrator` with state machine
- [ ] Create quality standards configuration file
- [ ] Build correction/revision system for failed gates
- [ ] Add comprehensive logging

### Phase 2: Integration (Week 3)

- [ ] Integrate quality gates into existing Scout agents
- [ ] Test each gate individually with mock data
- [ ] Test full workflow end-to-end
- [ ] Tune quality thresholds based on results
- [ ] Add monitoring dashboard

### Phase 3: Observability (Week 4)

- [ ] Implement `QualityMetricsTracker`
- [ ] Create quality reporting system
- [ ] Set up alerts for low-quality outputs
- [ ] Build quality trend analytics
- [ ] Document common failure patterns

### Phase 4: Optimization (Week 5-6)

- [ ] Analyze which gates fail most often
- [ ] Optimize correction prompts
- [ ] Add agent-specific quality improvements
- [ ] Implement caching for repeated validations
- [ ] Performance optimization

---

## 📊 EXPECTED OUTCOMES

### Before Quality Enforcement

| Metric | Value |
|--------|-------|
| Average quality score | 65-75/100 |
| Reports with missing citations | 40% |
| Generic recommendations | 60% |
| First-time usable output | 30% |
| Requires manual revision | 70% |

### After Quality Enforcement

| Metric | Target |
|--------|--------|
| Average quality score | 85-95/100 |
| Reports with missing citations | <5% |
| Generic recommendations | <10% |
| First-time usable output | >90% |
| Requires manual revision | <10% |

---

## 🚀 KEY BENEFITS

1. **Consistency**: Every research brief meets minimum standards
2. **Reliability**: Cannot produce low-quality output
3. **Visibility**: Clear metrics on what's passing/failing
4. **Improvement**: Data-driven optimization of quality
5. **Trust**: Team confidence in Scout's outputs
6. **Efficiency**: Less manual revision needed

---

## 📝 NOTES

- **Strict Mode**: When enabled, gates cannot be bypassed (recommended for production)
- **Dev Mode**: For testing, can set `strict_mode: false` to allow gate skipping
- **Customization**: All thresholds configurable via YAML
- **Extensibility**: Easy to add new gates or modify existing ones

---

**Document Version**: 1.0
**Last Updated**: November 14, 2025
**Status**: Implementation Ready
