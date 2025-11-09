"""
Email Agent

Sends notifications, reports, and alerts via email.

Features:
- Budget summaries
- Trade confirmations
- Weekly spending reports
- Investment performance updates
- Account alerts
"""

from .agent import create_email_agent, EmailAgentState, send_email

__all__ = ["create_email_agent", "EmailAgentState", "send_email"]
