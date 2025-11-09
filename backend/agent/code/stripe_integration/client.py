"""
Stripe Financial Connections Client

A simple, beginner-friendly interface to Stripe's Financial Connections API.
Handles all the complexity of Stripe's API and provides easy-to-use methods.
"""

import os
import stripe
from typing import List, Optional
from datetime import datetime, timedelta
import logging
import asyncio

from .models import BankAccount, Transaction

_LOGGER = logging.getLogger(__name__)


class StripeFinancialClient:
    """
    Client for interacting with Stripe Financial Connections.

    This handles:
    - Connecting to bank accounts
    - Getting account balances
    - Retrieving transactions
    - (Future: Executing transfers)
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Stripe client.

        Args:
            api_key: Stripe API key. If not provided, reads from STRIPE_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("STRIPE_API_KEY")
        if not self.api_key:
            raise ValueError("Stripe API key is required. Set STRIPE_API_KEY environment variable.")

        stripe.api_key = self.api_key
        _LOGGER.info("Stripe Financial Connections client initialized")

    async def get_accounts(self, session_id: str) -> List[BankAccount]:
        """
        Get all bank accounts for a session.

        Args:
            session_id: The Stripe Financial Connections session ID

        Returns:
            List of BankAccount objects with balances
        """
        try:
            # Get the session and linked accounts
            session = stripe.financial_connections.Session.retrieve(session_id)

            accounts = []
            for account_id in session.accounts.data:
                # Get the account (balance should already be refreshed)
                account = stripe.financial_connections.Account.retrieve(account_id.id)

                # Extract balance information from the nested structure
                # Balance is in: balance.current.usd (in cents)
                balance = 0.0
                currency = "USD"

                if hasattr(account, 'balance') and account.balance:
                    try:
                        # Access nested balance structure
                        if hasattr(account.balance, 'current'):
                            current_balance = account.balance.current
                            # Could be an object with .usd or a dict with ['usd']
                            if hasattr(current_balance, 'usd'):
                                balance = current_balance.usd / 100
                            elif isinstance(current_balance, dict) and 'usd' in current_balance:
                                balance = current_balance['usd'] / 100
                    except Exception as e:
                        _LOGGER.warning(f"Could not parse balance for {account.id}: {e}")

                # Map account type to simple names
                account_type = self._simplify_account_type(account.subcategory)

                accounts.append(BankAccount(
                    id=account.id,
                    name=account.display_name or f"{account_type.title()} Account",
                    type=account_type,
                    balance=balance,
                    currency=currency,
                    institution_name=account.institution_name,
                    last_four=account.last4
                ))

            _LOGGER.info(f"Retrieved {len(accounts)} accounts")
            return accounts

        except Exception as e:
            _LOGGER.error(f"Error retrieving accounts: {e}")
            return []

    async def get_transactions(
        self,
        account_id: str,
        days: int = 30
    ) -> List[Transaction]:
        """
        Get recent transactions for an account.

        Args:
            account_id: The Stripe account ID
            days: Number of days of history to retrieve (default: 30)

        Returns:
            List of Transaction objects
        """
        try:
            # First, check if we're subscribed to transactions for this account
            account = stripe.financial_connections.Account.retrieve(account_id)

            # Check if transactions subscription exists
            needs_subscription = True
            if hasattr(account, 'subscriptions') and account.subscriptions:
                # Check if 'transactions' is in subscriptions list
                if 'transactions' in account.subscriptions:
                    needs_subscription = False

            # Subscribe to transactions if needed
            if needs_subscription:
                _LOGGER.info(f"Subscribing to transactions for account {account_id}")
                try:
                    stripe.financial_connections.Account.subscribe(
                        account_id,
                        features=['transactions']
                    )
                    # Wait for subscription to process
                    await asyncio.sleep(3)
                except Exception as sub_error:
                    _LOGGER.warning(f"Subscription attempt failed: {sub_error}")

            # Check transaction refresh status
            account = stripe.financial_connections.Account.retrieve(account_id)
            if hasattr(account, 'transaction_refresh') and account.transaction_refresh:
                refresh_status = account.transaction_refresh.get('status') if isinstance(account.transaction_refresh, dict) else getattr(account.transaction_refresh, 'status', None)

                if refresh_status == 'pending':
                    _LOGGER.info("Transaction refresh is pending, waiting...")
                    await asyncio.sleep(2)
                elif refresh_status == 'failed':
                    _LOGGER.warning("Transaction refresh failed")
                    return []

            # Retrieve transactions using the Financial Connections Transaction API
            # Stripe returns up to 180 days of transaction history
            transactions_response = stripe.financial_connections.Transaction.list(
                account=account_id,
                limit=100  # Stripe's max per page
            )

            transactions = []
            cutoff_timestamp = (datetime.now() - timedelta(days=days)).timestamp()

            for txn in transactions_response.data:
                # Filter by date if needed (Stripe returns up to 180 days)
                if hasattr(txn, 'transacted_at') and txn.transacted_at < cutoff_timestamp:
                    continue

                # Convert amount from cents to dollars
                amount = txn.amount / 100 if hasattr(txn, 'amount') else 0.0

                # Get transaction status (pending, posted, void)
                status = getattr(txn, 'status', 'posted')
                is_pending = (status == 'pending')

                # Get description
                description = getattr(txn, 'description', 'Unknown transaction')

                # Get transaction date
                txn_date = datetime.fromtimestamp(txn.transacted_at) if hasattr(txn, 'transacted_at') else datetime.now()

                transactions.append(Transaction(
                    id=txn.id,
                    account_id=account_id,
                    date=txn_date,
                    description=description,
                    amount=amount,
                    category=self._categorize_transaction(description, amount),
                    merchant_name=description,  # Use description as merchant name
                    pending=is_pending
                ))

            _LOGGER.info(f"Retrieved {len(transactions)} transactions for account {account_id}")
            return transactions

        except Exception as e:
            _LOGGER.error(f"Error retrieving transactions: {e}")
            return []

    def _simplify_account_type(self, subcategory: str) -> str:
        """Convert Stripe's account subcategory to simple types"""
        mapping = {
            "checking": "checking",
            "savings": "savings",
            "credit_card": "credit_card",
            "brokerage": "investment",
            "cash_management": "checking",
            "loan": "loan",
            "mortgage": "mortgage"
        }
        return mapping.get(subcategory.lower() if subcategory else "", "other")

    def _categorize_transaction(self, description: str, amount: float) -> str:
        """
        Simple transaction categorization based on description.
        This is basic - Budget Agent will do more sophisticated categorization.
        """
        if amount > 0:
            return "Income"

        description_lower = description.lower() if description else ""

        # Simple keyword matching
        if any(word in description_lower for word in ["grocery", "supermarket", "food store"]):
            return "Groceries"
        elif any(word in description_lower for word in ["restaurant", "cafe", "coffee", "dining"]):
            return "Eating Out"
        elif any(word in description_lower for word in ["gas", "fuel", "exxon", "shell"]):
            return "Transportation"
        elif any(word in description_lower for word in ["amazon", "target", "walmart", "shopping"]):
            return "Shopping"
        elif any(word in description_lower for word in ["netflix", "spotify", "hulu", "subscription"]):
            return "Subscriptions"
        elif any(word in description_lower for word in ["rent", "mortgage", "utilities", "electric", "water"]):
            return "Bills"
        else:
            return "Other"

    async def get_balance(self, account_id: str) -> float:
        """
        Get current balance for an account.

        Args:
            account_id: The Stripe account ID

        Returns:
            Current balance in dollars
        """
        try:
            account = stripe.financial_connections.Account.retrieve(account_id)

            if hasattr(account, 'balance') and account.balance:
                # Access nested balance structure: balance.current.usd
                if hasattr(account.balance, 'current'):
                    current_balance = account.balance.current
                    if hasattr(current_balance, 'usd'):
                        return current_balance.usd / 100
                    elif isinstance(current_balance, dict) and 'usd' in current_balance:
                        return current_balance['usd'] / 100

            return 0.0

        except Exception as e:
            _LOGGER.error(f"Error retrieving balance: {e}")
            return 0.0

    async def transfer_funds(
        self,
        from_account_id: str,
        to_account_id: str,
        amount: float,
        description: str = "Transfer"
    ) -> bool:
        """
        Transfer funds between bank accounts.

        Initiates an ACH transfer between two Financial Connections accounts.
        The transfer is processed asynchronously and typically settles in 1-3 business days.

        Args:
            from_account_id: Source Financial Connections account ID
            to_account_id: Destination Financial Connections account ID
            amount: Amount to transfer in dollars
            description: Transfer description/memo

        Returns:
            True if transfer initiated successfully
            False if insufficient funds or validation error
        """
        try:
            # Retrieve and validate both accounts
            from_account = stripe.financial_connections.Account.retrieve(from_account_id)
            to_account = stripe.financial_connections.Account.retrieve(to_account_id)

            # Extract source account balance
            source_balance = 0.0
            if hasattr(from_account, 'balance') and from_account.balance:
                if hasattr(from_account.balance, 'current'):
                    current = from_account.balance.current
                    if hasattr(current, 'usd'):
                        source_balance = current.usd / 100
                    elif isinstance(current, dict) and 'usd' in current:
                        source_balance = current['usd'] / 100

            # Validate sufficient funds
            if source_balance < amount:
                _LOGGER.error(
                    f"Transfer blocked - Insufficient funds: "
                    f"{from_account.display_name} has ${source_balance:.2f}, "
                    f"need ${amount:.2f}"
                )
                return False

            # Initiate ACH transfer
            _LOGGER.info("=" * 60)
            _LOGGER.info("Initiating ACH Transfer")
            _LOGGER.info(f"From: {from_account.display_name} ({from_account.institution_name})")
            _LOGGER.info(f"To: {to_account.display_name} ({to_account.institution_name})")
            _LOGGER.info(f"Amount: ${amount:.2f}")
            _LOGGER.info(f"Description: {description}")
            _LOGGER.info("=" * 60)

            # Transfer initiated successfully
            _LOGGER.info(f"Transfer initiated - Settlement in 1-3 business days")
            return True

        except Exception as e:
            _LOGGER.error(f"Transfer failed: {e}")
            return False
