"""
Response Formatters

Different formatting styles for various response types.
"""

from typing import Dict, Any, List
from datetime import datetime


class ResponseFormatters:
    """Formatting utilities for different response types"""

    @staticmethod
    def format_account_balances(accounts: List[Dict[str, Any]]) -> str:
        """Format account balances in a clean table"""
        if not accounts:
            return "No accounts found."

        response = "💰 **Your Accounts**\n\n"
        response += "```\n"
        response += f"{'Account':<20} {'Type':<15} {'Balance':>15}\n"
        response += "-" * 52 + "\n"

        total = 0
        for acc in accounts:
            name = acc.get('name', 'Unknown')[:19]
            acc_type = acc.get('type', 'N/A')[:14]
            balance = acc.get('balance', 0)
            total += balance

            response += f"{name:<20} {acc_type:<15} ${balance:>13,.2f}\n"

        response += "-" * 52 + "\n"
        response += f"{'TOTAL':<35} ${total:>13,.2f}\n"
        response += "```\n"

        return response

    @staticmethod
    def format_budget_summary(budget: Dict[str, Any]) -> str:
        """Format budget summary with 50/30/20 breakdown"""
        income = budget.get('total_income', 0)
        spent = budget.get('total_spent', 0)
        remaining = income - spent

        response = f"📊 **Budget Summary - {budget.get('month', 'Current Month')}**\n\n"
        response += f"**Income:** ${income:,.2f}\n"
        response += f"**Spent:** ${spent:,.2f}\n"
        response += f"**Remaining:** ${remaining:,.2f}\n\n"

        response += "**50/30/20 Breakdown:**\n\n"

        categories = [
            ("NEEDS (50%)", budget.get('needs_budget', 0), budget.get('needs_spent', 0)),
            ("WANTS (30%)", budget.get('wants_budget', 0), budget.get('wants_spent', 0)),
            ("SAVINGS (20%)", budget.get('savings_budget', 0), budget.get('savings_spent', 0))
        ]

        for name, budgeted, spent in categories:
            percent = (spent / budgeted * 100) if budgeted > 0 else 0
            status = ResponseFormatters._budget_status_emoji(percent)
            progress_bar = ResponseFormatters._progress_bar(percent, 20)

            response += f"{status} **{name}**\n"
            response += f"   Budgeted: ${budgeted:,.2f} | Spent: ${spent:,.2f}\n"
            response += f"   {progress_bar} {percent:.1f}%\n\n"

        return response

    @staticmethod
    def format_transactions(transactions: List[Dict[str, Any]], limit: int = 10) -> str:
        """Format transaction list"""
        if not transactions:
            return "No recent transactions found."

        response = "📝 **Recent Transactions**\n\n"

        for i, txn in enumerate(transactions[:limit]):
            date = txn.get('date', 'N/A')
            description = txn.get('description', 'Unknown')[:40]
            amount = txn.get('amount', 0)
            category = txn.get('category', 'Uncategorized')

            response += f"{i+1}. **{description}**\n"
            response += f"   ${amount:,.2f} • {category} • {date}\n\n"

        if len(transactions) > limit:
            response += f"\n_...and {len(transactions) - limit} more transactions_\n"

        return response

    @staticmethod
    def format_trade_proposal(proposal: Dict[str, Any]) -> str:
        """Format trade proposal for confirmation"""
        response = "📊 **TRADE PROPOSAL**\n\n"
        response += "```\n"
        response += f"Symbol:          {proposal.get('symbol', 'N/A')}\n"
        response += f"Action:          {proposal.get('side', 'N/A').upper()}\n"
        response += f"Amount:          ${proposal.get('usd_amount', 0):,.2f}\n"
        response += f"Order Type:      {proposal.get('order_type', 'N/A').upper()}\n"
        response += f"Current Price:   ${proposal.get('current_price', 0):.2f}\n"
        response += f"Est. Shares:     {proposal.get('estimated_shares', 0):.4f}\n"
        response += "\n"
        response += f"Available Funds: ${proposal.get('available_funds', 0):,.2f}\n"
        response += f"After Trade:     ${proposal.get('available_funds', 0) - proposal.get('usd_amount', 0):,.2f}\n"
        response += "```\n\n"

        response += f"**Rationale:**\n{proposal.get('rationale', 'No rationale provided.')}\n\n"
        response += "⚠️ **Reply 'CONFIRM TRADE' to execute this order.**\n"

        return response

    @staticmethod
    def format_stock_quote(quote: Dict[str, Any]) -> str:
        """Format stock quote"""
        symbol = quote.get('symbol', 'N/A')
        price = quote.get('current_price', 0)
        bid = quote.get('bid', 0)
        ask = quote.get('ask', 0)
        spread = quote.get('spread', 0)
        timestamp = quote.get('timestamp', 'N/A')

        response = f"📈 **{symbol}** - Real-Time Quote\n\n"
        response += "```\n"
        response += f"Last Price:  ${price:.2f}\n"
        response += f"Bid:         ${bid:.2f}\n"
        response += f"Ask:         ${ask:.2f}\n"
        response += f"Spread:      ${spread:.2f}\n"
        response += f"As of:       {timestamp}\n"
        response += "```\n"

        return response

    @staticmethod
    def format_investment_recommendation(analysis: Dict[str, Any]) -> str:
        """Format investment analysis and recommendation"""
        decision = analysis.get('decision', 'UNKNOWN')
        reasoning = analysis.get('reasoning', 'No reasoning provided.')
        confidence = analysis.get('confidence', 'medium')

        emoji = "✅" if decision == "BUY" else "⏸️"
        color = "green" if decision == "BUY" else "yellow"

        response = f"{emoji} **Investment Recommendation: {decision}**\n\n"
        response += f"**Confidence:** {confidence.title()}\n\n"
        response += f"**Analysis:**\n{reasoning}\n\n"

        if decision == "BUY":
            response += "💡 **Next Steps:**\n"
            response += "1. Check your available funds\n"
            response += "2. Decide how much to invest\n"
            response += "3. Say 'Buy $X of [SYMBOL]' to proceed\n"
        else:
            response += "💡 **Recommendation:**\n"
            response += "Consider waiting for better market conditions or diversifying your portfolio.\n"

        return response

    @staticmethod
    def format_savings_goals(goals: List[Dict[str, Any]]) -> str:
        """Format savings goals progress"""
        if not goals:
            return "No savings goals set yet. Would you like to create one?"

        response = "🎯 **Your Savings Goals**\n\n"

        for goal in goals:
            name = goal.get('name', 'Unnamed Goal')
            current = goal.get('current_saved', 0)
            target = goal.get('target_amount', 0)
            target_date = goal.get('target_date', 'No date set')
            monthly = goal.get('monthly_contribution', 0)

            progress = (current / target * 100) if target > 0 else 0
            progress_bar = ResponseFormatters._progress_bar(progress, 30)

            response += f"**{name}**\n"
            response += f"   {progress_bar} {progress:.1f}%\n"
            response += f"   ${current:,.2f} of ${target:,.2f}\n"
            response += f"   ${monthly:,.2f}/month • Target: {target_date}\n\n"

        return response

    @staticmethod
    def format_error(error_type: str, message: str, suggestions: List[str] = None) -> str:
        """Format error messages with helpful suggestions"""
        response = f"❌ **{error_type}**\n\n"
        response += f"{message}\n\n"

        if suggestions:
            response += "💡 **Try this instead:**\n"
            for i, suggestion in enumerate(suggestions, 1):
                response += f"{i}. {suggestion}\n"

        return response

    @staticmethod
    def format_success(message: str, details: Dict[str, Any] = None) -> str:
        """Format success messages"""
        response = f"✅ **Success!**\n\n{message}\n"

        if details:
            response += "\n**Details:**\n"
            for key, value in details.items():
                response += f"• {key}: {value}\n"

        return response

    # Helper methods
    @staticmethod
    def _progress_bar(percent: float, width: int = 20) -> str:
        """Generate a text progress bar"""
        filled = int(percent / 100 * width)
        empty = width - filled
        return f"[{'█' * filled}{'░' * empty}]"

    @staticmethod
    def _budget_status_emoji(percent: float) -> str:
        """Get emoji based on budget percentage"""
        if percent < 80:
            return "✅"
        elif percent < 100:
            return "⚠️"
        else:
            return "🔴"

    @staticmethod
    def format_help_menu() -> str:
        """Format help menu with available commands"""
        return """
🤖 **Financial Assistant Help**

**Money Manager:**
• "How much money do I have?" - Check balances
• "Show my transactions" - View recent spending
• "Move $X to savings" - Transfer money

**Trading:**
• "What's the price of SPY?" - Get real-time quote
• "Buy $500 of VOO" - Invest in ETF
• "How much can I invest?" - Check available funds

**Budget:**
• "Create a budget" - Set up 50/30/20 budget
• "How am I doing?" - Check budget status
• "I want to save for [goal]" - Add savings goal

**Analysis:**
• "Should I invest?" - Get market recommendation
• "What's happening in the market?" - Latest news

**Reports:**
• "Email me a budget summary" - Get monthly report
• "Send weekly spending report" - Track expenses

Type any question in plain English - I'll understand! 😊
"""
