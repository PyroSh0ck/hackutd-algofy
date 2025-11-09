// app/subscriptions.tsx
import { useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  TouchableOpacity,
  View,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useRouter } from "expo-router";
import { ThemedView } from "@/components/themed-view";
import { ThemedText } from "@/components/themed-text";

type Sub = { id: string; name: string; price: number; email?: string };

const MOCK_SUBS: Sub[] = [
  { id: "1", name: "Spotify", price: 10.99, email: "support@spotify.com" },
  { id: "2", name: "Netflix", price: 15.49, email: "support@netflix.com" },
  { id: "3", name: "Notion", price: 8.0, email: "team@makenotion.com" },
  { id: "4", name: "Adobe", price: 19.99, email: "noreply@mail.adobe.com" },
];

const STEPS = ["DocGen Agent", "Response Agent", "Email Agent"] as const;
type Phase = "idle" | "loading" | "draft" | "sending" | "sent";

export default function SubscriptionsScreen() {
  const router = useRouter();
  const [selected, setSelected] = useState<Sub | null>(null);

  // Overlay states
  const [open, setOpen] = useState(false);
  const [phase, setPhase] = useState<Phase>("idle");
  const [stepIdx, setStepIdx] = useState(0);
  const [draft, setDraft] = useState("");

  // manage timers so we can clean up
  const timers = useRef<ReturnType<typeof setTimeout>[]>([]);
  const clearTimers = () => {
    timers.current.forEach(clearTimeout);
    timers.current = [];
  };
  useEffect(() => clearTimers, []); // cleanup on unmount

  const draftEmail = (s: Sub) => {
    const to = s.email ?? `support@${s.name.toLowerCase()}.com`;
    const body =
      `To: ${to}\n` +
      `Subject: Request to Cancel Subscription - ${s.name}\n\n` +
      `Hello ${s.name} Support,\n\n` +
      `Please cancel my subscription effective immediately and confirm any remaining billing details. ` +
      `Associated account email: <your-email-here>.\n\n` +
      `Thank you,\n` +
      `<Your Name>`;
    setDraft(body);
  };

  const runLoadingSequence = () => {
    setPhase("loading");
    setStepIdx(0);

    // advance 1 step per second
    STEPS.forEach((_, i) => {
      const t = setTimeout(() => {
        setStepIdx(i);
        if (i === STEPS.length - 1) {
          // after last step finishes, show draft
          const t2 = setTimeout(() => {
            if (selected) draftEmail(selected);
            setPhase("draft");
          }, 300); // a tiny pause feels nicer
          timers.current.push(t2);
        }
      }, 1000 * i);
      timers.current.push(t);
    });
  };

  const onCancelPress = () => {
    if (!selected) return;
    setOpen(true);
    clearTimers();
    runLoadingSequence();
  };

  const confirmSend = (yes: boolean) => {
    if (!yes) {
      setOpen(false);
      setPhase("idle");
      setDraft("");
      clearTimers();
      return;
    }
    setPhase("sending");
    const t = setTimeout(() => {
      setPhase("sent");
    }, 2000);
    timers.current.push(t);
  };

  return (
    <ThemedView style={{ flex: 1 }}>
      {/* Header card */}
      <LinearGradient
        colors={["#3a9eba", "#0f4959"]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        style={{
          margin: 16,
          borderRadius: 20,
          borderWidth: 3,
          borderColor: "rgba(24,55,68,0.2)",
          padding: 16,
        }}
      >
        <ThemedText
          style={{
            fontFamily: "Poppins_600SemiBold",
            fontSize: 18,
            marginBottom: 6,
            color: "#ffffff",
          }}
        >
          Subscriptions
        </ThemedText>
        <ThemedText style={{ fontSize: 12, opacity: 0.9 }}>
          Select a subscription to cancel. We’ll draft an email for you to
          review.
        </ThemedText>
      </LinearGradient>

      {/* List */}
      <FlatList
        data={MOCK_SUBS}
        keyExtractor={(i) => i.id}
        contentContainerStyle={{
          paddingHorizontal: 16,
          paddingBottom: 24,
          gap: 12,
        }}
        renderItem={({ item }) => {
          const active = selected?.id === item.id;
          return (
            <TouchableOpacity
              onPress={() => setSelected(item)}
              activeOpacity={0.9}
            >
              <ThemedView
                style={{
                  padding: 16,
                  borderRadius: 16,
                  borderWidth: 1,
                  borderColor: active ? "#62b2c4" : "rgba(24,55,68,0.2)",
                  backgroundColor: "rgba(16, 23, 28, 0.5)",
                }}
              >
                <ThemedText
                  style={{ fontFamily: "Poppins_600SemiBold", fontSize: 16 }}
                >
                  {item.name}
                </ThemedText>
                <ThemedText
                  style={{ marginTop: 4, fontSize: 12, opacity: 0.8 }}
                >
                  ${item.price.toFixed(2)}/mo
                </ThemedText>
              </ThemedView>
            </TouchableOpacity>
          );
        }}
      />

      {/* Actions */}
      <View style={{ paddingHorizontal: 16, paddingBottom: 24, gap: 12 }}>
        <TouchableOpacity
          onPress={onCancelPress}
          disabled={!selected}
          style={{
            opacity: selected ? 1 : 0.5,
            backgroundColor: "#3c8ca2",
            borderColor: "#62b2c4",
            borderWidth: 1,
            paddingVertical: 14,
            borderRadius: 14,
            alignItems: "center",
          }}
        >
          <ThemedText style={{ fontFamily: "Poppins_600SemiBold" }}>
            Draft cancellation email
          </ThemedText>
        </TouchableOpacity>

        <TouchableOpacity
          onPress={() => router.back()}
          style={{
            backgroundColor: "transparent",
            borderColor: "rgba(24,55,68,0.35)",
            borderWidth: 1,
            paddingVertical: 12,
            borderRadius: 14,
            alignItems: "center",
          }}
        >
          <ThemedText>Back</ThemedText>
        </TouchableOpacity>
      </View>

      {/* ---------- FULL-SCREEN OVERLAY (prevents any overlap) ---------- */}
      {open && (
        <ThemedView
          style={{
            position: "absolute",
            inset: 0,
            backgroundColor: "rgba(0,0,0,0.45)",
            justifyContent: "center",
            alignItems: "center",
            padding: 16,
            zIndex: 999,
          }}
          pointerEvents="auto"
        >
          <ThemedView
            style={{
              width: "100%",
              maxWidth: 560,
              borderRadius: 18,
              borderWidth: 1,
              borderColor: "rgba(24,55,68,0.35)",
              backgroundColor: "rgba(16,23,28,0.95)",
              padding: 16,
            }}
          >
            {/* Loading sequence */}
            {phase === "loading" && (
              <View>
                <ThemedText
                  style={{
                    fontFamily: "Poppins_600SemiBold",
                    marginBottom: 10,
                  }}
                >
                  Generating Draft…
                </ThemedText>

                {STEPS.map((label, i) => {
                  const isActive = i === stepIdx;
                  const isDone = i < stepIdx;
                  return (
                    <View
                      key={label}
                      style={{
                        flexDirection: "row",
                        alignItems: "center",
                        paddingVertical: 8,
                        gap: 10,
                        borderBottomWidth: i === STEPS.length - 1 ? 0 : 1,
                        borderBottomColor: "rgba(24,55,68,0.2)",
                      }}
                    >
                      <View
                        style={{
                          height: 22,
                          width: 22,
                          borderRadius: 11,
                          borderWidth: 1,
                          borderColor:
                            isDone || isActive
                              ? "#62b2c4"
                              : "rgba(24,55,68,0.5)",
                          alignItems: "center",
                          justifyContent: "center",
                          backgroundColor: isDone ? "#3c8ca2" : "transparent",
                        }}
                      >
                        {isActive ? (
                          <ActivityIndicator size="small" />
                        ) : isDone ? (
                          <ThemedText style={{ fontSize: 12 }}>✓</ThemedText>
                        ) : null}
                      </View>
                      <ThemedText
                        style={{ opacity: isDone || isActive ? 1 : 0.7 }}
                      >
                        {label}
                      </ThemedText>
                    </View>
                  );
                })}
              </View>
            )}

            {/* Draft view */}
            {phase === "draft" && (
              <View>
                <ThemedText
                  style={{ fontFamily: "Poppins_600SemiBold", marginBottom: 8 }}
                >
                  Drafted Email
                </ThemedText>
                <ThemedText
                  style={{
                    fontSize: 12,
                    lineHeight: 18,
                    backgroundColor: "rgba(0,0,0,0.15)",
                    padding: 12,
                    borderRadius: 10,
                  }}
                >
                  {draft}
                </ThemedText>

                <View style={{ flexDirection: "row", gap: 10, marginTop: 12 }}>
                  <TouchableOpacity
                    onPress={() => confirmSend(true)}
                    style={{
                      flex: 1,
                      backgroundColor: "#3c8ca2",
                      borderColor: "#62b2c4",
                      borderWidth: 1,
                      paddingVertical: 12,
                      borderRadius: 12,
                      alignItems: "center",
                    }}
                  >
                    <ThemedText style={{ fontFamily: "Poppins_600SemiBold" }}>
                      Yes, send
                    </ThemedText>
                  </TouchableOpacity>
                  <TouchableOpacity
                    onPress={() => confirmSend(false)}
                    style={{
                      flex: 1,
                      backgroundColor: "transparent",
                      borderColor: "rgba(24,55,68,0.35)",
                      borderWidth: 1,
                      paddingVertical: 12,
                      borderRadius: 12,
                      alignItems: "center",
                    }}
                  >
                    <ThemedText>No</ThemedText>
                  </TouchableOpacity>
                </View>
              </View>
            )}

            {/* Sending state */}
            {phase === "sending" && (
              <View style={{ alignItems: "center", gap: 12 }}>
                <ActivityIndicator />
                <ThemedText>Sending email…</ThemedText>
              </View>
            )}

            {/* Sent state */}
            {phase === "sent" && (
              <View style={{ gap: 10 }}>
                <ThemedText style={{ color: "#62b2c4" }}>
                  Email sent ✅
                </ThemedText>
                <TouchableOpacity
                  onPress={() => {
                    setOpen(false);
                    setPhase("idle");
                    setDraft("");
                  }}
                  style={{
                    alignSelf: "flex-start",
                    marginTop: 6,
                    backgroundColor: "transparent",
                    borderColor: "rgba(24,55,68,0.35)",
                    borderWidth: 1,
                    paddingVertical: 10,
                    paddingHorizontal: 14,
                    borderRadius: 10,
                  }}
                >
                  <ThemedText>Close</ThemedText>
                </TouchableOpacity>
              </View>
            )}
          </ThemedView>
        </ThemedView>
      )}
    </ThemedView>
  );
}
