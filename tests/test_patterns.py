"""
Tests for agentic patterns library.
"""

import pytest
import asyncio
from agentic_patterns import (
    get_pattern, 
    list_patterns, 
    register_pattern, 
    create_client,
    BasePattern,
    PatternResult
)
from agentic_patterns.patterns import (
    ChainOfThoughtPattern,
    ReflexionPattern,
    TreeOfThoughtsPattern,
    MultiAgentDebatePattern,
    ToolUsePattern
)


@pytest.fixture
def mock_client():
    """Create a mock LLM client for testing."""
    return create_client("mock")


@pytest.fixture
def sample_prompt():
    """Sample prompt for testing."""
    return "What is 2 + 2?"


class TestChainOfThoughtPattern:
    """Test Chain-of-Thought pattern."""
    
    @pytest.mark.asyncio
    async def test_execute(self, mock_client, sample_prompt):
        """Test basic execution."""
        pattern = ChainOfThoughtPattern(mock_client)
        result = await pattern.execute(sample_prompt)
        
        assert isinstance(result, PatternResult)
        assert result.response is not None
        assert result.cost >= 0
        assert result.pattern_name == "ChainOfThoughtPattern"
        assert result.success is True
        assert "original_prompt" in result.metadata
        assert "cot_prompt" in result.metadata
    
    @pytest.mark.asyncio
    async def test_cot_prompt_format(self, mock_client):
        """Test that CoT adds the correct instruction."""
        pattern = ChainOfThoughtPattern(mock_client)
        result = await pattern.execute("Test prompt")
        
        assert "Let's think step by step:" in result.metadata["cot_prompt"]
    
    def test_extract_reasoning_steps(self, mock_client):
        """Test reasoning step extraction."""
        pattern = ChainOfThoughtPattern(mock_client)
        response = "1. First step\n2. Second step\n3. Third step"
        steps = pattern._extract_reasoning_steps(response)
        
        assert len(steps) == 3
        assert "First step" in steps[0]


class TestReflexionPattern:
    """Test Reflexion pattern."""
    
    @pytest.mark.asyncio
    async def test_execute(self, mock_client, sample_prompt):
        """Test basic execution."""
        pattern = ReflexionPattern(mock_client, max_iterations=2)
        result = await pattern.execute(sample_prompt)
        
        assert isinstance(result, PatternResult)
        assert result.response is not None
        assert result.cost >= 0
        assert result.pattern_name == "ReflexionPattern"
        assert result.success is True
        assert "iterations" in result.metadata
    
    @pytest.mark.asyncio
    async def test_max_iterations(self, mock_client):
        """Test that pattern respects max iterations."""
        pattern = ReflexionPattern(mock_client, max_iterations=1)
        result = await pattern.execute("Test prompt")
        
        # Should complete in 1 iteration
        assert len(result.metadata["iterations"]) <= 1
    
    @pytest.mark.asyncio
    async def test_learnings_storage(self, mock_client):
        """Test that learnings are stored."""
        pattern = ReflexionPattern(mock_client, max_iterations=2)
        await pattern.execute("Test prompt")
        
        assert len(pattern.learnings) > 0


class TestTreeOfThoughtsPattern:
    """Test Tree of Thoughts pattern."""
    
    @pytest.mark.asyncio
    async def test_execute(self, mock_client, sample_prompt):
        """Test basic execution."""
        pattern = TreeOfThoughtsPattern(mock_client, max_depth=2, thoughts_per_level=2)
        result = await pattern.execute(sample_prompt)
        
        assert isinstance(result, PatternResult)
        assert result.response is not None
        assert result.cost >= 0
        assert result.pattern_name == "TreeOfThoughtsPattern"
        assert result.success is True
        assert "tree" in result.metadata
        assert "best_path" in result.metadata
    
    @pytest.mark.asyncio
    async def test_tree_depth(self, mock_client):
        """Test that tree respects max depth."""
        pattern = TreeOfThoughtsPattern(mock_client, max_depth=1, thoughts_per_level=2)
        result = await pattern.execute("Test prompt")
        
        # Should only have one level
        tree = result.metadata["tree"]
        max_level = max(t["level"] for t in tree["thoughts"])
        assert max_level == 0
    
    @pytest.mark.asyncio
    async def test_thoughts_per_level(self, mock_client):
        """Test that pattern generates correct number of thoughts."""
        pattern = TreeOfThoughtsPattern(mock_client, max_depth=1, thoughts_per_level=3)
        result = await pattern.execute("Test prompt")
        
        # Should have exactly 3 thoughts at level 0
        tree = result.metadata["tree"]
        level_0_thoughts = [t for t in tree["thoughts"] if t["level"] == 0]
        assert len(level_0_thoughts) == 3


class TestMultiAgentDebatePattern:
    """Test Multi-Agent Debate pattern."""
    
    @pytest.mark.asyncio
    async def test_execute(self, mock_client, sample_prompt):
        """Test basic execution."""
        pattern = MultiAgentDebatePattern(mock_client, num_agents=3)
        result = await pattern.execute(sample_prompt)
        
        assert isinstance(result, PatternResult)
        assert result.response is not None
        assert result.cost >= 0
        assert result.pattern_name == "MultiAgentDebatePattern"
        assert result.success is True
        assert "debate" in result.metadata
        assert "num_agents" in result.metadata
    
    @pytest.mark.asyncio
    async def test_debate_structure(self, mock_client):
        """Test that debate has correct structure."""
        pattern = MultiAgentDebatePattern(mock_client, num_agents=3)
        result = await pattern.execute("Test prompt")
        
        debate = result.metadata["debate"]
        assert len(debate) == 3  # 3 agents
        
        # Check agent names
        agent_names = [d["agent"] for d in debate]
        assert "Agent 1 (Optimistic)" in agent_names
        assert "Agent 2 (Critical)" in agent_names
        assert "Agent 3 (Analytical)" in agent_names


class TestToolUsePattern:
    """Test Tool-Use pattern."""
    
    @pytest.mark.asyncio
    async def test_execute(self, mock_client, sample_prompt):
        """Test basic execution."""
        pattern = ToolUsePattern(mock_client)
        result = await pattern.execute(sample_prompt)
        
        assert isinstance(result, PatternResult)
        assert result.response is not None
        assert result.cost >= 0
        assert result.pattern_name == "ToolUsePattern"
        assert result.success is True
        assert "tool_analysis" in result.metadata
        assert "tool_results" in result.metadata
    
    @pytest.mark.asyncio
    async def test_tool_detection(self, mock_client):
        """Test tool detection logic."""
        pattern = ToolUsePattern(mock_client)
        
        # Test with calculation prompt
        result = await pattern.execute("Calculate 5 + 5")
        
        assert "tool_analysis" in result.metadata
        tool_analysis = result.metadata["tool_analysis"]
        assert "needs_tools" in tool_analysis
        assert "tool_calls" in tool_analysis
    
    def test_default_tools(self, mock_client):
        """Test that default tools are available."""
        pattern = ToolUsePattern(mock_client)
        
        assert "calculate" in pattern.available_tools
        assert "sqrt" in pattern.available_tools
        assert "current_time" in pattern.available_tools


class TestFactory:
    """Test factory functions."""
    
    def test_get_pattern(self, mock_client):
        """Test getting patterns by name."""
        # Test valid patterns
        pattern = get_pattern("chain_of_thought", mock_client)
        assert isinstance(pattern, ChainOfThoughtPattern)
        
        pattern = get_pattern("reflexion", mock_client)
        assert isinstance(pattern, ReflexionPattern)
        
        pattern = get_pattern("tree_of_thoughts", mock_client)
        assert isinstance(pattern, TreeOfThoughtsPattern)
        
        pattern = get_pattern("multi_agent_debate", mock_client)
        assert isinstance(pattern, MultiAgentDebatePattern)
        
        pattern = get_pattern("tool_use", mock_client)
        assert isinstance(pattern, ToolUsePattern)
    
    def test_get_pattern_invalid(self, mock_client):
        """Test getting invalid pattern."""
        with pytest.raises(ValueError, match="Pattern.*not found"):
            get_pattern("invalid_pattern", mock_client)
    
    def test_list_patterns(self):
        """Test listing available patterns."""
        patterns = list_patterns()
        
        assert "chain_of_thought" in patterns
        assert "reflexion" in patterns
        assert "tree_of_thoughts" in patterns
        assert "multi_agent_debate" in patterns
        assert "tool_use" in patterns
        
        # Check descriptions
        for name, description in patterns.items():
            assert isinstance(description, str)
            assert len(description) > 0
    
    def test_register_custom_pattern(self, mock_client):
        """Test registering custom patterns."""
        class CustomPattern(BasePattern):
            async def execute(self, prompt: str):
                response = await self._call_llm(prompt)
                cost = self._estimate_cost(prompt, response)
                return {
                    "response": response,
                    "cost": cost,
                    "pattern_name": self.get_pattern_name(),
                    "metadata": {}
                }
        
        # Register custom pattern
        register_pattern("custom", CustomPattern, aliases=["my_custom"])
        
        # Test getting by primary name
        pattern = get_pattern("custom", mock_client)
        assert isinstance(pattern, CustomPattern)
        
        # Test getting by alias
        pattern = get_pattern("my_custom", mock_client)
        assert isinstance(pattern, CustomPattern)
    
    def test_register_invalid_pattern(self):
        """Test registering invalid pattern class."""
        class InvalidPattern:
            pass
        
        with pytest.raises(ValueError, match="must inherit from BasePattern"):
            register_pattern("invalid", InvalidPattern)


class TestClients:
    """Test LLM client implementations."""
    
    def test_create_mock_client(self):
        """Test creating mock client."""
        client = create_client("mock")
        assert client is not None
    
    def test_create_invalid_client(self):
        """Test creating invalid client."""
        with pytest.raises(ValueError, match="Unknown provider"):
            create_client("invalid_provider")
    
    @pytest.mark.asyncio
    async def test_mock_client_generate(self):
        """Test mock client generation."""
        client = create_client("mock")
        response = await client.generate("Test prompt")
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_mock_client_cost_estimation(self):
        """Test mock client cost estimation."""
        client = create_client("mock")
        cost = client.estimate_cost("Test prompt", "Test response")
        
        assert isinstance(cost, float)
        assert cost >= 0


class TestIntegration:
    """Integration tests."""
    
    @pytest.mark.asyncio
    async def test_pattern_switching(self, mock_client):
        """Test switching between patterns."""
        prompt = "Explain machine learning"
        patterns = ["chain_of_thought", "reflexion", "multi_agent_debate"]
        
        results = {}
        for pattern_name in patterns:
            pattern = get_pattern(pattern_name, mock_client)
            result = await pattern.execute(prompt)
            results[pattern_name] = result
        
        # All patterns should return valid results
        for pattern_name, result in results.items():
            assert result.response is not None
            assert result.success is True
            assert result.cost >= 0
    
    @pytest.mark.asyncio
    async def test_cost_comparison(self, mock_client):
        """Test cost comparison across patterns."""
        prompt = "What is Python?"
        patterns = ["chain_of_thought", "reflexion", "tree_of_thoughts"]
        
        costs = {}
        for pattern_name in patterns:
            pattern = get_pattern(pattern_name, mock_client)
            result = await pattern.execute(prompt)
            costs[pattern_name] = result.cost
        
        # All patterns should have costs
        for pattern_name, cost in costs.items():
            assert cost >= 0
            assert isinstance(cost, float)


if __name__ == "__main__":
    pytest.main([__file__]) 