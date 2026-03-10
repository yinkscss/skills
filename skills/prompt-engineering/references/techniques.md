# Prompting Techniques Reference

Comprehensive guide to all prompting techniques with detailed explanations, use cases, and implementation patterns.

## Table of Contents

1. [Basic Techniques](#basic-techniques)
2. [Reasoning Techniques](#reasoning-techniques)
3. [Retrieval and Augmentation](#retrieval-and-augmentation)
4. [Agent Techniques](#agent-techniques)
5. [Specialized Techniques](#specialized-techniques)

## Basic Techniques

### Zero-Shot Prompting

**Definition:** Instructing the model to perform a task without providing examples, relying solely on pre-training knowledge.

**When to Use:**
- Simple, well-defined tasks
- Tasks where model's training likely covers the pattern
- Quick prototyping
- General knowledge queries

**Structure:**
```
[Clear task description]
[Explicit instruction with action verb]
[Output format specification]
[Any constraints or requirements]
```

**Example:**
```
Task: Classify the sentiment of the following text.

Text: "This product exceeded my expectations!"

Instruction: Classify the sentiment as positive, negative, or neutral.

Output format: Return only the classification label.
```

**Best Practices:**
- Use clear, unambiguous language
- Specify exact output format
- Include all necessary context
- Use imperative verbs

**Limitations:**
- May not work for novel or highly specific tasks
- Performance depends on training data coverage
- May require iteration for optimal results

### Few-Shot Prompting

**Definition:** Providing a few examples to guide the model's response pattern and establish the desired format.

**When to Use:**
- Tasks requiring specific formatting
- Style transfer tasks
- Pattern matching
- When zero-shot performance is insufficient

**Structure:**
```
[Task description]
[Example 1: Input → Output]
[Example 2: Input → Output]
[Example 3: Input → Output]
[Target input to process]
```

**Example:**
```
Task: Convert dates from US format to ISO format.

Example 1:
Input: 12/25/2023
Output: 2023-12-25

Example 2:
Input: 01/05/2024
Output: 2024-01-05

Example 3:
Input: 07/04/2023
Output: 2023-07-04

Now convert: 03/15/2024
```

**Best Practices:**
- Use 2-5 examples typically (more can confuse, fewer may be insufficient)
- Ensure examples are diverse but consistent in format
- Examples should represent full range of desired outputs
- Maintain consistent formatting across all examples
- Order examples logically (simple to complex, or by frequency)

**Common Mistakes:**
- Too many examples (>10) causing confusion
- Inconsistent formatting between examples
- Examples that don't represent the task well
- Mixing different output styles

## Reasoning Techniques

### Chain-of-Thought (CoT) Prompting ⭐ **FUNDAMENTAL TECHNIQUE**

Chain-of-Thought (CoT) prompting is one of the most important and widely-used techniques in prompt engineering. It has revolutionized how we approach complex reasoning tasks with language models.

**Definition:** Encouraging the model to generate intermediate reasoning steps before producing the final answer, enabling it to break down complex problems into manageable parts.

**When to Use:**
- Complex problem-solving
- Arithmetic reasoning
- Multi-step logical tasks
- Tasks requiring explanation
- When transparency is needed
- Any task where reasoning improves accuracy

**Why CoT is Essential:**
- Dramatically improves performance on complex reasoning tasks
- Makes model reasoning transparent and debuggable
- Enables solving problems that seem impossible without step-by-step thinking
- Foundation for many advanced techniques (Self-Consistency, ToT, etc.)
- Works across diverse domains (math, logic, planning, analysis)

**Zero-Shot CoT Structure:**
```
[Problem statement]
Let's think step by step:
[Model generates reasoning]
[Final answer]
```

**Few-Shot CoT Structure:**
```
[Problem 1]
Let's think step by step:
[Reasoning steps]
[Answer 1]

[Problem 2]
Let's think step by step:
[Reasoning steps]
[Answer 2]

[Target problem]
Let's think step by step:
```

**Example:**
```
Problem: A store has 15 apples. They sell 6 apples in the morning and 4 apples in the afternoon. How many apples are left?

Let's think step by step:
1. Start with 15 apples
2. Subtract 6 sold in morning: 15 - 6 = 9
3. Subtract 4 sold in afternoon: 9 - 4 = 5
4. Final answer: 5 apples remain
```

**Variations:**
- **Zero-shot CoT**: Add trigger phrases like "Let's think step by step" or "Let's work through this"
- **Few-shot CoT**: Provide examples showing step-by-step reasoning
- **Manual CoT**: Provide explicit reasoning steps in the prompt
- **Automatic CoT**: Let model generate reasoning automatically

**Important Considerations:**
- Explicit CoT may negatively impact instruction-following in some models
- Test and verify behavior for your specific model
- CoT increases token usage
- May slow down response generation

**Best Practices:**
- Use clear trigger phrases
- Provide examples if few-shot CoT
- Allow sufficient token budget for reasoning
- Verify reasoning quality, not just final answer

### Self-Consistency

**Definition:** Sampling multiple reasoning paths and selecting the most consistent answer.

**When to Use:**
- Tasks with multiple valid reasoning paths
- Arithmetic problems
- Commonsense reasoning
- When reliability is critical
- High-stakes decisions

**Implementation Process:**
1. Generate multiple reasoning paths (typically 3-5)
2. Extract final answers from each path
3. Select answer appearing most frequently
4. Optionally use confidence scores

**Example:**
```
Problem: Calculate 25 × 17

Path 1: 25 × 10 = 250, 25 × 7 = 175, 250 + 175 = 425
Path 2: 20 × 17 = 340, 5 × 17 = 85, 340 + 85 = 425
Path 3: 25 × 20 = 500, 25 × 3 = 75, 500 - 75 = 425

Most consistent answer: 425
```

**Best Practices:**
- Generate 3-5 paths typically
- Use diverse reasoning approaches when possible
- Consider answer frequency and confidence
- May combine with CoT for better reasoning

**Limitations:**
- Increases computational cost
- Slower than single-path generation
- May not help if all paths are wrong
- Requires multiple API calls

### Tree of Thoughts (ToT)

**Definition:** Maintaining a tree of thoughts, allowing systematic exploration of multiple reasoning paths.

**When to Use:**
- Strategic problem-solving
- Tasks requiring exploration of alternatives
- Complex planning
- Game playing
- Creative problem-solving

**Structure:**
1. Generate multiple thought candidates at each step
2. Evaluate each thought (quality, feasibility, progress)
3. Expand promising thoughts further
4. Backtrack when paths become unpromising
5. Select best path based on evaluation

**Example:**
```
Problem: Plan a route visiting 5 cities with distance constraints

Step 1: Generate initial city choices
  - Thought A: Start with City 1
  - Thought B: Start with City 2
  - Thought C: Start with City 3

Step 2: Evaluate each thought
  - Thought A: Score 7/10
  - Thought B: Score 9/10
  - Thought C: Score 5/10

Step 3: Expand Thought B
  - Thought B1: Next go to City 3
  - Thought B2: Next go to City 4
  - Evaluate and continue...
```

**Best Practices:**
- Define clear evaluation criteria
- Limit tree depth to manage complexity
- Use pruning to eliminate unpromising paths
- Balance exploration vs exploitation

**Implementation Considerations:**
- Requires multiple model calls
- Needs evaluation mechanism
- Can be computationally expensive
- May need custom implementation

### Program-Aided Language Models (PAL)

**Definition:** Generate programs as intermediate reasoning steps, offloading solution steps to a programmatic runtime.

**When to Use:**
- Mathematical problems
- Algorithmic tasks
- Data manipulation
- Computational problems
- When precise calculation is needed

**Structure:**
```
[Problem statement]
[Generate Python code to solve]
[Execute code]
[Extract answer from code output]
```

**Example:**
```
Problem: Calculate the sum of all even numbers from 1 to 100.

Code:
```python
total = 0
for i in range(1, 101):
    if i % 2 == 0:
        total += i
print(total)
```

Execute: 2550
Answer: 2550
```

**Best Practices:**
- Use appropriate programming language
- Validate code before execution
- Handle errors gracefully
- Test code on sample inputs
- Extract answers clearly from output

**Limitations:**
- Requires code execution environment
- Code generation may have bugs
- Not suitable for all problem types
- Security concerns with code execution

## Retrieval and Augmentation

### Retrieval Augmented Generation (RAG)

**Definition:** Combine information retrieval with text generation to enhance factual consistency and reduce hallucinations.

**When to Use:**
- Knowledge-intensive tasks
- Domain-specific queries
- Reducing hallucinations
- Up-to-date information needs
- Factual accuracy critical

**Components:**
1. **Retrieval System**: Vector database, keyword search, or hybrid
2. **Context Integration**: Inject retrieved documents into prompt
3. **Generation**: Model produces answer using retrieved context

**Structure:**
```
[User query]
[Retrieve relevant documents]
[Construct prompt with retrieved context]
[Generate answer using context]
```

**Example:**
```
Query: What are the side effects of medication X?

Retrieved documents:
- Document 1: Clinical trial data on medication X
- Document 2: FDA approval documentation
- Document 3: Patient information leaflet

Prompt:
Based on the following documents, what are the side effects of medication X?

[Document 1 content]
[Document 2 content]
[Document 3 content]

Answer: [Generated from context]
```

**Best Practices:**
- Retrieve 3-5 relevant documents typically
- Include source citations in output
- Filter retrieved content for relevance
- Handle cases where no relevant documents found
- Use appropriate retrieval method (vector, keyword, hybrid)
- Chunk documents appropriately for retrieval

**Retrieval Methods:**
- **Vector Search**: Semantic similarity using embeddings
- **Keyword Search**: Traditional text matching
- **Hybrid**: Combine vector and keyword search
- **Re-ranking**: Improve retrieval quality

**Implementation Considerations:**
- Embedding model selection
- Chunk size optimization
- Retrieval top-k selection
- Context window management
- Source attribution

### GraphPrompts

**Definition:** Framework for graph-based prompting to improve performance on structured data tasks.

**When to Use:**
- Tasks involving relationships
- Network analysis
- Hierarchical data
- Knowledge graphs
- Structured information extraction

**Structure:**
```
[Graph representation]
[Query about graph]
[Generate answer using graph structure]
```

**Example:**
```
Graph:
- Node A connects to Node B and Node C
- Node B connects to Node D
- Node C connects to Node D and Node E

Query: What is the shortest path from A to E?

Answer: A → C → E
```

**Best Practices:**
- Represent graph structure clearly
- Use appropriate graph format
- Leverage graph properties (paths, cycles, etc.)
- Consider graph algorithms when relevant

## Agent Techniques

### Automatic Reasoning and Tool-use (ART)

**Definition:** Combine chain-of-thought prompting with tool use to address complex tasks.

**When to Use:**
- Tasks requiring external tools
- API calls needed
- Data retrieval from external sources
- Complex multi-step operations
- When tools can enhance capabilities

**Structure:**
1. Decompose task into subtasks
2. For each subtask, determine if tool use needed
3. Generate reasoning about tool selection
4. Execute tool with appropriate parameters
5. Integrate tool output into reasoning
6. Continue until task complete

**Example:**
```
Task: Get the current weather in Paris and suggest appropriate clothing.

Reasoning:
1. Need to get weather data → Use weather API tool
2. Tool call: get_weather(location="Paris")
3. Tool output: Temperature 15°C, Rainy
4. Reasoning: Cold and rainy → Need warm, waterproof clothing
5. Generate clothing suggestions
```

**Best Practices:**
- Clearly define available tools
- Specify tool parameters precisely
- Handle tool errors gracefully
- Validate tool outputs
- Integrate tool results into reasoning flow

**Tool Description Format:**
```
Tool: get_weather
Description: Retrieves current weather for a location
Parameters:
  - location (string, required): City name
Returns:
  - temperature (float): Temperature in Celsius
  - condition (string): Weather condition
  - humidity (float): Humidity percentage
```

### Prompt Chaining

**Definition:** Break complex tasks into subtasks, using output of one prompt as input for another.

**When to Use:**
- Multi-step processes
- Document analysis pipelines
- Complex workflows
- When intermediate outputs needed
- Sequential dependencies

**Structure:**
```
Prompt 1: [Initial task] → Output 1
Prompt 2: [Use Output 1] → Output 2
Prompt 3: [Use Output 2] → Final Output
```

**Example:**
```
Chain 1: Extract key points from document
  Input: Long document
  Output: List of key points

Chain 2: Summarize key points
  Input: List of key points from Chain 1
  Output: Concise summary

Chain 3: Generate recommendations
  Input: Summary from Chain 2
  Output: Actionable recommendations
```

**Best Practices:**
- Define clear interfaces between prompts
- Validate intermediate outputs
- Handle errors at each step
- Maintain context across chain
- Document data flow between steps

**Error Handling:**
- Validate each step's output
- Provide fallback mechanisms
- Log errors for debugging
- Allow chain to continue or abort based on error severity

### Reflexion

**Definition:** Introduce self-evaluation and reflection, enabling agents to learn from mistakes.

**When to Use:**
- Sequential decision-making
- Reasoning tasks
- Programming tasks
- Iterative improvement needed
- When learning from errors is valuable

**Structure:**
1. Attempt task
2. Evaluate output (self-evaluation or external)
3. Reflect on what went wrong
4. Generate improved approach
5. Retry with improvements

**Example:**
```
Attempt 1:
Task: Write a function to sort a list
Code: [Generated code with bug]
Evaluation: Fails on empty list
Reflection: Need to handle edge case of empty input

Attempt 2:
Task: Write a function to sort a list (handle empty list)
Code: [Improved code]
Evaluation: Passes all tests
```

**Best Practices:**
- Define clear evaluation criteria
- Provide specific feedback
- Focus reflection on actionable improvements
- Limit retry attempts to avoid loops
- Track what was learned

**Limitations:**
- Relies on model's self-evaluation capabilities
- May struggle with complex tasks
- Long-term memory constraints
- Code generation challenges with test-driven development
- May get stuck in improvement loops

### Active-Prompt

**Definition:** Adapt language models to specific tasks by selecting most effective examples for chain-of-thought reasoning.

**When to Use:**
- Task-specific optimization
- Improving CoT performance on new domains
- When example selection matters
- Domain adaptation

**Process:**
1. Start with task and candidate examples
2. Generate CoT reasoning for each example
3. Evaluate reasoning quality
4. Select best examples based on evaluation
5. Use selected examples for few-shot CoT

**Example:**
```
Candidate examples: 10 math problems
Generate CoT for each → Evaluate reasoning quality
Select top 3 examples with best reasoning
Use selected 3 for few-shot CoT on new problems
```

**Best Practices:**
- Use diverse candidate examples
- Define clear evaluation criteria
- Balance example quality and diversity
- Test selected examples on validation set

### Directional Stimulus Prompting

**Definition:** Guide model generation using a policy model to produce stimuli or hints.

**When to Use:**
- Tasks requiring fine-grained control
- Style transfer
- Controlled generation
- When hints improve performance

**Structure:**
```
[Task description]
[Policy model generates stimulus/hint]
[Main model uses stimulus to generate output]
```

**Example:**
```
Task: Write a poem about nature
Stimulus: Use imagery of seasons, include metaphors
Generated poem: [Uses seasonal imagery and metaphors]
```

## Additional Advanced Techniques

### Generated Knowledge Prompting

**Definition:** Prompt the model to generate relevant background knowledge before answering a question, enabling more accurate and contextually informed responses.

**When to Use:**
- Questions requiring background knowledge
- Complex topics needing context
- When factual accuracy is critical
- Domain-specific queries

**Structure:**
```
[Question]
First, generate relevant knowledge about this topic:
[Model generates knowledge]
Now, using this knowledge, answer the question:
[Model provides answer]
```

**Example:**
```
Question: What is the objective of golf?

Step 1 - Generate Knowledge:
Golf is a sport where players use clubs to hit balls into holes on a course. 
The objective is to complete the course with the fewest strokes possible. 
Each hole has a par score representing expected strokes.

Step 2 - Answer:
The objective of golf is to complete the course using the fewest number of strokes.
```

**Best Practices:**
- Generate knowledge relevant to the question
- Use generated knowledge to inform answer
- Verify knowledge accuracy when possible
- Combine with RAG for factual verification

### Least-to-Most Prompting

**Definition:** Break down complex tasks into simpler sub-tasks, solving each sequentially to build up to the original complex problem.

**When to Use:**
- Complex multi-step problems
- Tasks with dependencies
- When breaking down helps understanding
- Problems that can be decomposed

**Structure:**
```
[Complex problem]
Step 1: [Simplest sub-problem] → Solution 1
Step 2: [Use Solution 1 for next sub-problem] → Solution 2
Step 3: [Use Solutions 1 & 2 for next] → Solution 3
...
Final: [Combine all solutions] → Complete answer
```

**Example:**
```
Problem: Calculate total cost including tax and tip for a $50 meal with 8% tax and 15% tip.

Step 1: Calculate tax
  $50 × 0.08 = $4.00

Step 2: Calculate subtotal with tax
  $50 + $4.00 = $54.00

Step 3: Calculate tip on original amount
  $50 × 0.15 = $7.50

Step 4: Calculate total
  $54.00 + $7.50 = $61.50
```

**Best Practices:**
- Start with simplest sub-problem
- Build complexity gradually
- Use previous solutions in next steps
- Verify each step before proceeding
- Combine solutions systematically

### Self-Refine

**Definition:** Iteratively refine outputs using self-generated feedback, enhancing quality and accuracy over multiple iterations.

**When to Use:**
- Tasks requiring high quality
- When iterative improvement is possible
- Quality-critical outputs
- When initial output needs refinement

**Structure:**
```
1. Generate initial output
2. Self-evaluate: Identify issues or improvements
3. Generate refined output based on feedback
4. Repeat until satisfactory or max iterations
```

**Example:**
```
Initial Output: "The data shows an increase."
Self-Evaluation: "Too vague, lacks specifics, no numbers"
Refined: "The data shows a 15% increase from Q1 to Q2, rising from 100 to 115 units."
Self-Evaluation: "Better, but could include context"
Final: "The data shows a 15% increase from Q1 to Q2, rising from 100 to 115 units, 
        which represents the highest quarterly growth in the past year."
```

**Best Practices:**
- Define clear evaluation criteria
- Limit iterations to avoid loops
- Focus on specific improvements
- Track what changed in each iteration
- Set quality thresholds

**Limitations:**
- May not converge if criteria unclear
- Can be computationally expensive
- Requires good self-evaluation capability
- May over-optimize for certain aspects

### Maieutic Prompting

**Definition:** Engage the model in a Socratic dialogue, prompting it to question and elaborate on its responses to enhance depth and insight.

**When to Use:**
- Deep understanding needed
- Exploring assumptions
- Philosophical or complex reasoning tasks
- When surface-level answers insufficient

**Structure:**
```
[Initial question]
[Model provides answer]
Question: What assumptions underlie this answer?
[Model elaborates]
Question: What are the implications?
[Model explores further]
[Final synthesized understanding]
```

**Example:**
```
Q: Should we implement this policy?
A: Yes, it will improve efficiency.

Q: What assumptions are you making?
A: I assume the policy will be implemented correctly, 
   stakeholders will cooperate, and resources are available.

Q: What could go wrong?
A: Implementation might face resistance, resources might be insufficient, 
   or the policy might have unintended consequences.

Q: How do we address these risks?
A: We need stakeholder buy-in, adequate resources, and a pilot program 
   to test before full implementation.
```

**Best Practices:**
- Ask probing questions
- Challenge assumptions
- Explore implications
- Synthesize insights
- Guide dialogue toward deeper understanding

### Meta Prompting

**Definition:** Emphasize structural and syntactical aspects of tasks rather than specific content, creating abstract, structured interactions.

**When to Use:**
- Tasks requiring structured responses
- When format matters more than content
- Pattern-based problems
- When abstract patterns are more important than specifics

**Structure:**
```
[Abstract problem structure]
[Syntax template for solution]
[Category definitions]
[Generate solution following structure]
```

**Example:**
```
Problem Structure:
- Input: [category A] and [category B]
- Process: [operation] using [method]
- Output: [category C] with [properties]

Syntax Template:
Given [A] and [B], apply [operation] using [method] to produce [C] with [properties].

Specific Problem:
Given "customer data" and "sales data", apply "merge" using "join on customer_id" 
to produce "combined dataset" with "all customer and sales fields".
```

**Key Characteristics:**
- **Structure-oriented**: Focus on format and pattern over content
- **Syntax-focused**: Use syntax as template for responses
- **Abstract examples**: Illustrate structure without specific details
- **Versatile**: Applicable across domains
- **Categorical approach**: Emphasize categorization and logical arrangement

**Advantages:**
- Token efficient (abstract vs concrete examples)
- Fair comparison by minimizing specific examples
- Effective in zero-shot scenarios
- Generalizable across domains

**Best Practices:**
- Define clear structural templates
- Use abstract placeholders
- Focus on pattern recognition
- Maintain consistent syntax
- Test across different domains

### Automatic Prompt Engineer (APE)

**Definition:** Framework for automatic instruction generation and selection, treating instruction generation as natural language synthesis through black-box optimization.

**When to Use:**
- Optimizing prompts automatically
- Discovering effective zero-shot prompts
- When manual optimization is difficult
- Finding task-specific optimal prompts

**Process:**
1. **Instruction Generation**: Inference model generates instruction candidates based on output demonstrations
2. **Instruction Execution**: Target model executes these instructions
3. **Instruction Selection**: Most appropriate instruction selected based on evaluation scores

**Example:**
```
Demonstrations:
Input: "2 + 2" → Output: "4"
Input: "5 × 3" → Output: "15"

Generated Instructions:
1. "Solve the math problem"
2. "Calculate the answer step by step"
3. "Let's work this out in a step by step way to be sure we have the right answer"

Evaluation:
Instruction 3 scores highest on test problems
Selected: "Let's work this out in a step by step way to be sure we have the right answer"
```

**Benefits:**
- Discovers effective prompts automatically
- Can find zero-shot CoT prompts
- Optimizes for specific tasks
- Reduces manual prompt engineering effort
- May discover non-obvious effective prompts

**Best Practices:**
- Provide diverse output demonstrations
- Use appropriate evaluation metrics
- Generate sufficient candidate instructions
- Test on validation set
- Iterate on generation process

**Limitations:**
- Requires output demonstrations
- Computational cost of generation and evaluation
- May not generalize across tasks
- Quality depends on generation model

## Specialized Techniques

### Multimodal Chain-of-Thought

**Definition:** Incorporate both text and visual information in a two-stage framework.

**When to Use:**
- Tasks involving images
- Diagrams and charts
- Visual reasoning
- When both text and visual context needed

**Structure:**
1. Extract visual information
2. Generate text description of visual elements
3. Apply CoT reasoning to combined text and visual information
4. Produce final answer

**Example:**
```
Input: Image of a bar chart showing sales data
Step 1: Extract visual: "Bar chart with 4 bars, values 100, 150, 120, 180"
Step 2: Describe: "Sales increased from Q1 to Q2, decreased in Q3, increased in Q4"
Step 3: Reasoning: "Overall trend is positive, Q4 is highest"
Step 4: Answer: "Sales show overall growth with Q4 peak"
```

**Best Practices:**
- Clearly describe visual elements
- Integrate visual and text information
- Use appropriate visual description detail level
- Consider visual reasoning capabilities of model

## Technique Selection Guide

| Technique | Complexity | Use Case | Token Cost | Reliability |
|-----------|-----------|----------|------------|-------------|
| Zero-shot | Low | Simple tasks | Low | Medium |
| Few-shot | Low | Format-specific | Low | Medium-High |
| CoT | Medium | Reasoning tasks | Medium | High |
| Self-Consistency | High | Critical decisions | High | Very High |
| ToT | Very High | Strategic planning | Very High | High |
| RAG | Medium | Knowledge tasks | Medium | High |
| ART | High | Tool integration | High | High |
| Prompt Chaining | Medium | Multi-step workflows | Medium | Medium |
| Reflexion | High | Iterative improvement | High | Medium-High |
| Generated Knowledge | Medium | Knowledge-intensive | Medium | High |
| Least-to-Most | Medium | Complex decomposition | Medium | High |
| Self-Refine | High | Quality-critical | High | Medium-High |
| Maieutic | Medium | Deep understanding | Medium | Medium |
| Meta Prompting | Low | Structured tasks | Low | Medium-High |
| APE | Very High | Prompt optimization | Very High | High |

## Combining Techniques

Techniques can be combined for enhanced performance:

- **Few-shot + CoT**: Provide examples with reasoning steps
- **RAG + CoT**: Retrieve context and reason about it
- **CoT + Self-Consistency**: Generate multiple reasoning paths
- **Prompt Chaining + RAG**: Retrieve context at each step
- **ART + Reflexion**: Use tools and learn from mistakes

**Best Practices for Combination:**
- Start with simpler techniques
- Add complexity only when needed
- Test each combination
- Monitor token usage and cost
- Validate improvements
