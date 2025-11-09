import { ThemedView } from "@/components/themed-view"
import { ThemedText } from "@/components/themed-text"
import { TouchableOpacity, Image } from "react-native"
import { Link } from "expo-router"
import { IconSymbol } from "@/components/ui/icon-symbol"
import { DropDown } from "@/components/ui/dropdown"

export default function PrefPage() {
  return (
    <ThemedView style={{display: 'flex', flexDirection: 'column', alignItems:'center', height: '100%'}}>
      <ThemedView style={{display:'flex', flexDirection: 'row', justifyContent:'space-between', alignItems: 'center', paddingTop: 100}}>
        <ThemedView style={{display:'flex', flexDirection: 'column', alignItems: 'center', marginRight: 30}}>
          <ThemedText style={{fontFamily:'Poppins_600SemiBold', fontSize: 40, paddingTop: 30, color: '#abebe3'}}>Parth Modi</ThemedText>
          <ThemedText style={{fontSize: 15, color: '#abebe3'}}>parthmodi.amodi@gmail.com</ThemedText>
          <Link href='/'>
            <TouchableOpacity>
              <ThemedText style={{textDecorationLine: 'underline', color: '#abebe3'}}>edit profile</ThemedText>
            </TouchableOpacity>
          </Link>
        </ThemedView>
        <Image 
          source={require('@/assets/images/icon.png')}
          style={{width: 100, height: 100,}}
        />
      </ThemedView>
      <ThemedView style={{width: '90%', marginTop: 40}}>
        <DropDown dropDownName="Linked Accounts">
          <ThemedView style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems:'center', borderBottomWidth: 2, borderBottomColor: '#3b3b3b', marginTop: 10, width: '95%'}}>
            <ThemedView style={{display: 'flex', flexDirection: 'row', alignItems:'center'}}>
              <ThemedView style={{backgroundColor: '#3b3b3b', borderRadius: 10, margin: 20, padding: 8}}>
                <IconSymbol name='banknote' color='#abebe3' size={35} style={{ borderRadius: 10 }} />
              </ThemedView>
              <ThemedView style={{display: 'flex', flexDirection: 'column', justifyContent:'space-evenly', alignItems: 'flex-start'}}>
                <ThemedText style={{fontFamily: 'Poppins_600SemiBold', color: '#abebe3'}}>Fauget Bank</ThemedText>
                <ThemedText style={{color: '#8a8a8a', fontSize: 13}}>Checking Account</ThemedText>
              </ThemedView>
            </ThemedView>
            <ThemedText style={{color: 'green'}}>Linked</ThemedText>
          </ThemedView>
        </DropDown>
        <ThemedView style={{width: '100%', borderWidth: 1, borderRadius: 20, paddingLeft: 15, paddingVertical: 10, borderColor: '#abebe3'}}>
          <ThemedText style={{fontSize: 13, color: '#abebe3'}}>Allow Automatic Payments </ThemedText>
        </ThemedView>
      </ThemedView>
    </ThemedView>
  )
}
