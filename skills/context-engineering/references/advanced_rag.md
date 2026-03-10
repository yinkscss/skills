# Advanced RAG Reference

## Core Principle: Decouple Search and Retrieve

The text granularity you need to *find* a document is vastly different from what you need to *understand* it. Modern context engineering decouples the RAG pipeline into two distinct stages.

### The Search Stage (Semantic Matching)

Scan a massive database for clues. Use small, semantically pure text units.

- **Chunk size:** 100–256 tokens
- **Purpose:** High-precision recall, clear semantic focus, minimal noise
- **Method:** Dense, transformer-based embeddings (e.g., BERT) that capture semantic meaning ("feline pets" = "cats")

### The Retrieve Stage (Context Understanding)

Read a full chapter to grasp a concept. Use much larger chunks.

- **Chunk size:** 1024+ tokens
- **Purpose:** Logical completeness, sufficient background, sustained reasoning
- **Method:** Re-ranking retrieved chunks by relevance to the query

## Evolution of RAG

Early implementations (pre-2025) had severe reliability issues:
- Rudimentary data processing
- Sparse retrieval methods (TF-IDF, BM25) that only matched keywords without understanding meaning

By 2025–2026, context engineering formalised:
- Sophisticated chunking strategies
- Dense, transformer-based embeddings
- Hybrid search combining keyword + semantic
- Chunk attribution and utilisation metrics

## Chunking Strategies

Choosing the right splitting logic is one of the most critical context engineering decisions:

| Strategy | Best For |
|----------|----------|
| **Fixed-size** | Uniform, simple documents |
| **Recursive Character** | General-purpose, hierarchical text |
| **Semantic** | Documents where meaning boundaries don't follow structure |
| **Hierarchical** | Documents with clear section/subsection structure |
| **Code-aware** | Source code files |

## Key Tools

- **Docling** — Multi-modal data extraction from PDFs and tables
- **Chroma** — Open-source vector database
- **Pinecone** — Managed vector database (enterprise scale)
- **Weaviate** — Open-source vector search engine
- **Qdrant** — High-performance vector database

## Evaluation Metrics

Modern RAG systems are evaluated on:
1. **Chunk attribution** — How much retrieved context actually influenced the model's output
2. **Chunk utilisation** — What percentage of retrieved chunks were used vs. ignored
3. **Answer faithfulness** — Whether the response is grounded in retrieved documents
4. **Retrieval precision** — Relevance of returned chunks to the query
