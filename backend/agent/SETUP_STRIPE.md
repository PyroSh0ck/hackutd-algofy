# Stripe Financial Connections Setup

## ⚠️ Security First

**IMPORTANT**: Your Stripe keys were exposed. Please regenerate them:
1. Go to https://dashboard.stripe.com/test/apikeys
2. Click "Reveal test key" on your Secret key
3. Click "Roll key" to generate a new one
4. Use the NEW key below

## Setting Up Your Keys

### Option 1: Environment Variables (Recommended)

Create a file called `secrets.env` in the `backend/agent` folder:

```bash
# Stripe API Keys (TEST MODE)
STRIPE_API_KEY=sk_test_YOUR_NEW_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_PUBLISHABLE_KEY_HERE

# Existing keys
TAVILY_API_KEY=your_tavily_key
OPENROUTER_API_KEY=your_openrouter_key
```

### Option 2: In Notebook

If running on Brev, you can set them in a notebook cell:

```python
import os
os.environ["STRIPE_API_KEY"] = "sk_test_YOUR_NEW_KEY_HERE"
```

## Enabling Financial Connections

To use bank account features, you need to enable Stripe Financial Connections:

1. Go to https://dashboard.stripe.com/test/settings/financialconnections
2. Enable "Financial Connections"
3. This lets you connect to test bank accounts

## Using Test Bank Accounts

Stripe provides test bank accounts for development:

### Test Account Credentials
When connecting a bank account in test mode, use:
- **Bank**: Search for "Test Institution"
- **Username**: `user_good`
- **Password**: `pass_good`

This will give you test accounts with fake transactions to play with!

## Next Steps

Once you've:
1. ✅ Regenerated your keys
2. ✅ Added them to `secrets.env`
3. ✅ Enabled Financial Connections

You can run the financial assistant!

## Testing Connection

Run this to test if everything works:

```python
from stripe_integration import StripeFinancialClient

client = StripeFinancialClient()
print("✅ Stripe connected successfully!")
```
