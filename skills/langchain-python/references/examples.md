# Complete Examples

Working code examples for common LangChain use cases.

## Table of Contents

- [Simple Chatbot](#simple-chatbot)
- [RAG Q&A System](#rag-qa-system)
- [Agent with Tools](#agent-with-tools)
- [Multi-Agent System](#multi-agent-system)
- [Human-in-the-Loop](#human-in-the-loop)
- [Streaming Chat](#streaming-chat)

## Simple Chatbot

Basic conversational chatbot with memory.

```python
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain

# Initialize
llm = ChatOpenAI(model="gpt-4", temperature=0.7)
memory = ConversationBufferWindowMemory(k=5)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Chat loop
print("Chatbot: Hello! How can I help you?")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break
    
    response = conversation.predict(input=user_input)
    print(f"Chatbot: {response}")
```

## RAG Q&A System

Question-answering system over documents.

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate

# Load and process documents
loader = DirectoryLoader("./documents", glob="**/*.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Create RAG chain
llm = ChatOpenAI(model="gpt-4", temperature=0)
prompt = ChatPromptTemplate.from_template("""
Answer based on this context:
{context}

Question: {input}
""")

combine_docs_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

# Query
result = rag_chain.invoke({"input": "What is the main topic?"})
print(result["answer"])
```

## Agent with Tools

Agent that can use multiple tools.

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain import hub

# Define tools
@tool
def search(query: str) -> str:
    """Search for information."""
    # Implementation
    return f"Search results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# Create agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [search, calculate]
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

# Use agent
result = agent_executor.invoke({"input": "What is 15 * 23?"})
print(result["output"])
```

## Multi-Agent System

Multiple specialized agents working together.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from typing import TypedDict, Annotated
from operator import add

# State
class State(TypedDict):
    messages: Annotated[list, add]

# Tools
@tool
def research_tool(query: str) -> str:
    """Research information."""
    return f"Research: {query}"

@tool
def analysis_tool(data: str) -> str:
    """Analyze data."""
    return f"Analysis: {data}"

# Create agents
researcher = create_react_agent(
    ChatOpenAI(model="gpt-4"),
    [research_tool],
    messages_modifier="You are a researcher."
)

analyst = create_react_agent(
    ChatOpenAI(model="gpt-4"),
    [analysis_tool],
    messages_modifier="You are an analyst."
)

# Build workflow
workflow = StateGraph(State)

def research_node(state):
    return {"messages": researcher.invoke(state)["messages"]}

def analyst_node(state):
    return {"messages": analyst.invoke(state)["messages"]}

workflow.add_node("researcher", research_node)
workflow.add_node("analyst", analyst_node)

workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", END)

app = workflow.compile()

# Use
result = app.invoke({"messages": [("user", "Research AI trends")]})
print(result["messages"][-1].content)
```

## Human-in-the-Loop

Workflow requiring human approval.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from typing import TypedDict

class State(TypedDict):
    draft: str
    approved: bool
    final: str

llm = ChatOpenAI()

def generate(state):
    response = llm.invoke("Write a draft")
    return {"draft": response.content}

def finalize(state):
    if state["approved"]:
        return {"final": state["draft"]}
    return {}

# Build workflow
workflow = StateGraph(State)
workflow.add_node("generate", generate)
workflow.add_node("finalize", finalize)

workflow.add_edge(START, "generate")
workflow.add_edge("generate", "finalize")
workflow.add_edge("finalize", END)

# Compile with checkpointer
checkpointer = MemorySaver()
app = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["finalize"]
)

# Use
config = {"configurable": {"thread_id": "1"}}

# First run - pauses
state = app.invoke({"draft": "", "approved": False, "final": ""}, config)
print("Draft:", state["draft"])

# Approve and continue
app.update_state(config, {"approved": True})
final = app.invoke(None, config)
print("Final:", final["final"])
```

## Streaming Chat

Real-time streaming responses.

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import asyncio

# Create chain
llm = ChatOpenAI(streaming=True)
prompt = ChatPromptTemplate.from_template("Tell me about: {topic}")
chain = prompt | llm | StrOutputParser()

# Sync streaming
def stream_sync(topic: str):
    print(f"Topic: {topic}\n")
    for chunk in chain.stream({"topic": topic}):
        print(chunk, end="", flush=True)
    print("\n")

# Async streaming
async def stream_async(topic: str):
    print(f"Topic: {topic}\n")
    async for chunk in chain.astream({"topic": topic}):
        print(chunk, end="", flush=True)
    print("\n")

# Usage
stream_sync("artificial intelligence")
asyncio.run(stream_async("quantum computing"))
```

## Additional Patterns

### Error Handling

```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def robust_query(chain, query):
    try:
        return chain.invoke(query)
    except Exception as e:
        print(f"Error: {e}")
        raise
```

### Batch Processing

```python
# Process multiple queries efficiently
queries = [{"topic": f"topic{i}"} for i in range(10)]
results = chain.batch(queries)
```

### Caching

```python
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

set_llm_cache(InMemoryCache())

# Subsequent identical queries are cached
result1 = llm.invoke("What is AI?")  # API call
result2 = llm.invoke("What is AI?")  # Cached
```

### Fallbacks

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

primary = ChatOpenAI(model="gpt-4")
fallback = ChatAnthropic(model="claude-3-5-sonnet-20241022")

chain = primary.with_fallbacks([fallback])

# Uses fallback if primary fails
result = chain.invoke("Hello")
```

These examples provide starting points for common use cases. Adapt them to your specific requirements.
