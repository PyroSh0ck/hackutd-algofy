"""
Budget Helper Agent

Helps users create budgets, set savings goals, and manage spending.
Uses fixed categories to prevent hallucination and ensure consistency.
"""

from .agent import create_budget_agent, chat_with_budget_helper, BudgetAgentState
from .categories import BudgetCategory, CATEGORY_INFO
from .models import (
    SavingsGoal,
    CategoryBudget,
    MonthlyBudget,
    BudgetRecommendation,
    SpendingInsight
)
from .tools import create_budget_tools

__all__ = [
    "create_budget_agent",
    "chat_with_budget_helper",
    "BudgetAgentState",
    "BudgetCategory",
    "CATEGORY_INFO",
    "SavingsGoal",
    "CategoryBudget",
    "MonthlyBudget",
    "BudgetRecommendation",
    "SpendingInsight",
    "create_budget_tools"
]
