import { Stack } from "expo-router";

export default function ModalLayout() {
    return (
        <Stack>
            <Stack.Screen name="recommendations" options={{ presentation: 'modal', title: 'recommendations', headerShown: false }} />
        </Stack>
    )
}