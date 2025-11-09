"""
Test Stripe Financial Connections Setup

This script helps you:
1. Create a Financial Connections session
2. Connect test bank accounts
3. Verify everything works

Run this first to set up your test data!
"""

import os
import stripe
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../secrets.env")
load_dotenv("../variables.env")

def test_stripe_connection():
    """Test basic Stripe connection"""
    stripe_key = os.getenv("STRIPE_API_KEY")

    if not stripe_key:
        print("❌ STRIPE_API_KEY not found in environment variables")
        print("   Add it to backend/agent/secrets.env")
        return False

    if not stripe_key.startswith("sk_test_"):
        print("⚠️  Warning: You're not using a test key!")
        print("   Test keys start with 'sk_test_'")
        return False

    stripe.api_key = stripe_key
    print("✅ Stripe API key loaded")
    return True


def create_test_session():
    """Create a Financial Connections session for testing"""
    print("\n" + "="*60)
    print("Creating Financial Connections Session...")
    print("="*60)

    try:
        # First, create a test customer
        print("Creating test customer...")
        customer = stripe.Customer.create(
            name="Test User",
            email="test@example.com",
        )
        print(f"✅ Customer created: {customer.id}\n")

        # Now create the Financial Connections session
        print("Creating Financial Connections session...")
        session = stripe.financial_connections.Session.create(
            account_holder={
                "type": "customer",
                "customer": customer.id,
            },
            permissions=["balances", "transactions", "payment_method"],
            filters={"countries": ["US"]},
        )

        print(f"\n✅ Session created successfully!")
        print(f"\nSession ID: {session.id}")
        print(f"\n📋 SAVE THIS SESSION ID - You'll need it!")
        print(f"\n🔗 To connect test bank accounts, open this URL:")
        print(f"   {session.url}")
        print(f"\n📝 When prompted, use these test credentials:")
        print(f"   Bank: Search for 'Test Institution'")
        print(f"   Username: user_good")
        print(f"   Password: pass_good")
        print(f"\n💡 Stripe will give you fake checking and savings accounts to test with!")

        return session.id

    except stripe.error.StripeError as e:
        print(f"\n❌ Error creating session: {e}")
        return None


def list_connected_accounts(session_id):
    """List accounts connected to a session"""
    print("\n" + "="*60)
    print("Checking Connected Accounts...")
    print("="*60)

    try:
        session = stripe.financial_connections.Session.retrieve(session_id)

        if not session.accounts or len(session.accounts.data) == 0:
            print("\n⚠️  No accounts connected yet")
            print("   Open the URL above and connect test accounts first!")
            return

        print(f"\n✅ Found {len(session.accounts.data)} connected accounts:\n")

        for account in session.accounts.data:
            # Get full account details
            full_account = stripe.financial_connections.Account.retrieve(account.id)

            balance = "N/A"
            if hasattr(full_account, 'balance') and full_account.balance:
                balance = f"${full_account.balance.current / 100:.2f}"

            print(f"  📊 {full_account.display_name or 'Account'}")
            print(f"     Type: {full_account.subcategory}")
            print(f"     Balance: {balance}")
            print(f"     Last 4: {full_account.last4}")
            print(f"     ID: {full_account.id}")
            print()

        return True

    except stripe.error.StripeError as e:
        print(f"\n❌ Error retrieving accounts: {e}")
        return False


def main():
    print("="*60)
    print("STRIPE FINANCIAL CONNECTIONS TEST")
    print("="*60)

    # Step 1: Test connection
    if not test_stripe_connection():
        return

    # Step 2: Ask what to do
    print("\nWhat would you like to do?")
    print("1. Create a new test session (first time setup)")
    print("2. Check accounts on existing session")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        session_id = create_test_session()
        if session_id:
            print(f"\n💾 Save this session ID: {session_id}")
            print("   Open the URL, connect accounts, then run this script again with option 2")

    elif choice == "2":
        session_id = input("\nEnter your session ID: ").strip()
        list_connected_accounts(session_id)

    else:
        print("Invalid choice")

    print("\n" + "="*60)
    print("Done!")
    print("="*60)


if __name__ == "__main__":
    main()
