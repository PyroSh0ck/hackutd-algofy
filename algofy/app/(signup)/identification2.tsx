import { ThemedView } from "@/components/themed-view"
import { ThemedText } from "@/components/themed-text"
import { Image } from "expo-image"
import { IconSymbol } from "@/components/ui/icon-symbol"
import { StyleSheet } from "react-native"
import { Link } from "expo-router"
import { TouchableOpacity } from "react-native"
import { LinearGradient } from "expo-linear-gradient"

export default function Identification2Comp() {
    return (
        <ThemedView style={{display:'flex', flexDirection:'column', justifyContent: 'space-between', height: '100%'}}>
            <ThemedView style={{paddingTop: 120}}>
                <ThemedText style={{textAlign: 'center', fontFamily: 'Poppins_600SemiBold', fontSize: 30, paddingTop: 20, }}>Confirm Identification</ThemedText>
                <ThemedText style={{textAlign: 'center', fontFamily: 'Poppins_400Regular', fontSize: 15, paddingTop: 20, paddingHorizontal: 40}}>Ensure you are in a location with good lighting</ThemedText>
                <Image 
                    source={require('@/assets/images/scannedFace.png')}
                    style={{width: '55%', height: '40%', alignSelf:'center', marginTop: 30, borderRadius: 50}}
                />
                <ThemedText style={{textAlign: 'center', paddingTop:20, paddingHorizontal: 80, fontSize: 15}}>Keep your shoulders in frame, and keep your camera steady</ThemedText>
                <IconSymbol size={86} name="document.viewfinder.fill" color="white" style={{alignSelf: 'center', marginTop:20, }}/>
                <ThemedText style={{textAlign: 'center'}}>Scan Now!</ThemedText>
            </ThemedView>
                <ThemedView style={styles.continueButtonWrapper}>
                    <Link href='/(signup)/help' asChild>
                        <TouchableOpacity>
                            <LinearGradient
                                colors={['#3a9eba', '#0f4959']}
                                style={styles.continueButton}
                                start={{ x: 0, y: 0 }}
                                end={{ x: 1, y: 0 }}
                            >
                                <ThemedText style={styles.continueButtonText}>Continue</ThemedText>
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
