"""
Data models for Alpaca trading.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


class Quote(BaseModel):
    """Real-time quote for a symbol"""
    symbol: str
    bid_price: float
    bid_size: int
    ask_price: float
    ask_size: int
    last_price: float
    last_size: int
    timestamp: datetime

    @property
    def spread(self) -> float:
        """Bid-ask spread"""
        return self.ask_price - self.bid_price

    @property
    def mid_price(self) -> float:
        """Mid-point between bid and ask"""
        return (self.bid_price + self.ask_price) / 2


class TradeProposal(BaseModel):
    """Proposed trade for user confirmation"""
    symbol: str
    side: Literal["buy", "sell"]
    usd_amount: float
    order_type: Literal["market", "limit"]
    limit_price: Optional[float] = None
    current_price: float
    estimated_shares: float
    rationale: str
    available_funds: float

    def to_summary(self) -> str:
        """Human-readable trade summary"""
        order_desc = f"{self.order_type.upper()} order"
        if self.order_type == "limit":
            order_desc += f" at ${self.limit_price:.2f}"

        return f"""
📊 TRADE PROPOSAL

Symbol: {self.symbol}
Action: {self.side.upper()}
Amount: ${self.usd_amount:,.2f}
Order Type: {order_desc}
Current Price: ${self.current_price:.2f}
Estimated Shares: {self.estimated_shares:.4f}

Available Funds: ${self.available_funds:,.2f}
After Trade: ${self.available_funds - self.usd_amount:,.2f}

Rationale: {self.rationale}
"""


class Order(BaseModel):
    """Placed order details"""
    id: str
    symbol: str
    side: Literal["buy", "sell"]
    notional: float  # USD amount
    order_type: Literal["market", "limit"]
    status: str
    filled_qty: Optional[float] = None
    filled_avg_price: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    def to_summary(self) -> str:
        """Human-readable order summary"""
        status_emoji = {
            "filled": "✅",
            "partially_filled": "⏳",
            "pending_new": "🕐",
            "accepted": "🕐",
            "new": "🕐",
            "canceled": "❌",
            "rejected": "❌"
        }.get(self.status.lower(), "📋")

        summary = f"""
{status_emoji} ORDER {self.status.upper()}

Order ID: {self.id}
Symbol: {self.symbol}
Side: {self.side.upper()}
Notional: ${self.notional:,.2f}
Type: {self.order_type.upper()}
"""

        if self.filled_qty and self.filled_avg_price:
            summary += f"""
Filled: {self.filled_qty:.4f} shares @ ${self.filled_avg_price:.2f}
Total: ${self.filled_qty * self.filled_avg_price:,.2f}
"""

        return summary
