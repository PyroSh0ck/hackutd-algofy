"""
Stripe Financial Connections Integration

A beginner-friendly wrapper around Stripe's Financial Connections API.
Provides simple methods to access bank accounts, balances, and transactions.
"""

from .client import StripeFinancialClient
from .models import BankAccount, Transaction

__all__ = ["StripeFinancialClient", "BankAccount", "Transaction"]
