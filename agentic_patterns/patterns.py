"""
Implementation of various AI agent design patterns.
"""

import asyncio
import re
from typing import Any, Dict, List, Optional, Tuple
from .base import BasePattern, PatternResult, LLMClient


class ChainOfThoughtPattern(BasePattern):
    """Chain-of-Thought pattern that encourages step-by-step reasoning."""
    
    async def execute(self, prompt: str) -> PatternResult:
        try:
            # Add the CoT instruction to the prompt
            cot_prompt = f"{prompt}\n\nLet's think step by step:"
            
            # Generate response with step-by-step reasoning
            response = await self._call_llm(cot_prompt)
            cost = self._estimate_cost(cot_prompt, response)
            
            return PatternResult(
                response=response,
                cost=cost,
                pattern_name=self.get_pattern_name(),
                metadata={
                    "original_prompt": prompt,
                    "cot_prompt": cot_prompt,
                    "reasoning_steps": self._extract_reasoning_steps(response)
                }
            )
        except Exception as e:
            return PatternResult(
                response="",
                cost=0.0,
                pattern_name=self.get_pattern_name(),
                success=False,
                error_message=str(e),
                metadata={"original_prompt": prompt}
            )
    
    def _extract_reasoning_steps(self, response: str) -> List[str]:
        """Extract individual reasoning steps from the response."""
        # Simple extraction - look for numbered or bulleted items
        steps = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.|^[-*]\s|^Step\s', line):
                steps.append(line)
        return steps


class ReflexionPattern(BasePattern):
    """Reflexion pattern that iteratively improves responses through self-reflection."""
    
    def __init__(self, llm_client: LLMClient, max_iterations: int = 3, **kwargs):
        super().__init__(llm_client, **kwargs)
        self.max_iterations = max_iterations
        self.learnings = []
    
    async def execute(self, prompt: str) -> PatternResult:
        try:
            current_prompt = prompt
            total_cost = 0.0
            iterations = []
            
            for attempt in range(self.max_iterations):
                # Generate response
                response = await self._call_llm(current_prompt)
                cost = self._estimate_cost(current_prompt, response)
                total_cost += cost
                
                # Evaluate response quality
                evaluation = await self._evaluate_response(prompt, response)
                
                iterations.append({
                    "attempt": attempt + 1,
                    "response": response,
                    "evaluation": evaluation,
                    "cost": cost
                })
                
                # If response is good enough, return it
                if evaluation["score"] >= 7:
                    return PatternResult(
                        response=response,
                        cost=total_cost,
                        pattern_name=self.get_pattern_name(),
                        metadata={
                            "iterations": iterations,
                            "final_score": evaluation["score"],
                            "learnings": self.learnings
                        }
                    )
                
                # Generate reflection for improvement
                reflection = await self._generate_reflection(prompt, response, evaluation)
                current_prompt = f"{prompt}\n\nPrevious attempt: {response}\n\nWhat went wrong: {reflection}\n\nPlease try again:"
            
            # Return the best response from all attempts
            if iterations:
                best_iteration = max(iterations, key=lambda x: x["evaluation"]["score"])
                return PatternResult(
                    response=best_iteration["response"],
                    cost=total_cost,
                    pattern_name=self.get_pattern_name(),
                    metadata={
                        "iterations": iterations,
                        "best_score": best_iteration["evaluation"]["score"],
                        "learnings": self.learnings
                    }
                )
            else:
                return PatternResult(
                    response="",
                    cost=total_cost,
                    pattern_name=self.get_pattern_name(),
                    success=False,
                    error_message="No iterations completed",
                    metadata={"iterations": iterations, "learnings": self.learnings}
                )
        except Exception as e:
            return PatternResult(
                response="",
                cost=0.0,
                pattern_name=self.get_pattern_name(),
                success=False,
                error_message=str(e),
                metadata={"original_prompt": prompt}
            )
    
    async def _evaluate_response(self, original_prompt: str, response: str) -> Dict[str, Any]:
        """Evaluate the quality of a response."""
        evaluation_prompt = f"""
        Evaluate this response to the prompt: "{original_prompt}"
        
        Response: {response}
        
        Rate the response on a scale of 1-10 and provide brief feedback:
        - Relevance to the prompt
        - Completeness of the answer
        - Clarity and coherence
        """
        
        eval_response = await self._call_llm(evaluation_prompt)
        
        # Extract score from response
        score_match = re.search(r'(\d+)/10|score[:\s]*(\d+)', eval_response.lower())
        score = int(score_match.group(1) or score_match.group(2)) if score_match else 5
        
        return {
            "score": score,
            "feedback": eval_response,
            "raw_evaluation": eval_response
        }
    
    async def _generate_reflection(self, original_prompt: str, response: str, evaluation: Dict[str, Any]) -> str:
        """Generate reflection on what went wrong."""
        reflection_prompt = f"""
        The original prompt was: "{original_prompt}"
        
        The response was: "{response}"
        
        The evaluation feedback was: "{evaluation['feedback']}"
        
        Based on this, what specifically went wrong and how should the response be improved? Be specific and actionable.
        """
        
        reflection = await self._call_llm(reflection_prompt)
        self.learnings.append({
            "prompt": original_prompt,
            "response": response,
            "evaluation": evaluation,
            "reflection": reflection
        })
        
        return reflection


class TreeOfThoughtsPattern(BasePattern):
    """Tree of Thoughts pattern that explores multiple reasoning paths."""
    
    def __init__(self, llm_client: LLMClient, max_depth: int = 3, thoughts_per_level: int = 3, **kwargs):
        super().__init__(llm_client, **kwargs)
        self.max_depth = max_depth
        self.thoughts_per_level = thoughts_per_level
    
    async def execute(self, prompt: str) -> PatternResult:
        try:
            total_cost = 0.0
            tree = {"thoughts": [], "best_path": None, "best_score": 0}
            
            # Generate initial thoughts
            initial_thoughts = await self._generate_thoughts(prompt, level=0)
            if not initial_thoughts:
                return PatternResult(
                    response="",
                    cost=0.0,
                    pattern_name=self.get_pattern_name(),
                    success=False,
                    error_message="Failed to generate initial thoughts",
                    metadata={"original_prompt": prompt}
                )
            
            cost = sum(self._estimate_cost(prompt, thought) for thought in initial_thoughts)
            total_cost += cost
            
            tree["thoughts"].extend([
                {"content": thought, "level": 0, "score": 0, "parent": None}
                for thought in initial_thoughts
            ])
            
            # Evaluate initial thoughts
            for i, thought in enumerate(initial_thoughts):
                score = await self._evaluate_thought(prompt, thought)
                tree["thoughts"][i]["score"] = score
                total_cost += self._estimate_cost(prompt, f"Evaluation: {score}")
            
            # Expand best thoughts for deeper levels
            for level in range(1, self.max_depth):
                best_thoughts = sorted(
                    [t for t in tree["thoughts"] if t["level"] == level - 1],
                    key=lambda x: x["score"],
                    reverse=True
                )[:2]  # Take top 2 thoughts
                
                for parent_thought in best_thoughts:
                    sub_thoughts = await self._generate_thoughts(
                        prompt, 
                        level=level, 
                        parent_thought=parent_thought["content"]
                    )
                    
                    cost = sum(self._estimate_cost(prompt, thought) for thought in sub_thoughts)
                    total_cost += cost
                    
                    for sub_thought in sub_thoughts:
                        score = await self._evaluate_thought(prompt, sub_thought)
                        tree["thoughts"].append({
                            "content": sub_thought,
                            "level": level,
                            "score": score,
                            "parent": parent_thought["content"]
                        })
                        total_cost += self._estimate_cost(prompt, f"Evaluation: {score}")
            
            # Find best path through the tree
            best_path = self._find_best_path(tree)
            if not best_path:
                return PatternResult(
                    response="",
                    cost=total_cost,
                    pattern_name=self.get_pattern_name(),
                    success=False,
                    error_message="No valid path found in tree",
                    metadata={"tree": tree, "total_thoughts": len(tree["thoughts"])}
                )
            
            final_response = await self._synthesize_final_response(prompt, best_path)
            total_cost += self._estimate_cost(prompt, final_response)
            
            return PatternResult(
                response=final_response,
                cost=total_cost,
                pattern_name=self.get_pattern_name(),
                metadata={
                    "tree": tree,
                    "best_path": best_path,
                    "total_thoughts": len(tree["thoughts"])
                }
            )
        except Exception as e:
            return PatternResult(
                response="",
                cost=0.0,
                pattern_name=self.get_pattern_name(),
                success=False,
                error_message=str(e),
                metadata={"original_prompt": prompt}
            )
    
    async def _generate_thoughts(self, prompt: str, level: int, parent_thought: Optional[str] = None) -> List[str]:
        """Generate thoughts for a given level."""
        if level == 0:
            thought_prompt = f"""
            For the prompt: "{prompt}"
            
            Generate {self.thoughts_per_level} different initial approaches or thoughts to solve this problem.
            Each thought should be a distinct strategy or perspective.
            """
        else:
            thought_prompt = f"""
            For the prompt: "{prompt}"
            
            Previous thought: "{parent_thought}"
            
            Generate {self.thoughts_per_level} different ways to expand or refine this thought.
            Each should be a specific next step or consideration.
            """
        
        response = await self._call_llm(thought_prompt)
        
        # Split response into individual thoughts
        thoughts = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('#', '-', '*', '1.', '2.', '3.')):
                thoughts.append(line)
        
        return thoughts[:self.thoughts_per_level]
    
    async def _evaluate_thought(self, prompt: str, thought: str) -> float:
        """Evaluate the promise of a thought (1-10 scale)."""
        eval_prompt = f"""
        For the prompt: "{prompt}"
        
        Evaluate this thought: "{thought}"
        
        Rate how promising this thought is for solving the problem (1-10):
        - 1-3: Poor approach
        - 4-6: Moderate potential
        - 7-8: Good approach
        - 9-10: Excellent approach
        
        Provide only the number rating:
        """
        
        response = await self._call_llm(eval_prompt)
        
        # Extract score
        score_match = re.search(r'(\d+)', response)
        return float(score_match.group(1)) if score_match else 5.0
    
    def _find_best_path(self, tree: Dict[str, Any]) -> List[str]:
        """Find the best path through the thought tree."""
        # Find the thought with the highest score at the deepest level
        max_level = max(t["level"] for t in tree["thoughts"])
        best_thoughts = [t for t in tree["thoughts"] if t["level"] == max_level]
        
        if not best_thoughts:
            return []
        
        best_thought = max(best_thoughts, key=lambda x: x["score"])
        
        # Trace back to root
        path = [best_thought["content"]]
        current = best_thought
        
        while current["parent"]:
            parent = next(t for t in tree["thoughts"] if t["content"] == current["parent"])
            path.insert(0, parent["content"])
            current = parent
        
        return path
    
    async def _synthesize_final_response(self, prompt: str, best_path: List[str]) -> str:
        """Synthesize the final response from the best path."""
        synthesis_prompt = f"""
        For the prompt: "{prompt}"
        
        Here is the best reasoning path found:
        {chr(10).join(f"{i+1}. {thought}" for i, thought in enumerate(best_path))}
        
        Synthesize these thoughts into a comprehensive, well-structured final answer.
        """
        
        return await self._call_llm(synthesis_prompt)


class MultiAgentDebatePattern(BasePattern):
    """Multi-Agent Debate pattern with different perspectives."""
    
    def __init__(self, llm_client: LLMClient, num_agents: int = 3, **kwargs):
        super().__init__(llm_client, **kwargs)
        self.num_agents = num_agents
        self.agent_personas = [
            "Optimistic and solution-focused",
            "Critical and risk-aware", 
            "Analytical and evidence-based"
        ]
    
    async def execute(self, prompt: str) -> PatternResult:
        try:
            total_cost = 0.0
            debate = []
            
            # Agent 1: Initial answer
            agent1_prompt = f"""
            You are an AI agent with an optimistic and solution-focused perspective.
            
            Question: {prompt}
            
            Provide a comprehensive initial answer from your perspective:
            """
            
            agent1_response = await self._call_llm(agent1_prompt)
            cost = self._estimate_cost(agent1_prompt, agent1_response)
            total_cost += cost
            
            debate.append({
                "agent": "Agent 1 (Optimistic)",
                "response": agent1_response,
                "cost": cost
            })
            
            # Agent 2: Critique and alternative
            agent2_prompt = f"""
            You are an AI agent with a critical and risk-aware perspective.
            
            Question: {prompt}
            
            Previous response: {agent1_response}
            
            Critique the previous response and provide an alternative perspective:
            """
            
            agent2_response = await self._call_llm(agent2_prompt)
            cost = self._estimate_cost(agent2_prompt, agent2_response)
            total_cost += cost
            
            debate.append({
                "agent": "Agent 2 (Critical)",
                "response": agent2_response,
                "cost": cost
            })
            
            # Agent 3: Synthesis or third view
            agent3_prompt = f"""
            You are an AI agent with an analytical and evidence-based perspective.
            
            Question: {prompt}
            
            Agent 1 (Optimistic): {agent1_response}
            Agent 2 (Critical): {agent2_response}
            
            Provide a synthesis of these perspectives or offer a third analytical view:
            """
            
            agent3_response = await self._call_llm(agent3_prompt)
            cost = self._estimate_cost(agent3_prompt, agent3_response)
            total_cost += cost
            
            debate.append({
                "agent": "Agent 3 (Analytical)",
                "response": agent3_response,
                "cost": cost
            })
            
            # Optional: Judge agent to pick best answer
            judge_prompt = f"""
            You are a judge evaluating different perspectives on this question: {prompt}
            
            Perspectives:
            1. Optimistic: {agent1_response}
            2. Critical: {agent2_response}
            3. Analytical: {agent3_response}
            
            Synthesize the best elements from all perspectives into a comprehensive final answer.
            Acknowledge the strengths of each perspective while providing a balanced conclusion.
            """
            
            final_response = await self._call_llm(judge_prompt)
            cost = self._estimate_cost(judge_prompt, final_response)
            total_cost += cost
            
            return PatternResult(
                response=final_response,
                cost=total_cost,
                pattern_name=self.get_pattern_name(),
                metadata={
                    "debate": debate,
                    "num_agents": self.num_agents,
                    "agent_personas": self.agent_personas
                }
            )
        except Exception as e:
            return PatternResult(
                response="",
                cost=0.0,
                pattern_name=self.get_pattern_name(),
                success=False,
                error_message=str(e),
                metadata={"original_prompt": prompt}
            )


class ToolUsePattern(BasePattern):
    """Tool-Use pattern that detects and executes external tools."""
    
    def __init__(self, llm_client: LLMClient, available_tools: Optional[Dict[str, callable]] = None, **kwargs):
        super().__init__(llm_client, **kwargs)
        self.available_tools = available_tools or self._get_default_tools()
    
    async def execute(self, prompt: str) -> PatternResult:
        try:
            total_cost = 0.0
            tool_results = []
            
            # Analyze prompt for tool usage
            tool_analysis = await self._analyze_tool_usage(prompt)
            cost = self._estimate_cost(prompt, str(tool_analysis))
            total_cost += cost
            
            # Execute tools if needed
            if tool_analysis["needs_tools"]:
                for tool_call in tool_analysis["tool_calls"]:
                    try:
                        result = await self._execute_tool(tool_call)
                        tool_results.append({
                            "tool": tool_call["tool"],
                            "args": tool_call["args"],
                            "result": result,
                            "success": True
                        })
                    except Exception as e:
                        tool_results.append({
                            "tool": tool_call["tool"],
                            "args": tool_call["args"],
                            "result": str(e),
                            "success": False
                        })
            
            # Generate final response with tool results
            final_prompt = self._build_final_prompt(prompt, tool_results)
            final_response = await self._call_llm(final_prompt)
            cost = self._estimate_cost(final_prompt, final_response)
            total_cost += cost
            
            return PatternResult(
                response=final_response,
                cost=total_cost,
                pattern_name=self.get_pattern_name(),
                metadata={
                    "tool_analysis": tool_analysis,
                    "tool_results": tool_results,
                    "tools_used": len([r for r in tool_results if r["success"]])
                }
            )
        except Exception as e:
            return PatternResult(
                response="",
                cost=0.0,
                pattern_name=self.get_pattern_name(),
                success=False,
                error_message=str(e),
                metadata={"original_prompt": prompt}
            )
    
    async def _analyze_tool_usage(self, prompt: str) -> Dict[str, Any]:
        """Analyze if the prompt requires external tools."""
        analysis_prompt = f"""
        Analyze this prompt to determine if it requires external tools: "{prompt}"
        
        Available tools: {list(self.available_tools.keys())}
        
        If tools are needed, specify which ones and with what arguments.
        Format tool calls as: tool_name(arg1, arg2, ...)
        
        Respond with JSON:
        {{
            "needs_tools": true/false,
            "tool_calls": [
                {{"tool": "tool_name", "args": ["arg1", "arg2"]}}
            ]
        }}
        """
        
        response = await self._call_llm(analysis_prompt)
        
        # Simple parsing - in production, use proper JSON parsing
        needs_tools = "needs_tools" in response.lower() and "true" in response.lower()
        
        # Extract tool calls using regex
        tool_calls = []
        tool_pattern = r'(\w+)\(([^)]+)\)'
        matches = re.findall(tool_pattern, response)
        
        for tool_name, args_str in matches:
            if tool_name in self.available_tools:
                args = [arg.strip().strip('"\'') for arg in args_str.split(',')]
                tool_calls.append({
                    "tool": tool_name,
                    "args": args
                })
        
        return {
            "needs_tools": needs_tools,
            "tool_calls": tool_calls
        }
    
    async def _execute_tool(self, tool_call: Dict[str, Any]) -> Any:
        """Execute a tool with the given arguments."""
        tool_name = tool_call["tool"]
        args = tool_call["args"]
        
        if tool_name not in self.available_tools:
            raise ValueError(f"Tool '{tool_name}' not available")
        
        tool_func = self.available_tools[tool_name]
        
        # Handle async vs sync tools
        if asyncio.iscoroutinefunction(tool_func):
            return await tool_func(*args)
        else:
            return tool_func(*args)
    
    def _build_final_prompt(self, original_prompt: str, tool_results: List[Dict[str, Any]]) -> str:
        """Build the final prompt including tool results."""
        if not tool_results:
            return original_prompt
        
        tool_info = "\n\nTool Results:\n"
        for result in tool_results:
            tool_info += f"- {result['tool']}({', '.join(result['args'])}): {result['result']}\n"
        
        return f"{original_prompt}{tool_info}\n\nPlease provide a comprehensive answer using the tool results above."
    
    def _get_default_tools(self) -> Dict[str, callable]:
        """Get default available tools."""
        import math
        import datetime
        
        return {
            "calculate": lambda expr: eval(expr),  # Simple calculator
            "sqrt": math.sqrt,
            "log": math.log,
            "current_time": lambda: datetime.datetime.now().isoformat(),
            "len": len,
            "sum": sum,
            "max": max,
            "min": min,
        } 