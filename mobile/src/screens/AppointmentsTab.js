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
import { AppContext } from '../context/AppContext';

const AppointmentsTab = () => {
  const { appointments } = useContext(AppContext);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.userName}>RANDEVULARIM</Text>
      </View>
      <ScrollView style={styles.content}>
        <Text style={styles.sectionTitle}>Günün Ajandası</Text>
        {appointments.map((item, index) => (
          <View key={item.id || index} style={styles.listCard}>
            <View style={styles.dateInfo}>
              <Text style={styles.dateText}>{item.datetime ? item.datetime.split(' ')[1] : '--:--'}</Text>
              <Text style={styles.subDate}>{item.datetime ? item.datetime.split(' ')[0].split('-').slice(1).reverse().join('/') : ''}</Text>
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTitle}>{item.client_name}</Text>
              <Text style={styles.listSub}>{item.baslik1 || 'Görüşme'}</Text>
            </View>
            <TouchableOpacity onPress={() => Alert.alert('Konum', 'Haritalara yönlendiriliyorsunuz...')}>
              <MaterialCommunityIcons name="navigation-variant" size={24} color={Colors.gold} />
            </TouchableOpacity>
          </View>
        ))}
        {appointments.length === 0 && <Text style={styles.emptyText}>Bugün için randevunuz bulunmuyor.</Text>}
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
      emptyText: {
        color: Colors.textMuted,
        textAlign: 'center',
        marginTop: 40,
      },
      dateInfo: {
        alignItems: 'center',
        marginRight: 15,
        minWidth: 50,
      },
      dateText: {
        color: Colors.gold,
        fontSize: 16,
        fontWeight: 'bold',
      },
      subDate: {
        color: Colors.textMuted,
        fontSize: 10,
      },
});

export default AppointmentsTab;
