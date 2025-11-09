import { ThemedView } from "@/components/themed-view";
import { Link } from "expo-router";
import { LinearGradient } from "expo-linear-gradient";
import { TouchableOpacity, StyleSheet } from "react-native";
import { ThemedText } from "@/components/themed-text";

export default function CongratulationsComp() {
    return (
        <ThemedView style={{display:'flex', flexDirection:'column', alignItems: 'center', justifyContent:'space-between', height: '100%'}}>
            <ThemedView style={{paddingTop: 100}}>
                <ThemedText style={{fontSize: 30, fontFamily: 'Poppins_600SemiBold', paddingTop: 250, paddingHorizontal: 40, textAlign: 'center', lineHeight: 45, }}>Congratulations! You&apos;re all set!</ThemedText>
                <ThemedText style={{textAlign: 'center', paddingHorizontal: 40, paddingTop: 30}}>Get ready to manage your finances like a pro.</ThemedText>
            </ThemedView>
            <ThemedView style={styles.continueButtonWrapper}>
                <Link href='/(tabs)/dashboard' asChild>
                    <TouchableOpacity>
                        <LinearGradient
                            colors={['#3a9eba', '#0f4959']}
                            style={styles.continueButton}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                        >
                            <ThemedText style={styles.continueButtonText}>Complete</ThemedText>
                        </LinearGradient>
                    </TouchableOpacity>
                </Link>
            </ThemedView>
        </ThemedView>
    )
}

const styles = StyleSheet.create({
    continueButtonWrapper: {
        paddingBottom: 30,
        paddingTop: 60,
        width: '90%', 
        alignSelf: 'center',
        marginBottom: 30, 
    },
    continueButton: {
        borderRadius: 25,
        paddingVertical: 16,
        alignItems: 'center',
        justifyContent: 'center',
    },
    continueButtonText: {
        fontSize: 16,
        fontWeight: '600',
        color: '#ffffff',
    },
})
