# Chains

Chains compose LLM operations into sequential or parallel workflows using LangChain Expression Language (LCEL).

## Table of Contents

- [Quick Start](#quick-start)
- [LCEL Basics](#lcel-basics)
- [Sequential Chains](#sequential-chains)
- [Parallel Chains](#parallel-chains)
- [Retrieval Chains](#retrieval-chains)
- [Conversation Chains](#conversation-chains)
- [Routing](#routing)
- [Streaming](#streaming)
- [Best Practices](#best-practices)

## Quick Start

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# Create chain using LCEL
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model = ChatOpenAI()
output_parser = StrOutputParser()

chain = prompt | model | output_parser

# Invoke
result = chain.invoke({"topic": "programming"})
print(result)
```

## LCEL Basics

LangChain Expression Language (LCEL) uses the `|` operator to chain components.

### Basic Chain Structure

```python
# prompt | model | parser
chain = prompt | model | output_parser

# Equivalent to:
def chain(input):
    prompt_value = prompt.invoke(input)
    model_output = model.invoke(prompt_value)
    final_output = output_parser.invoke(model_output)
    return final_output
```

### Chain Components

**Prompts:**
```python
from langchain.prompts import ChatPromptTemplate, PromptTemplate

# Chat prompt
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "{question}")
])

# String prompt
string_prompt = PromptTemplate.from_template("Answer: {question}")
```

**Models:**
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4", temperature=0.7)
```

**Output Parsers:**
```python
from langchain.schema.output_parser import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

# String parser
str_parser = StrOutputParser()

# Structured parser
class Answer(BaseModel):
    answer: str
    confidence: float

pydantic_parser = PydanticOutputParser(pydantic_object=Answer)
```

## Sequential Chains

### Simple Sequential

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Step 1: Generate outline
outline_prompt = ChatPromptTemplate.from_template(
    "Create an outline for an essay about {topic}"
)

# Step 2: Write essay from outline
essay_prompt = ChatPromptTemplate.from_template(
    "Write an essay based on this outline:\n{outline}"
)

model = ChatOpenAI()

# Chain them
chain = (
    {"outline": outline_prompt | model | StrOutputParser()}
    | essay_prompt
    | model
    | StrOutputParser()
)

result = chain.invoke({"topic": "AI ethics"})
```

### With State Passing

```python
from langchain.schema.runnable import RunnablePassthrough

chain = (
    RunnablePassthrough.assign(
        summary=lambda x: summarize(x["text"])
    )
    | RunnablePassthrough.assign(
        analysis=lambda x: analyze(x["summary"])
    )
    | format_output
)

# Output contains: text, summary, analysis
result = chain.invoke({"text": "Long document..."})
```

### Multi-Step Processing

```python
# Step 1: Extract entities
extract_prompt = ChatPromptTemplate.from_template(
    "Extract entities from: {text}"
)

# Step 2: Classify sentiment
sentiment_prompt = ChatPromptTemplate.from_template(
    "Classify sentiment: {text}"
)

# Step 3: Generate summary
summary_prompt = ChatPromptTemplate.from_template(
    "Summarize with entities {entities} and sentiment {sentiment}: {text}"
)

model = ChatOpenAI()

chain = (
    RunnablePassthrough.assign(
        entities=extract_prompt | model | StrOutputParser(),
        sentiment=sentiment_prompt | model | StrOutputParser()
    )
    | summary_prompt
    | model
    | StrOutputParser()
)
```

## Parallel Chains

### Basic Parallel Execution

```python
from langchain.schema.runnable import RunnableParallel

# Execute multiple chains in parallel
chain = RunnableParallel(
    summary=prompt1 | model | StrOutputParser(),
    translation=prompt2 | model | StrOutputParser(),
    analysis=prompt3 | model | StrOutputParser()
)

result = chain.invoke({"text": "..."})
# Returns: {"summary": "...", "translation": "...", "analysis": "..."}
```

### Map-Reduce Pattern

```python
from langchain.schema.runnable import RunnableMap

# Process multiple items in parallel
def process_item(item):
    return model.invoke(f"Process: {item}")

map_chain = RunnableMap({
    f"item_{i}": process_item
    for i in range(5)
})

results = map_chain.invoke({"items": [1, 2, 3, 4, 5]})
```

### Parallel with Different Models

```python
# Use different models for different tasks
fast_model = ChatOpenAI(model="gpt-3.5-turbo")
smart_model = ChatOpenAI(model="gpt-4")

chain = RunnableParallel(
    quick_answer=prompt | fast_model | StrOutputParser(),
    detailed_answer=prompt | smart_model | StrOutputParser()
)
```

## Retrieval Chains

### Basic RAG Chain

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate

# Setup retriever
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(
    ["doc1 content", "doc2 content"],
    embeddings
)
retriever = vectorstore.as_retriever()

# Create chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using this context: {context}"),
    ("user", "{input}")
])

model = ChatOpenAI()

# Combine documents chain
combine_docs_chain = create_stuff_documents_chain(model, prompt)

# Retrieval chain
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

# Use
result = rag_chain.invoke({"input": "What is X?"})
print(result["answer"])
```

### Custom RAG Chain

```python
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

result = rag_chain.invoke("What is the main topic?")
```

### Multi-Query Retrieval

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

# Generate multiple query variations
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=ChatOpenAI(temperature=0)
)

# Retrieves using all query variations
docs = multi_query_retriever.get_relevant_documents("user query")
```

### Contextual Compression

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Compress retrieved documents
compressor = LLMChainExtractor.from_llm(model)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)

# Returns only relevant parts of documents
compressed_docs = compression_retriever.get_relevant_documents("query")
```

## Conversation Chains

### With Memory

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=model,
    memory=memory,
    verbose=True
)

# Maintains conversation history
response1 = conversation.predict(input="Hi, I'm John")
response2 = conversation.predict(input="What's my name?")  # Knows it's John
```

### Chat History Chain

```python
from langchain.schema.runnable import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

# Store for multiple conversations
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain = prompt | model

# Wrap with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use with session
result = chain_with_history.invoke(
    {"input": "Hi!"},
    config={"configurable": {"session_id": "user123"}}
)
```

### Summarization Memory

```python
from langchain.memory import ConversationSummaryMemory

summary_memory = ConversationSummaryMemory(llm=model)

# Automatically summarizes old messages
conversation = ConversationChain(
    llm=model,
    memory=summary_memory
)
```

## Routing

### Conditional Routing

```python
from langchain.schema.runnable import RunnableBranch

# Route based on input
branch = RunnableBranch(
    (lambda x: "code" in x["topic"], code_chain),
    (lambda x: "math" in x["topic"], math_chain),
    general_chain  # Default
)

chain = {"topic": lambda x: x} | branch
```

### Semantic Routing

```python
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate

# Define destination chains
physics_template = "You are a physics expert. {input}"
math_template = "You are a math expert. {input}"

prompt_infos = [
    {
        "name": "physics",
        "description": "Good for physics questions",
        "prompt_template": physics_template
    },
    {
        "name": "math",
        "description": "Good for math questions",
        "prompt_template": math_template
    }
]

# Create router
router_chain = MultiPromptChain.from_prompts(
    model,
    prompt_infos,
    verbose=True
)

# Automatically routes to appropriate chain
result = router_chain.run("What is gravity?")  # -> physics chain
```

## Streaming

### Stream Tokens

```python
chain = prompt | model | StrOutputParser()

# Stream output
for chunk in chain.stream({"topic": "AI"}):
    print(chunk, end="", flush=True)
```

### Async Streaming

```python
async for chunk in chain.astream({"topic": "AI"}):
    print(chunk, end="", flush=True)
```

### Stream Intermediate Steps

```python
from langchain.schema.runnable import RunnablePassthrough

chain = (
    RunnablePassthrough.assign(step1=chain1)
    | RunnablePassthrough.assign(step2=chain2)
    | RunnablePassthrough.assign(step3=chain3)
)

# Stream each step
for chunk in chain.stream(input_data):
    print(f"Intermediate result: {chunk}")
```

## Best Practices

### 1. Error Handling

```python
from langchain.schema.runnable import RunnableWithFallbacks

# Add fallbacks
chain_with_fallback = chain.with_fallbacks(
    [fallback_chain],
    exception_types=(ValueError, TimeoutError)
)
```

### 2. Retry Logic

```python
from langchain.schema.runnable import RunnableRetry

chain_with_retry = chain.with_retry(
    retry_if_exception_type=(APIError,),
    wait_exponential_jitter=True,
    stop_after_attempt=3
)
```

### 3. Caching

```python
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

set_llm_cache(InMemoryCache())

# Responses are cached automatically
chain = prompt | model | parser
```

### 4. Batch Processing

```python
# Process multiple inputs efficiently
inputs = [{"topic": f"topic{i}"} for i in range(10)]
results = chain.batch(inputs)
```

### 5. Async Processing

```python
import asyncio

# Async chain execution
results = await asyncio.gather(
    chain.ainvoke(input1),
    chain.ainvoke(input2),
    chain.ainvoke(input3)
)
```

### 6. Configuration

```python
from langchain.schema.runnable import RunnableConfig

config = RunnableConfig(
    max_concurrency=5,
    tags=["production"],
    metadata={"user_id": "123"}
)

result = chain.invoke(input_data, config=config)
```

### 7. Debugging

```python
from langchain.globals import set_debug

set_debug(True)

# Shows all intermediate steps
result = chain.invoke(input_data)
```

## Common Patterns

### Transform and Generate

```python
# Transform input, then generate
chain = (
    {"transformed": transform_function}
    | prompt
    | model
    | StrOutputParser()
)
```

### Generate, Parse, Validate

```python
from pydantic import BaseModel, ValidationError

class Output(BaseModel):
    field1: str
    field2: int

def validate_output(text):
    try:
        return Output.parse_raw(text)
    except ValidationError:
        return None

chain = (
    prompt
    | model
    | StrOutputParser()
    | validate_output
)
```

### Multi-Stage Refinement

```python
# Generate, critique, refine
chain = (
    RunnablePassthrough.assign(
        draft=prompt | model | StrOutputParser()
    )
    | RunnablePassthrough.assign(
        critique=lambda x: critique_prompt.format(text=x["draft"])
                          | model | StrOutputParser()
    )
    | (lambda x: refine_prompt.format(
        draft=x["draft"],
        critique=x["critique"]
    ))
    | model
    | StrOutputParser()
)
```

## Troubleshooting

### Chain Not Working

1. Test each component separately
2. Check input/output formats match
3. Enable debug mode
4. Verify all required variables are provided

### Performance Issues

1. Use batch processing for multiple inputs
2. Enable caching
3. Use async for I/O bound operations
4. Consider parallel execution

### Memory Leaks

1. Use summarization memory for long conversations
2. Clear memory periodically
3. Limit memory buffer size
4. Use windowed memory

### Type Errors

1. Ensure consistent data types between steps
2. Use proper output parsers
3. Validate intermediate outputs
4. Add type hints
