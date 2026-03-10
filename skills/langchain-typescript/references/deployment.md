# Deployment & Production Reference

## Overview

Guidance for deploying LangChain applications to production with LangSmith integration, monitoring, and best practices.

## Table of Contents

1. [LangSmith Integration](#langsmith-integration)
2. [Production Deployment](#production-deployment)
3. [Monitoring & Observability](#monitoring--observability)
4. [Testing](#testing)
5. [Performance Optimization](#performance-optimization)

## LangSmith Integration

### Setup

```typescript
// Environment variables
LANGSMITH_API_KEY=your_api_key
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT=your_project_name
```

```typescript
import { Client } from "langsmith";

const client = new Client({
  apiKey: process.env.LANGSMITH_API_KEY
});
```

### Tracing

Automatically trace all LangChain operations:

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  model: "gpt-4",
  callbacks: []  // LangSmith auto-instruments when env vars set
});

// All calls automatically traced to LangSmith
await model.invoke([{ role: "user", content: "Hello" }]);
```

### Custom Runs

```typescript
import { traceable } from "langsmith/traceable";

const myFunction = traceable(
  async (input: string) => {
    // Function logic
    return processInput(input);
  },
  { name: "custom_processor", project: "my-project" }
);

await myFunction("test input");
```

### Evaluation

```typescript
import { evaluate } from "langsmith/evaluation";

// Define evaluator
const correctnessEvaluator = async (run: Run, example: Example) => {
  const score = computeScore(run.outputs, example.outputs);
  return { key: "correctness", score };
};

// Run evaluation
await evaluate(
  async (input) => chain.invoke(input),
  {
    data: "dataset-name",
    evaluators: [correctnessEvaluator],
    projectName: "evaluation-run"
  }
);
```

## Production Deployment

### Environment Configuration

```typescript
// config.ts
export const config = {
  openai: {
    apiKey: process.env.OPENAI_API_KEY,
    model: process.env.OPENAI_MODEL || "gpt-4",
    temperature: parseFloat(process.env.TEMPERATURE || "0.7")
  },
  langsmith: {
    apiKey: process.env.LANGSMITH_API_KEY,
    project: process.env.LANGSMITH_PROJECT,
    enabled: process.env.LANGSMITH_TRACING_V2 === "true"
  },
  redis: {
    url: process.env.REDIS_URL
  }
};
```

### Next.js API Route

```typescript
// app/api/chat/route.ts
import { ChatOpenAI } from "@langchain/openai";
import { StreamingTextResponse } from "ai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";

export const runtime = "edge";  // Optional: Use edge runtime

export async function POST(req: Request) {
  try {
    const { message, sessionId } = await req.json();
    
    const model = new ChatOpenAI({
      model: "gpt-4",
      streaming: true
    });
    
    const agent = createReactAgent({
      llm: model,
      tools: tools
    });
    
    const stream = await agent.stream({
      messages: [{ role: "user", content: message }]
    }, {
      configurable: { thread_id: sessionId }
    });
    
    return new StreamingTextResponse(stream);
  } catch (error) {
    console.error("Chat error:", error);
    return new Response("Error processing request", { status: 500 });
  }
}
```

### Express.js Server

```typescript
import express from "express";
import { ChatOpenAI } from "@langchain/openai";

const app = express();
app.use(express.json());

app.post("/api/chat", async (req, res) => {
  try {
    const { message } = req.body;
    
    const model = new ChatOpenAI({ model: "gpt-4" });
    const response = await model.invoke([
      { role: "user", content: message }
    ]);
    
    res.json({ response: response.content });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
```

### Docker Deployment

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
      - LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
      - LANGSMITH_TRACING_V2=true
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

## Monitoring & Observability

### Logging

```typescript
import winston from "winston";

const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" })
  ]
});

// In production
if (process.env.NODE_ENV === "production") {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

// Usage
const model = new ChatOpenAI({
  callbacks: [{
    handleLLMStart: async () => {
      logger.info("LLM call started");
    },
    handleLLMEnd: async (output) => {
      logger.info("LLM call completed", {
        tokens: output.llmOutput?.tokenUsage
      });
    },
    handleLLMError: async (error) => {
      logger.error("LLM error", { error: error.message });
    }
  }]
});
```

### Metrics

```typescript
import { register, Counter, Histogram } from "prom-client";

const requestCounter = new Counter({
  name: "langchain_requests_total",
  help: "Total number of LangChain requests"
});

const requestDuration = new Histogram({
  name: "langchain_request_duration_seconds",
  help: "Duration of LangChain requests",
  buckets: [0.1, 0.5, 1, 2, 5, 10]
});

// Middleware
async function monitoredInvoke(chain: any, input: any) {
  const start = Date.now();
  requestCounter.inc();
  
  try {
    const result = await chain.invoke(input);
    return result;
  } finally {
    const duration = (Date.now() - start) / 1000;
    requestDuration.observe(duration);
  }
}

// Expose metrics endpoint
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});
```

### Error Tracking

```typescript
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV
});

// Wrap LangChain operations
async function safeInvoke(chain: any, input: any) {
  try {
    return await chain.invoke(input);
  } catch (error) {
    Sentry.captureException(error, {
      tags: { component: "langchain" },
      extra: { input }
    });
    throw error;
  }
}
```

## Testing

### Unit Tests

```typescript
import { describe, it, expect, vi } from "vitest";
import { ChatOpenAI } from "@langchain/openai";

describe("Chat Agent", () => {
  it("should respond to user messages", async () => {
    const model = new ChatOpenAI({
      model: "gpt-4",
      apiKey: "test-key"
    });
    
    // Mock the API call
    vi.spyOn(model, "invoke").mockResolvedValue({
      content: "Hello!"
    });
    
    const response = await model.invoke([
      { role: "user", content: "Hi" }
    ]);
    
    expect(response.content).toBe("Hello!");
  });
});
```

### Integration Tests

```typescript
import { describe, it, expect } from "vitest";

describe("Agent Integration", () => {
  it("should use tools correctly", async () => {
    const agent = createReactAgent({
      llm: model,
      tools: [calculatorTool]
    });
    
    const result = await agent.invoke({
      messages: [{ role: "user", content: "What is 15 * 24?" }]
    });
    
    expect(result.messages[result.messages.length - 1].content)
      .toContain("360");
  });
});
```

### End-to-End Tests

```typescript
import { test, expect } from "@playwright/test";

test("chat interface works", async ({ page }) => {
  await page.goto("http://localhost:3000");
  
  await page.fill('input[name="message"]', "Hello!");
  await page.click('button[type="submit"]');
  
  await expect(page.locator(".chat-message")).toContainText("Hello");
});
```

## Performance Optimization

### Caching

```typescript
import { InMemoryCache } from "@langchain/core/caches";
import { createClient } from "redis";

// In-memory cache (development)
const memoryCache = new InMemoryCache();

// Redis cache (production)
const redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

const model = new ChatOpenAI({
  cache: process.env.NODE_ENV === "production" 
    ? redisCache 
    : memoryCache
});
```

### Connection Pooling

```typescript
import { ChatOpenAI } from "@langchain/openai";

// Reuse model instances
const modelPool = new Map<string, ChatOpenAI>();

function getModel(modelName: string = "gpt-4"): ChatOpenAI {
  if (!modelPool.has(modelName)) {
    modelPool.set(modelName, new ChatOpenAI({
      model: modelName,
      maxConcurrency: 10  // Limit concurrent requests
    }));
  }
  return modelPool.get(modelName)!;
}
```

### Request Batching

```typescript
import pLimit from "p-limit";

const limit = pLimit(5);  // Max 5 concurrent requests

async function batchProcess(inputs: string[]) {
  const promises = inputs.map(input =>
    limit(() => model.invoke([{ role: "user", content: input }]))
  );
  
  return await Promise.all(promises);
}
```

### Streaming for Better UX

```typescript
// Instead of waiting for full response
const response = await model.invoke(messages);

// Stream tokens as they arrive
const stream = await model.stream(messages);
for await (const chunk of stream) {
  sendToClient(chunk.content);
}
```

### Rate Limiting

```typescript
import rateLimit from "express-rate-limit";

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // Limit each IP to 100 requests per window
  message: "Too many requests"
});

app.use("/api/chat", limiter);
```

## Best Practices

### 1. Health Checks

```typescript
app.get("/health", async (req, res) => {
  try {
    // Check Redis
    await redisClient.ping();
    
    // Check model availability
    await model.invoke([{ role: "user", content: "ping" }]);
    
    res.json({ status: "healthy" });
  } catch (error) {
    res.status(503).json({ status: "unhealthy", error: error.message });
  }
});
```

### 2. Graceful Shutdown

```typescript
process.on("SIGTERM", async () => {
  console.log("SIGTERM received, shutting down gracefully");
  
  // Close Redis connection
  await redisClient.quit();
  
  // Stop accepting new requests
  server.close(() => {
    console.log("Server closed");
    process.exit(0);
  });
});
```

### 3. Secret Management

```typescript
// Use environment variables
// Never commit secrets to git

// .env.example
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
LANGSMITH_API_KEY=your_key_here

// .gitignore
.env
.env.local
```

### 4. Cost Control

```typescript
const costTracker = {
  totalTokens: 0,
  totalCost: 0
};

const model = new ChatOpenAI({
  callbacks: [{
    handleLLMEnd: async (output) => {
      const tokens = output.llmOutput?.tokenUsage?.totalTokens || 0;
      costTracker.totalTokens += tokens;
      costTracker.totalCost += (tokens / 1000) * 0.03;  // Adjust rate
      
      if (costTracker.totalCost > 100) {  // Alert at $100
        logger.warn("High API costs detected", costTracker);
      }
    }
  }]
});
```

### 5. Load Balancing

```typescript
const models = [
  new ChatOpenAI({ apiKey: process.env.OPENAI_KEY_1 }),
  new ChatOpenAI({ apiKey: process.env.OPENAI_KEY_2 }),
  new ChatOpenAI({ apiKey: process.env.OPENAI_KEY_3 })
];

let currentIndex = 0;

function getNextModel(): ChatOpenAI {
  const model = models[currentIndex];
  currentIndex = (currentIndex + 1) % models.length;
  return model;
}
```
