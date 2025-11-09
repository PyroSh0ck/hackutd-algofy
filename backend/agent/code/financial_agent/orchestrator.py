"""
Main Financial Assistant Orchestrator

Coordinates between specialized agents:
- Money Manager (Banking Agent) - Account balances, transactions, transfers
- Stock Analysis Agent - Market analysis and investment recommendations
- Budget Helper (Coming soon) - Spending tracking and budgeting

Uses simple language for financial beginners.
"""

import logging
import os
from typing import Sequence, Any, Literal
from typing_extensions import Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from financial_agent.shared_state import FinancialState
from financial_agent.banking_agent.agent import create_banking_agent, BankingAgentState
from financial_agent.budget_agent.agent import create_budget_agent, BudgetAgentState
from financial_agent.trading_agent.agent import create_trading_agent, TradingAgentState
from docgen_agent.agent import graph as stock_analysis_graph, AgentState as StockAgentState
from stripe_integration.client import StripeFinancialClient

_LOGGER = logging.getLogger(__name__)


class OrchestratorState(FinancialState):
    """
    Extended state for the orchestrator that coordinates all agents.
    """
    messages: Sequence[BaseMessage] = []
    current_agent: str = "orchestrator"  # Which agent is currently handling the request
    user_query: str = ""  # The original user question


ORCHESTRATOR_SYSTEM_PROMPT = """
You are a friendly Financial Assistant helping someone learn about money!

You coordinate between different specialized helpers:

1. **Money Manager** - Handles bank accounts:
   - Checking balances ("How much money do I have?")
   - Viewing transactions ("What did I spend on groceries?")
   - Moving money ("Move $100 to savings")

2. **Trading Assistant** - Handles buying/selling stocks:
   - Getting real-time stock prices ("What's the current price of SPY?")
   - Buying stocks or ETFs ("Buy $500 of VOO", "Invest in the S&P 500")
   - Checking available funds ("How much can I invest?")
   - Requires explicit confirmation before executing trades

3. **Stock Analysis Helper** - Handles investment research:
   - Market analysis ("Should I invest in the S&P 500?")
   - Investment recommendations ("Is now a good time to buy stocks?")
   - Understanding market news ("Why are stocks going up?")

4. **Budget Helper** - Handles spending plans:
   - Creating budgets ("Help me create a budget")
   - Tracking spending ("How am I doing with my budget?")
   - Setting savings goals ("I want to save $1000 for a trip")
   - Adjusting when over budget ("I overspent on eating out")

Your job:
1. Understand what the user is asking about
2. Route them to the right specialist
3. Use simple, encouraging language
4. Never use confusing financial jargon

Examples:
- "How much money do I have?" → Money Manager
- "Buy $500 of SPY" → Trading Assistant
- "Should I invest $700?" → Stock Analysis Helper (then Trading Assistant to execute)
- "What did I buy this week?" → Money Manager
- "Is the stock market going up?" → Stock Analysis Helper
"""


ROUTING_PROMPT = """
Based on this user question, which specialist should handle it?

User question: {user_query}

Options:
- banking: Questions about bank accounts, balances, transactions, transferring money
- stocks: Questions about investments, stock market, S&P 500, buying stocks
- budget: Questions about budgets, spending plans, saving goals (not ready yet)
- general: Greetings, general questions, unclear requests

Respond with ONLY one word: banking, stocks, budget, or general
"""


async def route_to_agent(state: OrchestratorState, config: RunnableConfig) -> dict:
    """
    Decide which specialist agent should handle this request.
    """
    _LOGGER.info(f"Routing user query: {state.user_query}")

    # Get the LLM for routing
    model_name = config.get("configurable", {}).get("model", "nvidia/nemotron-nano-9b-v2")
    api_key = config.get("configurable", {}).get("openrouter_api_key")

    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.0,  # Be deterministic for routing
    )

    # Ask the LLM to route
    routing_messages = [
        SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT),
        HumanMessage(content=ROUTING_PROMPT.format(user_query=state.user_query))
    ]

    response = await llm.ainvoke(routing_messages)

    # Extract just the decision (last line or after "A:")
    content = response.content.strip()
    if "\nA:" in content:
        decision = content.split("\nA:")[-1].strip().lower()
    elif "\n" in content:
        decision = content.split("\n")[-1].strip().lower()
    else:
        decision = content.lower()

    _LOGGER.info(f"Routing decision: {decision}")

    # Map to actual agent names
    if "banking" in decision or "money" in decision:
        return {"current_agent": "banking"}
    elif "stock" in decision or "invest" in decision:
        return {"current_agent": "stocks"}
    elif "budget" in decision:
        return {"current_agent": "budget"}
    else:
        return {"current_agent": "general"}


async def banking_agent_node(state: OrchestratorState, config: RunnableConfig) -> dict:
    """
    Handle banking/money management requests.
    """
    _LOGGER.info("Delegating to Money Manager agent")

    # Create banking agent
    banking_agent = create_banking_agent()

    # Convert orchestrator state to banking state
    banking_state = BankingAgentState(**state.model_dump())
    banking_state.messages = list(state.messages) + [HumanMessage(content=state.user_query)]

    # Run the banking agent
    result = await banking_agent.ainvoke(banking_state, config)

    # Extract the response
    last_message = result["messages"][-1]

    return {
        "messages": [last_message],
        "accounts": result.get("accounts", state.accounts),
        "recent_transactions": result.get("recent_transactions", state.recent_transactions)
    }


async def stock_analysis_node(state: OrchestratorState, config: RunnableConfig) -> dict:
    """
    Handle stock market analysis and investment recommendations.
    """
    _LOGGER.info("Delegating to Stock Analysis agent")

    # Extract investment amount if mentioned
    investment_amount = 700.0  # Default

    # Simple parsing for investment amount
    query_lower = state.user_query.lower()
    import re
    amount_match = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', query_lower)
    if amount_match:
        investment_amount = float(amount_match.group(1).replace(',', ''))

    # Create stock analysis state
    stock_state = StockAgentState(
        topic="S&P 500 and SPY ETF - Recent Market Analysis",
        report_structure="Market Overview, Recent News Analysis, Investment Recommendation",
        investment_amount=investment_amount,
        messages=[]
    )

    # Run the stock analysis agent
    result = await stock_analysis_graph.ainvoke(stock_state, config)

    # Format the response in a beginner-friendly way
    report = result.get("report", "")
    decision = result.get("investment_decision", "")

    friendly_response = f"""
Let me help you understand the current stock market situation!

{report}

**What does this mean for you?**

Decision: **{decision}**

If you have more questions about investing, budgeting, or your bank accounts, just ask! I'm here to help you learn about money in simple terms.
"""

    return {
        "messages": [AIMessage(content=friendly_response)]
    }


async def budget_agent_node(state: OrchestratorState, config: RunnableConfig) -> dict:
    """
    Handle budgeting and savings goal requests.
    """
    _LOGGER.info("Delegating to Budget Helper agent")

    # Create budget agent
    budget_agent = create_budget_agent()

    # Convert orchestrator state to budget state
    budget_state = BudgetAgentState(**state.model_dump())
    budget_state.messages = list(state.messages) + [HumanMessage(content=state.user_query)]

    # Run the budget agent
    result = await budget_agent.ainvoke(budget_state, config)

    # Extract the response
    last_message = result["messages"][-1]

    return {
        "messages": [last_message],
        "current_budget": result.get("current_budget", state.current_budget),
        "user_goals": result.get("user_goals", state.user_goals)
    }


async def general_response_node(state: OrchestratorState, config: RunnableConfig) -> dict:
    """
    Handle general questions, greetings, and unclear requests.
    """
    _LOGGER.info("Providing general response")

    # Get LLM for general conversation
    model_name = config.get("configurable", {}).get("model", "nvidia/nemotron-nano-9b-v2")
    api_key = config.get("configurable", {}).get("openrouter_api_key")

    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
    )

    general_prompt = f"""
You are a friendly Financial Assistant. The user said: "{state.user_query}"

Respond warmly and explain what you can help with:
- Money Manager: Check balances, view transactions, move money between accounts
- Stock Analysis: Understand the market, get investment recommendations
- Budget Helper: Create budgets, set savings goals, track spending

Keep it simple, friendly, and encouraging. No jargon.
"""

    messages = [
        SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT),
        HumanMessage(content=general_prompt)
    ]

    response = await llm.ainvoke(messages)

    # Extract just the answer part (after "A:")
    content = response.content
    if "\nA:" in content:
        actual_response = content.split("\nA:")[-1].strip()
        response.content = actual_response

    return {"messages": [response]}


def route_after_decision(state: OrchestratorState) -> str:
    """
    Route to the appropriate agent based on the routing decision.
    """
    agent = state.current_agent

    if agent == "banking":
        return "banking"
    elif agent == "stocks":
        return "stocks"
    elif agent == "budget":
        return "budget"
    else:
        return "general"


def create_financial_orchestrator() -> StateGraph:
    """
    Create the main financial assistant orchestrator.

    This coordinates between all specialized agents and routes
    user queries to the right specialist.

    Returns:
        A compiled LangGraph workflow
    """
    # Create the graph
    workflow = StateGraph(OrchestratorState)

    # Add nodes
    workflow.add_node("router", route_to_agent)
    workflow.add_node("banking", banking_agent_node)
    workflow.add_node("stocks", stock_analysis_node)
    workflow.add_node("budget", budget_agent_node)
    workflow.add_node("general", general_response_node)

    # Define flow
    workflow.set_entry_point("router")

    # Route based on decision
    workflow.add_conditional_edges(
        "router",
        route_after_decision,
        {
            "banking": "banking",
            "stocks": "stocks",
            "budget": "budget",
            "general": "general"
        }
    )

    # All agents end after processing
    workflow.add_edge("banking", END)
    workflow.add_edge("stocks", END)
    workflow.add_edge("budget", END)
    workflow.add_edge("general", END)

    return workflow.compile()


async def chat_with_financial_assistant(
    user_query: str,
    state: FinancialState | None = None,
    config: RunnableConfig | None = None
) -> str:
    """
    Convenience function to chat with the Financial Assistant.

    Args:
        user_query: What the user wants to know or do
        state: Current financial state (creates new if None)
        config: Configuration with API keys

    Returns:
        The assistant's response
    """
    # Create default state if needed
    if state is None:
        state = FinancialState(
            user_id="default_user",
            stripe_session_id=os.getenv("STRIPE_SESSION_ID", "")
        )

    # Create default config if needed
    if config is None:
        config = {
            "configurable": {
                "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
                "model": "nvidia/nemotron-nano-9b-v2"
            }
        }

    # Create orchestrator
    orchestrator = create_financial_orchestrator()

    # Create orchestrator state
    orch_state = OrchestratorState(**state.model_dump())
    orch_state.user_query = user_query
    orch_state.messages = list(state.conversation_history) if hasattr(state, 'conversation_history') else []

    # Run the orchestrator
    result = await orchestrator.ainvoke(orch_state, config)

    # Get the last message
    last_message = result["messages"][-1]

    if isinstance(last_message, AIMessage):
        return last_message.content
    else:
        return str(last_message)


# Example usage
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv("../secrets.env")

    async def demo():
        """Demo the Financial Assistant orchestrator"""
        print("=" * 60)
        print("Financial Assistant Demo")
        print("=" * 60)

        # Create initial state
        state = FinancialState(
            user_id="demo_user",
            stripe_session_id=os.getenv("STRIPE_SESSION_ID", "")
        )

        # Test different types of queries
        test_queries = [
            "Hi, what can you help me with?",
            "How much money do I have in my checking account?",
            "Should I invest $700 in the stock market right now?",
            "What did I spend on groceries this month?",
            "Help me create a monthly budget for $3000 income",
            "I want to save $1000 for a trip in May 2026",
        ]

        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"You: {query}")
            print(f"{'='*60}\n")

            response = await chat_with_financial_assistant(query, state)
            print(f"Assistant: {response}\n")

            # Small delay between queries
            await asyncio.sleep(1)

    asyncio.run(demo())
