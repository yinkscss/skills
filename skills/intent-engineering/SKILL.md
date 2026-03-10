---
name: intent-engineering
description: "Comprehensive guide for intent engineering — the structural design of AI systems around goals, constraints, and measurable business outcomes. Use when (1) Defining objectives and success criteria for autonomous AI agents, (2) Building trade-off hierarchies to resolve conflicting priorities, (3) Designing decision autonomy protocols and escalation rules, (4) Creating stop rules and circuit breakers for agent safety, (5) Encoding organisational purpose into machine-readable intent schemas (YAML/JSON), (6) Auditing agent alignment with business strategy, (7) Preventing the intent gap where agents optimise for wrong objectives (e.g. Klarna case study). This skill sits above prompt engineering and context engineering in the AI Engineering Stack."
---

# Intent Engineering

Intent engineering is the structural design of AI systems around goals, constraints, and measurable business outcomes — not surface-level instructions.

It defines **what the system should optimise for over time** and how to make hard trade-offs when objectives conflict. Without intent engineering, even technically brilliant agents optimise for the wrong objectives.

## Core Concept: The Intent Gap

Intent is what determines how an agent acts when instructions run out. Agents only know what you've codified. Most organisations have codified far less than they think.

**Case Study — Klarna (2025):** An AI customer service agent handled 2.3M conversations, equivalent to 853 full-time employees. Resolution time dropped from 11 to 2 minutes. Cost savings: $60M. Technically flawless. But Klarna was forced to rehire human agents because the AI optimised ruthlessly for speed while alienating customers. Nobody had encoded relationship quality, brand trust, or customer lifetime value into the system.

## The 7-Component Intent Framework

Every autonomous agent should have an intent schema before it processes a single request:

| # | Component | Purpose |
|---|-----------|---------|
| 1 | **Objective** | Singular mission statement — the business problem to solve and why it matters |
| 2 | **Desired Outcomes** | Binary, measurable completion criteria from the user's perspective |
| 3 | **Health Metrics** | KPIs that must not degrade (non-regression guardrails) |
| 4 | **Strategic Context** | "Tribal knowledge" — the organisational Why behind the agent |
| 5 | **Constraints** | Hard boundaries: Data, Action, Communication, Compliance |
| 6 | **Decision Autonomy** | Protocols: Autonomous / Notify / Approve / Forbidden |
| 7 | **Stop Rules** | Deterministic kill switches and circuit breakers |

**See [Framework Reference](references/framework.md) for detailed definitions, rules, and examples for each component.**

## Trade-Off Hierarchies

When objectives conflict (speed vs accuracy, cost vs satisfaction), the agent defaults to whichever is easiest to optimise — almost never the right one. Explicitly encode:

1. **Priority ranking** with reasoning
2. **Conflict resolution rules** for each pair of objectives
3. **Override conditions** for exceptional scenarios
4. **Measurement** definitions for each objective

## Vibe Coding vs. Deterministic Intent

Intent engineering is the antidote to "vibe coding" — vaguely describing apps and letting LLMs generate architecture. It forces translation of informal vibes into strict prompt contracts and intent schemas, chaining AI to verifiable logic and organisational strategy.

## Workflow

1. **Define the Objective** — problem-focused, explains why it matters, guides trade-offs
2. **Set Desired Outcomes** — observable state changes, not activities
3. **Establish Health Metrics** — what must not degrade (solves Goodhart's Law)
4. **Provide Strategic Context** — load the organisational "Why"
5. **Encode Constraints** — hard boundaries across 4 categories
6. **Design Decision Autonomy** — escalation protocols
7. **Set Stop Rules** — deterministic kill switches
8. **Build Audit Trails** — make every AI decision traceable

## The PIV Loop as Practical Intent Engineering

The Plan-Implement-Validate (PIV) loop used in agentic coding maps directly to intent engineering phases:
- **Plan (Intent Capture):** Defining objectives, acceptance criteria, and validation criteria up front.
- **Implement (Intent Execution):** Working within defined constraints and boundaries.
- **Validate (Intent Verification):** Measuring outcomes against defined criteria.

Stop rules *are* explicit success conditions — structured agentic workflows have been performing intent engineering all along.

## The Three-Layer Intent Architecture

Intent operates across three distinct organisational layers. Each builds on the previous:

1. **Unified Context Infrastructure (Layer 1):** Agent-accessible data governance and standardisation (e.g., MCP implementation).
2. **AI Workflow Capability Map (Layer 2):** A living map determining which workflows are agent-ready, human-augmented, or human-only.
3. **Goal Translation Infrastructure (Layer 3):** Converts human-readable OKRs into agent-actionable parameters (The True Intent Layer).

## Human-Readable OKRs vs. Machine-Readable Intent

OKRs (Objectives and Key Results) work for humans because humans interpret guidance through institutional context, professional norms, and personal judgment. Agents cannot absorb organisational culture through osmosis.

They require:
- **Agent-Actionable Objectives:** Not "increase satisfaction," but "what observable signals indicate satisfaction, what data sources contain them, what actions am I authorised to take to improve them?"
- **Delegation Frameworks:** Decomposed principles. When request X conflicts with policy Y, use *this* explicit resolution hierarchy.
- **Feedback Loops:** Deterministic mechanisms to measure and correct alignment drift over time.

## Context vs. Autonomy Architectures

### Google ADK Context Layers
Google's Agent Development Kit structures agent context into four governed layers:
- **Working context** (immediate task)
- **Session memory** (current interaction)
- **Long-term memory** (persistent state)
- **Artifacts** (produced outputs)

### Five Levels of AI Autonomy (DeepMind)
Calibrate your intent alignment requirements based on the agent's autonomy level:
1. **Operator:** Executes explicit instructions only.
2. **Collaborator:** Works alongside humans with shared decision-making.
3. **Consultant:** Provides recommendations; humans decide.
4. **Approver:** Acts autonomously but seeks approval for defined boundary cases.
5. **Observer:** Monitors and flags; never acts.

## The Two-Cultures Problem

The people who understand organisational strategy (executives) rarely build agents, and the people building agents (engineers) rarely understand organisational strategy. This gap guarantees an intent failure. 

To solve this, organisations require an **AI Workflow Architect** — a role sitting between engineering, operations, and strategy to ensure agentic systems align with business intent.

## The Intent Race

The AI race in enterprise is no longer about model capability — frontier models are quickly commoditised. 

A company with a mediocre model and extraordinary organisational intent infrastructure will outperform a company with a frontier model and fragmented, unaligned knowledge every single time. The differentiator is the intent architecture, not the model subscription.

## Reference Materials

- **[Framework Reference](references/framework.md)** — Detailed definitions and examples for each of the 7 components, trade-off hierarchies, and audit trail design
- **[Templates Reference](references/templates.md)** — Production-ready prompt templates: Outcome-Driven Task Definition, Full Intent Schema Generator, Trade-Off Matrix, Audit Chain Architecture
