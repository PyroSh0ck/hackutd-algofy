// components/carousel.tsx
import * as React from "react";
import { Dimensions, TouchableOpacity, StyleSheet } from "react-native";
import { useSharedValue } from "react-native-reanimated";
import Carousel, { ICarouselInstance } from "react-native-reanimated-carousel";
import { useRouter } from "expo-router";
import { ThemedView } from "../themed-view";
import { IconSymbol } from "./icon-symbol";
import { CarouselCard } from "./carouselcard";

const data = [...new Array(6).keys()];
const width = Dimensions.get("window").width;

export function CarouselComp() {
  const ref = React.useRef<ICarouselInstance>(null);
  const progress = useSharedValue<number>(0);
  const router = useRouter();

  return (
    <ThemedView style={styles.mainContainer}>
      <Carousel
        ref={ref}
        width={width}
        height={width / 2}
        data={data}
        onProgressChange={progress}
        renderItem={() => (
          <ThemedView style={styles.renderedItem}>
            <TouchableOpacity activeOpacity={0.9} onPress={() => router.push("/(stack)/subscriptions")}>
              <CarouselCard />
            </TouchableOpacity>
          </ThemedView>
        )}
      />

      <TouchableOpacity style={styles.arrowleft} onPress={() => ref.current?.prev({ animated: true })}>
        <IconSymbol size={28} name="chevron.left" color="white" />
      </TouchableOpacity>
      <TouchableOpacity style={styles.arrowright} onPress={() => ref.current?.next({ animated: true })}>
        <IconSymbol size={28} name="chevron.right" color="white" />
      </TouchableOpacity>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  mainContainer: { flex: 1, position: "relative" },
  arrowleft: { position: "absolute", left: 0, top: "12%", marginLeft: 20 },
  arrowright: { position: "absolute", right: 0, top: "12%", marginRight: 20 },
  renderedItem: {
    height: "90%",
    width: "70%",
    alignSelf: "center",
    borderWidth: 1,
    justifyContent: "center",
    backgroundColor: "transparent",
    borderRadius: 20,
    borderColor: "rgba(24, 55, 68, 0.2)",
  },
});