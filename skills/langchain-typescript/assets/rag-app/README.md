# RAG Application Template

Retrieval-Augmented Generation (RAG) system for question-answering over documents.

## What is RAG?

RAG combines retrieval (finding relevant documents) with generation (creating answers). This enables LLMs to answer questions using your specific documents.

## Features

- **Document Processing**: Automatic chunking and embedding
- **Semantic Search**: Find relevant context using vector similarity
- **Context-Aware Answers**: Generate answers grounded in your documents
- **Extensible**: Add more documents dynamically

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run:
```bash
npm run dev
```

## How It Works

1. **Split Documents**: Break large documents into chunks
2. **Create Embeddings**: Convert chunks to vectors
3. **Store in Vector DB**: Index for fast similarity search
4. **Query**: Find relevant chunks for user question
5. **Generate**: LLM creates answer using context

## Customization

### Use Different Vector Store

```typescript
// Pinecone (production)
import { PineconeStore } from "@langchain/pinecone";
import { Pinecone } from "@pinecone-database/pinecone";

const pinecone = new Pinecone();
const index = pinecone.Index("my-index");

const vectorStore = await PineconeStore.fromDocuments(
  docs,
  embeddings,
  { pineconeIndex: index }
);
```

```typescript
// Chroma (local development)
import { Chroma } from "@langchain/community/vectorstores/chroma";

const vectorStore = await Chroma.fromDocuments(
  docs,
  embeddings,
  { collectionName: "my-collection" }
);
```

### Adjust Chunk Size

```typescript
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 500,      // Smaller chunks = more precise
  chunkOverlap: 50     // Less overlap = more unique chunks
});
```

### Change Retrieval Strategy

```typescript
// Get more/fewer chunks
const retriever = vectorStore.asRetriever({
  k: 10,  // Top 10 results
  searchType: "mmr",  // Maximum Marginal Relevance (diverse results)
  searchKwargs: { fetchK: 20, lambda: 0.5 }
});
```

### Add Metadata Filtering

```typescript
const retriever = vectorStore.asRetriever({
  k: 4,
  filter: {
    category: "technical",
    date: { $gte: "2024-01-01" }
  }
});
```

## Loading Documents

### From Files

```typescript
import { TextLoader } from "langchain/document_loaders/fs/text";
import { PDFLoader } from "langchain/document_loaders/fs/pdf";

// Load text file
const loader = new TextLoader("document.txt");
const docs = await loader.load();

// Load PDF
const pdfLoader = new PDFLoader("document.pdf");
const pdfDocs = await pdfLoader.load();
```

### From Web

```typescript
import { CheerioWebBaseLoader } from "langchain/document_loaders/web/cheerio";

const loader = new CheerioWebBaseLoader("https://example.com");
const docs = await loader.load();
```

### From Database

```typescript
const documents = await db.articles.findMany();
const textDocs = documents.map(doc => doc.content);
await rag.initialize(textDocs);
```

## Production Tips

1. **Use Persistent Vector Store**: Pinecone, Weaviate, or Chroma
2. **Cache Embeddings**: Avoid re-computing for same text
3. **Monitor Costs**: Embeddings can be expensive at scale
4. **Implement Re-ranking**: Improve result quality
5. **Add Metadata**: Filter results by source, date, etc.
