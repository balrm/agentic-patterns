"""
Base classes for AI agent design patterns.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class PatternResult(BaseModel):
    """Result returned by pattern execution."""
    
    response: str = Field(..., description="The final response from the pattern")
    cost: float = Field(default=0.0, description="Cost of the operation in tokens/credits")
    pattern_name: str = Field(..., description="Name of the pattern used")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Pattern-specific metadata")
    success: bool = Field(default=True, description="Whether the pattern execution was successful")
    error_message: Optional[str] = Field(default=None, description="Error message if execution failed")


class LLMClient(ABC):
    """Abstract interface for LLM clients."""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def estimate_cost(self, prompt: str, response: str) -> float:
        """Estimate the cost of the generation."""
        pass


class BasePattern(ABC):
    """Base class for all AI agent design patterns."""
    
    def __init__(self, llm_client: LLMClient, **kwargs):
        self.llm_client = llm_client
        self.config = kwargs
    
    @abstractmethod
    async def execute(self, prompt: str) -> PatternResult:
        """
        Execute the pattern with the given prompt.
        
        Args:
            prompt: The input prompt to process
            
        Returns:
            PatternResult containing the response and metadata
        """
        pass
    
    def get_pattern_name(self) -> str:
        """Get the name of this pattern."""
        return self.__class__.__name__
    
    async def _call_llm(self, prompt: str, **kwargs) -> str:
        """Helper method to call the LLM with error handling."""
        try:
            return await self.llm_client.generate(prompt, **kwargs)
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}") from e
    
    def _estimate_cost(self, prompt: str, response: str) -> float:
        """Helper method to estimate cost."""
        try:
            return self.llm_client.estimate_cost(prompt, response)
        except Exception:
            # Fallback to simple character-based estimation
            return len(prompt + response) / 1000.0  # Rough estimate 