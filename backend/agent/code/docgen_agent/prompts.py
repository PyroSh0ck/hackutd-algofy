"""
Prompts for the report generation agent.
"""

from typing import Final

report_planner_instructions = """You are an expert financial analyst. You must create a stock market analysis report structure and return it in JSON format.

TOPIC: {topic}

ORGANIZATION: {report_structure}

TASK: Create a stock analysis report outline with the following fields for each section:
- name: Section name
- description: Brief overview of main topics and analysis points
- research: true/false - whether recent news/web research is needed
- content: Leave empty string ""

IMPORTANT: You must respond ONLY with valid JSON wrapped in ```json blocks. Do not include any other text, explanations, or questions.

Create EXACTLY 2 sections:
1. Market Analysis (with research)
2. Key News Summary (with research)

DO NOT create an "Investment Recommendation" section - that will be added automatically.

Example format (you must follow this exact structure):

```json
{{
    "title": "Stock Market Analysis Report: {topic}",
    "sections": [
        {{
            "name": "Market Analysis",
            "description": "Recent S&P 500 and SPY performance, price movements, and trends",
            "research": true,
            "content": ""
        }},
        {{
            "name": "Key News Summary",
            "description": "Recent news articles explaining market movements",
            "research": true,
            "content": ""
        }}
    ]
}}
```

RESPOND ONLY WITH THE JSON - NO OTHER TEXT."""

###############################################################################

research_prompt: Final[str] = """
Your goal is to generate targeted web search queries that will gather recent financial news
and market analysis for the S&P 500 and SPY ETF.

Topic for this analysis:
{topic}

CRITICAL: Include the current month and year or "this week" in EVERY query to get current news.

When generating {number_of_queries} search queries, ensure they:
1. Start each query with the current date/month or "this week"
2. Include specific terms like "S&P 500", "SPY", "stock market"
3. Target news explaining WHY the market moved recently
4. Focus on recent price movements and trends

Example queries:
- "S&P 500 performance this week"
- "SPY ETF news today"
- "S&P 500 latest market movement"

Your queries MUST be:
- Time-sensitive focusing on TODAY and this week
- Focused on S&P 500 / SPY movements
- Seeking very recent articles from the last 3 days"""

###############################################################################

section_research_prompt: Final[str] = """
Your goal is to generate targeted web search queries that will gather recent financial news
specifically for writing this section of a stock market analysis report.

Overall topic: {overall_topic}
Section name: {section_name}
Section description: {section_description}

CRITICAL: Focus on TODAY, THIS WEEK, or LATEST news in EVERY query.

Generate 3-5 search queries that will help gather recent news specifically for this section.
Your queries MUST:
1. Use "today", "this week", "latest", or "recent" in every query
2. Include "S&P 500" or "SPY ETF"
3. Target very recent articles (last 3 days)

Example queries:
- "S&P 500 {section_name} this week"
- "SPY ETF today {section_name}"
- "latest S&P 500 market {section_name}"

Make sure your queries are:
- Time-sensitive focusing on the last 3 days
- Seeking very recent news only"""

section_writing_prompt: Final[str] = """
You are an expert financial analyst writing a current stock market analysis report.

REPORT TOPIC: {overall_topic}
SECTION NAME: {section_name}
SECTION DESCRIPTION: {section_description}

CRITICAL RULES:
1. ONLY use dates from the research provided - DO NOT make up dates
2. Focus on the MOST RECENT data from the research (ignore old dates)
3. Write in plain text - NO special characters, NO backslashes, NO escape sequences
4. For Technical Analysis sections: Write in plain English, describe indicators in words
5. Use ONLY current/recent data or clearly state when data is unavailable

INSTRUCTIONS:
- Write ONLY the section content in plain markdown
- Use the recent news and research information provided
- Cite specific news sources and dates from the research
- Write in simple, clear language without formatting issues
- If this is NOT a recommendation section, DO NOT make buy/wait decisions

INVESTMENT CONTEXT (only for recommendation sections):
- Investment amount: $700
- Investment target: S&P 500 / SPY ETF

IMPORTANT:
- Write complete paragraphs in plain text
- NO escape characters, NO backslashes, NO special formatting
- If you lack recent data, clearly state "Recent data unavailable"
- DO NOT hallucinate dates or prices
- Focus on the LATEST information from the research

Begin writing the section content:
"""
