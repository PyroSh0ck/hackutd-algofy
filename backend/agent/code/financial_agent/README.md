# Financial Assistant - Multi-Agent Orchestrator

Your personal AI assistant for managing money, explained in simple terms!

## What It Does

The Financial Assistant coordinates between specialized AI agents to help you with all aspects of money management:

### 💰 Money Manager (Banking Agent)
- **Check balances** - "How much money do I have?"
- **View transactions** - "What did I spend on groceries this week?"
- **Transfer money** - "Move $100 to savings"
- **Understand spending** - Get categorized breakdowns with simple explanations

### 📈 Stock Analysis Agent
- **Market analysis** - "Is the stock market going up or down?"
- **Investment advice** - "Should I invest $700 right now?"
- **Explain trends** - Learn WHY markets are moving
- **Beginner-friendly** - No confusing financial jargon

### 🎯 Budget Helper *(Coming Soon)*
- **Create budgets** - Set monthly spending limits
- **Track progress** - See how you're doing
- **Smart alerts** - Get notified when going over budget
- **Auto-adjust** - Automatically rebalance when overspending

## How It Works

The orchestrator automatically:
1. **Understands your question** - Figures out what you're asking about
2. **Routes to the right specialist** - Banking, stocks, or budgeting
3. **Gets the answer** - The specialist handles your request
4. **Explains in simple terms** - No jargon, just clear explanations

## Quick Start

### 1. Setup Stripe (for Banking Features)

First, connect your bank accounts using Stripe Financial Connections:

```bash
# Run the setup notebook
jupyter notebook stripe_setup_clean.ipynb
```

Follow the 4 steps:
1. Load API keys
2. Create session and connect test accounts
3. Verify accounts
4. Test with balances

Save your `STRIPE_SESSION_ID` to `secrets.env`.

### 2. Use the Financial Assistant

#### Option A: Simple Demo (Recommended)

```bash
jupyter notebook financial_assistant_quick_demo.ipynb
```

#### Option B: Full Demo

```bash
jupyter notebook financial_assistant_demo.ipynb
```

#### Option C: Python Code

```python
from financial_agent import chat_with_financial_assistant, FinancialState

# Create state
state = FinancialState(
    user_id="your_user_id",
    stripe_session_id="fcsess_...",  # From stripe setup
)

# Ask questions
response = await chat_with_financial_assistant(
    "How much money do I have?",
    state
)

print(response)
```

## Architecture

```
Financial Assistant (Orchestrator)
├── Money Manager Agent
│   ├── Stripe Financial Client
│   └── Banking Tools
│       ├── Get balances
│       ├── View transactions
│       └── Transfer funds
│
├── Stock Analysis Agent
│   ├── Market researcher
│   ├── Report writer
│   └── Investment decision maker
│
└── Budget Helper Agent (Coming Soon)
    ├── Budget creator
    ├── Spending tracker
    └── Auto-adjuster
```

## Files Structure

```
financial_agent/
├── orchestrator.py           # Main coordinator
├── shared_state.py           # State models for all agents
├── __init__.py               # Package exports
│
├── banking_agent/
│   ├── agent.py              # Money Manager LangGraph workflow
│   ├── tools.py              # Banking operations (balances, transactions, transfers)
│   └── prompts.py            # Beginner-friendly prompts
│
└── README.md                 # This file
```

## Example Conversations

### Banking Questions

**You:** "How much money do I have?"

**Assistant:** "Let me check all your accounts for you!

Your Money:

💰 Chase Checking: $2,450.75
   This is your checking account for everyday spending and bills.

💰 Chase Savings: $8,500.00
   This is your savings account for saving money and emergencies.

Total across all accounts: $10,950.75

✓ Your checking account looks healthy! That should cover your bills this month."

---

**You:** "What did I spend on groceries?"

**Assistant:** "Let me show you your grocery spending this month!

🛒 Groceries - $202.00
   • Whole Foods ($87.50)
   • Trader Joe's ($69.30)
   • Safeway ($45.20)

That's about $50 per week, which is normal for groceries!"

---

**You:** "Move $100 to savings"

**Assistant:** "I can help you save that money!

Here's what will happen:
  From: Chase Checking ($2,450.75)
  To: Chase Savings ($8,500.00)
  Amount: $100.00

After the transfer:
  Checking: $2,350.75 (still plenty for bills!)
  Savings: $8,600.00 (great job saving!)

Should I go ahead and move the money? (Reply 'yes' to confirm)"

### Investment Questions

**You:** "Should I invest $700 in the stock market?"

**Assistant:** "Let me analyze the current stock market for you!

(Researches recent market news and trends...)

# S&P 500 and SPY ETF Analysis

**Analysis Date:** November 8, 2025
**Investment Amount:** $700

## Market Overview
The S&P 500 is currently at 4,850, up 2.3% this week...

## Recent News Analysis
The Federal Reserve announced interest rate cuts...

## Investment Recommendation

**Decision: BUY NOW**

Based on recent positive market momentum and supportive Fed policy, now appears to be a good time to invest your $700 in an S&P 500 ETF like SPY.

**What does this mean for you?**
- The market has been going up recently
- Interest rates are coming down (good for stocks)
- $700 is a safe amount to start with
- SPY is a good beginner investment (it tracks 500 companies)

**Risks to know:**
- Markets can still go down in the short term
- Don't invest money you need for bills
- Consider dollar-cost averaging (invest a little each month)

Want to learn more about how to actually buy SPY?"

## Configuration

### Required Environment Variables

```bash
# secrets.env
OPENROUTER_API_KEY=sk-or-v1-...          # For LLM access
STRIPE_API_KEY=sk_test_...               # For Stripe API
STRIPE_SESSION_ID=fcsess_...             # After running stripe setup

# variables.env
TAVILY_API_KEY=tvly-...                  # For web search (stock analysis)
```

### Optional Settings

```python
state = FinancialState(
    user_id="your_id",
    stripe_session_id="fcsess_...",
    use_simple_language=True,    # Use beginner-friendly terms
)

config = {
    "configurable": {
        "openrouter_api_key": "...",
        "model": "openrouter/nvidia/llama-3.1-nemotron-70b-instruct"
    }
}
```

## API Reference

### Main Functions

#### `chat_with_financial_assistant(user_query, state, config)`

Chat with the financial assistant about any money topic.

**Parameters:**
- `user_query` (str): Your question or request
- `state` (FinancialState, optional): Your financial state
- `config` (RunnableConfig, optional): Configuration with API keys

**Returns:**
- `str`: The assistant's response

**Example:**
```python
response = await chat_with_financial_assistant(
    "How much money do I have?",
    state,
    config
)
```

#### `create_financial_orchestrator()`

Create the orchestrator LangGraph workflow.

**Returns:**
- `StateGraph`: Compiled LangGraph workflow

**Example:**
```python
orchestrator = create_financial_orchestrator()
result = await orchestrator.ainvoke(state, config)
```

### Specialized Agents

#### Money Manager

```python
from financial_agent.banking_agent import chat_with_money_manager

response = await chat_with_money_manager(
    "Show me my transactions",
    state,
    config
)
```

#### Stock Analysis

```python
from docgen_agent.agent import graph as stock_analysis_graph, AgentState

state = AgentState(
    topic="S&P 500 and SPY ETF Analysis",
    report_structure="Market Overview, Recent News, Investment Recommendation",
    investment_amount=700.0
)

result = await stock_analysis_graph.ainvoke(state, config)
print(result["report"])
```

## Testing

### Test Individual Agents

#### Money Manager
```bash
jupyter notebook money_manager_demo.ipynb
```

#### Stock Analysis
```bash
jupyter notebook stock_analysis_demo.ipynb
```

#### All Functions
```bash
jupyter notebook test_stripe_functions.ipynb
```

### Test Orchestrator

```bash
# Quick test
jupyter notebook financial_assistant_quick_demo.ipynb

# Full test
jupyter notebook financial_assistant_demo.ipynb

# Python test
python -m financial_agent.orchestrator
```

## Beginner-Friendly Design

The Financial Assistant is designed for people who don't know much about money:

### Simple Language
- ✅ "checking account" not "liquid assets"
- ✅ "eating out" not "discretionary dining expenditures"
- ✅ "money you have" not "current balance sheet"

### Educational Explanations
- Every answer explains WHY
- Tips for learning about money
- Encouragement for good financial habits

### Safety Features
- Always confirms before moving money
- Shows before/after amounts
- Warns about low balances
- Explains risks clearly

## Roadmap

### ✅ Completed
- [x] Stripe Financial Connections integration
- [x] Money Manager agent with banking tools
- [x] Stock Analysis agent for investments
- [x] Main orchestrator coordinator
- [x] Beginner-friendly prompts and explanations
- [x] Demo notebooks

### 🔄 In Progress
- [ ] Budget Helper agent
- [ ] FastAPI routes for web interface

### 📋 Planned
- [ ] Spending insights and patterns
- [ ] Bill tracking and reminders
- [ ] Savings goal tracker
- [ ] Financial literacy tips
- [ ] Multi-user support

## Contributing

Want to add more features?

1. **New agents**: Create in `financial_agent/[agent_name]/`
2. **New tools**: Add to `[agent_name]/tools.py`
3. **New prompts**: Add to `[agent_name]/prompts.py`
4. **Update orchestrator**: Add routing in `orchestrator.py`

## License

See main repository LICENSE file.

## Support

Questions? Issues?
- Check the demo notebooks first
- Review error messages carefully
- Make sure API keys are set correctly
- Ensure Stripe session is connected

## Acknowledgments

Built with:
- LangGraph - Agent orchestration
- Stripe Financial Connections - Bank account access
- OpenRouter - LLM API access
- Tavily - Web search for market news
