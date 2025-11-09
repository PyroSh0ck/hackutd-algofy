"""
Stock Analysis Client - Run the stock market analysis agent to get investment recommendations.

This script generates daily stock market analysis reports focused on S&P 500 and SPY,
providing actionable investment recommendations based on recent news and market movements.
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the docgen_agent package to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from docgen_agent.agent import AgentState, graph


async def run_stock_analysis(
    investment_amount: float = 700.0,
    output_file: str = None
):
    """
    Run the stock market analysis agent and generate an investment report.

    Args:
        investment_amount: Amount in USD to consider investing (default: $700)
        output_file: Optional path to save the report (default: auto-generated filename)

    Returns:
        dict: The final state containing the report and investment decision
    """
    print("=" * 80)
    print("STOCK MARKET ANALYSIS AGENT")
    print("=" * 80)
    print(f"Investment Amount: ${investment_amount}")
    print(f"Target: S&P 500 / SPY ETF")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

    # Define the initial state
    initial_state = AgentState(
        topic="S&P 500 and SPY ETF",
        report_structure="""
        Create a concise stock market analysis report with the following sections:
        1. Recent Market Performance - Overview of S&P 500 and SPY performance in the last few days
        2. News Impact Analysis - Analysis of recent news articles explaining market movements
        3. Investment Recommendation - Clear BUY or WAIT decision with reasoning
        """,
        investment_amount=investment_amount,
    )

    print("🔍 Starting stock market research...")
    print()

    # Run the agent workflow
    final_state = await graph.ainvoke(initial_state)

    # Extract the report and decision
    report = final_state.get("report", "")
    decision = final_state.get("investment_decision", "UNCLEAR")

    print()
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"Investment Decision: {decision}")
    print("=" * 80)
    print()

    # Save the report to a file
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"stock_analysis_report_{timestamp}.md"

    output_path = Path(__file__).parent / "reports" / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"📄 Report saved to: {output_path}")
    print()

    # Display a summary
    print("=" * 80)
    print("REPORT SUMMARY")
    print("=" * 80)
    print(report[:1000] + "..." if len(report) > 1000 else report)
    print()
    print("=" * 80)

    return final_state


def main():
    """Main entry point for the stock analysis client."""
    # Check for required environment variables
    required_vars = ["TAVILY_API_KEY", "OPENROUTER_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        print("Please set these variables in your .env file or environment.")
        sys.exit(1)

    # Parse command line arguments
    investment_amount = 700.0
    if len(sys.argv) > 1:
        try:
            investment_amount = float(sys.argv[1])
        except ValueError:
            print(f"❌ Error: Invalid investment amount: {sys.argv[1]}")
            sys.exit(1)

    # Run the analysis
    try:
        asyncio.run(run_stock_analysis(investment_amount=investment_amount))
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
