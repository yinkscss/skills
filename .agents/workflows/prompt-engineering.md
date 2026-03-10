---
description: Audit agent alignment with prompt-engineering principles
---

# Prompt Engineering Audit

1. Read the `prompt-engineering` skill documentation to ensure you have the latest principles in context: use `view_file` on `/Users/mac/Downloads/2026/skills/skills/prompt-engineering/SKILL.md`.
2. Verify that your system prompts adhere to the **System Prompt Goldilocks Rule**: they must not be too vague, nor too prescriptive (no hardcoded if-then logic trees). Define *outcomes* and constraints instead.
3. Validate your prompts against the **Architectural Hierarchy**: understand that the prompt is Layer 1 (Syntax), which lives inside Context (Layer 2), which lives inside Intent (Layer 3).
4. Review any **Tool Descriptions** you've written: they must describe the purpose (not implementation), have full schemas, and be concise.
5. Check against the core prompt writing rules: use structural delimiters (XML tags), imperative verbs, and explicit format specifications. Ensure Zero-Shot, Few-Shot, or Chain-of-Thought (CoT) techniques are used appropriately.
6. Provide a markdown checklist to the user summarizing your prompt engineering alignment, flagging any gaps or violations of the principles outlined in `SKILL.md`. Stop and wait for the user's feedback or confirmation before proceeding.
