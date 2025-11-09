"""
Budget Helper Agent

A LangGraph workflow that helps users create budgets, set goals,
and manage their money with beginner-friendly guidance.
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
from financial_agent.banking_agent.tools import BankingTools, create_banking_tools
from stripe_integration.client import StripeFinancialClient
from financial_agent.budget_agent.tools import create_budget_tools
from .prompts import (
    SYSTEM_PROMPT,
    CREATE_BUDGET_PROMPT,
    ADD_GOAL_PROMPT,
    ADJUST_BUDGET_PROMPT,
    TRACK_PROGRESS_PROMPT,
    WARNING_MESSAGES,
    ENCOURAGEMENT_MESSAGES
)

_LOGGER = logging.getLogger(__name__)


class BudgetAgentState(FinancialState):
    """Extended state for budget operations"""
    messages: Sequence[BaseMessage] = []
    current_operation: str = ""  # What the agent is currently doing


async def budget_assistant(state: BudgetAgentState, config: RunnableConfig):
    """
    Main budget assistant node - helps with budgets and goals.
    Uses Money Manager's banking tools to access account data.
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

    # Create banking tools from Money Manager
    stripe_client = StripeFinancialClient()
    banking_tools = BankingTools(stripe_client)

    # Create budget tools that use Money Manager
    budget_tools = create_budget_tools(banking_tools)

    # Also include Money Manager tools directly so Budget Helper can:
    # - Get balances
    # - Get transactions
    # - View spending patterns
    banking_tools_list = create_banking_tools(stripe_client)

    # Combine all tools
    all_tools = budget_tools + banking_tools_list
    llm_with_tools = llm.bind_tools(all_tools)

    # Build the messages for the LLM
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add context about current state
    if state.current_budget:
        context = f"User's current budget:\n"
        context += f"Monthly Income: ${state.current_budget.monthly_income:,.2f}\n"
        context += f"Total Budgeted: ${state.current_budget.total_budgeted:,.2f}\n"

        if state.current_budget.savings_goals:
            context += f"\nSavings Goals:\n"
            for goal in state.current_budget.savings_goals:
                context += f"- {goal.name}: ${goal.current_saved:,.2f} / ${goal.target_amount:,.2f}\n"

        messages.append(SystemMessage(content=context))
    elif state.user_goals.monthly_income > 0:
        messages.append(SystemMessage(content=f"User's monthly income: ${state.user_goals.monthly_income:,.2f}"))

    # Add conversation history
    messages.extend(state.messages)

    # Get response from LLM
    response = await llm_with_tools.ainvoke(messages)

    return {
        "messages": [response]
    }


async def tool_executor(state: BudgetAgentState, config: RunnableConfig):
    """
    Execute budget tools that the assistant requested.
    Uses Money Manager's banking tools for data access.
    """
    # Get the last message (should contain tool calls)
    last_message = state.messages[-1]

    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return {"messages": []}

    # Create banking tools from Money Manager
    stripe_client = StripeFinancialClient()
    banking_tools = BankingTools(stripe_client)

    # Create budget tools that use Money Manager
    budget_tools = create_budget_tools(banking_tools)

    # Include Money Manager tools
    banking_tools_list = create_banking_tools(stripe_client)

    # Combine all tools
    all_tools = budget_tools + banking_tools_list
    tool_node = ToolNode(all_tools)

    # Run the tools
    result = await tool_node.ainvoke(state, config)

    return result


def should_continue(state: BudgetAgentState) -> str:
    """
    Decide if we should call tools or end.
    """
    last_message = state.messages[-1]

    # If the last message has tool calls, execute them
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Otherwise, we're done
    return END


async def format_response(state: BudgetAgentState, config: RunnableConfig):
    """
    Format the final response in a beginner-friendly way.
    """
    last_message = state.messages[-1]

    # If it's already a nice response, just return it
    if isinstance(last_message, AIMessage):
        return state

    # Otherwise, format it nicely
    return state


def create_budget_agent() -> StateGraph:
    """
    Create the Budget Helper agent workflow.

    Returns:
        A compiled LangGraph workflow ready to use
    """
    # Create the graph
    workflow = StateGraph(BudgetAgentState)

    # Add nodes
    workflow.add_node("assistant", budget_assistant)
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


async def chat_with_budget_helper(
    user_message: str,
    state: FinancialState,
    config: RunnableConfig
) -> str:
    """
    Convenience function to chat with the Budget Helper.

    Args:
        user_message: What the user wants to do
        state: Current financial state
        config: Configuration with API keys

    Returns:
        The assistant's response
    """
    # Create the agent
    agent = create_budget_agent()

    # Add the user's message to state
    budget_state = BudgetAgentState(**state.model_dump())
    budget_state.messages = list(budget_state.messages) + [HumanMessage(content=user_message)]

    # Run the agent
    result = await agent.ainvoke(budget_state, config)

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
        """Demo the Budget Helper agent"""
        # Create initial state
        state = FinancialState(
            user_id="demo_user",
            stripe_session_id=os.getenv("STRIPE_SESSION_ID", "")
        )

        # Set monthly income
        state.user_goals.monthly_income = 3000.0

        # Config with API keys
        config = {
            "configurable": {
                "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
                "model": "nvidia/nemotron-nano-9b-v2"
            }
        }

        print("Budget Helper Demo")
        print("=" * 50)

        # Test conversation
        questions = [
            "Can you help me create a monthly budget? I make $3,000 per month.",
            "I want to save $1,000 for a trip in May 2026",
            "Show me my budget",
        ]

        for question in questions:
            print(f"\nYou: {question}")
            response = await chat_with_budget_helper(question, state, config)
            print(f"\nBudget Helper: {response}")
            print("-" * 50)

    asyncio.run(demo())
