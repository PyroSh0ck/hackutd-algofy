# Stock Market Analysis Agent

This agent has been transformed from a general AI report generation system into a specialized stock market analysis tool that provides daily investment recommendations for S&P 500 and SPY ETF.

## What This Agent Does

The agent now:

1. **Searches Recent News** - Looks for articles from the **last 3 days** about S&P 500 and SPY movements
2. **Analyzes Market Trends** - Examines why the market moved (earnings, economic data, Fed policy, etc.)
3. **Generates Reports** - Creates detailed analysis reports with market overview and news impact
4. **Makes Investment Decisions** - Provides clear **BUY NOW** or **WAIT** recommendations with reasoning

## Key Features

- ✅ Focuses on **recent news** (last 3 days by default)
- ✅ Uses **financial news sources** (Bloomberg, Reuters, CNBC, WSJ, MarketWatch)
- ✅ Provides **actionable recommendations** with specific reasoning
- ✅ Analyzes **$700 investment amount** (configurable)
- ✅ Includes **risk factors** and **timeline guidance**
- ✅ Generates **markdown reports** saved to disk

## Changes Made

### 1. Tools (`tools.py`)
- Changed search focus to **finance topic** by default
- Increased search results from 2 to **5 sources**
- Reduced search window to **3 days** for recent news
- Updated descriptions for financial context

### 2. Prompts (`prompts.py`)
- **Report Planner**: Now creates stock market analysis report structures
- **Research Prompt**: Focuses on recent S&P 500/SPY news and market movements
- **Section Research**: Targets financial news sources and time-sensitive queries
- **Section Writing**: Emphasizes investment analysis with clear BUY/WAIT decisions

### 3. Researcher (`researcher.py`)
- Updated system prompts to focus on financial analysis
- Generates search queries for recent stock market news

### 4. Author (`author.py`)
- Modified to write investment analysis sections
- Includes context about $700 investment amount
- Provides clear recommendations in sections

### 5. Main Agent (`agent.py`)
- Added `investment_amount` field (default: $700)
- Added `investment_decision` field ("BUY" or "WAIT")
- Added `decision_reasoning` field for explanation
- **New node**: `investment_decision_maker` - Final recommendation based on report
- Updated workflow to include investment decision step
- Enhanced report formatting with metadata

## How to Use

### Running the Agent

```bash
# Set up environment variables
export TAVILY_API_KEY="your_tavily_api_key"
export OPENROUTER_API_KEY="your_openrouter_api_key"

# Run with default $700 investment
python stock_analysis_client.py

# Run with custom investment amount
python stock_analysis_client.py 1000
```

### Programmatic Usage

```python
from docgen_agent.agent import AgentState, graph

# Create initial state
state = AgentState(
    topic="S&P 500 and SPY ETF",
    report_structure="Your custom structure...",
    investment_amount=700.0
)

# Run the agent
final_state = await graph.ainvoke(state)

# Get the results
report = final_state["report"]
decision = final_state["investment_decision"]  # "BUY NOW" or "WAIT"
reasoning = final_state["decision_reasoning"]

print(f"Decision: {decision}")
print(report)
```

## Configuration Options

You can customize the agent behavior by modifying:

### Investment Amount
```python
state = AgentState(
    topic="S&P 500 and SPY ETF",
    investment_amount=1500.0  # Change amount
)
```

### Search Window
In `tools.py`:
```python
SEARCH_DAYS = 3  # Change to 7 for weekly news
```

### Number of Search Results
In `tools.py`:
```python
MAX_RESULTS = 5  # Increase for more sources
```

### Number of Search Queries
In `agent.py`:
```python
_QUERIES_PER_SECTION = 5  # Increase for more comprehensive search
```

## Output Format

The agent generates reports in the following format:

```markdown
# Stock Market Analysis Report: S&P 500 and SPY ETF

**Analysis Date:** [timestamp]
**Investment Amount:** $700

## Market Overview
[Recent performance and trends]

## Recent News Analysis
[Impact of recent news on market]

## Investment Recommendation
[Detailed analysis from sections]

---

## Final Investment Recommendation

DECISION: BUY NOW / WAIT

REASONING:
[Detailed explanation based on all findings]

TIMELINE:
[When to reconsider or monitoring plan]

RISKS:
[Key risks to be aware of]
```

## Example Workflow

1. **Topic Research** - Agent searches for recent S&P 500 and SPY news
2. **Report Planning** - Creates structure with sections for market overview, news analysis, and recommendation
3. **Section Research** - Each section researches specific aspects (market data, news events, sentiment)
4. **Section Writing** - Writes detailed analysis for each section using research
5. **Report Assembly** - Combines all sections into coherent report
6. **Investment Decision** - Analyzes full report and makes final BUY/WAIT recommendation

## Dependencies

- `langchain-nvidia-ai-endpoints` - For LLM access via OpenRouter
- `langgraph` - For workflow orchestration
- `tavily-python` - For web search (financial news)
- `pydantic` - For data models
- `python-dotenv` - For environment variables

## Environment Variables

Required:
- `TAVILY_API_KEY` - Tavily API key for web search
- `OPENROUTER_API_KEY` - OpenRouter API key for LLM access

Optional:
- `THROTTLE_LLM_CALLS` - Set to "1" to throttle parallel LLM calls

## Tips for Best Results

1. **Run Daily** - Best results when run daily to catch fresh news
2. **Morning Analysis** - Run in the morning before market open
3. **Compare Over Time** - Save reports to track sentiment trends
4. **Verify Sources** - Always review cited sources in the report
5. **Use as Input** - Treat recommendations as one input among many for decisions

## Limitations

- Based on publicly available news articles (not real-time trading data)
- Does not include technical analysis indicators
- Recommendations are educational, not financial advice
- Limited to 3-day news window (configurable)
- Depends on quality of news sources found by Tavily

## Future Enhancements

Potential improvements:
- [ ] Add real-time price data integration
- [ ] Include technical indicators (RSI, MACD, etc.)
- [ ] Support multiple tickers and ETFs
- [ ] Add sentiment scoring from news
- [ ] Historical backtesting of recommendations
- [ ] Integration with brokerage APIs
- [ ] Email/SMS alerts for decisions
- [ ] Portfolio optimization logic

## Disclaimer

This agent provides analysis and recommendations for educational purposes only. It is NOT financial advice. Always conduct your own research and consult with a licensed financial advisor before making investment decisions.
