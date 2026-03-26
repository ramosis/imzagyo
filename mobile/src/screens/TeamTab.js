import React from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';

const TeamTab = () => (
  <SafeAreaView style={styles.container}>
    <View style={styles.header}>
      <Text style={styles.userName}>EKİP PANORAMASI</Text>
    </View>
    <ScrollView style={styles.content}>
      <Text style={styles.sectionTitle}>Saha Takibi</Text>
      <View style={styles.listCard}>
        <MaterialCommunityIcons name="account-circle" size={40} color={Colors.gold} style={{ marginRight: 15 }} />
        <View style={styles.listContent}>
          <Text style={styles.listTitle}>Ahmet Yılmaz</Text>
          <Text style={styles.listSub}>Son Check-in: Çatalca (10 dk önce)</Text>
        </View>
        <View style={styles.statusBadge}><Text style={styles.statusText}>AKTİF</Text></View>
      </View>
      <View style={styles.listCard}>
        <MaterialCommunityIcons name="account-circle" size={40} color={Colors.textMuted} style={{ marginRight: 15 }} />
        <View style={styles.listContent}>
          <Text style={styles.listTitle}>Ayşe Demir</Text>
          <Text style={styles.listSub}>Çevrimdışı (Mesai bitti)</Text>
        </View>
        <View style={[styles.statusBadge, { backgroundColor: '#444' }]}><Text style={styles.statusText}>PASİF</Text></View>
      </View>
    </ScrollView>
  </SafeAreaView>
);

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
      statusBadge: {
        backgroundColor: '#10B981',
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 6,
      },
      statusText: {
        color: Colors.bgDark,
        fontSize: 9,
        fontWeight: 'bold',
      },
});

export default TeamTab;
