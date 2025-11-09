"""
Banking Tools

Simple functions that the Money Manager agent uses to:
- Check account balances
- View transactions
- Transfer money between accounts

All wrapped with beginner-friendly error handling.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from langchain_core.tools import tool

from financial_agent.shared_state import FinancialState, BankAccount, Transaction
from stripe_integration.client import StripeFinancialClient
from stripe_integration.models import BankAccount as StripeBankAccount, Transaction as StripeTransaction

_LOGGER = logging.getLogger(__name__)


class BankingTools:
    """Collection of tools for banking operations"""

    def __init__(self, stripe_client: StripeFinancialClient):
        self.stripe_client = stripe_client

    @tool
    async def get_all_balances(self, state: FinancialState) -> Dict[str, Any]:
        """
        Get balances for all connected bank accounts.

        Returns a simple summary of how much money the user has in each account.
        """
        try:
            if not state.stripe_session_id:
                return {
                    "success": False,
                    "error": "no_accounts",
                    "message": "No bank accounts connected yet. Please connect accounts first."
                }

            # Get accounts from Stripe
            accounts = await self.stripe_client.get_accounts(state.stripe_session_id)

            if not accounts:
                return {
                    "success": False,
                    "error": "no_accounts",
                    "message": "No accounts found. Please connect your bank."
                }

            # Update state with current accounts
            state.accounts = [
                BankAccount(
                    id=acc.id,
                    name=acc.name,
                    type=acc.type,
                    balance=acc.balance,
                    currency=acc.currency
                )
                for acc in accounts
            ]

            # Calculate total
            total = sum(acc.balance for acc in state.accounts)

            return {
                "success": True,
                "accounts": [
                    {
                        "name": acc.name,
                        "type": acc.type,
                        "balance": acc.balance,
                        "institution": acc.institution_name,
                        "last_four": acc.last_four
                    }
                    for acc in state.accounts
                ],
                "total": total,
                "currency": state.accounts[0].currency if state.accounts else "USD"
            }

        except Exception as e:
            _LOGGER.error(f"Error getting balances: {e}")
            return {
                "success": False,
                "error": "api_error",
                "message": f"Couldn't connect to bank: {str(e)}"
            }

    @tool
    async def get_account_transactions(
        self,
        state: FinancialState,
        account_name: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get recent transactions for an account.

        Args:
            account_name: Name of account (like "Checking") or None for all accounts
            days: How many days of history to get (default: 30)
        """
        try:
            if not state.accounts:
                # Try to load accounts first
                balance_result = await self.get_all_balances(state)
                if not balance_result["success"]:
                    return balance_result

            # Find the account
            target_accounts = []
            if account_name:
                target_accounts = [
                    acc for acc in state.accounts
                    if account_name.lower() in acc.name.lower()
                ]
                if not target_accounts:
                    return {
                        "success": False,
                        "error": "account_not_found",
                        "message": f"Couldn't find account matching '{account_name}'",
                        "available_accounts": [acc.name for acc in state.accounts]
                    }
            else:
                target_accounts = state.accounts

            # Get transactions for each account
            all_transactions = []
            for account in target_accounts:
                transactions = await self.stripe_client.get_transactions(
                    account.id,
                    days=days
                )

                # Convert to our format
                for txn in transactions:
                    all_transactions.append(Transaction(
                        id=txn.id,
                        account_id=txn.account_id,
                        date=txn.date,
                        description=txn.description,
                        amount=txn.amount,
                        category=txn.category,
                        merchant_name=txn.merchant_name,
                        pending=txn.pending
                    ))

            # Update state
            state.recent_transactions = all_transactions

            # Group by category
            by_category = {}
            for txn in all_transactions:
                category = txn.category or "Other"
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append({
                    "description": txn.description,
                    "amount": txn.amount,
                    "date": txn.date.strftime("%b %d, %Y"),
                    "merchant": txn.merchant_name,
                    "pending": txn.pending
                })

            # Calculate totals
            total_spent = sum(abs(txn.amount) for txn in all_transactions if txn.amount < 0)
            total_income = sum(txn.amount for txn in all_transactions if txn.amount > 0)

            return {
                "success": True,
                "account_name": account_name or "All Accounts",
                "days": days,
                "transactions_by_category": by_category,
                "total_spent": total_spent,
                "total_income": total_income,
                "transaction_count": len(all_transactions)
            }

        except Exception as e:
            _LOGGER.error(f"Error getting transactions: {e}")
            return {
                "success": False,
                "error": "api_error",
                "message": f"Couldn't get transactions: {str(e)}"
            }

    @tool
    async def transfer_money(
        self,
        state: FinancialState,
        from_account: str,
        to_account: str,
        amount: float,
        reason: str = "Transfer"
    ) -> Dict[str, Any]:
        """
        Move money from one account to another.

        Args:
            from_account: Name of source account (like "Checking")
            to_account: Name of destination account (like "Savings")
            amount: Amount to move in dollars
            reason: Why this transfer is happening (for records)

        Returns:
            Success/failure with new balances
        """
        try:
            if not state.accounts:
                # Try to load accounts first
                balance_result = await self.get_all_balances(state)
                if not balance_result["success"]:
                    return balance_result

            # Find source account
            source_accounts = [
                acc for acc in state.accounts
                if from_account.lower() in acc.name.lower()
            ]
            if not source_accounts:
                return {
                    "success": False,
                    "error": "account_not_found",
                    "message": f"Couldn't find source account '{from_account}'",
                    "available_accounts": [acc.name for acc in state.accounts]
                }
            source = source_accounts[0]

            # Find destination account
            dest_accounts = [
                acc for acc in state.accounts
                if to_account.lower() in acc.name.lower()
            ]
            if not dest_accounts:
                return {
                    "success": False,
                    "error": "account_not_found",
                    "message": f"Couldn't find destination account '{to_account}'",
                    "available_accounts": [acc.name for acc in state.accounts]
                }
            destination = dest_accounts[0]

            # Check if source has enough money
            if source.balance < amount:
                return {
                    "success": False,
                    "error": "insufficient_funds",
                    "message": f"Not enough money in {source.name}",
                    "current_balance": source.balance,
                    "requested_amount": amount,
                    "shortage": amount - source.balance
                }

            # Calculate what balances will be after transfer
            new_source_balance = source.balance - amount
            new_dest_balance = destination.balance + amount

            # Prepare the transfer summary
            transfer_preview = {
                "from_account": {
                    "name": source.name,
                    "current_balance": source.balance,
                    "after_balance": new_source_balance
                },
                "to_account": {
                    "name": destination.name,
                    "current_balance": destination.balance,
                    "after_balance": new_dest_balance
                },
                "amount": amount,
                "reason": reason
            }

            # Check if user should be warned
            warnings = []
            if new_source_balance < 100:
                warnings.append(f"{source.name} will be low after this transfer (${new_source_balance:.2f})")

            if warnings:
                transfer_preview["warnings"] = warnings

            # Perform the transfer via Stripe
            success = await self.stripe_client.transfer_funds(
                from_account_id=source.id,
                to_account_id=destination.id,
                amount=amount,
                description=reason
            )

            if success:
                # Update local state
                source.balance = new_source_balance
                destination.balance = new_dest_balance

                return {
                    "success": True,
                    "transfer": transfer_preview,
                    "message": f"Successfully moved ${amount:.2f} from {source.name} to {destination.name}"
                }
            else:
                return {
                    "success": False,
                    "error": "api_error",
                    "message": "Transfer failed. Please try again."
                }

        except Exception as e:
            _LOGGER.error(f"Error transferring money: {e}")
            return {
                "success": False,
                "error": "api_error",
                "message": f"Couldn't complete transfer: {str(e)}"
            }

    @tool
    async def get_account_summary(self, state: FinancialState) -> Dict[str, Any]:
        """
        Get a comprehensive overview of all accounts and recent activity.

        Returns everything the user needs to know about their money in one view.
        """
        try:
            # Get balances
            balances = await self.get_all_balances(state)
            if not balances["success"]:
                return balances

            # Get recent transactions (last 30 days)
            transactions = await self.get_account_transactions(state, days=30)

            # Calculate some insights
            total_money = balances["total"]
            accounts_breakdown = balances["accounts"]

            # Spending patterns from transactions
            spending_summary = {}
            if transactions["success"]:
                spending_summary = {
                    "total_spent": transactions["total_spent"],
                    "total_income": transactions["total_income"],
                    "by_category": {
                        category: sum(txn["amount"] for txn in txns)
                        for category, txns in transactions["transactions_by_category"].items()
                    },
                    "transaction_count": transactions["transaction_count"]
                }

            # Check progress on goals
            goal_progress = {}
            if state.user_goals:
                if state.user_goals.emergency_fund_target > 0:
                    # Find savings balance
                    savings = next(
                        (acc for acc in state.accounts if acc.type == "savings"),
                        None
                    )
                    if savings:
                        progress = (savings.balance / state.user_goals.emergency_fund_target) * 100
                        goal_progress["emergency_fund"] = {
                            "current": savings.balance,
                            "target": state.user_goals.emergency_fund_target,
                            "progress_percent": min(progress, 100)
                        }

            return {
                "success": True,
                "total_money": total_money,
                "accounts": accounts_breakdown,
                "spending": spending_summary,
                "goals": goal_progress,
                "currency": balances["currency"]
            }

        except Exception as e:
            _LOGGER.error(f"Error getting account summary: {e}")
            return {
                "success": False,
                "error": "api_error",
                "message": f"Couldn't get summary: {str(e)}"
            }


def create_banking_tools(stripe_client: StripeFinancialClient) -> List[Any]:
    """
    Create all banking tools for use in the agent.

    Args:
        stripe_client: Initialized Stripe Financial Connections client

    Returns:
        List of LangChain tools
    """
    tools_instance = BankingTools(stripe_client)

    return [
        tools_instance.get_all_balances,
        tools_instance.get_account_transactions,
        tools_instance.transfer_money,
        tools_instance.get_account_summary
    ]
