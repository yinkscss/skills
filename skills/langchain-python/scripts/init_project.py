#!/usr/bin/env python3
"""
Initialize a new LangChain Python project from templates.

Usage:
    python init_project.py PROJECT_NAME [--template TEMPLATE]
    
Templates:
    - simple: Basic agent with tools (default)
    - langgraph: Advanced LangGraph workflow
    - rag: RAG Q&A application
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

TEMPLATES = {
    "simple": "simple-agent",
    "langgraph": "langgraph-agent",
    "rag": "rag-app"
}

def create_project(project_name: str, template: str):
    """Create a new LangChain project from template."""
    
    # Get template path
    script_dir = Path(__file__).parent
    template_dir = script_dir.parent / "assets" / TEMPLATES[template]
    
    if not template_dir.exists():
        print(f"Error: Template '{template}' not found at {template_dir}")
        sys.exit(1)
    
    # Create project directory
    project_dir = Path(project_name)
    
    if project_dir.exists():
        print(f"Error: Directory '{project_name}' already exists")
        sys.exit(1)
    
    print(f"Creating project '{project_name}' from '{template}' template...")
    
    # Copy template
    shutil.copytree(template_dir, project_dir)
    
    # Create .env file
    env_file = project_dir / ".env"
    with open(env_file, "w") as f:
        f.write("""# API Keys
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# LangSmith (optional, for tracing)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key-here
LANGCHAIN_PROJECT=my-project
""")
    
    # Create requirements.txt
    requirements = project_dir / "requirements.txt"
    with open(requirements, "w") as f:
        if template == "simple":
            f.write("""langchain==0.1.0
langchain-openai==0.0.5
langchain-community==0.0.20
python-dotenv==1.0.0
""")
        elif template == "langgraph":
            f.write("""langchain==0.1.0
langchain-openai==0.0.5
langgraph==0.0.30
python-dotenv==1.0.0
""")
        elif template == "rag":
            f.write("""langchain==0.1.0
langchain-openai==0.0.5
langchain-community==0.0.20
faiss-cpu==1.7.4
python-dotenv==1.0.0
""")
    
    # Create .gitignore
    gitignore = project_dir / ".gitignore"
    with open(gitignore, "w") as f:
        f.write("""# Environment
.env
venv/
__pycache__/
*.pyc

# Data
*.db
*.sqlite
faiss_index/
chroma_db/

# IDE
.vscode/
.idea/
""")
    
    print(f"\n✓ Project '{project_name}' created successfully!")
    print(f"\nNext steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. python -m venv venv")
    print(f"  3. source venv/bin/activate  # or 'venv\\Scripts\\activate' on Windows")
    print(f"  4. pip install -r requirements.txt")
    print(f"  5. Edit .env with your API keys")
    print(f"  6. Run the main script")
    print(f"\nRead README.md for more information.")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Initialize a new LangChain Python project"
    )
    
    parser.add_argument(
        "project_name",
        help="Name of the project to create"
    )
    
    parser.add_argument(
        "--template",
        "-t",
        choices=list(TEMPLATES.keys()),
        default="simple",
        help="Template to use (default: simple)"
    )
    
    args = parser.parse_args()
    
    create_project(args.project_name, args.template)

if __name__ == "__main__":
    main()
