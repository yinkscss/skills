# Custom Tool Template

Templates for creating custom tools for LangChain agents.

## What Are Tools?

Tools extend agent capabilities by:
- Connecting to external APIs
- Querying databases
- Reading/writing files
- Performing calculations
- Executing custom logic

## Basic Structure

```typescript
import { tool } from "@langchain/core/tools";
import { z } from "zod";

export const myTool = tool(
  async (input) => {
    // Your logic here
    return "result";
  },
  {
    name: "tool_name",
    description: "Clear description of what this tool does",
    schema: z.object({
      param: z.string().describe("Parameter description")
    })
  }
);
```

## Key Components

### 1. Name

Short, descriptive identifier:
```typescript
name: "get_weather"        // Good
name: "weatherGetter123"   // Bad
```

### 2. Description

Clear explanation of:
- What the tool does
- When to use it
- What it returns

```typescript
description: "Get current weather for a location. Use this when users ask about weather, temperature, or climate conditions."
```

### 3. Schema (Zod)

Define input parameters with types and descriptions:

```typescript
schema: z.object({
  location: z.string().describe("City name"),
  units: z.enum(["celsius", "fahrenheit"]).default("celsius"),
  includeHourly: z.boolean().optional()
})
```

### 4. Function

Implement the tool logic:

```typescript
async ({ location, units = "celsius" }) => {
  const result = await fetchWeather(location, units);
  return JSON.stringify(result);  // Always return string
}
```

## Best Practices

### 1. Return JSON Strings

Tools should return strings, preferably JSON:

```typescript
return JSON.stringify({
  temperature: 72,
  condition: "sunny",
  humidity: 60
});
```

### 2. Handle Errors Gracefully

```typescript
async ({ url }) => {
  try {
    const response = await fetch(url);
    return await response.text();
  } catch (error) {
    return `Error: ${error.message}`;
  }
}
```

### 3. Validate Inputs

```typescript
schema: z.object({
  email: z.string().email(),
  age: z.number().min(0).max(150),
  url: z.string().url()
})
```

### 4. Use Descriptive Parameters

```typescript
// Good
z.object({
  query: z.string().describe("Search query"),
  limit: z.number().describe("Max results")
})

// Bad
z.object({
  q: z.string(),
  n: z.number()
})
```

### 5. Include Examples in Descriptions

```typescript
description: `Search the database. 
Example: search for 'John Doe' to find user records.
Returns: Array of matching records with id, name, email.`
```

## Common Patterns

### Rate-Limited Tool

```typescript
import pLimit from "p-limit";

const limit = pLimit(5);

export const rateLimitedTool = tool(
  async ({ url }) => {
    return limit(async () => {
      return await fetch(url);
    });
  },
  // ...
);
```

### Tool with Caching

```typescript
const cache = new Map();

export const cachedTool = tool(
  async ({ key }) => {
    if (cache.has(key)) {
      return cache.get(key);
    }
    
    const result = await expensiveOperation(key);
    cache.set(key, result);
    return result;
  },
  // ...
);
```

### Tool with Authentication

```typescript
export const authenticatedTool = tool(
  async ({ endpoint }) => {
    const response = await fetch(endpoint, {
      headers: {
        "Authorization": `Bearer ${process.env.API_KEY}`
      }
    });
    return await response.json();
  },
  // ...
);
```

### Tool with Retry Logic

```typescript
async function withRetry(fn: () => Promise<any>, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
    }
  }
}

export const resilientTool = tool(
  async ({ url }) => {
    return await withRetry(() => fetch(url));
  },
  // ...
);
```

## Testing Tools

```typescript
import { describe, it, expect } from "vitest";

describe("weatherTool", () => {
  it("should return weather data", async () => {
    const result = await weatherTool.invoke({ location: "NYC" });
    const data = JSON.parse(result);
    
    expect(data).toHaveProperty("temperature");
    expect(data).toHaveProperty("condition");
  });
  
  it("should handle errors", async () => {
    const result = await weatherTool.invoke({ location: "" });
    expect(result).toContain("Error");
  });
});
```

## Using Multiple Tools

```typescript
import { createReactAgent } from "@langchain/langgraph/prebuilt";

const agent = createReactAgent({
  llm: model,
  tools: [
    weatherTool,
    searchDatabaseTool,
    apiTool,
    emailTool
  ]
});
```

## Tool Organization

For large projects, organize tools by domain:

```
tools/
├── weather/
│   ├── current.ts
│   ├── forecast.ts
│   └── index.ts
├── database/
│   ├── search.ts
│   ├── insert.ts
│   └── index.ts
└── index.ts  // Export all tools
```
