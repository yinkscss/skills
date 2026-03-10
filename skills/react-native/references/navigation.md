# React Navigation Guide

Complete guide to navigation in React Native apps using React Navigation.

## Table of Contents

- [Installation](#installation)
- [Stack Navigation](#stack-navigation)
- [Tab Navigation](#tab-navigation)
- [Drawer Navigation](#drawer-navigation)
- [Nested Navigators](#nested-navigators)
- [Deep Linking](#deep-linking)
- [Navigation Patterns](#navigation-patterns)

## Installation

Install React Navigation packages:

```bash
npm install @react-navigation/native
npx expo install react-native-screens react-native-safe-area-context
```

For specific navigator types:

```bash
# Stack Navigator
npm install @react-navigation/native-stack

# Tab Navigator
npm install @react-navigation/bottom-tabs

# Drawer Navigator
npm install @react-navigation/drawer
npx expo install react-native-gesture-handler react-native-reanimated
```

## Stack Navigation

Stack navigation provides a screen stack where new screens are pushed on top.

### Basic Setup

```tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { HomeScreen } from './screens/HomeScreen';
import { DetailsScreen } from './screens/DetailsScreen';

const Stack = createNativeStackNavigator();

export function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Navigation Options

```tsx
<Stack.Navigator
  screenOptions={{
    headerStyle: { backgroundColor: '#f4511e' },
    headerTintColor: '#fff',
    headerTitleStyle: { fontWeight: 'bold' },
  }}
>
  <Stack.Screen
    name="Home"
    component={HomeScreen}
    options={{ title: 'My Home' }}
  />
</Stack.Navigator>
```

### Navigating Between Screens

```tsx
import { useNavigation } from '@react-navigation/native';

function HomeScreen() {
  const navigation = useNavigation();
  
  return (
    <Button
      title="Go to Details"
      onPress={() => navigation.navigate('Details', { itemId: 86 })}
    />
  );
}

function DetailsScreen({ route }) {
  const { itemId } = route.params;
  // Use itemId
}
```

### Passing Parameters

```tsx
navigation.navigate('Details', {
  itemId: 86,
  otherParam: 'anything you want here',
});
```

## Tab Navigation

Bottom tab navigation for apps with multiple main sections.

### Basic Setup

```tsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { HomeScreen } from './screens/HomeScreen';
import { SettingsScreen } from './screens/SettingsScreen';

const Tab = createBottomTabNavigator();

export function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Home" component={HomeScreen} />
        <Tab.Screen name="Settings" component={SettingsScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

### Custom Tab Icons

```tsx
import { Ionicons } from '@expo/vector-icons';

<Tab.Navigator
  screenOptions={({ route }) => ({
    tabBarIcon: ({ focused, color, size }) => {
      let iconName;
      
      if (route.name === 'Home') {
        iconName = focused ? 'home' : 'home-outline';
      } else if (route.name === 'Settings') {
        iconName = focused ? 'settings' : 'settings-outline';
      }
      
      return <Ionicons name={iconName} size={size} color={color} />;
    },
    tabBarActiveTintColor: 'tomato',
    tabBarInactiveTintColor: 'gray',
  })}
>
```

## Drawer Navigation

Side drawer navigation for apps with many screens.

### Basic Setup

```tsx
import { createDrawerNavigator } from '@react-navigation/drawer';
import { HomeScreen } from './screens/HomeScreen';
import { ProfileScreen } from './screens/ProfileScreen';

const Drawer = createDrawerNavigator();

export function App() {
  return (
    <NavigationContainer>
      <Drawer.Navigator>
        <Drawer.Screen name="Home" component={HomeScreen} />
        <Drawer.Screen name="Profile" component={ProfileScreen} />
      </Drawer.Navigator>
    </NavigationContainer>
  );
}
```

### Custom Drawer Content

```tsx
import { DrawerContentScrollView, DrawerItemList } from '@react-navigation/drawer';

function CustomDrawerContent(props) {
  return (
    <DrawerContentScrollView {...props}>
      <DrawerItemList {...props} />
    </DrawerContentScrollView>
  );
}

<Drawer.Navigator drawerContent={(props) => <CustomDrawerContent {...props} />}>
```

## Nested Navigators

Combine different navigator types for complex navigation structures.

### Tabs Inside Stack

```tsx
const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function HomeTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Feed" component={FeedScreen} />
      <Tab.Screen name="Messages" component={MessagesScreen} />
    </Tab.Navigator>
  );
}

export function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeTabs} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## Deep Linking

Configure deep linking to open specific screens from URLs.

### Configuration

```tsx
import { Linking } from 'react-native';

const linking = {
  prefixes: ['myapp://', 'https://myapp.com'],
  config: {
    screens: {
      Home: '',
      Details: 'details/:id',
    },
  },
};

<NavigationContainer linking={linking}>
```

### Handling Deep Links

```tsx
useEffect(() => {
  const subscription = Linking.addEventListener('url', handleDeepLink);
  return () => subscription.remove();
}, []);
```

## Navigation Patterns

### Type Safety with TypeScript

```tsx
export type RootStackParamList = {
  Home: undefined;
  Details: { itemId: number };
  Profile: { userId: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();
```

### Header Buttons

```tsx
<Stack.Screen
  name="Details"
  component={DetailsScreen}
  options={({ navigation }) => ({
    headerRight: () => (
      <Button
        onPress={() => navigation.navigate('Settings')}
        title="Settings"
      />
    ),
  })}
/>
```

### Screen Options Per Screen

```tsx
function DetailsScreen({ navigation }) {
  React.useLayoutEffect(() => {
    navigation.setOptions({
      headerRight: () => <Button onPress={() => {}} title="Save" />,
    });
  }, [navigation]);
}
```

### Navigation Events

```tsx
import { useFocusEffect } from '@react-navigation/native';

function ProfileScreen() {
  useFocusEffect(
    React.useCallback(() => {
      // Screen is focused, refresh data
      return () => {
        // Screen is unfocused, cleanup
      };
    }, [])
  );
}
```
