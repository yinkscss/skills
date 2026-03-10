# Styling Guide

Complete guide to styling React Native applications.

## Table of Contents

- [StyleSheet API](#stylesheet-api)
- [Responsive Design](#responsive-design)
- [Platform-Specific Styles](#platform-specific-styles)
- [Theming](#theming)
- [Dynamic Styles](#dynamic-styles)
- [Best Practices](#best-practices)

## StyleSheet API

Use StyleSheet.create for better performance than inline styles.

### Basic Usage

```tsx
import { StyleSheet, View, Text } from 'react-native';

function MyComponent() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Hello</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
});
```

### Combining Styles

```tsx
<View style={[styles.container, styles.centered]}>
<View style={[styles.container, { backgroundColor: 'red' }]}>
```

### Conditional Styles

```tsx
<View style={[
  styles.container,
  isActive && styles.active,
  { opacity: disabled ? 0.5 : 1 }
]}>
```

## Responsive Design

Handle different screen sizes and orientations.

### Dimensions API

```tsx
import { Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    width: width * 0.9,
    padding: width < 400 ? 8 : 16,
  },
});
```

### Responsive Hook

```tsx
import { useState, useEffect } from 'react';
import { Dimensions } from 'react-native';

function useDimensions() {
  const [dimensions, setDimensions] = useState(Dimensions.get('window'));
  
  useEffect(() => {
    const subscription = Dimensions.addEventListener('change', ({ window }) => {
      setDimensions(window);
    });
    
    return () => subscription?.remove();
  }, []);
  
  return dimensions;
}

function MyComponent() {
  const { width, height } = useDimensions();
  const isTablet = width >= 768;
  
  return (
    <View style={[styles.container, isTablet && styles.tabletContainer]}>
      {/* content */}
    </View>
  );
}
```

### Percentage-Based Sizing

```tsx
const styles = StyleSheet.create({
  container: {
    width: '100%',
    height: '50%',
    paddingHorizontal: '5%',
  },
});
```

## Platform-Specific Styles

Apply different styles for iOS and Android.

### Platform API

```tsx
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === 'ios' ? 20 : 0,
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
      },
      android: {
        elevation: 5,
      },
    }),
  },
});
```

### Platform-Specific Files

Create separate files:
- `Component.ios.tsx`
- `Component.android.tsx`

React Native automatically loads the correct file.

## Theming

Create a consistent theme system.

### Theme Object

```tsx
export const theme = {
  colors: {
    primary: '#007AFF',
    secondary: '#5856D6',
    background: '#FFFFFF',
    text: '#000000',
    error: '#FF3B30',
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  typography: {
    h1: { fontSize: 32, fontWeight: 'bold' },
    h2: { fontSize: 24, fontWeight: 'bold' },
    body: { fontSize: 16 },
  },
};
```

### Using Theme

```tsx
import { theme } from './theme';

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.background,
    padding: theme.spacing.md,
  },
  title: {
    ...theme.typography.h1,
    color: theme.colors.text,
  },
});
```

### Dark Mode Theme

```tsx
export const lightTheme = {
  colors: {
    background: '#FFFFFF',
    text: '#000000',
  },
};

export const darkTheme = {
  colors: {
    background: '#000000',
    text: '#FFFFFF',
  },
};

function useTheme() {
  const colorScheme = useColorScheme();
  return colorScheme === 'dark' ? darkTheme : lightTheme;
}
```

## Dynamic Styles

Create styles based on component state or props.

### Function-Based Styles

```tsx
function getStyles(isActive: boolean, size: 'small' | 'large') {
  return StyleSheet.create({
    button: {
      backgroundColor: isActive ? '#007AFF' : '#CCCCCC',
      padding: size === 'large' ? 16 : 8,
    },
  });
}

function Button({ isActive, size }) {
  const styles = getStyles(isActive, size);
  return <View style={styles.button} />;
}
```

### useMemo for Performance

```tsx
import { useMemo } from 'react';

function Button({ isActive, size }) {
  const styles = useMemo(
    () => StyleSheet.create({
      button: {
        backgroundColor: isActive ? '#007AFF' : '#CCCCCC',
        padding: size === 'large' ? 16 : 8,
      },
    }),
    [isActive, size]
  );
  
  return <View style={styles.button} />;
}
```

## UI Component Libraries

For production apps, consider using established component libraries for consistent, accessible UI components.

### NativeWind (Tailwind CSS for React Native)

Utility-first CSS framework for React Native:

```bash
npm install nativewind
npm install --save-dev tailwindcss
npx tailwindcss init
```

Configure `tailwind.config.js`:

```js
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Usage:

```tsx
import { View, Text } from 'react-native';
import '../global.css';

export function MyComponent() {
  return (
    <View className="flex-1 items-center justify-center bg-white">
      <Text className="text-2xl font-bold text-gray-900">Hello</Text>
    </View>
  );
}
```

### shadcn-native

React Native port of shadcn/ui components. Provides accessible, customizable components:

```bash
# Install NativeWind first (required dependency)
npm install nativewind
npm install --save-dev tailwindcss

# Install shadcn-native
npm install shadcn-native

# Initialize
npx shadcn-native@latest init
```

Usage:

```tsx
import { Button } from 'shadcn-native';

export function MyComponent() {
  return (
    <Button onPress={() => {}}>
      Click me
    </Button>
  );
}
```

**Components available**: Button, Card, Input, Select, Dialog, Sheet, and more. See [shadcn-native documentation](https://shadcn-native.moveinready.casa) for full component list.

### Tamagui

High-performance UI library with excellent developer experience:

```bash
npm install @tamagui/core @tamagui/config
```

### React Native Paper

Material Design components for React Native:

```bash
npm install react-native-paper react-native-vector-icons
```

## Best Practices

### 1. Use StyleSheet.create

Always use StyleSheet.create instead of plain objects for better performance.

### 2. Extract Common Styles

```tsx
const commonStyles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
});
```

### 3. Use Flexbox

```tsx
const styles = StyleSheet.create({
  container: {
    flex: 1, // Takes available space
    flexDirection: 'row', // or 'column'
    justifyContent: 'space-between',
    alignItems: 'center',
  },
});
```

### 4. Avoid Inline Styles for Static Styles

```tsx
// ❌ Bad
<View style={{ padding: 16 }}>

// ✅ Good
<View style={styles.container}>
```

### 5. Use Constants for Repeated Values

```tsx
const SPACING = 16;
const BORDER_RADIUS = 8;

const styles = StyleSheet.create({
  container: {
    padding: SPACING,
    borderRadius: BORDER_RADIUS,
  },
});
```

### 6. Optimize Image Sizes

Use appropriate image sizes for different screen densities:

```tsx
<Image
  source={{
    uri: 'image.jpg',
    width: 200,
    height: 200,
  }}
  style={styles.image}
/>
```
