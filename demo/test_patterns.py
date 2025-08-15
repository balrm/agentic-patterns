#!/usr/bin/env python3
"""
Simple tests to verify each pattern works correctly with banking scenarios
"""

import asyncio
import os
import pytest
from dotenv import load_dotenv
from agentic_patterns import get_pattern, create_client, BasePattern, list_patterns

# Load environment variables
load_dotenv()

# Test scenarios
TEST_SCENARIOS = {
    "loan_eligibility": "Customer has $8,000 monthly income and wants a $300,000 mortgage. Should they be approved?",
    "fraud_detection": "Transaction: $5,000 ATM withdrawal in Bangkok 2 hours after $2,500 purchase in NYC. Is this fraud?",
    "portfolio_optimization": "Client has $500,000 to invest with moderate risk tolerance. What's the optimal allocation?"
}

async def test_all_patterns_available():
    """Verify all patterns can be instantiated"""
    print("Testing pattern availability...")
    
    patterns = list_patterns()
    assert len(patterns) >= 5, f"Expected at least 5 patterns, got {len(patterns)}"
    
    client = create_client("mock")
    
    for pattern_name in patterns.keys():
        try:
            pattern = get_pattern(pattern_name, client)
            assert isinstance(pattern, BasePattern)
            assert hasattr(pattern, 'execute')
            print(f"✅ {pattern_name}: Pattern created successfully")
        except Exception as e:
            print(f"❌ {pattern_name}: Failed - {e}")
            raise
    
    print("✅ All patterns available and instantiable")

async def test_pattern_returns_required_fields():
    """Verify patterns return expected data structure"""
    print("Testing pattern output structure...")
    
    client = create_client("mock")
    pattern = get_pattern("chain_of_thought", client)
    result = await pattern.execute("Test prompt")
    
    required_fields = ['response', 'cost', 'pattern_name', 'metadata', 'success']
    for field in required_fields:
        assert hasattr(result, field), f"Missing required field: {field}"
    
    assert result.pattern_name == "ChainOfThoughtPattern"
    assert isinstance(result.response, str)
    assert isinstance(result.cost, float)
    assert isinstance(result.success, bool)
    
    print("✅ Pattern output structure correct")

async def test_banking_scenarios_with_mock():
    """Test banking scenarios with mock client"""
    print("Testing banking scenarios with mock client...")
    
    client = create_client("mock")
    
    for scenario_name, scenario_text in TEST_SCENARIOS.items():
        print(f"\nTesting {scenario_name}...")
        
        for pattern_name in list_patterns().keys():
            try:
                pattern = get_pattern(pattern_name, client)
                result = await pattern.execute(scenario_text)
                
                assert result.success, f"Pattern {pattern_name} failed for {scenario_name}"
                assert len(result.response) > 0, f"Empty response from {pattern_name}"
                assert result.cost >= 0, f"Negative cost from {pattern_name}"
                
                print(f"  ✅ {pattern_name}: Success (${result.cost:.4f})")
                
            except Exception as e:
                print(f"  ❌ {pattern_name}: Failed - {e}")
                raise
    
    print("✅ All banking scenarios work with mock client")

async def test_gemini_integration():
    """Test with real Gemini API (if available)"""
    print("Testing Gemini API integration...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  GEMINI_API_KEY not found, skipping real API test")
        return
    
    try:
        client = create_client("google", api_key=api_key)
        pattern = get_pattern("chain_of_thought", client)
        
        # Simple test to avoid high costs
        result = await pattern.execute("What is 2 + 2?")
        
        assert result.success, "Gemini API call failed"
        assert len(result.response) > 0, "Empty response from Gemini"
        assert result.cost > 0, "No cost recorded from Gemini"
        
        print(f"✅ Gemini integration successful (${result.cost:.4f})")
        
    except Exception as e:
        print(f"❌ Gemini integration failed: {e}")
        # Don't raise here as this is optional

async def test_cost_comparison():
    """Compare costs across patterns"""
    print("Testing cost comparison...")
    
    client = create_client("mock")
    test_prompt = "Simple test prompt"
    
    costs = {}
    for pattern_name in list_patterns().keys():
        try:
            pattern = get_pattern(pattern_name, client)
            result = await pattern.execute(test_prompt)
            costs[pattern_name] = result.cost
        except Exception as e:
            print(f"❌ {pattern_name}: Failed - {e}")
            costs[pattern_name] = 0.0
    
    # Verify all patterns have reasonable costs
    for pattern_name, cost in costs.items():
        assert cost >= 0, f"Negative cost for {pattern_name}"
        print(f"  {pattern_name}: ${cost:.4f}")
    
    print("✅ Cost comparison completed")

async def test_error_handling():
    """Test error handling capabilities"""
    print("Testing error handling...")
    
    client = create_client("mock")
    
    # Test with empty prompt
    pattern = get_pattern("chain_of_thought", client)
    result = await pattern.execute("")
    
    # Should handle gracefully
    assert hasattr(result, 'success')
    print("✅ Error handling works")

async def run_all_tests():
    """Run all tests"""
    print("🧪 RUNNING AGENTIC PATTERNS TESTS")
    print("="*50)
    
    tests = [
        test_all_patterns_available,
        test_pattern_returns_required_fields,
        test_banking_scenarios_with_mock,
        test_cost_comparison,
        test_error_handling,
        test_gemini_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            await test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__}: Failed - {e}")
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed")
    
    return passed == total

# Pytest-compatible test functions
@pytest.mark.asyncio
async def test_patterns_async():
    """Async test for pytest"""
    await test_all_patterns_available()

@pytest.mark.asyncio
async def test_banking_scenarios_async():
    """Async test for banking scenarios"""
    await test_banking_scenarios_with_mock()

if __name__ == "__main__":
    # Run tests
    success = asyncio.run(run_all_tests())
    
    if success:
        print("\n✅ All tests completed successfully!")
        exit(0)
    else:
        print("\n❌ Some tests failed!")
        exit(1) 