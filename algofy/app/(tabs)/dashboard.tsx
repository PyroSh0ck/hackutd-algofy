import { StyleSheet, ScrollView, Image } from "react-native";

import { ThemedView } from "@/components/themed-view";
import { Box } from "@/components/ui/box";
import { IconBoxList } from "@/components/ui/iconboxlist";
import { CarouselComp } from "@/components/ui/carousel";
import { ThemedText } from "@/components/themed-text";
import { LinearGradient } from "expo-linear-gradient";
import { PieChart } from "react-native-chart-kit";

const data = [
  {
    name: "Seoul",
    population: 21500000,
    color: "rgba(131, 167, 234, 1)",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15,
  },
  {
    name: "Toronto",
    population: 2800000,
    color: "#F00",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15,
  },
  {
    name: "Beijing",
    population: 527612,
    color: "red",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15,
  },
  {
    name: "New York",
    population: 8538000,
    color: "#ffffff",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15,
  },
  {
    name: "Moscow",
    population: 11920000,
    color: "rgb(0, 0, 255)",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15,
  },
];

const chartConfig = {
  backgroundColor: "#e26a00",
  backgroundGradientFrom: "#fb8c00",
  backgroundGradientTo: "#ffa726",
  decimalPlaces: 2, // optional, defaults to 2dp
  color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
  labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
  style: {
    borderRadius: 16,
  },
  propsForDots: {
    r: "6",
    strokeWidth: "2",
    stroke: "#ffa726",
  },
};

export default function HomeScreen() {
  return (
    <ThemedView style={{ height: "100%" }}>
      <ScrollView contentContainerStyle={styles.mainContainer}>
        <ThemedView
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            justifyContent: "space-between",
            width: "100%",
            paddingTop: 100,
            paddingHorizontal: 20,
          }}
        >
          <ThemedView>
            <ThemedText style={{ color: "#abebe3", fontSize: 15 }}>
              Welcome back
            </ThemedText>
            <ThemedText
              style={{
                color: "#abebe3",
                fontSize: 25,
                fontFamily: "Poppins_600SemiBold",
                paddingTop: 15,
                paddingBottom: 10,
                paddingLeft: 5,
              }}
            >
              Parth Modi
            </ThemedText>
            <ThemedText style={{ color: "#abebe3", fontSize: 15 }}>
              parthmodi.amodi@gmail.com
            </ThemedText>
          </ThemedView>
          <Image
            source={require("@/assets/images/icon.png")}
            style={{ width: 80, height: 80 }}
          />
        </ThemedView>
        <ThemedView style={styles.box}>
          <Box />
        </ThemedView>
        <ThemedView style={styles.iconboxlist}>
          <IconBoxList />
        </ThemedView>
        <ThemedView
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
            height: 230,
          }}
        >
          <ThemedView
            style={{
              height: "80%",
              width: "40%",
              marginRight: 20,
              borderRadius: 20,
            }}
          >
            <LinearGradient
              colors={["#3a9eba", "#0f4959"]}
              style={{
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
              }}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
            >
              {/* Top Left Circle */}
              <ThemedView
                style={{
                  height: 60,
                  width: 60,
                  borderRadius: 9999,
                  backgroundColor: "rgba(211, 211, 211, 0.1)",
                  position: "absolute",
                  left: -15,
                  top: -15,
                }}
              />
              {/* Bottom Right Circle */}
              <ThemedView
                style={{
                  height: 120,
                  width: 120,
                  borderRadius: 9999,
                  backgroundColor: "rgba(211, 211, 211, 0.1)",
                  position: "absolute",
                  right: -20,
                  bottom: -20,
                }}
              />
              <ThemedText
                style={{
                  color: "#ffffff",
                  fontSize: 14,
                  fontFamily: "Poppins_600SemiBold",
                  marginBottom: 5,
                  textAlign: "center",
                }}
              >
                Savings Goals
              </ThemedText>
              <Image
                source={require("@/assets/images/pie.png")}
                style={{ width: "100%", height: "100%", flex: 1 }}
              />
            </LinearGradient>
          </ThemedView>
          <ThemedView
            style={{
              height: "80%",
              width: "40%",
              marginLeft: 20,
              borderRadius: 20,
            }}
          >
            <LinearGradient
              colors={["#3a9eba", "#0f4959"]}
              style={{
                borderWidth: 3,
                borderColor: "rgba(24, 55, 68, 0.2)",
                height: "100%",
                width: "100%",
                borderRadius: 20,
                position: "relative",
                overflow: "hidden",
              }}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
            >
              {/* Top Left Circle */}
              <ThemedView
                style={{
                  height: 80,
                  width: 80,
                  borderRadius: 9999,
                  backgroundColor: "rgba(211, 211, 211, 0.1)",
                  position: "absolute",
                  left: -25,
                  top: -25,
                }}
              />
              {/* Bottom Right Circle */}
              <ThemedView
                style={{
                  height: 100,
                  width: 100,
                  borderRadius: 9999,
                  backgroundColor: "rgba(211, 211, 211, 0.1)",
                  position: "absolute",
                  right: -25,
                  bottom: -25,
                }}
              />
            </LinearGradient>
          </ThemedView>
        </ThemedView>
        <ThemedView>
          <CarouselComp />
        </ThemedView>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  iconboxlist: {},
  mainContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    paddingBottom: 30,
  },
  box: {
    marginTop: 30,
    borderRadius: 20,
    width: "90%",
    height: 230,
  },
});
