import { StyleSheet } from 'react-native';
import { IconSymbol } from './icon-symbol';
import { ThemedView } from '../themed-view';

export function CustomIcon({ name }) {
    return (
        <ThemedView style={styles.mainContainer}>
            <IconSymbol size={45} name={name} color="white" style={styles.symbolStyle} />
        </ThemedView>
    )
}

const styles = StyleSheet.create({
    mainContainer: {
        backgroundColor: 'gray',
        padding: 11,
        borderRadius: 15,
    },
})
