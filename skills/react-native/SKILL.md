---
name: react-native
description: Comprehensive guide for React Native app development using Expo. Use when building mobile applications for iOS and Android, including project setup, navigation, state management, native module integration, testing, and deployment. Covers Expo managed workflow, React Navigation, state management patterns, styling, performance optimization, and EAS Build deployment.
license: Complete terms in LICENSE.txt
---

# React Native App Development

Build production-ready mobile applications for iOS and Android using React Native with Expo. This skill covers the complete development lifecycle from project initialization to app store deployment.

## Overview

React Native enables building native mobile apps using JavaScript and React. Expo provides a managed workflow that simplifies development, building, and deployment. Use this skill when creating new mobile apps, adding features to existing apps, or optimizing React Native applications.

**When to use Expo vs Bare React Native:**
- **Expo (recommended)**: Use for most apps. Provides managed workflow, OTA updates, easy builds, and access to Expo SDK APIs.
- **Bare React Native**: Use only when you need custom native code not available in Expo modules or require direct native module access.

## Quick Start

### Project Setup

Initialize a new Expo project:

```bash
npx create-expo-app@latest MyApp --template blank-typescript
```

Or use the helper script:

```bash
python scripts/init_expo_project.py MyApp --typescript
```

**Important**: Modern Expo uses Continuous Native Generation (CNG). Native projects (`ios/` and `android/` folders) are generated on-demand when you run `npx expo prebuild` or `npx expo run:ios/android`. This keeps your project clean and allows easy regeneration.

### Development Workflow

**Recommended: Development Builds**

For production apps, use development builds instead of Expo Go:

```bash
# Generate native projects (first time)
npx expo prebuild

# Run on iOS
npx expo run:ios

# Run on Android
npx expo run:android
```

**Expo Go (Quick Testing)**

For quick testing without native code:

```bash
npx expo start
```

- Press `i` for iOS simulator
- Press `a` for Android emulator
- Scan QR code with Expo Go app on physical device

**Note**: Expo Go has limitations. Use development builds for apps with custom native modules or production features.

## Core Development Patterns

### Component Structure

Create reusable components following this pattern:

```tsx
import { View, Text, StyleSheet } from 'react-native';

interface MyComponentProps {
  title: string;
}

export function MyComponent({ title }: MyComponentProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
  },
});
```

See `assets/templates/ComponentTemplate.tsx` for a complete template.

### Navigation

React Navigation is the standard navigation library. See [navigation.md](references/navigation.md) for:
- Stack navigation
- Tab navigation
- Drawer navigation
- Deep linking
- Navigation patterns

Quick setup:

```bash
npm install @react-navigation/native @react-navigation/native-stack
npx expo install react-native-screens react-native-safe-area-context react-native-gesture-handler
```

**Important**: Always use `npx expo install` for React Native packages to ensure compatibility with your Expo SDK version.

Or use the helper script:

```bash
python scripts/setup_navigation.py
```

### State Management

Choose based on complexity:

- **Context API**: Simple global state, theme, user preferences
- **Zustand**: Lightweight, great for medium complexity
- **Redux Toolkit**: Complex state, time-travel debugging, middleware

See [state-management.md](references/state-management.md) for patterns and examples.

### Styling

Use StyleSheet for performance. See [styling.md](references/styling.md) for:
- Responsive design patterns
- Platform-specific styles
- Theming
- Dynamic styles

**UI Component Libraries:**

For modern, accessible UI components, consider:

- **NativeWind** (Tailwind CSS for React Native): Popular styling solution
- **shadcn-native**: React Native port of shadcn/ui components (see [styling.md](references/styling.md) for setup)
- **Tamagui**: High-performance UI library
- **React Native Paper**: Material Design components

See [styling.md](references/styling.md) for component library integration patterns.

### Platform-Specific Code

Use Platform API for platform differences:

```tsx
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === 'ios' ? 20 : 0,
  },
});
```

For platform-specific files:
- `Component.ios.tsx` - iOS only
- `Component.android.tsx` - Android only

## Native Modules & Expo APIs

### Expo Modules

Expo provides many native modules out of the box. See [expo-apis.md](references/expo-apis.md) for:
- Camera
- Location
- Notifications
- File System
- SQLite
- And more

Install with:

```bash
npx expo install expo-camera
```

### Custom Native Code

With Expo's Continuous Native Generation (CNG), you can add custom native code without ejecting:

1. Generate native projects: `npx expo prebuild`
2. Add native code to `ios/` and `android/` folders
3. Regenerate as needed: `npx expo prebuild --clean`

See [native-modules.md](references/native-modules.md) for:
- Creating custom Expo modules
- Adding native code with CNG
- Native module bridging
- When to use custom native modules

## Testing

Set up testing with Jest and React Native Testing Library:

```bash
npm install --save-dev jest @testing-library/react-native
```

See [testing.md](references/testing.md) for:
- Unit testing components
- Integration testing
- E2E testing with Detox
- Test patterns and best practices

## Building & Deployment

### EAS Build

Expo Application Services (EAS) handles building for iOS and Android:

```bash
npm install -g eas-cli
eas login
eas build:configure
```

Build commands:

```bash
eas build --platform ios
eas build --platform android
eas build --platform all
```

Or use the helper script:

```bash
python scripts/build_and_deploy.py --platform ios
```

See [deployment.md](references/deployment.md) for:
- EAS Build configuration
- App store submission
- OTA updates
- Environment variables
- Build profiles

## Performance Optimization

See [performance.md](references/performance.md) for optimization techniques:

- FlatList optimization
- Image optimization
- Memoization patterns
- Bundle size reduction
- Profiling tools

## Dependency Compatibility

**Always use `npx expo install` for React Native packages** to ensure compatibility with your Expo SDK version:

```bash
# ✅ Correct - ensures compatible versions
npx expo install react-native-screens react-native-safe-area-context

# ❌ Incorrect - may install incompatible versions
npm install react-native-screens
```

Check for dependency issues:

```bash
npx expo doctor
```

This command identifies version mismatches and suggests fixes.

## Best Practices

1. **Use TypeScript**: Type safety catches errors early
2. **Use `expo install`**: Always use `npx expo install` for React Native packages
3. **Organize by feature**: Group related files together
4. **Optimize images**: Use appropriate formats and sizes
5. **Handle errors gracefully**: Implement error boundaries
6. **Test on real devices**: Simulators don't catch all issues
7. **Monitor performance**: Use React DevTools Profiler
8. **Follow accessibility guidelines**: Use semantic components
9. **Use development builds**: Prefer development builds over Expo Go for production features

## Decision Trees

### Choosing State Management

```
Simple state (theme, user prefs) → Context API
Medium complexity (shopping cart, filters) → Zustand
Complex state (time-travel, middleware) → Redux Toolkit
```

### Choosing Navigation Type

```
Simple app (few screens) → Stack Navigation
Tabs needed → Tab Navigation
Side menu needed → Drawer Navigation
Complex (combinations) → Nested Navigators
```

### When to Use Custom Native Code

```
Feature in Expo SDK? → Use Expo module
Feature not in Expo SDK? → Check community modules
Still not available? → Custom native module or eject
```

## Reference Files

Detailed documentation available in `references/`:

- **[navigation.md](references/navigation.md)**: Complete navigation guide
- **[state-management.md](references/state-management.md)**: State management patterns
- **[styling.md](references/styling.md)**: Styling and theming
- **[native-modules.md](references/native-modules.md)**: Native module integration
- **[testing.md](references/testing.md)**: Testing strategies
- **[deployment.md](references/deployment.md)**: Build and deployment
- **[performance.md](references/performance.md)**: Optimization techniques
- **[expo-apis.md](references/expo-apis.md)**: Expo SDK APIs

## Helper Scripts

Automation scripts in `scripts/`:

- **init_expo_project.py**: Initialize new Expo project with common config
- **setup_navigation.py**: Set up React Navigation with common patterns
- **create_component.py**: Generate component templates
- **build_and_deploy.py**: EAS build and deployment helpers

Run scripts with `--help` to see usage. Scripts can be executed directly without loading into context.

## Templates

Code templates in `assets/templates/`:

- **App.tsx**: Main app component with navigation
- **ComponentTemplate.tsx**: Reusable component structure
- **ScreenTemplate.tsx**: Screen component template
- **app.json**: Expo configuration template
- **package.json**: Common dependencies template

Copy and customize templates as needed for new projects.
