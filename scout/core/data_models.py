"""
Data models for Scout Intelligence Platform
Using Pydantic for type safety and validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class QualityGateStatus(Enum):
    """Status of quality gate validation"""
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_REVISION = "needs_revision"


class ConfidenceLevel(Enum):
    """Confidence level for facts and insights"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ResearchState(Enum):
    """Current state of research workflow"""
    PLANNING = 1
    DATA_GATHERING = 2
    FACT_EXTRACTION = 3
    VERIFICATION = 4
    ANALYSIS = 5
    BRIEF_GENERATION = 6
    QUALITY_ASSURANCE = 7
    COMPLETE = 8
    FAILED = 99


class QualityGateResult(BaseModel):
    """Result from quality gate validation"""
    gate_name: str
    gate_number: int
    status: QualityGateStatus
    score: float = Field(ge=0, le=100)
    checks: Dict[str, bool]
    failures: List[str]
    recommendations: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)


class Fact(BaseModel):
    """Extracted fact from research"""
    category: str
    claim: str
    quote: Optional[str] = None
    source_name: str
    source_url: str
    date_accessed: str
    confidence: ConfidenceLevel
    confidence_rationale: str
    fact_type: str
    relevance_score: int = Field(ge=1, le=10)
    tags: List[str] = []


class VerifiedFact(BaseModel):
    """Fact that has been cross-verified"""
    claim: str
    verification_status: str  # VERIFIED, LIKELY, UNCONFIRMED, DISPUTED
    confidence_score: int = Field(ge=0, le=100)
    sources: List[str]
    source_count: int
    has_conflict: bool = False
    conflict_resolution: Optional[str] = None
    source_credibility: int = Field(ge=1, le=10)


class Source(BaseModel):
    """Source document"""
    url: str
    content: str
    source_type: str  # company_official, data_provider, news, etc.
    date: Optional[str] = None
    credibility_score: int = Field(ge=1, le=10)
    word_count: int = 0

    @validator('word_count', always=True)
    def calculate_word_count(cls, v, values):
        if v == 0 and 'content' in values:
            return len(values['content'].split())
        return v


class ResearchRequest(BaseModel):
    """Research request from user"""
    company_name: str
    research_type: str
    focus_areas: List[str] = ["general"]
    urgency: str = "standard"
    user_id: str
    request_id: str = Field(default_factory=lambda: f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    timestamp: datetime = Field(default_factory=datetime.now)


class ResearchPlan(BaseModel):
    """Plan for executing research"""
    request_id: str
    company_name: str
    research_type: str
    focus_areas: List[str]
    success_metrics: Dict[str, Any]
    estimated_duration: str
    target_sources: int = 10
    target_facts: int = 30
    quality_threshold: int = 85


class ResearchBrief(BaseModel):
    """Final research output"""
    request_id: str
    company_name: str
    brief_text: str
    executive_summary: str
    sections: Dict[str, str]
    sources: List[str]
    total_sources: int
    verified_facts_count: int
    research_duration_minutes: float
    quality_score: float
    timestamp: datetime = Field(default_factory=datetime.now)
    confidence_distribution: Dict[str, int] = {}


class QualityMetrics(BaseModel):
    """Quality metrics for a research brief"""
    citation_score: float = Field(ge=0, le=100)
    insight_score: float = Field(ge=0, le=100)
    readability_score: float = Field(ge=0, le=100)
    actionability_score: float = Field(ge=0, le=100)
    professional_score: float = Field(ge=0, le=100)
    overall_score: float = Field(ge=0, le=100)
