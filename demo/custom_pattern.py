"""
Example of creating and registering custom patterns.
"""

import asyncio
from agentic_patterns import BasePattern, register_pattern, get_pattern, create_client


class CustomPromptingPattern(BasePattern):
    """Custom pattern that uses a specific prompting technique."""
    
    def __init__(self, llm_client, template: str = "Let's approach this systematically:", **kwargs):
        super().__init__(llm_client, **kwargs)
        self.template = template
    
    async def execute(self, prompt: str):
        # Apply custom template
        custom_prompt = f"{self.template}\n\n{prompt}"
        
        # Generate response
        response = await self._call_llm(custom_prompt)
        cost = self._estimate_cost(custom_prompt, response)
        
        return {
            "response": response,
            "cost": cost,
            "pattern_name": self.get_pattern_name(),
            "metadata": {
                "template": self.template,
                "original_prompt": prompt,
                "custom_prompt": custom_prompt
            }
        }


class MultiStepPattern(BasePattern):
    """Custom pattern that breaks down complex tasks into steps."""
    
    def __init__(self, llm_client, num_steps: int = 3, **kwargs):
        super().__init__(llm_client, **kwargs)
        self.num_steps = num_steps
    
    async def execute(self, prompt: str):
        total_cost = 0.0
        steps = []
        
        # Step 1: Break down the problem
        breakdown_prompt = f"""
        Break down this problem into {self.num_steps} clear steps:
        {prompt}
        
        Provide only the step titles, one per line:
        """
        
        breakdown_response = await self._call_llm(breakdown_prompt)
        total_cost += self._estimate_cost(breakdown_prompt, breakdown_response)
        
        # Extract step titles
        step_titles = [line.strip() for line in breakdown_response.split('\n') 
                      if line.strip() and not line.startswith(('#', '-', '*'))]
        step_titles = step_titles[:self.num_steps]
        
        # Execute each step
        for i, step_title in enumerate(step_titles, 1):
            step_prompt = f"""
            Step {i}: {step_title}
            
            Original problem: {prompt}
            
            Provide a detailed solution for this step:
            """
            
            step_response = await self._call_llm(step_prompt)
            total_cost += self._estimate_cost(step_prompt, step_response)
            
            steps.append({
                "step": i,
                "title": step_title,
                "response": step_response
            })
        
        # Synthesize final response
        synthesis_prompt = f"""
        Original problem: {prompt}
        
        Steps completed:
        {chr(10).join(f"{step['step']}. {step['title']}: {step['response'][:200]}..." for step in steps)}
        
        Provide a comprehensive final answer that synthesizes all the steps:
        """
        
        final_response = await self._call_llm(synthesis_prompt)
        total_cost += self._estimate_cost(synthesis_prompt, final_response)
        
        return {
            "response": final_response,
            "cost": total_cost,
            "pattern_name": self.get_pattern_name(),
            "metadata": {
                "num_steps": self.num_steps,
                "steps": steps,
                "breakdown": breakdown_response
            }
        }


async def main():
    """Demonstrate custom pattern creation and usage."""
    
    # Create mock client
    llm_client = create_client("mock")
    
    # Register custom patterns
    register_pattern("custom_prompt", CustomPromptingPattern, aliases=["cp"])
    register_pattern("multi_step", MultiStepPattern, aliases=["ms"])
    
    # Test custom patterns
    prompt = "How can we improve customer satisfaction in an e-commerce platform?"
    
    print("Testing Custom Patterns")
    print("=" * 50)
    
    # Test custom prompting pattern
    print("\n1. Custom Prompting Pattern:")
    custom_pattern = get_pattern("custom_prompt", llm_client, 
                               template="Let's think about this from a business perspective:")
    result = await custom_pattern.execute(prompt)
    print(f"Response: {result['response'][:200]}...")
    print(f"Cost: ${result['cost']:.4f}")
    
    # Test multi-step pattern
    print("\n2. Multi-Step Pattern:")
    multi_step_pattern = get_pattern("multi_step", llm_client, num_steps=4)
    result = await multi_step_pattern.execute(prompt)
    print(f"Response: {result['response'][:200]}...")
    print(f"Cost: ${result['cost']:.4f}")
    print(f"Steps completed: {len(result['metadata']['steps'])}")
    
    # Show pattern info
    print("\n3. Pattern Information:")
    from agentic_patterns import get_pattern_info
    for pattern_name in ["custom_prompt", "multi_step"]:
        info = get_pattern_info(pattern_name)
        if info:
            print(f"{pattern_name}: {info['description']}")


if __name__ == "__main__":
    asyncio.run(main()) 