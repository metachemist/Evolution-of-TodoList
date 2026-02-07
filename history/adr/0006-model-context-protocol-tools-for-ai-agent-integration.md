# ADR-0006: Model Context Protocol (MCP) Tools for AI Agent Integration

## Status
Proposed

## Date
2026-02-07

## Context
The application must support AI agent interactions through standardized protocols as mandated by the constitution. MCP tools provide a standardized interface between AI agents and application functionality.

## Decision
- MCP Tool Layer: Standardized interface layer between AI agents and core API
- Statelessness: All MCP tools read/write to database, not memory
- Clear Contracts: Well-defined JSON input/output schemas
- Error Handling: Structured error objects instead of exceptions
- Composability: Tools designed for chaining by AI agents

## Alternatives
- Alternative 1: Direct API calls from AI agents without standardized tools
- Alternative 2: GraphQL-based approach instead of REST/MCP
- Alternative 3: Custom protocol instead of MCP

## Consequences
- Positive: Standardized AI integration, clear contracts, composability
- Negative: Additional complexity, learning curve for MCP protocol
- Risk: MCP specification changes could impact implementation

## References
- @specs/2-plan/phase-2-fullstack.md
- @specs/2-plan/api-specs/rest-endpoints.md
- @constitution.md (AI-native architecture requirements)