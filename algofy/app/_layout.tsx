import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';
import * as SplashScreen from 'expo-splash-screen';
import { Poppins_400Regular, Poppins_600SemiBold, Poppins_500Medium, Poppins_300Light, useFonts } from '@expo-google-fonts/poppins';
import { useEffect } from 'react';

import { useColorScheme } from '@/hooks/use-color-scheme';

SplashScreen.preventAutoHideAsync()

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded, error] = useFonts({
    Poppins_400Regular,
    Poppins_600SemiBold,
    Poppins_500Medium,
    Poppins_300Light,
  });

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [loaded, error])

  if (!loaded && !error) {
    return null;
  }

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: '#151718',
          },
          headerTintColor: '#abebe3',
          headerTitleStyle: {
            fontFamily: 'Poppins_600SemiBold',
            fontSize: 20,
            color: '#abebe3',
          },
          headerShadowVisible: false,
          headerBackTitle: 'Back',
        }}
      >
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="(signup)" options={{ headerShown: false }} />
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="(modals)" options={{ headerShown: false }} />
        <Stack.Screen
          name="(stack)"
          options={{
            title: 'Investments',
            headerShown: true,
          }}
        />
      </Stack>
      <StatusBar style="light" />
    </ThemeProvider>
  );
}
