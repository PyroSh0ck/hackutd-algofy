import { ThemedView } from "@/components/themed-view";
import { ThemedText } from "@/components/themed-text";
import { LinearGradient } from "expo-linear-gradient";
import { StyleSheet, ScrollView } from "react-native";
import { View } from "react-native";
import { TextInput } from "react-native";
import { useState } from "react";
import { Link } from "expo-router";
import { TouchableOpacity } from "react-native";

export default function PasswordComp() {

    const [password, setPassword] = useState('')
    const [confirmPwd, setConfirmPwd] = useState('')

    return (
        <ScrollView style={{flex: 1}} contentContainerStyle={{flexGrow: 1}}>
        <ThemedView style={{display:'flex', flexDirection: 'column', justifyContent: 'space-between', minHeight: '100%'}}>
            <ThemedView style={{paddingTop: 100, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <ThemedText style={{textAlign:'center', fontFamily: 'Poppins_600SemiBold', fontSize: 30, paddingTop: 180 }}>Set Your Password</ThemedText>
                <ThemedText style={{paddingVertical: 40, paddingBottom: 60}}>Great! Please create a secure password!</ThemedText>
                <LinearGradient
                    colors={['#3a9eba', '#0f4959']}
                    style={styles.gradientInput}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 0 }}
                >
                    <View style={styles.inputContent}>
                        <ThemedText style={styles.label}>Password *</ThemedText>
                        <TextInput 
                            style={styles.input} 
                            value={password} 
                            onChangeText={setPassword}
                            keyboardType='visible-password'
                            autoCapitalize="none"
                            secureTextEntry={true}
                        />
                    </View>
                </LinearGradient>
                <LinearGradient
                    colors={['#3a9eba', '#0f4959']}
                    style={styles.gradientInput}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 0 }}
                >
                    <View style={styles.inputContent}>
                        <ThemedText style={styles.label}>Confirm Password *</ThemedText>
                        <TextInput 
                            style={styles.input} 
                            value={confirmPwd} 
                            onChangeText={setConfirmPwd}
                            keyboardType='visible-password'
                            autoCapitalize="none"
                            secureTextEntry={true}
                        />
                    </View>
                </LinearGradient>
            </ThemedView>
            <ThemedView style={styles.continueButtonWrapper}>
                <Link href='/(signup)/identification' asChild>
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
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    gradientInput: {
        borderRadius: 50,
        paddingVertical: 6,
        paddingHorizontal: 20,
        width: '70%', 
        marginBottom: 20, 
    },
    inputContent: {
        justifyContent: 'center',
        paddingVertical: 5
    }, 
    input: {
        fontSize: 15,
        color: '#ffffff',
        padding: 0,
        margin: 0,
    },
    label: {
        fontSize: 13,
        fontWeight: '600',
        color: '#ffffff',
        marginBottom: 4,
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
