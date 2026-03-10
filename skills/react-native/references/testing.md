# Testing Guide

Complete guide to testing React Native applications.

## Table of Contents

- [Jest Setup](#jest-setup)
- [Component Testing](#component-testing)
- [Integration Testing](#integration-testing)
- [E2E Testing](#e2e-testing)
- [Testing Patterns](#testing-patterns)

## Jest Setup

Jest is the default testing framework for React Native.

### Installation

```bash
npm install --save-dev jest @testing-library/react-native @testing-library/jest-native
```

### Configuration

Create `jest.config.js`:

```js
module.exports = {
  preset: 'react-native',
  setupFilesAfterEnv: ['@testing-library/jest-native/extend-expect'],
  transformIgnorePatterns: [
    'node_modules/(?!(react-native|@react-native|@react-navigation|expo|@expo)/)',
  ],
};
```

### Package.json Script

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch"
  }
}
```

## Component Testing

Test React Native components with React Native Testing Library.

### Basic Component Test

```tsx
import { render, screen, fireEvent } from '@testing-library/react-native';
import { Button } from './Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button title="Click me" />);
    expect(screen.getByText('Click me')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    render(<Button title="Click me" onPress={onPress} />);
    
    fireEvent.press(screen.getByText('Click me'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });
});
```

### Testing Styles

```tsx
import { render } from '@testing-library/react-native';
import { MyComponent } from './MyComponent';

it('applies correct styles', () => {
  const { getByTestId } = render(<MyComponent />);
  const container = getByTestId('container');
  
  expect(container).toHaveStyle({
    padding: 16,
    backgroundColor: '#fff',
  });
});
```

### Testing Navigation

```tsx
import { render } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { HomeScreen } from './HomeScreen';

const renderWithNavigation = (component) => {
  return render(
    <NavigationContainer>
      {component}
    </NavigationContainer>
  );
};

it('navigates to details screen', () => {
  const { getByText } = renderWithNavigation(<HomeScreen />);
  fireEvent.press(getByText('Go to Details'));
  // Assert navigation occurred
});
```

### Mocking Native Modules

```tsx
jest.mock('react-native', () => {
  const RN = jest.requireActual('react-native');
  return {
    ...RN,
    NativeModules: {
      ...RN.NativeModules,
      MyModule: {
        hello: jest.fn(() => Promise.resolve('Hello')),
      },
    },
  };
});
```

## Integration Testing

Test multiple components working together.

### Testing API Integration

```tsx
import { render, waitFor } from '@testing-library/react-native';
import { UserList } from './UserList';

// Mock API
jest.mock('./api', () => ({
  getUsers: jest.fn(() => Promise.resolve([
    { id: 1, name: 'John' },
    { id: 2, name: 'Jane' },
  ])),
}));

it('displays users from API', async () => {
  const { getByText } = render(<UserList />);
  
  await waitFor(() => {
    expect(getByText('John')).toBeTruthy();
    expect(getByText('Jane')).toBeTruthy();
  });
});
```

### Testing State Management

```tsx
import { render } from '@testing-library/react-native';
import { Provider } from 'react-redux';
import { store } from './store';
import { Counter } from './Counter';

const renderWithStore = (component) => {
  return render(
    <Provider store={store}>
      {component}
    </Provider>
  );
};

it('updates counter on button press', () => {
  const { getByText } = renderWithStore(<Counter />);
  fireEvent.press(getByText('Increment'));
  expect(getByText('1')).toBeTruthy();
});
```

## E2E Testing

End-to-end testing with Detox.

### Installation

```bash
npm install --save-dev detox
npm install --save-dev jest-circus
```

### Configuration

Create `.detoxrc.js`:

```js
module.exports = {
  testRunner: {
    args: {
      '$0': 'jest',
      config: 'e2e/jest.config.js'
    },
    jest: {
      setupTimeout: 120000
    }
  },
  apps: {
    'ios.debug': {
      type: 'ios.app',
      binaryPath: 'ios/build/Build/Products/Debug-iphonesimulator/MyApp.app',
      build: 'xcodebuild -workspace ios/MyApp.xcworkspace -scheme MyApp -configuration Debug -sdk iphonesimulator -derivedDataPath ios/build'
    },
    'android.debug': {
      type: 'android.apk',
      binaryPath: 'android/app/build/outputs/apk/debug/app-debug.apk',
      build: 'cd android && ./gradlew assembleDebug assembleAndroidTest -DtestBuildType=debug'
    }
  },
  devices: {
    simulator: {
      type: 'ios.simulator',
      device: {
        type: 'iPhone 14'
      }
    },
    emulator: {
      type: 'android.emulator',
      device: {
        avdName: 'Pixel_4_API_30'
      }
    }
  },
  configurations: {
    'ios.sim.debug': {
      device: 'simulator',
      app: 'ios.debug'
    },
    'android.emu.debug': {
      device: 'emulator',
      app: 'android.debug'
    }
  }
};
```

### E2E Test Example

```tsx
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it('should login successfully', async () => {
    await element(by.id('email-input')).typeText('user@example.com');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();
    
    await expect(element(by.id('home-screen'))).toBeVisible();
  });
});
```

## Testing Patterns

### Test Utilities

```tsx
// test-utils.tsx
import { render } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { Provider } from 'react-redux';
import { store } from './store';

export function renderWithProviders(ui) {
  return render(
    <Provider store={store}>
      <NavigationContainer>
        {ui}
      </NavigationContainer>
    </Provider>
  );
}
```

### Mocking Async Storage

```tsx
import AsyncStorage from '@react-native-async-storage/async-storage';

jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock')
);
```

### Snapshot Testing

```tsx
import renderer from 'react-test-renderer';
import { MyComponent } from './MyComponent';

it('matches snapshot', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

### Testing Hooks

```tsx
import { renderHook, act } from '@testing-library/react-native';
import { useCounter } from './useCounter';

it('increments counter', () => {
  const { result } = renderHook(() => useCounter());
  
  act(() => {
    result.current.increment();
  });
  
  expect(result.current.count).toBe(1);
});
```

## Best Practices

1. **Test Behavior, Not Implementation**: Test what users see and do
2. **Use Test IDs Sparingly**: Prefer text and accessibility labels
3. **Mock External Dependencies**: Mock APIs, native modules, navigation
4. **Keep Tests Fast**: Use unit tests for most cases, E2E for critical flows
5. **Test Edge Cases**: Empty states, error states, loading states
6. **Maintain Test Coverage**: Aim for 80%+ coverage on critical paths
