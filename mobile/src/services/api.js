import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = 'https://imzaemlak.com';

const getAuthToken = async () => {
  return await AsyncStorage.getItem('userToken');
};

export const login = async (username, password) => {
  const response = await fetch(`${API_URL}/api/mobile/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, app_type: 'investment' }),
  });
  return await response.json();
};

export const requestPasswordReset = async (email) => {
  const response = await fetch(`${API_URL}/api/auth/request-reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  });
  return await response.json();
};

export const getPortfolios = async () => {
  const token = await getAuthToken();
  const response = await fetch(`${API_URL}/api/portfoyler`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  return await response.json();
};

export const getLeads = async () => {
  const token = await getAuthToken();
  const response = await fetch(`${API_URL}/api/leads`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  return await response.json();
};

export const getAppointments = async () => {
  const token = await getAuthToken();
  const response = await fetch(`${API_URL}/api/appointments`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  return await response.json();
};

export const sendLocationUpdate = async (latitude, longitude, auto = false) => {
  const token = await getAuthToken();
  const response = await fetch(`${API_URL}/api/tracking/location`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      latitude,
      longitude,
      timestamp: new Date().toISOString(),
      auto,
    }),
  });
  return await response.json();
};
