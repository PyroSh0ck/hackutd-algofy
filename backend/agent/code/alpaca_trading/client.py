"""
Alpaca Trading Client

Provides real-time market data and paper trading using Alpaca Market Data v2 API.

Features:
- Fetch latest quotes (bid/ask + last trade)
- Place fractional orders by USD notional
- Paper trading environment
- Human-in-the-loop trade confirmation

Future Enhancement: Switch to WebSocket streaming for real-time updates
"""

import os
import logging
from datetime import datetime
from typing import Optional
import httpx

from .models import Quote, Order, TradeProposal

_LOGGER = logging.getLogger(__name__)


class AlpacaTradingClient:
    """
    Client for Alpaca Market Data v2 and Trading API.

    Uses Paper Trading environment by default.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        paper: bool = True
    ):
        """
        Initialize Alpaca client.

        Args:
            api_key: Alpaca API key (defaults to ALPACA_API_KEY env var)
            api_secret: Alpaca API secret (defaults to ALPACA_API_SECRET env var)
            paper: Use paper trading (default True)
        """
        self.api_key = api_key or os.getenv("ALPACA_API_KEY")
        self.api_secret = api_secret or os.getenv("ALPACA_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise ValueError(
                "Alpaca API credentials required. "
                "Set ALPACA_API_KEY and ALPACA_API_SECRET environment variables."
            )

        # API endpoints
        if paper:
            self.trading_base_url = "https://paper-api.alpaca.markets"
        else:
            self.trading_base_url = "https://api.alpaca.markets"

        self.data_base_url = "https://data.alpaca.markets"

        # HTTP client
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret,
        }

        _LOGGER.info(f"Alpaca client initialized (paper={paper})")

    async def get_latest_quote(self, symbol: str) -> Quote:
        """
        Fetch the latest quote for a symbol.

        Uses Alpaca Market Data v2 API:
        GET /v2/stocks/{symbol}/quotes/latest

        Args:
            symbol: Stock symbol (e.g., "SPY", "AAPL")

        Returns:
            Quote with bid, ask, and last trade

        Future: Switch to WebSocket for streaming quotes:
            wss://stream.data.alpaca.markets/v2/stocks
        """
        url = f"{self.data_base_url}/v2/stocks/{symbol.upper()}/quotes/latest"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

        quote_data = data["quote"]

        return Quote(
            symbol=symbol.upper(),
            bid_price=quote_data["bp"],
            bid_size=quote_data["bs"],
            ask_price=quote_data["ap"],
            ask_size=quote_data["as"],
            last_price=quote_data.get("p", quote_data["ap"]),  # Use ask if no last
            last_size=quote_data.get("s", 0),
            timestamp=datetime.fromisoformat(quote_data["t"].replace("Z", "+00:00"))
        )

    async def get_account(self) -> dict:
        """Get account information including buying power"""
        url = f"{self.trading_base_url}/v2/account"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def place_order(
        self,
        symbol: str,
        side: str,
        notional: float,
        order_type: str = "market",
        limit_price: Optional[float] = None
    ) -> Order:
        """
        Place a fractional order by USD notional amount.

        Args:
            symbol: Stock symbol
            side: "buy" or "sell"
            notional: USD amount to trade
            order_type: "market" or "limit"
            limit_price: Limit price (required if order_type="limit")

        Returns:
            Order confirmation

        Note: Uses `notional` parameter to trade in dollars, not shares.
              Alpaca automatically handles fractional shares.
        """
        if order_type == "limit" and not limit_price:
            raise ValueError("limit_price required for limit orders")

        url = f"{self.trading_base_url}/v2/orders"

        order_data = {
            "symbol": symbol.upper(),
            "side": side.lower(),
            "type": order_type.lower(),
            "time_in_force": "day",
            "notional": str(notional),  # USD amount
        }

        if order_type == "limit":
            order_data["limit_price"] = str(limit_price)

        _LOGGER.info(f"Placing order: {order_data}")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json=order_data
            )
            response.raise_for_status()
            data = response.json()

        return Order(
            id=data["id"],
            symbol=data["symbol"],
            side=data["side"],
            notional=float(data["notional"]) if data.get("notional") else notional,
            order_type=data["type"],
            status=data["status"],
            filled_qty=float(data["filled_qty"]) if data.get("filled_qty") else None,
            filled_avg_price=float(data["filled_avg_price"]) if data.get("filled_avg_price") else None,
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
        )

    async def get_order(self, order_id: str) -> Order:
        """Get order status by ID"""
        url = f"{self.trading_base_url}/v2/orders/{order_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

        return Order(
            id=data["id"],
            symbol=data["symbol"],
            side=data["side"],
            notional=float(data.get("notional", 0)),
            order_type=data["type"],
            status=data["status"],
            filled_qty=float(data["filled_qty"]) if data.get("filled_qty") else None,
            filled_avg_price=float(data["filled_avg_price"]) if data.get("filled_avg_price") else None,
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
        )

    async def create_trade_proposal(
        self,
        symbol: str,
        side: str,
        usd_amount: float,
        order_type: str = "market",
        limit_price: Optional[float] = None,
        rationale: str = "",
        available_funds: float = 0.0
    ) -> TradeProposal:
        """
        Create a trade proposal for user confirmation.

        Fetches current price and estimates shares.

        Args:
            symbol: Stock symbol
            side: "buy" or "sell"
            usd_amount: USD amount to trade
            order_type: "market" or "limit"
            limit_price: Limit price (if applicable)
            rationale: Why this trade makes sense
            available_funds: Available cash from budget

        Returns:
            TradeProposal for user review
        """
        # Get current quote
        quote = await self.get_latest_quote(symbol)

        # Estimate shares based on current price
        if order_type == "market":
            estimated_price = quote.ask_price if side == "buy" else quote.bid_price
        else:
            estimated_price = limit_price or quote.mid_price

        estimated_shares = usd_amount / estimated_price

        return TradeProposal(
            symbol=symbol.upper(),
            side=side.lower(),
            usd_amount=usd_amount,
            order_type=order_type.lower(),
            limit_price=limit_price,
            current_price=quote.last_price,
            estimated_shares=estimated_shares,
            rationale=rationale,
            available_funds=available_funds
        )


# Future Enhancement: WebSocket Streaming
"""
To switch to WebSocket streaming for real-time quotes:

```python
import websockets
import json

async def stream_quotes(symbols: list[str]):
    url = "wss://stream.data.alpaca.markets/v2/stocks"

    async with websockets.connect(url) as ws:
        # Authenticate
        await ws.send(json.dumps({
            "action": "auth",
            "key": ALPACA_API_KEY,
            "secret": ALPACA_API_SECRET
        }))

        # Subscribe to quotes
        await ws.send(json.dumps({
            "action": "subscribe",
            "quotes": symbols
        }))

        # Listen for updates
        async for message in ws:
            data = json.loads(message)
            if data[0]["T"] == "q":  # Quote
                yield Quote(
                    symbol=data[0]["S"],
                    bid_price=data[0]["bp"],
                    ask_price=data[0]["ap"],
                    # ... etc
                )
```

This provides real-time streaming quotes with lower latency than REST API polling.
"""
