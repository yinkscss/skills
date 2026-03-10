# LangGraph Reference

## Overview

LangGraph is a framework for building stateful, multi-actor applications with language models. It enables complex agent orchestration through graph-based workflows with nodes and edges.

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Quick Start](#quick-start)
3. [State Management](#state-management)
4. [Graph Construction](#graph-construction)
5. [Conditional Logic](#conditional-logic)
6. [Human-in-the-Loop](#human-in-the-loop)
7. [Persistence & Checkpoints](#persistence--checkpoints)
8. [Advanced Patterns](#advanced-patterns)

## Core Concepts

### Graph Structure

- **Nodes**: Functions that process state (agents, tools, transformations)
- **Edges**: Connections defining execution flow
- **State**: Data passed between nodes
- **Conditional Edges**: Dynamic routing based on state

### When to Use LangGraph vs Simple Agents

**Use Simple Agents when:**
- Linear tool calling workflow
- Single decision-making process
- Less than 5 steps
- No complex branching logic

**Use LangGraph when:**
- Multi-step workflows with branching
- Multiple agents collaborating
- State needs to persist across steps
- Loops and conditional logic required
- Human oversight needed
- Complex error handling and retries

## Quick Start

### Basic Graph

```typescript
import { StateGraph, MessagesAnnotation, START, END } from "@langchain/langgraph";
import { ChatOpenAI } from "@langchain/openai";

// Define a simple node
const callModel = async (state: typeof MessagesAnnotation.State) => {
  const model = new ChatOpenAI({ model: "gpt-4" });
  const response = await model.invoke(state.messages);
  return { messages: [response] };
};

// Build the graph
const graph = new StateGraph(MessagesAnnotation)
  .addNode("model", callModel)
  .addEdge(START, "model")
  .addEdge("model", END)
  .compile();

// Run it
const result = await graph.invoke({
  messages: [{ role: "user", content: "Hello!" }]
});
```

### Installation

```bash
npm install @langchain/langgraph @langchain/core @langchain/openai
```

## State Management

### Built-in State Annotations

**MessagesAnnotation**: For chat applications

```typescript
import { MessagesAnnotation } from "@langchain/langgraph";

// Automatically manages message history
const graph = new StateGraph(MessagesAnnotation)
  .addNode("chatNode", async (state) => {
    // state.messages contains full conversation
    return { messages: [newMessage] };
  });
```

### Custom State

Define your own state schema:

```typescript
import { Annotation } from "@langchain/langgraph";

const AgentState = Annotation.Root({
  messages: Annotation<BaseMessage[]>({
    reducer: (x, y) => x.concat(y),  // How to merge state updates
  }),
  currentStep: Annotation<string>(),
  results: Annotation<any[]>({
    reducer: (x, y) => x.concat(y),
  }),
  loopCount: Annotation<number>({
    reducer: (x, y) => x + y,
    default: () => 0,
  }),
});

const graph = new StateGraph(AgentState)
  .addNode("step1", async (state) => {
    return {
      currentStep: "processing",
      loopCount: 1
    };
  });
```

### State Reducers

Control how state updates are merged:

```typescript
const StateAnnotation = Annotation.Root({
  // Replace entire value
  status: Annotation<string>(),
  
  // Append to array
  results: Annotation<string[]>({
    reducer: (curr, update) => curr.concat(update)
  }),
  
  // Sum numbers
  totalCost: Annotation<number>({
    reducer: (curr, update) => curr + update,
    default: () => 0
  }),
  
  // Merge objects
  metadata: Annotation<Record<string, any>>({
    reducer: (curr, update) => ({ ...curr, ...update }),
    default: () => ({})
  })
});
```

## Graph Construction

### Adding Nodes

```typescript
const graph = new StateGraph(MessagesAnnotation)
  .addNode("researcher", researchNode)
  .addNode("analyzer", analyzerNode)
  .addNode("writer", writerNode);
```

### Static Edges

```typescript
// Start → researcher → analyzer → writer → End
graph
  .addEdge(START, "researcher")
  .addEdge("researcher", "analyzer")
  .addEdge("analyzer", "writer")
  .addEdge("writer", END);
```

### Parallel Execution

```typescript
// Execute multiple nodes in parallel
graph
  .addEdge(START, "nodeA")
  .addEdge(START, "nodeB")
  .addEdge(START, "nodeC")
  .addEdge("nodeA", "combiner")
  .addEdge("nodeB", "combiner")
  .addEdge("nodeC", "combiner")
  .addEdge("combiner", END);
```

## Conditional Logic

### Conditional Edges

Route based on state:

```typescript
function router(state: typeof AgentState.State): string {
  const lastMessage = state.messages[state.messages.length - 1];
  
  if (lastMessage.content.includes("error")) {
    return "error_handler";
  }
  if (state.loopCount > 10) {
    return END;
  }
  return "continue";
}

graph
  .addNode("processor", processorNode)
  .addNode("error_handler", errorNode)
  .addNode("continue", continueNode)
  .addConditionalEdges(
    "processor",
    router,
    {
      "error_handler": "error_handler",
      "continue": "continue",
      [END]: END
    }
  );
```

### Tool Decision Making

```typescript
import { ToolNode } from "@langchain/langgraph/prebuilt";

// Create a tool node
const tools = [searchTool, calculatorTool];
const toolNode = new ToolNode(tools);

function shouldContinue(state: typeof MessagesAnnotation.State) {
  const lastMessage = state.messages[state.messages.length - 1];
  
  // If the LLM called tools, execute them
  if ("tool_calls" in lastMessage && lastMessage.tool_calls?.length > 0) {
    return "tools";
  }
  // Otherwise, end
  return END;
}

const graph = new StateGraph(MessagesAnnotation)
  .addNode("agent", callModel)
  .addNode("tools", toolNode)
  .addEdge(START, "agent")
  .addConditionalEdges("agent", shouldContinue, {
    tools: "tools",
    [END]: END
  })
  .addEdge("tools", "agent")  // Loop back after tool execution
  .compile();
```

### Loops and Iteration

```typescript
const graph = new StateGraph(AgentState)
  .addNode("process", async (state) => {
    // Do work
    return { loopCount: 1 };
  })
  .addEdge(START, "process")
  .addConditionalEdges("process", (state) => {
    return state.loopCount < 5 ? "process" : END;  // Loop or finish
  }, {
    "process": "process",
    [END]: END
  })
  .compile();
```

## Human-in-the-Loop

### Interruptions

Pause execution for human review:

```typescript
import { MemorySaver } from "@langchain/langgraph";

const checkpointer = new MemorySaver();

const graph = new StateGraph(AgentState)
  .addNode("draft", draftNode)
  .addNode("review", reviewNode)
  .addNode("finalize", finalizeNode)
  .addEdge(START, "draft")
  .addEdge("draft", "review")
  // Interrupt before finalize for human review
  .addEdge("review", "finalize")
  .addEdge("finalize", END)
  .compile({
    checkpointer,
    interruptBefore: ["finalize"]  // Pause here
  });

// Initial run (stops at finalize)
const thread = { configurable: { thread_id: "1" } };
await graph.invoke(input, thread);

// Human reviews and approves
// Resume execution
await graph.invoke(null, thread);
```

### Manual State Updates

```typescript
// Get current state
const state = await graph.getState(thread);
console.log("Current state:", state.values);

// Manually update state
await graph.updateState(thread, {
  messages: [{ role: "user", content: "Human feedback: approve changes" }]
});

// Continue execution
await graph.invoke(null, thread);
```

### Approval Workflows

```typescript
const graph = new StateGraph(WorkflowState)
  .addNode("generate", generateNode)
  .addNode("await_approval", awaitApprovalNode)
  .addNode("execute", executeNode)
  .addEdge(START, "generate")
  .addEdge("generate", "await_approval")
  .addConditionalEdges("await_approval", (state) => {
    return state.approved ? "execute" : "generate";
  })
  .addEdge("execute", END)
  .compile({
    checkpointer,
    interruptBefore: ["await_approval"]
  });
```

## Persistence & Checkpoints

### Memory Saver

```typescript
import { MemorySaver } from "@langchain/langgraph";

const checkpointer = new MemorySaver();

const graph = new StateGraph(MessagesAnnotation)
  .addNode("chat", chatNode)
  .addEdge(START, "chat")
  .addEdge("chat", END)
  .compile({ checkpointer });

// Each thread has isolated state
const thread1 = { configurable: { thread_id: "user-1" } };
const thread2 = { configurable: { thread_id: "user-2" } };

await graph.invoke({ messages: [...] }, thread1);
await graph.invoke({ messages: [...] }, thread2);
```

### Custom Checkpointer

For production persistence (Redis, PostgreSQL, etc.):

```typescript
import { BaseCheckpointSaver } from "@langchain/langgraph";

class DatabaseCheckpointer extends BaseCheckpointSaver {
  async getTuple(config: RunnableConfig): Promise<CheckpointTuple> {
    // Load from database
  }
  
  async put(config: RunnableConfig, checkpoint: Checkpoint): Promise<void> {
    // Save to database
  }
  
  async list(config: RunnableConfig): Promise<CheckpointTuple[]> {
    // List checkpoints
  }
}

const checkpointer = new DatabaseCheckpointer();
const graph = graph.compile({ checkpointer });
```

### State History

```typescript
// Get all checkpoints for a thread
const history = await graph.getStateHistory(thread);

for await (const state of history) {
  console.log("Checkpoint:", state.values);
  console.log("Step:", state.metadata?.step);
}
```

## Advanced Patterns

### Subgraphs

Compose graphs within graphs:

```typescript
// Define a subgraph
const subGraph = new StateGraph(SubState)
  .addNode("step1", step1Node)
  .addNode("step2", step2Node)
  .addEdge(START, "step1")
  .addEdge("step1", "step2")
  .addEdge("step2", END)
  .compile();

// Use in parent graph
const parentGraph = new StateGraph(ParentState)
  .addNode("prepare", prepareNode)
  .addNode("subprocess", subGraph)  // Embed subgraph
  .addNode("finalize", finalizeNode)
  .addEdge(START, "prepare")
  .addEdge("prepare", "subprocess")
  .addEdge("subprocess", "finalize")
  .addEdge("finalize", END)
  .compile();
```

### Multi-Agent Collaboration

```typescript
const ResearcherState = Annotation.Root({
  query: Annotation<string>(),
  findings: Annotation<string[]>({ reducer: (x, y) => x.concat(y) })
});

const researcher = new StateGraph(ResearcherState)
  .addNode("search", searchNode)
  .addNode("analyze", analyzeNode)
  .addEdge(START, "search")
  .addEdge("search", "analyze")
  .addEdge("analyze", END)
  .compile();

const writer = new StateGraph(WriterState)
  .addNode("draft", draftNode)
  .addNode("edit", editNode)
  .addEdge(START, "draft")
  .addEdge("draft", "edit")
  .addEdge("edit", END)
  .compile();

// Orchestrate multiple agents
const orchestrator = new StateGraph(OrchestratorState)
  .addNode("research", researcher)
  .addNode("write", writer)
  .addEdge(START, "research")
  .addEdge("research", "write")
  .addEdge("write", END)
  .compile();
```

### Streaming Updates

```typescript
// Stream node outputs as they complete
const stream = await graph.stream(
  { messages: [{ role: "user", content: "Hello" }] },
  { streamMode: "updates" }  // "values", "updates", or "messages"
);

for await (const update of stream) {
  console.log("Update from node:", update);
}
```

### Error Handling

```typescript
const graph = new StateGraph(AgentState)
  .addNode("risky_operation", async (state) => {
    try {
      const result = await riskyFunction();
      return { result, error: null };
    } catch (error) {
      return { result: null, error: error.message };
    }
  })
  .addConditionalEdges("risky_operation", (state) => {
    return state.error ? "error_handler" : "success";
  })
  .addNode("error_handler", errorHandlerNode)
  .addNode("success", successNode)
  .addEdge(START, "risky_operation")
  .addEdge("error_handler", END)
  .addEdge("success", END)
  .compile();
```

### Dynamic Graph Construction

```typescript
function buildGraph(userPreferences: UserPrefs) {
  const graph = new StateGraph(AppState);
  
  // Add nodes based on preferences
  if (userPreferences.enableSearch) {
    graph.addNode("search", searchNode);
  }
  
  if (userPreferences.enableAnalysis) {
    graph.addNode("analyze", analyzeNode);
  }
  
  // Connect dynamically
  graph.addEdge(START, userPreferences.enableSearch ? "search" : "analyze");
  
  return graph.compile();
}
```

## Best Practices

### 1. Start Simple, Add Complexity

```typescript
// Phase 1: Linear flow
graph
  .addEdge(START, "step1")
  .addEdge("step1", "step2")
  .addEdge("step2", END);

// Phase 2: Add conditional logic
graph.addConditionalEdges("step2", router);

// Phase 3: Add loops and human-in-the-loop
```

### 2. Use Descriptive Node Names

```typescript
// Good
.addNode("search_documentation", searchNode)
.addNode("analyze_results", analyzeNode)
.addNode("generate_summary", summaryNode)

// Bad
.addNode("node1", searchNode)
.addNode("node2", analyzeNode)
.addNode("node3", summaryNode)
```

### 3. Keep State Minimal

```typescript
// Good: Only essential state
const AgentState = Annotation.Root({
  query: Annotation<string>(),
  results: Annotation<string[]>()
});

// Bad: Bloated state
const AgentState = Annotation.Root({
  query: Annotation<string>(),
  results: Annotation<string[]>(),
  intermediateResults1: Annotation<any>(),
  intermediateResults2: Annotation<any>(),
  debugInfo: Annotation<any>(),
  tempData: Annotation<any>()
});
```

### 4. Use Checkpointers for Production

```typescript
// Development
const checkpointer = new MemorySaver();

// Production
const checkpointer = new RedisCheckpointer(redisClient);
```

### 5. Visualize Your Graph

```typescript
// Generate Mermaid diagram
const mermaid = graph.getGraph().drawMermaid();
console.log(mermaid);

// Or use LangSmith Studio for visual debugging
```

## Common Pitfalls

### Infinite Loops

```typescript
// Bad: No exit condition
graph.addEdge("process", "process");

// Good: Conditional exit
graph.addConditionalEdges("process", (state) => {
  return state.done ? END : "process";
});
```

### State Not Updating

```typescript
// Bad: Forgetting to return updated state
const node = async (state) => {
  state.value = "new";  // Direct mutation doesn't work
};

// Good: Return new state
const node = async (state) => {
  return { value: "new" };
};
```

### Missing Checkpointer

```typescript
// Bad: Using threads without checkpointer
const thread = { configurable: { thread_id: "1" } };
await graph.invoke(input, thread);  // State not saved!

// Good: Provide checkpointer
const graph = builder.compile({ checkpointer: new MemorySaver() });
```
