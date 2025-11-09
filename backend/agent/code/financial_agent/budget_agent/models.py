"""
Budget Helper Data Models

Models for budgets, goals, and spending tracking.
"""

from datetime import datetime, date
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .categories import BudgetCategory


class SavingsGoal(BaseModel):
    """A specific savings goal the user wants to achieve"""
    id: str  # Unique identifier
    name: str  # "Trip to Hawaii", "New Car", etc.
    target_amount: float  # How much they need to save
    target_date: date  # When they need it by
    current_saved: float = 0.0  # How much they've saved so far
    monthly_contribution: float = 0.0  # How much to save per month
    priority: int = 1  # 1 = highest priority, 5 = lowest
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    def remaining_amount(self) -> float:
        """How much more they need to save"""
        return max(0, self.target_amount - self.current_saved)

    @property
    def months_until_target(self) -> int:
        """How many months until the target date"""
        today = date.today()
        months = (self.target_date.year - today.year) * 12 + (self.target_date.month - today.month)
        return max(1, months)  # At least 1 month

    @property
    def recommended_monthly(self) -> float:
        """Recommended monthly savings to hit goal"""
        return self.remaining_amount / self.months_until_target

    @property
    def is_achievable(self) -> bool:
        """Whether this goal is on track"""
        return self.monthly_contribution >= self.recommended_monthly

    @property
    def progress_percentage(self) -> float:
        """Progress towards goal as a percentage"""
        if self.target_amount == 0:
            return 100.0
        return min(100.0, (self.current_saved / self.target_amount) * 100)


class CategoryBudget(BaseModel):
    """Budget for a specific category"""
    category: BudgetCategory
    budgeted_amount: float  # How much they plan to spend
    spent_amount: float = 0.0  # How much they've actually spent this month
    last_updated: datetime = Field(default_factory=datetime.now)

    @property
    def remaining(self) -> float:
        """How much budget is left"""
        return self.budgeted_amount - self.spent_amount

    @property
    def is_overspent(self) -> bool:
        """Whether they've gone over budget"""
        return self.spent_amount > self.budgeted_amount

    @property
    def percentage_used(self) -> float:
        """Percentage of budget used"""
        if self.budgeted_amount == 0:
            return 0.0
        return min(100.0, (self.spent_amount / self.budgeted_amount) * 100)


class MonthlyBudget(BaseModel):
    """Complete monthly budget"""
    month: str  # "2025-11" format
    monthly_income: float  # Total income for the month
    categories: Dict[BudgetCategory, CategoryBudget] = {}
    savings_goals: List[SavingsGoal] = []
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

    @property
    def total_budgeted(self) -> float:
        """Total amount budgeted across all categories"""
        return sum(cat.budgeted_amount for cat in self.categories.values())

    @property
    def total_spent(self) -> float:
        """Total amount spent across all categories"""
        return sum(cat.spent_amount for cat in self.categories.values())

    @property
    def total_remaining(self) -> float:
        """Total budget remaining"""
        return self.total_budgeted - self.total_spent

    @property
    def total_savings_goals(self) -> float:
        """Total amount allocated to savings goals"""
        return sum(goal.monthly_contribution for goal in self.savings_goals)

    @property
    def overspent_categories(self) -> List[CategoryBudget]:
        """Categories that are over budget"""
        return [cat for cat in self.categories.values() if cat.is_overspent]

    @property
    def needs_total(self) -> float:
        """Total budgeted for essential needs"""
        from .categories import get_essential_categories
        essentials = get_essential_categories()
        return sum(
            cat.budgeted_amount
            for category, cat in self.categories.items()
            if category in essentials
        )

    @property
    def wants_total(self) -> float:
        """Total budgeted for wants"""
        from .categories import get_wants_categories
        wants = get_wants_categories()
        return sum(
            cat.budgeted_amount
            for category, cat in self.categories.items()
            if category in wants
        )

    @property
    def savings_total(self) -> float:
        """Total budgeted for savings and goals"""
        from .categories import get_savings_categories
        savings = get_savings_categories()
        return sum(
            cat.budgeted_amount
            for category, cat in self.categories.items()
            if category in savings
        ) + self.total_savings_goals

    @property
    def follows_50_30_20(self) -> bool:
        """Check if budget follows the 50/30/20 rule (roughly)"""
        if self.monthly_income == 0:
            return False

        needs_pct = (self.needs_total / self.monthly_income) * 100
        wants_pct = (self.wants_total / self.monthly_income) * 100
        savings_pct = (self.savings_total / self.monthly_income) * 100

        # Allow 10% variance
        return (
            40 <= needs_pct <= 60 and
            20 <= wants_pct <= 40 and
            10 <= savings_pct <= 30
        )


class BudgetRecommendation(BaseModel):
    """AI-generated budget recommendation"""
    recommended_budget: Dict[BudgetCategory, float]  # Category -> Amount
    total_allocated: float
    meets_goals: bool  # Whether this budget achieves all savings goals
    explanation: str  # Human-readable explanation of the budget
    adjustments_made: List[str] = []  # What was adjusted to fit goals
    warnings: List[str] = []  # Warnings about tight budget, unrealistic goals, etc.

    @property
    def needs_total(self) -> float:
        """Total for needs"""
        from .categories import get_essential_categories
        essentials = get_essential_categories()
        return sum(
            amount for category, amount in self.recommended_budget.items()
            if category in essentials
        )

    @property
    def wants_total(self) -> float:
        """Total for wants"""
        from .categories import get_wants_categories
        wants = get_wants_categories()
        return sum(
            amount for category, amount in self.recommended_budget.items()
            if category in wants
        )

    @property
    def savings_total(self) -> float:
        """Total for savings"""
        from .categories import get_savings_categories
        savings = get_savings_categories()
        return sum(
            amount for category, amount in self.recommended_budget.items()
            if category in savings
        )


class SpendingInsight(BaseModel):
    """Insight about user's spending patterns"""
    category: BudgetCategory
    average_monthly: float
    trend: str  # "increasing", "decreasing", "stable"
    comparison: str  # How it compares to typical budgets
    suggestion: str  # Advice for this category
