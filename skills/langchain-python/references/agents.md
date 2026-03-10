# Agents

Agents use LLMs to decide which actions to take. They are ideal for tasks requiring dynamic decision-making and tool use.

## Table of Contents

- [Quick Start](#quick-start)
- [Creating Agents](#creating-agents)
- [Agent Types](#agent-types)
- [Tool Usage](#tool-usage)
- [Structured Output](#structured-output)
- [Agent Configuration](#agent-configuration)
- [Streaming](#streaming)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Quick Start

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain import hub

# Get default ReAct prompt
prompt = hub.pull("hwchase17/react")

# Define tools
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

tools = [
    Tool(
        name="Search",
        func=search,
        description="Search for information"
    )
]

# Create agent
llm = ChatOpenAI(temperature=0, model="gpt-4")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run
result = agent_executor.invoke({"input": "What is LangChain?"})
```

## Creating Agents

### Using create_react_agent (Recommended)

The ReAct pattern (Reasoning + Acting) is the recommended starting point:

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub

# Load prompt template
prompt = hub.pull("hwchase17/react")

llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    handle_parsing_errors=True
)
```

### Custom Agent with LangGraph

For more control, use LangGraph directly:

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
agent_executor = create_react_agent(
    llm, 
    tools,
    messages_modifier="You are a helpful assistant."
)

result = agent_executor.invoke(
    {"messages": [("user", "What is the weather?")]}
)
```

## Agent Types

### ReAct Agent

Best for most use cases. Combines reasoning and acting:

```python
from langchain.agents import create_react_agent

agent = create_react_agent(llm, tools, prompt)
```

**When to use:**
- General-purpose agents
- Multi-step reasoning required
- Tool selection needs explanation

### OpenAI Functions Agent

Optimized for OpenAI's function calling:

```python
from langchain.agents import create_openai_functions_agent

agent = create_openai_functions_agent(llm, tools, prompt)
```

**When to use:**
- Using OpenAI models (GPT-4, GPT-3.5)
- Need reliable tool calling
- Structured output required

### Structured Chat Agent

For agents that need to handle structured input/output:

```python
from langchain.agents import create_structured_chat_agent

agent = create_structured_chat_agent(llm, tools, prompt)
```

**When to use:**
- Complex tool arguments
- Multi-input tools
- Structured conversation flow

## Tool Usage

### Defining Tools

**Function-based:**

```python
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information online."""
    # Implementation
    return results
```

**Class-based:**

```python
from langchain.tools import BaseTool
from typing import Optional
from pydantic import Field

class SearchTool(BaseTool):
    name: str = "search"
    description: str = "Search for information"
    
    def _run(self, query: str) -> str:
        """Execute search."""
        return f"Results for {query}"
    
    async def _arun(self, query: str) -> str:
        """Async version."""
        return self._run(query)
```

### Tool Selection

Agents select tools based on:
1. Tool name and description
2. Current context
3. Previous tool results

**Best practices:**
- Clear, descriptive tool names
- Detailed descriptions
- Document expected input format
- Include examples in descriptions

```python
@tool
def calculate(expression: str) -> float:
    """Calculate mathematical expressions.
    
    Args:
        expression: Math expression like "2 + 2" or "sqrt(16)"
    
    Returns:
        Numerical result
        
    Examples:
        calculate("10 * 5") -> 50.0
        calculate("2 ** 8") -> 256.0
    """
    return eval(expression)
```

## Structured Output

### Using Pydantic Models

```python
from pydantic import BaseModel, Field
from langchain.agents import create_openai_functions_agent
from langchain.output_parsers import PydanticOutputParser

class SearchResult(BaseModel):
    title: str = Field(description="Result title")
    url: str = Field(description="Result URL")
    snippet: str = Field(description="Brief description")
    relevance: float = Field(description="Relevance score 0-1")

parser = PydanticOutputParser(pydantic_object=SearchResult)

# Add to prompt
format_instructions = parser.get_format_instructions()
prompt_template = f"""Answer the question.
{format_instructions}

Question: {{input}}"""
```

### Structured Tool Responses

```python
from langchain.tools import StructuredTool
from pydantic import BaseModel

class SearchInput(BaseModel):
    query: str = Field(description="Search query")
    max_results: int = Field(default=5, description="Max results")

class SearchOutput(BaseModel):
    results: list[str]
    count: int

def search_func(query: str, max_results: int = 5) -> SearchOutput:
    # Implementation
    return SearchOutput(results=["result1", "result2"], count=2)

search_tool = StructuredTool.from_function(
    func=search_func,
    name="search",
    description="Search tool",
    args_schema=SearchInput,
    return_direct=False
)
```

## Agent Configuration

### Key Parameters

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    
    # Control
    max_iterations=15,              # Max reasoning steps
    max_execution_time=60,          # Timeout in seconds
    early_stopping_method="generate", # or "force"
    
    # Error handling
    handle_parsing_errors=True,     # Recover from parsing errors
    
    # Output
    verbose=True,                   # Print reasoning steps
    return_intermediate_steps=True, # Include reasoning in output
    
    # Memory
    memory=memory                   # Optional conversation memory
)
```

### Custom System Prompts

```python
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert assistant. Use tools to answer accurately."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
```

## Streaming

### Streaming Agent Responses

```python
# Stream tokens
for chunk in agent_executor.stream({"input": "What is AI?"}):
    if "output" in chunk:
        print(chunk["output"], end="", flush=True)

# Stream with intermediate steps
for step in agent_executor.iter({"input": "Calculate 15 * 23"}):
    if "actions" in step:
        print(f"Action: {step['actions']}")
    if "output" in step:
        print(f"Output: {step['output']}")
```

### Async Streaming

```python
async for chunk in agent_executor.astream({"input": "Search for news"}):
    print(chunk)
```

## Error Handling

### Parsing Errors

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,
    # Or custom handler:
    # handle_parsing_errors="Check your output and try again."
)
```

### Tool Errors

```python
from langchain.tools import Tool

def safe_tool(query: str) -> str:
    try:
        # Tool logic
        return result
    except Exception as e:
        return f"Error: {str(e)}"

tool = Tool(
    name="search",
    func=safe_tool,
    description="Search tool with error handling"
)
```

### Timeout Handling

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_execution_time=30,  # 30 second timeout
)

try:
    result = agent_executor.invoke({"input": query})
except TimeoutError:
    print("Agent execution timed out")
```

## Best Practices

### 1. Tool Design

- **Clear descriptions**: Help the agent understand when to use each tool
- **Type hints**: Use Pydantic models for complex inputs
- **Error messages**: Return helpful error messages, not exceptions
- **Idempotency**: Tools should be safe to retry

### 2. Prompt Engineering

- **Explicit instructions**: Tell the agent exactly what you want
- **Examples**: Include few-shot examples for complex tasks
- **Constraints**: Specify output format and requirements
- **Context**: Provide relevant background information

### 3. Iteration Limits

- Set reasonable `max_iterations` (10-15 typical)
- Monitor for infinite loops
- Use `early_stopping_method` appropriately

### 4. Model Selection

- **GPT-4**: Best reasoning, use for complex tasks
- **GPT-3.5-turbo**: Faster, cheaper, good for simple tasks
- **Claude**: Excellent for long context and detailed analysis

### 5. Testing

```python
def test_agent():
    test_cases = [
        {"input": "What is 2+2?", "expected": "4"},
        {"input": "Search for Python", "expected_tool": "search"},
    ]
    
    for case in test_cases:
        result = agent_executor.invoke(case)
        # Assert expected behavior
```

### 6. Monitoring

```python
from langchain.callbacks import StdOutCallbackHandler

handler = StdOutCallbackHandler()
result = agent_executor.invoke(
    {"input": query},
    callbacks=[handler]
)
```

### 7. Cost Management

- Use streaming to cancel expensive operations
- Cache tool results when possible
- Choose appropriate models (GPT-3.5 vs GPT-4)
- Set token limits

```python
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    max_tokens=500,  # Limit response length
    temperature=0    # Deterministic for consistency
)
```

## Common Patterns

### Agent with Memory

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory
)
```

### Multi-Tool Agent

```python
tools = [
    search_tool,
    calculator_tool,
    weather_tool,
    database_tool
]

agent = create_react_agent(llm, tools, prompt)
```

### Agent with Fallback

```python
from langchain.llms import OpenAI
from langchain.chat_models import ChatAnthropic

primary_llm = ChatOpenAI(model="gpt-4")
fallback_llm = ChatAnthropic(model="claude-3-sonnet")

llm_with_fallback = primary_llm.with_fallbacks([fallback_llm])
agent = create_react_agent(llm_with_fallback, tools, prompt)
```

## Troubleshooting

### Agent Not Using Tools

1. Check tool descriptions are clear
2. Verify prompt includes tool information
3. Ensure model supports function calling
4. Check tool names are descriptive

### Infinite Loops

1. Set `max_iterations` limit
2. Review tool outputs for clarity
3. Check for circular dependencies
4. Use `verbose=True` to debug

### Parsing Errors

1. Enable `handle_parsing_errors=True`
2. Validate tool output formats
3. Check prompt formatting
4. Use structured output parsers

### High Costs

1. Use GPT-3.5 instead of GPT-4
2. Reduce `max_iterations`
3. Implement caching
4. Set `max_tokens` limits
