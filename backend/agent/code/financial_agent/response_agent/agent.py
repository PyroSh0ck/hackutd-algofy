"""
Response Agent

Formats and delivers responses in the most appropriate format for the user.

Features:
- Context-aware formatting
- Tone adjustment (formal, casual, educational)
- Multi-format support (markdown, plain text, structured data)
- Response enhancement (adding tips, warnings, next steps)
"""

import logging
from typing import Sequence, Dict, Any, Literal
from typing_extensions import Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from financial_agent.shared_state import FinancialState
from .formatters import ResponseFormatters

_LOGGER = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are a Response Formatting Assistant!

Your job is to:
1. **Take raw data or information** and format it beautifully
2. **Add context and explanations** to make responses clear
3. **Adjust tone** based on user preferences (casual, educational, formal)
4. **Provide next steps** when appropriate
5. **Add helpful tips** related to the topic

Guidelines:
- Use emojis sparingly (only for categories/sections)
- Use markdown formatting for readability
- Break down complex information into digestible chunks
- Always end with a helpful question or next step suggestion
- Be encouraging and positive

Examples:
- Raw: "Balance: $2500" → Formatted: "💰 You have $2,500 in your checking account. That's great!"
- Raw: "Trade executed" → Formatted: "✅ Trade executed successfully! You now own 0.68 shares of SPY. Want to see your portfolio?"
- Raw: "Budget over" → Formatted: "⚠️ You're $50 over budget in 'Eating Out'. Try cooking at home this week to get back on track!"

Make everything easy to understand!
"""


class ResponseAgentState(FinancialState):
    """Extended state for response formatting"""
    messages: Sequence[BaseMessage] = []
    raw_data: Dict[str, Any] = {}
    response_type: str = ""  # "balances", "transactions", "budget", "trade", etc.
    tone: Literal["casual", "educational", "formal"] = "casual"
    formatted_response: str = ""


async def response_formatter(state: ResponseAgentState, config: RunnableConfig):
    """
    Main response formatter node.

    Takes raw data and formats it appropriately.
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

    # Build messages
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add formatting context
    if state.response_type:
        context = f"""
Response Type: {state.response_type}
Tone: {state.tone}
User Preferences: Simple language = {state.use_simple_language}

Raw Data:
{state.raw_data}

Format this data in a user-friendly way, using appropriate formatting from ResponseFormatters if applicable.
"""
        messages.append(SystemMessage(content=context))

    # Add conversation history
    messages.extend(state.messages)

    # Get response
    response = await llm.ainvoke(messages)

    # Extract just the answer part (after "A:")
    if hasattr(response, 'content') and response.content:
        content = response.content
        if "\nA:" in content:
            actual_response = content.split("\nA:")[-1].strip()
            response.content = actual_response

    return {
        "messages": [response],
        "formatted_response": response.content if hasattr(response, 'content') else str(response)
    }


def create_response_agent() -> StateGraph:
    """
    Create the Response Agent workflow.

    Returns:
        Compiled LangGraph workflow
    """
    workflow = StateGraph(ResponseAgentState)

    # Add nodes
    workflow.add_node("formatter", response_formatter)

    # Define flow
    workflow.set_entry_point("formatter")
    workflow.add_edge("formatter", END)

    return workflow.compile()


def format_response(
    data: Dict[str, Any],
    response_type: str,
    tone: str = "casual"
) -> str:
    """
    Quick format response without going through LLM.

    Args:
        data: Raw data to format
        response_type: Type of response (balances, budget, etc.)
        tone: Response tone (casual, educational, formal)

    Returns:
        Formatted response string
    """
    # Use direct formatters for common types
    formatters = {
        "balances": ResponseFormatters.format_account_balances,
        "budget": ResponseFormatters.format_budget_summary,
        "transactions": ResponseFormatters.format_transactions,
        "trade_proposal": ResponseFormatters.format_trade_proposal,
        "stock_quote": ResponseFormatters.format_stock_quote,
        "investment": ResponseFormatters.format_investment_recommendation,
        "savings_goals": ResponseFormatters.format_savings_goals,
        "error": lambda d: ResponseFormatters.format_error(
            d.get('type', 'Error'),
            d.get('message', 'An error occurred'),
            d.get('suggestions', [])
        ),
        "success": lambda d: ResponseFormatters.format_success(
            d.get('message', 'Operation successful'),
            d.get('details')
        ),
        "help": lambda d: ResponseFormatters.format_help_menu(),
    }

    formatter = formatters.get(response_type)

    if formatter:
        try:
            formatted = formatter(data)

            # Add tone-specific enhancements
            if tone == "educational":
                formatted += "\n\n💡 **Learn More:** Ask me 'Why?' and I'll explain the details!"
            elif tone == "formal":
                formatted = formatted.replace("!", ".")  # Less enthusiastic
            # casual is default, no changes needed

            return formatted
        except Exception as e:
            _LOGGER.error(f"Error formatting response: {e}")
            return f"Error formatting response: {str(e)}"

    # Fallback for unknown types
    return f"Data received:\n{data}"


async def chat_with_response_formatter(
    user_message: str,
    state: FinancialState,
    config: RunnableConfig,
    raw_data: Dict[str, Any] = None,
    response_type: str = ""
) -> str:
    """
    Convenience function to chat with Response Formatter.

    Args:
        user_message: User's message
        state: Current financial state
        config: Configuration with API keys
        raw_data: Raw data to format (optional)
        response_type: Type of response (optional)

    Returns:
        Formatted response
    """
    agent = create_response_agent()

    response_state = ResponseAgentState(**state.model_dump())
    response_state.raw_data = raw_data or {}
    response_state.response_type = response_type
    response_state.messages = list(response_state.messages) + [HumanMessage(content=user_message)]

    result = await agent.ainvoke(response_state, config)

    # Return the formatted response
    return result.get("formatted_response", "No response generated.")
