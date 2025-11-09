import { ThemedView } from "../themed-view";
import { StyleSheet } from "react-native";
import { IconBox } from "./iconbox";

export function IconBoxList() {
    return (
        <ThemedView style={styles.mainContainer}>
            <IconBox
                name="banknote.fill"
                title="Transfer"
            />
            <IconBox
                name="trophy.fill"
                title="Goals"
            />
            <IconBox
                name="chart.line.uptrend.xyaxis.circle.fill"
                title="Invest"
            />
            <IconBox
                name="person.crop.circle.fill"
                title="Assistant"
            />
            <IconBox
                name="clipboard.fill"
                title="Allocation"
            />
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
