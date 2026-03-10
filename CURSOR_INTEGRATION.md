# Cursor Integration Guide for Skills

## Understanding Cursor Rules vs Claude Skills

### Cursor Rules
- **Location**: `.cursor/rules/` directory in project root
- **Format**: `.mdc` files (Markdown Context)
- **Purpose**: Project-specific guidance for AI behavior
- **Required Fields**: `description` (mandatory)
- **Optional Fields**: `globs` (file patterns), `alwaysApply` (boolean)

### Claude Skills
- **Location**: `skills/` directory in plugin root
- **Format**: `.skill` files (zip archives) containing `SKILL.md`
- **Purpose**: Extend Claude's capabilities with specialized knowledge
- **Required Fields**: `name`, `description` in YAML frontmatter
- **Integration**: Skills are loaded by Claude, not directly by Cursor rules

## Error: Missing Description in Rule

### Error Message
```
There was an error passing the rule for Cursor because description is required, 
and there was no description in the rule. This rule has no description or file 
pattern, and it may never be used by Cursor.
```

### Cause
A rule file (`.mdc`) exists without a `description` field in its frontmatter.

### Solution
Every rule file must have this structure:

```markdown
---
description: Brief description of what this rule does
globs: ["**/*.md"]  # Optional: file patterns
alwaysApply: false  # Optional: always include this rule
---

# Rule Content

Detailed instructions or guidelines go here.
```

### Minimum Valid Rule
```markdown
---
description: Rule description here
---

Rule content.
```

## How Cursor Integrates Skills

Based on Cursor documentation:

1. **Skills are Claude Plugin Components**
   - Skills are packaged as `.skill` files
   - Imported into Cursor via Claude plugin system
   - Defined in `marketplace.json` or plugin configuration

2. **Skills vs Rules**
   - **Skills**: Model-invoked capabilities (Claude decides when to use)
   - **Rules**: Always-applied project guidance (Cursor applies based on context)
   - They work together but serve different purposes

3. **Integration Points**
   - Skills extend what Claude can do
   - Rules guide how Claude should behave in your project
   - Both are included in Claude's context when relevant

## Finding and Fixing Rule Issues

### Step 1: Locate Rule Files
```bash
find . -name "*.mdc" -o -name ".cursorrules"
find . -type d -name ".cursor"
```

### Step 2: Check Each Rule File
Ensure every `.mdc` file has:
- `description` field in frontmatter
- Valid YAML frontmatter
- Content after frontmatter

### Step 3: Fix Missing Descriptions
Add description to any rule missing it:

```markdown
---
description: [Add clear description here]
---
```

## Best Practices

1. **Rule Descriptions**
   - Be specific and clear
   - Describe what the rule does, not how
   - Keep under 100 characters for description field

2. **File Patterns (globs)**
   - Use globs to scope rules to specific files
   - Example: `["**/*.ts", "**/*.tsx"]` for TypeScript files
   - Leave empty or omit if rule applies broadly

3. **Organization**
   - Group related rules in subdirectories
   - Use descriptive filenames
   - Keep rules focused and composable

## References

- [Cursor Rules Documentation](https://docs.cursor.com/context/rules)
- [Claude Plugin Skills](https://docs.claude.com/en/docs/claude-code/plugins-reference)
- [Agent Skills Specification](https://agentskills.io/specification)

## Current Status

- ✅ Skills use proper SKILL.md format with description
- ⚠️ Need to check for any `.mdc` rule files missing descriptions
- ⚠️ Need to verify no orphaned rule files exist
