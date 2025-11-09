"""
Personal Finance Assistant - Multi-Agent System

A beginner-friendly financial management system with specialized agents:
- Money Manager: Handle bank accounts and transfers
- Stock Analysis: Analyze markets and recommend investments
- Budget Helper: Create budgets, set goals, track spending
- Main Assistant: Coordinate everything and explain in simple terms
"""

from .orchestrator import (
    create_financial_orchestrator,
    chat_with_financial_assistant,
    OrchestratorState
)
from .shared_state import FinancialState, SavingsGoal
from .banking_agent.agent import create_banking_agent, chat_with_money_manager
from .budget_agent.agent import create_budget_agent, chat_with_budget_helper
from .budget_agent.categories import BudgetCategory

__all__ = [
    "create_financial_orchestrator",
    "chat_with_financial_assistant",
    "OrchestratorState",
    "FinancialState",
    "SavingsGoal",
    "create_banking_agent",
    "chat_with_money_manager",
    "create_budget_agent",
    "chat_with_budget_helper",
    "BudgetCategory"
]
