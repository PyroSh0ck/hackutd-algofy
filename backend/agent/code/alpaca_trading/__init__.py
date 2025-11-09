"""
Alpaca Trading Integration

Provides real-time market data and paper trading capabilities.
"""

from .client import AlpacaTradingClient
from .models import Quote, Order, TradeProposal

__all__ = ["AlpacaTradingClient", "Quote", "Order", "TradeProposal"]
