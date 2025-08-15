"""
Factory module for creating and managing AI agent patterns.
"""

from typing import Dict, Type, Optional
from .base import BasePattern, LLMClient
from .patterns import (
    ChainOfThoughtPattern,
    ReflexionPattern,
    TreeOfThoughtsPattern,
    MultiAgentDebatePattern,
    ToolUsePattern,
)


# Registry of available patterns
_PATTERN_REGISTRY: Dict[str, Type[BasePattern]] = {
    "chain_of_thought": ChainOfThoughtPattern,
    "cot": ChainOfThoughtPattern,
    "reflexion": ReflexionPattern,
    "tree_of_thoughts": TreeOfThoughtsPattern,
    "tot": TreeOfThoughtsPattern,
    "multi_agent_debate": MultiAgentDebatePattern,
    "debate": MultiAgentDebatePattern,
    "tool_use": ToolUsePattern,
    "tools": ToolUsePattern,
}


def get_pattern(pattern_name: str, llm_client: LLMClient, **kwargs) -> BasePattern:
    """
    Get a pattern instance by name.
    
    Args:
        pattern_name: Name of the pattern to create
        llm_client: LLM client instance
        **kwargs: Additional configuration for the pattern
        
    Returns:
        Pattern instance
        
    Raises:
        ValueError: If pattern name is not found
    """
    pattern_name = pattern_name.lower().replace(" ", "_")
    
    if pattern_name not in _PATTERN_REGISTRY:
        available_patterns = ", ".join(_PATTERN_REGISTRY.keys())
        raise ValueError(
            f"Pattern '{pattern_name}' not found. Available patterns: {available_patterns}"
        )
    
    pattern_class = _PATTERN_REGISTRY[pattern_name]
    return pattern_class(llm_client, **kwargs)


def list_patterns() -> Dict[str, str]:
    """
    List all available patterns with their descriptions.
    
    Returns:
        Dictionary mapping pattern names to descriptions
    """
    return {
        "chain_of_thought": "Chain-of-Thought pattern for step-by-step reasoning",
        "reflexion": "Reflexion pattern for iterative self-improvement",
        "tree_of_thoughts": "Tree of Thoughts pattern for exploring multiple reasoning paths",
        "multi_agent_debate": "Multi-Agent Debate pattern with different perspectives",
        "tool_use": "Tool-Use pattern for external tool integration",
    }


def register_pattern(name: str, pattern_class: Type[BasePattern], aliases: Optional[list] = None) -> None:
    """
    Register a custom pattern.
    
    Args:
        name: Primary name for the pattern
        pattern_class: Pattern class that inherits from BasePattern
        aliases: Optional list of alternative names for the pattern
    """
    if not issubclass(pattern_class, BasePattern):
        raise ValueError("Pattern class must inherit from BasePattern")
    
    # Register primary name
    _PATTERN_REGISTRY[name.lower()] = pattern_class
    
    # Register aliases
    if aliases:
        for alias in aliases:
            _PATTERN_REGISTRY[alias.lower()] = pattern_class


def unregister_pattern(name: str) -> None:
    """
    Unregister a pattern.
    
    Args:
        name: Name of the pattern to unregister
    """
    name = name.lower()
    if name in _PATTERN_REGISTRY:
        del _PATTERN_REGISTRY[name]


def get_pattern_info(pattern_name: str) -> Optional[Dict[str, str]]:
    """
    Get information about a specific pattern.
    
    Args:
        pattern_name: Name of the pattern
        
    Returns:
        Dictionary with pattern information or None if not found
    """
    pattern_name = pattern_name.lower()
    
    if pattern_name not in _PATTERN_REGISTRY:
        return None
    
    pattern_class = _PATTERN_REGISTRY[pattern_name]
    
    return {
        "name": pattern_name,
        "class": pattern_class.__name__,
        "description": pattern_class.__doc__ or "No description available",
        "module": pattern_class.__module__,
    } 