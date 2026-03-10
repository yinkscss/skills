# Complete Examples

## Overview

Full working examples demonstrating common LangChain patterns and use cases.

## Table of Contents

1. [Simple Chatbot](#simple-chatbot)
2. [RAG Application](#rag-application)
3. [Research Agent](#research-agent)
4. [Multi-Agent System](#multi-agent-system)
5. [Human-in-the-Loop Workflow](#human-in-the-loop-workflow)

## Simple Chatbot

A basic conversational chatbot with memory:

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { BufferMemory } from "langchain/memory";
import { ConversationChain } from "langchain/chains";

class SimpleChatbot {
  private chain: ConversationChain;
  private memory: BufferMemory;
  
  constructor() {
    this.memory = new BufferMemory({
      returnMessages: true,
      memoryKey: "chat_history"
    });
    
    const model = new ChatOpenAI({
      model: "gpt-4",
      temperature: 0.7
    });
    
    this.chain = new ConversationChain({
      llm: model,
      memory: this.memory
    });
  }
  
  async chat(message: string): Promise<string> {
    const response = await this.chain.invoke({ input: message });
    return response.response;
  }
  
  async reset(): Promise<void> {
    await this.memory.clear();
  }
}

// Usage
const chatbot = new SimpleChatbot();
console.log(await chatbot.chat("Hi, I'm Alice"));
console.log(await chatbot.chat("What's my name?"));
```

## RAG Application

Retrieval-Augmented Generation for question answering:

```typescript
import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { createStuffDocumentsChain } from "langchain/chains/combine_documents";
import { createRetrievalChain } from "langchain/chains/retrieval";

class RAGApplication {
  private retriever: any;
  private chain: any;
  
  async initialize(documents: string[]) {
    // 1. Split documents into chunks
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 1000,
      chunkOverlap: 200
    });
    
    const docs = await splitter.createDocuments(documents);
    
    // 2. Create vector store
    const vectorStore = await MemoryVectorStore.fromDocuments(
      docs,
      new OpenAIEmbeddings()
    );
    
    this.retriever = vectorStore.asRetriever(4);
    
    // 3. Create QA chain
    const model = new ChatOpenAI({
      model: "gpt-4",
      temperature: 0
    });
    
    const prompt = ChatPromptTemplate.fromMessages([
      ["system", `Answer the question based only on this context:
      
{context}

If you don't know the answer, say you don't know.`],
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
  }
  
  async query(question: string) {
    const result = await this.chain.invoke({ input: question });
    
    return {
      answer: result.answer,
      sources: result.context.map((doc: any) => doc.pageContent)
    };
  }
}

// Usage
const rag = new RAGApplication();

await rag.initialize([
  "LangChain is a framework for building LLM applications...",
  "LangGraph is used for complex agent orchestration...",
  "TypeScript provides type safety for LangChain..."
]);

const result = await rag.query("What is LangGraph?");
console.log(result.answer);
console.log("Sources:", result.sources);
```

## Research Agent

An agent that researches topics using multiple tools:

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { DuckDuckGoSearch } from "@langchain/community/tools/duckduckgo_search";
import { WikipediaQueryRun } from "@langchain/community/tools/wikipedia_query_run";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

class ResearchAgent {
  private agent: any;
  
  constructor() {
    const model = new ChatOpenAI({
      model: "gpt-4",
      temperature: 0
    });
    
    // Create custom summarization tool
    const summarizeTool = tool(
      async ({ text }) => {
        const summaryModel = new ChatOpenAI({ model: "gpt-3.5-turbo" });
        const response = await summaryModel.invoke([
          { role: "system", content: "Summarize this text in 3 sentences:" },
          { role: "user", content: text }
        ]);
        return response.content;
      },
      {
        name: "summarize",
        description: "Summarize long text into key points",
        schema: z.object({
          text: z.string().describe("Text to summarize")
        })
      }
    );
    
    const tools = [
      new DuckDuckGoSearch({ maxResults: 5 }),
      new WikipediaQueryRun({ topKResults: 2 }),
      summarizeTool
    ];
    
    this.agent = createReactAgent({
      llm: model,
      tools,
      messageModifier: `You are a research assistant.

When researching a topic:
1. Use search to find current information
2. Use Wikipedia for background/definitions
3. Use summarize to distill long content
4. Synthesize findings into a comprehensive answer

Always cite your sources.`
    });
  }
  
  async research(topic: string): Promise<string> {
    const result = await this.agent.invoke({
      messages: [
        { 
          role: "user", 
          content: `Research this topic and provide a comprehensive summary: ${topic}` 
        }
      ]
    });
    
    const lastMessage = result.messages[result.messages.length - 1];
    return lastMessage.content;
  }
}

// Usage
const researcher = new ResearchAgent();
const report = await researcher.research("Impact of AI on software development");
console.log(report);
```

## Multi-Agent System

Multiple specialized agents working together:

```typescript
import { StateGraph, MessagesAnnotation, START, END } from "@langchain/langgraph";
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";

class MultiAgentSystem {
  private graph: any;
  
  constructor() {
    const model = new ChatOpenAI({ model: "gpt-4" });
    
    // Specialist agents
    const researchAgent = createReactAgent({
      llm: model,
      tools: [new DuckDuckGoSearch()],
      messageModifier: "You are a research specialist. Find factual information."
    });
    
    const writerAgent = createReactAgent({
      llm: model,
      tools: [],
      messageModifier: "You are a writer. Create engaging content from research."
    });
    
    const editorAgent = createReactAgent({
      llm: model,
      tools: [],
      messageModifier: "You are an editor. Improve clarity and fix errors."
    });
    
    // Orchestration
    const graph = new StateGraph(MessagesAnnotation)
      .addNode("research", researchAgent)
      .addNode("write", writerAgent)
      .addNode("edit", editorAgent)
      .addEdge(START, "research")
      .addEdge("research", "write")
      .addEdge("write", "edit")
      .addEdge("edit", END);
    
    this.graph = graph.compile();
  }
  
  async process(topic: string): Promise<string> {
    const result = await this.graph.invoke({
      messages: [
        { role: "user", content: `Create an article about: ${topic}` }
      ]
    });
    
    const finalMessage = result.messages[result.messages.length - 1];
    return finalMessage.content;
  }
}

// Usage
const system = new MultiAgentSystem();
const article = await system.process("The future of renewable energy");
console.log(article);
```

## Human-in-the-Loop Workflow

Workflow that pauses for human approval:

```typescript
import { StateGraph, Annotation, START, END } from "@langchain/langgraph";
import { MemorySaver } from "@langchain/langgraph";
import { ChatOpenAI } from "@langchain/openai";

const WorkflowState = Annotation.Root({
  input: Annotation<string>(),
  draft: Annotation<string>(),
  approved: Annotation<boolean>(),
  final: Annotation<string>()
});

class HumanInLoopWorkflow {
  private graph: any;
  private checkpointer: MemorySaver;
  
  constructor() {
    this.checkpointer = new MemorySaver();
    const model = new ChatOpenAI({ model: "gpt-4" });
    
    // Create draft
    const createDraft = async (state: typeof WorkflowState.State) => {
      const response = await model.invoke([
        { role: "user", content: `Create content for: ${state.input}` }
      ]);
      return { draft: response.content };
    };
    
    // Wait for approval
    const awaitApproval = async (state: typeof WorkflowState.State) => {
      // This node just passes through - approval happens externally
      return {};
    };
    
    // Finalize
    const finalize = async (state: typeof WorkflowState.State) => {
      return { final: state.draft };
    };
    
    // Router
    const router = (state: typeof WorkflowState.State) => {
      return state.approved ? "finalize" : "create_draft";
    };
    
    const graph = new StateGraph(WorkflowState)
      .addNode("create_draft", createDraft)
      .addNode("await_approval", awaitApproval)
      .addNode("finalize", finalize)
      .addEdge(START, "create_draft")
      .addEdge("create_draft", "await_approval")
      .addConditionalEdges("await_approval", router, {
        finalize: "finalize",
        create_draft: "create_draft"
      })
      .addEdge("finalize", END);
    
    this.graph = graph.compile({
      checkpointer: this.checkpointer,
      interruptBefore: ["await_approval"]
    });
  }
  
  async start(input: string, threadId: string) {
    const config = { configurable: { thread_id: threadId } };
    
    // Run until approval needed
    await this.graph.invoke({ input }, config);
    
    // Get current state
    const state = await this.graph.getState(config);
    return state.values.draft;
  }
  
  async approve(threadId: string, approved: boolean) {
    const config = { configurable: { thread_id: threadId } };
    
    // Update state with approval decision
    await this.graph.updateState(config, { approved });
    
    // Continue execution
    const result = await this.graph.invoke(null, config);
    return result.final;
  }
}

// Usage
const workflow = new HumanInLoopWorkflow();

// Step 1: Start workflow
const draft = await workflow.start("Write a blog post about AI", "thread-1");
console.log("Draft:", draft);

// Step 2: Human reviews draft
const humanApproves = true;  // Or false to regenerate

// Step 3: Continue workflow
const final = await workflow.approve("thread-1", humanApproves);
console.log("Final:", final);
```

## Advanced: Streaming Chat with Next.js

Full Next.js implementation with streaming:

```typescript
// app/api/chat/route.ts
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { DuckDuckGoSearch } from "@langchain/community/tools/duckduckgo_search";
import { MemorySaver } from "@langchain/langgraph";

export const runtime = "edge";

const checkpointer = new MemorySaver();

export async function POST(req: Request) {
  const { messages, sessionId } = await req.json();
  
  const model = new ChatOpenAI({
    model: "gpt-4",
    streaming: true
  });
  
  const tools = [new DuckDuckGoSearch({ maxResults: 3 })];
  
  const agent = createReactAgent({
    llm: model,
    tools
  });
  
  const graph = agent.compile({ checkpointer });
  
  const stream = await graph.stream(
    { messages },
    {
      streamMode: "values",
      configurable: { thread_id: sessionId }
    }
  );
  
  const encoder = new TextEncoder();
  
  const readable = new ReadableStream({
    async start(controller) {
      for await (const chunk of stream) {
        const lastMessage = chunk.messages[chunk.messages.length - 1];
        if (lastMessage.content) {
          controller.enqueue(encoder.encode(lastMessage.content + "\n"));
        }
      }
      controller.close();
    }
  });
  
  return new Response(readable, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive"
    }
  });
}
```

```typescript
// app/page.tsx
"use client";

import { useState } from "react";

export default function Chat() {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  
  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMessage = { role: "user", content: input };
    setMessages([...messages, userMessage]);
    setInput("");
    setLoading(true);
    
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: [...messages, userMessage],
        sessionId: "user-session"
      })
    });
    
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let assistantMessage = "";
    
    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;
      
      assistantMessage += decoder.decode(value);
      setMessages([
        ...messages,
        userMessage,
        { role: "assistant", content: assistantMessage }
      ]);
    }
    
    setLoading(false);
  };
  
  return (
    <div className="flex flex-col h-screen p-4">
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((msg, i) => (
          <div key={i} className={`mb-2 ${msg.role === "user" ? "text-right" : "text-left"}`}>
            <span className={`inline-block p-2 rounded ${
              msg.role === "user" ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}>
              {msg.content}
            </span>
          </div>
        ))}
      </div>
      
      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          className="flex-1 p-2 border rounded"
          placeholder="Type a message..."
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
```
