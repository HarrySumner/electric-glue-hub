"""
Agentic TV Campaign Impact Analyzer - Multi-Agent System

This module contains specialized AI agents for TV campaign causal analysis.
"""

from agents.data_agent import DataAgent, create_sample_data
from agents.validation_agent import ValidationAgent
from agents.analysis_agent import AnalysisAgent
from agents.interpretation_agent import InterpretationAgent
from agents.orchestrator import OrchestratorAgent, WorkflowState

__all__ = [
    'DataAgent',
    'ValidationAgent',
    'AnalysisAgent',
    'InterpretationAgent',
    'OrchestratorAgent',
    'WorkflowState',
    'create_sample_data'
]

__version__ = '1.0.0'
