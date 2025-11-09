"""
Trading Agent

Handles stock trading with human-in-the-loop confirmation.
Integrates with:
- Alpaca for real-time quotes and order execution
- Budget system to check available funds
- Stock analysis for investment recommendations
"""

from .agent import create_trading_agent, TradingAgentState

__all__ = ["create_trading_agent", "TradingAgentState"]
