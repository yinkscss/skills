import { StateGraph, MessagesAnnotation, START, END } from "@langchain/langgraph";
import { ChatOpenAI } from "@langchain/openai";
import { ToolNode } from "@langchain/langgraph/prebuilt";
import { DuckDuckGoSearch } from "@langchain/community/tools/duckduckgo_search";
import { MemorySaver } from "@langchain/langgraph";

/**
 * LangGraph Agent Template
 * 
 * This template demonstrates a graph-based agent with:
 * - State management
 * - Conditional routing
 * - Tool execution
 * - Persistence
 */

// Configure tools
const tools = [
  new DuckDuckGoSearch({ maxResults: 5 })
];

const toolNode = new ToolNode(tools);

// Configure model with tool binding
const model = new ChatOpenAI({
  model: "gpt-4",
  temperature: 0
}).bindTools(tools);

// Define agent node
async function callModel(state: typeof MessagesAnnotation.State) {
  const response = await model.invoke(state.messages);
  return { messages: [response] };
}

// Define routing logic
function shouldContinue(state: typeof MessagesAnnotation.State) {
  const lastMessage = state.messages[state.messages.length - 1];
  
  // If the LLM called tools, execute them
  if ("tool_calls" in lastMessage && lastMessage.tool_calls?.length > 0) {
    return "tools";
  }
  
  // Otherwise, end the conversation
  return END;
}

// Build the graph
const workflow = new StateGraph(MessagesAnnotation)
  .addNode("agent", callModel)
  .addNode("tools", toolNode)
  .addEdge(START, "agent")
  .addConditionalEdges("agent", shouldContinue, {
    tools: "tools",
    [END]: END
  })
  .addEdge("tools", "agent");  // Loop back after tool execution

// Compile with persistence
const checkpointer = new MemorySaver();
const graph = workflow.compile({ checkpointer });

// Run the agent
async function main() {
  const userQuery = "What are the latest developments in AI?";
  
  console.log(`User: ${userQuery}\n`);
  
  // Create a thread for this conversation
  const config = {
    configurable: {
      thread_id: "conversation-1"
    }
  };
  
  // Invoke with streaming
  const stream = await graph.stream(
    {
      messages: [{ role: "user", content: userQuery }]
    },
    {
      ...config,
      streamMode: "values"
    }
  );
  
  // Process stream
  for await (const event of stream) {
    const lastMessage = event.messages[event.messages.length - 1];
    if (lastMessage.content) {
      console.log(`\n${lastMessage._getType()}: ${lastMessage.content}`);
    }
  }
  
  // Continue conversation
  console.log("\n--- Second turn ---\n");
  
  const followUp = await graph.invoke(
    {
      messages: [{ role: "user", content: "Can you summarize that?" }]
    },
    config  // Same thread maintains context
  );
  
  const finalMessage = followUp.messages[followUp.messages.length - 1];
  console.log(`\nAssistant: ${finalMessage.content}`);
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

export { graph };
