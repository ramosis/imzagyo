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
import Geolocation from '@react-native-community/geolocation';
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
    revenue: '₺0'
  });
  const [recentPortfolios, setRecentPortfolios] = useState([]);
  const [leads, setLeads] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [userRole, setUserRole] = useState('staff'); // 'admin' or 'staff'
  const [currentTab, setCurrentTab] = useState('Dashboard'); // 'Dashboard', 'Leads', 'Appointments', 'Team'
  const [locationStatus, setLocationStatus] = useState(''); // Manuel konum durumu
  const [autoLocationStatus, setAutoLocationStatus] = useState(''); // Otomatik konum durumu
  const [isAutoLocationActive, setIsAutoLocationActive] = useState(false); // Otomatik konum aktif mi?
  const [batteryLevel, setBatteryLevel] = useState(null); // Pil seviyesi
  const [isBatterySaving, setIsBatterySaving] = useState(false); // Pil tasarrufu modu
  let autoLocationInterval = null; // Interval referansı

  // Component unmount olduğunda interval'i temizle
  useEffect(() => {
    return () => {
      if (autoLocationInterval) {
        clearInterval(autoLocationInterval);
      }
    };
  }, []);

  // Pil seviyesi değişikliklerini dinleme
  useEffect(() => {
    // Sadece tarayıcı ortamında çalış
    if (typeof navigator !== 'undefined' && navigator.getBattery) {
      navigator.getBattery().then(battery => {
        setBatteryLevel(battery.level * 100);
        
        battery.addEventListener('levelchange', () => {
          setBatteryLevel(battery.level * 100);
        });
      }).catch(err => {
        console.log('Pil bilgisi alınamadı:', err);
      });
    }
  }, []);

  // Mesai saatlerini kontrol eden fonksiyon (09:00 - 18:00)
  const isWorkHours = () => {
    const now = new Date();
    const hours = now.getHours();
    const day = now.getDay(); // 0 = Pazar, 1 = Pazartesi, ..., 6 = Cumartesi
    
    // Hafta sonu değilse ve mesai saatlerindeyse
    return day >= 1 && day <= 5 && hours >= 9 && hours < 18;
  };

  // Otomatik konum gönderimi için fonksiyon
  const sendAutoLocation = async () => {
    // Pil tasarrufu modu aktifse ve pil seviyesi düşükse gönderimi azalt
    if (isBatterySaving && batteryLevel !== null && batteryLevel < 20) {
      console.log('Düşük pil ve tasarruf modu aktif, konum gönderimi atlandı');
      setAutoLocationStatus('Pil tasarrufu: Konum gönderimi atlandı');
      return;
    }

    if (!isWorkHours()) {
      console.log('Mesai saatleri dışında, konum gönderimi yapılmıyor');
      return;
    }

    setAutoLocationStatus('Otomatik konum gönderiliyor...');
    
    try {
      // Konum izni kontrolü ve konum alma
      Geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          
          // Kullanıcı token'ını alma
          const token = await AsyncStorage.getItem('userToken');
          
          // Konum verisini sunucuya gönderme
          const response = await fetch(`${API_URL}/api/tracking/location`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
              latitude,
              longitude,
              timestamp: new Date().toISOString(),
              auto: true // Otomatik gönderim olduğunu belirtmek için
            })
          });
          
          const data = await response.json();
          
          if (response.ok) {
            setAutoLocationStatus('Otomatik konum başarıyla gönderildi');
          } else {
            setAutoLocationStatus('Otomatik konum gönderimi başarısız: ' + (data.error || 'Bilinmeyen hata'));
          }
        },
        (error) => {
          console.log('Otomatik konum hatası:', error);
          setAutoLocationStatus('Otomatik konum alınamadı: ' + error.message);
        },
        { 
          enableHighAccuracy: !isBatterySaving, // Pil tasarrufunda hassasiyeti düşür
          timeout: 15000, 
          maximumAge: isBatterySaving ? 300000 : 10000 // Pil tasarrufunda eski konumu daha uzun süre kabul et
        }
      );
    } catch (error) {
      console.log('Otomatik konum gönderimi hatası:', error);
      setAutoLocationStatus('Otomatik konum gönderimi başarısız: ' + error.message);
    }
  };

  // Otomatik konum gönderimini başlatan fonksiyon
  const startAutoLocationTracking = () => {
    if (autoLocationInterval) return; // Zaten çalışıyor
    
    // İlk gönderimi hemen yap
    sendAutoLocation();
    
    // Pil tasarrufu modu aktifse gönderim sıklığını azalt
    const intervalTime = isBatterySaving ? 30 * 60 * 1000 : 10 * 60 * 1000; // 30 dakika veya 10 dakika
    
    // Sonrasında belirlenen sıklıkta gönderim
    autoLocationInterval = setInterval(sendAutoLocation, intervalTime);
    setIsAutoLocationActive(true);
  };

  // Otomatik konum gönderimini durduran fonksiyon
  const stopAutoLocationTracking = () => {
    if (autoLocationInterval) {
      clearInterval(autoLocationInterval);
      autoLocationInterval = null;
      setIsAutoLocationActive(false);
      setAutoLocationStatus('Otomatik konum takibi durduruldu');
    }
  };

  useEffect(() => {
    checkLoginStatus();
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
        fetchDashboardData(token);
        fetchLeads(token);
        fetchAppointments(token);
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
        setUserRole(data.role || 'staff');
        fetchDashboardData(data.token);
        fetchLeads(data.token);
        fetchAppointments(data.token);
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

  const fetchLeads = async (token) => {
    try {
      const response = await fetch(`${API_URL}/api/leads`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      if (Array.isArray(data)) setLeads(data);
    } catch (error) {
      console.log('Leads çekme hatası:', error);
    }
  };

  const fetchAppointments = async (token) => {
    try {
      const response = await fetch(`${API_URL}/api/appointments`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      if (Array.isArray(data)) setAppointments(data);
    } catch (error) {
      console.log('Randevu çekme hatası:', error);
    }
  };

  // Konum gönderimi için fonksiyon
  const sendLocation = async () => {
    setLocationStatus('Konum alınıyor...');
    
    try {
      // Konum izni kontrolü ve konum alma
      Geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          
          // Kullanıcı token'ını alma
          const token = await AsyncStorage.getItem('userToken');
          
          // Konum verisini sunucuya gönderme
          const response = await fetch(`${API_URL}/api/tracking/location`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
              latitude,
              longitude,
              timestamp: new Date().toISOString()
            })
          });
          
          const data = await response.json();
          
          if (response.ok) {
            setLocationStatus('Konum başarıyla gönderildi');
            setTimeout(() => setLocationStatus(''), 3000); // 3 saniye sonra mesajı sil
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
        
          {/* Pil Seviyesi ve Tasarruf Modu */}
        <View style={styles.batterySection}>
          <Text style={styles.sectionTitle}>Pil Yönetimi</Text>
          <View style={styles.batteryInfo}>
            <MaterialCommunityIcons name="battery" size={24} color={Colors.gold} />
            <Text style={styles.batteryText}>
              Pil Seviyesi: {batteryLevel !== null ? `${Math.round(batteryLevel)}%` : 'Okunuyor...'}
            </Text>
          </View>
          
          <TouchableOpacity 
            style={[
              styles.toggleButton, 
              { backgroundColor: isBatterySaving ? Colors.gold : 'transparent' }
            ]} 
            onPress={() => setIsBatterySaving(!isBatterySaving)}
          >
            <Text style={[
              styles.toggleButtonText,
              { color: isBatterySaving ? Colors.bgDark : Colors.gold }
            ]}>
              {isBatterySaving ? 'Pil Tasarrufu Aktif' : 'Pil Tasarrufu'}
            </Text>
          </TouchableOpacity>
          
          {/* Pil Tasarrufu Aktifse Konum Sıklığını Azalt */}
          {isBatterySaving && (
            <View style={{ marginTop: 15, padding: 10, backgroundColor: 'rgba(212, 175, 55, 0.1)', borderRadius: 8 }}>
              <Text style={{ color: Colors.gold, fontSize: 12, textAlign: 'center' }}>
                ⚡ Pil tasarrufu modu aktif: Konum güncellemeleri azaltıldı
              </Text>
            </View>
          )}
        </View>
        
        {/* Manuel Konum Gönderimi Butonu */}
        <TouchableOpacity style={styles.locationBtn} onPress={sendLocation}>
          <MaterialCommunityIcons name="map-marker" size={24} color={Colors.white} />
          <Text style={styles.locationBtnText}>Konumumu Gönder</Text>
        </TouchableOpacity>
        
        {locationStatus ? (
          <Text style={{ 
            color: locationStatus.includes('başarıyla') ? Colors.gold : '#ff6b6b', 
            textAlign: 'center', 
            marginTop: 10,
            fontSize: 14
          }}>
            {locationStatus}
          </Text>
        ) : null}

        {/* Otomatik Konum Takibi Butonları */}
        <TouchableOpacity 
          style={[
            styles.locationBtn, 
            { backgroundColor: isAutoLocationActive ? '#ff6b6b' : Colors.gold }
          ]} 
          onPress={isAutoLocationActive ? stopAutoLocationTracking : startAutoLocationTracking}
        >
          <MaterialCommunityIcons 
            name={isAutoLocationActive ? "stop-circle" : "play-circle"} 
            size={24} 
            color={Colors.white} 
          />
          <Text style={styles.locationBtnText}>
            {isAutoLocationActive ? 'Otomatik Takibi Durdur' : 'Otomatik Takibi Başlat'}
          </Text>
        </TouchableOpacity>
        
        {autoLocationStatus ? (
          <Text style={{ 
            color: autoLocationStatus.includes('başarıyla') ? Colors.gold : '#ff6b6b', 
            textAlign: 'center', 
            marginTop: 10,
            fontSize: 14
          }}>
            {autoLocationStatus}
          </Text>
        ) : null}
      </ScrollView>
    </SafeAreaView>
  );

  const LeadsTab = () => (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.userName}>MÜŞTERİ ADAYLARI</Text>
        <TouchableOpacity style={styles.logoutBtn} onPress={() => fetchLeads(AsyncStorage.getItem('userToken'))}>
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

  const AppointmentsTab = () => (
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

  const BottomTabBar = () => (
    <View style={styles.tabBar}>
      <TabItem icon="view-dashboard" label="Özet" active={currentTab === 'Dashboard'} onClick={() => setCurrentTab('Dashboard')} />
      <TabItem icon="account-group" label="Adaylar" active={currentTab === 'Leads'} onClick={() => setCurrentTab('Leads')} />
      <TabItem icon="calendar-clock" label="Randevu" active={currentTab === 'Appointments'} onClick={() => setCurrentTab('Appointments')} />
      {userRole === 'admin' && (
        <TabItem icon="security" label="Yönetim" active={currentTab === 'Team'} onClick={() => setCurrentTab('Team')} />
      )}
    </View>
  );

  const TabItem = ({ icon, label, active, onClick }) => (
    <TouchableOpacity style={styles.tabItem} onPress={onClick}>
      <MaterialCommunityIcons name={icon} size={24} color={active ? Colors.gold : Colors.textMuted} />
      <Text style={[styles.tabLabel, { color: active ? Colors.gold : Colors.textMuted }]}>{label}</Text>
    </TouchableOpacity>
  );

  const renderContent = () => {
    switch (currentTab) {
      case 'Leads': return <LeadsTab />;
      case 'Appointments': return <AppointmentsTab />;
      case 'Team': return <TeamTab />;
      default: return <DashboardScreen />;
    }
  };

  return (
    <View style={styles.mainContainer}>
      <StatusBar barStyle="light-content" />
      {!isLoggedIn ? (
        currentScreen === 'Login' ? <LoginScreen /> : <ForgotScreen />
      ) : (
        <>
          {renderContent()}
          <BottomTabBar />
        </>
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
  locationBtn: {
    backgroundColor: Colors.gold,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 15,
    borderRadius: 12,
    marginTop: 20,
    shadowColor: Colors.gold,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  locationBtnText: {
    color: Colors.bgDark,
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 10,
    letterSpacing: 1,
  },
  batterySection: {
    backgroundColor: Colors.bgCard,
    padding: 20,
    borderRadius: 15,
    marginTop: 20,
    borderWidth: 1,
    borderColor: 'rgba(212, 175, 55, 0.1)',
  },
  batteryInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  batteryText: {
    color: Colors.white,
    fontSize: 16,
    marginLeft: 10,
  },
  toggleButton: {
    borderWidth: 1,
    borderColor: Colors.gold,
    borderRadius: 12,
    paddingVertical: 10,
    alignItems: 'center',
  },
  toggleButtonText: {
    fontSize: 14,
    fontWeight: '600',
  },
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

