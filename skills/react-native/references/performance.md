# Performance Optimization Guide

Complete guide to optimizing React Native app performance.

## Table of Contents

- [FlatList Optimization](#flatlist-optimization)
- [Image Optimization](#image-optimization)
- [Memoization](#memoization)
- [Bundle Size](#bundle-size)
- [Profiling](#profiling)

## FlatList Optimization

Optimize list rendering for large datasets.

### Basic Optimization

```tsx
import { FlatList } from 'react-native';

<FlatList
  data={items}
  renderItem={({ item }) => <Item data={item} />}
  keyExtractor={(item) => item.id}
  // Performance props
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={10}
  initialNumToRender={10}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

### Memoized Item Component

```tsx
import { memo } from 'react';

const Item = memo(({ data }) => {
  return <View>{/* render item */}</View>;
}, (prevProps, nextProps) => {
  return prevProps.data.id === nextProps.data.id;
});
```

### Virtualized Lists

For very long lists, use `VirtualizedList` or `SectionList`:

```tsx
import { SectionList } from 'react-native';

<SectionList
  sections={sections}
  renderItem={({ item }) => <Item data={item} />}
  renderSectionHeader={({ section }) => <Header title={section.title} />}
  keyExtractor={(item) => item.id}
/>
```

## Image Optimization

Optimize images for performance and memory.

### Image Sizing

```tsx
import { Image } from 'react-native';

<Image
  source={{ uri: 'image.jpg' }}
  style={{ width: 200, height: 200 }}
  resizeMode="cover"
/>
```

### Caching

```tsx
import { Image } from 'react-native';
import { CacheManager } from 'react-native-expo-image-cache';

// Cache images
await CacheManager.get('https://example.com/image.jpg').getPath();

// Use cached image
<Image source={{ uri: cachedPath }} />
```

### Progressive Loading

```tsx
import { Image } from 'expo-image';

<Image
  source={{ uri: 'image.jpg' }}
  placeholder={{ uri: 'placeholder.jpg' }}
  contentFit="cover"
  transition={200}
/>
```

### Lazy Loading

```tsx
import { useState } from 'react';
import { Image } from 'react-native';

function LazyImage({ uri }) {
  const [loaded, setLoaded] = useState(false);
  
  return (
    <View>
      {!loaded && <ActivityIndicator />}
      <Image
        source={{ uri }}
        onLoad={() => setLoaded(true)}
        style={{ opacity: loaded ? 1 : 0 }}
      />
    </View>
  );
}
```

## Memoization

Use memoization to prevent unnecessary re-renders.

### React.memo

```tsx
import { memo } from 'react';

const ExpensiveComponent = memo(({ data }) => {
  // Expensive rendering
  return <View>{/* complex UI */}</View>;
});
```

### useMemo

```tsx
import { useMemo } from 'react';

function MyComponent({ items }) {
  const sortedItems = useMemo(() => {
    return items.sort((a, b) => a.name.localeCompare(b.name));
  }, [items]);
  
  return <FlatList data={sortedItems} />;
}
```

### useCallback

```tsx
import { useCallback } from 'react';

function MyComponent({ onPress }) {
  const handlePress = useCallback(() => {
    onPress();
  }, [onPress]);
  
  return <Button onPress={handlePress} />;
}
```

### Custom Comparison

```tsx
const MyComponent = memo(({ data }) => {
  return <View>{/* render */}</View>;
}, (prevProps, nextProps) => {
  // Return true if props are equal (skip render)
  return prevProps.data.id === nextProps.data.id;
});
```

## Bundle Size

Reduce app bundle size for faster downloads.

### Analyze Bundle

```bash
npx react-native-bundle-visualizer
```

### Code Splitting

```tsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<ActivityIndicator />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Remove Unused Dependencies

```bash
# Find unused dependencies
npx depcheck

# Remove unused
npm uninstall unused-package
```

### Optimize Images

- Use WebP format when possible
- Compress images before bundling
- Use appropriate image sizes
- Consider using CDN for images

### Tree Shaking

Ensure tree shaking works:

```json
{
  "sideEffects": false
}
```

## Profiling

Profile app performance to identify bottlenecks.

### React DevTools Profiler

```tsx
import { Profiler } from 'react';

function onRenderCallback(id, phase, actualDuration) {
  console.log('Component:', id);
  console.log('Phase:', phase);
  console.log('Duration:', actualDuration);
}

<Profiler id="MyComponent" onRender={onRenderCallback}>
  <MyComponent />
</Profiler>
```

### Performance Monitor

```tsx
import { PerformanceObserver } from 'react-native';

const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log('Performance:', entry.name, entry.duration);
  }
});

observer.observe({ entryTypes: ['measure', 'navigation'] });
```

### Flipper Integration

Use Flipper for performance monitoring:

1. Install Flipper
2. Connect device
3. Use React DevTools plugin
4. Monitor component renders
5. Check network requests

### Memory Profiling

```tsx
import { InteractionManager } from 'react-native';

// Defer heavy operations
InteractionManager.runAfterInteractions(() => {
  // Heavy work
});
```

## Best Practices

1. **Use FlatList**: Always use FlatList for long lists
2. **Optimize Images**: Compress and size images appropriately
3. **Memoize Expensive Components**: Use React.memo for complex components
4. **Avoid Inline Functions**: Use useCallback for event handlers
5. **Lazy Load**: Load components and data lazily
6. **Profile Regularly**: Use profiling tools to identify issues
7. **Monitor Bundle Size**: Keep bundle size under control
8. **Use Native Modules**: For performance-critical code

## Common Performance Issues

### Too Many Re-renders

Solution: Use memoization and optimize state updates

### Large Lists Lagging

Solution: Use FlatList with proper optimization props

### Images Causing Memory Issues

Solution: Optimize image sizes and use caching

### Slow Navigation

Solution: Lazy load screens and optimize navigation structure

### Large Bundle Size

Solution: Code splitting, remove unused dependencies, optimize assets
