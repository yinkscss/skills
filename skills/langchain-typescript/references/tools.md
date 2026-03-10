# Tools Reference

## Overview

Tools allow agents to interact with external systems, APIs, and data sources. LangChain provides built-in tools and makes it easy to create custom ones.

## Table of Contents

1. [Built-in Tools](#built-in-tools)
2. [Creating Custom Tools](#creating-custom-tools)
3. [Tool Calling](#tool-calling)
4. [MCP Integration](#mcp-integration)
5. [Tool Patterns](#tool-patterns)

## Built-in Tools

### Search Tools

```typescript
import { DuckDuckGoSearch } from "@langchain/community/tools/duckduckgo_search";
import { WikipediaQueryRun } from "@langchain/community/tools/wikipedia_query_run";

const search = new DuckDuckGoSearch({ maxResults: 5 });
const wiki = new WikipediaQueryRun({ topKResults: 3 });

const result = await search.invoke("TypeScript best practices");
```

### Calculator

```typescript
import { Calculator } from "@langchain/community/tools/calculator";

const calculator = new Calculator();
const result = await calculator.invoke("2 + 2 * 3");  // "8"
```

### Web Browser

```typescript
import { WebBrowser } from "langchain/tools/webbrowser";
import { ChatOpenAI } from "@langchain/openai";

const browser = new WebBrowser({
  model: new ChatOpenAI(),
  embeddings: new OpenAIEmbeddings()
});

const content = await browser.invoke("https://example.com");
```

## Creating Custom Tools

### Using DynamicStructuredTool

```typescript
import { DynamicStructuredTool } from "@langchain/core/tools";
import { z } from "zod";

const weatherTool = new DynamicStructuredTool({
  name: "get_weather",
  description: "Get current weather for a location",
  schema: z.object({
    location: z.string().describe("City name"),
    units: z.enum(["celsius", "fahrenheit"]).default("celsius")
  }),
  func: async ({ location, units }) => {
    // Call weather API
    const weather = await fetchWeather(location, units);
    return JSON.stringify(weather);
  }
});
```

### Using tool Decorator

```typescript
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const searchDatabase = tool(
  async ({ query, limit }) => {
    const results = await db.search(query, limit);
    return results;
  },
  {
    name: "search_database",
    description: "Search the internal database",
    schema: z.object({
      query: z.string().describe("Search query"),
      limit: z.number().default(10).describe("Max results")
    })
  }
);
```

### Tool Class

```typescript
import { Tool } from "@langchain/core/tools";

class CustomTool extends Tool {
  name = "custom_tool";
  description = "Performs a custom operation";
  
  async _call(input: string): Promise<string> {
    // Tool logic here
    return `Processed: ${input}`;
  }
}

const tool = new CustomTool();
```

## Tool Calling

### With Agents

```typescript
import { createReactAgent } from "@langchain/langgraph/prebuilt";

const tools = [weatherTool, searchDatabase, calculator];

const agent = createReactAgent({
  llm: model,
  tools: tools
});

const result = await agent.invoke({
  messages: [{ role: "user", content: "What's the weather in NYC?" }]
});
```

### Manual Tool Execution

```typescript
// Model decides which tool to use
const modelWithTools = model.bind({ tools });

const response = await modelWithTools.invoke([
  new HumanMessage("What's 15 * 24?")
]);

// Extract tool call
const toolCall = response.additional_kwargs.tool_calls?.[0];

if (toolCall) {
  // Find the tool
  const tool = tools.find(t => t.name === toolCall.function.name);
  
  // Execute it
  const args = JSON.parse(toolCall.function.arguments);
  const result = await tool?.invoke(args);
  
  console.log(result);
}
```

### ToolNode (LangGraph)

```typescript
import { ToolNode } from "@langchain/langgraph/prebuilt";

const toolNode = new ToolNode(tools);

// In a graph
graph
  .addNode("agent", agentNode)
  .addNode("tools", toolNode)
  .addConditionalEdges("agent", shouldContinue, {
    continue: "tools",
    end: END
  })
  .addEdge("tools", "agent");
```

## MCP Integration

### Using MCP Tools

Model Context Protocol (MCP) enables standardized tool integrations:

```typescript
import { MCPClient } from "@modelcontextprotocol/sdk/client/index.js";

const client = new MCPClient({
  name: "my-app",
  version: "1.0.0"
});

// Connect to MCP server
await client.connect(transport);

// List available tools
const { tools } = await client.listTools();

// Call MCP tool
const result = await client.callTool({
  name: "tool_name",
  arguments: { param: "value" }
});
```

### Creating MCP-Compatible Tools

```typescript
// Your tool automatically works with MCP
const myTool = tool(
  async ({ input }) => {
    return processInput(input);
  },
  {
    name: "process_data",
    description: "Processes data according to rules",
    schema: z.object({
      input: z.string()
    })
  }
);
```

## Tool Patterns

### Error Handling

```typescript
const robustTool = tool(
  async ({ url }) => {
    try {
      const response = await fetch(url);
      return await response.text();
    } catch (error) {
      return `Error fetching ${url}: ${error.message}`;
    }
  },
  {
    name: "fetch_url",
    description: "Fetch content from URL",
    schema: z.object({ url: z.string().url() })
  }
);
```

### Async Tools

```typescript
const asyncTool = tool(
  async ({ query }) => {
    const results = await Promise.all([
      searchEngine1(query),
      searchEngine2(query),
      searchEngine3(query)
    ]);
    return combineResults(results);
  },
  {
    name: "multi_search",
    description: "Search multiple sources in parallel",
    schema: z.object({ query: z.string() })
  }
);
```

### Tools with State

```typescript
class StatefulTool extends Tool {
  name = "counter";
  description = "Increment a counter";
  private count = 0;
  
  async _call(input: string): Promise<string> {
    this.count++;
    return `Count: ${this.count}`;
  }
}
```

### Composed Tools

```typescript
const composedTool = tool(
  async ({ query }) => {
    // Use multiple tools in sequence
    const searchResults = await searchTool.invoke(query);
    const analyzed = await analyzeTool.invoke(searchResults);
    const summary = await summaryTool.invoke(analyzed);
    return summary;
  },
  {
    name: "research_and_summarize",
    description: "Research a topic and provide a summary",
    schema: z.object({ query: z.string() })
  }
);
```

### Rate-Limited Tools

```typescript
import pLimit from "p-limit";

const limit = pLimit(5);  // Max 5 concurrent calls

const rateLimitedTool = tool(
  async ({ url }) => {
    return limit(async () => {
      return await fetch(url);
    });
  },
  {
    name: "rate_limited_fetch",
    description: "Fetch with rate limiting",
    schema: z.object({ url: z.string() })
  }
);
```

## Best Practices

### 1. Descriptive Names and Descriptions

```typescript
// Good
const tool = new DynamicStructuredTool({
  name: "search_customer_database",
  description: "Search the customer database by name, email, or ID. Returns customer details including contact info and purchase history.",
  // ...
});

// Bad
const tool = new DynamicStructuredTool({
  name: "search",
  description: "Searches stuff",
  // ...
});
```

### 2. Validate Inputs

```typescript
const tool = tool(
  async ({ email }) => {
    if (!email.includes("@")) {
      throw new Error("Invalid email format");
    }
    return await lookupUser(email);
  },
  {
    name: "lookup_user",
    description: "Look up user by email",
    schema: z.object({
      email: z.string().email()  // Zod validates format
    })
  }
);
```

### 3. Return Structured Data

```typescript
const tool = tool(
  async ({ city }) => {
    const weather = await getWeather(city);
    
    // Return JSON string for agent to parse
    return JSON.stringify({
      temperature: weather.temp,
      condition: weather.condition,
      humidity: weather.humidity
    });
  },
  // ...
);
```

### 4. Handle Rate Limits

```typescript
async function callWithRetry(tool: Tool, input: any, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await tool.invoke(input);
    } catch (error) {
      if (error.message.includes("rate limit") && i < maxRetries - 1) {
        await sleep(Math.pow(2, i) * 1000);  // Exponential backoff
        continue;
      }
      throw error;
    }
  }
}
```

### 5. Log Tool Usage

```typescript
const loggedTool = tool(
  async (input) => {
    console.log(`[${new Date().toISOString()}] Tool called:`, input);
    const result = await performOperation(input);
    console.log(`[${new Date().toISOString()}] Tool result:`, result);
    return result;
  },
  // ...
);
```

## Common Tool Examples

### API Tool

```typescript
const apiTool = tool(
  async ({ endpoint, method, body }) => {
    const response = await fetch(`https://api.example.com/${endpoint}`, {
      method,
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined
    });
    return await response.json();
  },
  {
    name: "call_api",
    description: "Make API calls to the backend",
    schema: z.object({
      endpoint: z.string(),
      method: z.enum(["GET", "POST", "PUT", "DELETE"]),
      body: z.record(z.any()).optional()
    })
  }
);
```

### Database Tool

```typescript
const dbTool = tool(
  async ({ query }) => {
    const results = await prisma.$queryRaw`${query}`;
    return JSON.stringify(results);
  },
  {
    name: "query_database",
    description: "Execute SQL queries on the database",
    schema: z.object({
      query: z.string().describe("SQL query to execute")
    })
  }
);
```

### File System Tool

```typescript
import fs from "fs/promises";

const readFileTool = tool(
  async ({ path }) => {
    try {
      const content = await fs.readFile(path, "utf-8");
      return content;
    } catch (error) {
      return `Error reading file: ${error.message}`;
    }
  },
  {
    name: "read_file",
    description: "Read contents of a file",
    schema: z.object({
      path: z.string().describe("File path to read")
    })
  }
);
```
