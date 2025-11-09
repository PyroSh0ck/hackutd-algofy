import { Stack } from "expo-router";

export default function SignupLayout() {
    return (
        <Stack>
            <Stack.Screen name="initial" options={{ headerShown: false }} />
            <Stack.Screen name="password" options={{ headerShown: false }} />
            <Stack.Screen name="identification" options={{ headerShown: false }} />
            <Stack.Screen name="identification2" options={{ headerShown: false }} />
            <Stack.Screen name="help" options={{ headerShown: false }} />
            <Stack.Screen name="goals" options={{ headerShown: false }} />
            <Stack.Screen name="congratulations" options={{ headerShown: false }} />
        </Stack>
    )
}
