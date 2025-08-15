"""
Basic usage example for agentic-patterns library.
"""

import asyncio
import os
from agentic_patterns import get_pattern, list_patterns, create_client


async def main():
    """Demonstrate basic usage of the agentic patterns library."""
    
    # Create a mock client for demonstration (no API keys needed)
    llm_client = create_client("mock")
    
    # List available patterns
    print("Available patterns:")
    for name, description in list_patterns().items():
        print(f"  - {name}: {description}")
    print()
    
    # Example prompt
    prompt = "Explain how machine learning can be used to predict stock prices."
    
    # Try different patterns
    patterns_to_try = ["chain_of_thought", "reflexion", "multi_agent_debate"]
    
    for pattern_name in patterns_to_try:
        print(f"\n{'='*60}")
        print(f"Using {pattern_name.upper()} pattern:")
        print(f"{'='*60}")
        
        try:
            # Get pattern instance
            pattern = get_pattern(pattern_name, llm_client)
            
            # Execute pattern
            result = await pattern.execute(prompt)
            
            # Display results
            print(f"Response: {result.response}")
            print(f"Cost: ${result.cost:.4f}")
            print(f"Success: {result.success}")
            
            if result.metadata:
                print(f"Metadata: {result.metadata}")
                
        except Exception as e:
            print(f"Error with {pattern_name}: {e}")
    
    print(f"\n{'='*60}")
    print("Example completed!")


if __name__ == "__main__":
    asyncio.run(main()) 