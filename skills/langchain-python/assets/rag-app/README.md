# RAG Application Template

Complete RAG (Retrieval-Augmented Generation) system for question-answering over documents.

## Setup

1. Install dependencies:
```bash
pip install langchain langchain-openai langchain-community faiss-cpu python-dotenv
```

2. Create `.env` file:
```bash
OPENAI_API_KEY=your-api-key-here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
```

3. Prepare documents:
```bash
mkdir sample_docs
# Add your .txt files to sample_docs/
```

4. Run:
```bash
python rag_app.py
```

## Features

- Document loading from directory
- Smart text splitting
- Vector embeddings with OpenAI
- FAISS vector store
- MMR retrieval for diversity
- Context-aware generation
- Source citation

## Usage

### Initialize System

```python
from rag_app import RAGSystem

rag = RAGSystem("./documents")
rag.setup()
```

### Query Documents

```python
result = rag.query("What is the main topic?")
print(result["answer"])
```

### Rebuild Index

```python
rag.setup(force_rebuild=True)
```

## Customization

### Change Chunk Size

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Larger chunks
    chunk_overlap=100
)
```

### Adjust Retrieval

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",  # or "mmr"
    search_kwargs={"k": 6}  # More documents
)
```

### Use Different Embeddings

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

### Change Vector Store

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./chroma_db"
)
```

## Advanced Features

### Add Metadata Filtering

```python
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 4,
        "filter": {"source": "specific_doc.txt"}
    }
)
```

### Implement Reranking

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

compressor = CohereRerank()
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)
```

### Add Conversational Memory

```python
from langchain.chains import create_history_aware_retriever

history_aware_retriever = create_history_aware_retriever(
    llm,
    retriever,
    contextualize_prompt
)
```

## Production Considerations

1. Use persistent vector store (Chroma, Pinecone, Weaviate)
2. Implement caching for embeddings
3. Add error handling and retry logic
4. Monitor retrieval quality
5. Implement feedback collection
6. Add authentication
7. Use async operations for scalability
8. Implement rate limiting
9. Add logging and monitoring
10. Regular index updates

## Performance Tips

- Adjust chunk size based on document type
- Use appropriate embedding model
- Enable caching
- Use hybrid search (vector + keyword)
- Implement result caching
- Batch document processing

## Evaluation

```python
from langchain.evaluation import load_evaluator

evaluator = load_evaluator("embedding_distance")

for test_case in test_cases:
    retrieved = retriever.get_relevant_documents(test_case["query"])
    score = evaluator.evaluate_strings(
        prediction=retrieved[0].page_content,
        reference=test_case["expected"]
    )
    print(f"Score: {score}")
```
