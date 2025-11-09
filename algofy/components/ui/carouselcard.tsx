import { LinearGradient } from "expo-linear-gradient";
import { ThemedView } from "../themed-view";
import { ThemedText } from "../themed-text";
import { TouchableOpacity } from "react-native";
import { Link } from "expo-router";

export function CarouselCard() {
    const data = {
        title: "Something something modal blah blah",
        imgUrl: "coolios",
        desc: "oo this is gonna be long hehe",
        blah: 'lah'
    };
    return (
        <ThemedView>
<<<<<<< Updated upstream
           {/* Gradient */}  <LinearGradient
                colors={['#11b3a1', '#0e9c8f']}
                style={{height: '100%', width: '100%', borderRadius: 20, borderColor: 'rgba(24, 55, 68, 0.2)', borderWidth: 3, position:'relative', display:'flex', flexDirection:'column'}}
                start={{x:0, y:0}}
                end={{x:1,y:0}}
            >
           {/* Top Right Circle */} <ThemedView style={{height: 100, width: 100, borderRadius: 9999, backgroundColor: 'rgba(211, 211, 211, 0.1)', position: 'absolute', right: -25, top: -25}}></ThemedView>
            {/* Bottom Left Circle */} <ThemedView style={{height: 200, width: 200, borderRadius: 9999, backgroundColor: 'rgba(211, 211, 211, 0.1)', position: 'absolute', left: -30, bottom: -30}}></ThemedView>
            <ThemedView style={{borderWidth:1, height: 40, width: 40, borderRadius: 10, marginTop: 20, marginLeft: 20, marginBottom:15, backgroundColor: '#37beaf', borderColor: '#57c7ba'}}></ThemedView>
            <ThemedText style={{fontFamily:'Poppins_600SemiBold', marginLeft: 20, fontSize: 20}}>Watch your budget!</ThemedText>
          {/* Text */}   <ThemedView style={{marginHorizontal: 20, marginTop: 10, flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', backgroundColor: 'transparent'}}>
                <ThemedText style={{fontSize: 10, lineHeight: 20}}>You overspent </ThemedText>
                <ThemedView style={{paddingHorizontal: 6, paddingVertical: 3, backgroundColor: '#34b5a7', borderRadius: 4}}>
                    <ThemedText style={{fontSize: 10, fontFamily: 'Poppins_600SemiBold', lineHeight: 14}}>just a little</ThemedText>
                </ThemedView>
                <ThemedText style={{fontSize: 10, lineHeight: 20}}>on takeout this week. Maybe cutback on going out this week?</ThemedText>
            </ThemedView>
            </LinearGradient>
=======
            <Link href={{
                pathname: '/(modals)/recommendations',
                params: {
                    title: data.title,
                    imgUrl: data.imgUrl,
                    desc: data.desc,
                    blah: data.blah
                },
                }} 
                asChild
            >
                <TouchableOpacity>
                    <LinearGradient
                        colors={['#11b3a1', '#0e9c8f']}
                        style={{height: '100%', width: '100%', borderRadius: 20, borderColor: 'rgba(24, 55, 68, 0.2)', borderWidth: 3, position:'relative', display:'flex', flexDirection:'column'}}
                        start={{x:0, y:0}}
                        end={{x:1,y:0}}
                    >
                        <ThemedView style={{height: 100, width: 100, borderRadius: 9999, backgroundColor: 'rgba(211, 211, 211, 0.1)', position: 'absolute', right: -25, top: -25}}></ThemedView>
                        <ThemedView style={{height: 200, width: 200, borderRadius: 9999, backgroundColor: 'rgba(211, 211, 211, 0.1)', position: 'absolute', left: -30, bottom: -30}}></ThemedView>
                        <ThemedView style={{borderWidth:1, height: 40, width: 40, borderRadius: 10, marginTop: 20, marginLeft: 20, marginBottom:15, backgroundColor: '#37beaf', borderColor: '#57c7ba'}}></ThemedView>
                        <ThemedText style={{fontFamily:'Poppins_600SemiBold', marginLeft: 20, fontSize: 20}}>Watch your budget!</ThemedText>
                        <ThemedView style={{marginHorizontal: 20, marginTop: 10, flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', backgroundColor: 'transparent'}}>
                            <ThemedText style={{fontSize: 10, lineHeight: 20}}>You overspent </ThemedText>
                            <ThemedView style={{paddingHorizontal: 6, paddingVertical: 3, backgroundColor: '#34b5a7', borderRadius: 4}}>
                                <ThemedText style={{fontSize: 10, fontFamily: 'Poppins_600SemiBold', lineHeight: 14}}>just a little</ThemedText>
                            </ThemedView>
                            <ThemedText style={{fontSize: 10, lineHeight: 20}}>on takeout this week. Maybe cutback on going out this week?</ThemedText>
                        </ThemedView>
                    </LinearGradient>
                </TouchableOpacity>
            </Link>
>>>>>>> Stashed changes
        </ThemedView>
    )
}
