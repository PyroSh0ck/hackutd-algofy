import { TouchableOpacity, Animated } from "react-native"
import { ThemedView } from "../themed-view"
import { ThemedText } from "../themed-text"
import { IconSymbol } from "./icon-symbol"
import { useState, useRef, useEffect } from "react"

type DropDownProps = {
    children: React.ReactNode;
    dropDownName: string;
};

export function DropDown({ children, dropDownName } : DropDownProps) {
    const [open, setOpen] = useState(false);
    const rotateAnim = useRef(new Animated.Value(0)).current;

    useEffect(() => {
        Animated.timing(rotateAnim, {
            toValue: open ? 1 : 0,
            duration: 300,
            useNativeDriver: true,
        }).start();
    }, [open, rotateAnim]);

    const rotation = rotateAnim.interpolate({
        inputRange: [0, 1],
        outputRange: ['0deg', '90deg'],
    });

    return (
        <ThemedView style={{display:'flex', flexDirection:'column'}}>
            <TouchableOpacity onPress={() => {setOpen(prev => !prev)}}>
                <ThemedView style={{padding: 10, borderWidth: 2, borderRadius: 20, width: '100%', display:'flex', flexDirection: 'row', justifyContent:'space-between'}}>
                    <ThemedText style={{textAlign:'left', color: '#abebe3', fontSize: 12, fontFamily: 'Poppins_600SemiBold', paddingLeft: 5}}>{dropDownName}</ThemedText>
                    <Animated.View style={{transform: [{rotate: rotation}], justifyContent: 'center', alignItems: 'center', marginRight: 10}}>
                    <IconSymbol name="arrowtriangle.right.fill" color='#abebe3' size={10} />
                    </Animated.View>
                </ThemedView>
            </TouchableOpacity>
            <ThemedView style={{display: `${open ? 'flex' : 'none'}`, flexDirection: 'column', alignItems: 'center', marginTop: 10}}>
                {children}
            </ThemedView>
        </ThemedView>
    )
}
