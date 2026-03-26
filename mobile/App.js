import React, { useContext } from 'react';
import { StyleSheet, View, StatusBar, ActivityIndicator } from 'react-native';
import { AppProvider, AppContext } from './src/context/AppContext';
import AppNavigator from './src/navigation/AppNavigator';
import Colors from './src/constants/Colors';

const Root = () => {
  const { isLoading, isLoggedIn, userRole, handleLogin, username, setUsername, password, setPassword, resetEmail, setResetEmail, handleForgotPassword, handleLogout, stats, recentPortfolios, leads, appointments, fetchLeads, sendLocation, locationStatus, isAutoLocationActive, stopAutoLocationTracking, startAutoLocationTracking, autoLocationStatus } = useContext(AppContext);

  if (isLoading) {
    return (
      <View style={[styles.container, { justifyContent: 'center' }]}>
        <ActivityIndicator size="large" color={Colors.gold} />
      </View>
    );
  }

  return (
    <AppNavigator
      isLoggedIn={isLoggedIn}
      userRole={userRole}
      handleLogin={handleLogin}
      username={username}
      setUsername={setUsername}
      password={password}
      setPassword={setPassword}
      resetEmail={resetEmail}
      setResetEmail={setResetEmail}
      handleForgotPassword={handleForgotPassword}
      handleLogout={handleLogout}
      stats={stats}
      recentPortfolios={recentPortfolios}
      leads={leads}
      appointments={appointments}
      fetchLeads={fetchLeads}
      sendLocation={sendLocation}
      locationStatus={locationStatus}
      isAutoLocationActive={isAutoLocationActive}
      stopAutoLocationTracking={stopAutoLocationTracking}
      startAutoLocationTracking={startAutoLocationTracking}
      autoLocationStatus={autoLocationStatus}
    />
  );
}

export default function App() {
  return (
    <AppProvider>
      <View style={styles.mainContainer}>
        <StatusBar barStyle="light-content" />
        <Root />
      </View>
    </AppProvider>
  );
}

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    backgroundColor: Colors.bgDark,
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  },
});
