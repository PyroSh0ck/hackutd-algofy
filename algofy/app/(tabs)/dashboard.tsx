import { Image } from 'expo-image';
import { Platform, StyleSheet, ScrollView } from 'react-native';

import { HelloWave } from '@/components/hello-wave';
import ParallaxScrollView from '@/components/parallax-scroll-view';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Link } from 'expo-router';
import { Box } from '@/components/ui/box';
import { IconBoxList } from '@/components/ui/iconboxlist';
import { CarouselComp } from '@/components/ui/carousel';

export default function HomeScreen() {
  return (
    <ScrollView contentContainerStyle={styles.mainContainer}>
      <ThemedView style={styles.box}>
        <Box />
      </ThemedView>
      <ThemedView style={styles.iconboxlist}>
        <IconBoxList />
      </ThemedView>
      <ThemedView>
        <CarouselComp />
      </ThemedView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  iconboxlist: {
    
  },
  mainContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  box: {
    marginTop: 100,
    borderColor: 'red',
    borderRadius: 20,
    borderWidth: 1,
    width: '90%',
    padding: 20,
    height: '35%',

  }
});
