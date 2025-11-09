"""
User Prompt Agent

Provides guided, interactive prompts to help users through workflows.

Use cases:
- Onboarding new users
- Collecting information for budget setup
- Guiding investment decisions
- Confirming multi-step actions
- Providing contextual help
"""

import logging
from typing import Sequence, List, Dict, Any
from typing_extensions import Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from financial_agent.shared_state import FinancialState

_LOGGER = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are a User Prompt Assistant - a friendly guide helping users through financial tasks!

Your job is to:
1. **Guide users step-by-step** through complex workflows
2. **Ask clarifying questions** when information is missing
3. **Provide options** when users need to make decisions
4. **Explain next steps** clearly and simply
5. **Confirm understanding** before proceeding

Guidelines:
- Use numbered lists for multiple steps
- Provide examples when helpful
- Use emojis sparingly (only for emphasis)
- Always give users an "escape route" (how to cancel or go back)
- Never overwhelm - max 3 options at a time

Example workflows you help with:
- Budget setup: "Let's set up your first budget! I'll need a few things..."
- Investment guidance: "Before you invest, let me ask you a few questions..."
- Account linking: "To connect your bank, here's what we need to do..."
- Trade confirmation: "Let me make sure I understand what you want to do..."

Always be encouraging and patient!
"""


class PromptAgentState(FinancialState):
    """Extended state for prompt workflows"""
    messages: Sequence[BaseMessage] = []
    workflow_type: str = ""  # "budget_setup", "investment_guide", etc.
    collected_data: Dict[str, Any] = {}
    current_step: int = 0
    total_steps: int = 0


async def prompt_assistant(state: PromptAgentState, config: RunnableConfig):
    """
    Main prompt assistant node.

    Guides users through workflows with interactive prompts.
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

    # Add workflow context if we're in a multi-step process
    if state.workflow_type and state.total_steps > 0:
        context = f"""
Current Workflow: {state.workflow_type}
Progress: Step {state.current_step} of {state.total_steps}

Data collected so far:
{state.collected_data}

Continue guiding the user through the remaining steps.
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

    return {"messages": [response]}


def create_prompt_agent() -> StateGraph:
    """
    Create the User Prompt Agent workflow.

    Returns:
        Compiled LangGraph workflow
    """
    workflow = StateGraph(PromptAgentState)

    # Add nodes
    workflow.add_node("assistant", prompt_assistant)

    # Define flow
    workflow.set_entry_point("assistant")
    workflow.add_edge("assistant", END)

    return workflow.compile()


# Pre-defined prompt templates
class PromptTemplates:
    """Common prompt templates for different workflows"""

    @staticmethod
    def budget_setup_start() -> str:
        """Start budget setup workflow"""
        return """
👋 Let's set up your first budget!

To create a personalized budget, I need to know a few things:

1. **Monthly Income** - How much money do you make each month (after taxes)?
2. **Major Expenses** - Do you know your rent/mortgage amount?
3. **Savings Goals** - Are you saving for anything specific?

We'll use the **50/30/20 rule**:
- 50% for NEEDS (rent, groceries, bills)
- 30% for WANTS (fun stuff, eating out)
- 20% for SAVINGS (emergency fund, goals)

Let's start with #1 - what's your monthly take-home income?

(Type a number like "3000" or say "I don't know yet")
"""

    @staticmethod
    def investment_guide_start() -> str:
        """Start investment guidance workflow"""
        return """
📈 Great! Let's figure out if investing is right for you.

Before we proceed, I need to understand your situation:

**Quick Questions:**
1. Do you have an emergency fund (3-6 months of expenses)?
   - ✅ Yes, I'm covered
   - ⚠️  Working on it
   - ❌ Not yet

2. How much are you thinking of investing?

3. What's your goal?
   - 🏖️  Long-term growth (retirement, 5+ years)
   - 🎯 Medium-term (buying a house, 2-5 years)
   - 💰 Short-term (less than 2 years)

Let me know your answers and we'll create a plan!
"""

    @staticmethod
    def trade_confirmation(symbol: str, amount: float, action: str = "buy") -> str:
        """Confirm trade before execution"""
        return f"""
🔍 Let me make sure I understand what you want to do:

**Your Request:**
- Action: {action.upper()}
- Symbol: {symbol}
- Amount: ${amount:,.2f}

**Before I proceed, please confirm:**

1. Is this the correct symbol? ({symbol})
2. Is the amount right? (${amount:,.2f})
3. Are you ready to place this order?

Reply with:
- ✅ **"YES"** to proceed
- ❌ **"NO"** or **"CANCEL"** to stop
- 🔄 **"CHANGE"** to modify something

What would you like to do?
"""

    @staticmethod
    def bank_connection_guide() -> str:
        """Guide user through bank connection"""
        return """
🏦 Let's connect your bank account!

**What you'll need:**
- Your bank's online banking credentials
- 2-5 minutes of time
- Your phone (for 2-factor authentication)

**Here's the process:**
1. I'll open a secure connection to Stripe
2. You'll select your bank from a list
3. You'll log in with your normal banking credentials
4. You'll authorize read-only access (we can't move money!)
5. Done! Your accounts will sync automatically

**Security:**
- ✅ Bank-level encryption
- ✅ Read-only access
- ✅ No passwords stored
- ✅ You can disconnect anytime

Ready to start? Type **"START"** to begin!

(Or type "MORE INFO" if you have questions)
"""

    @staticmethod
    def workflow_complete(workflow_name: str, summary: Dict[str, Any]) -> str:
        """Completion message for workflows"""
        return f"""
🎉 **{workflow_name} Complete!**

Here's what we set up:

{chr(10).join(f"✅ {key}: {value}" for key, value in summary.items())}

**Next Steps:**
You can now use your new setup! Try asking me:
- "Show me my budget"
- "How much can I invest?"
- "What did I spend this week?"

Need help with anything else?
"""


async def chat_with_prompt_assistant(
    user_message: str,
    state: FinancialState,
    config: RunnableConfig,
    workflow_type: str = ""
) -> str:
    """
    Convenience function to chat with Prompt Assistant.

    Args:
        user_message: User's message
        state: Current financial state
        config: Configuration with API keys
        workflow_type: Optional workflow identifier

    Returns:
        Assistant's response
    """
    agent = create_prompt_agent()

    prompt_state = PromptAgentState(**state.model_dump())
    prompt_state.workflow_type = workflow_type
    prompt_state.messages = list(prompt_state.messages) + [HumanMessage(content=user_message)]

    result = await agent.ainvoke(prompt_state, config)

    last_message = result["messages"][-1]

    if isinstance(last_message, AIMessage):
        return last_message.content
    else:
        return str(last_message)
