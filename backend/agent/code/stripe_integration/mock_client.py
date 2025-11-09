"""
Mock Stripe Financial Client for Testing

This simulates Stripe Financial Connections without needing a real bank connection.
Perfect for testing and hackathons!
"""

import logging
from typing import List, Optional
from datetime import datetime, timedelta
import random

from .models import BankAccount, Transaction

_LOGGER = logging.getLogger(__name__)


class MockStripeFinancialClient:
    """
    A simulated Stripe Financial Connections client with fake data.

    Use this when you can't activate a real Stripe account but still want
    to test the Money Manager agent!
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the mock client"""
        self.api_key = api_key
        _LOGGER.info("Mock Stripe Financial Connections client initialized")

        # Create some fake accounts
        self._accounts = self._create_mock_accounts()
        self._transactions = self._create_mock_transactions()

    def _create_mock_accounts(self) -> List[BankAccount]:
        """Create fake bank accounts with realistic data"""
        return [
            BankAccount(
                id="fc_account_checking_123",
                name="Test Checking Account",
                type="checking",
                balance=2450.75,
                currency="USD",
                institution_name="Test Bank",
                last_four="4242"
            ),
            BankAccount(
                id="fc_account_savings_456",
                name="Test Savings Account",
                type="savings",
                balance=8500.00,
                currency="USD",
                institution_name="Test Bank",
                last_four="4343"
            ),
        ]

    def _create_mock_transactions(self) -> List[Transaction]:
        """Create fake transactions for the last 30 days"""
        transactions = []
        now = datetime.now()

        # Simulate various transactions
        mock_transactions_data = [
            # Groceries
            ("Whole Foods", -87.50, "Groceries", 2),
            ("Trader Joe's", -69.30, "Groceries", 5),
            ("Safeway", -45.20, "Groceries", 8),

            # Eating out
            ("Chipotle", -12.50, "Eating Out", 1),
            ("Local Restaurant", -45.00, "Eating Out", 3),
            ("Coffee Shop", -5.75, "Eating Out", 4),
            ("Pizza Place", -28.50, "Eating Out", 6),

            # Transportation
            ("Shell Gas Station", -65.00, "Transportation", 4),
            ("Uber", -18.50, "Transportation", 7),

            # Shopping
            ("Amazon", -89.99, "Shopping", 5),
            ("Target", -45.30, "Shopping", 9),

            # Bills
            ("Electric Company", -120.00, "Bills", 10),
            ("Internet Service", -79.99, "Bills", 12),

            # Subscriptions
            ("Netflix", -15.99, "Subscriptions", 15),
            ("Spotify", -10.99, "Subscriptions", 16),

            # Income
            ("Paycheck Deposit", 2500.00, "Income", 14),
            ("Freelance Payment", 450.00, "Income", 7),
        ]

        for merchant, amount, category, days_ago in mock_transactions_data:
            transaction_date = now - timedelta(days=days_ago)

            # Randomly assign to checking or savings (mostly checking)
            account_id = "fc_account_checking_123" if random.random() > 0.1 else "fc_account_savings_456"

            transactions.append(Transaction(
                id=f"txn_{merchant.replace(' ', '_').lower()}_{days_ago}",
                account_id=account_id,
                date=transaction_date,
                description=merchant,
                amount=amount,
                category=category,
                merchant_name=merchant,
                pending=False
            ))

        return sorted(transactions, key=lambda x: x.date, reverse=True)

    async def get_accounts(self, session_id: str = None) -> List[BankAccount]:
        """
        Get all mock bank accounts.

        Args:
            session_id: Ignored for mock client

        Returns:
            List of fake bank accounts
        """
        _LOGGER.info(f"Retrieved {len(self._accounts)} mock accounts")
        return self._accounts

    async def get_transactions(
        self,
        account_id: str,
        days: int = 30
    ) -> List[Transaction]:
        """
        Get mock transactions for an account.

        Args:
            account_id: The account ID
            days: Number of days of history (default: 30)

        Returns:
            List of fake transactions
        """
        # Filter transactions for this account
        account_transactions = [
            txn for txn in self._transactions
            if txn.account_id == account_id
        ]

        # Filter by date range
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered = [
            txn for txn in account_transactions
            if txn.date >= cutoff_date
        ]

        _LOGGER.info(f"Retrieved {len(filtered)} mock transactions for account {account_id}")
        return filtered

    async def get_balance(self, account_id: str) -> float:
        """
        Get mock balance for an account.

        Args:
            account_id: The account ID

        Returns:
            Current balance in dollars
        """
        account = next(
            (acc for acc in self._accounts if acc.id == account_id),
            None
        )

        if account:
            return account.balance
        return 0.0

    async def transfer_funds(
        self,
        from_account_id: str,
        to_account_id: str,
        amount: float,
        description: str = "Transfer"
    ) -> bool:
        """
        Simulate a transfer between mock accounts.

        Args:
            from_account_id: Source account
            to_account_id: Destination account
            amount: Amount to transfer
            description: Transfer description

        Returns:
            True if successful
        """
        # Find the accounts
        from_account = next(
            (acc for acc in self._accounts if acc.id == from_account_id),
            None
        )
        to_account = next(
            (acc for acc in self._accounts if acc.id == to_account_id),
            None
        )

        if not from_account or not to_account:
            _LOGGER.error("Account not found")
            return False

        if from_account.balance < amount:
            _LOGGER.error("Insufficient funds")
            return False

        # Update balances
        from_account.balance -= amount
        to_account.balance += amount

        # Add transactions to record the transfer
        now = datetime.now()

        self._transactions.append(Transaction(
            id=f"txn_transfer_out_{now.timestamp()}",
            account_id=from_account_id,
            date=now,
            description=f"Transfer to {to_account.name}: {description}",
            amount=-amount,
            category="Transfer",
            merchant_name="Internal Transfer",
            pending=False
        ))

        self._transactions.append(Transaction(
            id=f"txn_transfer_in_{now.timestamp()}",
            account_id=to_account_id,
            date=now,
            description=f"Transfer from {from_account.name}: {description}",
            amount=amount,
            category="Transfer",
            merchant_name="Internal Transfer",
            pending=False
        ))

        _LOGGER.info(f"Transferred ${amount} from {from_account.name} to {to_account.name}")
        return True
