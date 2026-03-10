"""
Simple LangChain Agent with Tools

A basic agent that can use tools to answer questions.
Includes search and calculator tools.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain import hub

# Load environment variables
load_dotenv()

# Define tools
@tool
def search(query: str) -> str:
    """Search for information online.
    
    Args:
        query: The search query
    
    Returns:
        Search results as a string
    """
    # In production, integrate with a real search API
    # Example: DuckDuckGo, Google Custom Search, etc.
    return f"Mock search results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions.
    
    Args:
        expression: Mathematical expression to evaluate
    
    Returns:
        Calculation result
    """
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

def create_agent():
    """Create and configure the agent."""
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Define tools
    tools = [search, calculator]
    
    # Get default ReAct prompt
    prompt = hub.pull("hwchase17/react")
    
    # Create agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )
    
    return agent_executor

def run_query(agent, query: str):
    """Run a query through the agent."""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}\n")
    
    result = agent.invoke({"input": query})
    
    print(f"\n{'='*60}")
    print(f"Answer: {result['output']}")
    print(f"{'='*60}\n")
    
    return result

def main():
    """Main function."""
    
    # Create agent
    agent = create_agent()
    
    # Example queries
    queries = [
        "What is the capital of France?",
        "Calculate 15 * 23 + 100",
        "Search for information about Python programming",
    ]
    
    for query in queries:
        run_query(agent, query)

if __name__ == "__main__":
    main()
