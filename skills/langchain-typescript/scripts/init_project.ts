#!/usr/bin/env node

/**
 * Initialize a new LangChain TypeScript project
 * 
 * Usage: tsx init_project.ts <project-name> [--template simple|langgraph|rag]
 */

import * as fs from "fs/promises";
import * as path from "path";

interface ProjectConfig {
  name: string;
  template: "simple" | "langgraph" | "rag";
}

const templates = {
  simple: {
    description: "Simple agent with tool calling",
    files: ["agent.ts", "package.json", "README.md"]
  },
  langgraph: {
    description: "Advanced LangGraph agent with state management",
    files: ["graph-agent.ts", "package.json", "README.md"]
  },
  rag: {
    description: "RAG application for question answering",
    files: ["rag.ts", "package.json", "README.md"]
  }
};

async function parseArgs(): Promise<ProjectConfig> {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === "--help" || args[0] === "-h") {
    console.log(`
LangChain TypeScript Project Initializer

Usage:
  tsx init_project.ts <project-name> [--template <type>]

Templates:
  simple     - Simple agent with tool calling (default)
  langgraph  - Advanced agent with LangGraph
  rag        - RAG application

Examples:
  tsx init_project.ts my-agent
  tsx init_project.ts my-app --template langgraph
  tsx init_project.ts qa-bot --template rag
    `);
    process.exit(0);
  }
  
  const name = args[0];
  const templateIndex = args.indexOf("--template");
  const template = templateIndex !== -1 && args[templateIndex + 1]
    ? args[templateIndex + 1] as "simple" | "langgraph" | "rag"
    : "simple";
  
  if (!["simple", "langgraph", "rag"].includes(template)) {
    console.error(`Invalid template: ${template}`);
    console.error("Available templates: simple, langgraph, rag");
    process.exit(1);
  }
  
  return { name, template };
}

async function copyTemplate(
  templatePath: string,
  targetPath: string
): Promise<void> {
  const files = await fs.readdir(templatePath);
  
  for (const file of files) {
    const sourcePath = path.join(templatePath, file);
    const destPath = path.join(targetPath, file);
    
    const stat = await fs.stat(sourcePath);
    
    if (stat.isDirectory()) {
      await fs.mkdir(destPath, { recursive: true });
      await copyTemplate(sourcePath, destPath);
    } else {
      await fs.copyFile(sourcePath, destPath);
    }
  }
}

async function createProject(config: ProjectConfig): Promise<void> {
  const { name, template } = config;
  
  console.log(`\n🚀 Creating LangChain TypeScript project: ${name}`);
  console.log(`   Template: ${template} - ${templates[template].description}\n`);
  
  // Create project directory
  const projectPath = path.join(process.cwd(), name);
  
  try {
    await fs.access(projectPath);
    console.error(`❌ Error: Directory '${name}' already exists`);
    process.exit(1);
  } catch {
    // Directory doesn't exist, proceed
  }
  
  await fs.mkdir(projectPath, { recursive: true });
  console.log(`✅ Created directory: ${name}`);
  
  // Determine template source path
  const scriptDir = path.dirname(new URL(import.meta.url).pathname);
  const templatePath = path.join(scriptDir, "..", "assets", `${template}-agent`);
  
  // Copy template files
  await copyTemplate(templatePath, projectPath);
  console.log(`✅ Copied template files`);
  
  // Create additional config files
  await createConfigFiles(projectPath);
  console.log(`✅ Created configuration files`);
  
  // Create .gitignore
  await fs.writeFile(
    path.join(projectPath, ".gitignore"),
    `node_modules/
dist/
.env
.env.local
*.log
.DS_Store
`
  );
  console.log(`✅ Created .gitignore`);
  
  // Create .env.example
  await fs.writeFile(
    path.join(projectPath, ".env.example"),
    `OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT=${name}
`
  );
  console.log(`✅ Created .env.example`);
  
  console.log(`\n✨ Project created successfully!\n`);
  console.log(`Next steps:`);
  console.log(`  1. cd ${name}`);
  console.log(`  2. npm install`);
  console.log(`  3. cp .env.example .env`);
  console.log(`  4. Edit .env and add your API keys`);
  console.log(`  5. npm run dev\n`);
}

async function createConfigFiles(projectPath: string): Promise<void> {
  // tsconfig.json
  const tsconfig = {
    compilerOptions: {
      target: "ES2022",
      module: "ESNext",
      moduleResolution: "bundler",
      esModuleInterop: true,
      strict: true,
      skipLibCheck: true,
      resolveJsonModule: true,
      outDir: "./dist",
      rootDir: "./",
      declaration: true,
      declarationMap: true,
      sourceMap: true
    },
    include: ["**/*.ts"],
    exclude: ["node_modules", "dist"]
  };
  
  await fs.writeFile(
    path.join(projectPath, "tsconfig.json"),
    JSON.stringify(tsconfig, null, 2)
  );
  
  // .editorconfig
  const editorconfig = `root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
`;
  
  await fs.writeFile(
    path.join(projectPath, ".editorconfig"),
    editorconfig
  );
}

// Main execution
async function main() {
  try {
    const config = await parseArgs();
    await createProject(config);
  } catch (error) {
    console.error(`\n❌ Error: ${(error as Error).message}`);
    process.exit(1);
  }
}

main();
