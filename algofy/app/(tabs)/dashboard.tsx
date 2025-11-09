import { useMemo, useState } from "react";
import { StyleSheet, ScrollView, Image, View, TouchableOpacity } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { MaterialCommunityIcons } from "@expo/vector-icons";

import { ThemedView } from "@/components/themed-view";
import { ThemedText } from "@/components/themed-text";
import { Box } from "@/components/ui/box";
import { IconBoxList } from "@/components/ui/iconboxlist";
import { CarouselComp } from "@/components/ui/carousel";

/* ---- Palette to match your theme ---- */
const C = {
  teal: "#abebe3",
  tealSoft: "rgba(171,235,227,0.16)",
  text: "#EAFBFC",
  textSoft: "rgba(234,251,252,0.7)",
  line: "rgba(255,255,255,0.08)",
  chipStroke: "rgba(171,235,227,0.35)",
  green: "#7DFF9E",
  red: "#FF8181",
  rowBg: "#121618",
  iconBg: "#1b2629",
};

type TxType = "Payment" | "Transfer";
type TxStatus = "Success" | "Failed";

type Tx = {
  id: string;
  name: string;
  date: string; // ISO or display
  type: TxType;
  status: TxStatus;
  icon: keyof typeof MaterialCommunityIcons.glyphMap; // material-community name
};

/* ---- Demo transactions ---- */
const TX_DATA: Tx[] = [
  { id: "t1", name: "Fauget Cafe", date: "2024-05-04", type: "Payment", status: "Success", icon: "coffee" },
  { id: "t2", name: "Larana, Inc.", date: "2024-05-03", type: "Payment", status: "Success", icon: "coffee" },
  { id: "t3", name: "Claudia Alves", date: "2024-05-02", type: "Transfer", status: "Failed", icon: "account" },
  { id: "t4", name: "Borcell e Cafe", date: "2024-05-01", type: "Payment", status: "Success", icon: "coffee" },
  { id: "t5", name: "Avery Clinic", date: "2024-05-01", type: "Transfer", status: "Success", icon: "hospital-building" },
  { id: "t6", name: "Metro Grocers", date: "2024-04-30", type: "Payment", status: "Success", icon: "cart" },
  { id: "t7", name: "Ravi Kumar", date: "2024-04-28", type: "Transfer", status: "Success", icon: "account-arrow-right" },
  { id: "t8", name: "Streamify", date: "2024-04-27", type: "Payment", status: "Success", icon: "play-circle" },
  { id: "t9", name: "Lift Share", date: "2024-04-27", type: "Payment", status: "Success", icon: "car" },
  { id: "t10", name: "Jenna Park", date: "2024-04-26", type: "Transfer", status: "Failed", icon: "account" },
  { id: "t11", name: "Sushi Place", date: "2024-04-25", type: "Payment", status: "Success", icon: "food" },
  { id: "t12", name: "GymPlus", date: "2024-04-24", type: "Payment", status: "Success", icon: "dumbbell" },
  { id: "t13", name: "Gail Rivera", date: "2024-04-23", type: "Transfer", status: "Success", icon: "account" },
];

const prettyDate = (iso: string) => {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { month: "long", day: "numeric", year: "numeric" });
};

export default function HomeScreen() {
  const [typeFilter, setTypeFilter] = useState<"All" | TxType>("All");
  const [sort, setSort] = useState<"Latest" | "Oldest">("Latest");

  const data = useMemo(() => {
    let arr = [...TX_DATA];
    if (typeFilter !== "All") arr = arr.filter((t) => t.type === typeFilter);
    arr.sort((a, b) =>
      sort === "Latest" ? +new Date(b.date) - +new Date(a.date) : +new Date(a.date) - +new Date(b.date)
    );
    return arr;
  }, [typeFilter, sort]);

  return (
    <ThemedView style={{ height: "100%" }}>
      <ScrollView contentContainerStyle={styles.mainContainer}>
        {/* Header */}
        <ThemedView style={styles.header}>
          <ThemedView>
            <ThemedText style={{ color: C.teal, fontSize: 15 }}>Welcome back</ThemedText>
            <ThemedText style={styles.headerName}>Parth Modi</ThemedText>
            <ThemedText style={{ color: C.teal, fontSize: 15 }}>parthmodi.amodi@gmail.com</ThemedText>
          </ThemedView>
          <Image source={require("@/assets/images/icon.png")} style={{ width: 80, height: 80 }} />
        </ThemedView>

        {/* Balance Card */}
        <ThemedView style={styles.box}>
          <Box />
        </ThemedView>

        {/* Quick Actions */}
        <ThemedView style={styles.iconboxlist}>
          <IconBoxList />
        </ThemedView>

        {/* Centered Carousel */}
        <ThemedView style={styles.carouselSection}>
          <View style={styles.carouselWrap}>
            <CarouselComp />
          </View>
        </ThemedView>

        {/* Goals */}
        <ThemedView style={styles.goalsContainer}>
          <ThemedView style={styles.goalLeft}>
            <LinearGradient colors={["#3a9eba", "#0f4959"]} style={styles.goalCard} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}>
              <ThemedView style={styles.circleTL} />
              <ThemedView style={styles.circleBR} />
              <ThemedText style={styles.goalTitle}>Savings Goals</ThemedText>
              <Image source={require("@/assets/images/pie.png")} style={{ width: "100%", height: "100%", flex: 1 }} />
            </LinearGradient>
          </ThemedView>

          <ThemedView style={styles.goalRight}>
            <LinearGradient colors={["#3a9eba", "#0f4959"]} style={styles.goalCard} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}>
              <ThemedView style={[styles.circleTL, { height: 80, width: 80, left: -25, top: -25 }]} />
              <ThemedView style={[styles.circleBR, { height: 100, width: 100, right: -25, bottom: -25 }]} />
              <ThemedText style={styles.goalTitle}>Spending Trends</ThemedText>
              <Image source={require("@/assets/images/chart.png")} style={{ width: "100%", height: "100%", flex: 1 }} />
            </LinearGradient>
          </ThemedView>
        </ThemedView>

        {/* Transactions */}
        <View style={{ width: "90%", marginTop: 28, height: 400 }}>
          {/* Toolbar */}
          <View style={styles.toolbar}>
            <TouchableOpacity
              style={styles.filterChip}
              activeOpacity={0.85}
              onPress={() =>
                setTypeFilter((prev) => (prev === "All" ? "Payment" : prev === "Payment" ? "Transfer" : "All"))
              }
            >
              <ThemedText style={styles.filterText}>
                {typeFilter === "All" ? "Transaction" : typeFilter}
              </ThemedText>
              <MaterialCommunityIcons name="chevron-down" size={16} color={C.teal} style={{ marginLeft: 4 }} />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.sortChip}
              activeOpacity={0.85}
              onPress={() => setSort((s) => (s === "Latest" ? "Oldest" : "Latest"))}
            >
              <ThemedText style={[styles.sortText, { marginRight: 4 }]}>Sort by {sort}</ThemedText>
              <MaterialCommunityIcons name="chevron-down" size={16} color={C.teal} />
            </TouchableOpacity>
          </View>

          {/* List */}
          <View style={styles.listWrap}>
            <ScrollView>
              {data.map((t, i) => (
                <View key={t.id}>
                  <View style={styles.row}>
                    <View style={styles.iconBlock}>
                      <MaterialCommunityIcons name={t.icon} size={20} color={C.teal} />
                    </View>

                    <View style={{ flex: 1 }}>
                      <ThemedText style={styles.name}>{t.name}</ThemedText>
                      <ThemedText style={styles.date}>{prettyDate(t.date)}</ThemedText>
                    </View>

                    <ThemedText style={styles.type}>{t.type}</ThemedText>
                    <ThemedText style={[styles.status, { color: t.status === "Success" ? C.green : C.red }]}>
                      {t.status}
                    </ThemedText>
                  </View>

                  {i !== data.length - 1 && <View style={styles.divider} />}
                </View>
              ))}
            </ScrollView>
          </View>
        </View>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  mainContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    paddingBottom: 30,
  },
  header: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    width: "100%",
    paddingTop: 100,
    paddingHorizontal: 20,
  },
  headerName: {
    color: C.teal,
    fontSize: 25,
    fontFamily: "Poppins_600SemiBold",
    paddingTop: 15,
    paddingBottom: 10,
    paddingLeft: 5,
  },
  iconboxlist: {},
  box: {
    marginTop: 30,
    borderRadius: 20,
    width: "90%",
    height: 230,
  },

  /* Centered carousel styles */
  carouselSection: {
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    marginTop: 25,
  },
  carouselWrap: {
    width: "90%",
    maxWidth: 480,
    alignSelf: "center",
    alignItems: "center",
    justifyContent: "center",
  },

  goalsContainer: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    height: 230,
    marginTop: 20,
  },
  goalLeft: {
    height: "80%",
    width: "40%",
    marginRight: 20,
    borderRadius: 20,
  },
  goalRight: {
    height: "80%",
    width: "40%",
    marginLeft: 20,
    borderRadius: 20,
  },
  goalCard: {
    borderWidth: 3,
    borderColor: "rgba(24, 55, 68, 0.2)",
    height: "100%",
    width: "100%",
    borderRadius: 20,
    padding: 10,
    display: "flex",
    flexDirection: "column",
    position: "relative",
    overflow: "hidden",
  },
  goalTitle: {
    color: "#ffffff",
    fontSize: 14,
    fontFamily: "Poppins_600SemiBold",
    marginBottom: 5,
    textAlign: "center",
  },
  circleTL: {
    height: 60,
    width: 60,
    borderRadius: 9999,
    backgroundColor: "rgba(211, 211, 211, 0.1)",
    position: "absolute",
    left: -15,
    top: -15,
  },
  circleBR: {
    height: 120,
    width: 120,
    borderRadius: 9999,
    backgroundColor: "rgba(211, 211, 211, 0.1)",
    position: "absolute",
    right: -20,
    bottom: -20,
  },

  /* Transactions */
  toolbar: {
    width: "100%",
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 6,
  },
  filterChip: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    paddingHorizontal: 14,
    borderRadius: 14,
    backgroundColor: C.tealSoft,
    borderWidth: 1,
    borderColor: C.chipStroke,
  },
  filterText: { color: C.teal, fontWeight: "700", fontSize: 13 },
  sortChip: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    paddingHorizontal: 14,
    borderRadius: 14,
    backgroundColor: C.tealSoft,
    borderWidth: 1,
    borderColor: C.chipStroke,
  },
  sortText: { color: C.teal, fontWeight: "700", fontSize: 13 },
  listWrap: {
    width: "100%",
    backgroundColor: C.rowBg,
    borderRadius: 18,
    borderWidth: 1,
    borderColor: C.line,
    overflow: "hidden",
    maxHeight: 400,
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 14,
    paddingHorizontal: 12,
  },
  iconBlock: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: C.iconBg,
    marginRight: 12,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: C.line,
  },
  name: { color: C.text, fontWeight: "800", fontSize: 15 },
  date: { color: C.textSoft, fontSize: 12, marginTop: 2 },
  type: { color: C.textSoft, fontSize: 13, marginRight: 12 },
  status: { fontWeight: "800", fontSize: 13 },
  divider: { height: 1, backgroundColor: C.line, marginLeft: 60 },
});
