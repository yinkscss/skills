import { View, Text, StyleSheet } from 'react-native';

interface ComponentTemplateProps {
  // Add props here
  title?: string;
}

export function ComponentTemplate({ title = 'Component' }: ComponentTemplateProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
});
