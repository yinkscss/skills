# State Management Guide

Guide to managing state in React Native applications.

## Table of Contents

- [Context API](#context-api)
- [Zustand](#zustand)
- [Redux Toolkit](#redux-toolkit)
- [Choosing a Solution](#choosing-a-solution)

## Context API

Built-in React solution for simple global state.

### Basic Setup

```tsx
import { createContext, useContext, useState } from 'react';

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  
  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
```

### Usage

```tsx
function App() {
  return (
    <ThemeProvider>
      <HomeScreen />
    </ThemeProvider>
  );
}

function HomeScreen() {
  const { theme, toggleTheme } = useTheme();
  return <Button title="Toggle Theme" onPress={toggleTheme} />;
}
```

### Performance Optimization

Split contexts to avoid unnecessary re-renders:

```tsx
const ThemeContext = createContext('light');
const ThemeUpdateContext = createContext(() => {});

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  return (
    <ThemeContext.Provider value={theme}>
      <ThemeUpdateContext.Provider value={setTheme}>
        {children}
      </ThemeUpdateContext.Provider>
    </ThemeContext.Provider>
  );
}
```

## Zustand

Lightweight state management library, great for medium complexity.

### Installation

```bash
npm install zustand
```

### Basic Store

```tsx
import { create } from 'zustand';

interface BearState {
  bears: number;
  increase: (by: number) => void;
}

export const useBearStore = create<BearState>((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
}));
```

### Usage in Components

```tsx
function BearCounter() {
  const bears = useBearStore((state) => state.bears);
  const increase = useBearStore((state) => state.increase);
  
  return (
    <View>
      <Text>{bears} bears around here...</Text>
      <Button title="Add bear" onPress={() => increase(1)} />
    </View>
  );
}
```

### Async Actions

```tsx
import { create } from 'zustand';

interface UserState {
  user: User | null;
  loading: boolean;
  fetchUser: (id: string) => Promise<void>;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  loading: false,
  fetchUser: async (id) => {
    set({ loading: true });
    try {
      const user = await api.getUser(id);
      set({ user, loading: false });
    } catch (error) {
      set({ loading: false });
    }
  },
}));
```

### Persistence

```tsx
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const useStore = create(
  persist(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
    }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

## Redux Toolkit

Powerful state management for complex applications.

### Installation

```bash
npm install @reduxjs/toolkit react-redux
```

### Store Setup

```tsx
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### Slice

```tsx
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CounterState {
  value: number;
}

const initialState: CounterState = {
  value: 0,
};

export const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;
```

### Provider Setup

```tsx
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
  return (
    <Provider store={store}>
      <HomeScreen />
    </Provider>
  );
}
```

### Usage with Hooks

```tsx
import { useSelector, useDispatch } from 'react-redux';
import { increment } from './counterSlice';

function Counter() {
  const count = useSelector((state: RootState) => state.counter.value);
  const dispatch = useDispatch();
  
  return (
    <View>
      <Text>{count}</Text>
      <Button title="Increment" onPress={() => dispatch(increment())} />
    </View>
  );
}
```

### Async Thunks

```tsx
import { createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId: string) => {
    const response = await api.getUser(userId);
    return response.data;
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState: { user: null, loading: false },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      });
  },
});
```

## Choosing a Solution

### Context API
- ✅ Simple global state
- ✅ Theme, user preferences
- ✅ Small apps
- ❌ Performance issues with frequent updates
- ❌ Complex state logic

### Zustand
- ✅ Medium complexity
- ✅ Simple API
- ✅ Good performance
- ✅ Built-in persistence
- ❌ Less ecosystem than Redux

### Redux Toolkit
- ✅ Complex state management
- ✅ Time-travel debugging
- ✅ Middleware support
- ✅ Large ecosystem
- ❌ More boilerplate
- ❌ Steeper learning curve
