import * as React from "react";
import { Dimensions, Text, View, TouchableOpacity } from "react-native";
import { useSharedValue } from "react-native-reanimated";
import Carousel, {
  ICarouselInstance,
  Pagination,
} from "react-native-reanimated-carousel";
import { ThemedView } from "../themed-view";
import { ThemedText } from "../themed-text";
import { StyleSheet } from "react-native";
import { IconSymbol } from "./icon-symbol";
import { CarouselCard } from "./carouselcard";
 
const data = [...new Array(6).keys()];
const width = Dimensions.get("window").width;
 
export function CarouselComp() {
  const ref = React.useRef<ICarouselInstance>(null);
  const progress = useSharedValue<number>(0);
  
  const onPressPagination = (index: number) => {
    ref.current?.scrollTo({
      /**
       * Calculate the difference between the current index and the target index
       * to ensure that the carousel scrolls to the nearest index
       */
      count: index - progress.value,
      animated: true,
    });
  };
  //change to parallax
 
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
                <CarouselCard />
            </ThemedView>
            )}
            
        />
        <TouchableOpacity style={styles.arrowleft} onPress={() => {ref.current?.prev({animated: true})}}>
            <IconSymbol size={28} name="chevron.left" color="white" />
        </TouchableOpacity>
        <TouchableOpacity style={styles.arrowright} onPress={() => {ref.current?.next({animated: true})}}>
            <IconSymbol size={28} name="chevron.right" color="white" />
        </TouchableOpacity>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        position: 'relative',
    },
    arrowleft: {
        position: 'absolute',
        left: 0,
        top: '12%',
        marginLeft: 20,
    },
    arrowright: {
        position: 'absolute',
        right: 0,
        top: '12%',
        marginRight: 20,
    },
    renderedItem: {
        height: '90%',
        width: '70%',
        alignSelf: 'center',
        borderWidth: 1,
        justifyContent: "center",
        backgroundColor: 'transparent',
        borderRadius: 20,
    },
    renderedText: {
        textAlign: 'center',
        fontSize: 30,
        padding: 20,
        color: 'black',
    },
})
