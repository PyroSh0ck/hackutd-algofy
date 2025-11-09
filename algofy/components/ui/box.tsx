import { Image } from 'expo-image';
import { View, StyleSheet } from "react-native"
import { ThemedText } from '../themed-text';
import { LinearGradient } from 'expo-linear-gradient';

export function Box() {

    return (
        <LinearGradient
            colors={['#3a9eba', '#0f4959']}
            style={{borderRadius: 20, padding: 20, }}
            start={{x:0, y:0}}
            end={{x:1, y:0}}
        >
            <View style={styles.mainContainer}>
                <Image 
                    source={require('@/assets/images/logoWhite.png')}
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
        </LinearGradient>
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
    },
    moneyText: {
        color: 'white',
        fontSize: 35,
        paddingTop: 30,
        fontFamily: 'Poppins_500Medium'
    },
    asterisks: {
        fontWeight: 'bold',
        fontSize: 20,
    },
    centsText: {
        fontSize: 20,
        fontFamily: 'Poppins_500Medium',
    },
    bankText: {
        fontFamily: 'Poppins_600SemiBold'
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
        height: 80,
        width: 80,
        top: 0,
        right: 0,
        position: 'absolute',
    },
})
