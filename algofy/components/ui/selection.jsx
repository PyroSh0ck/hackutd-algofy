import { LinearGradient } from "expo-linear-gradient";
import { ThemedView } from "../themed-view";
import { IconSymbol } from "./icon-symbol";
import { ThemedText } from "../themed-text";
import { StyleSheet, TouchableOpacity } from "react-native";
import { useState } from 'react';

export function Selection({ text, symbolName}) {
    const [selected, setSelected] = useState(false);
    return (
        <TouchableOpacity style={{width: '80%'}} onPress={() => {setSelected(prev => !prev)}}>
            <LinearGradient
                colors={['#3a9eba', '#0f4959']}
                start={{x: 0, y:0}}
                end={{x:1, y:0}}
                style={selected ? styles.selectedGradient : styles.gradient}
            >
                <ThemedView style={{display: 'flex', flexDirection: 'row', justifyContent:'flex-start', alignItems: 'center', backgroundColor: 'transparent' }}>
                    <IconSymbol size={45} name={symbolName} color="white" style={{alignSelf: 'center', margin: 10 }}/>
                    <ThemedText>{text}</ThemedText>
                </ThemedView>
            </LinearGradient>
        </TouchableOpacity>
    )
}

const styles = StyleSheet.create({
    gradient: {
        borderRadius: 20, 
        width: '100%', 
        marginBottom: 20
    },
    selectedGradient: {
        borderRadius: 20, 
        width: '100%', 
        marginBottom: 20,
        borderWidth: 3,
        borderColor: 'green',
    }
})
