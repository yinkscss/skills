# Prompt Engineering Templates

## Template 1: Structural Formatting Foundation

The single biggest leap in prompt quality. Separates role, context, task, format, and constraints into distinct XML sections.

```xml
<role>
You are a [specific role, e.g., senior data analyst specialising in SaaS metrics].
You communicate in [tone, e.g., clear, direct language suitable for a non-technical executive audience].
</role>

<context>
[Paste your background information, data, or reference material here.
This section should contain ONLY the information the model needs to work with — no instructions.]
</context>

<task>
[Write your specific instruction here. Use a strong action verb to start.
Be explicit about what "done" looks like.
Example: "Analyse the quarterly revenue data in <context> and identify the top 3 trends that explain the 12% decline in Q3."]
</task>

<format>
[Define the exact output structure you expect.
Example:
- Start with a one-sentence executive summary
- Follow with 3 numbered findings, each containing: the trend, the supporting data point, and a recommended action
- Close with a single paragraph summarising the risk if no action is taken
- Total length: 300-400 words]
</format>

<constraints>
[List what the model must NOT do.
Example:
- Do not speculate beyond the data provided in <context>
- Do not use jargon — explain any technical terms in plain English
- Do not exceed 400 words]
</constraints>
```

---

## Template 2: Few-Shot with Quality Control

Provide gold-standard examples that match the complexity of the actual task. The model doesn't interpret vague adjectives — it has concrete demonstrations.

```xml
<role>
You are a customer success specialist who writes empathetic, solution-focused responses to frustrated users.
</role>

<task>
Write a response to the customer complaint in <input>. Match the tone, structure, and length demonstrated in the examples below.
</task>

<examples>

<example_1>
<input>Your software crashed and I lost 3 hours of work. This is unacceptable.</input>
<output>I completely understand your frustration — losing 3 hours of work is genuinely terrible, and I'm sorry this happened to you.

Here's what I'm doing right now to help:
1. I've flagged the crash report from your session to our engineering team for immediate investigation
2. I'm checking whether your work can be recovered from our auto-save logs (I'll have an update within 2 hours)
3. I've added a 30-day extension to your subscription as a small acknowledgement that this shouldn't have happened

You'll hear from me by end of day with the recovery update. If you need anything before then, reply here and I'll prioritise it.</output>
</example_1>

<example_2>
<input>I've been waiting 5 days for a response to my billing query. This is ridiculous.</input>
<output>You're absolutely right — 5 days is far too long, and I apologise for the wait.

I've just reviewed your billing query and here's where we stand:
1. The duplicate charge of £49.99 on 15th March was a processing error on our end
2. I've initiated the refund — it will appear in your account within 3-5 working days
3. I've also flagged your account to ensure this doesn't recur

If the refund hasn't appeared by next Friday, reply to this message and I'll escalate it directly to our finance team. No more waiting.</output>
</example_2>

</examples>

<input>
[Paste the actual customer complaint here]
</input>

<format>
Follow the exact structure shown in the examples:
- Open with empathy acknowledging the specific frustration
- "Here's what I'm doing" section with numbered concrete actions
- Close with a specific next step and timeline
- Total length: 100-150 words
</format>
```

---

## Template 3: Chain-of-Thought Analysis

Force externalized, step-by-step reasoning before conclusions. The `<thinking>` section lets you audit the reasoning independently.

```xml
<role>
You are a senior business strategist analysing competitive market data.
</role>

<context>
[Paste your data, report, or information here]
</context>

<task>
Analyse the data in <context> and recommend whether we should enter the [specific market/segment].

IMPORTANT: Before providing your recommendation, you MUST work through your reasoning step-by-step inside <thinking> tags. Your thinking process must explicitly address:

1. Market size and growth trajectory — what do the numbers actually show?
2. Competitive landscape — who are the incumbents and what are their weaknesses?
3. Our capabilities — based on the context, what advantages and gaps do we have?
4. Risk factors — what are the top 3 things that could go wrong?
5. Financial viability — does the opportunity justify the investment based on the data provided?

Only AFTER completing all 5 reasoning steps should you provide your final recommendation.
</task>

<format>
Structure your response as:

<thinking>
[Your complete step-by-step reasoning here — be thorough, this is where the real analysis happens]
</thinking>

**Recommendation:** [Go / No-Go / Conditional Go]

**Rationale:** [3-4 sentences summarising the key reasoning]

**Key conditions:** [If conditional, list the specific conditions that must be met]

**Primary risk:** [The single biggest risk and how to mitigate it]
</format>
```

---

## Template 4: Meta Prompt Generator

Turn the model into a prompt engineering co-pilot. The critique step forces the model to audit its own work.

```xml
<role>
You are an expert prompt engineer. Your speciality is designing structured prompts that produce consistent, high-quality outputs from large language models.
</role>

<task>
I need a prompt that will [describe your goal in plain language, e.g., "help me write weekly project status updates that my CTO will actually read"].

Design a complete, production-ready prompt for this task. Your prompt must include:

1. A clearly defined role for the AI
2. Explicit context placeholders showing what information the user needs to provide
3. A specific task instruction with measurable completion criteria
4. An output format specification with exact structure
5. At least one few-shot example demonstrating the ideal output
6. Constraints listing what the AI must avoid

After writing the prompt, critique it:
- Identify any ambiguous words that could be interpreted multiple ways
- Flag any missing context that would cause inconsistent outputs
- Suggest one improvement that would make the output more reliable

Then provide the final, improved version.
</task>
```
