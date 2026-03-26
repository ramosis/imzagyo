import React from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  Alert,
} from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';
import AsyncStorage from '@react-native-async-storage/async-storage';


import React, { useContext } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  Alert,
} from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { AppContext } from '../context/AppContext';


const LeadsTab = () => {
  const { leads, fetchLeads } = useContext(AppContext);
  
  const handleRefresh = async () => {
    const token = await AsyncStorage.getItem('userToken');
    if (token) {
      fetchLeads(token);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.userName}>MÜŞTERİ ADAYLARI</Text>
        <TouchableOpacity style={styles.logoutBtn} onPress={handleRefresh}>
          <MaterialCommunityIcons name="refresh" size={20} color={Colors.gold} />
        </TouchableOpacity>
      </View>
      <ScrollView style={styles.content}>
        <Text style={styles.sectionTitle}>Akıllı Takip Listesi</Text>
        {leads.map((item, index) => (
          <View key={item.id || index} style={styles.listCard}>
            <View style={[styles.listIcon, { backgroundColor: item.ai_score > 70 ? 'rgba(16, 185, 129, 0.1)' : 'rgba(212, 175, 55, 0.1)' }]}>
              <Text style={{ color: item.ai_score > 70 ? '#10B981' : Colors.gold, fontWeight: 'bold' }}>{item.ai_score || 0}</Text>
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTitle}>{item.name}</Text>
              <Text style={styles.listSub}>{item.property_title || 'Genel İlgili'}</Text>
            </View>
            <View style={{ flexDirection: 'row', gap: 10 }}>
              <TouchableOpacity onPress={() => Alert.alert('Arama', `${item.phone} aranıyor...`)}>
                <MaterialCommunityIcons name="phone" size={24} color="#10B981" />
              </TouchableOpacity>
              <TouchableOpacity onPress={() => Alert.alert('WhatsApp', 'WhatsApp şablonu hazırlanıyor...')}>
                <MaterialCommunityIcons name="whatsapp" size={24} color="#25D366" />
              </TouchableOpacity>
            </View>
          </View>
        ))}
        {leads.length === 0 && <Text style={styles.emptyText}>Henüz aday bulunmuyor.</Text>}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
      },
      header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 24,
        paddingTop: 20,
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(212, 175, 55, 0.1)',
      },
      userName: {
        color: Colors.white,
        fontSize: 22,
        fontWeight: 'bold',
        letterSpacing: 1,
      },
      logoutBtn: {
        padding: 10,
        borderRadius: 12,
        backgroundColor: 'rgba(212, 175, 55, 0.1)',
      },
      content: {
        flex: 1,
        padding: 20,
      },
      sectionTitle: {
        color: Colors.gold,
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 20,
        letterSpacing: 1,
      },
      listCard: {
        backgroundColor: Colors.bgCard,
        padding: 15,
        borderRadius: 15,
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 12,
        borderWidth: 1,
        borderColor: 'rgba(212, 175, 55, 0.05)',
      },
      listIcon: {
        width: 45,
        height: 45,
        borderRadius: 12,
        backgroundColor: 'rgba(212, 175, 55, 0.1)',
        alignItems: 'center',
        justifyContent: 'center',
        marginRight: 15,
      },
      listContent: {
        flex: 1,
      },
      listTitle: {
        color: Colors.white,
        fontSize: 16,
        fontWeight: '600',
      },
      listSub: {
        color: Colors.textMuted,
        fontSize: 13,
        marginTop: 2,
      },
      emptyText: {
        color: Colors.textMuted,
        textAlign: 'center',
        marginTop: 40,
      },
});

export default LeadsTab;
