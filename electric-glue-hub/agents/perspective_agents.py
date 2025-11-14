"""
Perspective Agents - Multiple viewpoints on marketing data
Generates action-oriented insights from different personas
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


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

    def generate_insights(self, data_summary: Dict, context: Optional[Dict] = None) -> Dict:
        """
        Generate insights from this perspective.

        Parameters
        ----------
        data_summary : dict
            Summary of marketing data/metrics
        context : dict, optional
            Additional business context

        Returns
        -------
        dict with insights, recommendations, tone
        """
        if self.llm_available:
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

            return self._parse_response(response['choices'][0]['message']['content'])

        except Exception as e:
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

    def _rule_based_generate(self, data_summary: Dict, context: Optional[Dict]) -> Dict:
        """Fallback rule-based generation."""
        raise NotImplementedError("Subclass must implement _rule_based_generate")


class StingyCustomerAgent(PerspectiveAgent):
    """The budget-conscious, ROI-focused perspective."""

    def __init__(self):
        super().__init__(
            name="Stingy Customer",
            persona="a budget-conscious CFO who scrutinizes every pound spent on marketing",
            tone="Be skeptical of spending, focus on ROI and efficiency, question assumptions, demand proof of value"
        )

    def _rule_based_generate(self, data_summary: Dict, context: Optional[Dict]) -> Dict:
        """Rule-based insights for budget focus."""

        # Extract key metrics
        spend = data_summary.get('total_spend', 0)
        revenue = data_summary.get('revenue', 0)
        roas = revenue / spend if spend > 0 else 0

        # Generate insight based on ROAS
        if roas > 3:
            key_insight = f"Decent return at {roas:.1f}x ROAS, but can we do better? Let's cut the fat and focus on what's actually working."
        elif roas > 1:
            key_insight = f"Barely breaking even at {roas:.1f}x ROAS. We're spending £{spend:,.0f} to make £{revenue:,.0f}. Not good enough."
        else:
            key_insight = f"Losing money! {roas:.1f}x ROAS means we're burning cash. Time for serious cuts and pivot."

        # Top actions (budget-focused)
        actions = [
            f"**Cut bottom 20% performers immediately** - Reallocate that £{spend*0.2:,.0f} to proven channels",
            "**Demand proof before any new spend** - Pilot test with £5-10K max, measure ruthlessly",
            "**Negotiate all vendor contracts down 15-20%** - Everyone's overcharging, push back hard"
        ]

        # Warning
        warning = "Don't fall for 'brand building' excuses. If it can't be measured, it shouldn't be funded. Period."

        full_text = f"""
### 💰 Stingy Customer Perspective

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


class CriticalThinkerAgent(PerspectiveAgent):
    """The analytical, questioning, devil's advocate perspective."""

    def __init__(self):
        super().__init__(
            name="Critical Thinker",
            persona="a data scientist who questions every assumption and looks for flaws in logic",
            tone="Be skeptical, analytical, look for confounders and biases, demand rigor, play devil's advocate"
        )

    def _rule_based_generate(self, data_summary: Dict, context: Optional[Dict]) -> Dict:
        """Rule-based insights for critical analysis."""

        # Extract metrics
        sample_size = data_summary.get('sample_size', 0)
        time_period = data_summary.get('time_period_days', 0)
        channels = data_summary.get('channels', [])

        # Generate insight based on data quality
        if sample_size < 1000:
            key_insight = f"Small sample size ({sample_size}) raises serious questions about statistical power. Can we trust these results, or are we seeing random noise?"
        elif time_period < 30:
            key_insight = f"Only {time_period} days of data? That's not enough to account for seasonality, day-of-week effects, or external shocks. Conclusions are premature."
        else:
            key_insight = f"Data looks reasonable ({sample_size} samples over {time_period} days), but let's check for confounders, selection bias, and time-varying effects before declaring victory."

        # Top actions (analytical focus)
        actions = [
            "**Test key assumptions** - Are we assuming linearity? Constant effects? Check if these hold across segments and time periods",
            "**Look for confounders** - What else changed during this period? Competitors, seasonality, external events? Control for them",
            "**Run sensitivity analysis** - How much do results change with different assumptions? If fragile, we need more data"
        ]

        # Warning
        warning = "Correlation ≠ causation. Just because metric X moved when we did Y doesn't mean Y caused X. Be intellectually honest."

        full_text = f"""
### 🔬 Critical Thinker Perspective

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


class CreativeAdManAgent(PerspectiveAgent):
    """The bold, brand-focused, creative opportunities perspective."""

    def __init__(self):
        super().__init__(
            name="Creative Ad Man",
            persona="a creative director who sees opportunities for bold campaigns and brand building",
            tone="Be enthusiastic about creative opportunities, think big picture, focus on brand impact, suggest bold ideas"
        )

    def _rule_based_generate(self, data_summary: Dict, context: Optional[Dict]) -> Dict:
        """Rule-based insights for creative focus."""

        # Extract metrics
        brand_awareness = data_summary.get('brand_awareness', 0)
        engagement_rate = data_summary.get('engagement_rate', 0)
        channels = data_summary.get('channels', [])

        # Generate insight based on brand metrics
        if brand_awareness < 30:
            key_insight = f"Brand awareness at {brand_awareness}% is criminally low. We need a big, bold campaign that gets people talking. Think Super Bowl, not spreadsheet."
        elif engagement_rate < 2:
            key_insight = f"People aren't connecting with the brand. {engagement_rate}% engagement means our creative is forgettable. Time to take risks."
        else:
            key_insight = f"Solid foundation ({brand_awareness}% awareness, {engagement_rate}% engagement), but let's capitalize with a breakthrough campaign that owns the conversation."

        # Top actions (creative focus)
        actions = [
            "**Launch a provocative brand campaign** - Something that gets PR, social buzz, and watercooler talk. Safe = invisible",
            "**Partner with unexpected influencers** - Not the usual suspects. Find culture creators who align with brand values",
            "**Create a cultural moment** - Tie into something people care about. Activism, entertainment, lifestyle shifts"
        ]

        # Warning
        warning = "Don't let performance marketers kill every creative idea. Great creative compounds over time. You can't A/B test a Superbowl ad."

        full_text = f"""
### 🎨 Creative Ad Man Perspective

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
        StingyCustomerAgent(),
        CriticalThinkerAgent(),
        CreativeAdManAgent()
    ]


def get_perspective_agent(name: str) -> Optional[PerspectiveAgent]:
    """Get a specific perspective agent by name."""
    agents = {
        'stingy': StingyCustomerAgent(),
        'critical': CriticalThinkerAgent(),
        'creative': CreativeAdManAgent()
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
