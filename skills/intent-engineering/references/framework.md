# Intent Engineering Framework Reference

## Part 1: The Objective

### Definition
The objective defines the problem being solved and why it matters. It is aspirational and qualitative. It guides judgment when trade-offs arise.

### What a good objective does
- **Problem-focused:** What's broken or missing?
- **Explains why it matters:** Business value, user impact, strategic importance
- **Guides trade-offs:** When the agent faces ambiguity, the objective helps it choose

### Examples
- **Weak:** "Handle customer support tickets"
- **Strong:** "Help customers resolve issues quickly so they can get back to work, without creating more frustration than they started with."

When you explain the why, the agent can reason about edge cases and make better autonomous decisions. A 2024 paper (arXiv:2401.04729) demonstrated that supplying strategic context beyond raw task specifications significantly improves AI autonomy.

---

## Part 2: Desired Outcomes (Completion Criteria)

### Definition
Desired outcomes are observable states that indicate the objective has been achieved. They are **not** activities the agent performs.

### Rules for good outcomes
- Observable state changes (not activities)
- From user/stakeholder perspective (not the agent's)
- Measurable or verifiable (without relying on agent self-report)
- Leading, not lagging (observable during or shortly after, not months later)

### Example
```yaml
Objective: Help customers resolve Tier-1 issues without frustration
Desired Outcomes:
  - Customer confirms their issue is resolved
  - No follow-up ticket on same topic within 24 hours
  - Customer rates interaction as helpful
```

Two to four outcomes is usually right. More than that and you're either micromanaging or unclear on what matters.

---

## Part 3: Health Metrics (Non-Regression Guardrails)

### Definition
Health metrics define what **must not degrade** while optimising for outcomes.

### The Goodhart Problem
"When a measure becomes a target, it ceases to be a good measure."

Without health metrics:
- "Resolve issues faster" → Agent rushes, quality drops
- "Increase throughput" → Agent takes shortcuts
- "Reduce escalations" → Agent handles things it shouldn't

### How health metrics inform trade-offs
Health metrics primarily inform the prompt layer. They guide how the agent thinks.

```yaml
Health Metrics:
  - CSAT must stay above 4.2 — if trending down, be more conservative
  - Repeat contact rate must not increase above X — prioritize resolution quality
  - Escalation quality score must stay below Y — don't under-escalate to hit targets
```

Health metrics steer; guardrails enforce.

---

## Part 4: Strategic Context (Framework Loading)

3–5 sentences explaining **WHY** this agent exists in the broader organisational context. What business strategy does it serve? What happens if it fails?

This is the "tribal knowledge" the agent needs to make intelligent inferences that go beyond the literal instructions.

---

## Part 5: Constraints (Quality Standards)

8–12 hard rules the agent must never violate. 4 categories:

| Category | Examples |
|----------|----------|
| **Data** | What data it can/cannot access or share |
| **Action** | What it can/cannot do (e.g., no refunds over $50) |
| **Communication** | Tone, language, disclosure rules |
| **Compliance** | Legal, regulatory, or policy requirements |

**Steering constraints** are defined in the prompt layer. **Hard constraints** are enforced in the orchestration layer, not prompts.

---

## Part 6: Decision Autonomy (Delegation Protocol)

Explicit decision matrix:

| Level | Description | Examples |
|-------|-------------|----------|
| **AUTONOMOUS** | No approval needed | Password resets, FAQ answers |
| **NOTIFY** | Act, then inform human | Applying standard discount |
| **APPROVE** | Request human approval first | Refunds over threshold |
| **FORBIDDEN** | Never attempt, always escalate | Account deletion, legal matters |

---

## Part 7: Stop Rules (Kill Switches / Circuit Breakers)

5–7 deterministic conditions where the agent must immediately halt:

- **Confidence threshold:** If confidence drops below 70%, escalate
- **Error cascade:** If 3 consecutive actions fail, halt and alert
- **Boundary violation:** If any constraint is at risk of violation, halt immediately
- **Time/cost limit:** If the agent has spent more than X minutes or $Y, escalate
- **Anomaly detection:** Unusual patterns in user input or system behavior

---

## Trade-Off Hierarchies

When objectives conflict, explicitly encode the priority order. Without this, the AI defaults to whichever is easiest to optimise.

### Components
1. **Priority ranking** — Order objectives from highest to lowest with reasoning
2. **Conflict resolution rules** — Specific rule for each pair (e.g., "When SPEED conflicts with ACCURACY: Always choose accuracy")
3. **Override conditions** — Scenarios where the normal order flips (e.g., "During outage affecting 100+ users, SPEED becomes top priority")
4. **Measurement** — How the agent measures whether it's meeting each standard

---

## Audit Trail Design

When an AI agent makes a mistake, you need the full chain of reasoning:

### Event Taxonomy
Define every event type: decision made, tool invoked, context retrieved, escalation triggered, error encountered. Each event type has required fields.

### Payload Schema
```json
{
  "event_id": "unique-uuid",
  "timestamp": "ISO-8601",
  "agent_identity": "cryptographic-key-bound",
  "event_type": "decision_made",
  "input_data_hash": "sha256-of-input",
  "reasoning_trace": ["intent_rule_1", "intent_rule_3"],
  "action_taken": "applied_discount",
  "outcome": "customer_satisfied",
  "previous_hash": "sha256-of-previous-entry"
}
```

### Storage
Append-only, hash-chained database (e.g., WORM store). Tamper-evident. Clear retention policies and access controls.

---

## DoView Outcomes Modeling

Strategic intent cannot remain implicit. Extract the mental model, represent it visually, and verify that all parties share the same model.

A DoView diagram maps all interconnected outcomes. By comparing the DoView an agent is working from against the ideal business DoView, engineers can spot missing intent before deployment.
