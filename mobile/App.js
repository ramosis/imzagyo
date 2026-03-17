import React, { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TouchableOpacity, 
  TextInput, 
  ScrollView, 
  Dimensions, 
  SafeAreaView, 
  StatusBar,
  ActivityIndicator,
  Alert
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from './src/constants/Colors';

const { width } = Dimensions.get('window');
const isTablet = width > 600;

// API YAPILANDIRMASI
const API_URL = 'https://imzaemlak.com'; // Yeni ana alan adımız

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentScreen, setCurrentScreen] = useState('Login');
  const [isLoading, setIsLoading] = useState(true);
  
  // Login States
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  // Reset States
  const [resetEmail, setResetEmail] = useState('');
  
  // Dashboard Data
  const [stats, setStats] = useState({
    activePortfolio: 0,
    monthlyLeads: 0,
    roi: '0%',
    revenue: '₺0'
  });
  const [recentPortfolios, setRecentPortfolios] = useState([]);

  useEffect(() => {
    checkLoginStatus();
  }, []);

  const checkLoginStatus = async () => {
    try {
      const token = await AsyncStorage.getItem('userToken');
      if (token) {
        setIsLoggedIn(true);
        fetchDashboardData(token);
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
      const response = await fetch(`${API_URL}/api/mobile/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          username, 
          password, 
          app_type: 'investment' 
        }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        await AsyncStorage.setItem('userToken', data.token);
        await AsyncStorage.setItem('userData', JSON.stringify(data));
        setIsLoggedIn(true);
        fetchDashboardData(data.token);
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
    setCurrentScreen('Login');
  };

  const handleForgotPassword = async () => {
    if (!resetEmail) {
      Alert.alert('Hata', 'E-posta adresi gereklidir.');
      return;
    }
    
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/auth/request-reset`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: resetEmail }),
      });
      
      const data = await response.json();
      if (response.ok) {
        Alert.alert('Başarılı', data.message);
        setCurrentScreen('Login');
      } else {
        Alert.alert('Hata', data.error || 'İşlem başarısız.');
      }
    } catch (error) {
      Alert.alert('Bağlantı Hatası', 'E-posta servisine erişilemiyor.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchDashboardData = async (token) => {
    try {
      // Portföy sayılarını ve verileri çekme
      const response = await fetch(`${API_URL}/api/portfoyler`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      
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

  if (isLoading) {
    return (
      <View style={[styles.container, { justifyContent: 'center' }]}>
        <ActivityIndicator size="large" color={Colors.gold} />
      </View>
    );
  }

  // --- RENDERING SCREENS ---

  const LoginScreen = () => (
    <View style={styles.authContainer}>
      <View style={styles.logoCircle}>
        <MaterialCommunityIcons name="shield-crown" size={60} color={Colors.gold} />
      </View>
      <Text style={styles.authTitle}>İMZA GAYRİMENKUL</Text>
      <Text style={styles.authSubtitle}>VIP PORTAL ACCESS</Text>
      
      <View style={styles.inputGroup}>
        <TextInput 
          style={styles.input} 
          placeholder="Kullanıcı Adı" 
          placeholderTextColor={Colors.textMuted}
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
        />
        <TextInput 
          style={styles.input} 
          placeholder="Şifre" 
          placeholderTextColor={Colors.textMuted} 
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />
      </View>

      <TouchableOpacity style={styles.primaryBtn} onPress={handleLogin}>
        <Text style={styles.primaryBtnText}>GİRİŞ YAP</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => setCurrentScreen('Forgot')}>
        <Text style={styles.linkText}>Şifremi Unuttum</Text>
      </TouchableOpacity>
    </View>
  );

  const ForgotScreen = () => (
    <View style={styles.authContainer}>
      <TouchableOpacity style={styles.backBtn} onPress={() => setCurrentScreen('Login')}>
        <MaterialCommunityIcons name="arrow-left" size={24} color={Colors.gold} />
      </TouchableOpacity>
      
      <MaterialCommunityIcons name="lock-reset" size={60} color={Colors.gold} />
      <Text style={styles.authTitle}>Şifre Sıfırlama</Text>
      <Text style={[styles.authSubtitle, { textAlign: 'center', marginHorizontal: 40 }]}>
        E-posta adresinizi girin, size bir sıfırlama bağlantısı gönderelim.
      </Text>
      
      <View style={styles.inputGroup}>
        <TextInput 
          style={styles.input} 
          placeholder="E-posta Adresi" 
          placeholderTextColor={Colors.textMuted}
          keyboardType="email-address"
          autoCapitalize="none"
          value={resetEmail}
          onChangeText={setResetEmail}
        />
      </View>

      <TouchableOpacity style={styles.primaryBtn} onPress={handleForgotPassword}>
        <Text style={styles.primaryBtnText}>GÖNDER</Text>
      </TouchableOpacity>
    </View>
  );

  const DashboardScreen = () => (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.welcomeText}>Hoş Geldiniz,</Text>
          <Text style={styles.userName}>{username.toUpperCase()}</Text>
        </View>
        <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
          <MaterialCommunityIcons name="logout" size={24} color={Colors.gold} />
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.statsGrid}>
          <StatCard title="Aktif Portföy" value={stats.activePortfolio.toString()} icon="home-city" />
          <StatCard title="Aylık Lead" value={stats.monthlyLeads.toString()} icon="account-group" />
          <StatCard title="Ort. ROI" value={stats.roi} icon="trending-up" />
          <StatCard title="Toplam Ciro" value={stats.revenue} icon="currency-try" />
        </View>

        <Text style={styles.sectionTitle}>Bekleyen Talepler & Portföyler</Text>
        
        {recentPortfolios.map((item, index) => (
          <View key={item.id || index} style={styles.listCard}>
            <View style={styles.listIcon}>
              <MaterialCommunityIcons name="home-modern" size={24} color={Colors.gold} />
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTitle}>{item.baslik1 || 'Yeni İlan'}</Text>
              <Text style={styles.listSub}>{item.lokasyon || 'Lokasyon Belirtilmedi'}</Text>
            </View>
            <Text style={styles.listPrice}>{item.fiyat}</Text>
          </View>
        ))}
        
        {recentPortfolios.length === 0 && (
          <Text style={{ color: Colors.textMuted, textAlign: 'center', marginTop: 20 }}>
            Henüz gösterilecek veri bulunamadı.
          </Text>
        )}
      </ScrollView>
    </SafeAreaView>
  );

  return (
    <View style={styles.mainContainer}>
      <StatusBar barStyle="light-content" />
      {!isLoggedIn ? (
        currentScreen === 'Login' ? <LoginScreen /> : <ForgotScreen />
      ) : (
        <DashboardScreen />
      )}
    </View>
  );
}

const StatCard = ({ title, value, icon }) => (
  <View style={styles.statCard}>
    <MaterialCommunityIcons name={icon} size={28} color={Colors.gold} />
    <Text style={styles.statValue}>{value}</Text>
    <Text style={styles.statLabel}>{title}</Text>
  </View>
);

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    backgroundColor: Colors.bgDark,
  },
  container: {
    flex: 1,
  },
  authContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    backgroundColor: Colors.bgDark,
  },
  logoCircle: {
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 2,
    borderColor: Colors.gold,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
    backgroundColor: 'rgba(212, 175, 55, 0.05)',
  },
  authTitle: {
    color: Colors.white,
    fontSize: 28,
    fontWeight: 'bold',
    letterSpacing: 2,
    marginBottom: 5,
  },
  authSubtitle: {
    color: Colors.gold,
    fontSize: 14,
    letterSpacing: 4,
    marginBottom: 40,
  },
  inputGroup: {
    width: '100%',
    marginBottom: 30,
    maxWidth: 400,
  },
  input: {
    backgroundColor: Colors.bgCard,
    width: '100%',
    height: 55,
    borderRadius: 12,
    paddingHorizontal: 20,
    color: Colors.white,
    fontSize: 16,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: 'rgba(212, 175, 55, 0.2)',
  },
  primaryBtn: {
    backgroundColor: Colors.gold,
    width: '100%',
    maxWidth: 400,
    height: 55,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: Colors.gold,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 5,
  },
  primaryBtnText: {
    color: Colors.bgDark,
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 2,
  },
  linkText: {
    color: Colors.textMuted,
    marginTop: 20,
    fontSize: 14,
  },
  backBtn: {
    position: 'absolute',
    top: 60,
    left: 20,
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
  welcomeText: {
    color: Colors.textMuted,
    fontSize: 14,
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
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  statCard: {
    backgroundColor: Colors.bgCard,
    width: isTablet ? '23%' : '48%',
    padding: 20,
    borderRadius: 20,
    marginBottom: 15,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(212, 175, 55, 0.1)',
  },
  statValue: {
    color: Colors.white,
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 10,
  },
  statLabel: {
    color: Colors.textMuted,
    fontSize: 12,
    marginTop: 5,
    textAlign: 'center',
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
  listPrice: {
    color: Colors.gold,
    fontWeight: 'bold',
    fontSize: 16,
  },
});
