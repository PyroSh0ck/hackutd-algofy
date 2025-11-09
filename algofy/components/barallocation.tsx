// components/BarAllocation.tsx
import React from "react";
import { View, StyleSheet, ViewStyle } from "react-native";

type Slice = { name: string; value: number; color: string };
export default function BarAllocation({
  data,
  height = 160,        // <- make it visible by default
  radius = 14,
  style,
}: {
  data: Slice[];
  height?: number;
  radius?: number;
  style?: ViewStyle;
}) {
  const total = Math.max(
    1,
    data.reduce((s, d) => s + (d.value ?? 0), 0)
  );

  return (
    <View
      style={[
        styles.track,
        { height, borderRadius: radius },
        style,
      ]}
    >
      {data.map((d, i) => {
        const flex = (d.value ?? 0) / total || 0;
        const leftRadius = i === 0 ? radius : 0;
        const rightRadius = i === data.length - 1 ? radius : 0;

        return (
          <View
            key={d.name}
            style={{
              flex,
              backgroundColor: d.color,
              borderTopLeftRadius: leftRadius,
              borderBottomLeftRadius: leftRadius,
              borderTopRightRadius: rightRadius,
              borderBottomRightRadius: rightRadius,
            }}
          />
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  track: {
    width: "100%",
    overflow: "hidden",
    backgroundColor: "rgba(255,255,255,0.06)",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.10)",
  },
});