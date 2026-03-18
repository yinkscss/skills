---
name: prompt-engineering
description: "Comprehensive guide for prompt engineering — the syntax and foundation layer of the AI Engineering Stack. Use when crafting, optimizing, or analyzing prompts for large language models. Essential for (1) Structural formatting with XML delimiters to separate instructions from data, (2) In-Context Learning via zero-shot, one-shot, and few-shot paradigms, (3) Cognitive scaffolding with Chain-of-Thought reasoning and thinking tags, (4) Meta prompting — using AI to generate and critique its own prompts, (5) Advanced techniques (self-consistency, tree of thoughts, prompt chaining, reflexion), (6) Mitigating risks like prompt injection and hallucinations, (7) Understanding model capabilities and optimising for specific tasks. For context design and RAG pipelines, see the context-engineering skill. For agent alignment and trade-off hierarchies, see the intent-engineering skill."
license: Complete terms in LICENSE.txt
---

# Prompt Engineering

The foundation layer ("The Syntax") of the AI Engineering Stack. Prompt engineering is the craft of manipulating the probabilistic distribution of a model's next-token generation through clear structural formatting, in-context learning, and cognitive scaffolding.

## Quick Start

### When to Use Which Technique

| Task Type | Technique | See |
|-----------|-----------|-----|
| Simple tasks | Zero-shot | [Techniques](references/techniques.md#zero-shot-prompting) |
| Specific format needed | Few-shot | [Techniques](references/techniques.md#few-shot-prompting) |
| Complex reasoning | Chain-of-Thought ⭐ | [Techniques](references/techniques.md#chain-of-thought-cot-prompting-) |
| Critical decisions | Self-Consistency | [Techniques](references/techniques.md#self-consistency) |
| Strategic planning | Tree of Thoughts | [Techniques](references/techniques.md#tree-of-thoughts-tot) |
| Knowledge queries | RAG | [Techniques](references/techniques.md#retrieval-augmented-generation-rag) |
| Tool integration | ART | [Techniques](references/techniques.md#automatic-reasoning-and-tool-use-art) |
| Multi-step workflows | Prompt Chaining | [Techniques](references/techniques.md#prompt-chaining) |
| Iterative improvement | Reflexion | [Techniques](references/techniques.md#reflexion) |
| Strategic framing | Question Stacking | [Question Stacking](references/question-stacking.md) |
| Complex scoping | Socratic Meta-Prompt | [Question Stacking](references/question-stacking.md#advanced-application-the-socratic-meta-prompt) |

## Core Prompt Writing Rules

**CRITICAL: Follow these rules when writing prompts:**

1. **Use structural delimiters**: Use XML tags (`<role>`, `<context>`, `<task>`, `<format>`, `<constraints>`) to strictly separate instructions from data. This prevents prompt injection and guides model attention. Never write prompts as continuous prose.

2. **Use imperative verbs**: Start instructions with action verbs (Write, Classify, Summarize, Translate, Extract, Generate, Analyze, Compare)

3. **Be explicit and specific**: Specify exact output format, length constraints, style requirements, structural elements

4. **Structure lists hierarchically**:
   - Use consistent formatting (all dashes or all asterisks)
   - Maintain parallel structure (same grammatical form)
   - Order logically (importance, chronological, complexity)
   - Indent sub-items consistently

5. **Avoid negative instructions**: State what TO do, not what NOT to do
   - ❌ "Don't include personal information"
   - ✅ "Include only public domain information"

6. **Provide context boundaries**: Define scope, constraints, and boundaries explicitly

7. **Specify output format precisely**: markdown, JSON, plain text, structured lists, etc.

8. **Use examples strategically**: Ensure examples are representative, consistent, clear, and properly formatted

9. **Eliminate ambiguity**: Every instruction must have one clear interpretation. Audit for hidden ambiguity — words like "better" or "creative" need structural definitions.

## Fundamental Techniques

### Zero-Shot Prompting
Instruct the model without examples. Use for simple, well-defined tasks.

**Structure:**
```
[Clear task description]
[Explicit instruction with action verb]
[Output format specification]
```

### Few-Shot Prompting
Provide 2-5 examples to guide the model's response pattern.

**Structure:**
```
[Task description]
Example 1: Input → Output
Example 2: Input → Output
Example 3: Input → Output
[New input to process]
```

**Rules:**
- Use 2-5 examples (more confuses, fewer insufficient)
- Ensure examples are diverse but consistent
- Maintain consistent formatting

### Chain-of-Thought (CoT) Prompting ⭐ **MOST IMPORTANT**

LLMs don't have internal monologues. Their "thinking" only happens as they generate tokens. By forcing the model to output intermediate reasoning steps, you give it temporary working memory.

**Zero-shot CoT:**
```
[Problem statement]
Let's think step by step:
[Model generates reasoning]
[Final answer]
```

**Thinking Tags Pattern:**
Force reasoning inside `<thinking>` tags, then produce the final answer separately:
```xml
<task>
IMPORTANT: Before providing your answer, work through your reasoning
step-by-step inside <thinking> tags.
</task>

<thinking>
[Model's step-by-step reasoning here]
</thinking>

**Answer:** [Final answer based on reasoning]
```

**Variations:**
- **Zero-shot CoT**: Add "Let's think step by step"
- **Few-shot CoT**: Provide examples with explicit reasoning
- **Manual CoT**: Provide explicit numbered reasoning steps
- **Thinking Tags**: Contain reasoning in `<thinking>` tags (best for complex analysis)

**Important**: CoT adds latency and token cost. Use it when reasoning complexity demands it, not for simple tasks.

**See [Techniques Reference](references/techniques.md#chain-of-thought-cot-prompting-) for detailed examples and variations.**

### Self-Consistency
Generate multiple reasoning paths (3-5) and select the most consistent answer. Use for tasks with multiple valid paths or when reliability is critical.

### Tree of Thoughts (ToT)
Maintain a tree of thoughts, exploring multiple reasoning paths systematically. Use for strategic problem-solving and complex planning.

### Program-Aided Language Models (PAL)
Generate programs as reasoning steps. Use for mathematical problems, algorithmic tasks, data manipulation.

## Question Stacking & Socratic Techniques

Instead of asking AI for output directly, first ask it to surface the right questions — then answer them — then execute. This forces the model to adopt expert framing before generating, reducing shallow or misaligned outputs.

**The Pattern:**
```
"What would a [expert role] ask before [doing task]?
What information would they need?
What assumptions would they validate first?
Now answer those questions for [specific context], then [execute task]."
```

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

**The Socratic Meta-Prompt** takes this further: a full reusable system prompt that operationalizes question stacking as a structured intake workflow. The model interrogates the request through three lenses — ambiguity detection (INTERROGATOR), assumption auditing (LOGIC TESTER), and constraint definition (CONSTRAINT MANAGER) — before executing.

| Prompt Type | When to Use | Expected Gain |
|---|---|---|
| Direct instruction | Clear, bounded tasks | Speed |
| Question stacking | Strategic or multi-step tasks | Better framing |
| Socratic meta-prompt | Complex scoping sessions | Precision + reduced rework |

> The quality of AI output is limited by the quality of the frame you give it. Question stacking forces the model to build the right frame before it builds anything else.

**See [Question Stacking & Socratic Techniques](references/question-stacking.md) for the full pattern, domain-specific examples (strategy, engineering, code review), and the complete Socratic Meta-Prompt system prompt.**

## Advanced Techniques

### Generated Knowledge Prompting
Generate relevant background knowledge before answering. Use for knowledge-intensive queries.

### Least-to-Most Prompting
Break complex tasks into simpler sub-tasks, solving sequentially.

### Self-Refine
Iteratively refine outputs using self-generated feedback.

### Maieutic Prompting
Engage in Socratic dialogue for deeper understanding.

### Meta Prompting
Emphasize structural and syntactical aspects over specific content.

### Automatic Prompt Engineer (APE)
Framework for automatic instruction generation and selection.

**See [Techniques Reference](references/techniques.md) for all 20+ techniques with detailed explanations, examples, and best practices.**

## Retrieval & Agent Techniques

### Retrieval Augmented Generation (RAG)
Combine information retrieval with generation. Essential for knowledge-intensive tasks.

**Best practices:**
- Retrieve 3-5 relevant documents
- Include source citations
- Filter for relevance
- Handle missing documents gracefully

### Automatic Reasoning and Tool-use (ART)
Combine CoT with tool use for complex multi-step operations.

### Prompt Chaining
Break tasks into subtasks, using output of one as input for next.

### Reflexion
Introduce self-evaluation and reflection to learn from mistakes.

**See [Techniques Reference](references/techniques.md) for detailed implementation patterns.**

## Context Engineering

Design and optimize complete interaction context beyond individual prompts.

**Core components:**
- **System prompts**: Define agent behavior, role, capabilities
- **Task constraints**: Guide decision-making with explicit boundaries
- **Tool descriptions**: Clarify available functions and usage
- **Memory management**: Track state across interactions
- **Error handling**: Define failure handling patterns

**Best practices:**
- Eliminate all ambiguity
- Make expectations explicit
- Implement observability for debugging
- Iterate based on observed behavior
- Balance flexibility with necessary constraints

**See [Context Engineering Guide](references/context-engineering.md) for comprehensive patterns and implementation details.**

## Applications

Prompt engineering applies across many domains:

- **Fine-tuning**: Customize models for specific tasks
- **Deep Research**: Multi-step research with RAG and chaining
- **Context Caching**: Efficiently analyze large documents
- **Function Calling**: Integrate external tools and APIs
- **Document Processing**: Summarization, extraction, analysis
- **Code Generation**: Generate, explain, debug code
- **Content Creation**: Articles, marketing, documentation
- **Data Analysis**: Statistical analysis, insights generation

**See [Applications Guide](references/applications.md) for detailed patterns and implementations for each application.**

## Model Considerations

Different models require different approaches:

**Model size:**
- Small (1-7B): Faster, cheaper, less reasoning depth
- Medium (7-13B): Balance of capability and efficiency
- Large (13B+): Best reasoning, higher cost, slower

**Model types:**
- **Instruction-tuned**: Use clear, direct instructions
- **Base models**: Provide more context, use few-shot examples
- **Reasoning models**: Leverage CoT, allow reasoning space

**Context windows:**
- Short (2K-4K): Keep prompts concise
- Medium (8K-32K): Standard use cases
- Long (64K+): Complex documents, long conversations

**See [Model Guide](references/models.md) for model-specific optimization strategies.**

## Risk Mitigation

### Prompt Injection
**Prevention:** Validate inputs, use system prompts for boundaries, separate user content from instructions, implement filtering

### Hallucinations
**Mitigation:** Use RAG, request citations, cross-verify information, use self-consistency, implement fact-checking

### Biases
**Mitigation:** Use diverse examples, request balanced perspectives, test for bias patterns, apply debiasing techniques

### Output Quality Issues
**Solutions:** Specify language explicitly, request concise outputs, use structured formats, provide style guidelines

**See [Risk Management Guide](references/risks.md) for comprehensive mitigation strategies.**

## Prompt Writing Checklist

Before finalizing any prompt:

- [ ] Uses imperative verbs for all instructions
- [ ] Specifies exact output format
- [ ] Includes length constraints if needed
- [ ] Provides examples when helpful (2-5 for few-shot)
- [ ] Eliminates all ambiguity
- [ ] States what TO do (not what NOT to do)
- [ ] Defines scope and boundaries clearly
- [ ] Uses consistent formatting for lists
- [ ] Maintains parallel structure in lists
- [ ] Includes error handling instructions if needed
- [ ] Specifies style and tone requirements
- [ ] Uses appropriate technique for the task

## The System Prompt "Goldilocks" Rule

When crafting system prompts, avoid the two common failure modes:
- **Too vague:** Instructions like "Do a good job" provide no useful constraint or guidance.
- **Too prescriptive:** Hardcoding complex `if-then` logic into the system prompt. LLMs are reasoning engines; they should handle conditional reasoning dynamically, not be pre-programmed with brittle logic trees.

**The Sweet Spot:** Define the desired *outcomes*, the broad approach, and the constraints. Let the model fill in the conditional logic required to reach the outcome.

## Architectural Hierarchy

Prompt engineering is Layer 1 of the 3-layer AI Engineering Stack. Understanding this hierarchy prevents the "wrong tool for the wrong layer" problem:

1. **Prompt (Layer 1 - Syntax):** Dictates immediate instruction following and formatting. *Lives inside Context.*
2. **Context (Layer 2 - Information):** Knowledge infrastructure, RAG, and memory. *Lives inside Intent.*
3. **Intent (Layer 3 - Strategy):** Organisational purpose, guardrails, and business objectives.

## Tool Descriptions as Prompt Engineering

Writing tool function descriptions for agents is a distinct prompt engineering discipline:
- **Describe Purpose, Not Implementation:** Focus on what the tool achieves.
- **Full Schemas:** Include complete, accurate input parameter schemas and exact output schemas.
- **Information Density:** Keep it concise. Over-describing wastes tokens and creates noise; under-describing leads to hallucinated arguments and failed tool invocations.

The LLM reads these descriptions directly to determine: "Can I call this tool? Do I have all the required inputs yet? What format will the return data be in?"

## Historical Framing

Prompt engineering was the first iteration of AI interaction — an individual, synchronous, session-based discipline where one human iterated with one model to capture personal value. 

While prompt engineering remains the syntax foundation, **Context Engineering** and **Intent Engineering** are the organisational disciplines required to scale AI across teams, long time horizons, and autonomous agent runs.

## Reference Materials

For detailed information on specific topics:

- **[Techniques Reference](references/techniques.md)** — All 20+ prompting techniques with examples, structures, and best practices
- **[Prompt Templates](references/templates.md)** — Production-ready templates: Structural Formatting, Few-Shot Quality Control, CoT Analysis, Meta Prompt Generator
- **[Context Engineering Guide](references/context-engineering.md)** — Deep dive on context design, patterns, and implementation
- **[Applications Guide](references/applications.md)** — Detailed patterns for fine-tuning, research, document processing, code generation, etc.
- **[Risk Management](references/risks.md)** — Comprehensive strategies for prompt injection, hallucinations, biases, and quality issues
- **[Model Guide](references/models.md)** — Model-specific considerations, selection, and optimization strategies
- **[Question Stacking & Socratic Techniques](references/question-stacking.md)** — Question stacking pattern, domain examples, Socratic Meta-Prompt, and usage decision framework

## Related Skills

- **context-engineering** — For building RAG pipelines, AGENTS.md files, and MCP servers
- **intent-engineering** — For defining agent objectives, trade-off hierarchies, and stop rules

## Anti-Patterns

**Don't:**
- Use vague instructions like "make it better"
- Mix positive and negative instructions
- Provide inconsistent examples
- Use ambiguous pronouns without clear referents
- Assume model knows implicit context
- Use overly complex nested structures
- Provide too many examples (>10)
- Mix different output formats in examples

**Do:**
- Be explicit and specific
- Use consistent formatting
- Provide clear examples
- Define all terms
- Specify exact requirements
- Test prompts iteratively
- Validate outputs
- Document what works
