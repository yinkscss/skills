# Agents Reference

## Overview

Agents in LangChain use language models to determine which actions to take and in what order. They combine reasoning with tool execution to accomplish complex tasks.

## Table of Contents

1. [Quick Start](#quick-start)
2. [ReAct Agents](#react-agents)
3. [Creating Custom Agents](#creating-custom-agents)
4. [Agent Configuration](#agent-configuration)
5. [Agent Types](#agent-types)
6. [Best Practices](#best-practices)

## Quick Start

Create a simple agent in under 10 lines:

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { DuckDuckGoSearch } from "@langchain/community/tools/duckduckgo_search";

const model = new ChatOpenAI({
  model: "gpt-4",
  temperature: 0
});

const tools = [new DuckDuckGoSearch({ maxResults: 3 })];

const agent = createReactAgent({
  llm: model,
  tools: tools
});

// Run the agent
const result = await agent.invoke({
  messages: [{ role: "user", content: "What is the weather in San Francisco?" }]
});
```

## ReAct Agents

ReAct (Reason + Act) agents use a loop of reasoning and acting:

1. **Reason**: Think about what to do next
2. **Act**: Execute a tool or provide an answer
3. **Observe**: See the result of the action
4. **Repeat**: Continue until the task is complete

### ReAct Pattern

```typescript
import { createReactAgent } from "@langchain/langgraph/prebuilt";

const agent = createReactAgent({
  llm: model,
  tools: tools,
  messageModifier: `You are a helpful assistant. Use tools when necessary.`
});
```

### With Streaming

```typescript
const stream = await agent.stream({
  messages: [{ role: "user", content: "Search for TypeScript tutorials" }]
});

for await (const chunk of stream) {
  console.log(chunk);
}
```

## Creating Custom Agents

### Basic Custom Agent

```typescript
import { AgentExecutor } from "langchain/agents";
import { ChatOpenAI } from "@langchain/openai";

class CustomAgent {
  private executor: AgentExecutor;
  
  constructor(model: ChatOpenAI, tools: any[]) {
    this.executor = AgentExecutor.fromAgentAndTools({
      agent: this.createAgent(model, tools),
      tools: tools,
      verbose: true
    });
  }
  
  async run(input: string) {
    return await this.executor.invoke({ input });
  }
}
```

### With Memory

```typescript
import { BufferMemory } from "langchain/memory";

const memory = new BufferMemory({
  returnMessages: true,
  memoryKey: "chat_history"
});

const agent = createReactAgent({
  llm: model,
  tools: tools,
  checkpointSaver: memory  // For state persistence
});
```

## Agent Configuration

### Temperature and Model Selection

```typescript
const model = new ChatOpenAI({
  model: "gpt-4",           // Model to use
  temperature: 0,           // Deterministic (0) vs creative (1)
  maxTokens: 2000,          // Max response length
  timeout: 30000            // Timeout in ms
});
```

### Tool Configuration

```typescript
const tools = [
  new DuckDuckGoSearch({ maxResults: 5 }),
  new Calculator(),
  new WikipediaQueryRun({ topKResults: 3 })
];

const agent = createReactAgent({
  llm: model,
  tools: tools,
  messageModifier: `Available tools: search, calculate, wikipedia lookup.
Use them wisely to answer user questions.`
});
```

### Execution Options

```typescript
const result = await agent.invoke(
  { messages: [{ role: "user", content: "..." }] },
  {
    recursionLimit: 50,     // Max iterations
    streamMode: "values",   // or "updates", "messages"
    configurable: {
      thread_id: "user-123" // For conversation tracking
    }
  }
);
```

## Agent Types

### 1. ReAct Agent (Recommended)

Best for: Most use cases, especially when you need tool use

```typescript
import { createReactAgent } from "@langchain/langgraph/prebuilt";

const agent = createReactAgent({ llm, tools });
```

### 2. Conversational Agent

Best for: Chat applications with memory

```typescript
import { ConversationalAgent } from "langchain/agents";

const agent = ConversationalAgent.fromLLMAndTools(model, tools, {
  prefix: "You are a helpful assistant.",
  suffix: "Remember to use tools when needed."
});
```

### 3. Tool-Calling Agent

Best for: Models with native tool calling support (GPT-4, Claude)

```typescript
import { createToolCallingAgent } from "langchain/agents";

const agent = await createToolCallingAgent({
  llm: model,
  tools: tools,
  prompt: chatPromptTemplate
});
```

### 4. XML Agent

Best for: Models that work well with XML (Claude, Anthropic models)

```typescript
import { createXmlAgent } from "langchain/agents";

const agent = await createXmlAgent({
  llm: model,
  tools: tools,
  prompt: xmlPromptTemplate
});
```

## Best Practices

### 1. Start Simple

Begin with prebuilt agents before creating custom ones:

```typescript
// Good: Start here
const agent = createReactAgent({ llm, tools });

// Later: Customize when needed
const customAgent = createCustomReactAgent({ llm, tools, customLogic });
```

### 2. Provide Clear Instructions

```typescript
const agent = createReactAgent({
  llm: model,
  tools: tools,
  messageModifier: `You are an expert research assistant.
  
Rules:
1. Always cite sources when providing information
2. Use the search tool for current events
3. Use the calculator for mathematical operations
4. Be concise but thorough`
});
```

### 3. Handle Errors Gracefully

```typescript
try {
  const result = await agent.invoke({
    messages: [{ role: "user", content: userQuery }]
  });
  return result;
} catch (error) {
  if (error.message.includes("rate limit")) {
    // Implement retry logic
    await sleep(1000);
    return await agent.invoke({ messages: [{ role: "user", content: userQuery }] });
  }
  throw error;
}
```

### 4. Monitor Token Usage

```typescript
import { CallbackManager } from "@langchain/core/callbacks/manager";

const callbackManager = CallbackManager.fromHandlers({
  handleLLMEnd: async (output) => {
    console.log(`Tokens used: ${output.llmOutput?.tokenUsage}`);
  }
});

const model = new ChatOpenAI({
  model: "gpt-4",
  callbacks: callbackManager
});
```

### 5. Use Appropriate Recursion Limits

```typescript
// Simple queries: lower limit
await agent.invoke(input, { recursionLimit: 10 });

// Complex research: higher limit
await agent.invoke(input, { recursionLimit: 50 });

// Very complex: consider LangGraph instead
```

### 6. Test with Edge Cases

```typescript
const testCases = [
  "Simple question",
  "Question requiring tool use",
  "Multi-step complex query",
  "Ambiguous request",
  "Request outside of capabilities"
];

for (const testCase of testCases) {
  const result = await agent.invoke({
    messages: [{ role: "user", content: testCase }]
  });
  console.log(`Input: ${testCase}\nOutput: ${result}\n---`);
}
```

### 7. Leverage Streaming for UX

```typescript
import { StreamingTextResponse } from "ai";

export async function POST(req: Request) {
  const { message } = await req.json();
  
  const stream = await agent.stream({
    messages: [{ role: "user", content: message }]
  });
  
  return new StreamingTextResponse(stream);
}
```

## Common Patterns

### Agent with Fallback

```typescript
const primaryAgent = createReactAgent({ llm: gpt4, tools });
const fallbackAgent = createReactAgent({ llm: gpt35, tools });

async function runWithFallback(input: string) {
  try {
    return await primaryAgent.invoke({ messages: [{ role: "user", content: input }] });
  } catch (error) {
    console.log("Primary agent failed, using fallback");
    return await fallbackAgent.invoke({ messages: [{ role: "user", content: input }] });
  }
}
```

### Conditional Tool Selection

```typescript
function selectTools(userIntent: string) {
  const intentToTools = {
    research: [new DuckDuckGoSearch(), new WikipediaQueryRun()],
    calculation: [new Calculator()],
    coding: [new PythonREPLTool()],
    default: [new DuckDuckGoSearch()]
  };
  
  return intentToTools[userIntent] || intentToTools.default;
}

const tools = selectTools(detectedIntent);
const agent = createReactAgent({ llm: model, tools });
```

### Multi-Agent Collaboration

```typescript
const researchAgent = createReactAgent({
  llm: model,
  tools: [new DuckDuckGoSearch()],
  messageModifier: "You are a research specialist."
});

const summaryAgent = createReactAgent({
  llm: model,
  tools: [],
  messageModifier: "You summarize research findings."
});

// Research first, then summarize
const research = await researchAgent.invoke({ messages: [{ role: "user", content: query }] });
const summary = await summaryAgent.invoke({
  messages: [{ role: "user", content: `Summarize: ${research}` }]
});
```

## Debugging Agents

### Enable Verbose Mode

```typescript
const agent = createReactAgent({
  llm: model,
  tools: tools,
  verbose: true  // Logs all reasoning steps
});
```

### Use Callbacks for Tracing

```typescript
import { ConsoleCallbackHandler } from "@langchain/core/callbacks/console";

const agent = createReactAgent({
  llm: model.bind({ callbacks: [new ConsoleCallbackHandler()] }),
  tools: tools
});
```

### Inspect Intermediate Steps

```typescript
const result = await agent.invoke(
  { messages: [{ role: "user", content: query }] },
  { returnIntermediateSteps: true }
);

console.log("Steps taken:", result.intermediateSteps);
```
