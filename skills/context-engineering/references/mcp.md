# Model Context Protocol (MCP) Reference

## What is MCP?

MCP is the "USB-C port for AI applications." It is an open-source standard (emerged late 2025) that standardises how LLM clients (desktop apps, IDEs, cloud agents) connect to external data sources, enterprise databases, and execution tools.

Before MCP, developers wrote fragile, custom glue-code for every integration. MCP eliminates that technical debt through a language-agnostic, two-layer architecture.

## Architecture

### The Data Layer (JSON-RPC 2.0)

Defines strict protocols for client-server communication. Manages connection lifecycles and establishes three core primitives:

| Primitive | Type | Description |
|-----------|------|-------------|
| **Resources** | Read-only | File-like data providing foundational context (database schemas, API logs, policy documents) |
| **Tools** | Executable | Functions the LLM can invoke to take action (SQL queries, shell scripts, API calls) |
| **Prompts** | Reusable | Server-side instruction templates for standardised tasks |

The data layer supports real-time, bidirectional notifications. If a server's tools change or a resource updates, it sends notifications to the client — context shifts dynamically without human intervention.

### The Transport Layer

| Transport | Use Case | Characteristics |
|-----------|----------|-----------------|
| **STDIO** | Local integrations (e.g., Claude Desktop accessing local codebases) | Runs as local child process over standard I/O. Zero HTTP overhead. Local data stays on host machine. |
| **HTTP with SSE / Streamable HTTP** | Distributed enterprise deployments (remote BigQuery, AWS, Sentry) | Secure, stateless scalability across cloud environments. |

## Key Design Principle

An MCP Server is entirely agnostic to which LLM interacts with it. The server exposes capabilities via structured schemas. The protocol handles the secure handshake and format conversion.

**Build a tool once, containerise it, and expose it to any current or future AI model that supports the protocol.**

## MCP Server Design Checklist

When designing an MCP server, define:

1. **Resources** — List each with schema, description, access level, and explicit data redaction rules
2. **Tools** — List each with name, input parameters, return type, rate limits, and permission boundaries
3. **Prompts** — Design 2-3 server-side prompt templates for the most common agent tasks
4. **Transport** — Choose STDIO (local) vs HTTP/SSE (remote) based on deployment requirements
5. **Security boundaries** — Explicit redaction rules, read-only vs read-write operations, conditions for refusing requests
