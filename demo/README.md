# Banking Demo Examples

This directory contains comprehensive banking demos that showcase how different AI agent patterns approach the same financial problems with varying strategies and results.

## 🏦 Demo Overview

Each demo demonstrates **5 different AI patterns** solving the same banking problem:
- **Chain-of-Thought**: Linear step-by-step reasoning
- **Reflexion**: Iterative self-improvement
- **Tree of Thoughts**: Multiple reasoning paths exploration
- **Multi-Agent Debate**: Multiple specialist perspectives
- **Tool-Use**: Enhanced analysis with calculation tools

## 📁 Demo Files

### 1. `banking_loan_eligibility.py`
**Loan Approval Assessment** - All patterns analyze the same customer profile for mortgage eligibility.

**Features:**
- Real DTI ratio calculations
- Credit score assessment
- Employment stability evaluation
- Down payment adequacy analysis
- Final approval recommendations

**Usage:**
```bash
python demo/banking_loan_eligibility.py
```

### 2. `banking_fraud_detection.py`
**Fraud Detection Analysis** - Multiple fraud scenarios analyzed by each pattern.

**Scenarios:**
- Geographic anomalies (transactions across continents)
- Amount anomalies (unusual purchase amounts)
- Velocity anomalies (rapid-fire transactions)

**Usage:**
```bash
python demo/banking_fraud_detection.py
```

### 3. `banking_portfolio_optimization.py`
**Investment Portfolio Optimization** - Complex constraint handling for different client profiles.

**Scenarios:**
- Retirement planning (45-year-old professional)
- Income generation (65-year-old retiree)
- Growth optimization (30-year-old tech professional)

**Usage:**
```bash
python demo/banking_portfolio_optimization.py
```

### 4. `test_patterns.py`
**Comprehensive Testing** - Verifies all patterns work correctly with banking scenarios.

**Tests:**
- Pattern availability and instantiation
- Output structure validation
- Banking scenario compatibility
- Cost comparison analysis
- Error handling verification
- Gemini API integration

**Usage:**
```bash
python demo/test_patterns.py
```

## 🔧 Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
Create a `.env` file in the project root:
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**Note:** The `.env` file is already in `.gitignore` for security.

### 3. Run Demos
```bash
# Run specific demo
python demo/banking_loan_eligibility.py

# Run all tests
python demo/test_patterns.py
```

## 📊 Expected Output

Each demo provides:

### Individual Pattern Analysis
- Detailed response from each pattern
- Cost analysis per pattern
- Success/failure indicators
- Pattern-specific metadata

### Comparison Tables
- Cost comparison across patterns
- Decision consistency analysis
- Performance metrics
- Best pattern recommendations

### Summary Statistics
- Total cost analysis
- Pattern effectiveness ranking
- Cost-benefit recommendations

## 🎯 Key Features

### Real Banking Logic
- **DTI Ratios**: Debt-to-income calculations
- **Fraud Patterns**: Geographic, amount, velocity anomalies
- **Portfolio Constraints**: Risk tolerance, time horizon, tax considerations
- **Regulatory Compliance**: Banking standards and best practices

### Pattern Comparison
- **Same Problem**: Identical scenarios across all patterns
- **Different Approaches**: Each pattern's unique strategy
- **Cost Analysis**: Token usage and cost efficiency
- **Quality Assessment**: Response completeness and accuracy

### Runnable Demos
- **Standalone Execution**: Each file runs independently
- **Error Handling**: Graceful failure management
- **Progress Tracking**: Real-time execution feedback
- **Result Comparison**: Side-by-side pattern analysis

## 🔍 Pattern Insights

### Chain-of-Thought
- **Best for**: Systematic analysis, step-by-step reasoning
- **Strengths**: Clear logic flow, easy to follow
- **Cost**: Low to moderate
- **Use case**: Loan eligibility, fraud detection

### Reflexion
- **Best for**: Complex problems requiring iteration
- **Strengths**: Self-improvement, quality assurance
- **Cost**: Moderate to high
- **Use case**: Portfolio optimization, complex fraud cases

### Tree of Thoughts
- **Best for**: Exploring multiple solution paths
- **Strengths**: Comprehensive analysis, alternative viewpoints
- **Cost**: High
- **Use case**: Complex optimization, multi-faceted problems

### Multi-Agent Debate
- **Best for**: Balanced decision-making
- **Strengths**: Multiple perspectives, consensus building
- **Cost**: Moderate
- **Use case**: Risk assessment, policy decisions

### Tool-Use
- **Best for**: Calculations and data analysis
- **Strengths**: Precise computations, external data integration
- **Cost**: Low to moderate
- **Use case**: Financial calculations, quantitative analysis

## 🚀 Getting Started

1. **Quick Start**: Run the loan eligibility demo
   ```bash
   python demo/banking_loan_eligibility.py
   ```

2. **Explore Patterns**: Try different demos to see pattern differences
   ```bash
   python demo/banking_fraud_detection.py
   python demo/banking_portfolio_optimization.py
   ```

3. **Verify Setup**: Run tests to ensure everything works
   ```bash
   python demo/test_patterns.py
   ```

## 💡 Customization

### Adding New Scenarios
1. Add scenario to the appropriate demo file
2. Update the pattern analysis functions
3. Modify comparison logic as needed

### Using Different LLM Providers
Change the client creation in any demo:
```python
# For OpenAI
client = create_client("openai", api_key=os.getenv("OPENAI_API_KEY"))

# For Anthropic
client = create_client("anthropic", api_key=os.getenv("ANTHROPIC_API_KEY"))

# For Mock (testing)
client = create_client("mock")
```

### Custom Patterns
Register your own patterns and test them in the demos:
```python
from agentic_patterns import register_pattern, BasePattern

class CustomBankingPattern(BasePattern):
    # Your custom implementation
    pass

register_pattern("custom_banking", CustomBankingPattern)
```

## 📈 Performance Tips

1. **Use Mock Client**: For testing without API costs
2. **Limit Iterations**: Reduce max_iterations in Reflexion pattern
3. **Shallow Trees**: Use smaller depth in Tree of Thoughts
4. **Fewer Agents**: Reduce num_agents in Multi-Agent Debate

## 🔒 Security Notes

- API keys are stored in `.env` file (gitignored)
- Never commit API keys to version control
- Use environment variables for production deployments
- Consider rate limiting for high-volume usage

## 🤝 Contributing

1. Add new banking scenarios
2. Improve pattern comparisons
3. Add more sophisticated analysis metrics
4. Create industry-specific demos

---

**Happy Banking AI Exploration! 🏦🤖** 