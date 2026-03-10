"""
RAG (Retrieval-Augmented Generation) Application

A complete RAG system for question-answering over documents:
- Document loading and processing
- Vector store creation
- Semantic search
- Context-aware generation
"""

import os
from dotenv import load_dotenv
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

class RAGSystem:
    """RAG system for document Q&A."""
    
    def __init__(self, docs_path: str, index_path: str = "./faiss_index"):
        """Initialize RAG system.
        
        Args:
            docs_path: Path to documents directory
            index_path: Path to save/load vector index
        """
        self.docs_path = docs_path
        self.index_path = index_path
        self.vectorstore = None
        self.rag_chain = None
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        
    def load_documents(self):
        """Load documents from directory."""
        print(f"\nLoading documents from {self.docs_path}...")
        
        loader = DirectoryLoader(
            self.docs_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            show_progress=True
        )
        
        documents = loader.load()
        print(f"Loaded {len(documents)} documents")
        
        return documents
    
    def split_documents(self, documents):
        """Split documents into chunks."""
        print("\nSplitting documents into chunks...")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        return chunks
    
    def create_vectorstore(self, chunks):
        """Create vector store from chunks."""
        print("\nCreating vector store...")
        
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        
        # Save for later use
        self.vectorstore.save_local(self.index_path)
        print(f"Vector store saved to {self.index_path}")
        
        return self.vectorstore
    
    def load_vectorstore(self):
        """Load existing vector store."""
        print(f"\nLoading vector store from {self.index_path}...")
        
        self.vectorstore = FAISS.load_local(
            self.index_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        print("Vector store loaded")
        return self.vectorstore
    
    def create_rag_chain(self):
        """Create RAG chain."""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")
        
        print("\nCreating RAG chain...")
        
        # Create retriever with MMR for diversity
        retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 4, "fetch_k": 20}
        )
        
        # Create prompt
        prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context. If you cannot answer 
based on the context, say so.

Context:
{context}

Question: {input}

Answer: Provide a detailed answer and cite sources when possible.
""")
        
        # Create document chain
        combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        
        # Create retrieval chain
        self.rag_chain = create_retrieval_chain(retriever, combine_docs_chain)
        
        print("RAG chain created")
        return self.rag_chain
    
    def setup(self, force_rebuild=False):
        """Setup RAG system."""
        index_exists = Path(self.index_path).exists()
        
        if index_exists and not force_rebuild:
            # Load existing index
            self.load_vectorstore()
        else:
            # Build new index
            documents = self.load_documents()
            chunks = self.split_documents(documents)
            self.create_vectorstore(chunks)
        
        # Create RAG chain
        self.create_rag_chain()
        
        print("\n✓ RAG system ready!")
    
    def query(self, question: str):
        """Query the RAG system."""
        if self.rag_chain is None:
            raise ValueError("RAG chain not initialized. Call setup() first.")
        
        print(f"\n{'='*70}")
        print(f"Question: {question}")
        print(f"{'='*70}\n")
        
        result = self.rag_chain.invoke({"input": question})
        
        print(f"Answer: {result['answer']}\n")
        
        print("Sources:")
        for i, doc in enumerate(result['context'], 1):
            source = doc.metadata.get('source', 'Unknown')
            print(f"{i}. {source}")
        
        print(f"{'='*70}\n")
        
        return result

def main():
    """Main function."""
    
    # Example: Create sample documents
    docs_dir = "./sample_docs"
    os.makedirs(docs_dir, exist_ok=True)
    
    # Create sample documents
    with open(f"{docs_dir}/doc1.txt", "w") as f:
        f.write("""
LangChain is a framework for developing applications powered by language models.
It provides tools for chains, agents, memory, and more.
LangChain supports multiple LLM providers including OpenAI, Anthropic, and others.
""")
    
    with open(f"{docs_dir}/doc2.txt", "w") as f:
        f.write("""
LangGraph is an extension of LangChain for building stateful, multi-actor applications.
It provides graph-based orchestration with state management.
LangGraph is ideal for complex workflows with conditional logic.
""")
    
    # Initialize RAG system
    rag = RAGSystem(docs_dir)
    
    # Setup (creates vector store)
    rag.setup(force_rebuild=True)
    
    # Example queries
    queries = [
        "What is LangChain?",
        "What is LangGraph used for?",
        "What LLM providers does LangChain support?",
    ]
    
    for query in queries:
        rag.query(query)

if __name__ == "__main__":
    main()
