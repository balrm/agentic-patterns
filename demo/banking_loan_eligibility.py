#!/usr/bin/env python3
"""
Banking Example: Loan Eligibility Assessment
Demonstrates different patterns on the same problem with real banking logic
"""

import asyncio
import os
from dotenv import load_dotenv
from agentic_patterns import get_pattern, create_client, list_patterns

# Load environment variables
load_dotenv()

# Common problem for all patterns
LOAN_PROBLEM = """
Customer Profile:
- Monthly income: $8,000
- Monthly rent: $2,500
- Other monthly expenses: $1,200
- Existing loan payments: $500
- Credit score: 720
- Employment: 5 years at current job
- Down payment: $60,000 (20% of loan amount)
- Loan amount: $300,000
- Interest rate: 7%
- Loan term: 30 years

Question: Can this customer qualify for a $300,000 mortgage loan at 7% interest rate? 
Please provide a detailed analysis including:
1. Debt-to-Income (DTI) ratio calculation
2. Credit score assessment
3. Employment stability evaluation
4. Down payment adequacy
5. Final approval recommendation with reasoning
"""

async def demo_chain_of_thought():
    """Simple step-by-step reasoning"""
    print("\n=== Chain of Thought Pattern ===")
    print("Approach: Linear step-by-step analysis")
    
    client = create_client("google", api_key=os.getenv("GEMINI_API_KEY"))
    pattern = get_pattern("chain_of_thought", client)
    result = await pattern.execute(LOAN_PROBLEM)
    
    print(f"Response: {result.response[:300]}...")
    print(f"Cost: ${result.cost:.4f}")
    print(f"Steps found: {len(result.metadata.get('reasoning_steps', []))}")
    print(f"Success: {result.success}")
    
    return {
        'pattern': 'chain_of_thought',
        'cost': result.cost,
        'decision': 'Approved' if 'approve' in result.response.lower() else 'Denied',
        'confidence': 'High' if result.success else 'Low',
        'response_length': len(result.response)
    }

async def demo_reflexion():
    """Iterative improvement with self-correction"""
    print("\n=== Reflexion Pattern ===")
    print("Approach: Iterative improvement with self-evaluation")
    
    client = create_client("google", api_key=os.getenv("GEMINI_API_KEY"))
    pattern = get_pattern("reflexion", client, max_iterations=3)
    result = await pattern.execute(LOAN_PROBLEM)
    
    print(f"Iterations needed: {len(result.metadata.get('iterations', []))}")
    if result.metadata.get('iterations'):
        for i, iteration in enumerate(result.metadata['iterations']):
            score = iteration.get('evaluation', {}).get('score', 'N/A')
            print(f"  Iteration {i+1}: Score {score}/10")
    
    print(f"Final response: {result.response[:200]}...")
    print(f"Cost: ${result.cost:.4f}")
    print(f"Success: {result.success}")
    
    return {
        'pattern': 'reflexion',
        'cost': result.cost,
        'decision': 'Approved' if 'approve' in result.response.lower() else 'Denied',
        'confidence': 'High' if result.success else 'Low',
        'iterations': len(result.metadata.get('iterations', [])),
        'response_length': len(result.response)
    }

async def demo_tree_of_thoughts():
    """Explore multiple evaluation paths"""
    print("\n=== Tree of Thoughts Pattern ===")
    print("Approach: Explore multiple evaluation paths")
    
    client = create_client("google", api_key=os.getenv("GEMINI_API_KEY"))
    pattern = get_pattern("tree_of_thoughts", client, max_depth=2, thoughts_per_level=3)
    result = await pattern.execute(LOAN_PROBLEM)
    
    print(f"Paths explored: {result.metadata.get('total_thoughts', 0)}")
    print(f"Best path length: {len(result.metadata.get('best_path', []))}")
    print(f"Final response: {result.response[:200]}...")
    print(f"Cost: ${result.cost:.4f}")
    print(f"Success: {result.success}")
    
    return {
        'pattern': 'tree_of_thoughts',
        'cost': result.cost,
        'decision': 'Approved' if 'approve' in result.response.lower() else 'Denied',
        'confidence': 'High' if result.success else 'Low',
        'paths_explored': result.metadata.get('total_thoughts', 0),
        'response_length': len(result.response)
    }

async def demo_multi_agent_debate():
    """Multiple perspectives on loan decision"""
    print("\n=== Multi-Agent Debate Pattern ===")
    print("Approach: Multiple specialist perspectives")
    
    client = create_client("google", api_key=os.getenv("GEMINI_API_KEY"))
    pattern = get_pattern("multi_agent_debate", client, num_agents=3)
    result = await pattern.execute(LOAN_PROBLEM)
    
    print("Agent Perspectives:")
    for debate_entry in result.metadata.get('debate', []):
        agent_name = debate_entry.get('agent', 'Unknown')
        response = debate_entry.get('response', '')[:100]
        print(f"  {agent_name}: {response}...")
    
    print(f"Final consensus: {result.response[:200]}...")
    print(f"Cost: ${result.cost:.4f}")
    print(f"Success: {result.success}")
    
    return {
        'pattern': 'multi_agent_debate',
        'cost': result.cost,
        'decision': 'Approved' if 'approve' in result.response.lower() else 'Denied',
        'confidence': 'High' if result.success else 'Low',
        'agents_consulted': len(result.metadata.get('debate', [])),
        'response_length': len(result.response)
    }

async def demo_tool_use():
    """Using calculation tools for precise analysis"""
    print("\n=== Tool-Use Pattern ===")
    print("Approach: Use calculation tools for precise analysis")
    
    client = create_client("google", api_key=os.getenv("GEMINI_API_KEY"))
    pattern = get_pattern("tool_use", client)
    result = await pattern.execute(LOAN_PROBLEM)
    
    print(f"Tools used: {result.metadata.get('tools_used', 0)}")
    if result.metadata.get('tool_results'):
        for tool_result in result.metadata['tool_results']:
            if tool_result.get('success'):
                print(f"  {tool_result['tool']}: {tool_result['result']}")
    
    print(f"Final decision: {result.response[:200]}...")
    print(f"Cost: ${result.cost:.4f}")
    print(f"Success: {result.success}")
    
    return {
        'pattern': 'tool_use',
        'cost': result.cost,
        'decision': 'Approved' if 'approve' in result.response.lower() else 'Denied',
        'confidence': 'High' if result.success else 'Low',
        'tools_used': result.metadata.get('tools_used', 0),
        'response_length': len(result.response)
    }

async def compare_all_patterns():
    """Run all patterns and compare results"""
    print("\n" + "="*80)
    print("PATTERN COMPARISON: LOAN ELIGIBILITY ASSESSMENT")
    print("="*80)
    print(f"Problem: {LOAN_PROBLEM[:100]}...\n")
    
    patterns = [
        demo_chain_of_thought,
        demo_reflexion,
        demo_tree_of_thoughts,
        demo_multi_agent_debate,
        demo_tool_use
    ]
    
    results = []
    for pattern_func in patterns:
        try:
            result = await pattern_func()
            results.append(result)
        except Exception as e:
            print(f"Error with {pattern_func.__name__}: {e}")
            results.append({
                'pattern': pattern_func.__name__.replace('demo_', ''),
                'cost': 0.0,
                'decision': 'Error',
                'confidence': 'Low',
                'response_length': 0
            })
    
    # Display comparison table
    print(f"{'Pattern':<20} {'Cost':<10} {'Decision':<10} {'Confidence':<10} {'Response Length':<15}")
    print("-" * 75)
    for r in results:
        pattern_name = r['pattern'].replace('_', ' ').title()
        print(f"{pattern_name:<20} ${r['cost']:<9.4f} {r['decision']:<10} {r['confidence']:<10} {r['response_length']:<15}")
    
    # Summary statistics
    total_cost = sum(r['cost'] for r in results)
    approved_count = sum(1 for r in results if r['decision'] == 'Approved')
    
    print(f"\nSummary:")
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Approval rate: {approved_count}/{len(results)} patterns")
    print(f"Most expensive: {max(results, key=lambda x: x['cost'])['pattern']}")
    print(f"Least expensive: {min(results, key=lambda x: x['cost'])['pattern']}")

async def main():
    """Run all demos"""
    print("🏦 BANKING LOAN ELIGIBILITY DEMO")
    print("="*50)
    print("Testing all patterns on the same loan approval problem")
    print("Using Google Gemini API for realistic banking analysis")
    
    # Run individual demos
    await demo_chain_of_thought()
    await demo_reflexion()
    await demo_tree_of_thoughts()
    await demo_multi_agent_debate()
    await demo_tool_use()
    
    # Compare all patterns
    await compare_all_patterns()
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(main()) 