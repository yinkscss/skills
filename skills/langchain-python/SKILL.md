---
name: langchain-python
description: Build AI agents and applications using LangChain and LangGraph in Python. Use when building conversational AI, RAG systems, tool-using agents, multi-agent workflows, or any LLM-powered application. Covers agents (ReAct pattern, tool use), LangGraph (complex orchestration with state management, conditional routing, persistence), models (OpenAI, Anthropic, Google, etc.), tools (custom and built-in), chains (LCEL, retrieval, conversation), memory systems (short-term, long-term, vector-based), RAG (document loading, embeddings, vector stores, retrieval strategies), deployment (LangSmith, FastAPI, Docker), and complete working examples.
license: MIT - See LICENSE.txt
---

# LangChain & LangGraph Python

Build production-ready AI agents and LLM applications with LangChain and LangGraph in Python.

## Overview

LangChain is a framework for developing applications powered by language models. It provides a standard interface for:
- **Agents**: Autonomous decision-making with tool use
- **Chains**: Composable sequences of operations  
- **Models**: Unified interface for LLMs (OpenAI, Anthropic, etc.)
- **Tools**: Extend capabilities with external integrations
- **Memory**: Maintain conversation context

LangGraph extends LangChain for complex workflows with graph-based orchestration, state management, and human-in-the-loop support.

## Quick Start

### Simple Agent (10 Lines)

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain import hub

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

llm = ChatOpenAI(model="gpt-4")
agent = create_react_agent(llm, [search], hub.pull("hwchase17/react"))
executor = AgentExecutor(agent=agent, tools=[search])

result = executor.invoke({"input": "What's the weather in NYC?"})
```

### Installation

```bash
pip install langchain langchain-openai langchain-community langgraph
```

## Core Capabilities

### 1. Agents

Agents use LLMs to decide which actions to take. See **[references/agents.md](references/agents.md)** for:
- ReAct agents (recommended starting point)
- OpenAI Functions agents
- Structured chat agents
- Custom agent creation
- Tool selection and execution
- Structured output
- Streaming and error handling

**Common patterns:**
- Research agent with search tools
- Customer support agent with database access
- Coding agent with execution capabilities

### 2. LangGraph

Build complex multi-step workflows with graph-based orchestration. See **[references/langgraph.md](references/langgraph.md)** for:
- Graph construction (nodes, edges, conditional routing)
- State management with TypedDict
- Persistence and checkpoints (MemorySaver, SQLite)
- Human-in-the-loop workflows
- Subgraphs and parallel execution
- Streaming results

**Use when:**
- Your workflow has more than 5 steps
- You need branching logic or loops
- Multiple agents need to collaborate
- Human approval is required
- Error recovery is critical

### 3. Models

Unified interface for all major LLM providers. See **[references/models.md](references/models.md)** for:
- OpenAI (GPT-4, GPT-3.5, GPT-4o)
- Anthropic (Claude 3.5, Claude 3 Opus)
- Google (Gemini Pro, Gemini Vision)
- Model configuration (temperature, tokens, streaming)
- Structured output with Pydantic schemas
- Function calling
- Fallbacks and retries
- Cost optimization with caching

**Providers supported:**
- OpenAI, Azure OpenAI
- Anthropic (Claude)
- Google (Gemini)
- Ollama (local models)

### 4. Tools

Extend agent capabilities with custom and built-in tools. See **[references/tools.md](references/tools.md)** for:
- Creating tools with `@tool` decorator
- StructuredTool and BaseTool classes
- Built-in tools (search, calculator, file operations)
- Tool schemas with Pydantic
- Async tool implementations
- Error handling and validation
- MCP (Model Context Protocol) integration

**Template:** Use `assets/simple-agent/` for basic tool patterns.

### 5. Chains

Compose LLM operations with LCEL (LangChain Expression Language). See **[references/chains.md](references/chains.md)** for:
- Sequential and parallel execution
- Retrieval chains for RAG
- Conversation chains with memory
- Branching and routing logic
- Streaming and batching
- Error handling with fallbacks

**Pattern:**
```python
from langchain.schema.runnable import RunnablePassthrough

chain = prompt | model | output_parser
result = chain.invoke({"input": "..."})
```

### 6. Memory & State

Maintain context across interactions. See **[references/memory.md](references/memory.md)** for:
- Buffer memory (store all messages)
- Window memory (keep last N messages)
- Summary memory (summarize old context)
- Token buffer memory (limit by tokens)
- Entity memory (track facts about entities)
- Vector store memory (semantic search over history)
- Redis/PostgreSQL persistence

**For stateful workflows:** Use LangGraph's built-in state management instead of traditional memory.

### 7. RAG (Retrieval-Augmented Generation)

Answer questions using your own documents. See **[references/rag.md](references/rag.md)** for:
- Document loaders (PDF, text, web, CSV, JSON)
- Text splitting strategies
- Embeddings (OpenAI, HuggingFace, Cohere)
- Vector stores (FAISS, Chroma, Pinecone, Weaviate)
- Retrieval strategies (similarity, MMR, hybrid)
- Advanced patterns (HyDE, multi-query, reranking)

**Template:** Use `assets/rag-app/` for complete RAG implementation.

### 8. Deployment & Production

Production-ready patterns and best practices. See **[references/deployment.md](references/deployment.md)** for:
- LangSmith integration (tracing, evaluation, monitoring)
- FastAPI deployment patterns
- Docker and Kubernetes
- Monitoring, logging, and metrics
- Error handling and retry logic
- Performance optimization and caching
- Security best practices
- Scaling strategies

### 9. Complete Examples

Working code for common use cases. See **[references/examples.md](references/examples.md)** for:
- Simple chatbot with memory
- RAG application for Q&A
- Agent with multiple tools
- Multi-agent collaboration system
- Human-in-the-loop approval workflow
- Streaming chat implementation

## Templates

Ready-to-use project templates in `assets/`:

### Simple Agent (`assets/simple-agent/`)

Basic agent with tool calling. Start here for most projects.

**Features:**
- ReAct pattern agent
- Tool integration (search, calculator)
- Error handling
- ~80 lines of code

**Use for:** Chatbots, Q&A, simple automation

### LangGraph Agent (`assets/langgraph-agent/`)

Advanced agent with state management and graph orchestration.

**Features:**
- Graph-based workflow
- State management with TypedDict
- Conditional routing
- Iteration tracking
- Persistence with checkpointer

**Use for:** Complex workflows, multi-agent systems, human-in-the-loop

### RAG Application (`assets/rag-app/`)

Question-answering system over your documents.

**Features:**
- Document loading and processing
- Vector store creation and persistence
- MMR retrieval for diversity
- Context-aware generation
- Source citation

**Use for:** Document Q&A, knowledge bases, customer support

## Scripts

### Initialize Project

```bash
python scripts/init_project.py my-agent --template simple
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
│     Read: rag.md, chains.md
│
├─ Agent needs tools (search, calculator, API)?
│  └─ Use: Simple Agent + Custom Tools
│     Read: agents.md, tools.md
│
├─ Multi-step workflow with branching?
│  └─ Use: LangGraph Agent
│     Read: langgraph.md
│
├─ Multiple agents working together?
│  └─ Use: LangGraph + Multi-Agent Pattern
│     Read: langgraph.md, examples.md
│
└─ Need human approval in workflow?
   └─ Use: LangGraph with Human-in-the-Loop
      Read: langgraph.md (human-in-the-loop section)
```

## Common Patterns

### Pattern 1: Agent with Tools

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

agent = create_react_agent(
    ChatOpenAI(model="gpt-4"),
    [search_tool, calculator_tool, custom_tool],
    hub.pull("hwchase17/react")
)

executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

**When:** Agent needs to use external capabilities

### Pattern 2: RAG for Q&A

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

retriever = vectorstore.as_retriever()
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)
```

**When:** Answering questions from specific documents

### Pattern 3: Graph with Conditional Logic

```python
from langgraph.graph import StateGraph, START, END

workflow = StateGraph(StateDict)
workflow.add_node("step1", node1)
workflow.add_node("step2", node2)
workflow.add_conditional_edges("step1", router, {
    "continue": "step2",
    "end": END
})
```

**When:** Workflow needs branching based on results

### Pattern 4: Multi-Agent Collaboration

```python
from langgraph.prebuilt import create_react_agent

researcher = create_react_agent(llm, [search], "You are a researcher")
writer = create_react_agent(llm, [], "You are a writer")

workflow = StateGraph(State)
workflow.add_node("research", researcher)
workflow.add_node("write", writer)
```

**When:** Different specialists handle different tasks

## Best Practices

1. **Start Simple**: Use basic agents before LangGraph
2. **Use Type Hints**: Leverage Python typing for clarity
3. **Handle Errors**: Wrap calls in try-except
4. **Stream Responses**: Better UX for long operations
5. **Monitor Costs**: Track token usage with callbacks
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
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=my-project

# Other services (as needed)
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://...
```

## Architecture Guidance

### When to Use What

| Requirement | Use | Read |
|-------------|-----|------|
| Simple chatbot | Simple Agent + Memory | agents.md, memory.md |
| Tool-using agent | Simple Agent + Tools | agents.md, tools.md |
| Document Q&A | RAG Application | rag.md, chains.md |
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
   - Use `create_react_agent`

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
- Verify model supports function calling (GPT-4, Claude)
- Ensure tools are in the tools list
- Use `verbose=True` to debug

### Memory Not Persisting

- Verify checkpointer is configured
- Use same `thread_id` for conversations
- Check memory is passed to chain/agent

### High API Costs

- Use cheaper models (GPT-3.5 vs GPT-4)
- Implement caching
- Reduce `max_tokens`
- Use streaming to cancel early

### Slow Performance

- Enable streaming for better UX
- Use parallel execution where possible
- Cache repeated operations
- Consider model size tradeoffs

## Additional Resources

- **Official Docs**: https://python.langchain.com/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **LangSmith**: https://smith.langchain.com/
- **Examples Repo**: https://github.com/langchain-ai/langchain

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
- Enable `verbose=True` for detailed logging
