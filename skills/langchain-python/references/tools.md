# Tools

Tools extend agent capabilities by providing access to external functionality, APIs, databases, and custom logic.

## Table of Contents

- [Quick Start](#quick-start)
- [Creating Tools](#creating-tools)
- [Built-in Tools](#built-in-tools)
- [Tool Schemas](#tool-schemas)
- [Async Tools](#async-tools)
- [Error Handling](#error-handling)
- [MCP Integration](#mcp-integration)
- [Best Practices](#best-practices)

## Quick Start

```python
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information online."""
    # Implementation
    return f"Results for: {query}"

@tool
def calculate(expression: str) -> float:
    """Calculate mathematical expressions."""
    return eval(expression)

# Use with agent
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI

tools = [search, calculate]
agent = create_react_agent(
    ChatOpenAI(model="gpt-4"),
    tools,
    prompt
)
```

## Creating Tools

### Using @tool Decorator

Simplest method:

```python
from langchain.tools import tool

@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get current weather for a location.
    
    Args:
        location: City name or coordinates
        unit: Temperature unit (celsius or fahrenheit)
    
    Returns:
        Weather description
    """
    # API call
    return f"Weather in {location}: 20°{unit[0].upper()}"

# Tool automatically extracts:
# - name: "get_weather"
# - description: from docstring
# - args: from function signature
```

### Using StructuredTool

For more control:

```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(description="City name")
    unit: str = Field(default="celsius", description="Temperature unit")

def get_weather_func(location: str, unit: str = "celsius") -> str:
    """Get weather."""
    return f"Weather in {location}"

weather_tool = StructuredTool.from_function(
    func=get_weather_func,
    name="GetWeather",
    description="Get current weather for any location",
    args_schema=WeatherInput,
    return_direct=False  # Return to agent, not directly to user
)
```

### Using BaseTool Class

Maximum flexibility:

```python
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="Search query")
    max_results: int = Field(default=5, description="Maximum results")

class SearchTool(BaseTool):
    name: str = "search"
    description: str = "Search the internet for information"
    args_schema: Type[BaseModel] = SearchInput
    
    def _run(self, query: str, max_results: int = 5) -> str:
        """Synchronous implementation."""
        # Search logic
        return f"Found {max_results} results for: {query}"
    
    async def _arun(self, query: str, max_results: int = 5) -> str:
        """Async implementation."""
        # Async search logic
        return f"Found {max_results} results for: {query}"

search_tool = SearchTool()
```

## Built-in Tools

### DuckDuckGo Search

```python
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
result = search.run("Python programming")
```

### Wikipedia

```python
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
result = wikipedia.run("Artificial Intelligence")
```

### Python REPL

```python
from langchain_experimental.tools import PythonREPLTool

python_repl = PythonREPLTool()
result = python_repl.run("print(2 + 2)")
```

### Shell Tool

```python
from langchain_community.tools import ShellTool

shell = ShellTool()
result = shell.run("ls -la")
```

### File Management

```python
from langchain_community.tools import (
    ReadFileTool,
    WriteFileTool,
    ListDirectoryTool
)

read_tool = ReadFileTool()
write_tool = WriteFileTool()
list_tool = ListDirectoryTool()

content = read_tool.run("file.txt")
write_tool.run({"file_path": "output.txt", "text": "Hello"})
files = list_tool.run("./")
```

### HTTP Requests

```python
from langchain_community.tools import RequestsGetTool, RequestsPostTool

get_tool = RequestsGetTool()
post_tool = RequestsPostTool()

response = get_tool.run("https://api.example.com/data")
```

### Calculator

```python
from langchain.chains import LLMMathChain
from langchain_openai import ChatOpenAI

llm_math = LLMMathChain.from_llm(ChatOpenAI(temperature=0))
result = llm_math.run("What is 15% of 250?")
```

## Tool Schemas

### Basic Schema

```python
from pydantic import BaseModel, Field

class EmailInput(BaseModel):
    to: str = Field(description="Recipient email address")
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email body content")
    
@tool(args_schema=EmailInput)
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    # Email logic
    return f"Email sent to {to}"
```

### Complex Schema

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class DatabaseQueryInput(BaseModel):
    query: str = Field(description="SQL query to execute")
    database: str = Field(description="Database name")
    limit: Optional[int] = Field(default=100, description="Result limit")
    priority: Priority = Field(default=Priority.MEDIUM)
    
    @validator("query")
    def validate_query(cls, v):
        # Prevent dangerous queries
        forbidden = ["DROP", "DELETE", "UPDATE"]
        if any(word in v.upper() for word in forbidden):
            raise ValueError("Query contains forbidden operations")
        return v

@tool(args_schema=DatabaseQueryInput)
def query_database(query: str, database: str, limit: int = 100, priority: str = "medium") -> str:
    """Execute a read-only database query."""
    # Database logic
    return f"Executed query on {database}"
```

### Multiple Return Types

```python
from typing import Union, Dict, List

@tool
def search_products(query: str) -> Union[List[Dict], str]:
    """Search for products.
    
    Returns:
        List of product dicts, or error string
    """
    try:
        # Search logic
        return [
            {"name": "Product 1", "price": 29.99},
            {"name": "Product 2", "price": 39.99}
        ]
    except Exception as e:
        return f"Error: {str(e)}"
```

## Async Tools

### Async Function Tool

```python
import aiohttp
from langchain.tools import tool

@tool
async def async_fetch(url: str) -> str:
    """Fetch URL content asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### Async BaseTool

```python
from langchain.tools import BaseTool
import asyncio

class AsyncSearchTool(BaseTool):
    name: str = "async_search"
    description: str = "Asynchronous search tool"
    
    def _run(self, query: str) -> str:
        """Sync fallback."""
        return asyncio.run(self._arun(query))
    
    async def _arun(self, query: str) -> str:
        """Async implementation."""
        await asyncio.sleep(1)  # Simulate API call
        return f"Results for: {query}"
```

### Using Async Tools

```python
from langchain.agents import create_react_agent

# Tools can be mixed (sync and async)
tools = [sync_tool, async_tool]

agent = create_react_agent(llm, tools, prompt)

# Async invoke
result = await agent.ainvoke({"input": "Search for something"})
```

## Error Handling

### Tool-Level Error Handling

```python
@tool
def safe_tool(query: str) -> str:
    """Tool with built-in error handling."""
    try:
        # Risky operation
        result = risky_api_call(query)
        return result
    except APIError as e:
        return f"API Error: {str(e)}"
    except ValueError as e:
        return f"Invalid input: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
```

### Validation

```python
from pydantic import BaseModel, Field, validator

class ToolInput(BaseModel):
    url: str = Field(description="URL to process")
    
    @validator("url")
    def validate_url(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v

@tool(args_schema=ToolInput)
def fetch_url(url: str) -> str:
    """Fetch URL with validation."""
    # Implementation
    return "Content"
```

### Timeout Handling

```python
import signal
from contextlib import contextmanager

class TimeoutError(Exception):
    pass

@contextmanager
def timeout(seconds):
    def handler(signum, frame):
        raise TimeoutError()
    
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

@tool
def slow_operation(query: str) -> str:
    """Operation with timeout."""
    try:
        with timeout(10):
            # Long-running operation
            result = expensive_api_call(query)
            return result
    except TimeoutError:
        return "Operation timed out after 10 seconds"
```

## MCP Integration

Model Context Protocol (MCP) allows tools to provide dynamic context to models.

### Basic MCP Tool

```python
from langchain.tools import tool
from typing import Dict, Any

@tool
def mcp_enabled_tool(query: str) -> Dict[str, Any]:
    """Tool that returns structured data for MCP.
    
    Returns data that can be used as context by the model.
    """
    return {
        "result": "Query result",
        "metadata": {
            "source": "API",
            "confidence": 0.95,
            "timestamp": "2024-01-01"
        },
        "context": "Additional context for the model"
    }
```

### MCP Context Provider

```python
from langchain.tools import BaseTool

class MCPTool(BaseTool):
    name: str = "mcp_search"
    description: str = "Search with MCP context"
    
    def _run(self, query: str) -> dict:
        """Return structured context."""
        results = perform_search(query)
        
        return {
            "answer": results["top_result"],
            "sources": results["sources"],
            "related_topics": results["related"],
            # MCP uses this for context
            "context": {
                "search_quality": "high",
                "result_count": len(results["sources"]),
                "categories": results["categories"]
            }
        }
```

## Best Practices

### 1. Clear Descriptions

```python
# Bad
@tool
def tool1(x: str) -> str:
    """Does something."""
    return x

# Good
@tool
def search_customer_database(customer_id: str) -> str:
    """Search for customer information by ID.
    
    Retrieves customer profile including name, email, purchase history,
    and account status from the customer database.
    
    Args:
        customer_id: Unique customer identifier (format: CUST-XXXXX)
    
    Returns:
        JSON string with customer details, or error message if not found
        
    Example:
        search_customer_database("CUST-12345")
        -> '{"name": "John Doe", "email": "john@example.com", ...}'
    """
    # Implementation
    return customer_data
```

### 2. Type Safety

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SearchInput(BaseModel):
    query: str = Field(..., min_length=1, max_length=200)
    filters: Optional[List[str]] = Field(default=None)
    date_from: Optional[datetime] = Field(default=None)
    date_to: Optional[datetime] = Field(default=None)

@tool(args_schema=SearchInput)
def advanced_search(
    query: str,
    filters: Optional[List[str]] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None
) -> str:
    """Advanced search with type-safe inputs."""
    # Implementation
    return results
```

### 3. Idempotency

```python
@tool
def idempotent_update(record_id: str, value: str) -> str:
    """Update that can be safely retried.
    
    Uses idempotency key to prevent duplicate updates.
    """
    idempotency_key = f"{record_id}-{hash(value)}"
    
    if already_processed(idempotency_key):
        return get_cached_result(idempotency_key)
    
    result = perform_update(record_id, value)
    cache_result(idempotency_key, result)
    return result
```

### 4. Rate Limiting

```python
from functools import wraps
import time

def rate_limit(calls_per_second: float):
    """Rate limit decorator for tools."""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait = min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@tool
@rate_limit(calls_per_second=2)
def api_call(query: str) -> str:
    """API call with rate limiting."""
    return call_api(query)
```

### 5. Logging

```python
import logging

logger = logging.getLogger(__name__)

@tool
def logged_tool(query: str) -> str:
    """Tool with comprehensive logging."""
    logger.info(f"Tool called with query: {query}")
    
    try:
        result = process_query(query)
        logger.info(f"Tool succeeded: {len(result)} chars returned")
        return result
    except Exception as e:
        logger.error(f"Tool failed: {str(e)}", exc_info=True)
        return f"Error: {str(e)}"
```

### 6. Testing

```python
def test_tool():
    """Test tool behavior."""
    tool = my_custom_tool
    
    # Test normal operation
    result = tool.run("test query")
    assert isinstance(result, str)
    assert len(result) > 0
    
    # Test error handling
    result = tool.run("")
    assert "error" in result.lower()
    
    # Test schema
    assert tool.args_schema is not None
```

### 7. Documentation

```python
@tool
def well_documented_tool(
    param1: str,
    param2: int = 10,
    param3: Optional[str] = None
) -> dict:
    """One-line summary of what the tool does.
    
    More detailed description of the tool's purpose, when to use it,
    and any important considerations.
    
    Args:
        param1: Description of param1, including format and constraints
        param2: Description of param2 (default: 10)
        param3: Optional parameter description
    
    Returns:
        Dictionary containing:
            - 'result': The main result
            - 'metadata': Additional information
            - 'status': Success/failure status
    
    Raises:
        ValueError: When param1 is invalid
        APIError: When external API fails
    
    Examples:
        >>> tool.run(param1="test", param2=5)
        {'result': '...', 'metadata': {...}, 'status': 'success'}
        
        >>> tool.run(param1="another test", param3="optional")
        {'result': '...', 'metadata': {...}, 'status': 'success'}
    """
    # Implementation
    return {
        "result": f"Processed {param1}",
        "metadata": {"param2": param2},
        "status": "success"
    }
```

## Common Patterns

### Tool Factory

```python
def create_api_tool(api_name: str, endpoint: str, api_key: str):
    """Factory for creating API tools."""
    
    @tool
    def api_tool(query: str) -> str:
        f"""Query the {api_name} API."""
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{endpoint}?q={query}", headers=headers)
        return response.text
    
    api_tool.name = f"{api_name}_api"
    return api_tool

# Create tools for different APIs
weather_tool = create_api_tool("Weather", "https://api.weather.com", key1)
news_tool = create_api_tool("News", "https://api.news.com", key2)
```

### Tool Composition

```python
@tool
def search_and_summarize(query: str) -> str:
    """Search and summarize results."""
    # Use multiple tools
    search_results = search_tool.run(query)
    summary = summarize_tool.run(search_results)
    return summary
```

### Conditional Tool Loading

```python
def get_tools_for_user(user_role: str) -> List[BaseTool]:
    """Load tools based on user permissions."""
    basic_tools = [search_tool, calculator_tool]
    
    if user_role == "admin":
        return basic_tools + [database_tool, system_tool]
    elif user_role == "analyst":
        return basic_tools + [database_tool]
    else:
        return basic_tools
```

## Troubleshooting

### Tool Not Being Called

1. Improve tool description
2. Add examples to description
3. Verify tool name is clear
4. Check model supports function calling

### Type Errors

1. Use proper Pydantic schemas
2. Add type hints everywhere
3. Validate inputs explicitly

### Performance Issues

1. Add caching for expensive operations
2. Implement async versions
3. Use rate limiting
4. Optimize tool logic

### Error Messages Not Helpful

1. Return structured error info
2. Include context in errors
3. Log errors separately
4. Provide recovery suggestions
