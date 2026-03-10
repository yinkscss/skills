---
name: langchain-typescript
description: Build AI agents and applications using LangChain and LangGraph in TypeScript. Use when building conversational AI, RAG systems, tool-using agents, multi-agent workflows, or any LLM-powered application. Covers agents (ReAct pattern), LangGraph (complex orchestration with state management), models (OpenAI, Anthropic, etc.), tools (custom and built-in), chains (LCEL), memory systems, deployment, and complete working examples.
license: MIT - See LICENSE.txt
---

# LangChain & LangGraph TypeScript

Build production-ready AI agents and LLM applications with LangChain and LangGraph in TypeScript.

## Overview

LangChain is a framework for developing applications powered by language models. It provides a standard interface for:
- **Agents**: Autonomous decision-making with tool use
- **Chains**: Composable sequences of operations
- **Models**: Unified interface for LLMs (OpenAI, Anthropic, etc.)
- **Tools**: Extend capabilities with external integrations
- **Memory**: Maintain conversation context

LangGraph extends LangChain for complex workflows with graph-based orchestration, state management, and human-in-the-loop support.

## When to Use

**Use LangChain when:**
- Building conversational AI or chatbots
- Creating agents that use tools (search, calculator, API calls)
- Implementing RAG (Retrieval-Augmented Generation) for Q&A
- Composing multi-step LLM workflows
- Integrating multiple LLMs or switching providers

**Use LangGraph when:**
- Workflows need conditional branching or loops
- Multiple agents collaborate
- State must persist across steps
- Human approval is required
- Complex error handling with retries

## Quick Start

### Simple Agent (10 Lines)

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { DuckDuckGoSearch } from "@langchain/community/tools/duckduckgo_search";

const model = new ChatOpenAI({ model: "gpt-4" });
const tools = [new DuckDuckGoSearch()];
const agent = createReactAgent({ llm: model, tools });

const result = await agent.invoke({
  messages: [{ role: "user", content: "What's the weather in NYC?" }]
});
```

### Installation

```bash
npm install @langchain/core @langchain/openai @langchain/langgraph langchain
```

## Core Capabilities

### 1. Agents

Agents use LLMs to decide which actions to take. See **[references/agents.md](references/agents.md)** for:
- ReAct agents (recommended starting point)
- Custom agent creation
- Agent configuration and tuning
- Tool selection and execution
- Streaming and error handling

**Common patterns:**
- Research agent with search tools
- Customer support agent with database access
- Coding agent with execution capabilities

### 2. LangGraph

Build complex multi-step workflows with graph-based orchestration. See **[references/langgraph.md](references/langgraph.md)** for:
- Graph construction (nodes, edges, conditional routing)
- State management and custom state schemas
- Human-in-the-loop workflows
- Persistence and checkpoints
- Parallel execution and loops

**Use when:**
- Your workflow has more than 5 steps
- You need branching logic or loops
- Multiple agents need to collaborate
- Human approval is required

### 3. Models

Unified interface for all major LLM providers. See **[references/models.md](references/models.md)** for:
- OpenAI, Anthropic, Google Gemini
- Model configuration (temperature, tokens, streaming)
- Structured output with Zod schemas
- Function calling
- Cost optimization with fallbacks

**Providers supported:**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3.5)
- Google (Gemini)
- Azure OpenAI

### 4. Tools

Extend agent capabilities with custom and built-in tools. See **[references/tools.md](references/tools.md)** for:
- Built-in tools (search, calculator, web browser)
- Creating custom tools with Zod schemas
- API integrations and database queries
- MCP (Model Context Protocol) support
- Error handling and rate limiting

**Template:** Use `assets/tool-template/` for custom tool creation.

### 5. Chains

Compose LLM operations with LCEL (LangChain Expression Language). See **[references/chains.md](references/chains.md)** for:
- Sequential and parallel execution
- Retrieval chains for RAG
- Conversation chains with memory
- Branching and routing logic
- Streaming and batching

**Pattern:**
```typescript
const chain = prompt.pipe(model).pipe(outputParser);
const result = await chain.invoke({ input: "..." });
```

### 6. Memory & State

Maintain context across interactions. See **[references/memory.md](references/memory.md)** for:
- Buffer memory (store all messages)
- Window memory (keep last N messages)
- Summary memory (summarize old context)
- Vector store memory (semantic search over history)
- Redis/database persistence

**For stateful workflows:** Use LangGraph's built-in state management instead of traditional memory.

### 7. Deployment & Production

Production-ready patterns and best practices. See **[references/deployment.md](references/deployment.md)** for:
- LangSmith integration (tracing, evaluation)
- Next.js and Express.js deployment
- Docker and containerization
- Monitoring, logging, and error tracking
- Performance optimization and caching

### 8. Complete Examples

Working code for common use cases. See **[references/examples.md](references/examples.md)** for:
- Simple chatbot with memory
- RAG application for Q&A
- Research agent with multiple tools
- Multi-agent collaboration system
- Human-in-the-loop approval workflow
- Streaming chat with Next.js

## Templates

Ready-to-use project templates in `assets/`:

### Simple Agent (`assets/simple-agent/`)
Basic agent with tool calling. Start here for most projects.

**Features:**
- ReAct pattern agent
- Tool integration (search, calculator)
- Streaming support
- ~50 lines of code

**Use for:** Chatbots, Q&A, simple automation

### LangGraph Agent (`assets/langgraph-agent/`)
Advanced agent with state management and graph orchestration.

**Features:**
- Graph-based workflow
- Conditional routing
- State persistence
- Multi-step reasoning

**Use for:** Complex workflows, multi-agent systems, human-in-the-loop

### RAG Application (`assets/rag-app/`)
Question-answering system over your documents.

**Features:**
- Document chunking and embedding
- Vector store integration
- Semantic search
- Context-aware generation

**Use for:** Document Q&A, knowledge bases, customer support

### Tool Template (`assets/tool-template/`)
Examples for creating custom tools.

**Includes:**
- Weather API tool
- Database query tool
- File system tool
- Email sending tool

**Use for:** Extending agent capabilities with custom integrations

## Scripts

### Initialize Project

```bash
tsx scripts/init_project.ts my-agent --template simple
```

Creates a new LangChain project from a template.

**Options:**
- `simple`: Basic agent (default)
- `langgraph`: Advanced graph agent
- `rag`: RAG application

## Decision Tree

```
Start: What are you building?
│
├─ Simple Q&A or chatbot?
│  └─ Use: Simple Agent template + Memory
│     Read: agents.md, memory.md
│
├─ Search/analyze documents?
│  └─ Use: RAG Application template
│     Read: rag-app/ template, chains.md
│
├─ Agent needs tools (search, calculator, API)?
│  └─ Use: Simple Agent + Custom Tools
│     Read: agents.md, tools.md, tool-template/
│
├─ Multi-step workflow with branching?
│  └─ Use: LangGraph Agent
│     Read: langgraph.md, examples.md
│
├─ Multiple agents working together?
│  └─ Use: LangGraph + Multi-Agent Pattern
│     Read: langgraph.md, examples.md (multi-agent section)
│
└─ Need human approval in workflow?
   └─ Use: LangGraph with Human-in-the-Loop
      Read: langgraph.md (human-in-the-loop section)
```

## Common Patterns

### Pattern 1: Agent with Tools

```typescript
const agent = createReactAgent({
  llm: model,
  tools: [searchTool, calculatorTool, customTool],
  messageModifier: "You are a helpful assistant."
});
```

**When:** Agent needs to use external capabilities

### Pattern 2: RAG for Q&A

```typescript
const vectorStore = await MemoryVectorStore.fromDocuments(docs, embeddings);
const retriever = vectorStore.asRetriever();
const chain = await createRetrievalChain({ retriever, combineDocsChain });
```

**When:** Answering questions from specific documents

### Pattern 3: Graph with Conditional Logic

```typescript
const graph = new StateGraph(state)
  .addNode("step1", node1)
  .addNode("step2", node2)
  .addConditionalEdges("step1", router, { continue: "step2", end: END });
```

**When:** Workflow needs branching based on results

### Pattern 4: Multi-Agent Collaboration

```typescript
const researcher = createReactAgent({ llm, tools: [search] });
const writer = createReactAgent({ llm, tools: [] });
const graph = new StateGraph(state)
  .addNode("research", researcher)
  .addNode("write", writer);
```

**When:** Different specialists handle different tasks

## Best Practices

1. **Start Simple**: Use basic agents before LangGraph
2. **Use Types**: Leverage TypeScript for type safety
3. **Handle Errors**: Wrap calls in try-catch
4. **Stream Responses**: Better UX for long operations
5. **Monitor Costs**: Track token usage
6. **Cache Results**: Avoid redundant API calls
7. **Use LangSmith**: Production tracing and debugging
8. **Test Thoroughly**: Unit and integration tests

## Environment Setup

Required environment variables:

```bash
# Model providers (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# LangSmith (optional but recommended)
LANGSMITH_API_KEY=...
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT=my-project

# Other services (as needed)
REDIS_URL=redis://localhost:6379
DATABASE_URL=...
```

## Architecture Guidance

### When to Use What

| Requirement | Use | Read |
|-------------|-----|------|
| Simple chatbot | Simple Agent + Memory | agents.md, memory.md |
| Tool-using agent | Simple Agent + Tools | agents.md, tools.md |
| Document Q&A | RAG Application | rag-app/, chains.md |
| Complex workflow | LangGraph | langgraph.md |
| Multi-agent | LangGraph + Multiple Nodes | langgraph.md, examples.md |
| Human oversight | LangGraph + Interrupts | langgraph.md |
| Production app | Any + LangSmith | deployment.md |

### Complexity Ladder

1. **Level 1: Single LLM Call**
   - Just use `ChatOpenAI` directly
   - No agent needed

2. **Level 2: Simple Agent**
   - Agent + a few tools
   - Linear workflow
   - Use `createReactAgent`

3. **Level 3: Chains**
   - Multi-step processing
   - RAG application
   - Use LCEL chains

4. **Level 4: LangGraph**
   - Conditional logic
   - Loops and branches
   - State management

5. **Level 5: Multi-Agent**
   - Multiple specialized agents
   - Complex orchestration
   - Human-in-the-loop

## Troubleshooting

### Agent Not Using Tools

- Check tool descriptions are clear
- Verify `messageModifier` mentions tools
- Ensure model supports function calling (GPT-4, Claude)

### Memory Not Persisting

- Verify checkpointer is configured
- Use same `thread_id` for conversations
- Check memory is passed to chain/agent

### High API Costs

- Use cheaper models (GPT-3.5 vs GPT-4)
- Implement caching
- Reduce `maxTokens`
- Use streaming to cancel early

### Slow Performance

- Enable streaming for better UX
- Use parallel execution where possible
- Cache repeated operations
- Consider model size tradeoffs

## Additional Resources

- **Official Docs**: https://js.langchain.com/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraphjs/
- **LangSmith**: https://smith.langchain.com/
- **Examples Repo**: https://github.com/langchain-ai/langchainjs

## Progressive Learning Path

1. **Start**: Read Quick Start, create simple agent
2. **Add Tools**: Read tools.md, create custom tool
3. **Add Memory**: Read memory.md, implement conversation history
4. **Build RAG**: Use rag-app template, understand retrieval
5. **Advanced**: Read langgraph.md, build stateful workflow
6. **Production**: Read deployment.md, integrate LangSmith
7. **Master**: Read examples.md, build multi-agent system

## Getting Help

- Check examples.md for similar use cases
- Review template READMEs in assets/
- Search official documentation
- Use LangSmith for debugging traces
