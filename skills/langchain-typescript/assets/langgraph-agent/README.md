# LangGraph Agent Template

An advanced agent using LangGraph for complex orchestration with state management and conditional logic.

## Features

- **State Management**: Maintains conversation context
- **Conditional Routing**: Dynamic decision making
- **Tool Integration**: Seamless tool execution
- **Persistence**: State saved across sessions
- **Streaming**: Real-time output

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run:
```bash
npm run dev
```

## Key Concepts

### Graph Structure

```
START → agent → tools → agent → END
              ↓
              END (if no tools needed)
```

### State Annotation

```typescript
import { MessagesAnnotation } from "@langchain/langgraph";

// Automatically manages message history
const graph = new StateGraph(MessagesAnnotation);
```

### Conditional Edges

```typescript
function shouldContinue(state) {
  const lastMessage = state.messages[state.messages.length - 1];
  
  if (lastMessage.tool_calls?.length > 0) {
    return "tools";  // Execute tools
  }
  
  return END;  // Finish
}
```

## Customization

### Add More Nodes

```typescript
const workflow = new StateGraph(MessagesAnnotation)
  .addNode("researcher", researchNode)
  .addNode("analyzer", analyzerNode)
  .addNode("writer", writerNode)
  .addEdge(START, "researcher")
  .addEdge("researcher", "analyzer")
  .addEdge("analyzer", "writer")
  .addEdge("writer", END);
```

### Add Custom State

```typescript
import { Annotation } from "@langchain/langgraph";

const CustomState = Annotation.Root({
  messages: Annotation<BaseMessage[]>(),
  step: Annotation<number>(),
  results: Annotation<any[]>()
});

const graph = new StateGraph(CustomState);
```

### Use Persistent Storage

```typescript
import { RedisSaver } from "@langchain/langgraph-checkpoint-redis";

const checkpointer = new RedisSaver(redisClient);
const graph = workflow.compile({ checkpointer });
```

## Advanced Patterns

### Human-in-the-Loop

```typescript
const graph = workflow.compile({
  checkpointer,
  interruptBefore: ["critical_step"]
});

// Workflow pauses before critical_step
await graph.invoke(input, config);

// Human reviews and approves
await graph.updateState(config, { approved: true });

// Continue execution
await graph.invoke(null, config);
```

### Loops

```typescript
.addConditionalEdges("process", (state) => {
  return state.count < 5 ? "process" : END;
}, {
  process: "process",
  [END]: END
});
```
