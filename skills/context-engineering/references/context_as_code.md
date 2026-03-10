# Context as Code Reference

## The Paradigm Shift

Historically, system prompts, data schemas, and API docs were pasted manually into chat interfaces or hardcoded as string literals. This created:
- **Amnesia between sessions** — no persistent memory
- **Untraceable hallucinations** — no way to audit what knowledge drove behaviour
- **Zero reproducibility** — different results every time

A 2024 study found programmers spent up to **11.56% of their coding time** just instructing LLMs with context — nearly equal to the 14.05% spent writing actual code.

## GitOps for AI Memory

The Context as Code paradigm applies strict GitOps principles to AI memory management:

1. Context files, business logic, safety boundaries, and tool schemas get encoded into **structured files** (JSON, YAML, Markdown)
2. Committed directly into **version control** alongside application code
3. Reviewed like code changes (pull requests, diffs)
4. Testable and reproducible

## AGENTS.md — The Machine-Readable Blueprint

Unlike a standard README.md written for humans, `AGENTS.md` is written for AI agents. When an agent is pointed at a codebase, AGENTS.md standardises context injection.

### Recommended Structure

```markdown
# AGENTS.md

## Project Overview
[What this project is, who it serves, what success looks like]

## Tech Stack & Tools
[Languages, frameworks, platforms, integrations]

## Conventions & Standards
[Naming conventions (snake_case vs CamelCase), file structures, formatting rules, communication tone, testing frameworks]

## Domain Knowledge
[Key terms, business logic, industry-specific rules the AI must understand]

## Boundaries & Constraints
[What the AI must NEVER do, compliance requirements, security boundaries]

## Common Tasks
[The 5-10 most frequent tasks an AI will be asked to perform, with brief guidance]

## Known Pitfalls
[Mistakes AI agents commonly make on this project and how to avoid them]
```

## Benefits

### Deterministic Auditing
If an autonomous coding agent introduces a regression, run a deterministic audit by reviewing the exact Git commit of the context file that guided the agent at that timestamp. Context transforms from ephemeral chat state into a **durable, auditable corporate asset**.

### Context Bundling
Ensures every deployed AI tool across large teams shares identical, version-controlled memory about:
- Product vision
- Tone guidelines
- Edge cases
- Compliance requirements

## Other Context File Formats

- **`context.yaml`** — Structured key-value context for tool configuration
- **`rules.json`** — Machine-readable constraint definitions
- **`.cursorrules` / `.windsurfrules`** — IDE-specific AI context files
