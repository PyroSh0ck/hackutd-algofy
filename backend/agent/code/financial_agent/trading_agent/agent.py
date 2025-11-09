"""
Trading Agent

LangGraph workflow for stock trading with:
- Real-time quote fetching (Alpaca Market Data v2)
- Budget integration (check available funds)
- Stock analysis integration (investment recommendations)
- Human-in-the-loop confirmation (explicit user approval required)
- Paper trading (Alpaca Paper API)
"""

import logging
from typing import Sequence
from typing_extensions import Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI

from financial_agent.shared_state import FinancialState
from alpaca_trading.client import AlpacaTradingClient
from alpaca_trading.models import TradeProposal
from financial_agent.banking_agent.tools import BankingTools, create_banking_tools
from financial_agent.budget_agent.tools import BudgetTools, create_budget_tools
from stripe_integration.client import StripeFinancialClient
from .tools import create_trading_tools

_LOGGER = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are a Trading Assistant helping someone invest their money wisely!

Your job:
1. Get real-time stock prices
2. Check how much money they have available to invest
3. Propose trades based on their budget and investment recommendations
4. Get explicit confirmation before executing any trade

You have access to:
- **get_stock_quote**: Get current price for any stock (e.g., SPY, VOO, AAPL)
- **check_available_funds**: See how much money is available for investing based on their budget
- **propose_trade**: Create a trade proposal with all details for user review
- **execute_trade**: Execute a trade ONLY after user confirms with "CONFIRM TRADE"

Important Rules:
- NEVER execute a trade without explicit user confirmation
- ALWAYS check available funds before proposing a trade
- Use stock analysis recommendations to explain WHY a trade makes sense
- Be conservative - don't propose trades that exceed available funds
- For fractional/ETF investing, use market orders unless user requests limit orders

Use simple language - explain everything clearly!
"""


class TradingAgentState(FinancialState):
    """Extended state for trading operations"""
    messages: Sequence[BaseMessage] = []
    pending_trade_proposal: TradeProposal | None = None
    awaiting_confirmation: bool = False


async def trading_assistant(state: TradingAgentState, config: RunnableConfig):
    """
    Main trading assistant node.

    Helps user invest money by:
    1. Checking real-time prices
    2. Verifying available funds
    3. Proposing trades
    4. Requiring explicit confirmation
    """
    # Get the LLM from config
    model_name = config.get("configurable", {}).get("model", "nvidia/nemotron-nano-9b-v2")
    api_key = config.get("configurable", {}).get("openrouter_api_key")

    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
    )

    # Create tools
    alpaca_client = AlpacaTradingClient()
    stripe_client = StripeFinancialClient()
    banking_tools = BankingTools(stripe_client)
    budget_tools = BudgetTools(banking_tools)

    trading_tools_list = create_trading_tools(alpaca_client, banking_tools, budget_tools)

    # Also include banking and budget tools for context
    banking_tools_list = create_banking_tools(stripe_client)
    budget_tools_list = create_budget_tools(banking_tools)

    all_tools = trading_tools_list + banking_tools_list + budget_tools_list
    llm_with_tools = llm.bind_tools(all_tools)

    # Build messages
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add context about pending trades
    if state.pending_trade_proposal:
        context = f"""
⚠️ PENDING TRADE AWAITING CONFIRMATION

{state.pending_trade_proposal.to_summary()}

The user must explicitly say "CONFIRM TRADE" to execute this order.
"""
        messages.append(SystemMessage(content=context))

    # Add conversation history
    messages.extend(state.messages)

    # Get response
    response = await llm_with_tools.ainvoke(messages)

    # Extract just the answer part (after "A:")
    if hasattr(response, 'content') and response.content:
        content = response.content
        if "\nA:" in content:
            actual_response = content.split("\nA:")[-1].strip()
            response.content = actual_response

    return {"messages": [response]}


async def tool_executor(state: TradingAgentState, config: RunnableConfig):
    """Execute trading tools"""
    last_message = state.messages[-1]

    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return {"messages": []}

    # Create tools
    alpaca_client = AlpacaTradingClient()
    stripe_client = StripeFinancialClient()
    banking_tools = BankingTools(stripe_client)
    budget_tools = BudgetTools(banking_tools)

    trading_tools_list = create_trading_tools(alpaca_client, banking_tools, budget_tools)
    banking_tools_list = create_banking_tools(stripe_client)
    budget_tools_list = create_budget_tools(banking_tools)

    all_tools = trading_tools_list + banking_tools_list + budget_tools_list
    tool_node = ToolNode(all_tools)

    result = await tool_node.ainvoke(state, config)
    return result


def should_continue(state: TradingAgentState) -> str:
    """Decide if we should call tools or end"""
    last_message = state.messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


def create_trading_agent() -> StateGraph:
    """
    Create the Trading Agent workflow.

    Flow:
    1. User asks about investing or trading
    2. Agent checks prices and available funds
    3. Agent proposes a trade with full details
    4. User must confirm with "CONFIRM TRADE"
    5. Only then does agent execute the order

    Returns:
        Compiled LangGraph workflow
    """
    workflow = StateGraph(TradingAgentState)

    # Add nodes
    workflow.add_node("assistant", trading_assistant)
    workflow.add_node("tools", tool_executor)

    # Define flow
    workflow.set_entry_point("assistant")

    workflow.add_conditional_edges(
        "assistant",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )

    workflow.add_edge("tools", "assistant")

    return workflow.compile()


async def chat_with_trading_assistant(
    user_message: str,
    state: FinancialState,
    config: RunnableConfig
) -> str:
    """
    Convenience function to chat with Trading Assistant.

    Args:
        user_message: What the user wants to do
        state: Current financial state
        config: Configuration with API keys

    Returns:
        Assistant's response
    """
    agent = create_trading_agent()

    trading_state = TradingAgentState(**state.model_dump())
    trading_state.messages = list(trading_state.messages) + [HumanMessage(content=user_message)]

    result = await agent.ainvoke(trading_state, config)

    last_message = result["messages"][-1]

    if isinstance(last_message, AIMessage):
        return last_message.content
    else:
        return str(last_message)
