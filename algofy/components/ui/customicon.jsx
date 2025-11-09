import { StyleSheet } from 'react-native';
import { IconSymbol } from './icon-symbol';
import { ThemedView } from '../themed-view';

export function CustomIcon({ name }) {
    return (
        <ThemedView style={styles.mainContainer}>
            <IconSymbol size={45} name={name} color="#abebe3" style={styles.symbolStyle} />
        </ThemedView>
    )
}

const styles = StyleSheet.create({
    mainContainer: {
        backgroundColor: '#3b3b3b',
        padding: 11,
        borderRadius: 15,
    },
})
