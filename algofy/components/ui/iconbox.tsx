import { ThemedView } from '../themed-view'
import { ThemedText } from '../themed-text'
import { CustomIcon } from './customicon'
import { StyleSheet } from 'react-native'
export function IconBox({ name, title } : { name : string, title : string }) {
    return (
        <ThemedView style={styles.mainContainer}>
            <CustomIcon 
                name={name}
            />
            <ThemedText style={{fontSize: 14, color: '#abebe3'}}>{title}</ThemedText>
        </ThemedView>   
    )
}

const styles = StyleSheet.create({
    mainContainer: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-start',
        alignItems: 'center',
    },
})
