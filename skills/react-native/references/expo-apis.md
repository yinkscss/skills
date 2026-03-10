# Expo APIs Reference

Reference guide to common Expo SDK APIs.

## Table of Contents

- [Camera](#camera)
- [Location](#location)
- [Notifications](#notifications)
- [File System](#file-system)
- [SQLite](#sqlite)
- [Secure Store](#secure-store)
- [Image Picker](#image-picker)
- [Contacts](#contacts)
- [Calendar](#calendar)

## Camera

Take photos and record videos.

### Installation

```bash
npx expo install expo-camera
```

### Basic Usage

```tsx
import { Camera } from 'expo-camera';

const [permission, requestPermission] = Camera.useCameraPermissions();

if (!permission) {
  return <View />;
}

if (!permission.granted) {
  return (
    <View>
      <Text>No access to camera</Text>
      <Button onPress={requestPermission} title="Grant permission" />
    </View>
  );
}

return (
  <Camera style={{ flex: 1 }} type={Camera.Constants.Type.back}>
    {/* Camera UI */}
  </Camera>
);
```

### Take Photo

```tsx
const cameraRef = useRef<Camera>(null);

const takePicture = async () => {
  if (cameraRef.current) {
    const photo = await cameraRef.current.takePictureAsync();
    console.log(photo.uri);
  }
};
```

## Location

Get device location and track movement.

### Installation

```bash
npx expo install expo-location
```

### Get Current Location

```tsx
import * as Location from 'expo-location';

const getLocation = async () => {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') {
    return;
  }

  const location = await Location.getCurrentPositionAsync({});
  console.log(location.coords.latitude, location.coords.longitude);
};
```

### Watch Position

```tsx
const watchPosition = async () => {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') return;

  Location.watchPositionAsync(
    {
      accuracy: Location.Accuracy.Balanced,
      timeInterval: 1000,
      distanceInterval: 1,
    },
    (location) => {
      console.log('Location:', location.coords);
    }
  );
};
```

### Geocoding

```tsx
// Address to coordinates
const coords = await Location.geocodeAsync('1600 Amphitheatre Parkway');

// Coordinates to address
const addresses = await Location.reverseGeocodeAsync({
  latitude: 37.4219983,
  longitude: -122.084,
});
```

## Notifications

Send and receive push notifications.

### Installation

```bash
npx expo install expo-notifications
```

### Request Permissions

```tsx
import * as Notifications from 'expo-notifications';

const registerForPushNotifications = async () => {
  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== 'granted') {
    return;
  }

  const token = await Notifications.getExpoPushTokenAsync();
  console.log('Push token:', token);
};
```

### Schedule Notification

```tsx
await Notifications.scheduleNotificationAsync({
  content: {
    title: "Reminder",
    body: "Don't forget!",
    sound: true,
  },
  trigger: {
    seconds: 60,
  },
});
```

### Handle Notifications

```tsx
useEffect(() => {
  const subscription = Notifications.addNotificationReceivedListener(
    (notification) => {
      console.log('Notification received:', notification);
    }
  );

  return () => subscription.remove();
}, []);
```

## File System

Read and write files.

### Installation

```bash
npx expo install expo-file-system
```

### Read File

```tsx
import * as FileSystem from 'expo-file-system';

const readFile = async () => {
  const content = await FileSystem.readAsStringAsync(
    FileSystem.documentDirectory + 'file.txt'
  );
  console.log(content);
};
```

### Write File

```tsx
const writeFile = async () => {
  await FileSystem.writeAsStringAsync(
    FileSystem.documentDirectory + 'file.txt',
    'Hello, World!'
  );
};
```

### Download File

```tsx
const downloadFile = async () => {
  const { uri } = await FileSystem.downloadAsync(
    'https://example.com/file.pdf',
    FileSystem.documentDirectory + 'file.pdf'
  );
  console.log('Downloaded to:', uri);
};
```

## SQLite

Local database storage.

### Installation

```bash
npx expo install expo-sqlite
```

### Database Operations

```tsx
import * as SQLite from 'expo-sqlite';

const db = await SQLite.openDatabaseAsync('mydb.db');

// Create table
await db.execAsync(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
  );
`);

// Insert
await db.runAsync('INSERT INTO users (name) VALUES (?)', ['John']);

// Query
const result = await db.getAllAsync('SELECT * FROM users');
console.log(result);
```

## Secure Store

Securely store sensitive data.

### Installation

```bash
npx expo install expo-secure-store
```

### Store Data

```tsx
import * as SecureStore from 'expo-secure-store';

await SecureStore.setItemAsync('token', 'secret-token');
```

### Retrieve Data

```tsx
const token = await SecureStore.getItemAsync('token');
console.log(token);
```

### Delete Data

```tsx
await SecureStore.deleteItemAsync('token');
```

## Image Picker

Select images from device.

### Installation

```bash
npx expo install expo-image-picker
```

### Pick Image

```tsx
import * as ImagePicker from 'expo-image-picker';

const pickImage = async () => {
  const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
  if (status !== 'granted') return;

  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    quality: 1,
  });

  if (!result.canceled) {
    console.log(result.assets[0].uri);
  }
};
```

## Contacts

Access device contacts.

### Installation

```bash
npx expo install expo-contacts
```

### Get Contacts

```tsx
import * as Contacts from 'expo-contacts';

const getContacts = async () => {
  const { status } = await Contacts.requestPermissionsAsync();
  if (status !== 'granted') return;

  const { data } = await Contacts.getContactsAsync({
    fields: [Contacts.Fields.Name, Contacts.Fields.PhoneNumbers],
  });

  console.log(data);
};
```

## Calendar

Access device calendar.

### Installation

```bash
npx expo install expo-calendar
```

### Get Calendars

```tsx
import * as Calendar from 'expo-calendar';

const getCalendars = async () => {
  const { status } = await Calendar.requestCalendarPermissionsAsync();
  if (status !== 'granted') return;

  const calendars = await Calendar.getCalendarsAsync(
    Calendar.EntityTypes.EVENT
  );
  console.log(calendars);
};
```

### Create Event

```tsx
const createEvent = async () => {
  const { status } = await Calendar.requestCalendarPermissionsAsync();
  if (status !== 'granted') return;

  const eventId = await Calendar.createEventAsync(calendarId, {
    title: 'Meeting',
    startDate: new Date(),
    endDate: new Date(Date.now() + 3600000),
  });
};
```

## Best Practices

1. **Request Permissions**: Always request permissions before using APIs
2. **Handle Errors**: Wrap API calls in try-catch blocks
3. **Check Availability**: Some APIs may not be available on all platforms
4. **Clean Up**: Remove listeners and subscriptions in useEffect cleanup
5. **Performance**: Cache results when appropriate
6. **Privacy**: Only request permissions you actually need
