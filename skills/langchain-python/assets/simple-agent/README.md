# Simple Agent Template

A basic LangChain agent with tools for search and calculation.

## Setup

1. Install dependencies:
```bash
pip install langchain langchain-openai langchain-community python-dotenv
```

2. Create `.env` file:
```bash
OPENAI_API_KEY=your-api-key-here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
```

3. Run:
```bash
python agent.py
```

## Features

- ReAct agent pattern
- Search tool (mock implementation)
- Calculator tool
- Error handling
- Verbose output for debugging

## Customization

### Add New Tools

```python
@tool
def my_tool(input: str) -> str:
    """Tool description."""
    # Implementation
    return result

tools = [search, calculator, my_tool]
```

### Change Model

```python
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
```

### Adjust Agent Behavior

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=15,  # More reasoning steps
    early_stopping_method="generate"
)
```

## Production Considerations

1. Replace mock search with real API (DuckDuckGo, SerpAPI, etc.)
2. Add input validation
3. Implement rate limiting
4. Add logging
5. Handle API errors gracefully
