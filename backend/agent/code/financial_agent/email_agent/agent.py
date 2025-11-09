"""
Email Agent

Sends notifications, reports, and alerts via email using SMTP.

Features:
- HTML email templates
- Async email sending
- Multiple email types (confirmations, reports, alerts)
- Retry logic for failed sends
"""

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Sequence, Dict, Any, Optional
from typing_extensions import Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from financial_agent.shared_state import FinancialState
from .templates import EmailTemplates

_LOGGER = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are an Email Notification Assistant!

Your job is to:
1. **Determine what emails to send** based on user actions
2. **Format email content** using appropriate templates
3. **Confirm with user** before sending important notifications
4. **Provide email summaries** when emails are sent

Types of emails you send:
- Trade confirmations (after stock purchases)
- Budget summaries (weekly/monthly)
- Spending reports (weekly)
- Investment alerts (portfolio updates)
- Account notifications (new connections, changes)

Always ask for confirmation before sending emails unless it's an automated report the user has subscribed to.

Be concise and helpful!
"""


class EmailAgentState(FinancialState):
    """Extended state for email operations"""
    messages: Sequence[BaseMessage] = []
    pending_email: Optional[Dict[str, Any]] = None
    email_history: list[Dict[str, Any]] = []
    user_email: str = ""


async def email_assistant(state: EmailAgentState, config: RunnableConfig):
    """
    Main email assistant node.

    Decides when and what emails to send.
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

    # Add email context
    if state.user_email:
        context = f"""
User's email address: {state.user_email}
Emails sent this session: {len(state.email_history)}
Pending email: {state.pending_email is not None}
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


def create_email_agent() -> StateGraph:
    """
    Create the Email Agent workflow.

    Returns:
        Compiled LangGraph workflow
    """
    workflow = StateGraph(EmailAgentState)

    # Add nodes
    workflow.add_node("assistant", email_assistant)

    # Define flow
    workflow.set_entry_point("assistant")
    workflow.add_edge("assistant", END)

    return workflow.compile()


# Email sending functionality
async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    from_email: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: int = 587,
    smtp_username: Optional[str] = None,
    smtp_password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send an HTML email via SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email body
        from_email: Sender email (defaults to SMTP_FROM_EMAIL env var)
        smtp_server: SMTP server (defaults to SMTP_SERVER env var)
        smtp_port: SMTP port (default 587)
        smtp_username: SMTP username (defaults to SMTP_USERNAME env var)
        smtp_password: SMTP password (defaults to SMTP_PASSWORD env var)

    Returns:
        Dict with success status and message
    """
    # Get credentials from environment if not provided
    from_email = from_email or os.getenv("SMTP_FROM_EMAIL", "noreply@financial-assistant.com")
    smtp_server = smtp_server or os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_username = smtp_username or os.getenv("SMTP_USERNAME")
    smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")

    if not smtp_username or not smtp_password:
        _LOGGER.warning("SMTP credentials not configured. Email not sent.")
        return {
            "success": False,
            "message": "Email not configured. Set SMTP_USERNAME and SMTP_PASSWORD environment variables."
        }

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        _LOGGER.info(f"Email sent successfully to {to_email}")
        return {
            "success": True,
            "message": f"Email sent to {to_email}",
            "to": to_email,
            "subject": subject
        }

    except Exception as e:
        _LOGGER.error(f"Failed to send email: {e}")
        return {
            "success": False,
            "message": f"Failed to send email: {str(e)}",
            "error": str(e)
        }


# Convenience functions for common email types
async def send_trade_confirmation(
    to_email: str,
    trade_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Send trade confirmation email"""
    html_content = EmailTemplates.trade_confirmation(trade_data)
    subject = f"Trade Confirmation: {trade_data.get('symbol', 'N/A')} - {trade_data.get('side', 'N/A').upper()}"

    return await send_email(to_email, subject, html_content)


async def send_budget_summary(
    to_email: str,
    budget_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Send monthly budget summary email"""
    html_content = EmailTemplates.budget_summary(budget_data)
    subject = f"Monthly Budget Summary - {budget_data.get('month', 'Current Month')}"

    return await send_email(to_email, subject, html_content)


async def send_weekly_spending_report(
    to_email: str,
    spending_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Send weekly spending report email"""
    html_content = EmailTemplates.weekly_spending_report(spending_data)
    subject = "Your Weekly Spending Report"

    return await send_email(to_email, subject, html_content)


async def send_investment_alert(
    to_email: str,
    alert_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Send investment alert email"""
    html_content = EmailTemplates.investment_alert(alert_data)
    subject = alert_data.get('title', 'Investment Alert')

    return await send_email(to_email, subject, html_content)


async def chat_with_email_assistant(
    user_message: str,
    state: FinancialState,
    config: RunnableConfig,
    user_email: str = ""
) -> str:
    """
    Convenience function to chat with Email Assistant.

    Args:
        user_message: User's message
        state: Current financial state
        config: Configuration with API keys
        user_email: User's email address (optional)

    Returns:
        Assistant's response
    """
    agent = create_email_agent()

    email_state = EmailAgentState(**state.model_dump())
    email_state.user_email = user_email or os.getenv("USER_EMAIL", "")
    email_state.messages = list(email_state.messages) + [HumanMessage(content=user_message)]

    result = await agent.ainvoke(email_state, config)

    last_message = result["messages"][-1]

    if isinstance(last_message, AIMessage):
        return last_message.content
    else:
        return str(last_message)
