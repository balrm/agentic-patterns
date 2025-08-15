#!/usr/bin/env python3
"""
Banking Example: Fraud Detection
Shows how different patterns handle suspicious transactions with real fraud analysis
"""

import asyncio
import os
from dotenv import load_dotenv
from agentic_patterns import get_pattern, create_client

# Load environment variables
load_dotenv()

# Fraud scenarios for testing
FRAUD_SCENARIOS = {
    "geographic_anomaly": """
Transaction Alert - Geographic Anomaly:
- Card: **** **** **** 1234
- Customer: John Smith (ID: 12345)
- Normal behavior: Transactions in San Francisco, CA area
- Suspicious activity:
  * 14:00 - $5,000 ATM withdrawal in Bangkok, Thailand
  * 16:00 - $2,500 online purchase from NYC electronics store
  * 18:00 - $1,800 gas station purchase in Miami, FL
- Time span: 4 hours across 3 continents
- Customer reported: Card still in possession

Determine if this is fraudulent activity and recommend action.
""",
    
    "amount_anomaly": """
Transaction Alert - Amount Anomaly:
- Card: **** **** **** 5678
- Customer: Sarah Johnson (ID: 67890)
- Normal behavior: $50-200 purchases, mostly groceries and restaurants
- Suspicious activity:
  * 09:15 - $15,000 jewelry store purchase
  * 10:30 - $8,500 electronics store purchase
  * 11:45 - $12,000 luxury watch purchase
- Total: $35,500 in 2.5 hours
- Customer profile: Teacher, $45K annual income
- No prior large purchases

Determine if this is fraudulent activity and recommend action.
""",
    
    "velocity_anomaly": """
Transaction Alert - Velocity Anomaly:
- Card: **** **** **** 9012
- Customer: Mike Chen (ID: 34567)
- Normal behavior: 2-3 transactions per day
- Suspicious activity:
  * 08:00 - $500 gas station
  * 08:05 - $300 convenience store
  * 08:10 - $750 department store
  * 08:15 - $1,200 electronics store
  * 08:20 - $2,500 online purchase
  * 08:25 - $1,800 restaurant
- Pattern: 6 transactions in 25 minutes
- Total: $7,050
- All transactions successful

Determine if this is fraudulent activity and recommend action.
"""
}

async def analyze_fraud_with_pattern(pattern_name, scenario_name, scenario_text):
    """Analyze fraud scenario with a specific pattern"""
    print(f"\n=== {pattern_name.upper()} - {scenario_name.replace('_', ' ').title()} ===")
    
    client = create_client("google", api_key=os.getenv("GEMINI_API_KEY"))
    pattern = get_pattern(pattern_name, client)
    
    result = await pattern.execute(scenario_text)
    
    # Extract fraud indicators
    response_lower = result.response.lower()
    is_fraud = any(word in response_lower for word in ['fraud', 'suspicious', 'anomaly', 'block', 'deny'])
    confidence = 'High' if result.success else 'Low'
    
    print(f"Verdict: {'🚨 FRAUD' if is_fraud else '✅ LEGITIMATE'}")
    print(f"Confidence: {confidence}")
    print(f"Cost: ${result.cost:.4f}")
    print(f"Response: {result.response[:200]}...")
    
    return {
        'pattern': pattern_name,
        'scenario': scenario_name,
        'is_fraud': is_fraud,
        'confidence': confidence,
        'cost': result.cost,
        'response_length': len(result.response)
    }

async def demo_chain_of_thought_fraud():
    """Chain of Thought for systematic fraud analysis"""
    print("\n🔍 CHAIN OF THOUGHT FRAUD ANALYSIS")
    print("Approach: Systematic step-by-step fraud detection")
    
    results = []
    for scenario_name, scenario_text in FRAUD_SCENARIOS.items():
        result = await analyze_fraud_with_pattern("chain_of_thought", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def demo_reflexion_fraud():
    """Reflexion for iterative fraud assessment"""
    print("\n🔄 REFLEXION FRAUD ANALYSIS")
    print("Approach: Iterative improvement with self-correction")
    
    results = []
    for scenario_name, scenario_text in FRAUD_SCENARIOS.items():
        result = await analyze_fraud_with_pattern("reflexion", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def demo_tree_of_thoughts_fraud():
    """Tree of Thoughts for exploring multiple fraud hypotheses"""
    print("\n🌳 TREE OF THOUGHTS FRAUD ANALYSIS")
    print("Approach: Explore multiple fraud detection paths")
    
    results = []
    for scenario_name, scenario_text in FRAUD_SCENARIOS.items():
        result = await analyze_fraud_with_pattern("tree_of_thoughts", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def demo_multi_agent_debate_fraud():
    """Multi-Agent Debate for multiple specialist perspectives"""
    print("\n👥 MULTI-AGENT DEBATE FRAUD ANALYSIS")
    print("Approach: Multiple specialist perspectives")
    
    results = []
    for scenario_name, scenario_text in FRAUD_SCENARIOS.items():
        result = await analyze_fraud_with_pattern("multi_agent_debate", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def demo_tool_use_fraud():
    """Tool-Use for enhanced fraud detection with external tools"""
    print("\n🛠️ TOOL-USE FRAUD ANALYSIS")
    print("Approach: Enhanced detection with calculation tools")
    
    results = []
    for scenario_name, scenario_text in FRAUD_SCENARIOS.items():
        result = await analyze_fraud_with_pattern("tool_use", scenario_name, scenario_text)
        results.append(result)
    
    return results

async def compare_fraud_detection():
    """Compare all patterns on fraud detection"""
    print("\n" + "="*80)
    print("FRAUD DETECTION PATTERN COMPARISON")
    print("="*80)
    
    patterns = [
        ("Chain of Thought", demo_chain_of_thought_fraud),
        ("Reflexion", demo_reflexion_fraud),
        ("Tree of Thoughts", demo_tree_of_thoughts_fraud),
        ("Multi-Agent Debate", demo_multi_agent_debate_fraud),
        ("Tool-Use", demo_tool_use_fraud)
    ]
    
    all_results = []
    for pattern_name, pattern_func in patterns:
        try:
            results = await pattern_func()
            all_results.extend(results)
        except Exception as e:
            print(f"Error with {pattern_name}: {e}")
    
    # Analysis by scenario
    scenarios = list(FRAUD_SCENARIOS.keys())
    print(f"\n📊 FRAUD DETECTION RESULTS BY SCENARIO")
    print("-" * 80)
    
    for scenario in scenarios:
        scenario_results = [r for r in all_results if r['scenario'] == scenario]
        fraud_count = sum(1 for r in scenario_results if r['is_fraud'])
        total_count = len(scenario_results)
        
        print(f"\n{scenario.replace('_', ' ').title()}:")
        print(f"  Fraud detected: {fraud_count}/{total_count} patterns")
        print(f"  Detection rate: {(fraud_count/total_count)*100:.1f}%")
        
        for result in scenario_results:
            status = "🚨 FRAUD" if result['is_fraud'] else "✅ LEGIT"
            print(f"    {result['pattern']}: {status} (${result['cost']:.4f})")
    
    # Analysis by pattern
    print(f"\n📈 PATTERN PERFORMANCE SUMMARY")
    print("-" * 80)
    
    pattern_names = list(set(r['pattern'] for r in all_results))
    for pattern in pattern_names:
        pattern_results = [r for r in all_results if r['pattern'] == pattern]
        fraud_count = sum(1 for r in pattern_results if r['is_fraud'])
        total_cost = sum(r['cost'] for r in pattern_results)
        avg_confidence = sum(1 for r in pattern_results if r['confidence'] == 'High') / len(pattern_results)
        
        print(f"\n{pattern.replace('_', ' ').title()}:")
        print(f"  Fraud detected: {fraud_count}/{len(pattern_results)} scenarios")
        print(f"  Total cost: ${total_cost:.4f}")
        print(f"  High confidence rate: {avg_confidence*100:.1f}%")

async def main():
    """Run fraud detection demo"""
    print("🚨 BANKING FRAUD DETECTION DEMO")
    print("="*50)
    print("Testing all patterns on realistic fraud scenarios")
    print("Using Google Gemini API for advanced fraud analysis")
    
    # Run individual pattern analyses
    await demo_chain_of_thought_fraud()
    await demo_reflexion_fraud()
    await demo_tree_of_thoughts_fraud()
    await demo_multi_agent_debate_fraud()
    await demo_tool_use_fraud()
    
    # Compare all patterns
    await compare_fraud_detection()
    
    print("\n✅ Fraud detection demo completed!")

if __name__ == "__main__":
    asyncio.run(main()) 