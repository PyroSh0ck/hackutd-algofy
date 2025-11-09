import { Link } from "expo-router";
import { StyleSheet, ScrollView, TouchableOpacity, View } from "react-native";
import { LinearGradient } from "expo-linear-gradient";

import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";

export default function ModalScreen() {

  const overspendingStats = {
    totalOverspent: 450,
    categoryBreakdown: [
      { category: "Dining Out", budgeted: 300, spent: 485, overspent: 185 },
      { category: "Entertainment", budgeted: 150, spent: 245, overspent: 95, newBudget: 100 },
      { category: "Shopping", budgeted: 200, spent: 370, overspent: 170, newBudget: 150 },
    ],
    monthlyBudget: 2000,
    totalSpent: 2450,
    // After reallocation: Entertainment reduced by $50, Shopping reduced by $50
    // This frees up $100 to help offset the overspending
  };

  const handleReallocate = () => {
    console.log("Reallocating budget...");
  };

  return (
    <ThemedView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <ThemedView style={styles.header}>
          <ThemedText style={styles.title}>Budget Reallocation</ThemedText>
          <ThemedView style={styles.underline} />
        </ThemedView>

        {/* Overspending Summary */}
        <LinearGradient
          colors={["#ff6b6b", "#e63946"]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.mainCard}
        >
          <View style={styles.cardInner}>
            <ThemedText style={styles.cardLabel}>Total Overspending</ThemedText>
            <ThemedText style={styles.mainAmount}>
              ${overspendingStats.totalOverspent}
            </ThemedText>
            <View style={styles.budgetRow}>
              <ThemedText style={styles.budgetText}>
                Budget: ${overspendingStats.monthlyBudget}
              </ThemedText>
              <ThemedText style={styles.budgetText}>
                Spent: ${overspendingStats.totalSpent}
              </ThemedText>
            </View>
          </View>
        </LinearGradient>

        {/* Category Breakdown */}
        <ThemedView style={styles.section}>
          <ThemedView style={styles.sectionHeader}>
            <ThemedText style={styles.sectionTitle}>
              Category Breakdown
            </ThemedText>
            <ThemedView style={styles.underline} />
          </ThemedView>

          {overspendingStats.categoryBreakdown.map((item, i) => {
            const activeBudget = item.newBudget ?? item.budgeted;
            const pct = (item.spent / activeBudget) * 100;
            const greenPct = Math.min(pct, 100);
            const redPct =
              item.spent > activeBudget ? Math.min(((item.spent / activeBudget) - 1) * 100, 100) : 0;

            // Determine gradient colors based on category type
            const isOverspending = item.category === "Dining Out";

            return (
              <LinearGradient
                key={`${item.category}-${i}`}
                colors={isOverspending ? ["#e74c3c", "#c0392b"] : ["#3a9eba", "#0f4959"]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={styles.categoryCard}
              >
                <View style={styles.categoryInner}>
                  <View style={styles.categoryHeader}>
                    <ThemedText style={styles.categoryName}>{item.category}</ThemedText>
                    <View
                      style={[
                        item.overspent > 0 ? styles.overspentPill : styles.savedPill,
                        {
                          backgroundColor:
                            item.overspent > 0
                              ? "rgba(231, 76, 60, 0.3)"
                              : "rgba(46, 204, 113, 0.3)",
                        },
                      ]}
                    >
                      <ThemedText style={styles.overspentText}>+${item.overspent}</ThemedText>
                    </View>
                  </View>

                  <View style={styles.categoryStats}>
                    <View style={styles.statItem}>
                      <ThemedText style={styles.statLabel}>Budgeted</ThemedText>
                      {item.newBudget ? (
                        <View style={{ flexDirection: "row", alignItems: "center", gap: 4 }}>
                          <ThemedText
                            style={[
                              styles.statValue,
                              { textDecorationLine: "line-through", opacity: 0.5, fontSize: 13 },
                            ]}
                          >
                            ${item.budgeted}
                          </ThemedText>
                          <ThemedText style={[styles.statValue, { color: "#2ecc71" }]}>
                            ${item.newBudget}
                          </ThemedText>
                        </View>
                      ) : (
                        <ThemedText style={styles.statValue}>${item.budgeted}</ThemedText>
                      )}
                    </View>
                    <View style={styles.statItem}>
                      <ThemedText style={styles.statLabel}>Spent</ThemedText>
                      <ThemedText style={styles.statValue}>${item.spent}</ThemedText>
                    </View>
                  </View>

                  {/* Progress Bar */}
                  <ThemedView style={styles.progressTrack}>
                    {/* green fill up to budget */}
                    <View
                      style={[
                        styles.progressFillGreen,
                        { width: `${greenPct}%`, backgroundColor: "#4ade80" },
                      ]}
                    />
                    {/* red fill beyond budget */}
                    {redPct > 0 && (
                      <View
                        style={[
                          styles.progressFillRed,
                          { width: `${redPct}%`, backgroundColor: "#ef4444" },
                        ]}
                      />
                    )}
                    <View style={styles.budgetMarker} />
                  </ThemedView>
                </View>
              </LinearGradient>
            );
          })}
        </ThemedView>

        {/* Reallocate Button */}
        <TouchableOpacity onPress={handleReallocate} activeOpacity={0.8}>
          <LinearGradient
            colors={["#2ecc71", "#27ae60"]}
            style={styles.reallocateButton}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
          >
            <ThemedText style={styles.buttonText}>Reallocate Budget</ThemedText>
          </LinearGradient>
        </TouchableOpacity>

        {/* Back Link */}
        <Link href="/(tabs)/dashboard" dismissTo style={styles.backLink}>
          <ThemedText style={styles.backLinkText}>Back to Dashboard</ThemedText>
        </Link>
      </ScrollView>
    </ThemedView>
  );
}

/* ---------- STYLES ---------- */
const shadow = {
  shadowColor: "#000",
  shadowOpacity: 0.1,
  shadowRadius: 4,
  shadowOffset: { width: 0, height: 2 },
  elevation: 2,
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#151718", paddingTop: 80 },
  scrollContent: { padding: 20, paddingBottom: 32, gap: 16 },

  header: {
    marginBottom: 10,
  },
  title: {
    fontSize: 28,
    lineHeight: 32,
    fontFamily: "Poppins_600SemiBold",
    color: "#abebe3",
    marginBottom: 8,
    
  },
  underline: {
    height: 2,
    backgroundColor: "#abebe3",
    opacity: 0.3,
  },
  subtitle: { fontSize: 15, color: "#abebe3", opacity: 0.75 },

  mainCard: { borderRadius: 16, ...shadow },
  cardInner: {
    backgroundColor: "rgba(6, 14, 18, 0.55)",
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.08)",
    alignItems: "center",
  },
  cardLabel: { fontSize: 13, color: "#ffffff", opacity: 0.9, marginBottom: 6 },
  mainAmount: {
    fontSize: 42,
    lineHeight: 50,
    fontFamily: "Poppins_600SemiBold",
    color: "#ffffff",
    marginBottom: 10,
  },
  budgetRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: 10,
    paddingTop: 10,
    borderTopWidth: 0.5,
    borderTopColor: "rgba(255, 255, 255, 0.18)",
  },
  budgetText: { fontSize: 12, color: "#ffffff", opacity: 0.8 },

  section: { gap: 12 },
  sectionHeader: {
    marginBottom: 8,
  },
  sectionTitle: {
    fontSize: 20,
    fontFamily: "Poppins_600SemiBold",
    color: "#abebe3",
    marginBottom: 6,
  },

  categoryCard: { borderRadius: 14, ...shadow },
  categoryInner: {
    backgroundColor: "rgba(5, 18, 23, 0.5)",
    borderRadius: 12,
    padding: 12,
    gap: 8,
    borderWidth: 1,
    borderColor: "rgba(24, 55, 68, 0.25)",
  },
  categoryHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  categoryName: {
    fontSize: 15,
    fontFamily: "Poppins_600SemiBold",
    color: "#ffffff",
  },
  overspentPill: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 999,
  },
  overspentText: { fontSize: 12, fontFamily: "Poppins_600SemiBold" },
  savedPill: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 999 },
  savedText: { fontSize: 12, fontFamily: "Poppins_600SemiBold" },

  categoryStats: {
    flexDirection: "row",
    justifyContent: "space-around",
    paddingVertical: 4,
  },
  statItem: { alignItems: "center" },
  statLabel: { fontSize: 11, color: "#ffffff", opacity: 0.7, marginBottom: 2 },
  statValue: {
    fontSize: 14,
    fontFamily: "Poppins_600SemiBold",
    color: "#ffffff",
  },

  progressTrack: {
    height: 8,
    borderRadius: 999,
    backgroundColor: "rgba(255,255,255,0.12)",
    overflow: "hidden",
    borderWidth: 0.5,
    borderColor: "rgba(255,255,255,0.15)",
    position: "relative",
  },
  progressFillGreen: {
    position: "absolute",
    left: 0,
    top: 0,
    bottom: 0,
    borderRadius: 999,
  },
  progressFillRed: {
    position: "absolute",
    left: "100%",
    top: 0,
    bottom: 0,
    borderRadius: 999,
  },
  budgetMarker: {
    position: "absolute",
    left: "100%",
    top: -1,
    bottom: -1,
    width: 2,
    backgroundColor: "rgba(255,255,255,0.7)",
  },

  reallocateButton: {
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
    ...shadow,
    borderWidth: 1,
    borderColor: "rgba(46, 204, 113, 0.25)",
  },
  buttonText: {
    fontSize: 15,
    fontFamily: "Poppins_600SemiBold",
    color: "#ffffff",
  },
  backLink: { alignItems: "center", paddingVertical: 8 },
  backLinkText: { fontSize: 15, color: "#abebe3", opacity: 0.7 },
});
