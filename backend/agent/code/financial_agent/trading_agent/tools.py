"""
Trading Agent Tools

Tools for checking quotes, analyzing available funds, and proposing trades.
"""

import logging
from typing import Any, Dict
from langchain_core.tools import tool

from financial_agent.shared_state import FinancialState
from alpaca_trading.client import AlpacaTradingClient
from financial_agent.banking_agent.tools import BankingTools
from financial_agent.budget_agent.tools import BudgetTools

_LOGGER = logging.getLogger(__name__)


class TradingTools:
    """Tools for stock trading with budget integration"""

    def __init__(
        self,
        alpaca_client: AlpacaTradingClient,
        banking_tools: BankingTools,
        budget_tools: BudgetTools
    ):
        """
        Initialize trading tools.

        Args:
            alpaca_client: Alpaca client for market data and trading
            banking_tools: Banking tools to check account balances
            budget_tools: Budget tools to check available funds
        """
        self.alpaca = alpaca_client
        self.banking = banking_tools
        self.budget = budget_tools

    @tool
    async def get_stock_quote(self, state: FinancialState, symbol: str) -> Dict[str, Any]:
        """
        Get the latest real-time quote for a stock symbol.

        Args:
            state: Current financial state
            symbol: Stock symbol (e.g., "SPY", "AAPL", "VOO")

        Returns:
            Dictionary with current price, bid, ask, and spread
        """
        try:
            quote = await self.alpaca.get_latest_quote(symbol.upper())

            return {
                "success": True,
                "symbol": quote.symbol,
                "current_price": quote.last_price,
                "bid": quote.bid_price,
                "ask": quote.ask_price,
                "spread": quote.spread,
                "mid_price": quote.mid_price,
                "timestamp": quote.timestamp.isoformat(),
                "message": f"Current price for {quote.symbol}: ${quote.last_price:.2f} "
                           f"(Bid: ${quote.bid_price:.2f}, Ask: ${quote.ask_price:.2f})"
            }
        except Exception as e:
            _LOGGER.error(f"Error fetching quote for {symbol}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Could not fetch quote for {symbol}. Make sure it's a valid stock symbol."
            }

    @tool
    async def check_available_funds(self, state: FinancialState) -> Dict[str, Any]:
        """
        Check available funds for investing.

        This checks:
        1. Current account balances (from Money Manager)
        2. Current budget and allocated savings (from Budget Helper)
        3. Excess funds available for investing

        Args:
            state: Current financial state

        Returns:
            Dictionary with available funds breakdown
        """
        try:
            # Get current balances
            balances_result = await self.banking.get_all_balances(state)

            if not balances_result.get("success"):
                return {
                    "success": False,
                    "message": "Could not check account balances."
                }

            total_balance = balances_result.get("total_balance", 0)

            # Check budget
            available_for_investment = 0
            budget_message = ""

            if state.current_budget:
                # Calculate excess funds = savings allocation - current goals
                savings_allocated = state.current_budget.monthly_income * 0.20  # 20% for savings

                # Subtract existing goals
                goal_allocations = sum(
                    goal.monthly_contribution
                    for goal in state.current_budget.savings_goals
                )

                available_for_investment = savings_allocated - goal_allocations

                budget_message = f"""
Based on your budget:
- Monthly savings allocation: ${savings_allocated:.2f}
- Current savings goals: ${goal_allocations:.2f}
- Available for investing: ${available_for_investment:.2f}/month
"""
            else:
                # No budget - suggest using 20% of total balance as conservative estimate
                available_for_investment = total_balance * 0.20
                budget_message = f"""
You don't have a budget set up yet. As a conservative estimate:
- Total balance: ${total_balance:.2f}
- Suggested max investment (20% of balance): ${available_for_investment:.2f}
"""

            return {
                "success": True,
                "total_balance": total_balance,
                "available_for_investment": max(0, available_for_investment),
                "has_budget": state.current_budget is not None,
                "message": budget_message
            }

        except Exception as e:
            _LOGGER.error(f"Error checking available funds: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Could not check available funds."
            }

    @tool
    async def propose_trade(
        self,
        state: FinancialState,
        symbol: str,
        usd_amount: float,
        rationale: str,
        order_type: str = "market"
    ) -> Dict[str, Any]:
        """
        Propose a trade for user confirmation.

        This creates a detailed trade proposal showing:
        - Current price and estimated shares
        - Available funds and impact on budget
        - Investment rationale

        Args:
            state: Current financial state
            symbol: Stock symbol to trade
            usd_amount: USD amount to invest
            rationale: Why this is a good investment (from stock analysis)
            order_type: "market" or "limit" (default: market)

        Returns:
            Trade proposal requiring user confirmation
        """
        try:
            # Check available funds
            funds_check = await self.check_available_funds(state)

            if not funds_check.get("success"):
                return funds_check

            available_funds = funds_check["available_for_investment"]

            # Warn if amount exceeds available funds
            if usd_amount > available_funds:
                return {
                    "success": False,
                    "requires_confirmation": False,
                    "message": f"""
⚠️ INSUFFICIENT FUNDS

You want to invest ${usd_amount:.2f}, but you only have ${available_funds:.2f} available.

{funds_check['message']}

Would you like to:
1. Invest the maximum available amount (${available_funds:.2f})?
2. Create or adjust your budget to allocate more for investing?
"""
                }

            # Create trade proposal
            proposal = await self.alpaca.create_trade_proposal(
                symbol=symbol,
                side="buy",
                usd_amount=usd_amount,
                order_type=order_type,
                rationale=rationale,
                available_funds=available_funds
            )

            # Store proposal in state for confirmation
            state.pending_trade_proposal = proposal

            return {
                "success": True,
                "requires_confirmation": True,
                "proposal": proposal.model_dump(),
                "message": proposal.to_summary() + "\n\n**Reply 'CONFIRM TRADE' to execute this order.**"
            }

        except Exception as e:
            _LOGGER.error(f"Error creating trade proposal: {e}")
            return {
                "success": False,
                "requires_confirmation": False,
                "error": str(e),
                "message": f"Could not create trade proposal: {e}"
            }

    @tool
    async def execute_trade(self, state: FinancialState) -> Dict[str, Any]:
        """
        Execute the pending trade proposal.

        This should ONLY be called after user explicitly confirms.

        Args:
            state: Current financial state (must have pending_trade_proposal)

        Returns:
            Order confirmation or error
        """
        if not hasattr(state, 'pending_trade_proposal') or not state.pending_trade_proposal:
            return {
                "success": False,
                "message": "No pending trade to execute. Please create a trade proposal first."
            }

        proposal = state.pending_trade_proposal

        try:
            # Place the order
            order = await self.alpaca.place_order(
                symbol=proposal.symbol,
                side=proposal.side,
                notional=proposal.usd_amount,
                order_type=proposal.order_type,
                limit_price=proposal.limit_price
            )

            # Clear pending proposal
            state.pending_trade_proposal = None

            return {
                "success": True,
                "order": order.model_dump(),
                "message": order.to_summary() + "\n\nTrade executed successfully! 🎉"
            }

        except Exception as e:
            _LOGGER.error(f"Error executing trade: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Could not execute trade: {e}"
            }


def create_trading_tools(
    alpaca_client: AlpacaTradingClient,
    banking_tools: BankingTools,
    budget_tools: BudgetTools
) -> list:
    """
    Create trading tools list for LangChain.

    Args:
        alpaca_client: Alpaca trading client
        banking_tools: Banking tools instance
        budget_tools: Budget tools instance

    Returns:
        List of trading tools
    """
    tools_instance = TradingTools(alpaca_client, banking_tools, budget_tools)

    return [
        tools_instance.get_stock_quote,
        tools_instance.check_available_funds,
        tools_instance.propose_trade,
        tools_instance.execute_trade
    ]
