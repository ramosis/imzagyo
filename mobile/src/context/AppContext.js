import React, { createContext, useState, useEffect, useRef } from 'react';
import { Alert, Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Geolocation from 'react-native-geolocation-service';
import { request, PERMISSIONS, RESULTS } from 'react-native-permissions';
import * as api from '../services/api';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [resetEmail, setResetEmail] = useState('');
  const [stats, setStats] = useState({ revenue: '₺0' });
  const [recentPortfolios, setRecentPortfolios] = useState([]);
  const [leads, setLeads] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [userRole, setUserRole] = useState('staff');
  const [locationStatus, setLocationStatus] = useState('');
  const [autoLocationStatus, setAutoLocationStatus] = useState('');
  const [isAutoLocationActive, setIsAutoLocationActive] = useState(false);
  const autoLocationIntervalRef = useRef(null);

  useEffect(() => {
    checkLoginStatus();
    return () => {
      if (autoLocationIntervalRef.current) {
        clearInterval(autoLocationIntervalRef.current);
      }
    };
  }, []);

  const checkLoginStatus = async () => {
    try {
      const token = await AsyncStorage.getItem('userToken');
      if (token) {
        setIsLoggedIn(true);
        const userDataStr = await AsyncStorage.getItem('userData');
        if (userDataStr) {
          const userData = JSON.parse(userDataStr);
          setUserRole(userData.role || 'staff');
        }
        fetchDashboardData();
        fetchLeads();
        fetchAppointments();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Hata', 'Kullanıcı adı ve şifre gereklidir.');
      return;
    }
    
    setIsLoading(true);
    try {
      const data = await api.login(username, password);
      
      if (data.token) {
        await AsyncStorage.setItem('userToken', data.token);
        await AsyncStorage.setItem('userData', JSON.stringify(data));
        setIsLoggedIn(true);
        setUserRole(data.role || 'staff');
        fetchDashboardData();
        fetchLeads();
        fetchAppointments();
      } else {
        Alert.alert('Giriş Başarısız', data.error || 'Kontrol edip tekrar deneyin.');
      }
    } catch (error) {
      Alert.alert('Bağlantı Hatası', 'Sunucuya erişilemiyor. Lütfen internetinizi kontrol edin.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    await AsyncStorage.clear();
    setIsLoggedIn(false);
  };

  const handleForgotPassword = async () => {
    if (!resetEmail) {
      Alert.alert('Hata', 'E-posta adresi gereklidir.');
      return;
    }
    
    setIsLoading(true);
    try {
      const data = await api.requestPasswordReset(resetEmail);
      if (data.message) {
        Alert.alert('Başarılı', data.message);
      } else {
        Alert.alert('Hata', data.error || 'İşlem başarısız.');
      }
    } catch (error) {
      Alert.alert('Bağlantı Hatası', 'E-posta servisine erişilemiyor.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchDashboardData = async () => {
    try {
      const data = await api.getPortfolios();
      if (Array.isArray(data)) {
        setRecentPortfolios(data.slice(0, 5));
        setStats({
          activePortfolio: data.length,
          monthlyLeads: Math.floor(data.length * 4.2), // Mock hesaplama
          roi: '%18.4',
          revenue: '₺2.4M'
        });
      }
    } catch (error) {
      console.log('Veri çekme hatası:', error);
    }
  };

  const fetchLeads = async () => {
    try {
      const data = await api.getLeads();
      if (Array.isArray(data)) setLeads(data);
    } catch (error) {
      console.log('Leads çekme hatası:', error);
    }
  };

  const fetchAppointments = async () => {
    try {
      const data = await api.getAppointments();
      if (Array.isArray(data)) setAppointments(data);
    } catch (error) {
      console.log('Randevu çekme hatası:', error);
    }
  };

  const requestLocationPermission = async () => {
    const permission = Platform.select({
      ios: PERMISSIONS.IOS.LOCATION_WHEN_IN_USE,
      android: PERMISSIONS.ANDROID.ACCESS_FINE_LOCATION,
    });

    if (!permission) {
        return false;
    }

    const result = await request(permission);
    return result === RESULTS.GRANTED;
  };

  const sendLocation = async () => {
    setLocationStatus('Konum izni kontrol ediliyor...');
    const hasPermission = await requestLocationPermission();
    if (!hasPermission) {
      setLocationStatus('Konum izni reddedildi.');
      return;
    }
  
    setLocationStatus('Konum alınıyor...');
    try {
      Geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          const data = await api.sendLocationUpdate(latitude, longitude);
          
          if (data) {
            setLocationStatus('Konum başarıyla gönderildi');
            setTimeout(() => setLocationStatus(''), 3000);
          } else {
            setLocationStatus('Konum gönderimi başarısız: ' + (data.error || 'Bilinmeyen hata'));
          }
        },
        (error) => {
          console.log('Konum hatası:', error);
          setLocationStatus('Konum alınamadı: ' + error.message);
        },
        { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
      );
    } catch (error) {
      console.log('Konum gönderimi hatası:', error);
      setLocationStatus('Konum gönderimi başarısız: ' + error.message);
    }
  };
  
  const startAutoLocationTracking = () => {
      // ... (start auto location implementation)
  };

  const stopAutoLocationTracking = () => {
      // ... (stop auto location implementation)
  };

  return (
    <AppContext.Provider value={{
      isLoggedIn,
      isLoading,
      userRole,
      username, setUsername,
      password, setPassword,
      resetEmail, setResetEmail,
      stats,
      recentPortfolios,
      leads,
      appointments,
      locationStatus,
      autoLocationStatus,
      isAutoLocationActive,
      handleLogin,
      handleLogout,
      handleForgotPassword,
      fetchLeads,
      sendLocation,
      startAutoLocationTracking,
      stopAutoLocationTracking
    }}>
      {children}
    </AppContext.Provider>
  );
};
