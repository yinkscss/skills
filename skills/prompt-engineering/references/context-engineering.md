# Context Engineering Guide

Comprehensive guide to designing and optimizing context for AI agents and language models.

## Table of Contents

1. [Introduction](#introduction)
2. [Core Components](#core-components)
3. [Design Principles](#design-principles)
4. [Implementation Patterns](#implementation-patterns)
5. [Best Practices](#best-practices)
6. [Common Patterns](#common-patterns)

## Introduction

Context engineering is the process of designing and optimizing the instructions and relevant context provided to large language models to enhance their performance on specific tasks. This extends beyond simple prompt engineering by incorporating system prompts, task constraints, tool descriptions, memory management, and error handling patterns.

### Key Differences from Prompt Engineering

- **Scope**: Context engineering considers the entire interaction context, not just individual prompts
- **Persistence**: Manages state across multiple interactions
- **Architecture**: Designs complete agent systems, not just prompts
- **Observability**: Includes monitoring and debugging capabilities
- **Iteration**: Focuses on systematic improvement based on behavior

## Core Components

### System Prompts

Define the agent's behavior, role, and capabilities.

**Purpose:**
- Establish agent identity and role
- Set behavioral boundaries
- Define capabilities and limitations
- Guide decision-making framework

**Structure:**
```
You are [role/identity].
Your capabilities include: [list]
Your constraints are: [list]
Your goal is: [objective]
You should: [behavioral guidelines]
You must not: [prohibited actions]
```

**Example:**
```
You are a research assistant specialized in scientific literature analysis.

Your capabilities include:
- Searching academic databases
- Summarizing research papers
- Identifying key findings
- Comparing research methodologies

Your constraints are:
- Only use peer-reviewed sources
- Cite all sources properly
- Indicate confidence levels
- Acknowledge limitations

Your goal is to provide accurate, well-sourced research summaries.

You should:
- Verify information from multiple sources
- Use technical terminology accurately
- Provide balanced perspectives

You must not:
- Make unsupported claims
- Plagiarize content
- Provide medical or legal advice
```

**Best Practices:**
- Be explicit about role and identity
- Clearly define boundaries
- Specify capabilities precisely
- Include behavioral guidelines
- State constraints clearly

### Task Constraints

Guide decision-making processes with explicit boundaries.

**Purpose:**
- Limit action space
- Prevent undesirable behaviors
- Ensure task completion
- Maintain consistency

**Types of Constraints:**

1. **Scope Constraints**: Define what's in and out of scope
   ```
   Scope: Analyze only Q4 2023 financial data
   Out of scope: Projections, forecasts, other quarters
   ```

2. **Format Constraints**: Specify output format requirements
   ```
   Output format: JSON with fields: summary, key_points, recommendations
   ```

3. **Quality Constraints**: Define quality standards
   ```
   Quality requirements:
   - All claims must be supported by evidence
   - Use professional terminology
   - Maintain objective tone
   ```

4. **Process Constraints**: Define how to approach the task
   ```
   Process:
   1. Gather information
   2. Analyze patterns
   3. Generate insights
   4. Validate conclusions
   ```

**Best Practices:**
- Make constraints explicit and measurable
- Use positive framing when possible
- Provide examples of constraint adherence
- Test constraints for clarity

### Tool Descriptions

Clarify available functions and their proper usage.

**Purpose:**
- Document available tools
- Specify tool parameters
- Define return values
- Guide tool selection

**Structure:**
```
Tool: [tool_name]
Description: [what it does]
Parameters:
  - [param_name] ([type], [required/optional]): [description]
Returns: [return value description]
Example: [usage example]
When to use: [guidance on when to use this tool]
```

**Example:**
```
Tool: search_database
Description: Searches the research database for papers matching criteria
Parameters:
  - query (string, required): Search terms
  - year_min (integer, optional): Minimum publication year
  - year_max (integer, optional): Maximum publication year
  - limit (integer, optional): Maximum results (default: 10)
Returns: List of paper objects with title, authors, abstract, year
Example: search_database(query="machine learning", year_min=2020, limit=5)
When to use: When you need to find relevant research papers
```

**Best Practices:**
- Document all parameters clearly
- Specify types and constraints
- Provide usage examples
- Explain when to use each tool
- Document error conditions

### Memory Management

Track state across multiple interaction steps.

**Purpose:**
- Maintain conversation context
- Remember previous decisions
- Track task progress
- Store intermediate results

**Memory Types:**

1. **Short-term Memory**: Current conversation context
   - Recent messages
   - Current task state
   - Immediate context

2. **Long-term Memory**: Persistent information
   - User preferences
   - Past interactions
   - Learned patterns

3. **Working Memory**: Active task information
   - Current subtask
   - Intermediate results
   - Temporary state

**Implementation Patterns:**

**Pattern 1: Explicit State Tracking**
```
Current state:
- Task: Research analysis
- Step: 3 of 5 (Analyzing results)
- Completed: Data collection, Initial analysis
- Next: Generate insights
```

**Pattern 2: Context Summarization**
```
Summary of conversation so far:
- User requested analysis of Q4 sales data
- Retrieved data from database
- Identified 3 key trends
- Currently generating recommendations
```

**Pattern 3: Memory Updates**
```
Memory update:
- User preference: Prefer concise summaries
- Task context: Analyzing financial reports
- Previous finding: Revenue increased 15%
```

**Best Practices:**
- Update memory explicitly
- Summarize when context gets long
- Clear memory when task changes
- Track important decisions
- Maintain relevant context only

### Error Handling Patterns

Define how to handle failures and edge cases.

**Purpose:**
- Graceful failure handling
- Recovery strategies
- User communication
- Debugging support

**Error Types:**

1. **Tool Errors**: Tool execution failures
   ```
   If tool fails:
   1. Log error details
   2. Try alternative tool if available
   3. Inform user of limitation
   4. Suggest manual alternative
   ```

2. **Validation Errors**: Output validation failures
   ```
   If output invalid:
   1. Identify specific validation failure
   2. Regenerate with corrected constraints
   3. If still fails, request clarification
   ```

3. **Context Errors**: Context-related issues
   ```
   If context insufficient:
   1. Request missing information
   2. Use default values if appropriate
   3. Proceed with available context
   ```

**Error Handling Structure:**
```
Error handling:
- Tool failures: Retry once, then use alternative
- Validation failures: Regenerate with feedback
- Timeout errors: Extend timeout or simplify task
- Rate limits: Implement backoff strategy
```

**Best Practices:**
- Define error handling for each error type
- Provide user-friendly error messages
- Log errors for debugging
- Implement recovery strategies
- Test error scenarios

## Design Principles

### 1. Eliminate Ambiguity

Every instruction must have one clear interpretation.

**Techniques:**
- Use specific, measurable terms
- Provide examples
- Define all terms
- Avoid pronouns without clear referents
- Specify exact requirements

**Example:**
```
Ambiguous: Make it better
Clear: Increase accuracy by at least 5% while maintaining response time under 100ms

Ambiguous: Use appropriate format
Clear: Output JSON with fields: name (string), age (integer), email (string)
```

### 2. Make Expectations Explicit

State all expectations clearly.

**Areas to Cover:**
- Output format
- Quality standards
- Completion criteria
- Error handling
- Performance requirements

**Example:**
```
Expectations:
- Output: Markdown document with sections: Summary, Analysis, Recommendations
- Quality: All claims supported by at least 2 sources
- Completion: Task complete when all sections written and sources cited
- Errors: If source unavailable, note limitation and continue
- Performance: Complete within 5 minutes
```

### 3. Implement Observability

Enable monitoring and debugging of agent behavior.

**Observability Components:**

1. **Decision Logging**: Log all decisions and reasoning
   ```
   Decision log:
   - Chose tool X because Y
   - Retrieved Z documents
   - Selected approach A over B because C
   ```

2. **State Tracking**: Monitor current state
   ```
   State: Analyzing document
   Progress: 60% complete
   Current step: Extracting key points
   ```

3. **Error Tracking**: Log all errors
   ```
   Error log:
   - Tool X failed: Reason Y
   - Retried with parameters Z
   - Success on retry
   ```

**Best Practices:**
- Log key decisions
- Track progress
- Monitor errors
- Record reasoning
- Enable debugging

### 4. Iterate Based on Behavior

Systematically improve based on observed behavior.

**Iteration Process:**
1. Observe agent behavior
2. Identify issues or improvements
3. Update context/instructions
4. Test changes
5. Measure improvement

**Example:**
```
Observation: Agent skips validation step
Issue: Instructions unclear about validation requirement
Fix: Add explicit validation step with example
Test: Verify validation now occurs
Result: Validation rate increased from 60% to 95%
```

**Best Practices:**
- Start with minimal context
- Add constraints as issues arise
- Test each change
- Measure improvements
- Document what works

### 5. Balance Flexibility with Constraints

Provide enough structure without over-constraining.

**Balance Guidelines:**
- Constrain critical behaviors
- Allow flexibility in non-critical areas
- Provide guidance, not rigid rules
- Enable adaptation when appropriate

**Example:**
```
Flexible: Use appropriate analysis method
Constrained: Use statistical analysis (t-test, ANOVA, or regression)
Balanced: Use statistical analysis appropriate for data type (t-test for 2 groups, ANOVA for 3+ groups, regression for continuous predictors)
```

## Implementation Patterns

### Pattern 1: Layered Context

Structure context in layers from general to specific.

```
Layer 1: System prompt (role, capabilities)
Layer 2: Task description (what to do)
Layer 3: Constraints (how to do it)
Layer 4: Examples (demonstrations)
Layer 5: Current state (where we are)
```

### Pattern 2: Progressive Disclosure

Reveal information as needed.

```
Initial: High-level task description
Step 1: Detailed instructions for step 1
Step 2: Detailed instructions for step 2
...
```

### Pattern 3: Context Templates

Use templates for consistent context structure.

```
Template:
- Role definition
- Task description
- Available tools
- Constraints
- Examples
- Current state
```

### Pattern 4: State Machines

Model agent behavior as state machine.

```
States: Idle → Gathering → Processing → Validating → Complete
Transitions: Define when to move between states
Actions: Define what to do in each state
```

## Best Practices

### Context Design

1. **Start Simple**: Begin with minimal context, add as needed
2. **Be Explicit**: State everything clearly, assume nothing
3. **Provide Examples**: Show desired behavior with examples
4. **Define Boundaries**: Clearly state what's in and out of scope
5. **Specify Format**: Define exact output format requirements

### Testing and Validation

1. **Test Edge Cases**: Verify behavior in unusual situations
2. **Validate Outputs**: Check that outputs meet requirements
3. **Monitor Behavior**: Track agent decisions and actions
4. **Iterate Systematically**: Make changes based on observations
5. **Document Patterns**: Record what works and what doesn't

### Maintenance

1. **Review Regularly**: Periodically review and update context
2. **Track Issues**: Log problems and resolutions
3. **Update Examples**: Keep examples current and relevant
4. **Refine Constraints**: Adjust constraints based on behavior
5. **Measure Performance**: Track metrics to assess improvements

## Common Patterns

### Research Agent Pattern

```
System: Research assistant
Tools: Search, retrieve, summarize
Constraints: Cite sources, indicate confidence
Memory: Track research progress, store findings
Error handling: If source unavailable, note and continue
```

### Analysis Agent Pattern

```
System: Data analyst
Tools: Query data, compute statistics, visualize
Constraints: Use statistical methods, validate assumptions
Memory: Store intermediate results, track analysis steps
Error handling: If data insufficient, request more or note limitations
```

### Writing Agent Pattern

```
System: Writing assistant
Tools: Generate, edit, format
Constraints: Follow style guide, maintain tone
Memory: Track document structure, remember preferences
Error handling: If unclear, ask for clarification
```

## Anti-Patterns

**Don't:**
- Over-constrain without reason
- Assume implicit knowledge
- Skip error handling
- Ignore observability
- Set and forget (no iteration)

**Do:**
- Start simple and add complexity
- Make everything explicit
- Handle errors gracefully
- Monitor behavior
- Iterate based on observations
