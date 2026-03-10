# Native Modules Guide

Guide to integrating native code and modules in React Native apps.

## Table of Contents

- [Expo Modules](#expo-modules)
- [Custom Expo Modules](#custom-expo-modules)
- [Bare React Native Modules](#bare-react-native-modules)
- [Native Module Bridging](#native-module-bridging)
- [When to Use Native Code](#when-to-use-native-code)

## Expo Modules

Expo provides many native modules out of the box. See [expo-apis.md](expo-apis.md) for available modules.

### Installing Expo Modules

```bash
npx expo install expo-camera
npx expo install expo-location
npx expo install expo-notifications
```

Use `expo install` instead of `npm install` to ensure compatible versions.

### Using Expo Modules

```tsx
import { Camera } from 'expo-camera';
import * as Location from 'expo-location';

// Request permissions
const { status } = await Location.requestForegroundPermissionsAsync();

// Use the module
const location = await Location.getCurrentPositionAsync({});
```

## Custom Native Code with CNG

With Continuous Native Generation, add custom native code directly:

1. Generate native projects: `npx expo prebuild`
2. Add native code to `ios/` and `android/` folders
3. Regenerate as needed: `npx expo prebuild --clean`

## Custom Expo Modules

Create reusable custom native modules using Expo Module API.

### Module Structure

```
expo-module/
├── src/
│   └── ExpoModule.ts
├── ios/
│   └── ExpoModule.swift
├── android/
│   └── ExpoModule.kt
└── package.json
```

### TypeScript Interface

```tsx
// src/ExpoModule.ts
import { NativeModulesProxy, EventEmitter } from 'expo-modules-core';

export default NativeModulesProxy.ExpoModule;
```

### iOS Implementation

```swift
// ios/ExpoModule.swift
import ExpoModulesCore

public class ExpoModule: Module {
  public func definition() -> ModuleDefinition {
    Name("ExpoModule")
    
    Function("hello") { () -> String in
      return "Hello from native!"
    }
    
    AsyncFunction("doSomethingAsync") { (promise: Promise) in
      // Async work
      promise.resolve("Done")
    }
  }
}
```

### Android Implementation

```kotlin
// android/ExpoModule.kt
package expo.modules.expomodule

import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition

class ExpoModule : Module() {
  override fun definition() = ModuleDefinition {
    Name("ExpoModule")
    
    Function("hello") {
      return "Hello from native!"
    }
    
    AsyncFunction("doSomethingAsync") { promise: Promise ->
      // Async work
      promise.resolve("Done")
    }
  }
}
```

## Bare React Native Modules

For bare React Native projects, create native modules directly.

### iOS Native Module

```objc
// MyModule.h
#import <React/RCTBridgeModule.h>

@interface MyModule : NSObject <RCTBridgeModule>
@end

// MyModule.m
#import "MyModule.h"

@implementation MyModule

RCT_EXPORT_MODULE();

RCT_EXPORT_METHOD(hello:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)
{
  resolve(@"Hello from iOS!");
}

@end
```

### Android Native Module

```java
// MyModule.java
package com.myapp;

import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;
import com.facebook.react.bridge.Promise;

public class MyModule extends ReactContextBaseJavaModule {
  @Override
  public String getName() {
    return "MyModule";
  }

  @ReactMethod
  public void hello(Promise promise) {
    promise.resolve("Hello from Android!");
  }
}
```

### JavaScript Bridge

```tsx
import { NativeModules } from 'react-native';

const { MyModule } = NativeModules;

MyModule.hello().then((result) => {
  console.log(result);
});
```

## Native Module Bridging

Bridge native modules to JavaScript.

### Event Emitters

```tsx
import { NativeEventEmitter, NativeModules } from 'react-native';

const { MyModule } = NativeModules;
const emitter = new NativeEventEmitter(MyModule);

emitter.addListener('EventName', (data) => {
  console.log('Event received:', data);
});
```

### Callbacks

```tsx
// Native side
RCT_EXPORT_METHOD(doSomething:(NSDictionary *)options
                  callback:(RCTResponseSenderBlock)callback)
{
  callback(@[@"success", @"result"]);
}

// JavaScript side
MyModule.doSomething({}, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

## When to Use Native Code

### Use Expo Modules When:
- Feature is available in Expo SDK
- You want managed workflow benefits
- Quick development is priority

### Use Custom Modules When:
- Feature not in Expo SDK
- Need platform-specific optimizations
- Require direct native API access

### Continuous Native Generation (CNG)

Modern Expo uses CNG - native projects are generated on-demand:

```bash
# Generate native projects
npx expo prebuild

# Clean and regenerate
npx expo prebuild --clean
```

This creates `ios/` and `android/` directories. You can:
- Add custom native code
- Regenerate when needed
- Keep using Expo tooling

**No need to eject** - CNG allows you to add native code while maintaining Expo workflow benefits.

## Best Practices

1. **Prefer Expo Modules**: Use Expo modules when possible
2. **Check Community**: Look for existing modules before creating custom ones
3. **Documentation**: Document native module APIs clearly
4. **Error Handling**: Handle native errors gracefully
5. **Testing**: Test on both iOS and Android
6. **Performance**: Consider performance implications of native bridges
