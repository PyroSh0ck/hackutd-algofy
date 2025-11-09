"""
Money Manager Agent

A LangGraph workflow that helps users manage their bank accounts
with beginner-friendly language and explanations.
"""

import logging
from typing import Sequence, Any
from typing_extensions import Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI

from financial_agent.shared_state import FinancialState
from stripe_integration.client import StripeFinancialClient
from financial_agent.banking_agent.tools import create_banking_tools
from .prompts import (
    SYSTEM_PROMPT,
    BALANCE_CHECK_PROMPT,
    TRANSACTION_REVIEW_PROMPT,
    TRANSFER_PROMPT,
    ACCOUNT_SUMMARY_PROMPT,
    ERROR_MESSAGES
)

_LOGGER = logging.getLogger(__name__)


class BankingAgentState(FinancialState):
    """Extended state for banking operations"""
    messages: Sequence[BaseMessage] = []
    current_operation: str = ""  # What the agent is currently doing


async def banking_assistant(state: BankingAgentState, config: RunnableConfig):
    """
    Main banking assistant node - decides what to do and calls appropriate tools.
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

    # Bind the tools
    stripe_client = StripeFinancialClient()
    tools = create_banking_tools(stripe_client)
    llm_with_tools = llm.bind_tools(tools)

    # Build the messages for the LLM
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add any context about current state
    if state.accounts:
        context = "Connected accounts:\n"
        for acc in state.accounts:
            context += f"- {acc.name}: ${acc.balance:.2f}\n"
        messages.append(SystemMessage(content=context))

    # Add conversation history
    messages.extend(state.messages)

    # Get response from LLM
    response = await llm_with_tools.ainvoke(messages)

    return {
        "messages": [response]
    }


async def tool_executor(state: BankingAgentState, config: RunnableConfig):
    """
    Execute banking tools that the assistant requested.
    """
    # Get the last message (should contain tool calls)
    last_message = state.messages[-1]

    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return {"messages": []}

    # Execute tools
    stripe_client = StripeFinancialClient()
    tools = create_banking_tools(stripe_client)
    tool_node = ToolNode(tools)

    # Run the tools
    result = await tool_node.ainvoke(state, config)

    return result


def should_continue(state: BankingAgentState) -> str:
    """
    Decide if we should call tools or end.
    """
    last_message = state.messages[-1]

    # If the last message has tool calls, execute them
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Otherwise, we're done
    return END


async def format_response(state: BankingAgentState, config: RunnableConfig):
    """
    Format the final response in a beginner-friendly way.
    """
    last_message = state.messages[-1]

    # If it's already a nice response, just return it
    if isinstance(last_message, AIMessage):
        return state

    # Otherwise, format it nicely
    # (This is where we could add additional formatting if needed)
    return state


def create_banking_agent() -> StateGraph:
    """
    Create the Money Manager agent workflow.

    Returns:
        A compiled LangGraph workflow ready to use
    """
    # Create the graph
    workflow = StateGraph(BankingAgentState)

    # Add nodes
    workflow.add_node("assistant", banking_assistant)
    workflow.add_node("tools", tool_executor)
    workflow.add_node("format", format_response)

    # Define the flow
    workflow.set_entry_point("assistant")

    # After assistant, either call tools or format response
    workflow.add_conditional_edges(
        "assistant",
        should_continue,
        {
            "tools": "tools",
            END: "format"
        }
    )

    # After tools, go back to assistant
    workflow.add_edge("tools", "assistant")

    # After format, we're done
    workflow.add_edge("format", END)

    # Compile and return
    return workflow.compile()


async def chat_with_money_manager(
    user_message: str,
    state: FinancialState,
    config: RunnableConfig
) -> str:
    """
    Convenience function to chat with the Money Manager.

    Args:
        user_message: What the user wants to do
        state: Current financial state
        config: Configuration with API keys

    Returns:
        The assistant's response
    """
    # Create the agent
    agent = create_banking_agent()

    # Add the user's message to state
    banking_state = BankingAgentState(**state.model_dump())
    banking_state.messages = list(banking_state.messages) + [HumanMessage(content=user_message)]

    # Run the agent
    result = await agent.ainvoke(banking_state, config)

    # Get the last message
    last_message = result["messages"][-1]

    if isinstance(last_message, AIMessage):
        return last_message.content
    else:
        return str(last_message)


# Example usage
if __name__ == "__main__":
    import asyncio
    import os
    from dotenv import load_dotenv

    load_dotenv("../../secrets.env")

    async def demo():
        """Demo the Money Manager agent"""
        # Create initial state
        state = FinancialState(
            user_id="demo_user",
            stripe_session_id=os.getenv("STRIPE_SESSION_ID", "")
        )

        # Config with API keys
        config = {
            "configurable": {
                "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
                "model": "nvidia/nemotron-nano-9b-v2"
            }
        }

        print("Money Manager Demo")
        print("=" * 50)

        # Test conversation
        questions = [
            "How much money do I have?",
            "Show me what I spent this week",
            "Move $100 to savings"
        ]

        for question in questions:
            print(f"\nYou: {question}")
            response = await chat_with_money_manager(question, state, config)
            print(f"\nMoney Manager: {response}")
            print("-" * 50)

    asyncio.run(demo())
