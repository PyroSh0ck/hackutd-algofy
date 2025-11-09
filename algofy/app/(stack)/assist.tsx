import React, { useEffect, useRef, useState } from "react";
import {
  View,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  NativeSyntheticEvent,
  TextInputFocusEventData,
  LayoutChangeEvent,
  Keyboard,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { LinearGradient } from "expo-linear-gradient";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { ThemedView } from "@/components/themed-view";
import { ThemedText } from "@/components/themed-text";

/* ---------------- Theme ---------------- */
const c = {
  bg: "#0B0E0F",
  cardA: "#0F1A1D",
  cardB: "#142629",
  teal: "#9FEFF0",
  tealStrong: "#2DBAC5",
  ink: "rgba(255,255,255,0.92)",
  mut: "rgba(234,251,252,0.75)",
  stroke: "rgba(255,255,255,0.08)",
  line: "rgba(255,255,255,0.06)",
  chip: "rgba(157,239,240,0.10)",
  chipStroke: "rgba(157,239,240,0.25)",
  green: "#7FFFB2",
  red: "#FF8C8C",
};

/* ---------------- Timing ---------------- */
const CADENCE = {
  step: 1000,     // 1s per step
  postLight: 200,
  postHeavy: 1000,
};
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/* ---------------- Types ---------------- */
type Role = "user" | "assistant";
type Msg = { id: string; role: Role; text: string; ts: number };
type ThinkStep = { agent: string; detail: string };
type InlineThinking = {
  forId: string | null;
  open: boolean;
  title: string | null;
  steps: ThinkStep[];
};

/* ---------------- Presets ---------------- */
const EXAMPLES = [
  {
    id: "save_and_trip_combo",
    title: "Save $1,000 by 2026 + free cash for a trip",
    text:
      "Moni, plan to save $1,000 by 2026 and also rework my budget to free cash for a trip—use my data automatically.",
  },
  {
    id: "spy_report_invest",
    title: "Detailed report on SPY (+ ask to invest $200)",
    text:
      "Moni, create a detailed report on SPY and—if it looks reasonable—ask whether to invest $200 from my savings.",
  },
  {
    id: "auto_move_threshold",
    title: "Auto-move excess from Checking → Savings",
    text:
      "Moni, whenever my checking goes above a set amount, automatically sweep the extra into savings.",
  },
];

/* --- Recursive Research → … → Report steps for a ticker --- */
const buildRecursiveResearchSteps = (ticker = "SPY"): ThinkStep[] => [
  { agent: "Research Agent", detail: `Pass 1: seed query for ${ticker} (overview & fee)…` },
  { agent: "Research Agent", detail: "Pass 2: crawl issuer factsheets & methodology…" },
  { agent: "Research Agent", detail: "Pass 3: fetch latest news & dedup sources…" },
  { agent: "Research Agent", detail: "Pass 4: scan filings/prospectus for updates…" },
  { agent: "Research Agent", detail: "Pass 5: pull AUM, avg spread, daily volume…" },
  { agent: "Research Agent", detail: "Pass 6: compute sector weights & top holdings…" },
  { agent: "Report Agent",   detail: "Synthesize findings → concise brief & risks…" },
];

/* ---------------- Inline Thinking (attached to a message) ---------------- */
function InlineThinkingBox({
  title,
  steps,
  open,
  onToggle,
}: {
  title: string | null;
  steps: ThinkStep[];
  open: boolean;
  onToggle: () => void;
}) {
  if (!title) return null;
  return (
    <View style={styles.thinkWrapInline}>
      <TouchableOpacity onPress={onToggle} style={styles.thinkHeader} activeOpacity={0.9}>
        <ThemedText style={styles.thinkTitle}>
          {open ? "Thinking — details" : "Thinking"}
        </ThemedText>
        <MaterialCommunityIcons
          name={open ? "chevron-up" : "chevron-down"}
          size={18}
          color={c.teal}
        />
      </TouchableOpacity>

      {open && (
        <View style={styles.thinkBody}>
          <ThemedText style={styles.thinkLine}>
            <ThemedText style={{ color: c.mut }}>Route:</ThemedText> {title}
          </ThemedText>
          {steps.map((s, i) => (
            <View key={`${s.agent}-${i}`} style={styles.thinkRow}>
              <MaterialCommunityIcons
                name="progress-clock"
                size={16}
                color={c.teal}
                style={{ marginRight: 6 }}
              />
              <ThemedText style={styles.thinkLine}>
                <ThemedText style={{ color: c.teal }}>{s.agent}</ThemedText>
                <ThemedText style={{ color: c.mut }}> — </ThemedText>
                {s.detail}
              </ThemedText>
            </View>
          ))}
        </View>
      )}
    </View>
  );
}

/* ---------------- Assistant ---------------- */
export default function AssistantMoni() {
  const insets = useSafeAreaInsets();
  const TOP_GAP = insets.top + 28;
  const BOTTOM_GAP = Math.max(insets.bottom, 10);

  const [messages, setMessages] = useState<Msg[]>([
    {
      id: "assistant-init-0",
      role: "assistant",
      text:
        "Hey, I’m Moni. Your personal financial agent! I'm ready to help with whatever you need! Just ask me a question or choose an example to get started.",
      ts: Date.now(),
    },
  ]);
  const [text, setText] = useState("");
  const [waitingSpyDecision, setWaitingSpyDecision] = useState(false);

  const scrollRef = useRef<ScrollView>(null);
  const inputRef = useRef<TextInput>(null);
  const idCounter = useRef(1); // unique IDs
  const [kbHeight, setKbHeight] = useState(0);

  // Inline thinking state (always attached to a specific message)
  const [thinking, setThinking] = useState<InlineThinking>({
    forId: null,
    open: true,
    title: null,
    steps: [],
  });

  const nextId = (role: Role) => `${role}-${Date.now()}-${idCounter.current++}`;

  // Auto-scroll to bottom whenever messages change or thinking steps grow
  useEffect(() => {
    requestAnimationFrame(() => scrollRef.current?.scrollToEnd({ animated: true }));
  }, [messages.length, thinking.steps.length]);

  const handleContentSizeChange = () => {
    requestAnimationFrame(() => scrollRef.current?.scrollToEnd({ animated: true }));
  };

  // Keyboard listeners to keep input visible
  useEffect(() => {
    const show = Keyboard.addListener("keyboardDidShow", (e) => setKbHeight(e.endCoordinates.height));
    const hide = Keyboard.addListener("keyboardDidHide", () => setKbHeight(0));
    return () => {
      show.remove();
      hide.remove();
    };
  }, []);

  const addMsg = (role: Role, body: string): string => {
    const id = nextId(role);
    setMessages((prev) => [...prev, { id, role, text: body, ts: Date.now() }]);
    return id;
  };

  // Inline thinking helpers
  const resetThinking = () =>
    setThinking({ forId: null, open: true, title: null, steps: [] });

  const attachThinking = (forId: string, title: string) =>
    setThinking({ forId, open: true, title, steps: [] });

  const pushStep = (s: ThinkStep) =>
    setThinking((t) => ({ ...t, steps: [...t.steps, s] }));

  async function streamStepsInline(forId: string, routeLabel: string, items: ThinkStep[], heavy = false) {
    // attach to this message
    attachThinking(forId, routeLabel);

    for (let i = 0; i < items.length; i++) {
      await sleep(CADENCE.step);
      pushStep(items[i]);
    }
    await sleep(heavy ? CADENCE.postHeavy : CADENCE.postLight);
    // keep visible until the final result is posted
  }

  /* ---------------- Scripts ---------------- */
  const runScript = async (id: string) => {
    if (id === "save_and_trip_combo") {
      const userId = addMsg("user", EXAMPLES[0].text);

      await streamStepsInline(
        userId,
        "Orchestrator → Banking Agent → Budget Agent → Response Agent",
        [
          { agent: "Orchestrator", detail: "Dispatching to Budget pipeline…" },
          { agent: "Banking Agent", detail: "Pulling balances & recurring bills…" },
          { agent: "Ledger Agent", detail: "Reading last 3 months of category spend & variance…" },
          { agent: "Budget Agent", detail: "Estimating safe trims (low lifestyle impact)…" },
          { agent: "Budget Agent", detail: "Setting goal target & autosave schedule…" },
        ]
      );

      addMsg(
        "assistant",
        "Plan set: Save $45/mo for 22 months = $990, plus a one-time $10 from cashback → $1,000 by Dec 2026."
      );
      addMsg(
        "assistant",
        "Trip funding: trim Dining −$25, Shopping −$20, Entertainment −$15, Subscriptions −$10. Frees **$95/mo** to “Trip Fund”."
      );
      addMsg(
        "assistant",
        "Automation: created monthly autosave ($45) to HYSA goal “$1k by 2026” and monthly transfer ($95) to “Trip Fund”. I’ll alert you if trimmed categories trend over."
      );
      return;
    }

    if (id === "spy_report_invest") {
      const userId = addMsg("user", EXAMPLES[1].text);

      // Recursive Research → … → Report under THIS user message
      await streamStepsInline(
        userId,
        "Orchestrator → Research → Research → … → Report",
        buildRecursiveResearchSteps("SPY")
      );

      addMsg(
        "assistant",
        "SPY: low-cost S&P 500 exposure (0.09% fee), very liquid, diversified across large-cap sectors. Risks: broad market drawdowns + megacap concentration."
      );
      addMsg(
        "assistant",
        "You have about $200 idle in savings. Do you want me to invest that into SPY?"
      );

      setWaitingSpyDecision(true);
      return;
    }

    if (id === "auto_move_threshold") {
      const userId = addMsg("user", EXAMPLES[2].text);

      await streamStepsInline(
        userId,
        "Orchestrator → Banking Agent → Response Agent",
        [
          { agent: "Banking Agent", detail: "Reading Checking & Savings balances…" },
          { agent: "Banking Agent", detail: "Computing dynamic cushion (avg weekly outflows + 15%)…" },
          { agent: "Banking Agent", detail: "Composing sweep rule with threshold & schedule…" },
        ]
      );

      addMsg(
        "assistant",
        "Rule created: when Checking closes > $1,500, sweep excess to HYSA next morning at 6am. You’ll get a push when a sweep occurs. Want a different threshold?"
      );
      return;
    }
  };

  /* ---------------- Free send (and SPY confirm) ---------------- */
  const onSend = async () => {
    const body = text.trim();
    if (!body) return;
    const uid = addMsg("user", body);
    setText("");

    if (waitingSpyDecision) {
      setWaitingSpyDecision(false);

      const dollars = 200;
      const price = 509.42;
      const shares = +(dollars / price).toFixed(4);

      await streamStepsInline(
        uid,
        "Trading Agent → Alpaca",
        [
          { agent: "Trading Agent", detail: "Authenticating brokerage connection…" },
          { agent: "Trading Agent", detail: "Verifying available cash & fractional trading…" },
          { agent: "Alpaca", detail: `Placing market buy SPY for $${dollars.toFixed(2)}…` },
          { agent: "Alpaca", detail: "Awaiting execution & fill price…" },
        ],
        true
      );

      addMsg(
        "assistant",
        `Executed: Bought ~${shares} SPY @ ${price.toFixed(
          2
        )}. Estimated cost $${dollars.toFixed(2)}. Position will appear in your Portfolio card.`
      );
      return;
    }

    // Generic flow attached under this message
    await streamStepsInline(
      uid,
      "Orchestrator → Response Agent",
      [
        { agent: "Response Agent", detail: "Parsing intent…" },
        { agent: "Response Agent", detail: "Drafting response…" },
      ]
    );
    addMsg(
      "assistant",
      "Got it! I prepared a plan. If you want me to act on it automatically, say the word or pick a preset above."
    );
  };

  // When focusing the input, push scroll to bottom so the field is visible above keyboard
  // Use a permissive event type to satisfy different platform typings (web vs native)
  const onInputFocus = (_e?: any) => {
    requestAnimationFrame(() => scrollRef.current?.scrollToEnd({ animated: true }));
  };

  // Attach inline thinking box under the specific message
  const renderMessageWithThinking = (m: Msg) => {
    const isUser = m.role === "user";
    const showThinkingInline = thinking.forId === m.id;

    return (
      <View key={m.id} style={{ gap: 8 }}>
        <View
          style={[
            styles.bubble,
            isUser ? styles.bubbleUser : styles.bubbleAi,
            isUser ? { alignSelf: "flex-end" } : { alignSelf: "flex-start" },
          ]}
        >
          {m.role === "assistant" && (
            <View style={styles.aiBadge}>
              <MaterialCommunityIcons name="robot-happy-outline" size={12} color="#062C30" />
              <ThemedText style={styles.aiBadgeText}>Moni</ThemedText>
            </View>
          )}
          <ThemedText style={styles.bubbleText}>{m.text}</ThemedText>
        </View>

        {/* Inline thinking panel right under the message that triggered it */}
        {showThinkingInline && (
          <InlineThinkingBox
            title={thinking.title}
            steps={thinking.steps}
            open={thinking.open}
            onToggle={() => setThinking((t) => ({ ...t, open: !t.open }))}
          />
        )}
      </View>
    );
  };

  return (
    <ThemedView style={{ flex: 1, backgroundColor: c.bg }}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior="padding" // use padding on both platforms to ensure visibility
      >
        <ScrollView
          ref={scrollRef}
          style={{ flex: 1 }}
          keyboardShouldPersistTaps="handled"
          keyboardDismissMode={Platform.select({ ios: "interactive", android: "on-drag" })}
          onContentSizeChange={handleContentSizeChange}
          contentInsetAdjustmentBehavior="never"
          showsVerticalScrollIndicator={false}
          contentContainerStyle={{
            paddingBottom: (16 + BOTTOM_GAP + 76) + kbHeight * 0.2,
            paddingHorizontal: 16,
            alignItems: "stretch",
          }}
        >
          <View style={{ height: insets.top + 28 }} />

          {/* Hero */}
          <LinearGradient
            colors={["#0E3B43", "#167D7F"]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.hero}
          >
            <ThemedText style={styles.heroHi}>Assistant — Moni</ThemedText>
            <ThemedText style={styles.heroSub}>
              Tap an example, or ask me a question to see what I can do!
            </ThemedText>
          </LinearGradient>

          {/* Examples */}
          <View style={styles.exampleWrap}>
            {EXAMPLES.map((ex, idx) => (
              <TouchableOpacity
                key={`${ex.id}-${idx}`}
                activeOpacity={0.9}
                onPress={() => runScript(ex.id)}
                style={styles.exampleCard}
              >
                <View style={styles.exampleIcon}>
                  <MaterialCommunityIcons name="magic-staff" size={16} color={c.teal} />
                </View>
                <View style={{ flex: 1 }}>
                  <ThemedText style={styles.exampleTitle}>{ex.title}</ThemedText>
                  <ThemedText style={styles.exampleHint} numberOfLines={2}>
                    {ex.text}
                  </ThemedText>
                </View>
                <MaterialCommunityIcons name="arrow-top-right" size={16} color={c.teal} />
              </TouchableOpacity>
            ))}
          </View>

          {/* Messages + inline thinking */}
          <View style={{ gap: 10, marginTop: 6 }}>
            {messages.map(renderMessageWithThinking)}
          </View>
        </ScrollView>

        {/* Input Bar */}
        <View style={[styles.inputBar, { paddingBottom: BOTTOM_GAP }]}>
          <TextInput
            ref={inputRef}
            value={text}
            onChangeText={setText}
            onFocus={onInputFocus}
            placeholder={
              waitingSpyDecision ? "Type anything to confirm investing $200 in SPY…" : "Ask Moni…"
            }
            placeholderTextColor={c.mut}
            multiline
            style={styles.input}
            textAlignVertical="top"
          />
          <TouchableOpacity
            onPress={onSend}
            activeOpacity={0.9}
            style={[styles.sendBtn, { opacity: text.trim() ? 1 : 0.6 }]}
            disabled={!text.trim()}
          >
            <MaterialCommunityIcons name="send" size={18} color="#062C30" />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </ThemedView>
  );
}

/* ---------------- Styles ---------------- */
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
  heroHi: { color: "#E8FEFF", fontSize: 20, fontWeight: "800", marginBottom: 4 },
  heroSub: { color: "rgba(232,254,255,0.85)", fontSize: 13, lineHeight: 18 },

  thinkWrapInline: {
    alignSelf: "stretch",
    borderRadius: 16,
    overflow: "hidden",
    borderWidth: 1,
    borderColor: c.stroke,
    backgroundColor: c.cardA,
  },
  thinkHeader: {
    paddingHorizontal: 14,
    paddingVertical: 12,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  thinkTitle: { color: c.ink, fontWeight: "800", fontSize: 13 },
  thinkBody: { paddingHorizontal: 14, paddingBottom: 12, gap: 8 },
  thinkRow: { flexDirection: "row", alignItems: "center" },
  thinkLine: { color: c.ink, fontSize: 13 },

  exampleWrap: { width: "100%", gap: 8, marginBottom: 6 },
  exampleCard: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    padding: 12,
    backgroundColor: c.cardA,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: c.stroke,
  },
  exampleIcon: {
    width: 26,
    height: 26,
    borderRadius: 8,
    backgroundColor: c.chip,
    borderWidth: 1,
    borderColor: c.chipStroke,
    alignItems: "center",
    justifyContent: "center",
  },
  exampleTitle: { color: c.ink, fontWeight: "800", fontSize: 13 },
  exampleHint: { color: c.mut, fontSize: 12, marginTop: 2 },

  bubble: {
    maxWidth: "86%",
    borderRadius: 16,
    padding: 12,
    borderWidth: 1,
  },
  bubbleUser: { backgroundColor: c.tealStrong, borderColor: c.tealStrong },
  bubbleAi: { backgroundColor: c.cardA, borderColor: c.stroke },
  bubbleText: { color: c.ink, fontSize: 14, lineHeight: 20 },

  aiBadge: {
    alignSelf: "flex-start",
    flexDirection: "row",
    gap: 6,
    marginBottom: 6,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 999,
    backgroundColor: c.teal,
  },
  aiBadgeText: { color: "#062C30", fontWeight: "800", fontSize: 11 },

  inputBar: {
    position: "absolute",
    left: 16,
    right: 16,
    bottom: 0,
    flexDirection: "row",
    alignItems: "flex-end",
    gap: 10,
    paddingTop: 10,
    backgroundColor: "transparent",
  },
  input: {
    flex: 1,
    minHeight: 42,
    maxHeight: 140,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: c.stroke,
    backgroundColor: c.cardB,
    color: c.ink,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
  },
  sendBtn: {
    paddingHorizontal: 14,
    paddingVertical: 12,
    borderRadius: 12,
    backgroundColor: c.tealStrong,
  },
});
