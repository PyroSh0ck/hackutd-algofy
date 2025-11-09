"""
Simple data models for Stripe Financial Connections
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class BankAccount(BaseModel):
    """A bank account from Stripe"""
    id: str
    name: str
    type: str  # checking, savings, credit_card, etc.
    balance: float
    currency: str = "USD"
    institution_name: Optional[str] = None
    last_four: Optional[str] = None  # Last 4 digits of account number


class Transaction(BaseModel):
    """A transaction from a bank account"""
    id: str
    account_id: str
    date: datetime
    description: str
    amount: float  # Positive = money in, Negative = money out
    category: Optional[str] = None
    merchant_name: Optional[str] = None
    pending: bool = False
