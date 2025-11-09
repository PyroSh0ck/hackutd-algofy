import { Stack } from "expo-router";

export default function StackLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="stuff"
        options={{
          headerShown: false,
        }}
      />
      <Stack.Screen name="assist" options={{headerShown: false}} />
    </Stack>
  );
}