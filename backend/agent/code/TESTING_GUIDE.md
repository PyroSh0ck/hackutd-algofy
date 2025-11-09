# Testing Guide - Financial Assistant System

## Quick Start

### Option 1: Jupyter Notebook (Easiest)

```bash
cd "c:\Users\Arnav\CS Stuffs\agentc-ai\backend\agent\code"
jupyter notebook financial_assistant_quick_demo.ipynb
```

Run all cells - it will:
1. Load your Stripe session
2. Test Money Manager (balances, transactions)
3. Test Budget Helper (create budget, add goals)
4. Test Stock Analysis (investment advice)

### Option 2: Budget Helper Specific

```bash
jupyter notebook budget_helper_demo.ipynb
```

Focuses on:
- Creating budgets based on real spending
- Adding savings goals
- Auto-adjusting budget

### Option 3: Full Demo

```bash
jupyter notebook financial_assistant_demo.ipynb
```

Complete walkthrough with all features.

## What to Expect

### When You Create a Budget

**You ask:** "Help me create a monthly budget for $3000 income"

**Budget Helper will:**
1. Call Money Manager → `get_all_balances()`
   - Gets your Checking and Savings balances
2. Call Money Manager → `get_account_transactions()`
   - Gets last 90 days of transactions
3. Analyze spending patterns
   - Categorizes into: Groceries, Eating Out, Shopping, etc.
4. Create personalized budget
   - Based on 50/30/20 rule
   - Uses YOUR actual spending amounts

**You'll see:**
```
Let me create a budget for you!

First, checking your accounts...
✅ Found 2 accounts:
  - Checking: $2,450.75
  - Savings: $8,500.00

Analyzing your spending from last 3 months...
✅ Analyzed 87 transactions

Your Monthly Budget ($3,000 income):

NEEDS (50%): $1,500
  • Housing: $1,000
  • Groceries: $285 (avg from your spending)
  • Utilities: $115 (avg from your spending)
  • Transportation: $100

WANTS (30%): $900
  • Eating Out: $420 (avg from your spending)
  • Shopping: $280
  • Entertainment: $200

SAVINGS (20%): $600
  • Emergency Fund: $300
  • Retirement: $150
  • Other Savings: $150
```

### When You Add a Savings Goal

**You ask:** "I want to save $1000 for a trip in May 2026"

**Budget Helper will:**
1. Calculate: $1000 ÷ 6 months = $167/month
2. Get current budget
3. Find where to reduce spending
4. Auto-adjust budget to fit goal

**You'll see:**
```
Perfect! Let's save for your trip!

Target: $1,000
Date: May 2026 (6 months away)
Monthly needed: $167

I've adjusted your budget:

Reductions to fit your goal:
  • Eating Out: $420 → $300 (save $120)
  • Shopping: $280 → $227 (save $53)
  (Reduced by $173/month to make room)

Updated Budget:
NEEDS: $1,500 (50%)
WANTS: $727 (24%)
SAVINGS: $773 (26%)
  • Emergency Fund: $300
  • Retirement: $150
  • Trip Savings: $167 ✨ NEW!
  • Other: $156

In 6 months, you'll have $1,000 for your trip! 🎉
```

## Verifying Money Manager Integration

Look for these indicators that Budget Helper is using Money Manager:

### ✅ Indicators It's Working

1. **"Checking your accounts..."**
   - Budget Helper calling Money Manager's `get_all_balances()`

2. **"Analyzing your spending..."**
   - Budget Helper calling Money Manager's `get_account_transactions()`

3. **Real account balances shown**
   - Not made up numbers
   - Matches your actual Stripe accounts

4. **Spending amounts match transactions**
   - Budget categories use actual spending data
   - Not generic estimates

5. **See account names**
   - "Chase Checking", "Chase Savings", etc.
   - Your actual bank names from Stripe

### ❌ If Something's Wrong

**"No accounts found":**
```bash
# Make sure Stripe session is set
cat backend/agent/secrets.env | grep STRIPE_SESSION_ID

# If not set, run setup
jupyter notebook stripe_setup_clean.ipynb
```

**Import errors:**
- Make sure you're in the correct directory
- Run from `backend/agent/code/`

**"Could not load accounts":**
- Check STRIPE_SESSION_ID is valid
- Verify accounts are still connected
- Re-run stripe setup if needed

## Test Commands

### Quick System Check

```python
# In Python console or notebook
import sys
sys.path.append('c:/Users/Arnav/CS Stuffs/agentc-ai/backend/agent/code')

# Test imports
from financial_agent import FinancialState
from financial_agent.banking_agent.tools import BankingTools
from financial_agent.budget_agent.tools import BudgetTools
from stripe_integration.client import StripeFinancialClient

print("✅ All imports successful!")

# Test Money Manager
stripe_client = StripeFinancialClient()
banking_tools = BankingTools(stripe_client)
print("✅ Money Manager initialized!")

# Test Budget Helper
budget_tools = BudgetTools(banking_tools)
print("✅ Budget Helper initialized with Money Manager!")
```

### Test Money Manager Directly

```python
import asyncio
import os
from dotenv import load_dotenv

load_dotenv("backend/agent/secrets.env")

from financial_agent.banking_agent.tools import BankingTools
from stripe_integration.client import StripeFinancialClient
from financial_agent.shared_state import FinancialState

async def test():
    client = StripeFinancialClient()
    tools = BankingTools(client)

    state = FinancialState(
        stripe_session_id=os.getenv("STRIPE_SESSION_ID")
    )

    # Get balances
    result = await tools.get_all_balances(state)
    print(f"Balances: {result}")

    # Get transactions
    if state.accounts:
        txn_result = await tools.get_account_transactions(
            state,
            account_name=state.accounts[0].name,
            days=30
        )
        print(f"Transactions: {len(txn_result.get('transactions', []))}")

asyncio.run(test())
```

### Test Budget Helper with Money Manager

```python
import asyncio
import os
from dotenv import load_dotenv

load_dotenv("backend/agent/secrets.env")

from financial_agent import chat_with_budget_helper, FinancialState

async def test():
    state = FinancialState(
        user_id="test",
        stripe_session_id=os.getenv("STRIPE_SESSION_ID")
    )
    state.user_goals.monthly_income = 3000.0

    config = {
        "configurable": {
            "openrouter_api_key": os.getenv("OPENROUTER_API_KEY")
        }
    }

    response = await chat_with_budget_helper(
        "Create a budget for $3000 income",
        state,
        config
    )
    print(response)

asyncio.run(test())
```

## Expected Test Results

### ✅ Success Indicators

1. **No import errors**
2. **Real account balances displayed**
3. **Transaction data from Stripe**
4. **Budget amounts based on actual spending**
5. **Goals auto-adjust budget correctly**

### 📊 Sample Output

```
You: Help me create a monthly budget

Budget Helper:
Let me create a budget based on your income and spending!

Checking your accounts... (via Money Manager)
✅ Checking: $2,450.75
✅ Savings: $8,500.00

Analyzing spending patterns... (via Money Manager)
✅ Found 87 transactions in last 3 months

Average monthly spending:
  • Groceries: $285
  • Eating Out: $420
  • Shopping: $280
  • Utilities: $115
  • Transportation: $100

Your Personalized Budget:
[Budget details based on REAL spending...]
```

## Troubleshooting

### Import Error: "attempted relative import beyond top-level package"

**Fixed!** The import statements have been updated to absolute imports.

Make sure you're running from the correct directory:
```bash
cd "c:\Users\Arnav\CS Stuffs\agentc-ai\backend\agent\code"
```

### No Balances Showing

1. Check Stripe session:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv("backend/agent/secrets.env")
   print(os.getenv("STRIPE_SESSION_ID"))
   ```

2. Re-run Stripe setup:
   ```bash
   jupyter notebook stripe_setup_clean.ipynb
   ```

### Budget Amounts Seem Random

If budget amounts don't match your spending:
- Check that transactions are being loaded
- Verify transaction categorization is working
- Ensure enough transaction history (need 30+ days)

## Summary

✅ **Ready to test!**

The system is fully integrated:
1. Budget Helper uses Money Manager for all data
2. Money Manager uses Stripe for real banking data
3. Everything works together seamlessly

**Start with:**
```bash
jupyter notebook financial_assistant_quick_demo.ipynb
```

This will test everything and show you how it all works!
