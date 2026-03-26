import React from 'react';
import { StyleSheet, View, TouchableOpacity, Text } from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';

const BottomTabBar = ({ state, navigation, userRole }) => {
  const TabItem = ({ icon, label, routeName, active, onClick }) => (
    <TouchableOpacity style={styles.tabItem} onPress={onClick}>
      <MaterialCommunityIcons name={icon} size={24} color={active ? Colors.gold : Colors.textMuted} />
      <Text style={[styles.tabLabel, { color: active ? Colors.gold : Colors.textMuted }]}>{label}</Text>
    </TouchableOpacity>
  );

  const currentRouteName = state.routes[state.index].name;

  return (
    <View style={styles.tabBar}>
      <TabItem 
        icon="view-dashboard" 
        label="Özet" 
        routeName="Dashboard"
        active={currentRouteName === 'Dashboard'} 
        onClick={() => navigation.navigate('Dashboard')} 
      />
      <TabItem 
        icon="account-group" 
        label="Adaylar" 
        routeName="Leads"
        active={currentRouteName === 'Leads'} 
        onClick={() => navigation.navigate('Leads')} 
      />
      <TabItem 
        icon="calendar-clock" 
        label="Randevu" 
        routeName="Appointments"
        active={currentRouteName === 'Appointments'} 
        onClick={() => navigation.navigate('Appointments')} 
      />
      {userRole === 'admin' && (
        <TabItem 
          icon="security" 
          label="Yönetim" 
          routeName="Team"
          active={currentRouteName === 'Team'} 
          onClick={() => navigation.navigate('Team')} 
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  tabBar: {
    flexDirection: 'row',
    height: 70,
    backgroundColor: '#1A1A22',
    borderTopWidth: 1,
    borderTopColor: 'rgba(212, 175, 55, 0.1)',
    paddingBottom: 10,
  },
  tabItem: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  tabLabel: {
    fontSize: 10,
    marginTop: 4,
    fontWeight: '600',
  },
});

export default BottomTabBar;
