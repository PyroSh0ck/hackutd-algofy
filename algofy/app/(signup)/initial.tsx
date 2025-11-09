import { ThemedView } from "@/components/themed-view";
import { ThemedText } from "@/components/themed-text";
import { StyleSheet, TextInput, View, TouchableOpacity, ScrollView } from "react-native";
import { useState } from "react";
import { LinearGradient } from "expo-linear-gradient";
import { Link } from "expo-router";

export default function SignUp() {
    const [email, setEmail] = useState('')
    const [name, setName] = useState('')
    const [phoneNumber, setPhoneNumber] = useState('')
    const [birthDate, setBirthDate] = useState('')
    const [ssn, setSSN] = useState('')
    const [country, setCountry] = useState('')
    const [state, setState] = useState('')

    return (
        <ScrollView style={styles.container}>
            <ThemedView style={styles.contentContainer}>
                {/* Header Section */}
                <ThemedView style={styles.headerSection}>
                    <ThemedText style={{textAlign: 'center', fontSize: 31, paddingTop: 20, fontFamily: 'Poppins_600SemiBold'}}>Enter your information</ThemedText>
                    <ThemedText style={{fontSize: 15, fontFamily:'Poppins_400Regular', paddingHorizontal: 5, paddingTop: 40}}>
                        We need to use this to contact you and verify your credentials.
                    </ThemedText>
                </ThemedView>

                {/* Input Fields */}
                <ThemedView style={styles.inputsContainer}>
                    {/* Email */}
                    <View style={styles.inputWrapper}>
                        <LinearGradient
                            colors={['#3a9eba', '#0f4959']}
                            style={styles.gradientInput}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                        >
                            <View style={styles.inputContent}>
                                <ThemedText style={styles.label}>Email *</ThemedText>
                                <TextInput 
                                    style={styles.input} 
                                    value={email} 
                                    onChangeText={setEmail}
                                    keyboardType="email-address"
                                    autoCapitalize="none"
                                />
                            </View>
                        </LinearGradient>
                    </View>

                    {/* Name */}
                    <View style={styles.inputWrapper}>
                        <LinearGradient
                            colors={['#3a9eba', '#0f4959']}
                            style={styles.gradientInput}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                        >
                            <View style={styles.inputContent}>
                                <ThemedText style={styles.label}>Name *</ThemedText>
                                <TextInput
                                    style={styles.input}
                                    value={name}
                                    onChangeText={setName}
                                    autoCapitalize="words"
                                />
                            </View>
                        </LinearGradient>
                    </View>

                    {/* Phone Number */}
                    <View style={styles.inputWrapper}>
                        <LinearGradient
                            colors={['#3a9eba', '#0f4959']}
                            style={styles.gradientInput}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                        >
                            <View style={styles.inputContent}>
                                <ThemedText style={styles.label}>Phone Number *</ThemedText>
                                <TextInput 
                                    style={styles.input} 
                                    value={phoneNumber} 
                                    onChangeText={setPhoneNumber}
                                    keyboardType="phone-pad"
                                />
                            </View>
                        </LinearGradient>
                    </View>

                    {/* Birth Date */}
                    <View style={styles.inputWrapper}>
                        <LinearGradient
                            colors={['#3a9eba', '#0f4959']}
                            style={styles.gradientInput}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                        >
                            <View style={styles.inputContent}>
                                <ThemedText style={styles.label}>Birth Date *</ThemedText>
                                <TextInput 
                                    style={styles.input} 
                                    value={birthDate} 
                                    onChangeText={setBirthDate}
                                    placeholder="MM/DD/YYYY"
                                    placeholderTextColor="#006b7a"
                                />
                            </View>
                        </LinearGradient>
                    </View>

                    {/* SSN */}
                    <View style={styles.inputWrapper}>
                        <LinearGradient
                            colors={['#3a9eba', '#0f4959']}
                            style={styles.gradientInput}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                        >
                            <View style={styles.inputContent}>
                                <ThemedText style={styles.label}>SSN *</ThemedText>
                                <ThemedText style={styles.prototypeText}>N/A for the prototype</ThemedText>
                            </View>
                        </LinearGradient>
                    </View>

                    {/* Country and State Row */}
                    <View style={styles.rowContainer}>
                        <View style={styles.countryInput}>
                            <LinearGradient
                                colors={['#3a9eba', '#1D6579']}
                                style={[styles.gradientInput, styles.rowInput]}
                                start={{ x: 0, y: 0 }}
                                end={{ x: 1, y: 0 }}
                            >
                                <View style={styles.inputContent}>
                                    <ThemedText style={styles.label}>Country</ThemedText>
                                    <ThemedText style={styles.prototypeText}>US only (Stripe limitation)</ThemedText>
                                </View>
                            </LinearGradient>
                        </View>

                        <View style={styles.stateInput}>
                            <LinearGradient
                                colors={['#1D6579', '#0f4959']}
                                style={[styles.gradientInput, styles.rowInput]}
                                start={{ x: 0, y: 0 }}
                                end={{ x: 1, y: 0 }}
                            >
                                <View style={styles.inputContent}>
                                    <ThemedText style={styles.label}>State</ThemedText>
                                    <TextInput
                                        style={styles.input}
                                        value={state}
                                        onChangeText={setState}
                                        autoCapitalize="characters"
                                        maxLength={2}
                                    />
                                </View>
                            </LinearGradient>
                        </View>
                    </View>
                </ThemedView>

                {/* Continue Button */}
                <ThemedView style={styles.continueButtonWrapper}>
                    <Link href='/(signup)/password' asChild>
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
    container: {
        flex: 1,
        backgroundColor: '#1a1a1a',
    },
    contentContainer: {
        flex: 1,
        paddingHorizontal: 30,
        paddingTop: 90,
    },
    headerSection: {
        marginBottom: 40,
        paddingHorizontal: 10,
    },
    title: {
        fontSize: 24,
        fontWeight: '600',
        marginBottom: 15,
        color: '#ffffff',
    },
    subtitle: {
        fontSize: 14,
        color: '#cccccc',
        lineHeight: 20,
    },
    inputsContainer: {
        flex: 1,
    },
    inputWrapper: {
        marginBottom: 12,
    },
    gradientInput: {
        borderRadius: 25,
        paddingVertical: 12,
        paddingHorizontal: 20,
        minHeight: 65,
        justifyContent: 'center',
    },
    inputContent: {
        justifyContent: 'center',
    },
    label: {
        fontSize: 13,
        fontWeight: '600',
        color: '#ffffff',
        marginBottom: 4,
    },
    input: {
        fontSize: 15,
        color: '#ffffff',
        padding: 0,
        margin: 0,
    },
    prototypeText: {
        fontSize: 13,
        color: '#e0e0e0',
        fontStyle: 'italic',
    },
    rowContainer: {
        flexDirection: 'row',
        gap: 10,
        marginBottom: 12,
    },
    rowInput: {
        height: 90,
    },
    countryInput: {
        flex: 1,
    },
    stateInput: {
        width: '30%'
    },
    continueButtonWrapper: {
        paddingBottom: 30,
        paddingTop: 60,
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
