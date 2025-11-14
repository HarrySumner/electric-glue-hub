# SCOUT ASSISTANT IMPLEMENTATION GUIDE
## Building High-Quality Intelligence Output

---

## 📚 TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Agent Implementation Details](#agent-implementation-details)
3. [Prompt Engineering Best Practices](#prompt-engineering-best-practices)
4. [Output Quality Framework](#output-quality-framework)
5. [Data Source Integration](#data-source-integration)
6. [Quality Assurance System](#quality-assurance-system)
7. [Example Implementations](#example-implementations)
8. [Testing & Validation](#testing--validation)

---

## 🎯 SYSTEM OVERVIEW

### The Scout Architecture

Scout is a multi-agent intelligence system that transforms raw web data into strategic business intelligence. The key to high-quality output is not just what data you gather, but **how you synthesize it**.

```
┌─────────────────────────────────────────────────────────┐
│           ORCHESTRATOR AGENT                             │
│   • Manages workflow                                    │
│   • Routes tasks to specialist agents                   │
│   • Synthesizes final output                            │
│   • Ensures quality standards                           │
└─────────────────────────────────────────────────────────┘
                        ↓
    ┌───────────────────┼───────────────────┐
    ↓                   ↓                   ↓
┌─────────┐      ┌─────────┐      ┌─────────┐
│ COMPANY │      │COMPET-  │      │ MARKET  │
│RESEARCH │      │ ITIVE   │      │ TRENDS  │
│  AGENT  │      │ AGENT   │      │ AGENT   │
└─────────┘      └─────────┘      └─────────┘
    ↓                   ↓                   ↓
┌─────────────────────────────────────────────────────────┐
│         FACT EXTRACTION & VERIFICATION                   │
│   • Structured data extraction                          │
│   • Cross-source verification                           │
│   • Confidence scoring                                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│           STRATEGIC SYNTHESIS                            │
│   • Pattern recognition                                 │
│   • Insight generation                                  │
│   • Professional writing                                │
│   • Quality control                                     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│        FORMATTED INTELLIGENCE BRIEF                      │
│   • Executive summary                                   │
│   • Deep analysis                                       │
│   • Strategic recommendations                           │
│   • Source documentation                                │
└─────────────────────────────────────────────────────────┘
```

### Core Principle: Intelligence vs. Information

**Information**: "Glossier has 4.5M Instagram followers"

**Intelligence**: "Glossier maintains 3.2% engagement despite 4.5M followers—78% above industry average of 1.8%. This suggests community-driven content strategy still resonating, but Meta algorithm changes toward video content threaten Instagram-centric approach (65% of social presence). Competitors diversifying to TikTok faster: Fenty 40% TikTok vs. Glossier 25%."

The difference:
- Context (industry benchmarks)
- Analysis (what it means)
- Synthesis (connections to other findings)
- Implications (risks and opportunities)

---

## 🤖 AGENT IMPLEMENTATION DETAILS

### Agent 1: Company Research Agent

#### Purpose
Deep-dive into target company's business model, strategy, and market position

#### Implementation Structure

```python
from typing import Dict, List
from dataclasses import dataclass
import anthropic

@dataclass
class CompanyProfile:
    name: str
    industry: str
    founded: int
    hq_location: str
    employee_count: int
    funding_total: float
    valuation: float
    revenue_estimate: float
    confidence_scores: Dict[str, str]

@dataclass
class BusinessIntelligence:
    profile: CompanyProfile
    business_model: Dict
    marketing_strategy: Dict
    financial_health: Dict
    strategic_priorities: List[str]
    sources: List[Dict]

class CompanyResearchAgent:
    def __init__(self, anthropic_api_key: str):
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.system_prompt = self._load_system_prompt()

    def research_company(
        self,
        company_name: str,
        focus_areas: List[str] = None
    ) -> BusinessIntelligence:
        """Main entry point for company research"""

        # Stage 1: Data gathering
        raw_data = self._gather_data(company_name)

        # Stage 2: Fact extraction
        facts = self._extract_facts(raw_data)

        # Stage 3: Verification
        verified_facts = self._verify_facts(facts)

        # Stage 4: Analysis
        intelligence = self._analyze_company(verified_facts, focus_areas)

        # Stage 5: Quality check
        self._quality_check(intelligence)

        return intelligence

    def _gather_data(self, company_name: str) -> Dict:
        """Gather data from multiple sources"""
        sources = {}

        # Crunchbase data
        sources['crunchbase'] = self._query_crunchbase(company_name)

        # LinkedIn data
        sources['linkedin'] = self._query_linkedin(company_name)

        # Company website
        sources['website'] = self._scrape_website(company_name)

        # News & press
        sources['news'] = self._search_news(company_name)

        # Web search for additional context
        sources['web'] = self._web_search(company_name)

        return sources

    def _extract_facts(self, raw_data: Dict) -> List[Dict]:
        """Extract structured facts from raw data using LLM"""

        # Use enhanced fact extraction prompt
        extraction_prompt = """
        You are extracting structured intelligence from raw sources.

        For each fact you extract, provide:
        1. Category (PROFILE, FINANCIAL, STRATEGY, MARKETING, etc.)
        2. Claim (the factual statement)
        3. Quote (exact text from source if available)
        4. Source (which data source this came from)
        5. Confidence (HIGH/MEDIUM/LOW with rationale)
        6. Relevance (1-10 score)

        Extract all verifiable facts. Do not infer or generate.

        Raw data:
        {raw_data}

        Output as JSON array of fact objects.
        """

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=self._load_extraction_prompt(),
            messages=[{
                "role": "user",
                "content": extraction_prompt.format(
                    raw_data=json.dumps(raw_data, indent=2)
                )
            }]
        )

        facts = json.loads(response.content[0].text)
        return facts

    def _verify_facts(self, facts: List[Dict]) -> List[Dict]:
        """Cross-reference and verify facts"""

        verification_prompt = """
        Cross-reference these extracted facts.

        For each fact:
        1. Check if multiple sources confirm it
        2. Identify any conflicts between sources
        3. Calculate confidence score (0-100)
        4. Mark as VERIFIED, LIKELY, or UNCONFIRMED

        Facts to verify:
        {facts}

        Return verified fact database with confidence scores.
        """

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=self._load_verification_prompt(),
            messages=[{
                "role": "user",
                "content": verification_prompt.format(
                    facts=json.dumps(facts, indent=2)
                )
            }]
        )

        verified = json.loads(response.content[0].text)
        return verified

    def _analyze_company(
        self,
        verified_facts: List[Dict],
        focus_areas: List[str]
    ) -> BusinessIntelligence:
        """Analyze verified facts to generate intelligence"""

        analysis_prompt = """
        You are a senior business analyst generating strategic intelligence.

        Using these verified facts, create comprehensive company analysis:

        {verified_facts}

        Focus areas: {focus_areas}

        Generate:
        1. Company profile (structured data)
        2. Business model analysis (how they make money, defensibility)
        3. Marketing strategy analysis (channels, messaging, performance)
        4. Financial health assessment (funding, runway, growth)
        5. Strategic priorities (what they're focused on next 12 months)
        6. Key insights (non-obvious patterns and implications)

        Write for C-suite audience. Be specific, cite sources, provide confidence levels.
        """

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            system=self._load_analysis_prompt(),
            messages=[{
                "role": "user",
                "content": analysis_prompt.format(
                    verified_facts=json.dumps(verified_facts, indent=2),
                    focus_areas=", ".join(focus_areas or ["general"])
                )
            }]
        )

        # Parse response into BusinessIntelligence object
        intelligence = self._parse_intelligence(response.content[0].text)
        return intelligence

    def _quality_check(self, intelligence: BusinessIntelligence) -> bool:
        """Verify output meets quality standards"""

        checks = {
            "has_sources": len(intelligence.sources) >= 10,
            "has_citations": self._count_citations(intelligence) >= 15,
            "has_confidence_levels": self._has_confidence_scores(intelligence),
            "profile_complete": all([
                intelligence.profile.name,
                intelligence.profile.employee_count,
                intelligence.profile.funding_total
            ]),
            "insights_present": len(intelligence.strategic_priorities) >= 3
        }

        if not all(checks.values()):
            failed = [k for k, v in checks.items() if not v]
            raise QualityCheckError(f"Quality checks failed: {failed}")

        return True
```

#### Key Implementation Points

1. **Multi-Stage Processing**: Don't try to do everything in one LLM call
   - Stage 1: Data gathering (APIs + web scraping)
   - Stage 2: Fact extraction (LLM with extraction prompt)
   - Stage 3: Verification (LLM with verification prompt)
   - Stage 4: Analysis (LLM with analysis prompt)
   - Stage 5: Quality control (programmatic checks + LLM review)

2. **Structured Data Flow**: Use dataclasses/Pydantic models for type safety

3. **Source Diversity**: Minimum 10 unique sources per company research

4. **Confidence Scoring**: Every fact needs confidence level

---

### Agent 2: Competitive Analysis Agent

#### Purpose
Map competitive landscape, positioning, and share of voice

#### Key Implementation Considerations

```python
class CompetitiveAnalysisAgent:
    def analyze_competitive_landscape(
        self,
        primary_company: str,
        industry: str,
        geographic_scope: str = "US"
    ) -> CompetitiveLandscape:
        """Generate comprehensive competitive analysis"""

        # Step 1: Identify competitive set
        competitors = self._identify_competitors(primary_company, industry)

        # Step 2: Gather data on each competitor
        competitor_data = {}
        for competitor in competitors:
            competitor_data[competitor] = self._gather_competitor_data(competitor)

        # Step 3: Calculate share of voice
        sov = self._calculate_share_of_voice(primary_company, competitors)

        # Step 4: Positioning analysis
        positioning = self._analyze_positioning(primary_company, competitor_data)

        # Step 5: Synthesize insights
        analysis = self._synthesize_competitive_intelligence(
            primary_company,
            competitors,
            sov,
            positioning,
            competitor_data
        )

        return analysis

    def _calculate_share_of_voice(
        self,
        primary: str,
        competitors: List[str]
    ) -> Dict:
        """Calculate SOV across channels"""

        sov = {
            "organic_search": self._organic_sov(primary, competitors),
            "paid_search": self._paid_sov(primary, competitors),
            "social_media": self._social_sov(primary, competitors),
            "pr_media": self._pr_sov(primary, competitors)
        }

        # Calculate weighted overall SOV
        weights = {
            "organic_search": 0.3,
            "paid_search": 0.2,
            "social_media": 0.3,
            "pr_media": 0.2
        }

        for company in [primary] + competitors:
            overall = sum(
                sov[channel].get(company, 0) * weight
                for channel, weight in weights.items()
            )
            sov["overall"][company] = overall

        return sov
```

#### Share of Voice Calculation Methods

**Organic Search SOV**:
```python
def _organic_sov(self, primary: str, competitors: List[str]) -> Dict[str, float]:
    """Calculate organic search share of voice using SEMrush data"""

    # Get top 100 keywords for category
    category_keywords = self._get_category_keywords(primary)

    # For each competitor, count ranking positions
    rankings = {}
    for company in [primary] + competitors:
        company_ranks = self._get_keyword_rankings(company, category_keywords)

        # Weight by keyword volume and position
        score = sum(
            keyword_volume / (position ** 1.5)  # Position decay
            for keyword, (position, keyword_volume) in company_ranks.items()
        )
        rankings[company] = score

    # Convert to percentages
    total = sum(rankings.values())
    sov = {company: (score / total) * 100 for company, score in rankings.items()}

    return sov
```

**Social Media SOV**:
```python
def _social_sov(self, primary: str, competitors: List[str]) -> Dict[str, float]:
    """Calculate social media share of voice"""

    scores = {}
    for company in [primary] + competitors:
        instagram = self._get_instagram_data(company)
        tiktok = self._get_tiktok_data(company)
        twitter = self._get_twitter_data(company)

        # Weighted scoring: followers + engagement
        score = (
            instagram['followers'] * (instagram['engagement_rate'] / 100) * 0.5 +
            tiktok['followers'] * (tiktok['engagement_rate'] / 100) * 0.3 +
            twitter['followers'] * (twitter['engagement_rate'] / 100) * 0.2
        )
        scores[company] = score

    # Convert to percentages
    total = sum(scores.values())
    sov = {company: (score / total) * 100 for company, score in scores.items()}

    return sov
```

---

### Agent 3: Market Trends Agent

#### Purpose
Identify emerging trends and forecast market direction

#### Implementation Pattern

```python
class MarketTrendsAgent:
    def analyze_market_trends(
        self,
        industry: str,
        time_horizon: str = "12_months",
        geographic_focus: str = "US"
    ) -> TrendAnalysis:
        """Analyze market trends and forecast direction"""

        # Step 1: Trend discovery
        emerging_trends = self._discover_trends(industry)

        # Step 2: Validate signals (multiple sources)
        validated_trends = self._validate_trend_signals(emerging_trends)

        # Step 3: Impact analysis
        trend_impacts = self._analyze_trend_impacts(validated_trends, industry)

        # Step 4: Forecast
        forecast = self._generate_forecast(trend_impacts, time_horizon)

        # Step 5: Strategic implications
        implications = self._synthesize_implications(forecast, industry)

        return TrendAnalysis(
            trends=validated_trends,
            impacts=trend_impacts,
            forecast=forecast,
            implications=implications
        )

    def _discover_trends(self, industry: str) -> List[Dict]:
        """Discover emerging trends from multiple signals"""

        signals = []

        # Google Trends: Rising searches
        google_trends = self._query_google_trends(industry)
        signals.extend(self._parse_google_trends(google_trends))

        # News mentions: Topic clustering
        news = self._search_industry_news(industry, days=180)
        signals.extend(self._extract_topics(news))

        # Reddit/Social: Conversation analysis
        social_convos = self._analyze_social_conversations(industry)
        signals.extend(social_convos)

        # Startup funding: Where VCs investing
        startup_funding = self._query_crunchbase_category(industry)
        signals.extend(self._extract_funding_trends(startup_funding))

        # Cluster signals into trend themes
        trend_clusters = self._cluster_signals(signals)

        return trend_clusters

    def _validate_trend_signals(self, trends: List[Dict]) -> List[Dict]:
        """Validate trends across multiple sources"""

        validated = []
        for trend in trends:
            # Check: Is this appearing in multiple independent sources?
            source_diversity = self._count_unique_sources(trend)

            # Check: Is search volume actually increasing?
            search_growth = self._verify_search_growth(trend['keywords'])

            # Check: Are credible outlets covering this?
            media_coverage = self._check_media_coverage(trend['theme'])

            # Calculate signal strength
            signal_strength = (
                source_diversity * 0.3 +
                search_growth * 0.4 +
                media_coverage * 0.3
            )

            if signal_strength >= 0.5:  # 50% threshold
                trend['signal_strength'] = signal_strength
                trend['validation_status'] = 'VALIDATED'
                validated.append(trend)

        return validated
```

---

## 📝 PROMPT ENGINEERING BEST PRACTICES

### Principle 1: Persona-Driven Prompts

**Bad Prompt**:
```
Analyze this company and tell me about their marketing.
```

**Good Prompt**:
```
You are a senior investment analyst at Sequoia Capital conducting due diligence
on a $10M Series A investment.

Your managing partner needs to understand:
- Is this a viable business with defensible moat?
- What's the growth trajectory?
- What are the risk factors?

Analyze [Company]'s business model and marketing strategy with the skepticism
and rigor of an investor who will be held accountable for this decision.

Write for an audience of: Limited Partners reviewing this deal.
```

**Why it's better**:
- Clear role and perspective
- Specific stakeholder needs
- Defined audience
- Sets expectation for tone and depth

---

### Principle 2: Structure Over Freedom

**Bad Prompt**:
```
Extract facts from these sources.
```

**Good Prompt**:
```
Extract facts from sources using this structure:

For EACH fact, provide:
1. Category: [PROFILE|FINANCIAL|STRATEGY|MARKETING|COMPETITIVE|PERFORMANCE|LEADERSHIP|TRENDS|OPPORTUNITY]
2. Claim: [One-sentence factual statement]
3. Quote: [Exact text from source, if available]
4. Source: [Source name and URL]
5. Date: [When accessed or published]
6. Confidence: [HIGH|MEDIUM|LOW]
7. Confidence Rationale: [Why this confidence level?]
8. Relevance: [1-10 score for research question]
9. Tags: [Relevant tags for filtering]

Example:
{
  "category": "MARKETING",
  "claim": "Glossier's Instagram has 4.5M followers with 3.2% engagement",
  "quote": "4.5M followers, engagement rate: 3.2%",
  "source": "Instagram.com/glossier",
  "date": "2025-11-03",
  "confidence": "HIGH",
  "confidence_rationale": "Direct observation from platform",
  "relevance": 8,
  "tags": ["social_media", "engagement", "instagram"]
}

Now extract all facts using this format.
```

**Why it's better**:
- Exact structure specified
- Example provided
- Output format clear
- Reduces ambiguity

---

### Principle 3: Multi-Turn Refinement

Instead of one massive prompt, use conversational refinement:

```python
# Turn 1: Initial extraction
response_1 = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{
        "role": "user",
        "content": "Extract facts from these sources: {sources}"
    }]
)

# Turn 2: Ask for confidence levels
response_2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[
        {"role": "user", "content": "Extract facts..."},
        {"role": "assistant", "content": response_1.content[0].text},
        {"role": "user", "content": """
            For each fact you extracted, assign confidence level:
            HIGH: Multiple sources confirm, or authoritative single source
            MEDIUM: Credible single source, or inferred from strong data
            LOW: Weak source, outdated, or speculative

            Also flag any conflicts between sources.
        """}
    ]
)

# Turn 3: Request synthesis
response_3 = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[
        # ... previous messages ...
        {"role": "user", "content": """
            Now synthesize these facts into strategic insights.
            For each major theme, provide:
            1. What the data says (facts)
            2. What it means (analysis)
            3. Why it matters (implications)
        """}
    ]
)
```

---

### Principle 4: Quality Checks in Prompts

Embed quality expectations directly in prompts:

```markdown
Before finalizing your analysis, self-check:

✅ Every quantitative claim has a cited source
✅ Confidence levels assigned and justified
✅ No repetition of information
✅ Insights are specific, not generic ("they should improve marketing" is not acceptable)
✅ Recommendations are actionable within 30 days
✅ Professional tone maintained throughout

If any check fails, revise that section before delivering.
```

---

## 🎨 OUTPUT QUALITY FRAMEWORK

### The Three Layers of Quality

```
┌─────────────────────────────────────────┐
│  LAYER 1: CONTENT QUALITY                │
│  • Factual accuracy                     │
│  • Source credibility                   │
│  • Insight depth                        │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  LAYER 2: STRUCTURAL QUALITY             │
│  • Logical flow                         │
│  • Clear narrative                      │
│  • Proper formatting                    │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  LAYER 3: STRATEGIC QUALITY              │
│  • Actionable recommendations           │
│  • Pitch-ready insights                 │
│  • Competitive differentiation          │
└─────────────────────────────────────────┘
```

### Quality Metrics

Implement programmatic quality scoring:

```python
class QualityScorer:
    def score_brief(self, brief: str) -> QualityScore:
        """Score research brief across multiple dimensions"""

        scores = {
            "citation_density": self._score_citations(brief),
            "insight_ratio": self._score_insights(brief),
            "readability": self._score_readability(brief),
            "structure": self._score_structure(brief),
            "actionability": self._score_actionability(brief),
            "professional_tone": self._score_tone(brief)
        }

        overall = sum(scores.values()) / len(scores)

        return QualityScore(
            overall=overall,
            dimensions=scores,
            recommendations=self._generate_improvements(scores)
        )

    def _score_citations(self, brief: str) -> float:
        """Score citation quality (0-100)"""

        # Count citations
        citation_pattern = r'\[Source:.*?\]'
        citations = re.findall(citation_pattern, brief)

        # Count factual claims (numbers, specific statements)
        claim_pattern = r'\d+[%KMB]|\$\d+'
        claims = re.findall(claim_pattern, brief)

        # Calculate ratio
        if len(claims) == 0:
            return 50  # No claims to cite

        citation_ratio = len(citations) / len(claims)

        # Score: 100% if all claims cited, scale down from there
        score = min(100, citation_ratio * 100)

        return score

    def _score_insights(self, brief: str) -> float:
        """Score insight density (0-100)"""

        # Use LLM to identify insights vs. facts
        analysis_prompt = """
        Analyze this research brief and categorize each statement as:
        - FACT: Raw information (e.g., "Company has 200 employees")
        - INSIGHT: Analysis or implication (e.g., "40% headcount growth signals aggressive expansion")

        Count:
        - Total facts: X
        - Total insights: Y

        Return: {facts: X, insights: Y}

        Brief: {brief}
        """

        response = self.llm.generate(analysis_prompt.format(brief=brief))
        counts = json.loads(response)

        # Target: 1 insight per 3 facts minimum
        insight_ratio = counts['insights'] / max(counts['facts'], 1)
        target_ratio = 0.33

        score = min(100, (insight_ratio / target_ratio) * 100)

        return score

    def _score_actionability(self, brief: str) -> float:
        """Score how actionable recommendations are (0-100)"""

        # Extract recommendations section
        rec_section = self._extract_section(brief, "Opportunities")

        # Check for actionability signals
        actionability_markers = [
            r'specific.*\d+',  # Specific numbers
            r'(within|by|before) \d+ (days|weeks|months)',  # Timeframes
            r'(partner with|launch|create|build|implement)',  # Action verbs
            r'estimated.*\$',  # Value estimates
        ]

        signals_found = sum(
            len(re.findall(pattern, rec_section, re.IGNORECASE))
            for pattern in actionability_markers
        )

        # Score based on density
        words = len(rec_section.split())
        density = signals_found / (words / 100)  # Per 100 words

        score = min(100, density * 20)  # 5 signals per 100 words = 100 score

        return score
```

---

## 🔗 DATA SOURCE INTEGRATION

### API Integration Patterns

#### Pattern 1: Graceful Degradation

```python
class DataGatherer:
    def gather_company_data(self, company_name: str) -> Dict:
        """Gather from multiple sources with fallbacks"""

        data = {}

        # Try primary sources
        try:
            data['crunchbase'] = self.crunchbase_api.get_company(company_name)
        except APIError as e:
            logger.warning(f"Crunchbase failed: {e}, trying fallback")
            data['crunchbase'] = self._scrape_crunchbase(company_name)
        except Exception as e:
            logger.error(f"Crunchbase completely failed: {e}")
            data['crunchbase'] = None

        # Always continue even if one source fails
        try:
            data['linkedin'] = self.linkedin_api.get_company(company_name)
        except Exception as e:
            logger.error(f"LinkedIn failed: {e}")
            data['linkedin'] = None

        # ... more sources ...

        # Validate we got minimum required data
        if not self._has_minimum_data(data):
            raise InsufficientDataError(
                f"Could not gather enough data for {company_name}"
            )

        return data
```

#### Pattern 2: Caching for Cost Efficiency

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedAPIClient:
    def __init__(self, api_client, cache_duration_hours=24):
        self.client = api_client
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache = {}

    def get_company_data(self, company_name: str) -> Dict:
        """Get company data with caching"""

        cache_key = f"company:{company_name}"

        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                logger.info(f"Cache hit for {company_name}")
                return cached_data

        # Cache miss, fetch from API
        logger.info(f"Cache miss, fetching {company_name}")
        data = self.client.get_company(company_name)

        # Store in cache
        self.cache[cache_key] = (data, datetime.now())

        return data
```

#### Pattern 3: Rate Limiting

```python
import time
from collections import deque

class RateLimitedAPI:
    def __init__(self, api_client, requests_per_minute=60):
        self.client = api_client
        self.rpm = requests_per_minute
        self.request_times = deque(maxlen=requests_per_minute)

    def make_request(self, *args, **kwargs):
        """Make API request with rate limiting"""

        # Check if we're at limit
        if len(self.request_times) >= self.rpm:
            # Calculate time to wait
            oldest_request = self.request_times[0]
            time_since_oldest = time.time() - oldest_request

            if time_since_oldest < 60:
                wait_time = 60 - time_since_oldest
                logger.info(f"Rate limit reached, waiting {wait_time:.1f}s")
                time.sleep(wait_time)

        # Make request
        self.request_times.append(time.time())
        return self.client.request(*args, **kwargs)
```

---

## ✅ QUALITY ASSURANCE SYSTEM

### Automated Quality Checks

```python
class QualityAssurance:
    def __init__(self):
        self.checks = [
            self.check_executive_summary,
            self.check_citations,
            self.check_structure,
            self.check_insight_density,
            self.check_actionability,
            self.check_formatting,
            self.check_professional_tone
        ]

    def run_qa(self, brief: str) -> QAReport:
        """Run all quality checks on brief"""

        results = {}
        for check in self.checks:
            try:
                results[check.__name__] = check(brief)
            except Exception as e:
                logger.error(f"QA check {check.__name__} failed: {e}")
                results[check.__name__] = QAResult(
                    passed=False,
                    score=0,
                    message=str(e)
                )

        # Calculate overall score
        overall_score = sum(r.score for r in results.values()) / len(results)

        # Determine pass/fail
        passed = overall_score >= 80  # 80% threshold

        return QAReport(
            passed=passed,
            overall_score=overall_score,
            check_results=results,
            recommendations=self._generate_recommendations(results)
        )

    def check_executive_summary(self, brief: str) -> QAResult:
        """Verify executive summary quality"""

        # Extract exec summary
        summary = self._extract_section(brief, "Executive Summary")

        checks = {
            "length": 150 <= len(summary.split()) <= 250,
            "has_bluf": "BOTTOM LINE" in summary or "KEY FINDING" in summary,
            "has_situation": any(word in summary.lower() for word in ["founded", "company", "business"]),
            "has_challenge": any(word in summary.lower() for word in ["challenge", "tension", "facing", "opportunity"]),
            "has_implication": "Electric Glue" in summary
        }

        score = (sum(checks.values()) / len(checks)) * 100
        passed = score >= 80

        failed_checks = [k for k, v in checks.items() if not v]
        message = f"Passed: {passed}. Failed checks: {failed_checks}" if failed_checks else "All checks passed"

        return QAResult(passed=passed, score=score, message=message)

    def check_citations(self, brief: str) -> QAResult:
        """Verify adequate citation of sources"""

        # Count claims vs citations
        citations = len(re.findall(r'\[Source:.*?\]', brief))

        # Count quantitative claims
        numbers = len(re.findall(r'\d+[%KMB$]', brief))

        # Calculate ratio
        if numbers == 0:
            return QAResult(passed=True, score=100, message="No claims to cite")

        ratio = citations / numbers
        score = min(100, ratio * 100)
        passed = score >= 70  # 70% of claims should be cited

        message = f"{citations} citations for {numbers} claims ({ratio:.1%})"

        return QAResult(passed=passed, score=score, message=message)
```

### Human-in-the-Loop Review

For first X briefs, implement human review:

```python
class HumanReviewQueue:
    def __init__(self, slack_webhook_url: str):
        self.webhook = slack_webhook_url
        self.review_threshold = 50  # First 50 briefs need review
        self.briefs_generated = 0

    def submit_for_review(
        self,
        brief: str,
        metadata: Dict
    ) -> ReviewStatus:
        """Submit brief for human review"""

        self.briefs_generated += 1

        # First N briefs always get reviewed
        if self.briefs_generated <= self.review_threshold:
            needs_review = True
            reason = "First N briefs policy"
        # After that, review based on quality score
        elif metadata['quality_score'] < 85:
            needs_review = True
            reason = f"Quality score below threshold ({metadata['quality_score']})"
        else:
            needs_review = False
            reason = "Passed automated QA"

        if needs_review:
            # Send to Slack for review
            self._send_slack_notification(brief, metadata, reason)

            # Mark as pending review
            status = ReviewStatus.PENDING
        else:
            # Auto-approve
            status = ReviewStatus.APPROVED

        return status
```

---

## 🧪 TESTING & VALIDATION

### Unit Tests for Agents

```python
import pytest
from scout.agents import CompanyResearchAgent

class TestCompanyResearchAgent:
    @pytest.fixture
    def agent(self):
        return CompanyResearchAgent(api_key="test-key")

    def test_data_gathering_multiple_sources(self, agent):
        """Verify agent gathers from multiple sources"""

        data = agent._gather_data("Glossier")

        assert 'crunchbase' in data
        assert 'linkedin' in data
        assert 'website' in data
        assert 'news' in data

        # Verify data has content
        assert len(data['crunchbase']) > 0

    def test_fact_extraction_structure(self, agent):
        """Verify facts extracted with proper structure"""

        raw_data = {"test": "data"}
        facts = agent._extract_facts(raw_data)

        # Verify each fact has required fields
        required_fields = ['category', 'claim', 'source', 'confidence']
        for fact in facts:
            for field in required_fields:
                assert field in fact

    def test_confidence_scoring(self, agent):
        """Verify confidence scores are valid"""

        facts = [
            {"claim": "Test", "sources": ["A", "B"], "date": "2025-11-01"},
            {"claim": "Test2", "sources": ["A"], "date": "2025-11-01"}
        ]

        verified = agent._verify_facts(facts)

        for fact in verified:
            assert 'confidence_score' in fact
            assert 0 <= fact['confidence_score'] <= 100

    def test_minimum_source_requirement(self, agent):
        """Verify minimum sources enforced"""

        # This should fail quality check
        with pytest.raises(QualityCheckError):
            agent._quality_check(
                BusinessIntelligence(
                    sources=[{"url": "only-one-source"}],
                    # ... other fields ...
                )
            )
```

### Integration Tests

```python
class TestFullResearchWorkflow:
    def test_end_to_end_company_research(self):
        """Test full research workflow"""

        orchestrator = ResearchOrchestrator()

        result = orchestrator.research_company(
            company_name="Glossier",
            research_type="pitch_prep"
        )

        # Verify output structure
        assert result['executive_summary']
        assert result['deep_analysis']
        assert result['opportunities']
        assert result['sources']

        # Verify quality metrics
        assert result['quality_score'] >= 80
        assert len(result['sources']) >= 15
        assert result['execution_time_minutes'] <= 30

    def test_error_handling_invalid_company(self):
        """Test error handling for invalid input"""

        orchestrator = ResearchOrchestrator()

        with pytest.raises(InvalidCompanyError):
            orchestrator.research_company(
                company_name="XYZ123NOTREAL",
                research_type="pitch_prep"
            )
```

### Validation Dataset

Create validation set of "known good" outputs:

```python
VALIDATION_SET = [
    {
        "company": "Glossier",
        "expected_facts": [
            {"claim": "Founded 2014", "confidence": "HIGH"},
            {"claim": "Series E $80M", "confidence": "HIGH"},
            {"claim": "Valuation $1.8B", "confidence": "HIGH"}
        ],
        "expected_competitors": ["Fenty", "Rare Beauty", "Milk Makeup"],
        "minimum_sources": 20,
        "minimum_quality_score": 90
    },
    # ... more validation cases ...
]

def validate_against_known_good(brief: str, expected: Dict) -> ValidationResult:
    """Validate brief against known-good data"""

    results = {}

    # Check expected facts are present
    for expected_fact in expected['expected_facts']:
        present = expected_fact['claim'] in brief
        results[f"fact_{expected_fact['claim']}"] = present

    # Check competitors mentioned
    for competitor in expected['expected_competitors']:
        mentioned = competitor in brief
        results[f"competitor_{competitor}"] = mentioned

    # Check quality thresholds
    quality_score = calculate_quality_score(brief)
    results['quality_score'] = quality_score >= expected['minimum_quality_score']

    passed = all(results.values())

    return ValidationResult(passed=passed, checks=results)
```

---

## 📊 EXAMPLE IMPLEMENTATIONS

### Complete Mini-Example: Fact Extraction

```python
import anthropic
import json

def extract_facts_from_sources(sources: Dict[str, str], company_name: str) -> List[Dict]:
    """
    Extract structured facts from multiple sources

    Args:
        sources: Dict of {source_name: source_content}
        company_name: Company being researched

    Returns:
        List of structured facts
    """

    client = anthropic.Anthropic(api_key="your-key")

    # Enhanced extraction prompt
    extraction_prompt = f"""
You are extracting intelligence from raw sources about {company_name}.

For EACH distinct fact you find, create a structured fact object:

{{
  "category": "PROFILE|FINANCIAL|STRATEGY|MARKETING|COMPETITIVE|PERFORMANCE",
  "claim": "One-sentence factual statement",
  "quote": "Exact quote from source (if applicable)",
  "source_name": "Which source this came from",
  "date": "Publication or access date",
  "confidence": "HIGH|MEDIUM|LOW",
  "confidence_rationale": "Why this confidence level",
  "relevance": 1-10,
  "tags": ["tag1", "tag2"]
}}

RULES:
1. Extract ONLY explicitly stated facts, no inference
2. For numbers, include units (employees, $M, %, etc.)
3. Distinguish between official statements and estimates
4. Flag any inconsistencies between sources

Sources:
{json.dumps(sources, indent=2)}

Return as JSON array of fact objects.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        temperature=0,  # Low temperature for factual extraction
        messages=[{
            "role": "user",
            "content": extraction_prompt
        }]
    )

    # Parse response
    facts_text = response.content[0].text

    # Extract JSON from response (handle markdown code blocks)
    if "```json" in facts_text:
        facts_text = facts_text.split("```json")[1].split("```")[0]
    elif "```" in facts_text:
        facts_text = facts_text.split("```")[1].split("```")[0]

    facts = json.loads(facts_text.strip())

    return facts

# Example usage
sources = {
    "crunchbase": "Glossier raised $80M Series E in July 2022...",
    "linkedin": "Glossier • 200 employees • Beauty & Personal Care...",
    "techcrunch": "Glossier, the beauty startup valued at $1.8B..."
}

facts = extract_facts_from_sources(sources, "Glossier")

for fact in facts:
    print(f"[{fact['category']}] {fact['claim']}")
    print(f"  Confidence: {fact['confidence']} - {fact['confidence_rationale']}")
    print(f"  Source: {fact['source_name']}")
    print()
```

---

## 🎓 KEY TAKEAWAYS

### What Makes Scout Output High-Quality

1. **Multi-Stage Processing**: Don't try to do everything in one prompt
2. **Structured Data Flow**: Type-safe intermediate representations
3. **Confidence Scoring**: Always indicate certainty level
4. **Cross-Source Verification**: Never trust single source
5. **Synthesis Over Summarization**: Extract insights, not just facts
6. **Professional Writing Standards**: C-suite ready output
7. **Quality Control**: Automated checks + human review
8. **Iterative Refinement**: Multiple passes improve quality

### Common Pitfalls to Avoid

❌ **One-shot generation**: Trying to generate perfect brief in single LLM call
✅ **Multi-stage pipeline**: Gather → Extract → Verify → Analyze → Synthesize

❌ **No confidence indicators**: Presenting all facts as equally certain
✅ **Explicit confidence**: Every claim has HIGH/MEDIUM/LOW confidence

❌ **Information dump**: Listing facts without analysis
✅ **Intelligence synthesis**: Facts → Insights → Implications

❌ **Generic recommendations**: "Improve marketing", "Expand product line"
✅ **Specific opportunities**: "Build retail-to-digital attribution system to prove Sephora campaign ROI"

❌ **Poor formatting**: Wall of text
✅ **Strategic formatting**: Scannable with headers, tables, emphasis

---

## 📚 ADDITIONAL RESOURCES

### Recommended Reading
- *Competitive Intelligence* by Craig Fleisher
- *Good Strategy Bad Strategy* by Richard Rumelt (for synthesis principles)
- *The Pyramid Principle* by Barbara Minto (for structured writing)

### Tools & Libraries
- **LangGraph**: Agent orchestration
- **Anthropic Claude**: LLM for intelligence generation
- **Pydantic**: Type-safe data models
- **pytest**: Testing framework

### APIs Mentioned
- Crunchbase API
- LinkedIn API (via RapidAPI)
- SEMrush API
- Ahrefs API
- Google Trends API
- SerpAPI

---

**Document Version**: 1.0
**Last Updated**: November 14, 2025
**Maintained By**: Electric Glue Engineering Team
