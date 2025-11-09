// data/transactions.ts
import type { Txn } from "@/components/TransactionRow";

export const TRANSACTIONS: Txn[] = [
  { id: "t1", date: "2025-11-07", merchant: "H-E-B Market", category: "Groceries", amount: -64.28, account: "Fauget Checking", status: "posted" },
  { id: "t2", date: "2025-11-07", merchant: "Uber", category: "Transport", amount: -18.90, account: "Fauget Checking", status: "posted" },
  { id: "t3", date: "2025-11-06", merchant: "Spotify", category: "Entertainment", amount: -10.99, account: "Fauget Checking", status: "posted" },
  { id: "t4", date: "2025-11-06", merchant: "Starbucks", category: "Restaurants", amount: -6.45, account: "Fauget Checking", status: "posted" },
  { id: "t5", date: "2025-11-05", merchant: "Reliant Energy", category: "Utilities", amount: -82.13, account: "Fauget Checking", status: "posted" },
  { id: "t6", date: "2025-11-05", merchant: "Amazon", category: "Shopping", amount: -29.79, account: "Fauget Checking", status: "posted" },
  { id: "t7", date: "2025-11-04", merchant: "Alpaca – SPY buy", category: "Investing", amount: -200.00, account: "Fauget Checking", status: "posted" },
  { id: "t8", date: "2025-11-04", merchant: "Direct Deposit", category: "Income", amount: +2300.00, account: "Fauget Checking", status: "posted" },
  { id: "t9", date: "2025-11-03", merchant: "Transfer to HYSA", category: "Transfer", amount: -150.00, account: "Fauget Checking", status: "posted" },
  { id: "t10", date: "2025-11-02", merchant: "Lyft", category: "Transport", amount: -12.84, account: "Fauget Checking", status: "posted" },
  { id: "t11", date: "2025-11-02", merchant: "Delta Airlines", category: "Travel", amount: -216.40, account: "Fauget Checking", status: "posted" },
  { id: "t12", date: "2025-11-01", merchant: "Fauget Bank", category: "Fees", amount: -2.50, account: "Fauget Checking", status: "posted" },
  { id: "t13", date: "2025-10-31", merchant: "CVS Pharmacy", category: "Health", amount: -14.29, account: "Fauget Checking", status: "posted" },
];
