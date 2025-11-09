# Budget Helper ↔ Money Manager Integration ✅

## Overview

The Budget Helper now uses the Money Manager's tools to access all banking data instead of directly calling Stripe. This creates better separation of concerns and reuses existing functionality.

## Architecture

```
Budget Helper Agent
    ↓
Uses Money Manager Tools
    ↓
Money Manager (BankingTools)
    ↓
Stripe Financial Client
    ↓
Stripe API
```

## What Changed

### Before (Direct Stripe Access)
```python
class BudgetTools:
    def __init__(self, stripe_client: StripeFinancialClient):
        self.stripe_client = stripe_client

    async def analyze_spending_patterns(self, state):
        # Direct Stripe calls
        accounts = await self.stripe_client.get_accounts(...)
        transactions = await self.stripe_client.get_transactions(...)
```

### After (Uses Money Manager)
```python
class BudgetTools:
    def __init__(self, banking_tools: BankingTools):
        self.banking_tools = banking_tools

    async def analyze_spending_patterns(self, state):
        # Uses Money Manager tools
        balances = await self.banking_tools.get_all_balances(state)
        txn_result = await self.banking_tools.get_account_transactions(state, ...)
```

## Tools Available to Budget Helper

The Budget Helper now has access to **ALL** Money Manager tools:

### From Money Manager (BankingTools)
1. **`get_all_balances()`**
   - Gets current balances for all accounts
   - Updates state with account information
   - Returns total balance

2. **`get_account_transactions()`**
   - Gets transaction history for an account
   - Can filter by days/timeframe
   - Returns categorized transactions

3. **`transfer_money()`**
   - Validates and simulates transfers
   - Checks sufficient balance
   - Updates account balances

### Budget Helper's Own Tools
1. **`create_budget(monthly_income)`**
   - Uses Money Manager to get balances & transactions
   - Analyzes spending patterns
   - Creates personalized budget

2. **`add_savings_goal(goal_name, amount, date)`**
   - Calculates monthly contribution needed
   - Uses Money Manager for current financial state
   - Auto-adjusts budget to fit goal

3. **`view_budget()`**
   - Shows current budget status
   - Displays progress toward goals
   - Lists overspent categories

## Data Flow Example

### User Request: "Create a budget for $3000 income"

```
1. User → Budget Helper Agent
   "Help me create a monthly budget for $3000 income"

2. Budget Helper → Money Manager (get_all_balances)
   Gets: Checking $2,450.75, Savings $8,500

3. Budget Helper → Money Manager (get_account_transactions)
   For each account, gets last 90 days of transactions

4. Budget Helper → analyze_spending_patterns()
   Categorizes transactions:
   - Groceries: $285/month avg
   - Eating Out: $420/month avg
   - Rent: $1,000/month
   etc.

5. Budget Helper → create_budget_recommendation()
   Applies 50/30/20 rule:
   - Needs (50%): $1,500
   - Wants (30%): $900
   - Savings (20%): $600

6. Budget Helper → User
   Returns complete budget with categories and amounts
```

### User Request: "I want to save $1000 for a trip in May 2026"

```
1. User → Budget Helper Agent
   "I want to save $1000 for a trip in May 2026"

2. Budget Helper → Calculates
   Target: $1000
   Months: 6
   Monthly needed: $167

3. Budget Helper → Money Manager (get_all_balances)
   Gets current balances to validate feasibility

4. Budget Helper → Money Manager (get_account_transactions)
   Gets spending patterns to find where to cut

5. Budget Helper → create_budget_recommendation()
   Adjusts budget:
   - Reduces Eating Out: $400 → $300 (save $100)
   - Reduces Shopping: $300 → $233 (save $67)
   - Adds Savings Goal: $167

6. Budget Helper → User
   Returns updated budget with goal included
```

## Code Changes

### 1. BudgetTools Constructor
**File:** `financial_agent/budget_agent/tools.py`

```python
# OLD
def __init__(self, stripe_client: StripeFinancialClient):
    self.stripe_client = stripe_client

# NEW
def __init__(self, banking_tools: BankingTools):
    self.banking_tools = banking_tools
```

### 2. Spending Pattern Analysis
**File:** `financial_agent/budget_agent/tools.py`

```python
async def analyze_spending_patterns(self, state, months=3):
    # Get accounts using Money Manager
    if not state.accounts:
        balances_result = await self.banking_tools.get_all_balances(state)

    # Get transactions using Money Manager
    for account in state.accounts:
        txn_result = await self.banking_tools.get_account_transactions(
            state,
            account_name=account.name,
            days=months * 30
        )

        # Convert transaction data to Transaction objects
        for txn_data in txn_result["transactions"]:
            all_transactions.append(Transaction(...))
```

### 3. Budget Agent Setup
**File:** `financial_agent/budget_agent/agent.py`

```python
async def budget_assistant(state, config):
    # Create banking tools
    stripe_client = StripeFinancialClient()
    banking_tools = BankingTools(stripe_client)

    # Create budget tools that use Money Manager
    budget_tools = create_budget_tools(banking_tools)

    # Include Money Manager tools directly
    from ..banking_agent.tools import create_banking_tools
    banking_tools_list = create_banking_tools(stripe_client)

    # Combine all tools
    all_tools = budget_tools + banking_tools_list
    llm_with_tools = llm.bind_tools(all_tools)
```

### 4. Tool Creation Function
**File:** `financial_agent/budget_agent/tools.py`

```python
# OLD
def create_budget_tools(stripe_client: StripeFinancialClient) -> List:
    tools_instance = BudgetTools(stripe_client)
    return [...]

# NEW
def create_budget_tools(banking_tools: BankingTools) -> List:
    """
    Create budget tools that use Money Manager for data access.

    Args:
        banking_tools: BankingTools instance from Money Manager
    """
    tools_instance = BudgetTools(banking_tools)
    return [...]
```

### 5. Updated Prompts
**File:** `financial_agent/budget_agent/prompts.py`

```python
SYSTEM_PROMPT = """
You have access to Money Manager tools to:
- Get current account balances
- View transaction history
- See spending patterns by category
- Use this data to create personalized budgets
"""

CREATE_BUDGET_PROMPT = """
Steps:
1. Ask for their monthly income
2. Use get_all_balances to see their current money
3. Use get_account_transactions to analyze spending
4. Create budget using 50/30/20 rule based on actual spending
"""
```

## Benefits of Integration

### 1. **Single Source of Truth**
- All banking data flows through Money Manager
- Consistent data format across agents
- No duplicate Stripe calls

### 2. **Reusable Components**
- Budget Helper leverages existing Money Manager tools
- Don't repeat balance/transaction logic
- Easier to maintain

### 3. **Better Separation of Concerns**
```
Money Manager → Knows HOW to get banking data
Budget Helper → Knows WHAT to do with the data
```

### 4. **Combined Capabilities**
The Budget Helper can now:
- ✅ Get balances (from Money Manager)
- ✅ Get transactions (from Money Manager)
- ✅ Analyze spending patterns (own logic)
- ✅ Create budgets (own logic)
- ✅ Set goals (own logic)
- ✅ Transfer funds (from Money Manager)

### 5. **Smarter Budgeting**
```python
# Example: Budget Helper can now do this automatically

# 1. Check current balance
balances = await get_all_balances()
# Result: Checking $2,450, Savings $8,500

# 2. Get spending history
transactions = await get_account_transactions(days=90)
# Result: 127 transactions, $6,300 total spent

# 3. Analyze patterns
patterns = analyze_spending_patterns()
# Result: Groceries $285/mo, Eating Out $420/mo, etc.

# 4. Create personalized budget
budget = create_budget(income=3000, patterns=patterns)
# Result: Budget based on ACTUAL spending, not estimates

# 5. Set up automatic savings
goal = add_savings_goal("Trip", 1000, "2026-05")
# Result: $167/month, budget auto-adjusted
```

## Testing

### Test Budget Helper with Money Manager Integration

```python
from financial_agent import chat_with_budget_helper, FinancialState

state = FinancialState(
    user_id="test_user",
    stripe_session_id="fcsess_..."  # Your Stripe session
)

# Budget Helper will automatically:
# 1. Use Money Manager to get balances
# 2. Use Money Manager to get transactions
# 3. Analyze spending from real data
# 4. Create personalized budget

response = await chat_with_budget_helper(
    "Create a budget for $3000 income",
    state,
    config
)

print(response)
# Shows budget based on actual spending patterns!
```

### Run Demo Notebook

```bash
jupyter notebook budget_helper_demo.ipynb
```

The demo will show:
- Budget Helper getting balances via Money Manager
- Budget Helper analyzing transactions via Money Manager
- Creating budgets based on real spending data
- Setting goals and auto-adjusting budget

## Summary

✅ **Integration Complete!**

The Budget Helper now:
1. Uses Money Manager for ALL banking data access
2. Has access to balances, transactions, and transfers
3. Creates budgets based on REAL spending patterns
4. Automatically pulls current balances and transactions
5. Works seamlessly with the Money Manager agent

**Result:** More accurate budgets, better separation of concerns, and easier maintenance! 🚀
