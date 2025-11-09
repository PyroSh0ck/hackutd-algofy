# New Agents Guide

## Overview

Three new utility agents have been added to enhance the Financial Assistant system:

1. **User Prompt Agent** - Guides users through multi-step workflows
2. **Email Agent** - Sends notifications and reports via email
3. **Response Agent** - Formats responses for optimal readability

---

## 1. User Prompt Agent

### Purpose
Provides interactive, guided prompts to help users through complex workflows.

### Use Cases

```
✅ Onboarding new users
✅ Collecting information for budget setup
✅ Guiding investment decisions
✅ Confirming multi-step actions
✅ Providing contextual help
```

### Example Usage

```python
from financial_agent.prompt_agent import chat_with_prompt_assistant
from financial_agent.prompt_agent.agent import PromptTemplates

# Start budget setup workflow
response = await chat_with_prompt_assistant(
    user_message="I want to create a budget",
    state=financial_state,
    config=config,
    workflow_type="budget_setup"
)

# Or use pre-built templates
budget_prompt = PromptTemplates.budget_setup_start()
print(budget_prompt)
```

### Pre-Built Templates

#### Budget Setup
```python
PromptTemplates.budget_setup_start()
# Guides user through:
# 1. Monthly income
# 2. Major expenses
# 3. Savings goals
```

#### Investment Guidance
```python
PromptTemplates.investment_guide_start()
# Asks about:
# 1. Emergency fund status
# 2. Investment amount
# 3. Investment timeline/goals
```

#### Trade Confirmation
```python
PromptTemplates.trade_confirmation(symbol="SPY", amount=500, action="buy")
# Confirms:
# - Correct symbol
# - Correct amount
# - User readiness
```

#### Bank Connection Guide
```python
PromptTemplates.bank_connection_guide()
# Explains:
# - What's needed
# - Step-by-step process
# - Security features
```

### Workflow State Tracking

The agent tracks multi-step workflows:

```python
class PromptAgentState(FinancialState):
    workflow_type: str = ""          # "budget_setup", "investment_guide", etc.
    collected_data: Dict[str, Any] = {}  # Data gathered so far
    current_step: int = 0             # Current step in workflow
    total_steps: int = 0              # Total steps in workflow
```

---

## 2. Email Agent

### Purpose
Sends professional HTML emails for notifications, confirmations, and reports.

### Email Types

#### 1. Trade Confirmations

```python
from financial_agent.email_agent import send_trade_confirmation

await send_trade_confirmation(
    to_email="user@example.com",
    trade_data={
        "order_id": "abc-123",
        "symbol": "SPY",
        "side": "buy",
        "filled_qty": 0.6834,
        "filled_avg_price": 585.22,
        "total_amount": 400.00,
        "status": "filled"
    }
)
```

**Email Preview:**
```
✅ Trade Executed Successfully

Order Details:
┌────────────────┬──────────────────┐
│ Order ID       │ abc-123          │
│ Symbol         │ SPY              │
│ Action         │ BUY              │
│ Shares         │ 0.6834           │
│ Average Price  │ $585.22          │
│ Total Amount   │ $400.00          │
│ Status         │ FILLED           │
└────────────────┴──────────────────┘
```

#### 2. Budget Summaries

```python
from financial_agent.email_agent import send_budget_summary

await send_budget_summary(
    to_email="user@example.com",
    budget_data={
        "month": "January 2025",
        "total_income": 3000.00,
        "needs_budget": 1500.00,
        "needs_spent": 1200.00,
        "needs_remaining": 300.00,
        "needs_percent": 80.0,
        # ... wants and savings data
        "goals": [
            {"name": "Hawaii Trip", "current": 500, "target": 1000},
            {"name": "Emergency Fund", "current": 2000, "target": 5000}
        ]
    }
)
```

#### 3. Weekly Spending Reports

```python
from financial_agent.email_agent import send_weekly_spending_report

await send_weekly_spending_report(
    to_email="user@example.com",
    spending_data={
        "week_start": "Jan 1, 2025",
        "week_end": "Jan 7, 2025",
        "total_spent": 450.00,
        "categories": [
            {"name": "Groceries", "amount": 150.00, "percent": 33.3},
            {"name": "Eating Out", "amount": 100.00, "percent": 22.2},
            # ...
        ],
        "notable_transactions": [
            {"date": "Jan 3", "description": "Whole Foods", "amount": 85.50},
            # ...
        ],
        "alert_message": "You're on track this week!"
    }
)
```

#### 4. Investment Alerts

```python
from financial_agent.email_agent import send_investment_alert

await send_investment_alert(
    to_email="user@example.com",
    alert_data={
        "type": "success",  # or "warning", "info"
        "title": "Portfolio Update",
        "message": "Your portfolio has grown 5% this month!",
        "portfolio_value": 5250.00,
        "total_invested": 5000.00,
        "gain_loss": 250.00,
        "return_percent": 5.0
    }
)
```

### Email Configuration

Set these environment variables:

```bash
# Gmail example
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Use app-specific password
SMTP_FROM_EMAIL=noreply@financial-assistant.com

# User's email
USER_EMAIL=user@example.com
```

### Custom Email Sending

```python
from financial_agent.email_agent import send_email

await send_email(
    to_email="user@example.com",
    subject="Custom Notification",
    html_content="<h1>Hello!</h1><p>Custom email body</p>"
)
```

---

## 3. Response Agent

### Purpose
Formats raw data into beautiful, user-friendly responses with appropriate tone and context.

### Quick Formatting

```python
from financial_agent.response_agent import format_response

# Format account balances
formatted = format_response(
    data=[
        {"name": "Checking", "type": "checking", "balance": 2500.00},
        {"name": "Savings", "type": "savings", "balance": 5000.00}
    ],
    response_type="balances",
    tone="casual"
)

print(formatted)
```

**Output:**
```
💰 **Your Accounts**

```
Account              Type            Balance
----------------------------------------------------
Checking             checking       $2,500.00
Savings              savings        $5,000.00
----------------------------------------------------
TOTAL                               $7,500.00
```
```

### Response Types

#### 1. Account Balances

```python
format_response(
    data=[...],
    response_type="balances"
)
```

#### 2. Budget Summary

```python
format_response(
    data={
        "month": "January 2025",
        "total_income": 3000,
        "needs_budget": 1500,
        "needs_spent": 1200,
        # ...
    },
    response_type="budget"
)
```

**Output:**
```
📊 **Budget Summary - January 2025**

**Income:** $3,000.00
**Spent:** $1,200.00
**Remaining:** $1,800.00

**50/30/20 Breakdown:**

✅ **NEEDS (50%)**
   Budgeted: $1,500.00 | Spent: $1,200.00
   [████████████████░░░░] 80.0%

✅ **WANTS (30%)**
   ...
```

#### 3. Transactions

```python
format_response(
    data=[
        {"date": "2025-01-05", "description": "Whole Foods", "amount": 85.50, "category": "Groceries"},
        # ...
    ],
    response_type="transactions"
)
```

#### 4. Trade Proposal

```python
format_response(
    data={
        "symbol": "SPY",
        "side": "buy",
        "usd_amount": 400.00,
        "order_type": "market",
        "current_price": 585.22,
        "estimated_shares": 0.6834,
        "available_funds": 400.00,
        "rationale": "Market conditions favorable..."
    },
    response_type="trade_proposal"
)
```

#### 5. Stock Quote

```python
format_response(
    data={
        "symbol": "SPY",
        "current_price": 585.22,
        "bid": 585.20,
        "ask": 585.25,
        "spread": 0.05,
        "timestamp": "2025-01-09T14:30:00Z"
    },
    response_type="stock_quote"
)
```

**Output:**
```
📈 **SPY** - Real-Time Quote

```
Last Price:  $585.22
Bid:         $585.20
Ask:         $585.25
Spread:      $0.05
As of:       2025-01-09T14:30:00Z
```
```

#### 6. Investment Recommendation

```python
format_response(
    data={
        "decision": "BUY",
        "reasoning": "Market showing positive momentum...",
        "confidence": "high"
    },
    response_type="investment"
)
```

**Output:**
```
✅ **Investment Recommendation: BUY**

**Confidence:** High

**Analysis:**
Market showing positive momentum...

💡 **Next Steps:**
1. Check your available funds
2. Decide how much to invest
3. Say 'Buy $X of [SYMBOL]' to proceed
```

#### 7. Savings Goals

```python
format_response(
    data=[
        {
            "name": "Hawaii Trip",
            "current_saved": 500,
            "target_amount": 1000,
            "target_date": "May 2026",
            "monthly_contribution": 100
        },
        # ...
    ],
    response_type="savings_goals"
)
```

**Output:**
```
🎯 **Your Savings Goals**

**Hawaii Trip**
   [███████████████░░░░░░░░░░░░░░░] 50.0%
   $500.00 of $1,000.00
   $100.00/month • Target: May 2026
```

#### 8. Error Messages

```python
format_response(
    data={
        "type": "Insufficient Funds",
        "message": "You don't have enough money to complete this trade.",
        "suggestions": [
            "Check your available balance",
            "Reduce the investment amount",
            "Transfer money from savings"
        ]
    },
    response_type="error"
)
```

#### 9. Success Messages

```python
format_response(
    data={
        "message": "Budget created successfully!",
        "details": {
            "Monthly Income": "$3,000",
            "Categories": "3 (Needs, Wants, Savings)",
            "Goals": "2 savings goals"
        }
    },
    response_type="success"
)
```

#### 10. Help Menu

```python
format_response(
    data={},
    response_type="help"
)
```

### Tone Adjustment

The Response Agent supports three tones:

#### Casual (Default)
```python
format_response(data, response_type="balances", tone="casual")
# Uses emojis, exclamation marks, friendly language
# "Great! You have $2,500 in checking!"
```

#### Educational
```python
format_response(data, response_type="balances", tone="educational")
# Adds learning tips and explanations
# "You have $2,500 in checking. 💡 Learn More: Ask me 'Why?' and I'll explain!"
```

#### Formal
```python
format_response(data, response_type="balances", tone="formal")
# Professional, minimal emojis, no exclamations
# "Your checking account balance is $2,500."
```

---

## Integration with Main System

### Using in Orchestrator

```python
from financial_agent.prompt_agent import chat_with_prompt_assistant
from financial_agent.email_agent import send_trade_confirmation
from financial_agent.response_agent import format_response

async def handle_user_request(user_query: str, state: FinancialState):
    # 1. Guide user if needed
    if "help" in user_query.lower() or "how" in user_query.lower():
        response = await chat_with_prompt_assistant(
            user_message=user_query,
            state=state,
            config=config
        )
        return response

    # 2. Process request (e.g., get balances)
    balances = await get_balances(state)

    # 3. Format response
    formatted = format_response(
        data=balances,
        response_type="balances",
        tone=state.use_simple_language and "casual" or "formal"
    )

    # 4. Send email if requested
    if "email" in user_query.lower():
        await send_email(
            to_email=state.user_email,
            subject="Your Account Balances",
            html_content=formatted
        )

    return formatted
```

---

## Environment Variables Summary

Add these to your `secrets.env`:

```bash
# SMTP Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@financial-assistant.com

# User Email
USER_EMAIL=user@example.com
```

---

## Examples

### Complete Workflow: Budget Setup with Email Confirmation

```python
# 1. Guide user through setup
from financial_agent.prompt_agent.agent import PromptTemplates

prompt = PromptTemplates.budget_setup_start()
# User provides: income=$3000, rent=$1200, goals=[Hawaii trip]

# 2. Create budget
budget_data = create_budget(income=3000, rent=1200)

# 3. Format confirmation
from financial_agent.response_agent import format_response

formatted = format_response(
    data=budget_data,
    response_type="budget",
    tone="educational"
)

# 4. Send email confirmation
from financial_agent.email_agent import send_budget_summary

await send_budget_summary(
    to_email="user@example.com",
    budget_data=budget_data
)

# 5. Return to user
return formatted + "\n\n✉️ I've also emailed you a copy!"
```

### Complete Workflow: Investment with Email Notification

```python
# 1. Get investment recommendation
analysis = await analyze_market("SPY")

# 2. Format recommendation
recommendation = format_response(
    data=analysis,
    response_type="investment",
    tone="casual"
)

# User decides to invest

# 3. Guide trade confirmation
from financial_agent.prompt_agent.agent import PromptTemplates

confirmation = PromptTemplates.trade_confirmation(
    symbol="SPY",
    amount=400,
    action="buy"
)

# User confirms

# 4. Execute trade
order = await execute_trade(symbol="SPY", amount=400)

# 5. Send email confirmation
from financial_agent.email_agent import send_trade_confirmation

await send_trade_confirmation(
    to_email="user@example.com",
    trade_data=order
)

# 6. Format response
response = format_response(
    data=order,
    response_type="success",
    tone="casual"
)

return response + "\n\n✉️ Confirmation email sent!"
```

---

## Best Practices

### 1. User Prompt Agent
- Use for complex, multi-step workflows
- Provide escape routes ("Type CANCEL to stop")
- Track progress (Step 2 of 5)
- Use templates for consistency

### 2. Email Agent
- Always ask for confirmation before sending (unless subscribed)
- Use appropriate templates for each type
- Include actionable next steps
- Keep emails concise but informative

### 3. Response Agent
- Match tone to user preferences
- Use appropriate formatter for data type
- Add context and next steps
- Be consistent with formatting style

---

## Summary

These three agents work together to enhance the user experience:

1. **Prompt Agent** guides users through complex tasks
2. **Email Agent** keeps users informed via email
3. **Response Agent** makes all responses beautiful and clear

All three integrate seamlessly with the existing Financial Assistant system!
