# Context Engineering Templates

## Template 1: Context Gap Analysis

Use when your AI consistently underperforms. Turns the model into a diagnostic tool for your own system.

```xml
<role>
You are a context engineering consultant. Your job is to identify exactly what information is missing, ambiguous, or contradictory in the context you've been given — and explain how each gap affects your ability to complete the task accurately.
</role>

<context>
[Paste the full context you currently provide to your AI for this task]
</context>

<task>
I need you to [describe the task this context is meant to support, e.g., "write accurate product descriptions for our e-commerce store"].

Before attempting the task, perform a thorough context audit:

1. **MISSING INFORMATION:** List every piece of information you would need to complete this task reliably that is NOT present in <context>. For each item, explain specifically how its absence would degrade your output.

2. **AMBIGUOUS INFORMATION:** Identify any statements in <context> that could be interpreted multiple ways. For each, list possible interpretations and explain which one you'd default to (and why that default might be wrong).

3. **CONTRADICTORY INFORMATION:** Flag any statements that conflict with each other. Explain how you'd resolve the contradiction and why that resolution might be incorrect.

4. **NOISE:** Identify any information in <context> that is irrelevant to the task and could distract from the core objective.

5. **CONTEXT SCORE:** Rate the context 1-10 for task readiness, with a one-sentence justification.

6. **PRIORITY FIXES:** List the top 3 context additions that would most improve output quality, ranked by impact.
</task>

<format>
Use the numbered structure above. Be specific and actionable — don't say "more product information needed," say "the material composition and care instructions for each product are missing, which means I'll either hallucinate these details or omit them."
</format>
```

---

## Template 2: AGENTS.md Generator

Bootstrap a machine-readable context file from a plain-language project description.

```xml
<role>
You are a context engineering specialist who creates machine-readable context files for AI agents.
</role>

<task>
I'm going to describe my project/business/workflow. Based on what I tell you, generate a complete `AGENTS.md` file that any AI agent could consume to immediately understand:

- What this project is and what problem it solves
- The tech stack, tools, and conventions in use
- The coding/writing/communication standards we follow
- The boundaries and rules an AI must respect when working on this project
- Common mistakes an AI would make without this context

Here's my project description:
[Describe your project, business, or workflow in plain language — be thorough]
</task>

<format>
Generate the file using this structure:

# AGENTS.md

## Project Overview
[What this project is, who it serves, what success looks like]

## Tech Stack & Tools
[Languages, frameworks, platforms, integrations]

## Conventions & Standards
[Naming conventions, file structures, formatting rules, communication tone]

## Domain Knowledge
[Key terms, business logic, industry-specific rules the AI must understand]

## Boundaries & Constraints
[What the AI must NEVER do, compliance requirements, security boundaries]

## Common Tasks
[The 5-10 most frequent tasks an AI will be asked to perform, with brief guidance on each]

## Known Pitfalls
[Mistakes AI agents commonly make on this project and how to avoid them]
</format>
```

---

## Template 3: RAG Architecture Designer

Design your RAG pipeline before writing any code.

```xml
<role>
You are a senior AI infrastructure engineer specialising in Retrieval-Augmented Generation systems.
</role>

<context>
I have the following data source that I need to make searchable by an AI agent:

- **Data type:** [e.g., internal company wiki, legal contracts, customer support transcripts, technical documentation, codebase]
- **Total size:** [e.g., 500 documents, ~2 million words]
- **Structure:** [e.g., highly structured with headers/sections, semi-structured, unstructured prose, mixed media]
- **Primary use case:** [e.g., "Customer support agents need to find accurate answers to product questions in under 3 seconds"]
- **Accuracy requirements:** [e.g., "Zero tolerance for hallucination — answers must cite the exact source document"]
</context>

<task>
Design a complete RAG pipeline architecture for this use case:

1. **Chunking Strategy:** Recommend optimal approach (Fixed-size, Recursive Character, Semantic, Hierarchical, Code-aware). Specify chunk sizes for Search (small) and Retrieve (large) stages.

2. **Embedding Model:** Recommend a specific model and justify.

3. **Vector Database:** Recommend store (Chroma, Pinecone, Weaviate, Qdrant) and justify.

4. **Retrieval Strategy:** Semantic only, hybrid (semantic + keyword), or re-ranking pipeline? Explain trade-offs.

5. **Evaluation Plan:** Define 3 metrics (chunk attribution, answer faithfulness, retrieval precision).

6. **Failure Modes:** Top 3 ways this pipeline could fail and how to detect each early.
</task>

<format>
For each recommendation, provide: The recommendation, Why it's best for THIS use case, What would go wrong with the alternative.
</format>
```

---

## Template 4: MCP Server Blueprint

Design an MCP server's capability schema.

```xml
<role>
You are an AI systems architect specialising in Model Context Protocol (MCP) server design.
</role>

<context>
I want to build an MCP server that gives AI agents access to:
[Describe your data sources and tools, e.g., "our PostgreSQL customer database, our internal Confluence wiki, and our Stripe billing API"]

The agents using this server will primarily need to:
[Describe the tasks, e.g., "answer customer questions about their accounts, look up billing history, and find relevant help articles"]

Security requirements:
[e.g., "Agents must never see raw credit card numbers. All database queries must be read-only. API calls to Stripe must be limited to lookup operations only — no mutations."]
</context>

<task>
Design the complete MCP server blueprint:

1. **Resources** (read-only data): List each resource with schema, description, access level, and explicitly redacted data.

2. **Tools** (executable functions): List each with name, input parameters, return type, description, rate limits, and permission boundaries.

3. **Prompts** (reusable templates): Design 2-3 server-side prompt templates for the most common agent tasks.

4. **Transport recommendation:** STDIO (local) vs. HTTP/SSE (remote) — recommend the right transport and explain.

5. **Security boundaries:** Explicit data redaction rules, read-only vs. read-write operations, conditions for refusing requests.
</task>
```
