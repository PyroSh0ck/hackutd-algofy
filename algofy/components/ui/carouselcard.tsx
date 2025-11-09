// components/carouselcard.tsx
import { LinearGradient } from "expo-linear-gradient";
import { TouchableOpacity } from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { ThemedView } from "../themed-view";
import { ThemedText } from "../themed-text";

type Props = { onPress?: () => void };

export function CarouselCard({ onPress }: Props) {
  const Card = (
    <ThemedView>
      <LinearGradient
        colors={["#3a9eba", "#0f4959"]}
        style={{
          height: "100%",
          width: "100%",
          borderRadius: 20,
          borderColor: "rgba(24, 55, 68, 0.2)",
          borderWidth: 3,
          position: "relative",
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
      >
        {/* Accents */}
        <ThemedView
          style={{
            height: 100,
            width: 100,
            borderRadius: 9999,
            backgroundColor: "rgba(211, 211, 211, 0.1)",
            position: "absolute",
            right: -25,
            top: -25,
          }}
        />
        <ThemedView
          style={{
            height: 200,
            width: 200,
            borderRadius: 9999,
            backgroundColor: "rgba(211, 211, 211, 0.1)",
            position: "absolute",
            left: -30,
            bottom: -30,
          }}
        />

        {/* Badge */}
        <ThemedView
          style={{
            borderWidth: 1,
            height: 40,
            width: 40,
            borderRadius: 10,
            marginTop: 20,
            marginLeft: 20,
            marginBottom: 15,
            backgroundColor: "#3c8ca2",
            borderColor: "#62b2c4",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <MaterialCommunityIcons name="email-outline" size={20} color="#ffffff" />
        </ThemedView>

        <ThemedText
          style={{
            fontFamily: "Poppins_600SemiBold",
            marginLeft: 20,
            fontSize: 20,
            color: "#ffffff",
          }}
        >
          Watch your budget!
        </ThemedText>

        {/* Message */}
        <ThemedView
          style={{
            marginHorizontal: 20,
            marginTop: 10,
            flexDirection: "row",
            flexWrap: "wrap",
            alignItems: "center",
            backgroundColor: "transparent",
          }}
        >
          <ThemedText style={{ fontSize: 12, lineHeight: 18, color: "#EAFBFC" }}>
            You spent over $100 in the last 3 weeks on subscriptions. Do you want to cancel one?
          </ThemedText>
        </ThemedView>
      </LinearGradient>
    </ThemedView>
  );

  if (onPress) {
    return (
      <TouchableOpacity activeOpacity={0.9} onPress={onPress}>
        {Card}
      </TouchableOpacity>
    );
  }
  return Card;
}
