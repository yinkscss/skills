# Simple Agent Template

A basic LangChain agent with tool-calling capabilities.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run the agent:
```bash
npm run dev
```

## Customization

### Change the Model

```typescript
const model = new ChatOpenAI({
  model: "gpt-3.5-turbo",  // Cheaper option
  temperature: 0.7          // More creative
});
```

### Add More Tools

```typescript
import { WikipediaQueryRun } from "@langchain/community/tools/wikipedia_query_run";

const tools = [
  new DuckDuckGoSearch(),
  new Calculator(),
  new WikipediaQueryRun({ topKResults: 3 })
];
```

### Customize Instructions

```typescript
const agent = createReactAgent({
  llm: model,
  tools: tools,
  messageModifier: `You are a customer support agent.
  
Rules:
- Always be polite and professional
- Use the search tool to find up-to-date information
- Escalate to human if issue is complex`
});
```

## Usage

```typescript
const result = await agent.invoke({
  messages: [{ role: "user", content: "Your question here" }]
});

console.log(result.messages[result.messages.length - 1].content);
```
