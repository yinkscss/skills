# Intent Engineering Templates

## Template 1: Outcome-Driven Task Definition

Shift from outputs to outcomes. Format serves the intent, not the other way around.

```xml
<role>
You are a [specific role] operating as part of [team/organisation].
</role>

<intent>
OBJECTIVE: [The business problem this task exists to solve]
Example: "Enable the product team to prioritise the Q3 roadmap by providing a data-backed analysis of feature requests ranked by revenue impact."

SUCCESS CRITERIA — this task is complete when:
- [ ] [Measurable outcome 1, e.g., "The top 10 feature requests are ranked by estimated revenue impact with supporting data"]
- [ ] [Measurable outcome 2, e.g., "Each recommendation includes implementation effort estimate (S/M/L) so the team can assess ROI"]
- [ ] [Measurable outcome 3, e.g., "The analysis is concise enough to be consumed in under 10 minutes"]

AUDIENCE: [Who will consume this output and what decision will they make with it]
Example: "Product VP and 3 senior PMs. They will use this to lock the Q3 roadmap in their Thursday planning session."
</intent>

<context>
[Your data and background information]
</context>

<constraints>
- [What must be avoided]
- [Hard boundaries]
- [Quality standards]
</constraints>

<format>
[Structure specification — format serves the intent, not the other way round]
</format>
```

---

## Template 2: Full 7-Component Intent Schema Generator

Generate a complete, deployable intent configuration from a plain-language agent description. Output as YAML for direct repository commit.

```xml
<role>
You are an intent engineering architect. You design structured, machine-readable intent schemas that govern autonomous AI agent behaviour.
</role>

<task>
I'm deploying an AI agent for the following purpose:

**Agent purpose:** [Describe what the agent will do, e.g., "Autonomously review and respond to customer support tickets for our SaaS platform"]

**Operating environment:** [Where it operates, e.g., "Integrated with Zendesk via API, accessing our knowledge base and customer database"]

**Autonomy level:** [How much independence it has, e.g., "Can resolve Tier 1 tickets independently. Must escalate Tier 2+ to human agents."]

Generate a complete 7-Component Intent Schema:

1. **OBJECTIVE (Unlock Question)**
   Write a singular mission statement (1-2 sentences) that defines the exact business problem this agent exists to solve. Must be specific enough that any ambiguous edge case can be resolved by asking "does this action serve the objective?"

2. **DESIRED OUTCOMES (Completion Criteria)**
   Define 5-7 explicit, measurable conditions that define success. Each must be binary — either met or not met. Include positive and negative criteria.

3. **HEALTH METRICS (Non-Regression Guardrails)**
   Define 4-6 KPIs with: metric name, acceptable range, alert threshold, escalation threshold.

4. **STRATEGIC CONTEXT (Framework Loading)**
   Write 3-5 sentences explaining WHY this agent exists in the broader organisational context.

5. **CONSTRAINTS (Quality Standards)**
   List 8-12 hard rules categorised as: Data, Action, Communication, Compliance.

6. **DECISION AUTONOMY (Delegation Protocol)**
   Create an explicit decision matrix: AUTONOMOUS, NOTIFY, APPROVE, FORBIDDEN.

7. **STOP RULES (Kill Switches / Circuit Breakers)**
   Define 5-7 deterministic halt conditions including: confidence threshold, error cascade, boundary violation, time/cost limit.
</task>

<format>
Output the schema as a structured YAML document that can be directly committed to a repository and consumed by an agent orchestration framework.
</format>
```

---

## Template 3: Trade-Off Matrix

Explicitly encode priority order when objectives conflict.

```xml
<task>
I'm building an AI agent that operates in a domain where the following objectives frequently conflict:

- [Objective A, e.g., "Response speed — resolve issues quickly"]
- [Objective B, e.g., "Customer satisfaction — ensure the customer feels heard and valued"]
- [Objective C, e.g., "Cost efficiency — minimise resource usage per interaction"]
- [Objective D, e.g., "Accuracy — ensure all information provided is correct"]

Design a trade-off hierarchy that explicitly defines:

1. **Priority ranking:** Order from highest to lowest priority. Explain reasoning.

2. **Conflict resolution rules:** For each pair of conflicting objectives, write a specific rule. Example:
   - "When SPEED conflicts with ACCURACY: Always choose accuracy. A slow correct answer is acceptable; a fast wrong answer is not."
   - "When SATISFACTION conflicts with COST: Choose satisfaction when the customer's lifetime value exceeds £500."

3. **Override conditions:** Specific scenarios where the normal priority order flips. Example:
   - "During a system outage affecting more than 100 users, SPEED becomes the top priority regardless of normal hierarchy."

4. **Measurement:** For each objective, define how the agent should measure whether it's meeting the standard (specific metrics, not vague assessments).
</task>

<format>
Output as a structured decision matrix that an agent orchestration system can consume programmatically.
</format>
```

---

## Template 4: Audit Chain Architecture

Make every AI decision traceable.

```xml
<role>
You are a systems architect specialising in AI governance and compliance infrastructure.
</role>

<task>
Design a traceable audit chain for an autonomous AI agent that:

**Agent description:** [What the agent does]
**Risk level:** [Low / Medium / High / Critical]
**Regulatory requirements:** [Any compliance frameworks, e.g., GDPR, SOC 2, FCA guidelines]

Your audit chain design must include:

1. **Event taxonomy:** Define every event type the agent can produce (decision made, tool invoked, context retrieved, escalation triggered, error encountered). For each, specify exact fields to log.

2. **Payload schema:** JSON payload structure for audit log entries including: Unique event ID, Timestamp (ISO 8601), Agent identity (cryptographic key), Event type, Input data hash, Reasoning trace, Action taken, Outcome, Hash of previous log entry.

3. **Storage architecture:** Append-only database type, retention policy, access controls.

4. **Verification mechanism:** How to verify the chain hasn't been tampered with. Include hashing algorithm and verification procedure.

5. **Alert triggers:** 5 conditions that should generate automatic alerts to the human oversight team.
</task>
```
