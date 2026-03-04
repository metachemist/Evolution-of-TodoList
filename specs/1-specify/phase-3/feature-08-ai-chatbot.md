# Feature Specification: AI Chatbot for Todo Management (Phase III)

**Feature Branch**: `feature-08-ai-chatbot`
**Created**: 2026-03-04
**Status**: Draft
**Input**: Phase III requirements from Hackathon II + constitutional mandates in `constitution.md`

## Constitutional Compliance

This specification is governed by `constitution.md` as the source of truth and explicitly enforces:

- SDD loop order: Specify -> Plan -> Tasks -> Implement
- Mandatory monorepo structure under `specs/1-specify/phase-3/`
- Phase III stack: OpenAI ChatKit, OpenAI Agents SDK, Official MCP SDK (Python), FastAPI, SQLModel, Neon PostgreSQL
- AI-native architecture: MCP tools as first-class interaction pattern
- Stateless service design: no in-memory session state on server
- Security requirements: JWT validation on every protected request, user isolation, structured errors

## User Scenarios & Testing (mandatory)

### User Story 1 - Natural Language Task Management (Priority: P1)

An authenticated user can manage their todos in plain language through a chatbot.

**Why this priority**: This is the core value of Phase III and the primary architectural shift from CRUD UI to AI-native interaction.

**Independent Test**: Send chat messages for create/list/update/complete/delete and verify correct MCP tool invocation plus database state changes.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they say "Add a task to buy groceries", **Then** the agent invokes `add_task` and confirms creation.
2. **Given** an authenticated user, **When** they ask "Show my pending tasks", **Then** the agent invokes `list_tasks(status="pending")` and returns only that user's pending tasks.
3. **Given** an authenticated user, **When** they say "Mark task 3 complete", **Then** the agent invokes `complete_task` and confirms completion.
4. **Given** an authenticated user, **When** they say "Delete task 2", **Then** the agent invokes `delete_task` and confirms deletion.
5. **Given** an authenticated user, **When** they say "Rename task 1 to Pay bills tonight", **Then** the agent invokes `update_task` and confirms update.

---

### User Story 2 - Stateless Conversation Continuity (Priority: P1)

The chatbot maintains context through database-persisted conversation and message history while keeping the API server stateless.

**Why this priority**: Constitution requires stateless architecture and database-persisted state for AI scalability.

**Independent Test**: Create a conversation, restart backend, continue same conversation ID, verify continuity.

**Acceptance Scenarios**:

1. **Given** a user starts a chat without `conversation_id`, **When** first message is sent, **Then** a new conversation is created and returned.
2. **Given** a user provides existing `conversation_id`, **When** another message is sent, **Then** prior history is loaded from DB and used by the agent.
3. **Given** backend restarts, **When** user resumes a conversation by ID, **Then** history remains available and response quality is preserved.

---

### User Story 3 - Secure Multi-User Isolation in Chat (Priority: P1)

Chat interactions and task operations are strictly user-scoped.

**Why this priority**: Constitution mandates user isolation and JWT validation for all protected API calls.

**Independent Test**: User A cannot access or mutate User B conversations/tasks through chat endpoint or MCP tool invocation.

**Acceptance Scenarios**:

1. **Given** User A token and User B `user_id` path, **When** chat request is sent, **Then** API returns 403.
2. **Given** valid token but conversation owned by another user, **When** request is sent, **Then** API returns 404 or 403 according to authorization policy without data leakage.
3. **Given** missing/invalid token, **When** request is sent, **Then** API returns 401 with structured error.

---

### User Story 4 - Graceful AI and Tool Error Handling (Priority: P2)

The chatbot returns safe, structured, user-friendly failures when AI/tool operations fail.

**Why this priority**: Reliability and trust require predictable failure behavior.

**Independent Test**: Simulate MCP tool errors, unavailable DB, and invalid inputs; verify structured error responses and user-safe assistant messaging.

**Acceptance Scenarios**:

1. **Given** a non-existent task ID, **When** user asks to complete/delete it, **Then** tool returns structured `TASK_NOT_FOUND` and assistant responds clearly.
2. **Given** transient DB failure, **When** chat is processed, **Then** API returns structured `SERVICE_UNAVAILABLE` and does not lose already stored user message intent.
3. **Given** malformed request body, **When** endpoint is called, **Then** API returns `VALIDATION_ERROR` with 400.

## Edge Cases

- Ambiguous user request requiring tool disambiguation (e.g., "delete the meeting task" when multiple matches exist)
- Repeated duplicate messages (idempotency expectations for tool calls where possible)
- MCP tool timeout or model timeout
- Very long conversation history requiring truncation strategy while preserving recent context
- Expired token mid-conversation

## Requirements (mandatory)

### Functional Requirements

- **FR-001**: System MUST provide a chat UI using OpenAI ChatKit.
- **FR-002**: System MUST expose `POST /api/{user_id}/chat` for chat interactions.
- **FR-003**: Chat endpoint MUST accept `message` and optional `conversation_id`.
- **FR-004**: If `conversation_id` is omitted, system MUST create a new conversation.
- **FR-005**: System MUST persist user and assistant messages in database.
- **FR-006**: Server MUST remain stateless between requests (no in-memory conversation/session state as source of truth).
- **FR-007**: Agent runtime MUST use OpenAI Agents SDK.
- **FR-008**: Agent MUST invoke task operations through MCP tools, not direct ad-hoc logic.
- **FR-009**: MCP server MUST use Official MCP SDK (Python).
- **FR-010**: MCP tools MUST be stateless and DB-backed.
- **FR-011**: MCP server MUST expose tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`.
- **FR-012**: Chat responses MUST include `conversation_id`, assistant `response`, and `tool_calls` metadata.
- **FR-013**: All protected requests MUST validate JWT and enforce user isolation.
- **FR-014**: Path `user_id` MUST match authenticated principal before processing request.
- **FR-015**: Task and conversation access MUST be scoped to the authenticated user.
- **FR-016**: All API responses MUST use standard envelope `{success,data,error}`.
- **FR-017**: All errors MUST return structured error objects with stable codes/messages.
- **FR-018**: System MUST log structured JSON for chat requests, tool invocations, and failures.
- **FR-019**: Tool invocation outputs MUST be schema-validated before being returned to the agent.
- **FR-020**: Agent MUST provide confirmation-style responses for successful state-changing operations.
- **FR-021**: Agent MUST gracefully handle tool failures and request clarification when intent is ambiguous.
- **FR-022**: Conversation records MUST survive backend restart.
- **FR-023**: Database schema MUST include `conversations` and `messages` with `user_id` ownership and timestamps.
- **FR-024**: API MUST support listing/filtering tasks via natural language intents mapped to MCP tool parameters.

### MCP Tool Contracts

#### Tool: `add_task`

- **Input**: `user_id: str` (required), `title: str` (required), `description: str | null` (optional)
- **Output**: `{ "task_id": <id>, "status": "created", "title": <title> }`

#### Tool: `list_tasks`

- **Input**: `user_id: str` (required), `status: "all" | "pending" | "completed"` (optional, default `all`)
- **Output**: `[{ "id": <id>, "title": <str>, "completed": <bool> }, ...]`

#### Tool: `complete_task`

- **Input**: `user_id: str` (required), `task_id: int | str` (required)
- **Output**: `{ "task_id": <id>, "status": "completed", "title": <title> }`

#### Tool: `delete_task`

- **Input**: `user_id: str` (required), `task_id: int | str` (required)
- **Output**: `{ "task_id": <id>, "status": "deleted", "title": <title> }`

#### Tool: `update_task`

- **Input**: `user_id: str` (required), `task_id: int | str` (required), `title: str | null` (optional), `description: str | null` (optional)
- **Output**: `{ "task_id": <id>, "status": "updated", "title": <title> }`

### API Contract

#### Endpoint

- **Method**: `POST`
- **Path**: `/api/{user_id}/chat`
- **Auth**: Required (JWT)

#### Request Body

```json
{
  "conversation_id": "optional-id",
  "message": "string"
}
```

#### Success Response (200)

```json
{
  "success": true,
  "data": {
    "conversation_id": "id",
    "response": "assistant response",
    "tool_calls": [
      {
        "name": "list_tasks",
        "arguments": {"status": "pending"},
        "result": {}
      }
    ]
  },
  "error": null
}
```

#### Error Response (example)

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Please log in to continue."
  }
}
```

## Data Model (Phase III Additions)

- **Conversation**: `id`, `user_id`, `created_at`, `updated_at`
- **Message**: `id`, `user_id`, `conversation_id`, `role` (`user` | `assistant`), `content`, `created_at`

Constraints:

- `Conversation.user_id` and `Message.user_id` MUST reference authenticated owner
- `Message.conversation_id` MUST reference `Conversation.id`
- Indexes on `user_id`, `conversation_id`, and `created_at`

## Security Requirements

- **SEC-001**: JWT required for chat endpoint.
- **SEC-002**: 401 for missing/invalid token.
- **SEC-003**: 403 for `{user_id}` mismatch.
- **SEC-004**: No cross-user conversation/message/task visibility.
- **SEC-005**: Input validation for all endpoint and MCP tool inputs.
- **SEC-006**: No raw SQL for tool operations; ORM only.
- **SEC-007**: Structured error outputs only; no stack trace leakage.
- **SEC-008**: Rate limiting applies to chat endpoint and tool-triggering flows.

## Performance & Scalability Requirements

- **PERF-001**: P95 end-to-end AI chat response time MUST be <= 2 seconds under normal load.
- **PERF-002**: Phase III deployment MUST support at least 100 concurrent users.
- **PERF-003**: Chat endpoint and tool invocation paths MUST be fully async for I/O.
- **PERF-004**: Conversation retrieval and message persistence queries MUST be indexed.

## Testing Requirements

- **TEST-001**: Phase III automated test coverage target MUST be >= 65% for business logic.
- **TEST-002**: MCP tool invocation tests are mandatory for all tools.
- **TEST-003**: Integration tests MUST verify conversation persistence across restart.
- **TEST-004**: Authorization tests MUST verify 401/403/user isolation behavior.
- **TEST-005**: API contract tests MUST verify response envelope and error catalog consistency.

## Non-Goals (Phase III base scope)

- Kubernetes/Helm/Minikube deployment concerns (Phase IV)
- Kafka/Dapr/event-driven extensions (Phase V)
- Voice command support (bonus track)
- Urdu localization support (bonus track)

## Success Criteria (mandatory)

- **SC-001**: User can create/list/update/complete/delete tasks via natural language chat.
- **SC-002**: Chat state survives backend restart using DB-backed conversations/messages.
- **SC-003**: 100% cross-user isolation in chat and task operations.
- **SC-004**: Agent uses MCP tools for task operations (verified in tool call telemetry/tests).
- **SC-005**: P95 chat response <= 2s at Phase III load target.
- **SC-006**: Coverage and test requirements in this spec are met.

## Assumptions

- Phase II authentication and user-scoped task APIs are available and stable.
- Existing task CRUD contracts remain backward compatible for MCP tool composition.
- OpenAI ChatKit and Agents SDK credentials/configuration will be provided through environment variables.
