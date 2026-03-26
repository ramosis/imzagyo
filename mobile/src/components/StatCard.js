import React from 'react';
import { StyleSheet, Text, View, Dimensions } from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';

const { width } = Dimensions.get('window');
const isTablet = width > 600;

import React from 'react';
import { StyleSheet, Text, View, Dimensions } from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Colors from '../constants/Colors';
import SkeletonPlaceholder from 'react-native-skeleton-placeholder';

const { width } = Dimensions.get('window');
const isTablet = width > 600;

const StatCard = ({ title, value, icon, isLoading }) => {
  if (isLoading) {
    return (
      <SkeletonPlaceholder>
        <View style={styles.statCard} />
      </SkeletonPlaceholder>
    );
  }

  return (
    <View style={styles.statCard}>
      <MaterialCommunityIcons name={icon} size={28} color={Colors.gold} />
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statLabel}>{title}</Text>
    </View>
  );
};

  const styles = StyleSheet.create({
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
  })

  export default StatCard;

  const styles = StyleSheet.create({
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
  })

  export default StatCard;