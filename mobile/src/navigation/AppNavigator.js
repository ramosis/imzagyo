import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

import LoginScreen from '../screens/LoginScreen';
import ForgotScreen from '../screens/ForgotScreen';
import DashboardScreen from '../screens/DashboardScreen';
import LeadsTab from '../screens/LeadsTab';
import AppointmentsTab from '../screens/AppointmentsTab';
import TeamTab from '../screens/TeamTab';
import BottomTabBar from '../components/BottomTabBar';
import Colors from '../constants/Colors';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

const AuthStack = ({
  handleLogin,
  username,
  setUsername,
  password,
  setPassword,
  resetEmail,
  setResetEmail,
  handleForgotPassword,
}) => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="Login">
      {props => <LoginScreen {...props} 
        handleLogin={handleLogin}
        username={username}
        setUsername={setUsername}
        password={password}
        setPassword={setPassword}
      />}
    </Stack.Screen>
    <Stack.Screen name="ForgotPassword">
      {props => <ForgotScreen {...props} 
        resetEmail={resetEmail}
        setResetEmail={setResetEmail}
        handleForgotPassword={handleForgotPassword}
      />}
    </Stack.Screen>
  </Stack.Navigator>
);

const MainTabs = ({
  userRole,
  handleLogout,
  stats,
  recentPortfolios,
  leads,
  appointments,
  fetchLeads,
  sendLocation,
  locationStatus,
  isAutoLocationActive,
  stopAutoLocationTracking,
  startAutoLocationTracking,
  autoLocationStatus
}) => (
  <Tab.Navigator
    tabBar={props => <BottomTabBar {...props} userRole={userRole} />}
  >
    <Tab.Screen name="Dashboard">
      {props => <DashboardScreen {...props} 
        handleLogout={handleLogout}
        stats={stats}
        recentPortfolios={recentPortfolios}
        sendLocation={sendLocation}
        locationStatus={locationStatus}
        isAutoLocationActive={isAutoLocationActive}
        stopAutoLocationTracking={stopAutoLocationTracking}
        startAutoLocationTracking={startAutoLocationTracking}
        autoLocationStatus={autoLocationStatus}
      />}
    </Tab.Screen>
    <Tab.Screen name="Leads">
      {props => <LeadsTab {...props} leads={leads} fetchLeads={fetchLeads} />}
    </Tab.Screen>
    <Tab.Screen name="Appointments">
      {props => <AppointmentsTab {...props} appointments={appointments} />}
    </Tab.Screen>
    <Tab.Screen name="Team" component={TeamTab} />
  </Tab.Navigator>
);

const AppNavigator = (props) => {
  const { isLoggedIn } = props;

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isLoggedIn ? (
          <Stack.Screen name="Main">
            {navProps => <MainTabs {...navProps} {...props} />}
          </Stack.Screen>
        ) : (
          <Stack.Screen name="Auth">
            {navProps => <AuthStack {...navProps} {...props} />}
          </Stack.Screen>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
