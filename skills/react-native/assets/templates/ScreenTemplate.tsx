import { View, Text, StyleSheet, SafeAreaView } from 'react-native';

export function ScreenTemplate() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Screen Title</Text>
        <Text style={styles.subtitle}>Screen content goes here</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    padding: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#000',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
  },
});
