# Memory

Memory systems enable agents and chains to maintain context across interactions.

## Table of Contents

- [Overview](#overview)
- [Short-Term Memory](#short-term-memory)
- [Long-Term Memory](#long-term-memory)
- [Memory Types](#memory-types)
- [LangGraph Memory](#langgraph-memory)
- [Vector Store Memory](#vector-store-memory)
- [Custom Memory](#custom-memory)
- [Best Practices](#best-practices)

## Overview

Memory in LangChain comes in two forms:

**Short-term memory:**
- Conversation history within a session
- Recent context for current task
- Cleared when session ends

**Long-term memory:**
- Facts and information across sessions
- User preferences and profile
- Persisted to database/disk

## Short-Term Memory

### Buffer Memory

Stores all messages in a buffer:

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

memory = ConversationBufferMemory()
llm = ChatOpenAI()

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

response1 = conversation.predict(input="Hi, I'm Alice")
response2 = conversation.predict(input="What's my name?")
# Remembers: "Alice"
```

### Window Memory

Keeps only the last N messages:

```python
from langchain.memory import ConversationBufferWindowMemory

# Keep last 5 messages
memory = ConversationBufferWindowMemory(k=5)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

### Token Buffer Memory

Limits memory by token count:

```python
from langchain.memory import ConversationTokenBufferMemory

memory = ConversationTokenBufferMemory(
    llm=llm,
    max_token_limit=2000  # Max tokens to keep
)
```

### Summary Memory

Summarizes old messages:

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(llm=llm)

# Automatically summarizes old conversations
conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

### Summary Buffer Memory

Combination of summary and buffer:

```python
from langchain.memory import ConversationSummaryBufferMemory

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=1000  # Summarize when exceeding limit
)
```

## Long-Term Memory

### Entity Memory

Tracks facts about entities:

```python
from langchain.memory import ConversationEntityMemory

memory = ConversationEntityMemory(llm=llm)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)

# Stores facts: "Alice likes Python", "Bob works at Google"
response = conversation.predict(input="Alice likes Python")
# Later retrieves relevant entity facts
```

### Knowledge Graph Memory

Structured entity relationships:

```python
from langchain.memory import ConversationKGMemory

memory = ConversationKGMemory(llm=llm)

# Builds knowledge graph of entities and relationships
conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

### File-Based Persistence

```python
import json
from langchain.memory import ConversationBufferMemory

# Save memory
memory = ConversationBufferMemory()
# ... use memory ...

# Save to file
with open("memory.json", "w") as f:
    json.dump(memory.dict(), f)

# Load from file
with open("memory.json", "r") as f:
    saved_memory = json.load(f)
    
memory = ConversationBufferMemory(**saved_memory)
```

### Database Persistence

```python
from langchain.memory import PostgresChatMessageHistory

# Postgres-backed memory
message_history = PostgresChatMessageHistory(
    connection_string="postgresql://user:pass@localhost/dbname",
    session_id="user_123"
)

memory = ConversationBufferMemory(
    chat_memory=message_history
)
```

## Memory Types

### Chat Message History

```python
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()

history.add_user_message("Hello!")
history.add_ai_message("Hi there!")

# Get messages
messages = history.messages
```

### Redis Memory

```python
from langchain.memory import RedisChatMessageHistory

message_history = RedisChatMessageHistory(
    url="redis://localhost:6379",
    session_id="session_123"
)

memory = ConversationBufferMemory(
    chat_memory=message_history
)
```

### MongoDB Memory

```python
from langchain.memory import MongoDBChatMessageHistory

message_history = MongoDBChatMessageHistory(
    connection_string="mongodb://localhost:27017",
    session_id="user_456"
)
```

### Multiple Memories

```python
from langchain.memory import CombinedMemory

# Combine different memory types
buffer_memory = ConversationBufferWindowMemory(k=5)
entity_memory = ConversationEntityMemory(llm=llm)

combined_memory = CombinedMemory(memories=[buffer_memory, entity_memory])

conversation = ConversationChain(
    llm=llm,
    memory=combined_memory
)
```

## LangGraph Memory

### Thread-Based Memory

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

# Create graph with memory
checkpointer = MemorySaver()
graph = StateGraph(StateDict)
# ... add nodes ...
app = graph.compile(checkpointer=checkpointer)

# Each thread maintains separate memory
config1 = {"configurable": {"thread_id": "user_1"}}
config2 = {"configurable": {"thread_id": "user_2"}}

app.invoke(input1, config1)  # Memory for user_1
app.invoke(input2, config2)  # Separate memory for user_2
```

### SQLite Checkpointer

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Persistent checkpoints
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
app = graph.compile(checkpointer=checkpointer)

# Memory persists across restarts
config = {"configurable": {"thread_id": "session_123"}}
result = app.invoke(input_data, config)
```

### State as Memory

```python
from typing import TypedDict, Annotated
from operator import add

class MemoryState(TypedDict):
    messages: Annotated[list, add]  # Accumulates messages
    user_name: str  # Persists user name
    preferences: dict  # Stores preferences

def node_with_memory(state: MemoryState):
    # Access memory from state
    previous_messages = state["messages"]
    user_name = state["user_name"]
    
    # Update memory
    return {
        "messages": ["New message"],
        "user_name": user_name  # Preserves existing value
    }
```

## Vector Store Memory

### Semantic Memory

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(
    ["Initial memory"],
    embeddings
)

# Memory retrieves relevant past conversations
memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

# Automatically retrieves similar past interactions
conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

### Zep Memory

```python
from langchain.memory.zep_memory import ZepMemory

# Managed memory service
memory = ZepMemory(
    session_id="user_123",
    url="http://localhost:8000",
    api_key="your-key"
)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

## Custom Memory

### Simple Custom Memory

```python
from langchain.memory import BaseChatMemory
from pydantic import Field

class CustomMemory(BaseChatMemory):
    memory_data: dict = Field(default_factory=dict)
    
    def save_context(self, inputs: dict, outputs: dict):
        """Save context from this conversation turn."""
        # Custom save logic
        user_message = inputs.get("input", "")
        ai_message = outputs.get("output", "")
        
        self.memory_data[user_message] = ai_message
    
    def load_memory_variables(self, inputs: dict) -> dict:
        """Load memory variables."""
        # Custom load logic
        return {"history": str(self.memory_data)}
    
    def clear(self):
        """Clear memory."""
        self.memory_data = {}
```

### Context-Aware Memory

```python
class ContextualMemory(BaseChatMemory):
    """Memory that adapts to context."""
    
    def load_memory_variables(self, inputs: dict) -> dict:
        """Load relevant memory based on current input."""
        current_topic = extract_topic(inputs["input"])
        
        # Retrieve only relevant memories
        relevant_history = [
            msg for msg in self.history
            if current_topic in msg
        ]
        
        return {"history": relevant_history}
```

### Tiered Memory

```python
class TieredMemory(BaseChatMemory):
    """Combines short-term and long-term memory."""
    
    short_term: ConversationBufferWindowMemory
    long_term: VectorStoreRetrieverMemory
    
    def load_memory_variables(self, inputs: dict) -> dict:
        # Get recent context
        recent = self.short_term.load_memory_variables(inputs)
        
        # Get relevant historical context
        historical = self.long_term.load_memory_variables(inputs)
        
        return {
            "recent_history": recent["history"],
            "relevant_past": historical["history"]
        }
```

## Best Practices

### 1. Choose Appropriate Memory Type

```python
# Simple chatbot: Buffer Memory
memory = ConversationBufferMemory()

# Long conversations: Window or Summary Memory
memory = ConversationBufferWindowMemory(k=10)

# Complex interactions: Entity Memory
memory = ConversationEntityMemory(llm=llm)

# Semantic search over history: Vector Store Memory
memory = VectorStoreRetrieverMemory(retriever=retriever)
```

### 2. Set Appropriate Limits

```python
# Prevent unbounded memory growth
memory = ConversationBufferWindowMemory(
    k=20,  # Last 20 messages
    return_messages=True
)

# Token-based limits
memory = ConversationTokenBufferMemory(
    llm=llm,
    max_token_limit=2000
)
```

### 3. Clear Memory When Needed

```python
# Clear at session end
conversation.memory.clear()

# Partial clear (keep system messages)
def selective_clear(memory):
    system_messages = [m for m in memory.messages if m.type == "system"]
    memory.clear()
    for msg in system_messages:
        memory.chat_memory.add_message(msg)
```

### 4. Separate User Memories

```python
# Use session/user IDs
def get_memory(user_id: str):
    return ConversationBufferMemory(
        chat_memory=RedisChatMessageHistory(
            url="redis://localhost",
            session_id=user_id
        )
    )

user1_memory = get_memory("user_1")
user2_memory = get_memory("user_2")
```

### 5. Monitor Memory Usage

```python
import sys

def check_memory_size(memory):
    """Check memory object size."""
    size_bytes = sys.getsizeof(memory.dict())
    size_mb = size_bytes / (1024 * 1024)
    print(f"Memory size: {size_mb:.2f} MB")
    
    if size_mb > 10:
        print("Warning: Memory getting large, consider summarizing")

# Check periodically
check_memory_size(conversation.memory)
```

### 6. Backup and Restore

```python
import pickle

def backup_memory(memory, filepath):
    """Save memory to disk."""
    with open(filepath, 'wb') as f:
        pickle.dump(memory.dict(), f)

def restore_memory(filepath):
    """Load memory from disk."""
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    return ConversationBufferMemory(**data)

# Backup
backup_memory(conversation.memory, "backup.pkl")

# Restore
conversation.memory = restore_memory("backup.pkl")
```

### 7. Async Memory Operations

```python
from langchain.memory import AsyncChatMessageHistory

class AsyncMemory(BaseChatMemory):
    """Async memory for high-performance applications."""
    
    async def asave_context(self, inputs: dict, outputs: dict):
        """Async save operation."""
        # Non-blocking save to database
        await async_db_save(inputs, outputs)
    
    async def aload_memory_variables(self, inputs: dict) -> dict:
        """Async load operation."""
        history = await async_db_load(inputs)
        return {"history": history}
```

## Common Patterns

### Conversation with Context Window

```python
# Keep last N exchanges, summarize older
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=500,
    return_messages=True
)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

### Multi-User Conversations

```python
class MultiUserMemory:
    """Manage memory for multiple users."""
    
    def __init__(self):
        self.user_memories = {}
    
    def get_memory(self, user_id: str):
        if user_id not in self.user_memories:
            self.user_memories[user_id] = ConversationBufferMemory()
        return self.user_memories[user_id]
    
    def clear_user(self, user_id: str):
        if user_id in self.user_memories:
            self.user_memories[user_id].clear()

# Usage
memory_manager = MultiUserMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory_manager.get_memory("user_123")
)
```

### Hierarchical Memory

```python
# Combine immediate, short-term, and long-term
class HierarchicalMemory:
    def __init__(self, llm):
        self.immediate = ConversationBufferWindowMemory(k=3)
        self.short_term = ConversationSummaryBufferMemory(
            llm=llm, max_token_limit=500
        )
        self.long_term = VectorStoreRetrieverMemory(
            retriever=vector_retriever
        )
    
    def get_context(self, query: str) -> str:
        immediate = self.immediate.load_memory_variables({})
        short = self.short_term.load_memory_variables({})
        long = self.long_term.load_memory_variables({"input": query})
        
        return f"""
        Recent: {immediate['history']}
        Summary: {short['history']}
        Relevant past: {long['history']}
        """
```

## Troubleshooting

### Memory Growing Too Large

1. Use window memory (limit by messages)
2. Use token buffer (limit by tokens)
3. Use summary memory (compress old messages)
4. Clear periodically

### Slow Performance

1. Use async memory operations
2. Cache memory loads
3. Use vector store for large histories
4. Limit retrieval to relevant parts

### Context Not Maintained

1. Check memory is passed to chain
2. Verify save_context is called
3. Check session ID consistency
4. Test memory persistence

### Memory Leaks

1. Clear memory after sessions
2. Set appropriate limits
3. Monitor memory usage
4. Use weak references for caches
