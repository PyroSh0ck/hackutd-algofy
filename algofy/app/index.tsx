import { ThemedView } from "@/components/themed-view";
import { ThemedText } from "@/components/themed-text";
import { StyleSheet, Image, TouchableOpacity } from "react-native";
import { LinearGradient } from 'expo-linear-gradient';
import { Link } from 'expo-router';

export default function Welcome() {
    return (
        <ThemedView style={styles.mainContainer}>
            <ThemedView style={styles.subContainer}>
                <Image 
                    source={require('@/assets/images/logoWhite.png')}
                    style={styles.logo}
                />
                <ThemedText style={styles.text}>AutoFy</ThemedText>
            </ThemedView>
            <ThemedView style={styles.subContainer2}>
                <Link href='/(tabs)/dashboard' asChild>
                    <TouchableOpacity style={styles.touchable}>
                        <LinearGradient
                            colors={['#3a9eba', '#0f4959']}
                            style={styles.buttonStyle}
                            start={{ x: 0, y: 0}}
                            end={{ x: 1, y: 0}}
                        >
                            <ThemedText style={styles.buttonText}>Log in</ThemedText>
                        </LinearGradient>
                    </TouchableOpacity>
                </Link>
                <Link href='/initial' style={{ paddingTop: 20 }}>
                    <ThemedText style={{ fontSize: 20, fontFamily: 'Poppins_600SemiBold' }}> Don&apos;t have an account? <ThemedText style={{ textDecorationLine: 'underline', fontSize: 20, fontFamily: 'Poppins_600SemiBold'}}>Sign Up</ThemedText></ThemedText>
                </Link>
            </ThemedView>
        </ThemedView>
    )
}

const styles = StyleSheet.create({
    mainContainer: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-around',
        alignItems: 'center',
        height: '100%',
    },
    buttonStyle: {
        padding: 15,
        borderRadius: 40,
        textAlign: 'center',
        width: '100%',
    },
    touchable: {
        width: '80%',
        alignSelf: 'center', 
    },
    buttonText: {
        textAlign: 'center',
        fontSize: 20,
        fontFamily: 'Poppins_600SemiBold',
    },
    subContainer: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
    },
    subContainer2: {
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    text: {
        fontSize: 40,
        paddingTop: 20,
    },
    logo: {
        width: 200,
        height: 200,
    },
})
