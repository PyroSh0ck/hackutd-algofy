"""
Budget Helper Tools

Tools for analyzing spending, creating budgets, and managing savings goals.
Uses Money Manager tools to access banking data.
"""

import logging
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from collections import defaultdict

from langchain_core.tools import tool

from financial_agent.shared_state import FinancialState, Transaction
from financial_agent.banking_agent.tools import BankingTools
from stripe_integration.client import StripeFinancialClient
from .categories import (
    BudgetCategory,
    CATEGORY_INFO,
    categorize_transaction,
    get_essential_categories,
    get_wants_categories,
    get_savings_categories,
    BUDGET_RULE_50_30_20
)
from .models import (
    MonthlyBudget,
    CategoryBudget,
    SavingsGoal,
    BudgetRecommendation,
    SpendingInsight
)

_LOGGER = logging.getLogger(__name__)


class BudgetTools:
    """Tools for budget management and goal tracking"""

    def __init__(self, banking_tools: BankingTools):
        """
        Initialize with Money Manager's banking tools.

        Args:
            banking_tools: BankingTools instance from Money Manager
        """
        self.banking_tools = banking_tools

    async def analyze_spending_patterns(
        self,
        state: FinancialState,
        months: int = 3
    ) -> Dict[BudgetCategory, float]:
        """
        Analyze user's spending patterns from transaction history.
        Uses Money Manager to get account data.

        Returns average monthly spending per category.
        """
        _LOGGER.info(f"Analyzing spending patterns for last {months} months")

        # Get accounts from Money Manager if not already loaded
        if not state.accounts:
            balances_result = await self.banking_tools.get_all_balances(state)
            if not balances_result.get("success"):
                _LOGGER.warning("Could not load accounts, using empty data")
                return {}

        # Get transactions from all accounts using Money Manager
        all_transactions: List[Transaction] = []

        for account in state.accounts:
            # Use Money Manager to get transactions
            txn_result = await self.banking_tools.get_account_transactions(
                state,
                account_name=account.name,
                days=months * 30
            )

            if txn_result.get("success") and "transactions" in txn_result:
                # Convert to Transaction objects
                for txn_data in txn_result["transactions"]:
                    all_transactions.append(Transaction(
                        id=txn_data.get("id", ""),
                        date=datetime.fromisoformat(txn_data["date"]) if isinstance(txn_data["date"], str) else txn_data["date"],
                        description=txn_data.get("description", ""),
                        amount=txn_data.get("amount", 0),
                        category=txn_data.get("category"),
                        account_id=account.id,
                        is_expense=txn_data.get("amount", 0) < 0
                    ))

        # Categorize transactions
        spending_by_category: Dict[BudgetCategory, List[float]] = defaultdict(list)

        for txn in all_transactions:
            # Only count expenses (negative amounts)
            if txn.amount < 0:
                category = categorize_transaction(
                    txn.merchant_name or txn.description,
                    txn.description
                )
                spending_by_category[category].append(abs(txn.amount))

        # Calculate average monthly spending per category
        average_spending: Dict[BudgetCategory, float] = {}

        for category, amounts in spending_by_category.items():
            total = sum(amounts)
            average = total / months
            average_spending[category] = round(average, 2)

        _LOGGER.info(f"Found spending in {len(average_spending)} categories")
        return average_spending

    async def create_budget_recommendation(
        self,
        state: FinancialState,
        monthly_income: float,
        savings_goals: List[SavingsGoal] = None
    ) -> BudgetRecommendation:
        """
        Create a budget recommendation based on:
        - User's income
        - Historical spending patterns
        - Savings goals
        - 50/30/20 rule

        Returns a complete budget with explanations.
        """
        _LOGGER.info(f"Creating budget recommendation for income: ${monthly_income}")

        if savings_goals is None:
            savings_goals = []

        # Analyze current spending
        avg_spending = await self.analyze_spending_patterns(state)

        # Calculate totals needed for goals
        total_goal_savings = sum(goal.monthly_contribution for goal in savings_goals)

        # Apply 50/30/20 rule
        needs_budget = monthly_income * BUDGET_RULE_50_30_20["needs"]
        wants_budget = monthly_income * BUDGET_RULE_50_30_20["wants"]
        savings_budget = monthly_income * BUDGET_RULE_50_30_20["savings"]

        recommended: Dict[BudgetCategory, float] = {}
        adjustments: List[str] = []
        warnings: List[str] = []

        # 1. Allocate NEEDS (50% of income)
        essential_categories = get_essential_categories()
        essential_spending = {
            cat: avg_spending.get(cat, 0)
            for cat in essential_categories
        }

        total_essentials = sum(essential_spending.values())

        # If essentials exceed 50%, warn and use actual amounts
        if total_essentials > needs_budget:
            warnings.append(
                f"Your essential expenses (${total_essentials:.2f}) are more than 50% "
                f"of your income. This leaves less for wants and savings."
            )
            for cat, amount in essential_spending.items():
                recommended[cat] = amount
            adjustments.append("Used actual spending for essentials (they're over 50%)")
        else:
            # Essentials fit in budget, use them
            for cat, amount in essential_spending.items():
                recommended[cat] = amount

        # 2. Allocate SAVINGS GOALS (part of 20% savings)
        savings_categories = get_savings_categories()

        # Emergency fund - always allocate if not at target
        emergency_target = monthly_income * 3  # 3 months of income
        current_emergency = sum(acc.balance for acc in state.accounts if "savings" in acc.name.lower())

        if current_emergency < emergency_target:
            emergency_monthly = min(
                monthly_income * 0.10,  # 10% of income
                (emergency_target - current_emergency) / 6  # Build over 6 months
            )
            recommended[BudgetCategory.EMERGENCY_FUND] = round(emergency_monthly, 2)
            adjustments.append(f"Building emergency fund: ${emergency_monthly:.2f}/month")
        else:
            recommended[BudgetCategory.EMERGENCY_FUND] = 0

        # Retirement - 5% of income
        recommended[BudgetCategory.RETIREMENT] = round(monthly_income * 0.05, 2)

        # User's savings goals
        recommended[BudgetCategory.SAVINGS_GOALS] = round(total_goal_savings, 2)

        # Check if savings goals are achievable
        total_savings_allocated = sum(
            recommended.get(cat, 0)
            for cat in savings_categories
        ) + total_goal_savings

        if total_savings_allocated > savings_budget:
            warnings.append(
                f"Your savings goals (${total_savings_allocated:.2f}) exceed 20% of income. "
                f"You may need to adjust timelines or reduce spending elsewhere."
            )

        # 3. Allocate WANTS (30% of income)
        wants_categories = get_wants_categories()
        wants_spending = {
            cat: avg_spending.get(cat, 0)
            for cat in wants_categories
        }

        total_wants = sum(wants_spending.values())

        # Available for wants = income - needs - savings
        available_for_wants = monthly_income - sum(
            recommended.get(cat, 0)
            for cat in essential_categories
        ) - total_savings_allocated

        # If wants are over budget, scale them down proportionally
        if total_wants > available_for_wants:
            scale_factor = available_for_wants / total_wants if total_wants > 0 else 1
            for cat, amount in wants_spending.items():
                recommended[cat] = round(amount * scale_factor, 2)
            adjustments.append(
                f"Reduced non-essential spending by {(1-scale_factor)*100:.0f}% to fit budget"
            )
        else:
            # Wants fit in budget
            for cat, amount in wants_spending.items():
                recommended[cat] = amount

        # 4. Handle remaining categories
        for category in BudgetCategory:
            if category not in recommended:
                recommended[category] = avg_spending.get(category, 0)

        # Calculate totals
        total_allocated = sum(recommended.values())

        # Check if we meet all goals
        meets_goals = total_savings_allocated >= total_goal_savings

        # Generate explanation
        explanation = self._generate_budget_explanation(
            monthly_income,
            recommended,
            savings_goals,
            meets_goals
        )

        return BudgetRecommendation(
            recommended_budget=recommended,
            total_allocated=round(total_allocated, 2),
            meets_goals=meets_goals,
            explanation=explanation,
            adjustments_made=adjustments,
            warnings=warnings
        )

    def _generate_budget_explanation(
        self,
        income: float,
        budget: Dict[BudgetCategory, float],
        goals: List[SavingsGoal],
        meets_goals: bool
    ) -> str:
        """Generate a human-readable explanation of the budget"""

        # Calculate percentages
        needs = sum(budget.get(cat, 0) for cat in get_essential_categories())
        wants = sum(budget.get(cat, 0) for cat in get_wants_categories())
        savings = sum(budget.get(cat, 0) for cat in get_savings_categories())

        needs_pct = (needs / income * 100) if income > 0 else 0
        wants_pct = (wants / income * 100) if income > 0 else 0
        savings_pct = (savings / income * 100) if income > 0 else 0

        explanation = f"""
Your Monthly Budget (${income:,.2f} income):

📊 Budget Breakdown:
  • Needs (essentials): ${needs:,.2f} ({needs_pct:.0f}%)
  • Wants (fun stuff): ${wants:,.2f} ({wants_pct:.0f}%)
  • Savings & Goals: ${savings:,.2f} ({savings_pct:.0f}%)

🎯 Your Savings Goals:
"""

        if goals:
            for goal in goals:
                progress = (goal.current_saved / goal.target_amount * 100) if goal.target_amount > 0 else 0
                explanation += f"  • {goal.name}: ${goal.current_saved:,.2f} / ${goal.target_amount:,.2f} ({progress:.0f}%)\n"
                explanation += f"    Saving ${goal.monthly_contribution:,.2f}/month → Target: {goal.target_date.strftime('%B %Y')}\n"
        else:
            explanation += "  (No specific goals set yet)\n"

        if meets_goals:
            explanation += "\n✅ This budget will help you reach your goals on time!"
        else:
            explanation += "\n⚠️ To meet your goals, you may need to earn more or adjust your timeline."

        return explanation

    @tool
    async def create_budget(self, state: FinancialState, monthly_income: float) -> Dict[str, Any]:
        """
        Create a personalized budget based on your income and spending.

        Args:
            monthly_income: Your total monthly income

        Returns:
            A complete budget with amounts for each category
        """
        try:
            # Create budget recommendation
            recommendation = await self.create_budget_recommendation(
                state,
                monthly_income,
                state.current_budget.savings_goals if state.current_budget else []
            )

            return {
                "success": True,
                "budget": {
                    category.value: amount
                    for category, amount in recommendation.recommended_budget.items()
                    if amount > 0
                },
                "explanation": recommendation.explanation,
                "adjustments": recommendation.adjustments_made,
                "warnings": recommendation.warnings,
                "follows_50_30_20": recommendation.meets_goals
            }

        except Exception as e:
            _LOGGER.error(f"Error creating budget: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    @tool
    async def add_savings_goal(
        self,
        state: FinancialState,
        goal_name: str,
        target_amount: float,
        target_date_str: str
    ) -> Dict[str, Any]:
        """
        Add a new savings goal and automatically adjust your budget.

        Args:
            goal_name: What you're saving for (e.g., "Trip to Hawaii")
            target_amount: How much you need (e.g., 1000)
            target_date_str: When you need it (e.g., "2026-05-01")

        Returns:
            Updated budget with new goal included
        """
        try:
            # Parse target date
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()

            # Create the goal
            goal = SavingsGoal(
                id=f"goal_{len(state.user_goals.savings_goals if hasattr(state.user_goals, 'savings_goals') else [])}",
                name=goal_name,
                target_amount=target_amount,
                target_date=target_date,
                monthly_contribution=0  # Will be calculated
            )

            # Calculate recommended monthly contribution
            months_until = goal.months_until_target
            recommended_monthly = goal.recommended_monthly

            goal.monthly_contribution = recommended_monthly

            # Add to state
            if not hasattr(state.user_goals, 'savings_goals'):
                state.user_goals.savings_goals = []
            state.user_goals.savings_goals.append(goal)

            # Recreate budget with new goal
            if state.user_goals.monthly_income > 0:
                recommendation = await self.create_budget_recommendation(
                    state,
                    state.user_goals.monthly_income,
                    state.user_goals.savings_goals
                )

                return {
                    "success": True,
                    "goal": {
                        "name": goal.name,
                        "target": goal.target_amount,
                        "target_date": goal.target_date.strftime("%B %d, %Y"),
                        "monthly_needed": recommended_monthly,
                        "months_until": months_until
                    },
                    "updated_budget": {
                        category.value: amount
                        for category, amount in recommendation.recommended_budget.items()
                        if amount > 0
                    },
                    "explanation": recommendation.explanation,
                    "warnings": recommendation.warnings
                }
            else:
                return {
                    "success": True,
                    "goal": {
                        "name": goal.name,
                        "target": goal.target_amount,
                        "target_date": goal.target_date.strftime("%B %d, %Y"),
                        "monthly_needed": recommended_monthly,
                        "months_until": months_until
                    },
                    "message": "Goal added! Set your monthly income to get a complete budget."
                }

        except Exception as e:
            _LOGGER.error(f"Error adding savings goal: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    @tool
    async def view_budget(self, state: FinancialState) -> Dict[str, Any]:
        """
        View your current budget and how you're doing.

        Returns:
            Current budget with spending vs budgeted for each category
        """
        if not state.current_budget:
            return {
                "success": False,
                "message": "No budget set yet. Create one first!"
            }

        budget = state.current_budget

        categories_status = []
        for category, cat_budget in budget.categories.items():
            categories_status.append({
                "category": category.value,
                "budgeted": cat_budget.budgeted_amount,
                "spent": cat_budget.spent_amount,
                "remaining": cat_budget.remaining,
                "percentage_used": cat_budget.percentage_used,
                "over_budget": cat_budget.is_overspent
            })

        return {
            "success": True,
            "month": budget.month,
            "income": budget.monthly_income,
            "total_budgeted": budget.total_budgeted,
            "total_spent": budget.total_spent,
            "total_remaining": budget.total_remaining,
            "categories": categories_status,
            "savings_goals": [
                {
                    "name": goal.name,
                    "target": goal.target_amount,
                    "saved": goal.current_saved,
                    "remaining": goal.remaining_amount,
                    "monthly": goal.monthly_contribution,
                    "progress": goal.progress_percentage
                }
                for goal in budget.savings_goals
            ],
            "overspent_categories": [
                cat.category.value for cat in budget.overspent_categories
            ]
        }


def create_budget_tools(banking_tools: BankingTools) -> List:
    """
    Create the budget helper tools.

    Args:
        banking_tools: BankingTools instance from Money Manager

    Returns:
        List of budget tools that use Money Manager for data access
    """
    tools_instance = BudgetTools(banking_tools)

    return [
        tools_instance.create_budget,
        tools_instance.add_savings_goal,
        tools_instance.view_budget
    ]
