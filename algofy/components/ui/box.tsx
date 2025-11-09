import { Image } from 'expo-image';
import { View, Text, StyleSheet } from "react-native"
import { ThemedText } from '../themed-text';

export function Box() {

    return (
        <View style={styles.mainContainer}>
            <Image 
                source={require('@/assets/images/partial-react-logo.png')}
                style={styles.logo}
            />  
            <View style={styles.leftSide}>
                <View style={styles.topLeft}>
                    <ThemedText style={styles.moneyText}>$5,500<ThemedText style={styles.centsText}>.50</ThemedText></ThemedText>
                    <ThemedText style={styles.text}>Balance</ThemedText>
                </View>
                <View style={styles.bottomLeft}>
                    <ThemedText style={styles.asterisks}>*****</ThemedText>
                    <ThemedText style={styles.text}>123-456-7890</ThemedText>
                </View>
            </View>
            <View style={styles.rightSide}>
                <ThemedText style={styles.bankText}>Fauget Bank</ThemedText>
                <ThemedText style={styles.text}>Credit Card</ThemedText>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    mainContainer: {
        display: 'flex',
        position: 'relative',
        flexDirection: 'row',
        justifyContent: 'space-between',
        padding: 'auto',
        height: '100%',

    },
    text: {
        color: 'white',
        fontWeight: '300',
    },
    moneyText: {
        color: 'white',
        fontSize: 35,
        fontWeight: 'bold',
        paddingTop: 30,
    },
    asterisks: {
        fontWeight: 'bold',
        fontSize: 20,
    },
    centsText: {
        fontSize: 20,
        fontWeight: '300',
    },
    bankText: {
        fontWeight: 'bold',
    },
    leftSide: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',

    },
    rightSide: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-end',
        alignItems: 'flex-end',
    },
    topLeft: {

    },
    bottomLeft: {

    },
    logo: {
        height: '10%',
        width: '10%',
        top: 0,
        right: 0,
        position: 'absolute',
    },
})
