"""
LangGraph Agent with State Management

An advanced agent using LangGraph for complex workflows with:
- State management
- Conditional routing
- Persistence
- Human-in-the-loop support
"""

import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# Load environment variables
load_dotenv()

# Define state schema
class AgentState(TypedDict):
    """State for the agent workflow."""
    messages: Annotated[list, add]  # Accumulates messages
    iterations: int
    result: str
    status: str

# Define tools
@tool
def research_tool(query: str) -> str:
    """Research information on a topic."""
    return f"Research results for: {query}"

@tool
def analysis_tool(data: str) -> str:
    """Analyze data and extract insights."""
    return f"Analysis of: {data}"

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# Initialize components
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [research_tool, analysis_tool, calculator]

# Create React agent
react_agent = create_react_agent(
    llm,
    tools,
    messages_modifier="You are a helpful assistant. Use tools when needed."
)

# Define nodes
def agent_node(state: AgentState):
    """Main agent processing node."""
    print(f"\n[Agent Node] Iteration {state['iterations'] + 1}")
    
    # Run agent
    result = react_agent.invoke(state)
    
    return {
        "messages": result["messages"],
        "iterations": state["iterations"] + 1,
        "status": "processing"
    }

def should_continue(state: AgentState) -> str:
    """Decide whether to continue or end."""
    
    # Check if we have a final answer
    last_message = state["messages"][-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    
    # Check iteration limit
    if state["iterations"] >= 5:
        return "end"
    
    # Check if task is complete
    if "final" in last_message.content.lower():
        return "end"
    
    return "continue"

def finalize_node(state: AgentState):
    """Finalize the result."""
    print("\n[Finalize Node] Preparing final output")
    
    last_message = state["messages"][-1]
    
    return {
        "result": last_message.content,
        "status": "complete"
    }

# Build the graph
def create_workflow():
    """Create the LangGraph workflow."""
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("finalize", finalize_node)
    
    # Add edges
    workflow.add_edge(START, "agent")
    
    # Conditional routing
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "agent",  # Loop back
            "end": "finalize"
        }
    )
    
    workflow.add_edge("finalize", END)
    
    # Compile with checkpointer for persistence
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    
    return app

def run_agent(query: str):
    """Run the agent with a query."""
    
    print(f"\n{'='*70}")
    print(f"Query: {query}")
    print(f"{'='*70}")
    
    # Create app
    app = create_workflow()
    
    # Configure with thread ID for persistence
    config = {"configurable": {"thread_id": "example-1"}}
    
    # Initial state
    initial_state = {
        "messages": [("user", query)],
        "iterations": 0,
        "result": "",
        "status": "started"
    }
    
    # Run workflow
    final_state = app.invoke(initial_state, config)
    
    print(f"\n{'='*70}")
    print(f"Result: {final_state['result']}")
    print(f"Iterations: {final_state['iterations']}")
    print(f"Status: {final_state['status']}")
    print(f"{'='*70}\n")
    
    return final_state

def main():
    """Main function."""
    
    # Example queries
    queries = [
        "Research AI trends and calculate the market size",
        "Analyze the benefits of machine learning in healthcare",
        "What is 25 * 17 + 50?",
    ]
    
    for query in queries:
        run_agent(query)

if __name__ == "__main__":
    main()
