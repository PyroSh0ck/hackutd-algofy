import { ThemedView } from "@/components/themed-view";
import { ThemedText } from "@/components/themed-text";
import { LinearGradient } from "expo-linear-gradient";
import { Link } from "expo-router";
import { TouchableOpacity } from "react-native";
import { StyleSheet } from "react-native";
import { Selection } from "@/components/ui/selection";

export default function HelpComp() {
    return (
        <ThemedView style={{display: 'flex', flexDirection: 'column', justifyContent:'space-between', height:'100%'}}>
            <ThemedView style={{paddingTop: 100}}>
                <ThemedText style={{textAlign:'center', fontFamily:'Poppins_600SemiBold', fontSize: 30, paddingTop: 20 }}>Where can we help?</ThemedText>
                <ThemedText style={{textAlign:'center', paddingTop: 20}}>Choose all options that apply.</ThemedText>
            </ThemedView>
            <ThemedView style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', width: '100%'}}>
                <Selection text={'Lower My Bills'} symbolName={'text.page.badge.magnifyingglass'} />
                <Selection text={'Create A Budget'} symbolName={'rectangle.grid.3x2'} />
                <Selection text={'Track My Spending'} symbolName={'chart.xyaxis.line'} />
                <Selection text={'Track My Networth'} symbolName={'chart.bar.fill'} />
                <Selection text={'Cancel Subscriptions'} symbolName={'nosign'} />
            </ThemedView>
            <ThemedView style={styles.continueButtonWrapper}>
                <Link href='/(signup)/goals' asChild>
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
    gradient: {
        borderRadius: 20, 
        width: '80%', 
        marginBottom: 20
    },
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
