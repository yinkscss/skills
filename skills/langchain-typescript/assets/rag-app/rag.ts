import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { createStuffDocumentsChain } from "langchain/chains/combine_documents";
import { createRetrievalChain } from "langchain/chains/retrieval";
import { Document } from "@langchain/core/documents";

/**
 * RAG (Retrieval-Augmented Generation) Application Template
 * 
 * This template demonstrates:
 * - Document loading and splitting
 * - Vector store creation
 * - Semantic search
 * - Context-aware generation
 */

class RAGApplication {
  private retriever: any;
  private chain: any;
  private vectorStore: MemoryVectorStore | null = null;
  
  /**
   * Initialize the RAG system with documents
   */
  async initialize(documents: string[]) {
    console.log("Initializing RAG application...");
    
    // 1. Split documents into chunks
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 1000,
      chunkOverlap: 200,
      separators: ["\n\n", "\n", " ", ""]
    });
    
    console.log(`Splitting ${documents.length} documents...`);
    const docs = await splitter.createDocuments(documents);
    console.log(`Created ${docs.length} chunks`);
    
    // 2. Create embeddings and vector store
    const embeddings = new OpenAIEmbeddings({
      model: "text-embedding-3-small"
    });
    
    console.log("Creating vector store...");
    this.vectorStore = await MemoryVectorStore.fromDocuments(
      docs,
      embeddings
    );
    
    // 3. Create retriever
    this.retriever = this.vectorStore.asRetriever({
      k: 4,  // Return top 4 most relevant chunks
      searchType: "similarity"
    });
    
    // 4. Create QA chain
    const model = new ChatOpenAI({
      model: "gpt-4",
      temperature: 0
    });
    
    const prompt = ChatPromptTemplate.fromMessages([
      ["system", `You are a helpful assistant. Answer questions based on the following context:

{context}

If the answer is not in the context, say "I don't have enough information to answer that question."`],
      ["user", "{input}"]
    ]);
    
    const combineDocsChain = await createStuffDocumentsChain({
      llm: model,
      prompt
    });
    
    this.chain = await createRetrievalChain({
      retriever: this.retriever,
      combineDocsChain
    });
    
    console.log("RAG application initialized!\n");
  }
  
  /**
   * Query the RAG system
   */
  async query(question: string) {
    if (!this.chain) {
      throw new Error("RAG application not initialized. Call initialize() first.");
    }
    
    console.log(`Question: ${question}\n`);
    
    const result = await this.chain.invoke({ input: question });
    
    return {
      answer: result.answer,
      sources: result.context.map((doc: Document) => ({
        content: doc.pageContent,
        metadata: doc.metadata
      }))
    };
  }
  
  /**
   * Add more documents to the vector store
   */
  async addDocuments(documents: string[]) {
    if (!this.vectorStore) {
      throw new Error("Vector store not initialized.");
    }
    
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 1000,
      chunkOverlap: 200
    });
    
    const docs = await splitter.createDocuments(documents);
    await this.vectorStore.addDocuments(docs);
    
    console.log(`Added ${docs.length} new chunks to vector store`);
  }
  
  /**
   * Search for similar documents
   */
  async search(query: string, k: number = 4) {
    if (!this.vectorStore) {
      throw new Error("Vector store not initialized.");
    }
    
    const results = await this.vectorStore.similaritySearch(query, k);
    return results.map(doc => ({
      content: doc.pageContent,
      metadata: doc.metadata
    }));
  }
}

// Example usage
async function main() {
  const rag = new RAGApplication();
  
  // Sample documents (replace with your actual documents)
  const documents = [
    `LangChain is a framework for developing applications powered by language models. 
    It provides tools for prompt management, chains, data augmented generation, agents, 
    and memory systems.`,
    
    `LangGraph is a library for building stateful, multi-actor applications with LLMs. 
    It extends LangChain with the ability to create cyclic graphs for agent runtimes. 
    Key features include state management, human-in-the-loop, and persistence.`,
    
    `TypeScript is a strongly typed programming language that builds on JavaScript. 
    It adds optional static typing, classes, and interfaces. TypeScript code compiles 
    to plain JavaScript and runs anywhere JavaScript runs.`,
    
    `Vector databases store high-dimensional vectors representing data embeddings. 
    They enable semantic search by finding vectors similar to a query vector. 
    Common vector databases include Pinecone, Weaviate, and Chroma.`
  ];
  
  // Initialize with documents
  await rag.initialize(documents);
  
  // Query the system
  const result1 = await rag.query("What is LangGraph?");
  console.log(`Answer: ${result1.answer}\n`);
  console.log(`Sources (${result1.sources.length} chunks):`);
  result1.sources.forEach((source, i) => {
    console.log(`${i + 1}. ${source.content.substring(0, 100)}...`);
  });
  
  console.log("\n---\n");
  
  // Another query
  const result2 = await rag.query("How do vector databases work?");
  console.log(`Answer: ${result2.answer}\n`);
  
  console.log("\n---\n");
  
  // Search for similar documents
  const searchResults = await rag.search("programming language", 2);
  console.log("Similar documents:");
  searchResults.forEach((doc, i) => {
    console.log(`${i + 1}. ${doc.content.substring(0, 150)}...`);
  });
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

export { RAGApplication };
