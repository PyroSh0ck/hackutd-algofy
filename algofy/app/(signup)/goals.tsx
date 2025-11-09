import { ThemedView } from "@/components/themed-view";
import { ThemedText } from "@/components/themed-text";
import { LinearGradient } from "expo-linear-gradient";
import { Link } from "expo-router";
import { TouchableOpacity } from "react-native";
import { StyleSheet } from "react-native";
import { Selection } from "@/components/ui/selection";

export default function GoalsComp() {
    return (
        <ThemedView style={{display: 'flex', flexDirection: 'column', justifyContent:'space-between', height:'100%'}}>
            <ThemedView style={{paddingTop: 100}}>
                <ThemedText style={{textAlign:'center', fontFamily:'Poppins_600SemiBold', fontSize: 30, paddingTop: 30, paddingHorizontal: 20, lineHeight:45 }}>What are your top financial goals?</ThemedText>
            </ThemedView>
            <ThemedView style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', width: '100%'}}>
                <Selection text={'Reduce Spending'} symbolName={'wallet.bifold'} />
                <Selection text={'Stay on top of finances'} symbolName={'chart.pie.fill'} />
                <Selection text={'Grow my Savings'} symbolName={'dollarsign.bank.building'} />
                <Selection text={'Pay off my debt'} symbolName={'banknote'} />
                <Selection text={'Investing'} symbolName={'chart.bar.xaxis.ascending'} />
            </ThemedView>
            <ThemedView style={styles.continueButtonWrapper}>
                <Link href='/(signup)/congratulations' asChild>
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
