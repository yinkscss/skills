import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { DuckDuckGoSearch } from "@langchain/community/tools/duckduckgo_search";
import { Calculator } from "@langchain/community/tools/calculator";

/**
 * Simple ReAct Agent Template
 * 
 * This template creates a basic agent with tool-calling capabilities.
 * Customize the model, tools, and instructions for your use case.
 */

// Configure the language model
const model = new ChatOpenAI({
  model: "gpt-4",           // or "gpt-3.5-turbo" for cheaper option
  temperature: 0,           // 0 = deterministic, 1 = creative
  apiKey: process.env.OPENAI_API_KEY
});

// Configure tools
const tools = [
  new DuckDuckGoSearch({ maxResults: 5 }),
  new Calculator()
  // Add more tools here
];

// Create the agent
const agent = createReactAgent({
  llm: model,
  tools: tools,
  messageModifier: `You are a helpful assistant.
  
Rules:
- Use tools when needed to answer questions accurately
- Be concise but thorough
- Always cite sources when using search results
- Admit when you don't know something`
});

// Run the agent
async function main() {
  const userQuery = "What is the weather in San Francisco and calculate 15 * 24?";
  
  console.log(`User: ${userQuery}\n`);
  
  const result = await agent.invoke({
    messages: [{ role: "user", content: userQuery }]
  });
  
  const lastMessage = result.messages[result.messages.length - 1];
  console.log(`Assistant: ${lastMessage.content}`);
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

export { agent };
