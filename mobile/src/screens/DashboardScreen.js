import React from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  Dimensions,
} from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';
import StatCard from '../components/StatCard';

const { width } = Dimensions.get('window');
const isTablet = width > 600;

import React, { useContext } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  Dimensions,
} from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';
import StatCard from '../components/StatCard';
import { AppContext } from '../context/AppContext';

const { width } = Dimensions.get('window');
const isTablet = width > 600;

const DashboardScreen = () => {
  const {
    username,
    handleLogout,
    stats,
    recentPortfolios,
    sendLocation,
    locationStatus,
    isAutoLocationActive,
    stopAutoLocationTracking,
    startAutoLocationTracking,
    autoLocationStatus,
    isLoading,
  } = useContext(AppContext);

  return (
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
          <StatCard title="Aktif Portföy" value={stats.activePortfolio.toString()} icon="home-city" isLoading={isLoading} />
          <StatCard title="Aylık Lead" value={stats.monthlyLeads.toString()} icon="account-group" isLoading={isLoading} />
          <StatCard title="Ort. ROI" value={stats.roi} icon="trending-up" isLoading={isLoading} />
          <StatCard title="Toplam Ciro" value={stats.revenue} icon="currency-try" isLoading={isLoading} />
        </View>

        <Text style={styles.sectionTitle}>Bekleyen Talepler & Portföyler</Text>

        {isLoading ? (
          <SkeletonPlaceholder>
            <View style={{ marginBottom: 12 }}>
              <View style={{ height: 70, borderRadius: 15 }} />
            </View>
            <View style={{ marginBottom: 12 }}>
              <View style={{ height: 70, borderRadius: 15 }} />
            </View>
            <View style={{ marginBottom: 12 }}>
              <View style={{ height: 70, borderRadius: 15 }} />
            </View>
          </SkeletonPlaceholder>
        ) : (
          <>
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
          </>
        )}

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
})

export default DashboardScreen;
