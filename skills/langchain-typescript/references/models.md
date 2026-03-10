# Models Reference

## Overview

LangChain provides a standardized interface for working with language models from different providers, making it easy to swap between OpenAI, Anthropic, Google, and others.

## Table of Contents

1. [Model Types](#model-types)
2. [Chat Models](#chat-models)
3. [Model Configuration](#model-configuration)
4. [Streaming](#streaming)
5. [Structured Output](#structured-output)
6. [Provider-Specific Features](#provider-specific-features)
7. [Best Practices](#best-practices)

## Model Types

### Chat Models

Conversational models that take messages as input:

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { ChatAnthropic } from "@langchain/anthropic";
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";

const openai = new ChatOpenAI({ model: "gpt-4" });
const claude = new ChatAnthropic({ model: "claude-3-5-sonnet-20241022" });
const gemini = new ChatGoogleGenerativeAI({ model: "gemini-pro" });
```

### LLMs (Legacy)

Text-in, text-out models (mostly deprecated in favor of chat models):

```typescript
import { OpenAI } from "@langchain/openai";

const llm = new OpenAI({
  model: "gpt-3.5-turbo-instruct",
  temperature: 0.7
});
```

### Embedding Models

Convert text to vector representations:

```typescript
import { OpenAIEmbeddings } from "@langchain/openai";

const embeddings = new OpenAIEmbeddings({
  model: "text-embedding-3-small"
});

const vectors = await embeddings.embedDocuments([
  "Hello world",
  "Goodbye world"
]);
```

## Chat Models

### Basic Usage

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";

const model = new ChatOpenAI({
  model: "gpt-4",
  temperature: 0
});

const messages = [
  new SystemMessage("You are a helpful assistant."),
  new HumanMessage("What is 2+2?")
];

const response = await model.invoke(messages);
console.log(response.content);  // "2+2 equals 4."
```

### Message Types

```typescript
import {
  SystemMessage,
  HumanMessage,
  AIMessage,
  ToolMessage
} from "@langchain/core/messages";

const conversation = [
  new SystemMessage("You are a coding assistant."),
  new HumanMessage("Write a function to add two numbers"),
  new AIMessage("Here's a function: function add(a, b) { return a + b; }"),
  new HumanMessage("Can you add type annotations?"),
  new AIMessage("function add(a: number, b: number): number { return a + b; }")
];

const response = await model.invoke(conversation);
```

### Model Providers

**OpenAI**:
```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  model: "gpt-4-turbo-preview",  // or "gpt-4", "gpt-3.5-turbo"
  apiKey: process.env.OPENAI_API_KEY,
  temperature: 0.7,
  maxTokens: 2000
});
```

**Anthropic (Claude)**:
```typescript
import { ChatAnthropic } from "@langchain/anthropic";

const model = new ChatAnthropic({
  model: "claude-3-5-sonnet-20241022",  // or "claude-3-opus-20240229"
  apiKey: process.env.ANTHROPIC_API_KEY,
  temperature: 0,
  maxTokens: 4096
});
```

**Google (Gemini)**:
```typescript
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";

const model = new ChatGoogleGenerativeAI({
  model: "gemini-pro",
  apiKey: process.env.GOOGLE_API_KEY,
  temperature: 0.9
});
```

**Azure OpenAI**:
```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
  azureOpenAIApiDeploymentName: "gpt-4",
  azureOpenAIApiVersion: "2023-05-15",
  azureOpenAIBasePath: "https://your-resource.openai.azure.com/openai/deployments"
});
```

## Model Configuration

### Temperature

Controls randomness (0 = deterministic, 1 = creative):

```typescript
// Deterministic (for data extraction, math)
const precise = new ChatOpenAI({ temperature: 0 });

// Balanced (general use)
const balanced = new ChatOpenAI({ temperature: 0.7 });

// Creative (for writing, brainstorming)
const creative = new ChatOpenAI({ temperature: 1 });
```

### Token Limits

```typescript
const model = new ChatOpenAI({
  model: "gpt-4",
  maxTokens: 2000,  // Max tokens in response
  timeout: 30000     // Request timeout (ms)
});
```

### Model Parameters

```typescript
const model = new ChatOpenAI({
  model: "gpt-4",
  temperature: 0.7,
  maxTokens: 2000,
  topP: 1,              // Nucleus sampling
  frequencyPenalty: 0,  // Reduce repetition
  presencePenalty: 0,   // Encourage topic diversity
  n: 1,                 // Number of completions
  stop: ["\n\n"]        // Stop sequences
});
```

### Retry Logic

```typescript
const model = new ChatOpenAI({
  model: "gpt-4",
  maxRetries: 3,
  timeout: 60000
});
```

## Streaming

### Basic Streaming

```typescript
const model = new ChatOpenAI({
  model: "gpt-4",
  streaming: true
});

const stream = await model.stream([
  new HumanMessage("Write a short story about a robot")
]);

for await (const chunk of stream) {
  process.stdout.write(chunk.content);
}
```

### With Callbacks

```typescript
import { CallbackManager } from "@langchain/core/callbacks/manager";

const model = new ChatOpenAI({
  model: "gpt-4",
  streaming: true,
  callbacks: CallbackManager.fromHandlers({
    handleLLMNewToken: async (token: string) => {
      process.stdout.write(token);
    }
  })
});

await model.invoke([new HumanMessage("Hello!")]);
```

### Server-Sent Events (SSE)

For web applications:

```typescript
import { ChatOpenAI } from "@langchain/openai";

export async function POST(req: Request) {
  const { message } = await req.json();
  const model = new ChatOpenAI({ model: "gpt-4", streaming: true });
  
  const stream = await model.stream([new HumanMessage(message)]);
  
  const encoder = new TextEncoder();
  const readable = new ReadableStream({
    async start(controller) {
      for await (const chunk of stream) {
        controller.enqueue(encoder.encode(chunk.content));
      }
      controller.close();
    }
  });
  
  return new Response(readable, {
    headers: { "Content-Type": "text/event-stream" }
  });
}
```

## Structured Output

### Using Zod Schemas

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";

const model = new ChatOpenAI({
  model: "gpt-4",
  temperature: 0
});

const schema = z.object({
  name: z.string().describe("Person's name"),
  age: z.number().describe("Person's age"),
  email: z.string().email().describe("Email address")
});

const structuredModel = model.withStructuredOutput(schema);

const result = await structuredModel.invoke([
  new HumanMessage("Extract info: John is 30 years old, email john@example.com")
]);

console.log(result);
// { name: "John", age: 30, email: "john@example.com" }
```

### JSON Mode

```typescript
const model = new ChatOpenAI({
  model: "gpt-4-turbo-preview",
  modelKwargs: {
    response_format: { type: "json_object" }
  }
});

const response = await model.invoke([
  new SystemMessage("You always respond with valid JSON"),
  new HumanMessage("List 3 colors")
]);

const data = JSON.parse(response.content as string);
// { "colors": ["red", "blue", "green"] }
```

### Function Calling

```typescript
const model = new ChatOpenAI({ model: "gpt-4" });

const tools = [
  {
    type: "function",
    function: {
      name: "get_weather",
      description: "Get weather for a location",
      parameters: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "City name"
          }
        },
        required: ["location"]
      }
    }
  }
];

const modelWithTools = model.bind({ tools });

const response = await modelWithTools.invoke([
  new HumanMessage("What's the weather in San Francisco?")
]);

if (response.additional_kwargs.tool_calls) {
  const toolCall = response.additional_kwargs.tool_calls[0];
  console.log(toolCall.function.name);  // "get_weather"
  console.log(toolCall.function.arguments);  // { "location": "San Francisco" }
}
```

## Provider-Specific Features

### OpenAI Vision

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "@langchain/core/messages";

const model = new ChatOpenAI({ model: "gpt-4-vision-preview" });

const response = await model.invoke([
  new HumanMessage({
    content: [
      { type: "text", text: "What's in this image?" },
      {
        type: "image_url",
        image_url: { url: "https://example.com/image.jpg" }
      }
    ]
  })
]);
```

### Claude with Caching

```typescript
import { ChatAnthropic } from "@langchain/anthropic";

const model = new ChatAnthropic({
  model: "claude-3-5-sonnet-20241022",
  // Enable prompt caching for large system prompts
  cache_control: { type: "ephemeral" }
});
```

### Gemini Multimodal

```typescript
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";

const model = new ChatGoogleGenerativeAI({
  model: "gemini-pro-vision"
});

// Can process images, videos, and text
```

## Best Practices

### 1. Use Environment Variables

```typescript
// Good
const model = new ChatOpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Bad
const model = new ChatOpenAI({
  apiKey: "sk-..." // Hardcoded key
});
```

### 2. Choose Appropriate Temperature

```typescript
// Data extraction: temperature = 0
const extractor = new ChatOpenAI({ temperature: 0 });

// Creative writing: temperature = 0.8-1.0
const writer = new ChatOpenAI({ temperature: 0.9 });

// General chat: temperature = 0.7
const chatbot = new ChatOpenAI({ temperature: 0.7 });
```

### 3. Set Token Limits

```typescript
const model = new ChatOpenAI({
  model: "gpt-4",
  maxTokens: 500  // Prevent runaway costs
});
```

### 4. Handle Errors

```typescript
async function callModel(messages: BaseMessage[]) {
  try {
    return await model.invoke(messages);
  } catch (error) {
    if (error.code === "rate_limit_exceeded") {
      await sleep(1000);
      return await model.invoke(messages);
    }
    throw error;
  }
}
```

### 5. Use Fallbacks

```typescript
import { ChatOpenAI } from "@langchain/openai";

const primary = new ChatOpenAI({ model: "gpt-4" });
const fallback = new ChatOpenAI({ model: "gpt-3.5-turbo" });

const modelWithFallback = primary.withFallbacks([fallback]);

// Automatically uses fallback if primary fails
const response = await modelWithFallback.invoke(messages);
```

### 6. Monitor Token Usage

```typescript
import { CallbackManager } from "@langchain/core/callbacks/manager";

let totalTokens = 0;

const model = new ChatOpenAI({
  model: "gpt-4",
  callbacks: CallbackManager.fromHandlers({
    handleLLMEnd: async (output) => {
      const usage = output.llmOutput?.tokenUsage;
      totalTokens += usage?.totalTokens || 0;
      console.log(`Tokens used: ${usage?.totalTokens}`);
      console.log(`Total tokens: ${totalTokens}`);
    }
  })
});
```

### 7. Cache Responses

```typescript
import { InMemoryCache } from "@langchain/core/caches";

const cache = new InMemoryCache();

const model = new ChatOpenAI({
  model: "gpt-4",
  cache
});

// First call hits the API
await model.invoke([new HumanMessage("What is 2+2?")]);

// Second identical call uses cache
await model.invoke([new HumanMessage("What is 2+2?")]);
```

### 8. Batch Requests

```typescript
const messages = [
  [new HumanMessage("Translate to French: Hello")],
  [new HumanMessage("Translate to Spanish: Hello")],
  [new HumanMessage("Translate to German: Hello")]
];

// Batch process for efficiency
const results = await model.batch(messages);
```

## Common Patterns

### Model Switching

```typescript
function getModel(task: string) {
  if (task === "coding") {
    return new ChatOpenAI({ model: "gpt-4" });
  } else if (task === "chat") {
    return new ChatOpenAI({ model: "gpt-3.5-turbo" });
  } else {
    return new ChatAnthropic({ model: "claude-3-5-sonnet-20241022" });
  }
}
```

### Cost Optimization

```typescript
// Use cheaper model for simple tasks
const simpleModel = new ChatOpenAI({ model: "gpt-3.5-turbo" });

// Use expensive model only when needed
const complexModel = new ChatOpenAI({ model: "gpt-4" });

async function processQuery(query: string) {
  // Try simple model first
  const result = await simpleModel.invoke([new HumanMessage(query)]);
  
  // If confidence is low, escalate to complex model
  if (needsComplexReasoning(result)) {
    return await complexModel.invoke([new HumanMessage(query)]);
  }
  
  return result;
}
```

### Model Comparison

```typescript
const models = [
  new ChatOpenAI({ model: "gpt-4" }),
  new ChatAnthropic({ model: "claude-3-5-sonnet-20241022" }),
  new ChatGoogleGenerativeAI({ model: "gemini-pro" })
];

const prompt = [new HumanMessage("Explain quantum computing")];

const results = await Promise.all(
  models.map(model => model.invoke(prompt))
);

results.forEach((result, i) => {
  console.log(`Model ${i}: ${result.content}`);
});
```
