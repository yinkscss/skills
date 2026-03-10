---
description: Audit agent alignment with context-engineering principles
---

# Context Engineering Audit

1. Read the `context-engineering` skill documentation to ensure you have the latest principles in context: use `view_file` on `/Users/mac/Downloads/2026/skills/skills/context-engineering/SKILL.md`.
2. Analyze your recent actions, proposed architecture, or generated code against the **6-Component Context Schema** and the **Goldilocks Principle** (are you trying to stuff too much into context?).
3. Check any **tool descriptions** you have written. Are they specific, concise, and do they include full schemas?
4. If designing an agent that runs autonomously over multiple iterations, verify you are employing **Long-Horizon Context Strategies** (Compaction, Memory KV store, Agent Decomposition).
5. Ensure you are taking an **Iterative Resource Discovery** approach (e.g., using MCP) rather than predicting and front-loading all resources at once.
6. Provide a markdown checklist to the user summarizing your context engineering alignment, flagging any gaps or violations of the principles outlined in `SKILL.md`. Stop and wait for the user's feedback or confirmation before proceeding.
