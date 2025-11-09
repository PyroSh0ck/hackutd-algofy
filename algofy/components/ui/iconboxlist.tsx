import { ThemedView } from "../themed-view";
import { StyleSheet } from "react-native";
import { IconBox } from "./iconbox";

export function IconBoxList() {
    return (
        <ThemedView style={styles.mainContainer}>
            <IconBox
                name="dollarsign"
                title="Transfer"
            />
            <IconBox
                name="dollarsign"
                title="Goals"
            />
            <IconBox
                name="dollarsign"
                title="Scan"
            />
            <IconBox
                name="dollarsign"
                title="Swap"
            />
            <IconBox
                name="ellipsis"
                title="More"
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
        padding: 20
    },
})
