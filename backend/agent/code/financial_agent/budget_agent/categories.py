"""
Standard Budget Categories

Fixed categories to prevent hallucination and ensure consistency.
These are based on common spending patterns and financial best practices.
"""

from enum import Enum
from typing import Dict, List
from pydantic import BaseModel, Field


class BudgetCategory(str, Enum):
    """
    Standard budget categories - NEVER create new ones.

    These are the ONLY categories allowed for budgeting.
    """
    # Essential/Needs (50% of income)
    HOUSING = "Housing"  # Rent, mortgage, property tax
    UTILITIES = "Utilities"  # Electric, gas, water, internet, phone
    GROCERIES = "Groceries"  # Food for home cooking
    TRANSPORTATION = "Transportation"  # Gas, car payment, insurance, maintenance, public transit
    INSURANCE = "Insurance"  # Health, life, disability (not car/home - those are in other categories)
    MINIMUM_DEBT = "Minimum Debt Payments"  # Minimum payments on credit cards, loans

    # Wants (30% of income)
    EATING_OUT = "Eating Out"  # Restaurants, takeout, delivery, coffee shops
    ENTERTAINMENT = "Entertainment"  # Movies, streaming, concerts, hobbies
    SHOPPING = "Shopping"  # Clothes, electronics, non-essential purchases
    SUBSCRIPTIONS = "Subscriptions"  # Streaming services, gym, memberships
    PERSONAL_CARE = "Personal Care"  # Haircuts, cosmetics, spa

    # Savings & Goals (20% of income)
    EMERGENCY_FUND = "Emergency Fund"  # 3-6 months of expenses
    RETIREMENT = "Retirement"  # 401k, IRA, etc.
    SAVINGS_GOALS = "Savings Goals"  # Trip, car, house down payment, etc.
    EXTRA_DEBT = "Extra Debt Payments"  # Above minimum payments

    # Other
    UNCATEGORIZED = "Other"  # Everything else


class CategoryInfo(BaseModel):
    """Information about a budget category"""
    name: BudgetCategory
    description: str
    typical_percentage: float  # Typical % of income for this category
    is_essential: bool  # True for needs, False for wants
    examples: List[str] = []


# Category metadata
CATEGORY_INFO: Dict[BudgetCategory, CategoryInfo] = {
    BudgetCategory.HOUSING: CategoryInfo(
        name=BudgetCategory.HOUSING,
        description="Your home costs like rent or mortgage",
        typical_percentage=30.0,
        is_essential=True,
        examples=["Rent", "Mortgage payment", "Property tax", "HOA fees"]
    ),
    BudgetCategory.UTILITIES: CategoryInfo(
        name=BudgetCategory.UTILITIES,
        description="Bills to keep your home running",
        typical_percentage=5.0,
        is_essential=True,
        examples=["Electric bill", "Gas/heating", "Water", "Internet", "Phone bill"]
    ),
    BudgetCategory.GROCERIES: CategoryInfo(
        name=BudgetCategory.GROCERIES,
        description="Food you buy to cook at home",
        typical_percentage=10.0,
        is_essential=True,
        examples=["Supermarket", "Whole Foods", "Trader Joe's", "Costco"]
    ),
    BudgetCategory.TRANSPORTATION: CategoryInfo(
        name=BudgetCategory.TRANSPORTATION,
        description="Getting around - car or public transit",
        typical_percentage=15.0,
        is_essential=True,
        examples=["Gas", "Car payment", "Car insurance", "Metro card", "Uber", "Parking"]
    ),
    BudgetCategory.INSURANCE: CategoryInfo(
        name=BudgetCategory.INSURANCE,
        description="Protection for your health and life",
        typical_percentage=5.0,
        is_essential=True,
        examples=["Health insurance", "Life insurance", "Disability insurance"]
    ),
    BudgetCategory.MINIMUM_DEBT: CategoryInfo(
        name=BudgetCategory.MINIMUM_DEBT,
        description="Required monthly payments on debts",
        typical_percentage=5.0,
        is_essential=True,
        examples=["Credit card minimum", "Student loan payment", "Personal loan"]
    ),
    BudgetCategory.EATING_OUT: CategoryInfo(
        name=BudgetCategory.EATING_OUT,
        description="Restaurants and takeout",
        typical_percentage=10.0,
        is_essential=False,
        examples=["Restaurants", "Fast food", "Coffee shops", "Delivery", "Doordash"]
    ),
    BudgetCategory.ENTERTAINMENT: CategoryInfo(
        name=BudgetCategory.ENTERTAINMENT,
        description="Fun activities and hobbies",
        typical_percentage=5.0,
        is_essential=False,
        examples=["Movies", "Concerts", "Games", "Sports tickets", "Hobbies"]
    ),
    BudgetCategory.SHOPPING: CategoryInfo(
        name=BudgetCategory.SHOPPING,
        description="Clothes and things you want but don't need",
        typical_percentage=10.0,
        is_essential=False,
        examples=["Clothes", "Electronics", "Amazon", "Target", "Home decor"]
    ),
    BudgetCategory.SUBSCRIPTIONS: CategoryInfo(
        name=BudgetCategory.SUBSCRIPTIONS,
        description="Monthly services and memberships",
        typical_percentage=3.0,
        is_essential=False,
        examples=["Netflix", "Spotify", "Gym membership", "Amazon Prime"]
    ),
    BudgetCategory.PERSONAL_CARE: CategoryInfo(
        name=BudgetCategory.PERSONAL_CARE,
        description="Taking care of yourself",
        typical_percentage=2.0,
        is_essential=False,
        examples=["Haircuts", "Salon", "Cosmetics", "Skincare"]
    ),
    BudgetCategory.EMERGENCY_FUND: CategoryInfo(
        name=BudgetCategory.EMERGENCY_FUND,
        description="Money saved for unexpected problems",
        typical_percentage=10.0,
        is_essential=True,
        examples=["Savings account transfer", "Emergency savings"]
    ),
    BudgetCategory.RETIREMENT: CategoryInfo(
        name=BudgetCategory.RETIREMENT,
        description="Saving for when you stop working",
        typical_percentage=5.0,
        is_essential=True,
        examples=["401k", "IRA", "Roth IRA"]
    ),
    BudgetCategory.SAVINGS_GOALS: CategoryInfo(
        name=BudgetCategory.SAVINGS_GOALS,
        description="Saving for specific things you want",
        typical_percentage=5.0,
        is_essential=True,
        examples=["Vacation fund", "New car fund", "House down payment"]
    ),
    BudgetCategory.EXTRA_DEBT: CategoryInfo(
        name=BudgetCategory.EXTRA_DEBT,
        description="Paying extra to get rid of debt faster",
        typical_percentage=5.0,
        is_essential=True,
        examples=["Extra credit card payment", "Extra student loan payment"]
    ),
    BudgetCategory.UNCATEGORIZED: CategoryInfo(
        name=BudgetCategory.UNCATEGORIZED,
        description="Other expenses that don't fit elsewhere",
        typical_percentage=5.0,
        is_essential=False,
        examples=["Gifts", "Donations", "Misc"]
    ),
}


def get_essential_categories() -> List[BudgetCategory]:
    """Get all essential (needs) categories"""
    return [
        cat for cat, info in CATEGORY_INFO.items()
        if info.is_essential and cat not in [BudgetCategory.EMERGENCY_FUND, BudgetCategory.RETIREMENT, BudgetCategory.SAVINGS_GOALS, BudgetCategory.EXTRA_DEBT]
    ]


def get_wants_categories() -> List[BudgetCategory]:
    """Get all wants categories"""
    return [
        cat for cat, info in CATEGORY_INFO.items()
        if not info.is_essential
    ]


def get_savings_categories() -> List[BudgetCategory]:
    """Get all savings/goals categories"""
    return [
        BudgetCategory.EMERGENCY_FUND,
        BudgetCategory.RETIREMENT,
        BudgetCategory.SAVINGS_GOALS,
        BudgetCategory.EXTRA_DEBT
    ]


def categorize_transaction(merchant: str, description: str) -> BudgetCategory:
    """
    Categorize a transaction based on merchant and description.

    Uses keyword matching to assign to one of the standard categories.
    """
    text = f"{merchant} {description}".lower()

    # Housing
    if any(word in text for word in ["rent", "mortgage", "property tax", "hoa"]):
        return BudgetCategory.HOUSING

    # Utilities
    if any(word in text for word in ["electric", "pg&e", "gas", "water", "internet", "comcast", "verizon", "at&t", "t-mobile", "phone bill"]):
        return BudgetCategory.UTILITIES

    # Groceries
    if any(word in text for word in ["grocery", "supermarket", "whole foods", "trader joe", "safeway", "kroger", "walmart grocery", "costco", "target grocery"]):
        return BudgetCategory.GROCERIES

    # Transportation
    if any(word in text for word in ["gas", "shell", "chevron", "bp", "exxon", "uber", "lyft", "parking", "metro", "transit", "car payment", "auto insurance"]):
        return BudgetCategory.TRANSPORTATION

    # Insurance
    if any(word in text for word in ["health insurance", "life insurance", "disability insurance", "insurance premium"]) and "auto" not in text and "car" not in text:
        return BudgetCategory.INSURANCE

    # Minimum Debt
    if any(word in text for word in ["credit card payment", "loan payment", "student loan", "minimum payment"]):
        return BudgetCategory.MINIMUM_DEBT

    # Eating Out
    if any(word in text for word in ["restaurant", "cafe", "coffee", "starbucks", "chipotle", "mcdonald", "pizza", "doordash", "uber eats", "grubhub", "takeout"]):
        return BudgetCategory.EATING_OUT

    # Entertainment
    if any(word in text for word in ["movie", "cinema", "netflix", "spotify", "hulu", "concert", "theater", "game", "steam", "xbox", "playstation"]):
        return BudgetCategory.ENTERTAINMENT

    # Shopping
    if any(word in text for word in ["amazon", "target", "walmart", "best buy", "clothing", "clothes", "apparel", "electronics"]):
        return BudgetCategory.SHOPPING

    # Subscriptions
    if any(word in text for word in ["subscription", "membership", "gym", "planet fitness", "amazon prime"]):
        return BudgetCategory.SUBSCRIPTIONS

    # Personal Care
    if any(word in text for word in ["salon", "haircut", "barber", "spa", "cosmetic", "sephora", "ulta"]):
        return BudgetCategory.PERSONAL_CARE

    # Savings/Transfers
    if any(word in text for word in ["transfer to savings", "emergency fund", "401k", "ira", "retirement"]):
        if "emergency" in text:
            return BudgetCategory.EMERGENCY_FUND
        elif "retirement" in text or "401k" in text or "ira" in text:
            return BudgetCategory.RETIREMENT
        else:
            return BudgetCategory.SAVINGS_GOALS

    # Default to uncategorized
    return BudgetCategory.UNCATEGORIZED


# 50/30/20 Rule - Financial best practice
BUDGET_RULE_50_30_20 = {
    "needs": 0.50,  # Essential expenses
    "wants": 0.30,  # Non-essential spending
    "savings": 0.20,  # Savings and debt payoff
}
