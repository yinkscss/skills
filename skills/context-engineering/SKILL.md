---
name: context-engineering
description: "Comprehensive guide for context engineering — the systematic practice of designing, optimising, and maintaining the exact configuration of tokens available to an LLM during inference. Use when (1) Building or designing RAG pipelines (chunking strategies, vector databases, hybrid search), (2) Creating machine-readable context files like AGENTS.md or context.yaml (Context as Code), (3) Designing MCP (Model Context Protocol) servers for standardised AI tool/data access, (4) Auditing what context an AI agent has vs. what it needs, (5) Managing AI memory (short-term rolling windows, long-term vector storage), (6) Architecting the full environment an autonomous agent operates in, (7) Optimising context window usage and noise filtering. This skill is the infrastructure layer of the AI Engineering Stack, sitting between prompt engineering (syntax) and intent engineering (strategy)."
---

# Context Engineering

Context engineering is the systematic practice of designing, optimising, and maintaining the exact configuration of tokens available to an LLM during inference.

**Core principle: Your AI agent is only as capable as the information it can immediately access.**

If prompt engineering is giving a digital worker a specific task, context engineering is providing them with the correct files, historical records, tools, and environmental awareness needed to execute that task. The question is not "how do I word this?" but "what specific configuration of context is most likely to generate the desired behaviour?"

## Quick Start: 4 Core Skills

| Skill | Purpose | See |
|-------|---------|-----|
| Context Auditing | Map knowledge gaps before adding context | [Templates](references/templates.md#template-1-context-gap-analysis) |
| Context as Code | Encode context into version-controlled files | [Context as Code](references/context_as_code.md) |
| RAG Pipeline Design | Build retrieval systems for large knowledge bases | [Advanced RAG](references/advanced_rag.md) |
| MCP Server Design | Standardise external tool/data access for agents | [MCP](references/mcp.md) |

## What Context Engineering Encompasses

- **Memory management:** Short-term state (rolling conversation window) and long-term vector storage (persistent indexed facts)
- **Prompt chain management:** Orchestrating multi-step prompt sequences
- **Dynamic variable injection:** Time, system state, user persona
- **Noise filtering:** Precision over volume — wrong context is worse than missing context
- **RAG orchestration:** Semantic chunking, hybrid search, chunk attribution
- **Context as Code:** Version-controlled `AGENTS.md`, `context.yaml` files committed alongside application code
- **MCP integration:** Standardised protocol for tool/data routing

## Where Prompts Fail, Context Succeeds

Every hallucination, every inconsistent output, every "the AI doesn't understand my business" complaint traces back to a **context failure**, not a prompt failure. The model isn't wrong — it's uninformed.

The most common mistake is adding more context when the real problem is wrong context. Dumping an entire company wiki into a prompt drowns the signal in noise.

## The 6-Component Context Window Schema

The context window is not just "a prompt" — it has 6 distinct components with different growth behaviours:
1. **User message:** The initial prompt or instruction.
2. **System prompt:** Static guardrails, roles, and instructions.
3. **Tool descriptions:** Specific, precise schemas of available tools.
4. **Resources:** Business data, private context, or retrieved documents.
5. **Assistant messages:** The conversation history (grows over time/iterations).
6. **Tool calls & results:** History of actions taken and their outcomes (grows over time).

## The Goldilocks Principle of Context

More context ≠ better results. The optimal context window fill is **60–70%**. 

Maxing out the context window with too many tokens consistently degrades the model's output quality, reasoning capability, and instruction-following. It is better to retrieve fewer, highly relevant chunks than to stuff the context window.

## Tool Description Design

Writing tool descriptions is a critical context engineering task:
- **Be specific and concise:** No verbose explanations. Describe the tool's purpose and what data flows in or out.
- **Include full schemas:** Provide complete input parameter schemas and expected output formats.
- **Why it matters:** The LLM reads these to determine if it can call the tool, if it has required inputs, and what to expect back. Under-describing causes hallucinated arguments; over-describing wastes precious tokens.

## Long-Horizon Context Strategies

For agents that run autonomously over many iterations, context management is critical as Assistant Messages and Tool Results grow.

- **Compaction:** Use an LLM call to summarise large retrieved resources (e.g., a 50k token document) into a concise 500-word summary before injecting it into the active agent's context.
- **Memory (Local KV Store):** Attach a local key-value store directly to the agent. Store intermediate results, large JSONs, or bulky contexts here, keyed for retrieval in later steps, keeping the active context window lean.
- **Agent Decomposition:** When a sub-task requires extensive LLM iteration (e.g., complex document search), split it into its own sub-agent. The parent agent delegates the task and only receives the final summary output in its context.

## MCP Iterative Resource Discovery

Instead of predicting all necessary resources upfront, use **Iterative Discovery**:
1. Describe the *available* resources in the context (using MCP or similar).
2. Ask the LLM: "Based on the user message, which of these resources do you need?"
3. Fetch *only* those explicitly requested resources for the next call. 

## Organisational Context Infrastructure

The "shadow agents" problem: Every team rolling their own context stack creates security risks, governance issues, and semantic inconsistency. 

Effective context engineering requires a **Unified Context Infrastructure**:
- Governed access controls for agent data retrieval
- Freshness guarantees for vector stores and indexed data
- Semantic consistency across departments (e.g., the sales agent and engineering agent share the same understanding of a "customer" entity)

## Reference Materials

- **[Advanced RAG](references/advanced_rag.md)** — Search/Retrieve decoupling, chunking strategies, evaluation metrics
- **[Context as Code](references/context_as_code.md)** — AGENTS.md, GitOps for AI memory, context bundling
- **[MCP](references/mcp.md)** — Model Context Protocol architecture, server design, transport layers
- **[Templates](references/templates.md)** — Production-ready templates: Context Gap Analysis, AGENTS.md Generator, RAG Architecture Designer, MCP Server Blueprint
