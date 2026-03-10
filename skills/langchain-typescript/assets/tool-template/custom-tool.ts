import { tool } from "@langchain/core/tools";
import { z } from "zod";

/**
 * Custom Tool Template
 * 
 * This template shows how to create custom tools for LangChain agents.
 * Tools extend agent capabilities by connecting to APIs, databases, or custom logic.
 */

// Example 1: Simple Tool
export const weatherTool = tool(
  async ({ location }) => {
    // Your API call or logic here
    const temperature = Math.floor(Math.random() * 30) + 50;
    return JSON.stringify({
      location,
      temperature: `${temperature}°F`,
      condition: "Sunny"
    });
  },
  {
    name: "get_weather",
    description: "Get current weather for a location. Use this when users ask about weather, temperature, or climate.",
    schema: z.object({
      location: z.string().describe("City name or location")
    })
  }
);

// Example 2: Database Tool
export const searchDatabaseTool = tool(
  async ({ query, limit = 10 }) => {
    // Simulated database search
    // Replace with actual database queries
    const results = [
      { id: 1, title: "Result 1", relevance: 0.95 },
      { id: 2, title: "Result 2", relevance: 0.87 }
    ];
    
    return JSON.stringify({
      query,
      results: results.slice(0, limit),
      total: results.length
    });
  },
  {
    name: "search_database",
    description: "Search the internal database for information. Returns relevant records.",
    schema: z.object({
      query: z.string().describe("Search query"),
      limit: z.number().default(10).describe("Maximum number of results to return")
    })
  }
);

// Example 3: API Integration Tool
export const apiTool = tool(
  async ({ endpoint, method = "GET", body }) => {
    try {
      const response = await fetch(`https://api.example.com/${endpoint}`, {
        method,
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${process.env.API_KEY}`
        },
        body: body ? JSON.stringify(body) : undefined
      });
      
      const data = await response.json();
      return JSON.stringify(data);
    } catch (error: any) {
      return `Error calling API: ${error.message}`;
    }
  },
  {
    name: "call_api",
    description: "Make HTTP requests to the API. Use for fetching or updating data.",
    schema: z.object({
      endpoint: z.string().describe("API endpoint path (e.g., 'users/123')"),
      method: z.enum(["GET", "POST", "PUT", "DELETE"]).default("GET"),
      body: z.record(z.any()).optional().describe("Request body for POST/PUT")
    })
  }
);

// Example 4: File System Tool
export const readFileTool = tool(
  async ({ path }) => {
    try {
      const fs = await import("fs/promises");
      const content = await fs.readFile(path, "utf-8");
      return content;
    } catch (error: any) {
      return `Error reading file: ${error.message}`;
    }
  },
  {
    name: "read_file",
    description: "Read contents of a file from the filesystem",
    schema: z.object({
      path: z.string().describe("Full path to the file")
    })
  }
);

// Example 5: Complex Tool with Multiple Operations
export const dataProcessorTool = tool(
  async ({ data, operation }) => {
    const operations = {
      sum: (arr: number[]) => arr.reduce((a, b) => a + b, 0),
      average: (arr: number[]) => arr.reduce((a, b) => a + b, 0) / arr.length,
      max: (arr: number[]) => Math.max(...arr),
      min: (arr: number[]) => Math.min(...arr),
      sort: (arr: number[]) => [...arr].sort((a, b) => a - b)
    };
    
    try {
      const numbers = JSON.parse(data);
      const result = operations[operation as keyof typeof operations](numbers);
      
      return JSON.stringify({
        operation,
        input: numbers,
        result
      });
    } catch (error: any) {
      return `Error processing data: ${error.message}`;
    }
  },
  {
    name: "process_data",
    description: "Process numerical data with various operations (sum, average, max, min, sort)",
    schema: z.object({
      data: z.string().describe("JSON array of numbers"),
      operation: z.enum(["sum", "average", "max", "min", "sort"]).describe("Operation to perform")
    })
  }
);

// Example 6: Async Tool with Error Handling
export const emailTool = tool(
  async ({ to, subject, body }) => {
    try {
      // Simulate email sending
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      console.log(`Email sent to ${to}: ${subject}`);
      
      return JSON.stringify({
        success: true,
        to,
        subject,
        timestamp: new Date().toISOString()
      });
    } catch (error: any) {
      return JSON.stringify({
        success: false,
        error: error.message
      });
    }
  },
  {
    name: "send_email",
    description: "Send an email to a recipient. Use when user wants to send notifications or messages.",
    schema: z.object({
      to: z.string().email().describe("Recipient email address"),
      subject: z.string().describe("Email subject line"),
      body: z.string().describe("Email message body")
    })
  }
);

// Using tools with an agent
async function example() {
  const { ChatOpenAI } = await import("@langchain/openai");
  const { createReactAgent } = await import("@langchain/langgraph/prebuilt");
  
  const model = new ChatOpenAI({ model: "gpt-4" });
  
  const tools = [
    weatherTool,
    searchDatabaseTool,
    apiTool,
    readFileTool,
    dataProcessorTool,
    emailTool
  ];
  
  const agent = createReactAgent({
    llm: model,
    tools: tools
  });
  
  const result = await agent.invoke({
    messages: [
      { role: "user", content: "What's the weather in San Francisco?" }
    ]
  });
  
  console.log(result.messages[result.messages.length - 1].content);
}

// Export all tools
export const allTools = [
  weatherTool,
  searchDatabaseTool,
  apiTool,
  readFileTool,
  dataProcessorTool,
  emailTool
];
