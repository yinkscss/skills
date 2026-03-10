# Deployment Guide

Complete guide to building and deploying React Native apps.

## Table of Contents

- [EAS Build Setup](#eas-build-setup)
- [Build Configuration](#build-configuration)
- [iOS Deployment](#ios-deployment)
- [Android Deployment](#android-deployment)
- [OTA Updates](#ota-updates)
- [Environment Variables](#environment-variables)

## EAS Build Setup

Expo Application Services (EAS) handles building for iOS and Android.

### Installation

```bash
npm install -g eas-cli
eas login
```

### Initial Configuration

```bash
eas build:configure
```

This creates `eas.json` with build profiles.

## Build Configuration

### eas.json Structure

```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "env": {
        "API_URL": "https://api.example.com"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890"
      },
      "android": {
        "serviceAccountKeyPath": "./service-account.json",
        "track": "internal"
      }
    }
  }
}
```

### Build Profiles

- **development**: Development builds with dev client
- **preview**: Internal testing builds (APK/IPA)
- **production**: App store builds

### Building

```bash
# Build for specific platform
eas build --platform ios
eas build --platform android
eas build --platform all

# Build with specific profile
eas build --platform ios --profile production

# Local builds (requires native tooling)
eas build --platform ios --local
```

## iOS Deployment

### Prerequisites

1. Apple Developer account ($99/year)
2. App Store Connect app created
3. Certificates and provisioning profiles (handled by EAS)

### Build for iOS

```bash
eas build --platform ios --profile production
```

### Submit to App Store

```bash
eas submit --platform ios
```

Or configure automatic submission in `eas.json`:

```json
{
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "TEAM123456"
      }
    }
  }
}
```

### App Store Connect Setup

1. Create app in App Store Connect
2. Configure app information
3. Set up TestFlight for beta testing
4. Submit for review

### Version Management

Update version in `app.json`:

```json
{
  "expo": {
    "version": "1.0.0",
    "ios": {
      "buildNumber": "1"
    }
  }
}
```

## Android Deployment

### Prerequisites

1. Google Play Developer account ($25 one-time)
2. App created in Google Play Console
3. Service account for automated submission (optional)

### Build for Android

```bash
eas build --platform android --profile production
```

### Submit to Google Play

```bash
eas submit --platform android
```

Or configure automatic submission:

```json
{
  "submit": {
    "production": {
      "android": {
        "serviceAccountKeyPath": "./service-account.json",
        "track": "internal"
      }
    }
  }
}
```

### Google Play Console Setup

1. Create app in Google Play Console
2. Set up app signing
3. Configure store listing
4. Upload to internal/alpha/beta track
5. Submit for production

### Version Management

Update version in `app.json`:

```json
{
  "expo": {
    "version": "1.0.0",
    "android": {
      "versionCode": 1
    }
  }
}
```

## OTA Updates

Over-the-air updates for JavaScript and assets without app store review.

### Setup

```bash
npx expo install expo-updates
```

### Configuration

```json
{
  "expo": {
    "updates": {
      "enabled": true,
      "checkAutomatically": "ON_LOAD",
      "fallbackToCacheTimeout": 0
    }
  }
}
```

### Publishing Updates

```bash
eas update --branch production --message "Bug fixes"
```

### Update Channels

```json
{
  "build": {
    "production": {
      "channel": "production"
    },
    "preview": {
      "channel": "preview"
    }
  }
}
```

Publish to specific channel:

```bash
eas update --branch production --channel production
```

### Update Strategy

- **ON_LOAD**: Check on app start
- **ON_ERROR_RECOVERY**: Check after errors
- **NEVER**: Manual updates only

## Environment Variables

Manage different environments (dev, staging, production).

### Using EAS Secrets

```bash
eas secret:create --name API_URL --value https://api.example.com --scope project
```

Access in code:

```tsx
import Constants from 'expo-constants';

const apiUrl = Constants.expoConfig?.extra?.apiUrl;
```

### Environment-Specific Config

Create `app.config.js`:

```js
export default {
  expo: {
    name: 'MyApp',
    extra: {
      apiUrl: process.env.API_URL || 'https://api.example.com',
    },
  },
};
```

### Build-Time Variables

```json
{
  "build": {
    "production": {
      "env": {
        "API_URL": "https://api.production.com"
      }
    },
    "staging": {
      "env": {
        "API_URL": "https://api.staging.com"
      }
    }
  }
}
```

## Best Practices

1. **Version Bumping**: Always increment version before building
2. **Test Builds**: Test preview builds before production
3. **OTA Updates**: Use for bug fixes, not breaking changes
4. **Environment Variables**: Use secrets for sensitive data
5. **Build Profiles**: Separate dev, staging, and production
6. **Automation**: Set up CI/CD for automated builds
7. **Monitoring**: Monitor crash reports and analytics

## Troubleshooting

### Build Failures

- Check EAS build logs: `eas build:list`
- Verify certificates and provisioning profiles
- Check app.json configuration
- Review native dependencies

### Submission Issues

- Verify app store credentials
- Check app metadata completeness
- Ensure compliance with store guidelines
- Review rejection reasons carefully
