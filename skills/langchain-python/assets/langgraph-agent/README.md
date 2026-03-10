# LangGraph Agent Template

Advanced agent using LangGraph for complex workflows with state management.

## Setup

1. Install dependencies:
```bash
pip install langchain langchain-openai langgraph python-dotenv
```

2. Create `.env` file:
```bash
OPENAI_API_KEY=your-api-key-here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
```

3. Run:
```bash
python graph_agent.py
```

## Features

- State management with TypedDict
- Conditional routing based on state
- Iteration tracking and limits
- Persistence with MemorySaver
- Multiple tools integration
- Graph-based workflow

## Architecture

```
START → agent → [continue/end] → finalize → END
           ↑         |
           └─────────┘ (loop)
```

## Customization

### Add More Nodes

```python
def new_node(state: AgentState):
    # Node logic
    return {"status": "updated"}

workflow.add_node("new_node", new_node)
workflow.add_edge("agent", "new_node")
```

### Modify Routing Logic

```python
def should_continue(state: AgentState) -> str:
    if state["custom_condition"]:
        return "custom_path"
    return "default_path"
```

### Add Human-in-the-Loop

```python
app = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["finalize"]  # Pause for approval
)
```

## Advanced Features

### Parallel Execution

```python
workflow.add_edge("start", ["node1", "node2"])  # Run in parallel
```

### Subgraphs

```python
subgraph = create_subgraph()
workflow.add_node("subgraph", subgraph)
```

### Streaming

```python
for chunk in app.stream(initial_state, config):
    print(chunk)
```

## Production Considerations

1. Add proper error handling in nodes
2. Implement retry logic for failed operations
3. Add monitoring and logging
4. Use persistent checkpointer (SQLite, Postgres)
5. Implement proper state validation
