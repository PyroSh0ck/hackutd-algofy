"""
Response Agent

Formats and delivers responses to users in the most appropriate way.

Features:
- Response formatting (markdown, HTML, plain text)
- Multi-modal responses (text + visualizations)
- Context-aware formatting
- Tone adjustment (formal, casual, educational)
"""

from .agent import create_response_agent, ResponseAgentState, format_response

__all__ = ["create_response_agent", "ResponseAgentState", "format_response"]
