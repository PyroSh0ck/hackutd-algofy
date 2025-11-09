// app/(stack)/investments.tsx
import React, { useMemo } from "react";
import {
  View,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { ThemedView } from "@/components/themed-view";
import { ThemedText } from "@/components/themed-text";
import { IconSymbol } from "@/components/ui/icon-symbol";
import { DropDown } from "@/components/ui/dropdown";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import BarAllocation from "@/components/barallocation";
/** ---------- Theme (matched to app) ---------- */
const c = {
  bg: "#151718",
  cardA: "rgba(58, 158, 186, 0.1)",
  cardB: "rgba(58, 158, 186, 0.15)",
  teal: "#abebe3",
  tealStrong: "#3a9eba",
  ink: "#ffffff",
  mut: "rgba(171, 235, 227, 0.7)",
  stroke: "rgba(171, 235, 227, 0.15)",
  line: "rgba(171, 235, 227, 0.1)",
  red: "#e74c3c",
  green: "#2ecc71",
  chip: "rgba(171, 235, 227, 0.1)",
  chipStroke: "rgba(171, 235, 227, 0.25)",
};

type Holding = {
  symbol: string;
  name: string;
  qty: number;
  price: number; // current
  changePct: number; // day change %
  trend: number[]; // last N pseudo points for sparkline (0..1)
  bucket: "Core" | "Growth" | "Income";
};

const HOLDINGS: Holding[] = [
  {
    symbol: "SPY",
    name: "S&P 500 ETF",
    qty: 12.4,
    price: 512.23,
    changePct: 0.86,
    trend: [0.2, 0.26, 0.21, 0.34, 0.48, 0.44, 0.62, 0.58, 0.73, 0.69, 0.82],
    bucket: "Core",
  },
  {
    symbol: "VTI",
    name: "Total US Market",
    qty: 8.1,
    price: 263.11,
    changePct: -0.42,
    trend: [0.8, 0.76, 0.71, 0.63, 0.58, 0.61, 0.54, 0.56, 0.51, 0.49, 0.52],
    bucket: "Core",
  },
  {
    symbol: "QQQ",
    name: "Nasdaq 100",
    qty: 5.0,
    price: 436.02,
    changePct: 1.15,
    trend: [0.35, 0.4, 0.48, 0.44, 0.57, 0.66, 0.61, 0.69, 0.76, 0.83, 0.9],
    bucket: "Growth",
  },
  {
    symbol: "BND",
    name: "Total Bond",
    qty: 20.0,
    price: 73.40,
    changePct: 0.10,
    trend: [0.48, 0.49, 0.5, 0.49, 0.51, 0.5, 0.52, 0.53, 0.52, 0.53, 0.54],
    bucket: "Income",
  },
];

export default function InvestmentsScreen() {
  const totalValue = useMemo(() => {
    return HOLDINGS.reduce((sum, h) => sum + h.price * h.qty, 0);
  }, []);

  const dayChangePct = useMemo(() => {
    // quick fake aggregate: mean of weighted changes
    const cap = HOLDINGS.reduce((s, h) => s + h.price * h.qty, 0);
    const weighted =
      HOLDINGS.reduce((s, h) => s + (h.price * h.qty * h.changePct) / 100, 0) /
      cap;
    return weighted * 100;
  }, []);


  return (
    <ThemedView style={{ flex: 1, backgroundColor: c.bg }}>
      <ScrollView
        style={{ flex: 1 }}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{
          paddingTop: 20,
          paddingBottom: 28,
          paddingHorizontal: 16,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-start',
          alignItems: "stretch",
        }}
      >
        {/* ---------- Portfolio Header ---------- */}
        <LinearGradient
          colors={["#3a9eba", "#0f4959"]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={styles.hero}
        >
          <ThemedText style={styles.heroHi}>Investments</ThemedText>
          <ThemedText style={styles.heroSub}>
            Your portfolio overview and recent performance.
          </ThemedText>

          <View style={styles.valueRow}>
            <ThemedText style={{color: c.ink, fontSize: 28, fontFamily: 'Poppins_600SemiBol', letterSpacing: 0.3, paddingTop: 20}}>
              ${formatMoney(totalValue)}
            </ThemedText>
            <Pill
              kind={dayChangePct >= 0 ? "up" : "down"}
              label={`${dayChangePct >= 0 ? "▲" : "▼"} ${dayChangePct
                .toFixed(2)
                .replace("-", "")}% today`}
            />
          </View>

          <View style={styles.quickRow}>
            <QuickAction
              icon="plus-circle-outline"
              label="Deposit"
              onPress={() => {}}
            />
            <QuickAction
              icon="swap-horizontal"
              label="Transfer"
              onPress={() => {}}
            />
            <QuickAction
              icon="cart-arrow-down"
              label="Buy/Sell"
              onPress={() => {}}
            />
          </View>
        </LinearGradient>

        {/* ---------- Watchlist (example) ---------- */}
          <View style={styles.card}>
            <ScrollView>
              <WatchRow symbol="NVDA" name="NVIDIA" price={128.22} changePct={-0.92} />
              <WatchRow symbol="MSFT" name="Microsoft" price={423.12} changePct={0.24} />
              <WatchRow symbol="AAPL" name="Apple" price={192.44} changePct={0.31} />
              <WatchRow symbol="AMZN" name="Amazon" price={181.73} changePct={-0.12} />
              <WatchRow symbol="GOOGL" name="Alphabet Class A" price={165.88} changePct={0.47} />
              <WatchRow symbol="META" name="Meta Platforms" price={492.10} changePct={-0.28} />
              <WatchRow symbol="TSLA" name="Tesla" price={204.55} changePct={1.15} />
              <WatchRow symbol="BRK.B" name="Berkshire Hathaway B" price={449.62} changePct={0.05} />
              <WatchRow symbol="V" name="Visa" price={282.91} changePct={0.19} />
              <WatchRow symbol="XOM" name="ExxonMobil" price={113.74} changePct={-0.41} />
              <WatchRow symbol="JPM" name="JPMorgan Chase" price={197.32} changePct={0.22} />
              <WatchRow symbol="UNH" name="UnitedHealth" price={546.89} changePct={-0.36} last />
            </ScrollView>
          </View>

        {/* ---------- Holdings ---------- */}
        <DropDown dropDownName="Holdings">
          <View style={{width: '100%', marginBottom: 8, borderWidth: 1, borderColor: c.stroke, borderRadius: 20, overflow: 'scroll', backgroundColor: c.cardA, padding: 12}}>
            {HOLDINGS.map((h, i) => (
              <HoldingRow key={h.symbol} holding={h} last={i === HOLDINGS.length - 1} />
            ))}
          </View>
        </DropDown>



        {/* ---------- Tip ---------- */}
        <LinearGradient
          colors={["#3a9eba", "#0f4959"]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={styles.tip}
        >
          <MaterialCommunityIcons
            name="information-outline"
            size={16}
            color={c.teal}
            style={{ marginRight: 8 }}
          />
          <ThemedText style={styles.tipText}>
            Pro tip: Set “Allow investing payments” in Safety Controls to let Algofy
            auto-invest excess cash after bills.
          </ThemedText>
        </LinearGradient>
      </ScrollView>
    </ThemedView>
  );
}

/** ---------- Atoms ---------- */
function Pill({ kind, label }: { kind: "up" | "down"; label: string }) {
  const bg = kind === "up" ? "rgba(127,255,178,0.18)" : "rgba(255,142,142,0.18)";
  const border = kind === "up" ? "rgba(127,255,178,0.45)" : "rgba(255,142,142,0.45)";
  const color = kind === "up" ? c.green : c.red;
  return (
    <View
      style={{
        paddingHorizontal: 10,
        paddingVertical: 6,
        borderRadius: 999,
        backgroundColor: bg,
        borderWidth: 1,
        borderColor: border,
      }}
    >
      <ThemedText style={{ color, fontWeight: "700", fontSize: 12 }}>{label}</ThemedText>
    </View>
  );
}

function QuickAction({
  icon,
  label,
  onPress,
}: {
  icon: keyof typeof MaterialCommunityIcons.glyphMap;
  label: string;
  onPress: () => void;
}) {
  return (
    <TouchableOpacity onPress={onPress} style={styles.quick}>
      <MaterialCommunityIcons name={icon} size={18} color={c.teal} />
      <ThemedText style={styles.quickText}>{label}</ThemedText>
    </TouchableOpacity>
  );
}

/** ---------- Rows ---------- */
function HoldingRow({ holding, last }: { holding: Holding; last?: boolean }) {
  const value = holding.qty * holding.price;
  const color = holding.changePct >= 0 ? c.green : c.red;

  return (
    <View
      style={[
        styles.hRow,
        !last && { borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: c.line },
      ]}
    >
      <View style={styles.hLeft}>
        <View style={styles.logoBox}>
          <ThemedText style={styles.logoText}>{holding.symbol.slice(0, 3)}</ThemedText>
        </View>
        <View style={{ flex: 1 }}>
          <ThemedText style={styles.hName}>{holding.name}</ThemedText>
          <ThemedText style={styles.hSub}>
            {holding.symbol} • {holding.qty} shares
          </ThemedText>
        </View>
      </View>

      <View style={styles.hRight}>
        <View style={{ alignItems: "flex-end" }}>
          <ThemedText style={styles.hValue}>${formatMoney(value)}</ThemedText>
          <ThemedText style={[styles.hChange, { color }]}>
            {holding.changePct >= 0 ? "+" : ""}
            {holding.changePct.toFixed(2)}%
          </ThemedText>
        </View>
      </View>
    </View>
  );
}

function WatchRow({
  symbol,
  name,
  price,
  changePct,
  last,
}: {
  symbol: string;
  name: string;
  price: number;
  changePct: number;
  last?: boolean;
}) {
  const color = changePct >= 0 ? c.green : c.red;
  return (
    <View
      style={[
        styles.hRow,
        !last && { borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: c.line },
      ]}
    >
      <View style={styles.hLeft}>
        <View style={[styles.logoBox, { backgroundColor: c.cardB }]}>
          <IconSymbol name="eye" size={16} color={c.teal} />
        </View>
        <View>
          <ThemedText style={styles.hName}>{name}</ThemedText>
          <ThemedText style={styles.hSub}>{symbol}</ThemedText>
        </View>
      </View>

      <View style={{ alignItems: "flex-end" }}>
        <ThemedText style={styles.hValue}>${price.toFixed(2)}</ThemedText>
        <ThemedText style={[styles.hChange, { color }]}>
          {changePct >= 0 ? "+" : ""}
          {changePct.toFixed(2)}%
        </ThemedText>
      </View>
    </View>
  );
}

/** ---------- Utils ---------- */
function formatMoney(n: number) {
  return n
    .toFixed(2)
    .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/** ---------- Styles ---------- */
const styles = StyleSheet.create({
  hero: {
    width: "100%",
    alignSelf: "stretch",
    marginBottom: 14,
    borderRadius: 24,
    padding: 18,
    borderWidth: 1,
    borderColor: c.stroke,
    shadowColor: "#000",
    shadowOpacity: 0.35,
    shadowRadius: 14,
    shadowOffset: { width: 0, height: 10 },
    elevation: 8,
  },
  heroHi: {
    color: "#E8FEFF",
    fontSize: 20,
    fontWeight: "800",
    marginBottom: 4,
  },
  heroSub: { color: "rgba(232,254,255,0.85)", fontSize: 13, lineHeight: 18 },
  valueRow: {
    marginTop: 14,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  valueText: { color: c.ink, fontSize: 28, fontWeight: "800", letterSpacing: 0.3 },
  quickRow: {
    marginTop: 14,
    flexDirection: "row",
    gap: 10,
  },
  quick: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    backgroundColor: c.chip,
    borderColor: c.chipStroke,
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 8,
    borderRadius: 12,
  },
  quickText: { color: c.teal, fontWeight: "700", fontSize: 12 },

  card: {
    width: "100%",
    alignSelf: "stretch",
    marginBottom: 12,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: c.stroke,
    overflow: "hidden",
    backgroundColor: c.cardA,
    padding: 12,
    maxHeight: 300,
  },
  sectionTitle: { color: c.ink, fontWeight: "800", fontSize: 14, marginBottom: 10 },

  allocWrap: {
    height: 20,
    borderRadius: 10,
    overflow: "hidden",
    backgroundColor: c.cardB,
    borderWidth: 1,
    borderColor: c.line,
  },
  legendRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
    marginTop: 10,
  },
  legendItem: { flexDirection: "row", alignItems: "center", gap: 6 },
  legendDot: { width: 10, height: 10, borderRadius: 5 },
  legendText: { color: c.mut, fontSize: 12 },

  hRow: {
    paddingVertical: 12,
    paddingHorizontal: 8,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  hLeft: { flexDirection: "row", alignItems: "center", gap: 10, flex: 1 },
  hRight: { flexDirection: "row", alignItems: "center", gap: 12 },
  logoBox: {
    width: 32,
    height: 32,
    borderRadius: 10,
    backgroundColor: c.chip,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: c.chipStroke,
  },
  logoText: { color: c.teal, fontWeight: "800", fontSize: 11, letterSpacing: 0.5 },
  hName: { color: c.ink, fontWeight: "700", fontSize: 13 },
  hSub: { color: c.mut, fontSize: 11, marginTop: 2 },
  hValue: { color: c.ink, fontWeight: "800", fontSize: 13 },
  hChange: { fontWeight: "800", fontSize: 11 },

  tip: {
    width: "100%",
    alignSelf: "stretch",
    marginTop: 6,
    marginBottom: 24,
    borderRadius: 16,
    padding: 12,
    borderWidth: 1,
    borderColor: c.line,
    flexDirection: "row",
    alignItems: "center",
  },
  tipText: { color: "rgba(232,254,255,0.9)", fontSize: 12, lineHeight: 18, paddingHorizontal: 20 },
});
