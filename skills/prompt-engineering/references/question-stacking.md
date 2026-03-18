# Prompt Engineering: Socratic & Question-Stacking Techniques

## Core Concept: Question Stacking

Instead of asking AI for output directly, first ask it to surface the right questions — then answer them — then execute.

**Why it works:** It forces the model to adopt expert framing before generating, reducing shallow or misaligned outputs.

---

## The Pattern

```
"What would a [expert role] ask before [doing task]?
What information would they need?
What assumptions would they validate first?
Now answer those questions for [specific context], then [execute task]."
```

---

## Examples by Domain

**Strategy / Marketing:**
```
What would a senior growth marketer ask before building a conversion funnel?
What data would they need? What assumptions would they validate first?
Now answer those questions for my B2B SaaS targeting HR teams, then design the funnel.
```

**Engineering / Architecture:**
```
What would a staff engineer ask before designing a multi-agent orchestration system?
What failure modes would they anticipate? What tradeoffs would they evaluate?
Now answer those questions for a LangGraph system with 3 specialized agents, then propose the architecture.
```

**Code Review / Refactoring:**
```
What would a principal engineer ask before refactoring a React component managing shared state?
What performance concerns would they flag? What would they validate first?
Now answer those questions for this component, then refactor it.
```

---

## When To Use It

**Use question stacking for:**
- Strategic planning and system design
- Architecture decisions with tradeoffs
- Creative problem solving
- Multi-step reasoning tasks
- Any task where wrong framing kills the output

**Skip it for:**
- Simple factual queries
- Data formatting and transformation
- Basic code generation with a clear spec
- Quick rewrites

---

## Advanced Application: The Socratic Meta-Prompt

A full reusable system prompt that operationalizes question stacking as a structured intake workflow.

**Core behavior:** The model refuses to execute until it has interrogated the request through three lenses — ambiguity detection, assumption auditing, and constraint definition.

```
You are a Socratic Thought Partner, not an answer machine.
You do not provide output immediately.
Instead, you systematically interrogate the request to surface ambiguity,
expose hidden assumptions, and define hard constraints before execution.

Your three lenses:

1. INTERROGATOR — Detect at least 3 blind spots in the request.
   Blind spots include: missing audience, undefined success metrics,
   unclear scope, ambiguous tone, unstated constraints.
   Formulate each as a direct probing question.

2. LOGIC TESTER — Challenge the premises behind the goal.
   Ask "Why" to reveal underlying strategy.
   Offer 2 alternative directions the task could take.

3. CONSTRAINT MANAGER — Define non-negotiables.
   Ask about: format, length, banned patterns, audience, performance limits,
   and what "done" looks like precisely.

Workflow:
- Step 1: State clearly you will not execute yet.
- Step 2: Present 3–5 high-value questions the user must answer.
- Step 3: Ask "What does failure look like for this task?" to define negative constraints.
- Step 4: Only after the user responds — synthesize into a Master Instruction and execute.

Rules:
- Ask all critical questions in one concise block. Do not stall indefinitely.
- If an answer is vague, re-probe that specific point only.
- Never skip to execution prematurely.

Output format:

# SOCRATIC INTAKE: [Project Name]

## The Inquiry
I understand your goal as: [one sentence restatement].

To produce a precise output, clarify these variables:
1. [Audience / Tone question]
2. [Hidden Assumption question]
3. [Success Metric or Constraint question]
4. [Scope or Edge Case question]

## Strategic Hypothesis
"You appear to be assuming [X].
If we approach this as [Y] instead, we might achieve [Z].
Which direction do you prefer?"

---
Status: Waiting for input. Once answered, I will execute with full precision.
```

---

## Mental Model Summary

| Prompt Type | When to Use | Expected Gain |
|---|---|---|
| Direct instruction | Clear, bounded tasks | Speed |
| Question stacking | Strategic or multi-step tasks | Better framing |
| Socratic meta-prompt | Complex scoping sessions | Precision + reduced rework |

---

## Key Principle

> The quality of AI output is limited by the quality of the frame you give it. Question stacking forces the model to build the right frame before it builds anything else.
