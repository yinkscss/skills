# Cursor Rule Error Analysis

## Error Message
```
There was an error passing the rule for Cursor because description is required, 
and there was no description in the rule. This rule has no description or file 
pattern, and it may never be used by Cursor.
```

## Investigation Results

### Files Searched
- ✅ No `.mdc` files found in skills directory
- ✅ No `.cursorrules` files found
- ✅ No `.cursor/rules/` directory found
- ✅ Skills have proper `description` in SKILL.md frontmatter

### Cursor Rules System (from documentation)

**Location**: `.cursor/rules/` directory in project root

**Required Format**:
```markdown
---
description: Brief description (REQUIRED)
globs: ["pattern/**/*.ext"]  # Optional
alwaysApply: false  # Optional
---

Rule content here.
```

**Key Points**:
- Every `.mdc` file MUST have a `description` field
- Rules without description or file patterns may never be used
- Rules are different from Skills (Skills are `.skill` files, Rules are `.mdc` files)

## Possible Causes

1. **Hidden Rule File**: A rule file might exist in a parent directory or hidden location
2. **Cursor Auto-Detection**: Cursor might be trying to interpret a file as a rule
3. **Plugin Configuration**: The error might be in how the skill is registered in Cursor

## Recommended Actions

### 1. Check for Rule Files
```bash
# Check current directory and parent directories
find . -name "*.mdc" -o -name ".cursorrules"
find .. -name "*.mdc" -o -name ".cursorrules" 2>/dev/null

# Check for .cursor directory
find . -type d -name ".cursor"
find .. -type d -name ".cursor" 2>/dev/null
```

### 2. Check Cursor Settings
- Open Cursor Settings > Rules
- Look for any rules without descriptions
- Check for rules pointing to this project

### 3. Verify Skill Format
The prompt-engineering skill has proper format:
```yaml
---
name: prompt-engineering
description: Comprehensive guide for prompt engineering...
---
```

This is correct for a Skill, not a Cursor Rule.

### 4. Create Rule File (if needed)
If you want to create a Cursor rule for this project:

```bash
mkdir -p .cursor/rules
```

Create `.cursor/rules/prompt-engineering.mdc`:
```markdown
---
description: Use prompt engineering best practices when crafting prompts
globs: ["**/*.md", "**/*.txt"]
alwaysApply: false
---

When working with prompts or prompt engineering:
- Follow strict formatting rules for bullet points
- Use imperative verbs for instructions
- Be explicit and specific
- Reference the prompt-engineering skill when needed
```

## Cursor Integration Summary

### Skills (Claude Plugin)
- Format: `.skill` files (zip) containing `SKILL.md`
- Location: `skills/` directory
- Required: `name`, `description` in frontmatter
- Purpose: Extend Claude's capabilities

### Rules (Cursor Project Guidance)
- Format: `.mdc` files in `.cursor/rules/`
- Required: `description` field
- Purpose: Project-specific AI behavior guidance

### Integration
- Skills are loaded by Claude plugin system
- Rules are loaded by Cursor based on context
- They work together but are separate systems

## Next Steps

1. **Locate the problematic rule**: Check Cursor Settings > Rules
2. **Add description**: If a rule exists without description, add it
3. **Remove invalid rules**: Delete any rules that shouldn't exist
4. **Verify skill format**: Confirm SKILL.md has proper description (✅ already correct)

## Communication to Cursor Team

If reporting this issue to Cursor:

**Issue**: Rule validation error - missing description
**Context**: Working with Claude Skills plugin
**Error**: "This rule has no description or file pattern"
**Investigation**: No `.mdc` or `.cursorrules` files found in project
**Question**: 
- Could Cursor be interpreting SKILL.md files as rules?
- Should Skills have different handling than Rules?
- Is there a way to exclude Skills from rule validation?

**Skill Format (Current)**:
```yaml
---
name: prompt-engineering
description: Comprehensive guide for prompt engineering...
---
```

This format is correct per Agent Skills Spec, but Cursor might be trying to validate it as a rule.
