import React, { useContext } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, TextInput } from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';
import { AppContext } from '../context/AppContext';

const LoginScreen = ({ navigation }) => {
  const {
    username,
    setUsername,
    password,
    setPassword,
    handleLogin,
  } = useContext(AppContext);

  return (
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

      <TouchableOpacity onPress={() => navigation.navigate('ForgotPassword')}>
        <Text style={styles.linkText}>Şifremi Unuttum</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
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
.
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
});

export default LoginScreen;