"""
Agentic Patterns - A standardized library for AI agent design patterns.

This package provides a collection of proven AI agent design patterns
that can be easily swapped and combined for different use cases.
"""

from .base import BasePattern, PatternResult
from .patterns import (
    ChainOfThoughtPattern,
    ReflexionPattern,
    TreeOfThoughtsPattern,
    MultiAgentDebatePattern,
    ToolUsePattern,
)
from .factory import get_pattern, list_patterns, register_pattern, get_pattern_info
from .clients import create_client

__version__ = "0.1.0"
__all__ = [
    "BasePattern",
    "PatternResult",
    "ChainOfThoughtPattern",
    "ReflexionPattern", 
    "TreeOfThoughtsPattern",
    "MultiAgentDebatePattern",
    "ToolUsePattern",
    "get_pattern",
    "list_patterns",
    "register_pattern",
    "get_pattern_info",
    "create_client",
] 