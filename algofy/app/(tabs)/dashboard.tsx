import { StyleSheet, ScrollView, Image } from 'react-native';

<<<<<<< Updated upstream
import { ThemedView } from '@/components/themed-view';
import { Box } from '@/components/ui/box';
import { IconBoxList } from '@/components/ui/iconboxlist';
import { CarouselComp } from '@/components/ui/carousel';
import { ThemedText } from '@/components/themed-text';
import { LinearGradient } from 'expo-linear-gradient';
import {PieChart} from 'react-native-chart-kit'

const data = [
  {
    name: "Seoul",
    population: 21500000,
    color: "rgba(131, 167, 234, 1)",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15
  },
  {
    name: "Toronto",
    population: 2800000,
    color: "#F00",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15
  },
  {
    name: "Beijing",
    population: 527612,
    color: "red",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15
  },
  {
    name: "New York",
    population: 8538000,
    color: "#ffffff",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15
  },
  {
    name: "Moscow",
    population: 11920000,
    color: "rgb(0, 0, 255)",
    legendFontColor: "#7F7F7F",
    legendFontSize: 15
  }
];

const chartConfig = {
  backgroundColor: "#e26a00",
  backgroundGradientFrom: "#fb8c00",
  backgroundGradientTo: "#ffa726",
  decimalPlaces: 2, // optional, defaults to 2dp
  color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
  labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
  style: {
    borderRadius: 16
  },
  propsForDots: {
    r: "6",
    strokeWidth: "2",
    stroke: "#ffa726"
  }
}
=======
import { ThemedView } from "@/components/themed-view";
import { Box } from "@/components/ui/box";
import { IconBoxList } from "@/components/ui/iconboxlist";
import { CarouselComp } from "@/components/ui/carousel";
import { ThemedText } from "@/components/themed-text";
import { LinearGradient } from "expo-linear-gradient";

>>>>>>> Stashed changes

export default function HomeScreen() {
  return (
    <ThemedView style={{height: '100%'}}>
      <ScrollView contentContainerStyle={styles.mainContainer}>
        <ThemedView style={{display:'flex', flexDirection:'row', alignItems:'center', justifyContent:'space-between', width: '100%', paddingTop: 100, paddingHorizontal: 20, }}>
          <ThemedView>
            <ThemedText style={{color: '#abebe3', fontSize: 15}}>Welcome back</ThemedText>
            <ThemedText style={{color: '#abebe3', fontSize: 25, fontFamily: 'Poppins_600SemiBold', paddingTop: 15, paddingBottom: 10, paddingLeft: 5}}>Parth Modi</ThemedText>
            <ThemedText style={{color: '#abebe3', fontSize: 15}}>parthmodi.amodi@gmail.com</ThemedText>
          </ThemedView>
          <Image 
            source={require('@/assets/images/icon.png')}
            style={{width: 80, height: 80}}
          />
        </ThemedView>
        <ThemedView style={styles.box}>
          <Box />
        </ThemedView>
        <ThemedView style={styles.iconboxlist}>
          <IconBoxList />
        </ThemedView>
        <ThemedView style={{display:'flex', flexDirection:'row', justifyContent: 'space-between', alignItems: 'center', height: 230}}>
          <ThemedView style={{height: '80%', width: '40%', marginRight: 20, borderRadius: 20}}>
            <LinearGradient
              colors={['#3a9eba', '#0f4959']}
              style={{borderWidth: 1, height: '100%', width: '100%', borderRadius: 20}}
              start={{x:0, y:0}}
              end={{x:1,y:0}}
            >
              <Image 
              
              />
            </LinearGradient>
          </ThemedView>
          <ThemedView style={{height: '80%', width: '40%', marginLeft: 20, borderRadius: 20}}>
            <LinearGradient
              colors={['#3a9eba', '#0f4959']}
              style={{borderWidth: 1, height: '100%', width: '100%', borderRadius: 20}}
              start={{x:0, y:0}}
              end={{x:1, y:0}}
            >

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
    height: '100%', 
  },
  box: {
    marginTop: 30,
    borderRadius: 20,
    width: '90%',
    height: 230,

  }
});
