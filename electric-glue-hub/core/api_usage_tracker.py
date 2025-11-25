"""
API Usage Tracker - Monitor OpenAI and Anthropic API costs
Tracks tokens, requests, and estimated costs for all LLM operations
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
import threading

@dataclass
class APICall:
    """Record of a single API call."""
    timestamp: str
    provider: str  # 'openai' or 'anthropic'
    model: str
    operation: str  # 'qa_validation', 'scout_research', 'perspective_generation', etc.
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost: float
    success: bool
    error: Optional[str] = None

class APIUsageTracker:
    """
    Track API usage and costs across all Electric Glue products.

    Thread-safe, persistent storage in JSON file.
    """

    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        'openai': {
            'gpt-4': {'input': 30.0, 'output': 60.0},  # $30/$60 per 1M tokens
            'gpt-4-turbo': {'input': 10.0, 'output': 30.0},
            'gpt-3.5-turbo': {'input': 0.5, 'output': 1.5}
        },
        'anthropic': {
            'claude-3-5-sonnet-20241022': {'input': 3.0, 'output': 15.0},  # $3/$15 per 1M tokens
            'claude-3-opus': {'input': 15.0, 'output': 75.0},
            'claude-3-sonnet': {'input': 3.0, 'output': 15.0},
            'claude-3-haiku': {'input': 0.25, 'output': 1.25}
        }
    }

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize usage tracker.

        Args:
            storage_path: Path to store usage data (defaults to .electric_glue_usage.json)
        """
        if storage_path is None:
            # Store in project root
            storage_path = Path(__file__).parent.parent / '.electric_glue_usage.json'

        self.storage_path = storage_path
        self.lock = threading.Lock()
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist."""
        if not self.storage_path.exists():
            with open(self.storage_path, 'w') as f:
                json.dump({
                    'calls': [],
                    'summary': {
                        'total_calls': 0,
                        'total_tokens': 0,
                        'total_cost': 0.0,
                        'by_provider': {},
                        'by_operation': {}
                    }
                }, f, indent=2)

    def track_call(
        self,
        provider: str,
        model: str,
        operation: str,
        input_tokens: int,
        output_tokens: int,
        success: bool = True,
        error: Optional[str] = None
    ) -> float:
        """
        Track an API call and return estimated cost.

        Args:
            provider: 'openai' or 'anthropic'
            model: Model name (e.g., 'gpt-4', 'claude-3-5-sonnet-20241022')
            operation: Operation type (e.g., 'qa_validation', 'scout_research')
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            success: Whether the call succeeded
            error: Error message if failed

        Returns:
            Estimated cost in USD
        """
        total_tokens = input_tokens + output_tokens
        estimated_cost = self._calculate_cost(provider, model, input_tokens, output_tokens)

        call = APICall(
            timestamp=datetime.now().isoformat(),
            provider=provider,
            model=model,
            operation=operation,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost=estimated_cost,
            success=success,
            error=error
        )

        self._save_call(call)
        return estimated_cost

    def _calculate_cost(self, provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate estimated cost for a call."""
        pricing = self.PRICING.get(provider, {}).get(model)

        if not pricing:
            # Unknown model, use average pricing
            if provider == 'openai':
                pricing = {'input': 10.0, 'output': 30.0}
            else:
                pricing = {'input': 3.0, 'output': 15.0}

        # Convert from per 1M tokens to actual cost
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']

        return input_cost + output_cost

    def _save_call(self, call: APICall):
        """Save call to storage (thread-safe)."""
        with self.lock:
            data = self._load_data()
            data['calls'].append(asdict(call))
            self._update_summary(data, call)

            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

    def _update_summary(self, data: Dict, call: APICall):
        """Update summary statistics."""
        summary = data['summary']

        summary['total_calls'] += 1
        summary['total_tokens'] += call.total_tokens
        summary['total_cost'] += call.estimated_cost

        # By provider
        if call.provider not in summary['by_provider']:
            summary['by_provider'][call.provider] = {
                'calls': 0,
                'tokens': 0,
                'cost': 0.0
            }
        summary['by_provider'][call.provider]['calls'] += 1
        summary['by_provider'][call.provider]['tokens'] += call.total_tokens
        summary['by_provider'][call.provider]['cost'] += call.estimated_cost

        # By operation
        if call.operation not in summary['by_operation']:
            summary['by_operation'][call.operation] = {
                'calls': 0,
                'tokens': 0,
                'cost': 0.0
            }
        summary['by_operation'][call.operation]['calls'] += 1
        summary['by_operation'][call.operation]['tokens'] += call.total_tokens
        summary['by_operation'][call.operation]['cost'] += call.estimated_cost

    def _load_data(self) -> Dict:
        """Load data from storage."""
        with open(self.storage_path, 'r') as f:
            return json.load(f)

    def get_summary(self) -> Dict:
        """Get usage summary."""
        with self.lock:
            data = self._load_data()
            return data['summary']

    def get_recent_calls(self, limit: int = 10) -> List[Dict]:
        """Get most recent API calls."""
        with self.lock:
            data = self._load_data()
            calls = data['calls']
            return calls[-limit:] if calls else []

    def get_daily_summary(self, days: int = 7) -> Dict:
        """Get summary for last N days."""
        with self.lock:
            data = self._load_data()
            calls = data['calls']

            # Filter calls from last N days
            cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
            recent_calls = [
                c for c in calls
                if datetime.fromisoformat(c['timestamp']).timestamp() > cutoff
            ]

            # Aggregate by day
            daily_stats = {}
            for call in recent_calls:
                date = call['timestamp'].split('T')[0]
                if date not in daily_stats:
                    daily_stats[date] = {
                        'calls': 0,
                        'tokens': 0,
                        'cost': 0.0,
                        'by_provider': {}
                    }

                daily_stats[date]['calls'] += 1
                daily_stats[date]['tokens'] += call['total_tokens']
                daily_stats[date]['cost'] += call['estimated_cost']

                provider = call['provider']
                if provider not in daily_stats[date]['by_provider']:
                    daily_stats[date]['by_provider'][provider] = {
                        'calls': 0,
                        'cost': 0.0
                    }
                daily_stats[date]['by_provider'][provider]['calls'] += 1
                daily_stats[date]['by_provider'][provider]['cost'] += call['estimated_cost']

            return daily_stats

    def reset_stats(self):
        """Reset all usage statistics."""
        with self.lock:
            with open(self.storage_path, 'w') as f:
                json.dump({
                    'calls': [],
                    'summary': {
                        'total_calls': 0,
                        'total_tokens': 0,
                        'total_cost': 0.0,
                        'by_provider': {},
                        'by_operation': {}
                    }
                }, f, indent=2)


# Global tracker instance
_tracker = None

def get_tracker() -> APIUsageTracker:
    """Get or create global tracker instance."""
    global _tracker
    if _tracker is None:
        _tracker = APIUsageTracker()
    return _tracker
