# LangGraph

LangGraph is a framework for building stateful, multi-step workflows with LLMs. It provides graph-based orchestration, state management, and human-in-the-loop support.

## Table of Contents

- [Overview](#overview)
- [Core Concepts](#core-concepts)
- [Building Graphs](#building-graphs)
- [State Management](#state-management)
- [Conditional Routing](#conditional-routing)
- [Persistence & Checkpoints](#persistence--checkpoints)
- [Human-in-the-Loop](#human-in-the-loop)
- [Streaming](#streaming)
- [Subgraphs](#subgraphs)
- [Best Practices](#best-practices)

## Overview

LangGraph extends LangChain for complex workflows that need:
- **Conditional branching**: Different paths based on results
- **Loops**: Retry logic, iterative refinement
- **State persistence**: Resume after failures
- **Human oversight**: Approval gates, corrections
- **Multi-agent collaboration**: Specialized agents working together

### When to Use LangGraph

Use LangGraph when:
- Workflow has >5 steps
- Need branching or loops
- State must persist across steps
- Human approval required
- Multiple agents collaborate
- Error recovery is critical

Use simple chains/agents when:
- Linear workflow (A → B → C)
- No branching logic
- Single-shot operations
- No state persistence needed

## Core Concepts

### Graphs

A graph consists of:
- **Nodes**: Functions that process state
- **Edges**: Connections between nodes
- **State**: Shared data structure
- **Entry point**: START node
- **Exit point**: END node

```python
from langgraph.graph import StateGraph, START, END

# Define graph structure
graph = StateGraph(StateClass)
graph.add_node("step1", node_function_1)
graph.add_node("step2", node_function_2)
graph.add_edge(START, "step1")
graph.add_edge("step1", "step2")
graph.add_edge("step2", END)

# Compile and run
app = graph.compile()
result = app.invoke(initial_state)
```

### Nodes

Nodes are functions that:
- Take state as input
- Return state updates
- Can call LLMs, tools, or other logic

```python
from typing import TypedDict

class State(TypedDict):
    messages: list
    count: int

def my_node(state: State) -> dict:
    """Node function."""
    # Process state
    new_count = state["count"] + 1
    
    # Return updates (merged into state)
    return {"count": new_count}
```

### Edges

**Regular edges** (fixed routing):
```python
graph.add_edge("node_a", "node_b")  # Always go A → B
```

**Conditional edges** (dynamic routing):
```python
def router(state: State) -> str:
    if state["count"] > 5:
        return "done"
    return "continue"

graph.add_conditional_edges(
    "node_a",
    router,
    {
        "continue": "node_b",
        "done": END
    }
)
```

## Building Graphs

### Basic Graph

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Define state
class AgentState(TypedDict):
    messages: list[str]
    next_action: str

# Define nodes
def process_input(state: AgentState) -> dict:
    message = state["messages"][-1]
    return {"next_action": "respond"}

def generate_response(state: AgentState) -> dict:
    response = f"Processed: {state['messages'][-1]}"
    return {"messages": state["messages"] + [response]}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("process", process_input)
graph.add_node("respond", generate_response)

graph.add_edge(START, "process")
graph.add_edge("process", "respond")
graph.add_edge("respond", END)

# Compile
app = graph.compile()

# Run
result = app.invoke({
    "messages": ["Hello!"],
    "next_action": ""
})
print(result["messages"])
```

### Agent Graph

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
tools = [search_tool, calculator_tool]

# Create agent with built-in graph
agent = create_react_agent(llm, tools)

# Use like any graph
result = agent.invoke({
    "messages": [("user", "What is 25 * 17?")]
})
```

### Custom Agent Graph

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import Annotated
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], "Messages in conversation"]

def should_continue(state: AgentState) -> str:
    """Decide whether to continue or end."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

def call_model(state: AgentState) -> dict:
    """Invoke the LLM."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Add edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)
workflow.add_edge("tools", "agent")

app = workflow.compile()
```

## State Management

### State Schemas

**TypedDict (recommended):**

```python
from typing import TypedDict, Annotated

class MyState(TypedDict):
    messages: list[str]
    count: int
    user_id: str
```

**Pydantic (for validation):**

```python
from pydantic import BaseModel, Field

class MyState(BaseModel):
    messages: list[str] = Field(default_factory=list)
    count: int = 0
    user_id: str = Field(..., min_length=1)
```

### State Reducers

Control how state updates are merged:

```python
from typing import Annotated
from operator import add

class State(TypedDict):
    # Append to list (default for lists)
    messages: Annotated[list, add]
    
    # Replace value (default for primitives)
    count: int
    
    # Custom reducer
    total: Annotated[int, lambda x, y: x + y]
```

### Accessing State

Nodes receive full state and return partial updates:

```python
def my_node(state: State) -> dict:
    # Read from state
    current_count = state["count"]
    messages = state["messages"]
    
    # Return updates only
    return {
        "count": current_count + 1,
        "messages": ["New message"]  # Appended due to reducer
    }
```

## Conditional Routing

### Simple Conditions

```python
def route_by_count(state: State) -> str:
    """Route based on state."""
    if state["count"] < 3:
        return "continue"
    return "finish"

graph.add_conditional_edges(
    "process",
    route_by_count,
    {
        "continue": "process",  # Loop back
        "finish": END
    }
)
```

### Complex Routing

```python
def intelligent_router(state: State) -> str:
    """Route based on multiple conditions."""
    message = state["messages"][-1]
    
    if "error" in message.lower():
        return "error_handler"
    elif state["retries"] > 3:
        return "give_up"
    elif "complete" in message.lower():
        return "finalize"
    else:
        return "continue_processing"

graph.add_conditional_edges(
    "main_node",
    intelligent_router,
    {
        "error_handler": "handle_error",
        "give_up": END,
        "finalize": "final_step",
        "continue_processing": "next_step"
    }
)
```

### Routing with Multiple Outputs

```python
def multi_path_router(state: State) -> list[str]:
    """Return multiple next nodes (parallel execution)."""
    tasks = []
    
    if state["need_search"]:
        tasks.append("search")
    if state["need_calculation"]:
        tasks.append("calculate")
    
    return tasks or ["default"]

graph.add_conditional_edges(
    "dispatcher",
    multi_path_router,
    ["search", "calculate", "default"]
)
```

## Persistence & Checkpoints

### Memory Checkpoint

```python
from langgraph.checkpoint.memory import MemorySaver

# Add persistence
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Run with thread ID
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke(initial_state, config)

# Continue same thread
result2 = app.invoke(new_input, config)
```

### SQLite Checkpoint

```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
app = graph.compile(checkpointer=checkpointer)

# Use same as MemorySaver
config = {"configurable": {"thread_id": "session-456"}}
result = app.invoke(state, config)
```

### Resume from Checkpoint

```python
# Get checkpoint history
history = app.get_state_history(config)

for checkpoint in history:
    print(f"Step: {checkpoint.metadata['step']}")
    print(f"State: {checkpoint.values}")

# Resume from specific checkpoint
result = app.invoke(
    None,  # No new input
    {
        "configurable": {
            "thread_id": "user-123",
            "checkpoint_id": specific_checkpoint_id
        }
    }
)
```

## Human-in-the-Loop

### Interrupts

```python
from langgraph.checkpoint.memory import MemorySaver

graph.add_node("needs_approval", approval_node)

# Compile with interrupt
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["needs_approval"]  # Pause before this node
)

# First run - stops at interrupt
config = {"configurable": {"thread_id": "abc"}}
result = app.invoke(input_data, config)

# Get current state
state = app.get_state(config)
print(f"Paused at: {state.next}")

# Continue after approval
result = app.invoke(None, config)  # Resume
```

### Dynamic Interrupts

```python
def needs_review(state: State) -> bool:
    """Decide if human review is needed."""
    return state["confidence"] < 0.8

graph.add_node("review_point", review_node)

app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=lambda state: ["review_point"] if needs_review(state) else []
)
```

### Update State During Interrupt

```python
# Graph is paused
state = app.get_state(config)

# Human modifies state
updated_state = {
    **state.values,
    "approved": True,
    "corrections": "Use formal tone"
}

# Update and continue
app.update_state(config, updated_state)
result = app.invoke(None, config)
```

## Streaming

### Stream Node Outputs

```python
for chunk in app.stream(input_data, config):
    node_name = list(chunk.keys())[0]
    node_output = chunk[node_name]
    print(f"{node_name}: {node_output}")
```

### Stream Tokens

```python
for chunk in app.stream(input_data, config, stream_mode="values"):
    # Get messages from state
    if "messages" in chunk:
        print(chunk["messages"][-1].content, end="", flush=True)
```

### Stream with Updates

```python
async for chunk in app.astream(input_data, config, stream_mode="updates"):
    # Only state changes
    print(f"Update: {chunk}")
```

## Subgraphs

### Creating Subgraphs

```python
from langgraph.graph import StateGraph

# Subgraph for specialized task
def create_research_graph():
    subgraph = StateGraph(ResearchState)
    subgraph.add_node("search", search_node)
    subgraph.add_node("analyze", analyze_node)
    subgraph.add_edge(START, "search")
    subgraph.add_edge("search", "analyze")
    subgraph.add_edge("analyze", END)
    return subgraph.compile()

# Main graph
main_graph = StateGraph(MainState)
main_graph.add_node("research", create_research_graph())
main_graph.add_node("write", write_node)
main_graph.add_edge(START, "research")
main_graph.add_edge("research", "write")
main_graph.add_edge("write", END)

app = main_graph.compile()
```

### Parallel Subgraphs

```python
def parallel_node(state: State) -> dict:
    """Run multiple subgraphs in parallel."""
    # Execute subgraphs
    results = []
    for subgraph in [research_graph, analysis_graph]:
        result = subgraph.invoke(state)
        results.append(result)
    
    return {"results": results}
```

## Best Practices

### 1. Node Granularity

**Too fine-grained (bad):**
```python
graph.add_node("add_1", lambda s: {"count": s["count"] + 1})
graph.add_node("multiply_2", lambda s: {"count": s["count"] * 2})
graph.add_node("subtract_5", lambda s: {"count": s["count"] - 5})
```

**Appropriate granularity (good):**
```python
graph.add_node("process_numbers", process_all_math)
graph.add_node("validate_result", validate)
```

### 2. State Design

**Keep state minimal:**
```python
# Bad - too much
class State(TypedDict):
    messages: list
    intermediate_step_1: str
    intermediate_step_2: str
    temp_var: int
    debug_info: dict

# Good - essentials only
class State(TypedDict):
    messages: list
    result: str
```

### 3. Error Handling

```python
def safe_node(state: State) -> dict:
    """Node with error handling."""
    try:
        result = risky_operation(state)
        return {"result": result, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}

def error_router(state: State) -> str:
    if state.get("error"):
        return "error_handler"
    return "continue"
```

### 4. Testing Graphs

```python
def test_graph():
    """Test graph execution."""
    test_state = {
        "messages": ["test input"],
        "count": 0
    }
    
    result = app.invoke(test_state)
    
    assert result["count"] > 0
    assert len(result["messages"]) > 1
```

### 5. Monitoring

```python
from langchain.callbacks import StdOutCallbackHandler

app = graph.compile()

result = app.invoke(
    input_data,
    {"callbacks": [StdOutCallbackHandler()]}
)
```

### 6. Resource Management

```python
def cleanup_node(state: State) -> dict:
    """Cleanup resources."""
    # Close connections, clear cache, etc.
    return {"cleaned": True}

# Always add cleanup
graph.add_edge("main_work", "cleanup")
graph.add_edge("cleanup", END)
```

## Common Patterns

### Retry Loop

```python
def should_retry(state: State) -> str:
    if state.get("error") and state["retries"] < 3:
        return "retry"
    elif state.get("error"):
        return "failed"
    return "success"

graph.add_node("attempt", attempt_task)
graph.add_conditional_edges(
    "attempt",
    should_retry,
    {
        "retry": "attempt",
        "failed": "handle_failure",
        "success": END
    }
)
```

### Multi-Agent Collaboration

```python
class MultiAgentState(TypedDict):
    messages: list
    next_agent: str

def router(state: MultiAgentState) -> str:
    return state["next_agent"]

graph.add_node("researcher", researcher_agent)
graph.add_node("writer", writer_agent)
graph.add_node("reviewer", reviewer_agent)

graph.add_conditional_edges(
    "researcher",
    router,
    {
        "writer": "writer",
        "reviewer": "reviewer",
        "done": END
    }
)
```

### Human Review Loop

```python
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["human_review"]
)

# First invocation
result = app.invoke(data, config)

# Human reviews and approves
approved = human_approval_ui()

if approved:
    # Continue
    result = app.invoke(None, config)
else:
    # Reject and restart
    app.update_state(config, {"restart": True})
    result = app.invoke(None, config)
```

## Troubleshooting

### State Not Updating

- Check reducer annotations
- Ensure nodes return dicts
- Verify state schema matches

### Infinite Loops

- Add iteration counters
- Set maximum loop counts
- Use `interrupt_after` for debugging

### Checkpoints Not Working

- Verify checkpointer is passed to `compile()`
- Check `thread_id` is consistent
- Ensure state is serializable

### Performance Issues

- Reduce node granularity
- Minimize state size
- Use streaming for large outputs
- Cache expensive operations
