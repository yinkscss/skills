# Models

LangChain provides a unified interface for all major LLM providers, making it easy to switch models and use multiple providers.

## Table of Contents

- [Quick Start](#quick-start)
- [Supported Providers](#supported-providers)
- [Model Configuration](#model-configuration)
- [Streaming](#streaming)
- [Structured Output](#structured-output)
- [Function Calling](#function-calling)
- [Fallbacks & Retries](#fallbacks--retries)
- [Cost Optimization](#cost-optimization)
- [Best Practices](#best-practices)

## Quick Start

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# OpenAI
openai_model = ChatOpenAI(model="gpt-4", temperature=0.7)

# Anthropic
anthropic_model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Google
google_model = ChatGoogleGenerativeAI(model="gemini-pro")

# Use any model the same way
response = openai_model.invoke("What is AI?")
```

## Supported Providers

### OpenAI

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4",  # or "gpt-4-turbo", "gpt-3.5-turbo"
    temperature=0.7,
    max_tokens=1000,
    api_key="your-key"  # or set OPENAI_API_KEY env var
)
```

**Models:**
- `gpt-4` - Most capable, best reasoning
- `gpt-4-turbo` - Faster, cheaper than GPT-4
- `gpt-3.5-turbo` - Fast, cheap, good for simple tasks
- `gpt-4o` - Optimized version with vision support

### Anthropic (Claude)

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=4096,
    api_key="your-key"  # or set ANTHROPIC_API_KEY env var
)
```

**Models:**
- `claude-3-5-sonnet-20241022` - Best balance of speed and intelligence
- `claude-3-opus-20240229` - Most capable, deep analysis
- `claude-3-sonnet-20240229` - Good balance
- `claude-3-haiku-20240307` - Fastest, most cost-effective

**Strengths:**
- Long context (200K tokens)
- Detailed, thoughtful responses
- Strong at analysis and writing
- Excellent instruction following

### Google (Gemini)

```python
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.7,
    google_api_key="your-key"
)
```

**Models:**
- `gemini-pro` - General purpose
- `gemini-pro-vision` - Multimodal (text + images)
- `gemini-1.5-pro` - Extended context, improved capabilities

### Azure OpenAI

```python
from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    azure_endpoint="https://your-resource.openai.azure.com/",
    api_key="your-key",
    api_version="2024-02-01",
    deployment_name="gpt-4"
)
```

### Ollama (Local Models)

```python
from langchain_community.llms import Ollama

model = Ollama(
    model="llama2",  # or "mistral", "codellama", etc.
    temperature=0.7
)
```

**Benefits:**
- Free, runs locally
- No API costs
- Privacy (data stays local)
- Good for development/testing

## Model Configuration

### Temperature

Controls randomness (0.0 = deterministic, 1.0 = creative):

```python
# Deterministic (for math, facts, code)
model = ChatOpenAI(temperature=0)

# Balanced (general use)
model = ChatOpenAI(temperature=0.7)

# Creative (stories, brainstorming)
model = ChatOpenAI(temperature=1.0)
```

### Max Tokens

Limit response length:

```python
model = ChatOpenAI(
    max_tokens=500,  # Max tokens in response
    model="gpt-4"
)
```

### Top P (Nucleus Sampling)

Alternative to temperature:

```python
model = ChatOpenAI(
    top_p=0.9,  # Consider top 90% probable tokens
    temperature=1
)
```

### Stop Sequences

Stop generation at specific tokens:

```python
model = ChatOpenAI(
    stop=["END", "\n\n\n"],  # Stop at these sequences
)
```

### Timeout

Set request timeout:

```python
model = ChatOpenAI(
    request_timeout=30,  # 30 second timeout
)
```

## Streaming

### Basic Streaming

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(streaming=True)

for chunk in model.stream("Write a poem"):
    print(chunk.content, end="", flush=True)
```

### Async Streaming

```python
async for chunk in model.astream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

### Streaming with Callbacks

```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

model = ChatOpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

response = model.invoke("Hello!")
```

## Structured Output

### Using Pydantic Models

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class Person(BaseModel):
    name: str = Field(description="Person's full name")
    age: int = Field(description="Person's age")
    email: str = Field(description="Email address")

model = ChatOpenAI(model="gpt-4")

# Get structured output
structured_model = model.with_structured_output(Person)
result = structured_model.invoke("Extract info: John Doe, 30 years old, john@example.com")

print(result.name)  # "John Doe"
print(result.age)   # 30
```

### JSON Mode

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4",
    model_kwargs={"response_format": {"type": "json_object"}}
)

response = model.invoke("Return JSON with name and age")
# Returns valid JSON
```

### With Schema

```python
from langchain.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=Person)

prompt = f"""Extract person information.
{parser.get_format_instructions()}

Text: John Smith is 25 years old"""

result = model.invoke(prompt)
parsed = parser.parse(result.content)
```

## Function Calling

### Define Functions

```python
from langchain_openai import ChatOpenAI

functions = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
]

model = ChatOpenAI(model="gpt-4")
response = model.invoke(
    "What's the weather in Paris?",
    functions=functions
)
```

### Using Tools

```python
from langchain.tools import tool
from langchain_openai import ChatOpenAI

@tool
def calculator(expression: str) -> float:
    """Calculate mathematical expressions."""
    return eval(expression)

model = ChatOpenAI(model="gpt-4")
model_with_tools = model.bind_tools([calculator])

response = model_with_tools.invoke("What is 15 * 23?")
```

### Forcing Function Calls

```python
# Force model to call a specific function
model = ChatOpenAI(model="gpt-4")
response = model.invoke(
    prompt,
    functions=functions,
    function_call={"name": "get_weather"}  # Must call this function
)
```

## Fallbacks & Retries

### Model Fallback

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

primary = ChatOpenAI(model="gpt-4")
fallback = ChatAnthropic(model="claude-3-5-sonnet-20241022")

model = primary.with_fallbacks([fallback])

# If GPT-4 fails, tries Claude
response = model.invoke("Hello")
```

### Multiple Fallbacks

```python
expensive = ChatOpenAI(model="gpt-4")
medium = ChatOpenAI(model="gpt-3.5-turbo")
cheap = ChatAnthropic(model="claude-3-haiku-20240307")

model = expensive.with_fallbacks([medium, cheap])
```

### Retry Logic

```python
from langchain.llms import OpenAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

model = ChatOpenAI(
    max_retries=3,  # Retry on failure
    request_timeout=30
)
```

### Custom Fallback Logic

```python
def try_with_fallback(prompt: str) -> str:
    models = [
        ChatOpenAI(model="gpt-4"),
        ChatAnthropic(model="claude-3-5-sonnet-20241022"),
        ChatOpenAI(model="gpt-3.5-turbo")
    ]
    
    for model in models:
        try:
            return model.invoke(prompt).content
        except Exception as e:
            print(f"Failed with {model}: {e}")
            continue
    
    raise Exception("All models failed")
```

## Cost Optimization

### Choose Appropriate Models

```python
# Expensive but capable
expensive = ChatOpenAI(model="gpt-4")  # ~$0.03/1K tokens

# Balanced
balanced = ChatOpenAI(model="gpt-3.5-turbo")  # ~$0.002/1K tokens

# Cheap for simple tasks
cheap = ChatAnthropic(model="claude-3-haiku-20240307")  # ~$0.00025/1K tokens
```

### Limit Token Usage

```python
model = ChatOpenAI(
    max_tokens=500,  # Limit response length
    model="gpt-4"
)
```

### Caching

```python
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

set_llm_cache(InMemoryCache())

model = ChatOpenAI()

# First call - hits API
response1 = model.invoke("What is AI?")

# Second call - returns cached result
response2 = model.invoke("What is AI?")
```

### SQLite Cache

```python
from langchain.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path=".langchain.db"))
```

### Prompt Caching (Anthropic)

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    # Enable prompt caching
    model_kwargs={"cache_control": {"type": "ephemeral"}}
)
```

## Best Practices

### 1. Model Selection

Choose based on task requirements:

| Task Type | Recommended Model | Why |
|-----------|------------------|-----|
| Complex reasoning | GPT-4, Claude Opus | Best capabilities |
| General chat | GPT-3.5, Claude Sonnet | Good balance |
| Simple tasks | Claude Haiku | Fast and cheap |
| Long context | Claude 3.5 Sonnet | 200K context |
| Code generation | GPT-4, Claude Sonnet | Strong coding |
| Creative writing | Claude Opus, GPT-4 | Best creativity |

### 2. Temperature Settings

```python
# Factual, deterministic tasks
model = ChatOpenAI(temperature=0, model="gpt-4")

# Balanced responses
model = ChatOpenAI(temperature=0.7, model="gpt-4")

# Creative tasks
model = ChatOpenAI(temperature=0.9, model="gpt-4")
```

### 3. Error Handling

```python
from openai import OpenAIError
from anthropic import AnthropicError

def safe_invoke(model, prompt):
    try:
        return model.invoke(prompt)
    except OpenAIError as e:
        print(f"OpenAI error: {e}")
        # Fallback logic
    except AnthropicError as e:
        print(f"Anthropic error: {e}")
        # Fallback logic
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
```

### 4. Context Management

```python
from langchain.schema import SystemMessage, HumanMessage

def create_messages(context: str, query: str) -> list:
    """Build message list with context."""
    return [
        SystemMessage(content=context),
        HumanMessage(content=query)
    ]

messages = create_messages(
    "You are a helpful assistant.",
    "What is the capital of France?"
)
response = model.invoke(messages)
```

### 5. Monitoring

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    response = model.invoke("Tell me a joke")
    print(f"Tokens: {cb.total_tokens}")
    print(f"Cost: ${cb.total_cost}")
```

### 6. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute):
    min_interval = 60.0 / calls_per_minute
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

@rate_limit(calls_per_minute=10)
def call_model(prompt):
    return model.invoke(prompt)
```

### 7. Testing

```python
def test_model_response():
    """Test model output."""
    model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    
    response = model.invoke("What is 2+2?")
    
    assert "4" in response.content
    assert len(response.content) < 100  # Should be concise
```

## Common Patterns

### Multi-Model Pipeline

```python
# Use different models for different tasks
cheap_model = ChatOpenAI(model="gpt-3.5-turbo")
expensive_model = ChatOpenAI(model="gpt-4")

# Quick classification
category = cheap_model.invoke("Classify: [user input]")

# Detailed response if needed
if category == "complex":
    response = expensive_model.invoke("[detailed prompt]")
else:
    response = cheap_model.invoke("[simple prompt]")
```

### Chain with Different Models

```python
from langchain.prompts import ChatPromptTemplate

# Summarizer with cheap model
summarizer = ChatPromptTemplate.from_template(
    "Summarize: {text}"
) | ChatOpenAI(model="gpt-3.5-turbo")

# Analyzer with expensive model
analyzer = ChatPromptTemplate.from_template(
    "Analyze deeply: {summary}"
) | ChatOpenAI(model="gpt-4")

# Chain them
summary = summarizer.invoke({"text": long_text})
analysis = analyzer.invoke({"summary": summary.content})
```

### Model Routing

```python
def route_to_model(query: str):
    """Route query to appropriate model."""
    if len(query) > 1000 or "complex" in query:
        return ChatOpenAI(model="gpt-4")
    return ChatOpenAI(model="gpt-3.5-turbo")

model = route_to_model(user_query)
response = model.invoke(user_query)
```

## Troubleshooting

### Rate Limit Errors

- Implement exponential backoff
- Use `max_retries` parameter
- Add delays between requests
- Consider upgrading API tier

### Timeout Errors

- Increase `request_timeout`
- Use streaming for long responses
- Split large requests

### Token Limit Errors

- Reduce `max_tokens`
- Shorten prompts
- Use models with larger context (Claude)

### Cost Management

- Start with cheaper models
- Use caching aggressively
- Implement request batching
- Monitor usage with callbacks
