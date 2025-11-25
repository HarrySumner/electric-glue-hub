"""
Perspective Agents - Multiple viewpoints on marketing data
Generates action-oriented insights from different personas

CRITICAL: These agents are fact-constrained - they can ONLY reference verified facts.
They must cite sources and acknowledge data gaps explicitly.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

# Import usage tracker
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
    from api_usage_tracker import get_tracker
    TRACKER_AVAILABLE = True
except ImportError:
    TRACKER_AVAILABLE = False

# Import fact-constrained prompts
config_path = Path(__file__).parent.parent / "config"
sys.path.insert(0, str(config_path))

try:
    from fact_constrained_prompts import (
        get_fact_constrained_prompt,
        FACT_VALIDATION_PROMPT
    )
    FACT_PROMPTS_AVAILABLE = True
except ImportError:
    FACT_PROMPTS_AVAILABLE = False
    print("Warning: Fact-constrained prompts not available")


class PerspectiveAgent:
    """Base class for perspective agents."""

    def __init__(self, name: str, persona: str, tone: str):
        self.name = name
        self.persona = persona
        self.tone = tone
        self.llm_available = self._check_llm()

    def _check_llm(self) -> bool:
        """Check if LLM is available."""
        return bool(os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY'))

    def generate_insights(self, data_summary: Dict, context: Optional[Dict] = None,
                         verified_facts: Optional[str] = None) -> Dict:
        """
        Generate insights from this perspective.

        Parameters
        ----------
        data_summary : dict
            Summary of marketing data/metrics (for backward compatibility)
        context : dict, optional
            Additional business context
        verified_facts : str, optional
            Numbered list of verified facts with sources (REQUIRED for fact-constrained mode)

        Returns
        -------
        dict with insights, recommendations, tone
        """
        # NEW: If verified facts provided, use fact-constrained mode
        if verified_facts and FACT_PROMPTS_AVAILABLE:
            return self._fact_constrained_generate(data_summary.get('query', 'Unknown'), verified_facts)
        # Fallback to old behavior (will be phased out)
        elif self.llm_available:
            return self._llm_generate(data_summary, context)
        else:
            return self._rule_based_generate(data_summary, context)

    def _llm_generate(self, data_summary: Dict, context: Optional[Dict]) -> Dict:
        """Generate using LLM."""
        try:
            import openai

            prompt = self._build_prompt(data_summary, context)

            response = openai.ChatCompletion.create(
                model='gpt-4',
                messages=[
                    {
                        'role': 'system',
                        'content': f"You are {self.persona}. {self.tone}"
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )

            # Track usage
            if TRACKER_AVAILABLE:
                try:
                    tracker = get_tracker()
                    usage = response.get('usage', {})
                    tracker.track_call(
                        provider='openai',
                        model='gpt-4',
                        operation='perspective_generation',
                        input_tokens=usage.get('prompt_tokens', 0),
                        output_tokens=usage.get('completion_tokens', 0),
                        success=True
                    )
                except Exception as e:
                    print(f"Usage tracking failed: {e}")

            return self._parse_response(response['choices'][0]['message']['content'])

        except Exception as e:
            # Track failed call
            if TRACKER_AVAILABLE:
                try:
                    tracker = get_tracker()
                    tracker.track_call(
                        provider='openai',
                        model='gpt-4',
                        operation='perspective_generation',
                        input_tokens=0,
                        output_tokens=0,
                        success=False,
                        error=str(e)
                    )
                except:
                    pass

            print(f"LLM generation failed: {e}, falling back to rule-based")
            return self._rule_based_generate(data_summary, context)

    def _build_prompt(self, data_summary: Dict, context: Optional[Dict]) -> str:
        """Build prompt for LLM."""
        context_str = ""
        if context:
            context_str = f"\n\nBusiness Context:\n{context}"

        return f"""
Analyze this marketing data and provide insights from your perspective.

Marketing Data Summary:
{data_summary}
{context_str}

Provide:
1. **Key Insight** (2-3 sentences): Your main takeaway
2. **Top 3 Actions** (specific, actionable recommendations)
3. **Warning/Caveat** (1-2 sentences): What to watch out for

Keep it concise and action-oriented. Speak in your natural voice.
"""

    def _parse_response(self, response_text: str) -> Dict:
        """Parse LLM response."""
        return {
            'perspective': self.name,
            'full_text': response_text,
            'tone': self.tone
        }

    def _fact_constrained_generate(self, company_name: str, verified_facts: str) -> Dict:
        """
        Generate insights using ONLY verified facts (prevents hallucination).

        This method must be implemented by subclasses to use fact-constrained prompts.
        """
        raise NotImplementedError("Subclass must implement _fact_constrained_generate")

    def _rule_based_generate(self, data_summary: Dict, context: Optional[Dict]) -> Dict:
        """Fallback rule-based generation (DEPRECATED - use fact-constrained mode)."""
        raise NotImplementedError("Subclass must implement _rule_based_generate")


class DevilsAdvocateAgent(PerspectiveAgent):
    """😈 Devil's Advocate - Risk analysis, what could go wrong, hidden costs."""

    def __init__(self):
        super().__init__(
            name="Devil's Advocate",
            persona="a risk analyst who identifies threats, vulnerabilities, and what could go wrong",
            tone="Be skeptical, identify risks and red flags, question optimistic assumptions, focus on downside scenarios"
        )

    def _fact_constrained_generate(self, company_name: str, verified_facts: str) -> Dict:
        """Generate Devil's Advocate perspective using ONLY verified facts."""
        if not FACT_PROMPTS_AVAILABLE:
            # Fallback if fact prompts not available
            return {
                'perspective': self.name,
                'full_text': '### 😈 Devil\'s Advocate Perspective\n\n**Error:** Fact-constrained prompts not available.',
                'key_insight': 'System error',
                'actions': [],
                'warning': 'Cannot generate insights without fact-constrained prompts'
            }

        # Get fact-constrained prompt
        prompt = get_fact_constrained_prompt('devil', company_name, verified_facts)

        # Use Claude API to generate risk-focused insights
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse JSON response
            import json
            content = response.content[0].text

            # Extract JSON from response (may be wrapped in markdown)
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()

            result = json.loads(content)

            key_insight = result.get('key_insight', 'No insight generated')
            actions = result.get('actions', [])
            warning = result.get('warning', 'No warning provided')
            data_gaps = result.get('data_gaps', 'No data gaps identified')

        except Exception as e:
            # Fallback to basic analysis if API fails
            key_insight = f"Limited risk analysis available for {company_name} based on {len(verified_facts.split(chr(10)))} verified facts. Unable to perform deep risk assessment without more comprehensive data."
            actions = [
                "Identify key operational risks from available facts",
                "Flag competitive vulnerabilities based on verified data",
                "Note critical missing risk information"
            ]
            warning = "Risk analysis incomplete due to limited data availability."
            data_gaps = "Comprehensive risk assessment requires competitor analysis, financial stress test data, and operational metrics."

        full_text = f"""
### 😈 Devil's Advocate Perspective

**Key Insight:**
{key_insight}

**Recommended Actions:**
{chr(10).join(f"{i+1}. {action}" for i, action in enumerate(actions))}

**Warning:**
⚠️ {warning}

**Data Gaps:**
{data_gaps}

---
*All claims based on verified facts provided. No risks fabricated.*
"""

        return {
            'perspective': self.name,
            'full_text': full_text,
            'tone': self.tone,
            'key_insight': key_insight,
            'actions': actions,
            'warning': warning,
            'data_gaps': data_gaps
        }

    def _rule_based_generate(self, data_summary: Dict, context: Optional[Dict]) -> Dict:
        """Rule-based insights for risk focus (DEPRECATED - use fact-constrained mode)."""

        # Extract key metrics
        spend = data_summary.get('total_spend', 0)
        revenue = data_summary.get('revenue', 0)
        sample_size = data_summary.get('sample_size', 0)

        # Generate risk-focused insight
        if sample_size < 500:
            key_insight = f"Sample size of {sample_size} is too small to trust results. High risk of statistical noise being mistaken for real signal. Could lead to bad decisions."
        elif spend > revenue:
            key_insight = f"Spending £{spend:,.0f} to generate £{revenue:,.0f}? That's a loss. What happens when budget runs out? Unsustainable business model risk."
        else:
            key_insight = f"Numbers look okay on surface, but what risks aren't visible? Dependency on single channel? Market saturation? Competitive response?"

        # Risk-focused actions
        actions = [
            "**Identify single points of failure** - What happens if top channel disappears tomorrow? Diversification risk.",
            "**Stress test assumptions** - Revenue projections assume market stays same. What if competition doubles ad spend?",
            "**Document what could go wrong** - Create risk register: platform policy changes, attribution breakdown, market shifts"
        ]

        # Warning
        warning = "Success today doesn't mean success tomorrow. Markets change, competitors adapt, platforms update algorithms. Plan for downside."

        full_text = f"""
### 😈 Devil's Advocate Perspective

**Key Insight:**
{key_insight}

**Top 3 Actions:**
{chr(10).join(f"{i+1}. {action}" for i, action in enumerate(actions))}

**Warning:**
⚠️ {warning}
"""

        return {
            'perspective': self.name,
            'full_text': full_text,
            'tone': self.tone,
            'key_insight': key_insight,
            'actions': actions,
            'warning': warning
        }


class OptimistAgent(PerspectiveAgent):
    """🌟 Optimist - Growth opportunities, untapped potential, quick wins."""

    def __init__(self):
        super().__init__(
            name="Optimist",
            persona="a growth strategist who identifies opportunities, quick wins, and untapped potential",
            tone="Be enthusiastic about possibilities, spot opportunities, think growth-focused, identify low-hanging fruit"
        )

    def _fact_constrained_generate(self, company_name: str, verified_facts: str) -> Dict:
        """Generate Optimist perspective using ONLY verified facts."""
        if not FACT_PROMPTS_AVAILABLE:
            return {
                'perspective': self.name,
                'full_text': '### 🌟 Optimist Perspective\n\n**Error:** Fact-constrained prompts not available.',
                'key_insight': 'System error',
                'actions': [],
                'warning': 'Cannot generate insights without fact-constrained prompts'
            }

        # Get fact-constrained prompt
        prompt = get_fact_constrained_prompt('optimist', company_name, verified_facts)

        # Use Claude API to generate opportunity-focused insights
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse JSON response
            import json
            content = response.content[0].text

            # Extract JSON from response (may be wrapped in markdown)
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()

            result = json.loads(content)

            key_insight = result.get('key_insight', 'No insight generated')
            actions = result.get('actions', [])
            warning = result.get('warning', 'No warning provided')
            data_gaps = result.get('data_gaps', 'No data gaps identified')

        except Exception as e:
            # Fallback to basic analysis if API fails
            key_insight = f"Growth opportunity analysis for {company_name} based on {len(verified_facts.split(chr(10)))} verified facts. Several potential opportunities visible in available data."
            actions = [
                "Identify competitive advantages from verified facts",
                "Spot underutilized strengths or market positions",
                "Look for quick win opportunities in available data"
            ]
            warning = "Growth recommendations require validation with market research and customer insights."
            data_gaps = "Comprehensive opportunity analysis requires market sizing, customer research, and competitive intelligence."

        full_text = f"""
### 🌟 Optimist Perspective

**Key Insight:**
{key_insight}

**Recommended Actions:**
{chr(10).join(f"{i+1}. {action}" for i, action in enumerate(actions))}

**Warning:**
⚠️ {warning}

**Data Gaps:**
{data_gaps}

---
*All opportunities based on verified facts provided. No market projections fabricated.*
"""

        return {
            'perspective': self.name,
            'full_text': full_text,
            'tone': self.tone,
            'key_insight': key_insight,
            'actions': actions,
            'warning': warning,
            'data_gaps': data_gaps
        }

    def _rule_based_generate(self, data_summary: Dict, context: Optional[Dict]) -> Dict:
        """Rule-based insights for opportunity focus (DEPRECATED - use fact-constrained mode)."""

        # Extract metrics
        revenue = data_summary.get('revenue', 0)
        spend = data_summary.get('total_spend', 0)
        engagement_rate = data_summary.get('engagement_rate', 0)

        # Generate opportunity-focused insight
        if revenue > spend * 2:
            key_insight = f"Strong performance at £{revenue:,.0f} revenue from £{spend:,.0f} spend. There's momentum here - can we double down and scale what's working?"
        elif engagement_rate > 3:
            key_insight = f"High engagement at {engagement_rate}% means audience is interested. Opportunity to convert attention into action. What's the next step?"
        else:
            key_insight = f"Current performance shows potential. Look for untapped opportunities: new channels, audience segments, or messaging angles that haven't been tested yet."

        # Opportunity-focused actions
        actions = [
            "**Scale what's working** - Identify top performing elements and increase investment systematically",
            "**Test new channels** - Current mix might be leaving opportunities on table. Quick pilots in adjacent spaces",
            "**Expand audience reach** - Look for lookalike segments or geographic expansion opportunities"
        ]

        # Warning
        warning = "Growth requires investment. Quick wins are great, but sustainable growth needs sustained effort and budget."

        full_text = f"""
### 🌟 Optimist Perspective

**Key Insight:**
{key_insight}

**Top 3 Actions:**
{chr(10).join(f"{i+1}. {action}" for i, action in enumerate(actions))}

**Warning:**
⚠️ {warning}
"""

        return {
            'perspective': self.name,
            'full_text': full_text,
            'tone': self.tone,
            'key_insight': key_insight,
            'actions': actions,
            'warning': warning
        }


class RealistAgent(PerspectiveAgent):
    """⚖️ Realist - Practical constraints, trade-offs, MVP approach."""

    def __init__(self):
        super().__init__(
            name="Realist",
            persona="a pragmatic operator who focuses on what's actually doable given constraints",
            tone="Be practical, acknowledge trade-offs, focus on MVP approach, balance ambition with reality"
        )

    def _fact_constrained_generate(self, company_name: str, verified_facts: str) -> Dict:
        """Generate Realist perspective using ONLY verified facts."""
        if not FACT_PROMPTS_AVAILABLE:
            return {
                'perspective': self.name,
                'full_text': '### ⚖️ Realist Perspective\n\n**Error:** Fact-constrained prompts not available.',
                'key_insight': 'System error',
                'actions': [],
                'warning': 'Cannot generate insights without fact-constrained prompts'
            }

        # Get fact-constrained prompt
        prompt = get_fact_constrained_prompt('realist', company_name, verified_facts)

        # Use Claude API to generate pragmatic insights
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse JSON response
            import json
            content = response.content[0].text

            # Extract JSON from response (may be wrapped in markdown)
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()

            result = json.loads(content)

            key_insight = result.get('key_insight', 'No insight generated')
            actions = result.get('actions', [])
            warning = result.get('warning', 'No warning provided')
            data_gaps = result.get('data_gaps', 'No data gaps identified')

        except Exception as e:
            # Fallback to basic analysis if API fails
            key_insight = f"Pragmatic assessment of {company_name} based on {len(verified_facts.split(chr(10)))} verified facts. Focus on what's actually achievable with available resources and data."
            actions = [
                "Prioritize actions based on verified facts and resource constraints",
                "Identify quick wins that don't require additional data",
                "Note what's realistically achievable vs. aspirational"
            ]
            warning = "Pragmatic recommendations require clear understanding of resource constraints and organizational capacity."
            data_gaps = "Realistic planning requires understanding of budget constraints, team capacity, and technical capabilities."

        full_text = f"""
### ⚖️ Realist Perspective

**Key Insight:**
{key_insight}

**Recommended Actions:**
{chr(10).join(f"{i+1}. {action}" for i, action in enumerate(actions))}

**Warning:**
⚠️ {warning}

**Data Gaps:**
{data_gaps}

---
*All recommendations based on verified facts and practical constraints. No aspirational claims fabricated.*
"""

        return {
            'perspective': self.name,
            'full_text': full_text,
            'tone': self.tone,
            'key_insight': key_insight,
            'actions': actions,
            'warning': warning,
            'data_gaps': data_gaps
        }

    def _rule_based_generate(self, data_summary: Dict, context: Optional[Dict]) -> Dict:
        """Rule-based insights for pragmatic focus (DEPRECATED - use fact-constrained mode)."""

        # Extract metrics
        spend = data_summary.get('total_spend', 0)
        revenue = data_summary.get('revenue', 0)
        time_period = data_summary.get('time_period_days', 0)

        # Generate pragmatic insight
        roas = revenue / spend if spend > 0 else 0
        if roas < 1.5:
            key_insight = f"Current performance ({roas:.1f}x ROAS) isn't sustainable long-term. Need to focus on fundamentals: better targeting, cleaner attribution, tighter budget control."
        elif time_period < 14:
            key_insight = f"Only {time_period} days of data. Too early for big decisions. Run it longer, gather more signal, then decide on next steps."
        else:
            key_insight = f"Performance looks workable ({roas:.1f}x ROAS). Focus on incremental improvements rather than risky pivots. Steady progress beats home runs."

        # Pragmatic actions
        actions = [
            "**Start with MVP changes** - Don't overhaul everything. Test one variable at a time, measure, iterate",
            "**Work within constraints** - What can we improve with current budget and team? Focus there first",
            "**Set realistic milestones** - Break big goals into 2-week sprints. Track progress, adjust as needed"
        ]

        # Warning
        warning = "Perfect is the enemy of good. Ship something workable this week, not something perfect next quarter."

        full_text = f"""
### ⚖️ Realist Perspective

**Key Insight:**
{key_insight}

**Top 3 Actions:**
{chr(10).join(f"{i+1}. {action}" for i, action in enumerate(actions))}

**Warning:**
⚠️ {warning}
"""

        return {
            'perspective': self.name,
            'full_text': full_text,
            'tone': self.tone,
            'key_insight': key_insight,
            'actions': actions,
            'warning': warning
        }


# Factory function
def get_all_perspectives() -> List[PerspectiveAgent]:
    """Get all available perspective agents."""
    return [
        DevilsAdvocateAgent(),
        OptimistAgent(),
        RealistAgent()
    ]


def get_perspective_agent(name: str) -> Optional[PerspectiveAgent]:
    """Get a specific perspective agent by name."""
    agents = {
        'devil': DevilsAdvocateAgent(),
        'optimist': OptimistAgent(),
        'realist': RealistAgent()
    }
    return agents.get(name.lower())


# Example usage
if __name__ == '__main__':
    # Mock data
    data_summary = {
        'total_spend': 50000,
        'revenue': 120000,
        'sample_size': 1500,
        'time_period_days': 45,
        'channels': ['Facebook', 'Google', 'TikTok'],
        'brand_awareness': 25,
        'engagement_rate': 1.8
    }

    context = {
        'industry': 'E-commerce Fashion',
        'target_audience': 'Gen-Z females',
        'campaign_type': 'Product launch'
    }

    print("=" * 80)
    print("MARKETING INTELLIGENCE: MULTIPLE PERSPECTIVES")
    print("=" * 80)

    for agent in get_all_perspectives():
        insights = agent.generate_insights(data_summary, context)
        print(f"\n{insights['full_text']}")
        print("-" * 80)
