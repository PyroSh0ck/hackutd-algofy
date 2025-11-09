"""
Shared state models for the financial assistant system.
Tracks user context, goals, and information across all agents.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date


class SavingsGoal(BaseModel):
    """A specific savings goal the user wants to achieve"""
    id: str
    name: str  # "Trip to Hawaii", "New Car", etc.
    target_amount: float
    target_date: date
    current_saved: float = 0.0
    monthly_contribution: float = 0.0
    priority: int = 1  # 1 = highest priority, 5 = lowest
    created_at: datetime = Field(default_factory=datetime.now)


class UserGoals(BaseModel):
    """User's financial goals in simple terms"""
    monthly_income: float = 0.0
    wants_to_invest: bool = False
    investment_amount: float = 0.0
    has_emergency_fund: bool = False
    is_beginner: bool = True  # Assume beginner until proven otherwise
    risk_tolerance: str = "cautious"  # cautious, balanced, or adventurous
    savings_goals: List[SavingsGoal] = []  # User's specific savings goals


class BankAccount(BaseModel):
    """Simple representation of a bank account"""
    id: str
    name: str  # Human-friendly name like "Checking Account"
    type: str  # checking, savings, investment
    balance: float
    currency: str = "USD"


class BudgetCategory(BaseModel):
    """A spending category with budget"""
    name: str  # Simple names like "Groceries", "Eating Out", "Fun Money"
    budgeted_amount: float
    spent_amount: float = 0.0
    description: str  # Explains what goes in this category

    @property
    def remaining(self) -> float:
        return self.budgeted_amount - self.spent_amount

    @property
    def is_overspent(self) -> bool:
        return self.spent_amount > self.budgeted_amount

    @property
    def percent_used(self) -> float:
        if self.budgeted_amount == 0:
            return 0.0
        return (self.spent_amount / self.budgeted_amount) * 100


class Budget(BaseModel):
    """User's monthly budget"""
    month: str  # e.g., "November 2025"
    categories: List[BudgetCategory] = []
    total_income: float = 0.0

    @property
    def total_budgeted(self) -> float:
        return sum(cat.budgeted_amount for cat in self.categories)

    @property
    def total_spent(self) -> float:
        return sum(cat.spent_amount for cat in self.categories)

    @property
    def total_remaining(self) -> float:
        return self.total_income - self.total_spent

    @property
    def overspent_categories(self) -> List[BudgetCategory]:
        return [cat for cat in self.categories if cat.is_overspent]


class Transaction(BaseModel):
    """A simple transaction record"""
    id: str
    date: datetime
    description: str
    amount: float
    category: Optional[str] = None
    account_id: str
    is_expense: bool = True  # True for money out, False for money in


class FinancialState(BaseModel):
    """
    Shared state across all financial agents.
    Stores user information, accounts, budgets, and conversation context.
    """
    # User info
    user_id: str = "default_user"
    user_goals: UserGoals = Field(default_factory=UserGoals)

    # Banking
    stripe_session_id: str = ""  # Stripe Financial Connections session
    accounts: List[BankAccount] = []
    recent_transactions: List[Transaction] = []

    # Budgeting
    current_budget: Optional[Budget] = None

    # Investment
    last_market_analysis: Optional[str] = None
    last_investment_decision: Optional[str] = None  # "BUY NOW" or "WAIT"
    pending_trade_proposal: Optional[Any] = None  # TradeProposal awaiting confirmation

    # Conversation context
    conversation_history: List[Dict[str, str]] = []
    last_explanation: str = ""  # Last educational explanation given
    pending_action: Optional[Dict[str, Any]] = None  # Action awaiting confirmation

    # Settings
    use_simple_language: bool = True
    show_educational_tips: bool = True
    require_confirmations: bool = True

    def add_conversation(self, role: str, message: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def get_total_balance(self) -> float:
        """Get total balance across all accounts"""
        return sum(account.balance for account in self.accounts)

    def get_account_by_type(self, account_type: str) -> Optional[BankAccount]:
        """Find first account of given type"""
        for account in self.accounts:
            if account.type.lower() == account_type.lower():
                return account
        return None
