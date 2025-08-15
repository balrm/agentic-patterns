#!/usr/bin/env python3
"""
Banking Example: Investment Portfolio Optimization
Demonstrates complex constraint handling and optimization strategies
"""

import asyncio
import os
from dotenv import load_dotenv
from agentic_patterns import get_pattern, create_client

# Load environment variables
load_dotenv()

# Portfolio optimization scenarios
PORTFOLIO_SCENARIOS = {
    "retirement_planning": """
Client Portfolio Optimization Request - Retirement Planning:
- Client: 45-year-old professional
- Total investment: $500,000
- Risk tolerance: Moderate
- Time horizon: 20 years to retirement
- Requirements:
  * Minimum 5% annual income generation
  * ESG compliant investments only
  * Maximum 30% international exposure
  * Tax-efficient (client in 32% tax bracket)
  * Inflation protection
- Current portfolio: 100% cash
- Additional constraints:
  * No more than 10% in any single stock
  * Minimum 20% in bonds for stability
  * Maximum 40% in growth stocks

Design optimal portfolio allocation with specific asset recommendations.
""",
    
    "income_generation": """
Client Portfolio Optimization Request - Income Generation:
- Client: 65-year-old retiree
- Total investment: $750,000
- Risk tolerance: Conservative
- Primary goal: Generate $3,000/month income
- Requirements:
  * Stable monthly income stream
  * Capital preservation priority
  * Low volatility
  * Tax-efficient income
- Current portfolio: 60% bonds, 40% cash
- Additional constraints:
  * No more than 5% in any single investment
  * Maximum 20% in equities
  * Minimum 50% in investment-grade bonds
  * Prefer dividend-paying stocks

Design income-focused portfolio with specific recommendations.
""",
    
    "growth_optimization": """
Client Portfolio Optimization Request - Growth Optimization:
- Client: 30-year-old tech professional
- Total investment: $200,000
- Risk tolerance: Aggressive
- Time horizon: 30+ years
- Requirements:
  * Maximum long-term growth potential
  * Technology sector focus
  * International diversification
  * ESG considerations
- Current portfolio: 80% tech stocks, 20% cash
- Additional constraints:
  * No more than 25% in any single stock
  * Minimum 20% international exposure
  * Maximum 60% in technology sector
  * Include emerging markets

Design growth-optimized portfolio with specific recommendations.
"""
}

async def optimize_portfolio_with_pattern(pattern_name, scenario_name, scenario_text):
    """Optimize portfolio with a specific pattern"""
    print(f"\n=== {pattern_name.upper()} - {scenario_name.replace('_', ' ').title()} ===")
    
    client = create_client("google", api_key=os.getenv("GEMINI_API_KEY"))
    pattern = get_pattern(pattern_name, client)
    
    result = await pattern.execute(scenario_text)
    
    # Extract optimization indicators
    response_lower = result.response.lower()
    has_allocation = any(word in response_lower for word in ['allocation', 'percentage', '%', 'bonds', 'stocks', 'equity'])
    has_specific_recommendations = any(word in response_lower for word in ['recommend', 'suggest', 'invest in', 'allocate'])
    
    print(f"Allocation provided: {'✅ Yes' if has_allocation else '❌ No'}")
    print(f"Specific recommendations: {'✅ Yes' if has_specific_recommendations else '❌ No'}")
    print(f"Cost: ${result.cost:.4f}")
    print(f"Response: {result.response[:300]}...")
    
    return {
        'pattern': pattern_name,
        'scenario': scenario_name,
        'has_allocation': has_allocation,
        'has_recommendations': has_specific_recommendations,
        'cost': result.cost,
        'response_length': len(result.response),
        'success': result.success
    }

async def demo_chain_of_thought_portfolio():
    """Chain of Thought for systematic portfolio analysis"""
    print("\n📊 CHAIN OF THOUGHT PORTFOLIO OPTIMIZATION")
    print("Approach: Systematic step-by-step portfolio construction")
    
    results = []
    for scenario_name, scenario_text in PORTFOLIO_SCENARIOS.items():
        result = await optimize_portfolio_with_pattern("chain_of_thought", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def demo_reflexion_portfolio():
    """Reflexion for iterative portfolio improvement"""
    print("\n🔄 REFLEXION PORTFOLIO OPTIMIZATION")
    print("Approach: Iterative improvement with constraint validation")
    
    results = []
    for scenario_name, scenario_text in PORTFOLIO_SCENARIOS.items():
        result = await optimize_portfolio_with_pattern("reflexion", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def demo_tree_of_thoughts_portfolio():
    """Tree of Thoughts for exploring multiple portfolio strategies"""
    print("\n🌳 TREE OF THOUGHTS PORTFOLIO OPTIMIZATION")
    print("Approach: Explore multiple portfolio construction paths")
    
    results = []
    for scenario_name, scenario_text in PORTFOLIO_SCENARIOS.items():
        result = await optimize_portfolio_with_pattern("tree_of_thoughts", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def demo_multi_agent_debate_portfolio():
    """Multi-Agent Debate for multiple specialist perspectives"""
    print("\n👥 MULTI-AGENT DEBATE PORTFOLIO OPTIMIZATION")
    print("Approach: Multiple investment specialist perspectives")
    
    results = []
    for scenario_name, scenario_text in PORTFOLIO_SCENARIOS.items():
        result = await optimize_portfolio_with_pattern("multi_agent_debate", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def demo_tool_use_portfolio():
    """Tool-Use for enhanced portfolio optimization with calculation tools"""
    print("\n🛠️ TOOL-USE PORTFOLIO OPTIMIZATION")
    print("Approach: Enhanced optimization with financial calculation tools")
    
    results = []
    for scenario_name, scenario_text in PORTFOLIO_SCENARIOS.items():
        result = await optimize_portfolio_with_pattern("tool_use", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def compare_portfolio_optimization():
    """Compare all patterns on portfolio optimization"""
    print("\n" + "="*80)
    print("PORTFOLIO OPTIMIZATION PATTERN COMPARISON")
    print("="*80)
    
    patterns = [
        ("Chain of Thought", demo_chain_of_thought_portfolio),
        ("Reflexion", demo_reflexion_portfolio),
        ("Tree of Thoughts", demo_tree_of_thoughts_portfolio),
        ("Multi-Agent Debate", demo_multi_agent_debate_portfolio),
        ("Tool-Use", demo_tool_use_portfolio)
    ]
    
    all_results = []
    for pattern_name, pattern_func in patterns:
        try:
            results = await pattern_func()
            all_results.extend(results)
        except Exception as e:
            print(f"Error with {pattern_name}: {e}")
    
    # Analysis by scenario
    scenarios = list(PORTFOLIO_SCENARIOS.keys())
    print(f"\n📊 PORTFOLIO OPTIMIZATION RESULTS BY SCENARIO")
    print("-" * 80)
    
    for scenario in scenarios:
        scenario_results = [r for r in all_results if r['scenario'] == scenario]
        allocation_count = sum(1 for r in scenario_results if r['has_allocation'])
        recommendation_count = sum(1 for r in scenario_results if r['has_recommendations'])
        total_count = len(scenario_results)
        
        print(f"\n{scenario.replace('_', ' ').title()}:")
        print(f"  Allocation provided: {allocation_count}/{total_count} patterns")
        print(f"  Specific recommendations: {recommendation_count}/{total_count} patterns")
        
        for result in scenario_results:
            alloc_status = "✅" if result['has_allocation'] else "❌"
            rec_status = "✅" if result['has_recommendations'] else "❌"
            print(f"    {result['pattern']}: Allocation {alloc_status}, Recs {rec_status} (${result['cost']:.4f})")
    
    # Analysis by pattern
    print(f"\n📈 PATTERN PERFORMANCE SUMMARY")
    print("-" * 80)
    
    pattern_names = list(set(r['pattern'] for r in all_results))
    for pattern in pattern_names:
        pattern_results = [r for r in all_results if r['pattern'] == pattern]
        allocation_rate = sum(1 for r in pattern_results if r['has_allocation']) / len(pattern_results)
        recommendation_rate = sum(1 for r in pattern_results if r['has_recommendations']) / len(pattern_results)
        total_cost = sum(r['cost'] for r in pattern_results)
        success_rate = sum(1 for r in pattern_results if r['success']) / len(pattern_results)
        
        print(f"\n{pattern.replace('_', ' ').title()}:")
        print(f"  Allocation rate: {allocation_rate*100:.1f}%")
        print(f"  Recommendation rate: {recommendation_rate*100:.1f}%")
        print(f"  Success rate: {success_rate*100:.1f}%")
        print(f"  Total cost: ${total_cost:.4f}")
    
    # Best pattern recommendations
    print(f"\n🏆 BEST PATTERN RECOMMENDATIONS")
    print("-" * 80)
    
    # Find best pattern for allocations
    best_allocation = max(pattern_names, key=lambda p: 
        sum(1 for r in all_results if r['pattern'] == p and r['has_allocation']) / 
        sum(1 for r in all_results if r['pattern'] == p))
    
    # Find best pattern for recommendations
    best_recommendations = max(pattern_names, key=lambda p: 
        sum(1 for r in all_results if r['pattern'] == p and r['has_recommendations']) / 
        sum(1 for r in all_results if r['pattern'] == p))
    
    # Find most cost-effective pattern
    most_cost_effective = min(pattern_names, key=lambda p: 
        sum(r['cost'] for r in all_results if r['pattern'] == p))
    
    print(f"Best for allocations: {best_allocation.replace('_', ' ').title()}")
    print(f"Best for recommendations: {best_recommendations.replace('_', ' ').title()}")
    print(f"Most cost-effective: {most_cost_effective.replace('_', ' ').title()}")

async def main():
    """Run portfolio optimization demo"""
    print("📈 BANKING PORTFOLIO OPTIMIZATION DEMO")
    print("="*50)
    print("Testing all patterns on complex portfolio optimization problems")
    print("Using Google Gemini API for advanced financial analysis")
    
    # Run individual pattern analyses
    await demo_chain_of_thought_portfolio()
    await demo_reflexion_portfolio()
    await demo_tree_of_thoughts_portfolio()
    await demo_multi_agent_debate_portfolio()
    await demo_tool_use_portfolio()
    
    # Compare all patterns
    await compare_portfolio_optimization()
    
    print("\n✅ Portfolio optimization demo completed!")

if __name__ == "__main__":
    asyncio.run(main()) 