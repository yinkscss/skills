# RAG (Retrieval-Augmented Generation)

RAG combines document retrieval with LLM generation to answer questions using your own data.

## Table of Contents

- [Overview](#overview)
- [Document Loading](#document-loading)
- [Text Splitting](#text-splitting)
- [Embeddings](#embeddings)
- [Vector Stores](#vector-stores)
- [Retrievers](#retrievers)
- [RAG Chains](#rag-chains)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)

## Overview

RAG workflow:
1. **Load** documents from various sources
2. **Split** documents into chunks
3. **Embed** chunks into vectors
4. **Store** vectors in vector database
5. **Retrieve** relevant chunks for queries
6. **Generate** answers using LLM + retrieved context

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate

# 1. Load
loader = TextLoader("document.txt")
docs = loader.load()

# 2. Split
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3 & 4. Embed and store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 5. Retrieve
retriever = vectorstore.as_retriever()

# 6. Generate
llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("""
Answer using this context:
{context}

Question: {input}
""")

combine_docs_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

result = rag_chain.invoke({"input": "What is the main topic?"})
print(result["answer"])
```

## Document Loading

### Text Files

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("document.txt")
docs = loader.load()
```

### PDFs

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
pages = loader.load()
```

### URLs

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com")
docs = loader.load()
```

### Directories

```python
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader("./docs", glob="**/*.txt")
docs = loader.load()
```

### CSV

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("data.csv")
docs = loader.load()
```

### JSON

```python
from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path="data.json",
    jq_schema=".messages[].content",
    text_content=False
)
docs = loader.load()
```

### Multiple Sources

```python
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    WebBaseLoader
)

loaders = [
    TextLoader("doc1.txt"),
    PyPDFLoader("doc2.pdf"),
    WebBaseLoader("https://example.com")
]

docs = []
for loader in loaders:
    docs.extend(loader.load())
```

## Text Splitting

### Character Splitter

```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separator="\n"
)

chunks = splitter.split_documents(docs)
```

### Recursive Character Splitter (Recommended)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

chunks = splitter.split_documents(docs)
```

### Token Splitter

```python
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)
```

### Code Splitter

```python
from langchain.text_splitter import (
    Language,
    RecursiveCharacterTextSplitter
)

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=500,
    chunk_overlap=50
)

js_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.JS,
    chunk_size=500,
    chunk_overlap=50
)
```

### Semantic Splitter

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile"
)

chunks = splitter.split_documents(docs)
```

## Embeddings

### OpenAI Embeddings

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # or "text-embedding-3-large"
    api_key="your-key"
)

# Embed text
vector = embeddings.embed_query("sample text")

# Embed documents
vectors = embeddings.embed_documents(["doc1", "doc2"])
```

### HuggingFace Embeddings

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

### Cohere Embeddings

```python
from langchain_community.embeddings import CohereEmbeddings

embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key="your-key"
)
```

### Local Embeddings

```python
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="llama2"
)
```

## Vector Stores

### FAISS (In-Memory)

```python
from langchain_community.vectorstores import FAISS

# Create from documents
vectorstore = FAISS.from_documents(chunks, embeddings)

# Save and load
vectorstore.save_local("faiss_index")
loaded_vectorstore = FAISS.load_local("faiss_index", embeddings)

# Search
results = vectorstore.similarity_search("query", k=4)
```

### Chroma (Persistent)

```python
from langchain_community.vectorstores import Chroma

# Create with persistence
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Load existing
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

### Pinecone (Cloud)

```python
from langchain_community.vectorstores import Pinecone
import pinecone

pinecone.init(api_key="your-key", environment="us-west1-gcp")

vectorstore = Pinecone.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name="my-index"
)
```

### Weaviate

```python
from langchain_community.vectorstores import Weaviate
import weaviate

client = weaviate.Client("http://localhost:8080")

vectorstore = Weaviate.from_documents(
    documents=chunks,
    embedding=embeddings,
    client=client
)
```

### Qdrant

```python
from langchain_community.vectorstores import Qdrant

vectorstore = Qdrant.from_documents(
    chunks,
    embeddings,
    url="http://localhost:6333",
    collection_name="my_documents"
)
```

## Retrievers

### Basic Retriever

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

docs = retriever.get_relevant_documents("query")
```

### MMR (Maximum Marginal Relevance)

```python
# Balances similarity and diversity
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20}
)
```

### Similarity Score Threshold

```python
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.5, "k": 4}
)
```

### Multi-Query Retriever

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

# Generates multiple query variations
docs = retriever.get_relevant_documents("original query")
```

### Contextual Compression

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)

# Returns compressed, relevant excerpts
docs = compression_retriever.get_relevant_documents("query")
```

### Ensemble Retriever

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Combine vector search and keyword search
bm25_retriever = BM25Retriever.from_documents(chunks)
vector_retriever = vectorstore.as_retriever()

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]
)

docs = ensemble_retriever.get_relevant_documents("query")
```

## RAG Chains

### Basic RAG Chain

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context provided.

Context: {context}

Question: {input}

Answer:
""")

combine_docs_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

result = rag_chain.invoke({"input": "What is X?"})
print(result["answer"])
```

### Custom RAG Chain (LCEL)

```python
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is the capital of France?")
```

### Conversational RAG

```python
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

# Contextualize question based on history
contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given chat history and latest question, formulate standalone question."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

history_aware_retriever = create_history_aware_retriever(
    llm,
    retriever,
    contextualize_prompt
)

# Answer chain
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using context: {context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

qa_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

# Use with chat history
result = rag_chain.invoke({
    "input": "What did we discuss?",
    "chat_history": [
        ("human", "Hi"),
        ("ai", "Hello!"),
    ]
})
```

## Advanced Patterns

### Multi-Document RAG

```python
# Different retrievers for different document types
tech_retriever = tech_vectorstore.as_retriever()
legal_retriever = legal_vectorstore.as_retriever()

def route_query(query: str):
    if "technical" in query.lower():
        return tech_retriever
    elif "legal" in query.lower():
        return legal_retriever
    return tech_retriever  # default

# Use in chain
retriever = route_query(user_query)
docs = retriever.get_relevant_documents(user_query)
```

### HyDE (Hypothetical Document Embeddings)

```python
# Generate hypothetical answer, then search for it
hyde_prompt = ChatPromptTemplate.from_template(
    "Write a hypothetical answer to: {question}"
)

hyde_chain = (
    hyde_prompt
    | llm
    | StrOutputParser()
    | retriever
)

docs = hyde_chain.invoke({"question": "What is quantum computing?"})
```

### Parent Document Retriever

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

# Store full documents
docstore = InMemoryStore()

# Retrieve using small chunks, return full docs
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=small_chunk_splitter,
    parent_splitter=large_chunk_splitter
)
```

### Self-Query Retriever

```python
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

metadata_field_info = [
    AttributeInfo(
        name="source",
        description="Document source",
        type="string"
    ),
    AttributeInfo(
        name="date",
        description="Publication date",
        type="string"
    )
]

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="Scientific papers",
    metadata_field_info=metadata_field_info
)

# Automatically constructs metadata filters
docs = retriever.get_relevant_documents(
    "Papers about AI from 2023"
)
```

## Best Practices

### 1. Chunk Size

```python
# Balance: too small = no context, too large = noise
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # ~125 tokens
    chunk_overlap=50,  # 10% overlap
)
```

### 2. Metadata

```python
# Add metadata for filtering
for doc in chunks:
    doc.metadata["source"] = "documentation"
    doc.metadata["version"] = "v1.0"
    doc.metadata["topic"] = "API"

# Filter retrieval
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 4,
        "filter": {"topic": "API"}
    }
)
```

### 3. Hybrid Search

```python
# Combine vector + keyword search
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7]  # Favor vector search
)
```

### 4. Reranking

```python
from langchain.retrievers.document_compressors import CohereRerank

# Retrieve more, rerank to top K
compressor = CohereRerank(model="rerank-english-v2.0", top_n=4)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 20})
)
```

### 5. Citation

```python
# Include source in prompt
prompt = ChatPromptTemplate.from_template("""
Answer and cite sources.

Context:
{context}

Question: {input}

Answer (include [Source: ...]):
""")

def format_docs_with_sources(docs):
    return "\n\n".join(
        f"[Source: {doc.metadata['source']}]\n{doc.page_content}"
        for doc in docs
    )
```

### 6. Evaluation

```python
from langchain.evaluation import load_evaluator

# Test retrieval quality
evaluator = load_evaluator("embedding_distance")

for query, expected_doc in test_cases:
    retrieved_docs = retriever.get_relevant_documents(query)
    score = evaluator.evaluate_strings(
        prediction=retrieved_docs[0].page_content,
        reference=expected_doc
    )
    print(f"Score: {score}")
```

## Troubleshooting

### Poor Retrieval Quality

1. Adjust chunk size/overlap
2. Try different embedding models
3. Use hybrid search (vector + keyword)
4. Add reranking step
5. Improve metadata filtering

### High Latency

1. Use smaller embedding models
2. Reduce number of retrieved documents
3. Use approximate nearest neighbor search
4. Cache embeddings
5. Batch operations

### High Costs

1. Use smaller embedding models
2. Cache embeddings
3. Reduce document overlap
4. Use local embeddings (HuggingFace)

### Irrelevant Results

1. Improve document quality
2. Add metadata filters
3. Use contextual compression
4. Increase retrieval threshold
5. Try multi-query retrieval
