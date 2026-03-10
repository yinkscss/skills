# Chains Reference

## Overview

Chains are sequences of calls to LLMs, tools, or data processing steps. LangChain provides LCEL (LangChain Expression Language) for building composable chains.

## Table of Contents

1. [LCEL Basics](#lcel-basics)
2. [Chain Types](#chain-types)
3. [Composition](#composition)
4. [Parallel Execution](#parallel-execution)
5. [Advanced Patterns](#advanced-patterns)

## LCEL Basics

### Simple Chain

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

const prompt = ChatPromptTemplate.fromMessages([
  ["system", "You are a helpful assistant."],
  ["user", "{input}"]
]);

const model = new ChatOpenAI({ model: "gpt-4" });
const outputParser = new StringOutputParser();

// Chain using pipe operator
const chain = prompt.pipe(model).pipe(outputParser);

const result = await chain.invoke({ input: "Hello!" });
```

### Chain Syntax

```typescript
// Using .pipe()
const chain = step1.pipe(step2).pipe(step3);

// Equivalent to manual composition
const chain = {
  invoke: async (input) => {
    const result1 = await step1.invoke(input);
    const result2 = await step2.invoke(result1);
    return await step3.invoke(result2);
  }
};
```

## Chain Types

### Sequential Chain

Process steps one after another:

```typescript
const translationChain = ChatPromptTemplate
  .fromTemplate("Translate to French: {text}")
  .pipe(model)
  .pipe(new StringOutputParser());

const result = await translationChain.invoke({ text: "Hello world" });
// "Bonjour le monde"
```

### Retrieval Chain

Combine retrieval with generation:

```typescript
import { createRetrievalChain } from "langchain/chains/retrieval";
import { createStuffDocumentsChain } from "langchain/chains/combine_documents";

const retriever = vectorStore.asRetriever();

const combineDocsChain = await createStuffDocumentsChain({
  llm: model,
  prompt: ChatPromptTemplate.fromMessages([
    ["system", "Answer based on context: {context}"],
    ["user", "{input}"]
  ])
});

const retrievalChain = await createRetrievalChain({
  retriever,
  combineDocsChain
});

const result = await retrievalChain.invoke({
  input: "What is LangChain?"
});
```

### Conversation Chain

Maintain chat history:

```typescript
import { ConversationChain } from "langchain/chains";
import { BufferMemory } from "langchain/memory";

const memory = new BufferMemory();

const chain = new ConversationChain({
  llm: model,
  memory: memory
});

await chain.invoke({ input: "Hi, I'm Alice" });
await chain.invoke({ input: "What's my name?" });
// "Your name is Alice"
```

## Composition

### Chaining Multiple Steps

```typescript
const step1 = ChatPromptTemplate
  .fromTemplate("Summarize this text: {text}")
  .pipe(model)
  .pipe(new StringOutputParser());

const step2 = ChatPromptTemplate
  .fromTemplate("Translate to Spanish: {summary}")
  .pipe(model)
  .pipe(new StringOutputParser());

// Compose into single chain
const fullChain = RunnableSequence.from([
  { summary: step1 },
  step2
]);

const result = await fullChain.invoke({
  text: "Long article text..."
});
```

### Branching Logic

```typescript
import { RunnableBranch } from "@langchain/core/runnables";

const classificationChain = ChatPromptTemplate
  .fromTemplate("Classify sentiment: {text}")
  .pipe(model)
  .pipe(new StringOutputParser());

const branch = RunnableBranch.from([
  [
    (input) => input.includes("positive"),
    positiveResponseChain
  ],
  [
    (input) => input.includes("negative"),
    negativeResponseChain
  ],
  neutralResponseChain  // default
]);

const result = await branch.invoke("The text is positive");
```

### With Fallbacks

```typescript
const primaryChain = prompt.pipe(expensiveModel);
const fallbackChain = prompt.pipe(cheapModel);

const chainWithFallback = primaryChain.withFallbacks([fallbackChain]);

const result = await chainWithFallback.invoke({ input: "Hello" });
```

## Parallel Execution

### RunnableParallel

Execute multiple chains simultaneously:

```typescript
import { RunnableParallel } from "@langchain/core/runnables";

const analysisChain = RunnableParallel.from({
  sentiment: sentimentChain,
  summary: summaryChain,
  keywords: keywordChain
});

const result = await analysisChain.invoke({ text: "Article text..." });
// {
//   sentiment: "positive",
//   summary: "Brief summary",
//   keywords: ["ai", "ml", "tech"]
// }
```

### Map-Reduce Pattern

```typescript
// Map: Process each document
const mapChain = ChatPromptTemplate
  .fromTemplate("Summarize: {doc}")
  .pipe(model)
  .pipe(new StringOutputParser());

// Reduce: Combine summaries
const reduceChain = ChatPromptTemplate
  .fromTemplate("Combine these summaries: {summaries}")
  .pipe(model)
  .pipe(new StringOutputParser());

// Process multiple documents
const documents = ["Doc 1", "Doc 2", "Doc 3"];
const summaries = await Promise.all(
  documents.map(doc => mapChain.invoke({ doc }))
);

const finalSummary = await reduceChain.invoke({
  summaries: summaries.join("\n")
});
```

## Advanced Patterns

### Router Chain

Route to different chains based on input:

```typescript
import { RouterChain } from "langchain/chains";

const mathChain = createMathChain();
const historyChain = createHistoryChain();
const generalChain = createGeneralChain();

const router = new RouterChain({
  chains: {
    math: mathChain,
    history: historyChain,
    general: generalChain
  },
  routerChain: createRouterChain()  // Decides which chain to use
});

const result = await router.invoke("What is 2+2?");
// Routes to mathChain
```

### Transform Chain

Apply custom transformations:

```typescript
import { RunnableLambda } from "@langchain/core/runnables";

const transform = new RunnableLambda({
  func: (input: string) => input.toUpperCase()
});

const chain = transform
  .pipe(prompt)
  .pipe(model);

const result = await chain.invoke("hello");
// Processes "HELLO"
```

### Streaming Chains

```typescript
const streamingChain = prompt
  .pipe(model)
  .pipe(new StringOutputParser());

const stream = await streamingChain.stream({ input: "Tell me a story" });

for await (const chunk of stream) {
  process.stdout.write(chunk);
}
```

### Batch Processing

```typescript
const chain = prompt.pipe(model).pipe(new StringOutputParser());

const inputs = [
  { input: "Question 1" },
  { input: "Question 2" },
  { input: "Question 3" }
];

const results = await chain.batch(inputs);
// Process all inputs efficiently
```

### Caching

```typescript
import { InMemoryCache } from "@langchain/core/caches";

const cache = new InMemoryCache();

const chain = prompt
  .pipe(model.bind({ cache }))
  .pipe(new StringOutputParser());

// First call hits the model
await chain.invoke({ input: "What is AI?" });

// Second call uses cache
await chain.invoke({ input: "What is AI?" });
```

## Best Practices

### 1. Name Your Chains

```typescript
const chain = prompt
  .pipe(model)
  .pipe(new StringOutputParser())
  .withConfig({ runName: "translation_chain" });
```

### 2. Add Retry Logic

```typescript
const chain = prompt
  .pipe(model.bind({ maxRetries: 3 }))
  .pipe(outputParser);
```

### 3. Handle Errors

```typescript
const chain = prompt
  .pipe(model)
  .pipe(new StringOutputParser())
  .withFallbacks([
    defaultChain
  ]);
```

### 4. Use Structured Output

```typescript
import { StructuredOutputParser } from "langchain/output_parsers";

const parser = StructuredOutputParser.fromZodSchema(
  z.object({
    answer: z.string(),
    confidence: z.number()
  })
);

const chain = prompt
  .pipe(model)
  .pipe(parser);
```

### 5. Monitor Performance

```typescript
import { CallbackManager } from "@langchain/core/callbacks/manager";

const chain = prompt
  .pipe(
    model.bind({
      callbacks: CallbackManager.fromHandlers({
        handleChainStart: async () => {
          console.time("chain");
        },
        handleChainEnd: async () => {
          console.timeEnd("chain");
        }
      })
    })
  );
```

## Common Chain Patterns

### Question Answering

```typescript
const qaChain = ChatPromptTemplate
  .fromTemplate(`Answer the question based on context:
    
Context: {context}
Question: {question}

Answer:`)
  .pipe(model)
  .pipe(new StringOutputParser());
```

### Text Summarization

```typescript
const summaryChain = ChatPromptTemplate
  .fromTemplate("Summarize in 3 sentences: {text}")
  .pipe(model)
  .pipe(new StringOutputParser());
```

### Data Extraction

```typescript
import { JsonOutputParser } from "@langchain/core/output_parsers";

const extractionChain = ChatPromptTemplate
  .fromTemplate(`Extract structured data from: {text}
  
Format: JSON with fields: name, age, email`)
  .pipe(model)
  .pipe(new JsonOutputParser());
```

### Multi-Step Reasoning

```typescript
const reasoningChain = RunnableSequence.from([
  {
    analysis: ChatPromptTemplate
      .fromTemplate("Analyze: {input}")
      .pipe(model),
    
    context: (input) => input
  },
  ChatPromptTemplate
    .fromTemplate("Based on {analysis}, answer: {context}")
    .pipe(model),
  
  new StringOutputParser()
]);
```
