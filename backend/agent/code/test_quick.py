"""
Quick test script for Financial Assistant
Run this to test the complete system
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment
load_dotenv("secrets.env")
load_dotenv("variables.env")

from financial_agent import chat_with_financial_assistant, FinancialState


async def main():
    """Test the Financial Assistant with all features"""

    print("=" * 60)
    print("Financial Assistant - Quick Test")
    print("=" * 60)

    # Create state
    state = FinancialState(
        user_id="test_user",
        stripe_session_id=os.getenv("STRIPE_SESSION_ID", "")
    )

    # Check if we have required env vars
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY not found in secrets.env")
        return

    if not os.getenv("STRIPE_SESSION_ID"):
        print("⚠️  STRIPE_SESSION_ID not found - some features may be limited")
        print("   Run: jupyter notebook stripe_setup_clean.ipynb")
    else:
        print(f"✅ Stripe session: {os.getenv('STRIPE_SESSION_ID')[:30]}...")

    print("✅ Financial Assistant initialized!\n")

    # Test questions
    questions = [
        ("How much money do I have?", "Banking"),
        ("What did I spend on this week?", "Banking"),
        ("Help me create a budget for $3000 income", "Budget"),
        ("I want to save $1000 for a trip in May 2026", "Budget"),
    ]

    for question, agent_type in questions:
        print("\n" + "=" * 60)
        print(f"TEST: {agent_type}")
        print("=" * 60)
        print(f"\nYou: {question}\n")

        try:
            response = await chat_with_financial_assistant(question, state)
            print(f"Assistant:\n{response}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
