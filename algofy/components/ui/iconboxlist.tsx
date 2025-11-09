import { ThemedView } from "../themed-view";
import { StyleSheet, TouchableOpacity } from "react-native";
import { IconBox } from "./iconbox";
import { Link } from "expo-router";

export function IconBoxList() {
    return (
        <ThemedView style={styles.mainContainer}>
            <Link href='/' asChild>
                <TouchableOpacity>
                    <IconBox
                        name="banknote.fill"
                        title="Transfer"
                    />
                </TouchableOpacity>
            </Link>
            <Link href='/' asChild>
                <TouchableOpacity>
                    <IconBox
                        name="trophy.fill"
                        title="Goals"
                    />
                </TouchableOpacity>
            </Link>
            <Link href='/(stack)/stuff' asChild>
                <TouchableOpacity>
                    <IconBox
                        name="chart.line.uptrend.xyaxis.circle.fill"
                        title="Invest"
                    />
                </TouchableOpacity>
            </Link>
            <Link href='/(stack)/assist' asChild>
                <TouchableOpacity>
                    <IconBox
                        name="person.crop.circle.fill"
                        title="Assistant"
                    />
                </TouchableOpacity>
            </Link>
            <Link href='/(modals)/recommendations' asChild>
                <TouchableOpacity>
                    <IconBox
                        name="clipboard.fill"
                        title="Allocation"
                    />
                </TouchableOpacity>
            </Link>
            
        </ThemedView>
    )
}

const styles = StyleSheet.create({
    mainContainer: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '98%',
        paddingTop: 20,
        paddingHorizontal: 20,
    },
})
