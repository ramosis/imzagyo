import React, { useContext } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, TextInput } from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';
import { AppContext } from '../context/AppContext';

const ForgotScreen = ({ navigation }) => {
  const {
    resetEmail,
    setResetEmail,
    handleForgotPassword,
  } = useContext(AppContext);

  return (
    <View style={styles.authContainer}>
      <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
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
};

const styles = StyleSheet.create({
  authContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    backgroundColor: Colors.bgDark,
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
  backBtn: {
    position: 'absolute',
    top: 60,
    left: 20,
  },
});

export default ForgotScreen;
