"""
The main agent that orchestrates the report generation process.
"""

import asyncio
import json
import logging
import os
import re
from typing import Annotated, Any, Sequence, cast

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from . import author, researcher
from .prompts import report_planner_instructions
from .json_utils import parse_json_response

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3
_QUERIES_PER_SECTION = 5
_THROTTLE_LLM_CALLS = os.getenv("THROTTLE_LLM_CALLS", "0")

llm = ChatNVIDIA(
    base_url="https://openrouter.ai/api/v1",
    model="nvidia/nemotron-nano-9b-v2",
    temperature=0.0,
    api_key=os.getenv("OPENROUTER_API_KEY")
)


class Report(BaseModel):
    title: str
    sections: list[author.Section]


class AgentState(BaseModel):
    topic: str
    report_structure: str
    investment_amount: float = 700.0  # Default investment amount
    report_plan: Report | None = None
    report: str | None = None
    investment_decision: str | None = None  # "BUY" or "WAIT"
    decision_reasoning: str | None = None
    messages: Annotated[Sequence[Any], add_messages] = []


async def topic_research(state: AgentState, config: RunnableConfig):
    """Research recent stock market news and movements."""
    _LOGGER.info("Performing stock market research for S&P 500 and SPY.")

    # Focus research on recent market news
    research_topic = f"{state.topic} - Focus on recent news from last 3 days explaining market movements"

    researcher_state = researcher.ResearcherState(
        topic=research_topic,
        number_of_queries=_QUERIES_PER_SECTION,
        messages=state.messages,
    )

    research = await researcher.graph.ainvoke(researcher_state, config)

    return {"messages": research.get("messages", [])}


async def report_planner(state: AgentState, config: RunnableConfig):
    """Plan the stock market analysis report structure."""
    _LOGGER.info("Calling stock analysis report planner.")

    user_prompt = report_planner_instructions.format(
        topic=state.topic,
        report_structure=state.report_structure,
    )

    for count in range(_MAX_LLM_RETRIES):
        # Use only system and user messages for report planning to avoid confusion from conversation history
        messages = [
            {"role": "system", "content": "/no_think You are a financial analyst planning a stock market analysis report. Respond only with valid JSON in the requested format."},
            {"role": "user", "content": user_prompt}
        ]
        response = await llm.ainvoke(messages, config)

        if response and response.content:
            try:
                # Parse JSON response into Report model
                parsed_report = parse_json_response(response.content, Report)
                state.report_plan = parsed_report
                return state
            except ValueError as e:
                _LOGGER.warning("Failed to parse JSON response on attempt %d: %s", count + 1, e)
                if count == _MAX_LLM_RETRIES - 1:
                    _LOGGER.error("Raw response was: %s", response.content)
        else:
            _LOGGER.warning("Empty response on attempt %d", count + 1)

        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )

    raise RuntimeError("Failed to call model after %d attempts.", _MAX_LLM_RETRIES)


async def section_author_orchestrator(state: AgentState, config: RunnableConfig):
    """Orchestrate the section authoring process."""
    if not state.report_plan:
        raise ValueError("Report plan is not set.")

    _LOGGER.info("Orchestrating the section authoring process.")

    writers = []
    for idx, section in enumerate(state.report_plan.sections):
        _LOGGER.info("Creating author agent for section: %s", section.name)

        section_writer_state = author.SectionWriterState(
            index=idx,
            section=section,
            topic=state.topic,
            messages=[],  # Start with empty messages for each section to avoid interference
        )
        writers.append(author.graph.ainvoke(section_writer_state, config))

    all_sections = []
    if _THROTTLE_LLM_CALLS == "1":
        # Throttle LLM calls by writing one section at a time
        _LOGGER.info("Throttling LLM calls.")
        for writer in writers:
            all_sections.append(await writer)
            await asyncio.sleep(30)
    else:
        # Without throttling, write all sections at once
        all_sections = await asyncio.gather(*writers)
    all_sections = cast(list[dict[str, Any]], all_sections)

    for section in all_sections:
        index = section["index"]
        content = section["section"].content
        section_name = state.report_plan.sections[index].name
        
        # Debug: Log section content details
        _LOGGER.info("Finished section: %s", section_name)
        _LOGGER.info("Section content length: %d characters", len(content))
        if "Note: The actual section content will be drafted" in content:
            _LOGGER.warning("Section '%s' contains placeholder content!", section_name)
        _LOGGER.info("Section content preview: %s", content[:200] + "..." if len(content) > 200 else content)
        
        state.report_plan.sections[index].content = content

    return state


async def report_author(state: AgentState, config: RunnableConfig):
    """Write the stock analysis report."""
    if not state.report_plan:
        raise ValueError("Report plan is not set.")

    _LOGGER.info("Authoring the stock analysis report.")

    from datetime import datetime
    current_date = datetime.now().strftime("%B %d, %Y")

    output = f"# {state.report_plan.title}\n\n"
    output += f"**Analysis Date:** {current_date}\n\n"
    output += f"**Investment Amount:** ${state.investment_amount}\n\n"

    for section in state.report_plan.sections:
        output += f"## {section.name}\n\n"
        output += section.content
        output += "\n\n"

    state.report = output
    return state


async def investment_decision_maker(state: AgentState, config: RunnableConfig):
    """Make a final investment recommendation based on the report."""
    if not state.report:
        raise ValueError("Report is not generated yet.")

    _LOGGER.info("Making investment decision.")

    from datetime import datetime
    current_date = datetime.now().strftime("%B %d, %Y")

    decision_prompt = f"""
You are a financial advisor making an investment decision on {current_date}.

Based on the stock market analysis report below, provide ONE CLEAR recommendation.

REPORT:
{state.report}

INVESTMENT PARAMETERS:
- Amount: ${state.investment_amount}
- Target: S&P 500 / SPY ETF
- Date: {current_date}

CRITICAL RULES:
1. Make ONE decision only: "BUY NOW" or "WAIT"
2. Base decision on the MOST RECENT data from the report
3. Ignore any old/outdated data
4. Write in plain text - NO special characters, NO backslashes

Format your response as:

DECISION: [BUY NOW or WAIT]

REASONING:
[2-3 sentences based on the recent market analysis in the report]

TIMELINE:
[If WAIT: when to reconsider. If BUY: monitoring plan]

RISKS:
[1-2 key risks to be aware of]
"""

    for count in range(_MAX_LLM_RETRIES):
        messages = [
            {"role": "system", "content": "/no_think You are an expert investment advisor making actionable recommendations based on market analysis."},
            {"role": "user", "content": decision_prompt}
        ]
        response = await llm.ainvoke(messages, config)

        if response and response.content:
            # Extract the decision (BUY NOW or WAIT)
            decision_text = str(response.content)
            if "BUY NOW" in decision_text.upper():
                state.investment_decision = "BUY NOW"
            elif "WAIT" in decision_text.upper():
                state.investment_decision = "WAIT"
            else:
                state.investment_decision = "UNCLEAR"

            state.decision_reasoning = decision_text

            # Append decision to the report
            state.report += f"\n\n---\n\n## Final Investment Recommendation\n\n{decision_text}\n"

            return state

        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )

    raise RuntimeError("Failed to call model after %d attempts.", _MAX_LLM_RETRIES)


workflow = StateGraph(AgentState)

workflow.add_node("topic_research", topic_research)
workflow.add_node("report_planner", report_planner)
workflow.add_node("section_author_orchestrator", section_author_orchestrator)
workflow.add_node("report_author", report_author)
workflow.add_node("investment_decision_maker", investment_decision_maker)

workflow.add_edge(START, "topic_research")
workflow.add_edge("topic_research", "report_planner")
workflow.add_edge("report_planner", "section_author_orchestrator")
workflow.add_edge("section_author_orchestrator", "report_author")
workflow.add_edge("report_author", "investment_decision_maker")
workflow.add_edge("investment_decision_maker", END)

graph = workflow.compile()
