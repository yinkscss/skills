# Memory & State Management Reference

## Overview

Memory enables chains and agents to maintain context across interactions. LangChain provides various memory types for different use cases.

## Table of Contents

1. [Memory Types](#memory-types)
2. [Conversation Memory](#conversation-memory)
3. [State Persistence](#state-persistence)
4. [Vector Store Memory](#vector-store-memory)
5. [Best Practices](#best-practices)

## Memory Types

### Buffer Memory

Stores all messages in memory:

```typescript
import { BufferMemory } from "langchain/memory";

const memory = new BufferMemory({
  returnMessages: true,
  memoryKey: "chat_history"
});

await memory.saveContext(
  { input: "Hi, I'm Alice" },
  { output: "Hello Alice! How can I help?" }
);

const history = await memory.loadMemoryVariables({});
console.log(history.chat_history);
```

### Buffer Window Memory

Keep only the last N messages:

```typescript
import { BufferWindowMemory } from "langchain/memory";

const memory = new BufferWindowMemory({
  k: 5,  // Keep last 5 messages
  returnMessages: true
});
```

### Summary Memory

Summarize old messages to save space:

```typescript
import { ConversationSummaryMemory } from "langchain/memory";

const memory = new ConversationSummaryMemory({
  llm: model,
  returnMessages: true
});

// Automatically summarizes when context gets long
```

### Entity Memory

Track specific entities mentioned:

```typescript
import { EntityMemory } from "langchain/memory";

const memory = new EntityMemory({
  llm: model
});

// Tracks: "Alice is a software engineer"
// Remembers: { "Alice": "software engineer" }
```

## Conversation Memory

### With Chains

```typescript
import { ConversationChain } from "langchain/chains";
import { BufferMemory } from "langchain/memory";

const memory = new BufferMemory();

const chain = new ConversationChain({
  llm: model,
  memory: memory
});

await chain.invoke({ input: "My name is Bob" });
await chain.invoke({ input: "What's my name?" });
// "Your name is Bob"
```

### With Agents

```typescript
import { BufferMemory } from "langchain/memory";
import { createReactAgent } from "@langchain/langgraph/prebuilt";

const memory = new BufferMemory({
  returnMessages: true,
  memoryKey: "chat_history"
});

const agent = createReactAgent({
  llm: model,
  tools: tools,
  messageModifier: async (messages) => {
    const history = await memory.loadMemoryVariables({});
    return [...history.chat_history, ...messages];
  }
});
```

### Custom Memory

```typescript
import { BaseChatMemory } from "langchain/memory";

class CustomMemory extends BaseChatMemory {
  private storage: Map<string, any> = new Map();
  
  async loadMemoryVariables(values: any): Promise<any> {
    return {
      history: this.storage.get("history") || []
    };
  }
  
  async saveContext(input: any, output: any): Promise<void> {
    const history = this.storage.get("history") || [];
    history.push({ input, output });
    this.storage.set("history", history);
  }
}
```

## State Persistence

### LangGraph State Management

```typescript
import { MemorySaver } from "@langchain/langgraph";
import { MessagesAnnotation, StateGraph } from "@langchain/langgraph";

const checkpointer = new MemorySaver();

const graph = new StateGraph(MessagesAnnotation)
  .addNode("chat", chatNode)
  .addEdge(START, "chat")
  .addEdge("chat", END)
  .compile({ checkpointer });

// Each thread maintains separate state
const thread1 = { configurable: { thread_id: "user-1" } };
const thread2 = { configurable: { thread_id: "user-2" } };

await graph.invoke({ messages: [...] }, thread1);
await graph.invoke({ messages: [...] }, thread2);
```

### Redis Persistence

```typescript
import { createClient } from "redis";
import { RedisChatMessageHistory } from "@langchain/redis";

const client = createClient({
  url: process.env.REDIS_URL
});

await client.connect();

const memory = new BufferMemory({
  chatHistory: new RedisChatMessageHistory({
    sessionId: "user-123",
    client: client
  }),
  returnMessages: true
});
```

### Database Persistence

```typescript
import { BaseListChatMessageHistory } from "@langchain/core/chat_history";
import { BaseMessage } from "@langchain/core/messages";

class DatabaseChatHistory extends BaseListChatMessageHistory {
  private sessionId: string;
  
  constructor(sessionId: string) {
    super();
    this.sessionId = sessionId;
  }
  
  async getMessages(): Promise<BaseMessage[]> {
    const messages = await db.messages.findMany({
      where: { sessionId: this.sessionId }
    });
    return messages;
  }
  
  async addMessage(message: BaseMessage): Promise<void> {
    await db.messages.create({
      data: {
        sessionId: this.sessionId,
        type: message._getType(),
        content: message.content
      }
    });
  }
  
  async clear(): Promise<void> {
    await db.messages.deleteMany({
      where: { sessionId: this.sessionId }
    });
  }
}
```

## Vector Store Memory

### Long-term Memory with Vectors

```typescript
import { VectorStoreRetrieverMemory } from "langchain/memory";
import { OpenAIEmbeddings } from "@langchain/openai";
import { MemoryVectorStore } from "langchain/vectorstores/memory";

const vectorStore = new MemoryVectorStore(new OpenAIEmbeddings());

const memory = new VectorStoreRetrieverMemory({
  vectorStoreRetriever: vectorStore.asRetriever(3),
  memoryKey: "history"
});

// Add memories
await memory.saveContext(
  { input: "My favorite color is blue" },
  { output: "That's a lovely color!" }
);

// Retrieve relevant memories
const relevantMemories = await memory.loadMemoryVariables({
  input: "What's my favorite color?"
});
```

### Semantic Memory Search

```typescript
import { Pinecone } from "@pinecone-database/pinecone";
import { PineconeStore } from "@langchain/pinecone";

const pinecone = new Pinecone();
const index = pinecone.Index("chat-history");

const vectorStore = await PineconeStore.fromExistingIndex(
  new OpenAIEmbeddings(),
  { pineconeIndex: index }
);

const memory = new VectorStoreRetrieverMemory({
  vectorStoreRetriever: vectorStore.asRetriever(5),
  inputKey: "input",
  memoryKey: "relevant_history"
});
```

## Best Practices

### 1. Choose Appropriate Memory Type

```typescript
// Short conversations: BufferMemory
const shortConvo = new BufferMemory();

// Long conversations: BufferWindowMemory
const longConvo = new BufferWindowMemory({ k: 10 });

// Very long: ConversationSummaryMemory
const veryLong = new ConversationSummaryMemory({ llm: model });
```

### 2. Implement Memory Limits

```typescript
class LimitedMemory extends BufferMemory {
  private maxSize = 1000;  // Max characters
  
  async saveContext(input: any, output: any): Promise<void> {
    await super.saveContext(input, output);
    
    const history = await this.loadMemoryVariables({});
    const totalSize = JSON.stringify(history).length;
    
    if (totalSize > this.maxSize) {
      // Trim old messages
      await this.clear();
    }
  }
}
```

### 3. Handle Memory Failures

```typescript
async function saveWithFallback(memory: BaseChatMemory, input: any, output: any) {
  try {
    await memory.saveContext(input, output);
  } catch (error) {
    console.error("Memory save failed:", error);
    // Use in-memory fallback
    inMemoryBackup.push({ input, output, timestamp: Date.now() });
  }
}
```

### 4. Clear Memory Periodically

```typescript
// Clear memory after session ends
async function endSession(sessionId: string) {
  const memory = getMemory(sessionId);
  await memory.clear();
  console.log(`Session ${sessionId} memory cleared`);
}

// Or implement time-based expiry
async function cleanExpiredSessions() {
  const expiredSessions = await db.sessions.findMany({
    where: {
      lastActivity: {
        lt: new Date(Date.now() - 24 * 60 * 60 * 1000)  // 24 hours
      }
    }
  });
  
  for (const session of expiredSessions) {
    await session.memory.clear();
  }
}
```

### 5. Use Thread IDs for Isolation

```typescript
// Each user gets isolated memory
function getUserMemory(userId: string) {
  return new BufferMemory({
    chatHistory: new RedisChatMessageHistory({
      sessionId: `user:${userId}`,
      client: redisClient
    })
  });
}

// Usage
const aliceMemory = getUserMemory("alice");
const bobMemory = getUserMemory("bob");
```

## Common Patterns

### Session Management

```typescript
class SessionManager {
  private sessions = new Map<string, BufferMemory>();
  
  getOrCreateSession(sessionId: string): BufferMemory {
    if (!this.sessions.has(sessionId)) {
      this.sessions.set(sessionId, new BufferMemory({
        returnMessages: true
      }));
    }
    return this.sessions.get(sessionId)!;
  }
  
  async destroySession(sessionId: string): Promise<void> {
    const memory = this.sessions.get(sessionId);
    if (memory) {
      await memory.clear();
      this.sessions.delete(sessionId);
    }
  }
}
```

### Memory with TTL

```typescript
interface MemoryEntry {
  messages: BaseMessage[];
  expiresAt: number;
}

class TTLMemory extends BufferMemory {
  private ttlMs: number;
  
  constructor(ttlMs: number = 3600000) {  // 1 hour default
    super();
    this.ttlMs = ttlMs;
  }
  
  async loadMemoryVariables(values: any): Promise<any> {
    const entry = await this.getEntry();
    
    if (entry && Date.now() > entry.expiresAt) {
      await this.clear();
      return { chat_history: [] };
    }
    
    return super.loadMemoryVariables(values);
  }
  
  async saveContext(input: any, output: any): Promise<void> {
    await super.saveContext(input, output);
    await this.updateExpiry();
  }
  
  private async updateExpiry(): Promise<void> {
    // Update expiry timestamp
  }
}
```

### Multi-Memory System

```typescript
class MultiMemory {
  private shortTerm: BufferWindowMemory;
  private longTerm: VectorStoreRetrieverMemory;
  
  constructor() {
    this.shortTerm = new BufferWindowMemory({ k: 10 });
    this.longTerm = new VectorStoreRetrieverMemory({
      vectorStoreRetriever: vectorStore.asRetriever()
    });
  }
  
  async loadMemoryVariables(input: any): Promise<any> {
    const [recent, relevant] = await Promise.all([
      this.shortTerm.loadMemoryVariables(input),
      this.longTerm.loadMemoryVariables(input)
    ]);
    
    return {
      recent_history: recent.chat_history,
      relevant_history: relevant.history
    };
  }
  
  async saveContext(input: any, output: any): Promise<void> {
    await Promise.all([
      this.shortTerm.saveContext(input, output),
      this.longTerm.saveContext(input, output)
    ]);
  }
}
```
