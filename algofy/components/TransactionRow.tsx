// components/TransactionRow.tsx
import React from "react";
import { View, StyleSheet, TouchableOpacity } from "react-native";
import { ThemedText } from "@/components/themed-text";
import { MaterialCommunityIcons } from "@expo/vector-icons";

const c = {
  ink: "rgba(255,255,255,0.9)",
  mut: "rgba(234,251,252,0.65)",
  chip: "rgba(157,239,240,0.10)",
  chipStroke: "rgba(157,239,240,0.25)",
  red: "#FF8C8C",
  green: "#7FFFB2",
  line: "rgba(255,255,255,0.06)",
};

export type Txn = {
  id: string;
  date: string;           // ISO date
  merchant: string;
  category: "Groceries"|"Restaurants"|"Transport"|"Shopping"|"Utilities"|"Entertainment"|"Income"|"Transfer"|"Investing"|"Fees"|"Health"|"Travel";
  amount: number;         // negative = debit, positive = credit
  account?: string;       // e.g., 'Fauget Checking'
  status?: "posted"|"pending";
};

const ICONS: Record<Txn["category"], keyof typeof MaterialCommunityIcons.glyphMap> = {
  Groceries: "cart-outline",
  Restaurants: "silverware-fork-knife",
  Transport: "car-outline",
  Shopping: "bag-personal-outline",
  Utilities: "flash-outline",
  Entertainment: "ticket-confirmation-outline",
  Income: "cash-plus",
  Transfer: "swap-horizontal",
  Investing: "chart-line",
  Fees: "receipt-outline",
  Health: "heart-pulse",
  Travel: "airplane",
};

export function formatCurrency(v: number) {
  const s = Math.abs(v).toFixed(2);
  return `${v < 0 ? "-" : "+"}$${s}`;
}
export function formatDate(iso: string) {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

export default function TransactionRow({ txn, last }: { txn: Txn; last?: boolean }) {
  const color = txn.amount >= 0 ? c.green : c.red;
  return (
    <TouchableOpacity activeOpacity={0.9}>
      <View style={[styles.row, !last && { borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: c.line }]}>
        <View style={styles.iconWrap}>
          <MaterialCommunityIcons name={ICONS[txn.category]} size={18} color={c.mut} />
        </View>
        <View style={{ flex: 1 }}>
          <ThemedText style={styles.title}>{txn.merchant}</ThemedText>
          <ThemedText style={styles.sub}>
            {txn.category} • {formatDate(txn.date)}
            {txn.status === "pending" ? " • pending" : ""}
          </ThemedText>
        </View>
        <ThemedText style={[styles.amount, { color }]}>{formatCurrency(txn.amount)}</ThemedText>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", alignItems: "center", gap: 10, paddingHorizontal: 14, paddingVertical: 12 },
  iconWrap: {
    width: 28, height: 28, borderRadius: 8,
    backgroundColor: c.chip, borderWidth: 1, borderColor: c.chipStroke,
    alignItems: "center", justifyContent: "center",
  },
  title: { color: c.ink, fontWeight: "700", fontSize: 14 },
  sub: { color: c.mut, fontSize: 12, marginTop: 2 },
  amount: { fontWeight: "800", fontSize: 13 },
});
