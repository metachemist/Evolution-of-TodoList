# Feature 01: Task CRUD Operations

## User Stories

### US-2.1: As a user, I want to create tasks so that I can organize and track my activities

**Acceptance Criteria:**
- Given I am logged in, when I navigate to the task creation page, then I should see a form to create a new task
- Given I have filled in a valid task title and optional description, when I submit the form, then the task should be created successfully and visible in my task list
- Given I have entered an invalid task (empty title or exceeding character limits), when I submit the form, then I should see an appropriate error message and the task should not be created
- Given I am on the task creation page, when I decide not to create a task, then I should be able to navigate away without saving

### US-2.2: As a user, I want to view my tasks so that I can see what I need to do

**Acceptance Criteria:**
- Given I am logged in, when I visit the dashboard or task list page, then I should see all tasks that belong to me
- Given I have many tasks, when I view my task list, then I should see them organized with the most recent tasks at the top
- Given I have completed and pending tasks, when I view my task list, then I should be able to distinguish between completed and pending tasks
- Given I have no tasks, when I visit my task list, then I should see an appropriate message indicating that there are no tasks

### US-2.3: As a user, I want to update my tasks so that I can modify information as needed

**Acceptance Criteria:**
- Given I am viewing a task, when I select the edit option, then I should be able to modify the task details
- Given I have made changes to a task, when I save the changes, then the task should be updated and reflect the changes in my task list
- Given I am editing a task and decide not to save changes, when I cancel the edit, then the original task details should remain unchanged
- Given I attempt to update a task with invalid information, when I save, then I should see an error message and the task should remain unchanged

### US-2.4: As a user, I want to delete tasks so that I can remove items I no longer need

**Acceptance Criteria:**
- Given I am viewing a task I want to remove, when I select the delete option, then I should be prompted for confirmation
- Given I confirm deletion, when I proceed with deletion, then the task should be removed from my task list permanently
- Given I decide not to delete the task, when I cancel the deletion, then the task should remain unchanged
- Given I attempt to delete another user's task, when I proceed, then the operation should be denied with an appropriate error message

### US-2.5: As a user, I want to mark tasks as complete so that I can track my progress

**Acceptance Criteria:**
- Given I am viewing a pending task, when I select the complete option, then the task should be marked as completed in my task list
- Given I have marked a task as completed, when I view it again, then it should be visually distinguished from pending tasks
- Given I accidentally marked a task as complete, when I toggle the completion status, then the task should revert to pending status
- Given I attempt to mark another user's task as complete, when I proceed, then the operation should be denied with an appropriate error message

## Functional Requirements

### FR-2.1: Create Task

**Input:**
- Title (string, required, 1-200 characters after trimming)
- Description (string, optional, 0-1000 characters)

**Process:**
1. Extract user_id from authenticated JWT token
2. Validate title is not empty after trimming whitespace
3. Validate title length ≤ 200 characters
4. Validate description length ≤ 1000 characters (if provided)
5. Create task record in database:
   - user_id = authenticated user from JWT
   - title = provided title (trimmed)
   - description = provided description (or null)
   - completed = false (default)
   - created_at = current UTC timestamp
   - updated_at = current UTC timestamp
6. Insert into tasks table
7. Return created task object with auto-generated ID

**Output:**
Task object with all fields including auto-generated ID

**Error Cases:**
- Empty title (after trim) → 400 "Title is required"
- Title > 200 chars → 400 "Title must be 200 characters or less"
- Description > 1000 chars → 400 "Description must be 1000 characters or less"
- Database connection failed → 500 "Failed to create task. Please try again."
- Invalid JWT token → 401 "Authentication required"
- user_id mismatch → 403 "Unauthorized to access this resource"

**Database Schema:**
```sql
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES ($1, $2, $3, false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
RETURNING *;
```

**API Example:**
```bash
curl -X POST http://localhost:8000/api/user_abc123/tasks \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"title":"Prepare Q4 presentation","description":"Slides for board meeting"}'
```

### FR-2.2: List Tasks (Filtering by user_id, Ordering)

**Input:**
- user_id (extracted from JWT token, validated against URL parameter)
- Optional query parameters: limit, offset for pagination

**Process:**
1. Extract authenticated user_id from JWT token
2. Validate user_id in token matches URL parameter
3. Query tasks table filtering by user_id
4. Order results by created_at descending (most recent first)
5. Apply pagination if specified
6. Return array of task objects

**Output:**
Array of task objects with all fields

**Error Cases:**
- Invalid JWT token → 401 "Authentication required"
- user_id mismatch → 403 "Unauthorized to access this resource"
- Database connection failed → 500 "Failed to retrieve tasks. Please try again."

**Database Schema:**
```sql
SELECT * FROM tasks
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT $2 OFFSET $3;
```

**API Example:**
```bash
curl -X GET http://localhost:8000/api/user_abc123/tasks \
  -H "Authorization: Bearer eyJhbGc..."
```

### FR-2.3: Get Single Task

**Input:**
- user_id (extracted from JWT token, validated against URL parameter)
- task_id (integer from URL path parameter)

**Process:**
1. Extract authenticated user_id from JWT token
2. Validate user_id in token matches URL parameter
3. Validate task_id is a positive integer
4. Query tasks table for specific task_id and user_id combination
5. Return single task object if found

**Output:**
Single task object with all fields

**Error Cases:**
- Invalid JWT token → 401 "Authentication required"
- user_id mismatch → 403 "Unauthorized to access this resource"
- Task not found → 404 "Task not found"
- Invalid task_id → 400 "Invalid task ID"
- Database connection failed → 500 "Failed to retrieve task. Please try again."

**Database Schema:**
```sql
SELECT * FROM tasks
WHERE id = $1 AND user_id = $2;
```

**API Example:**
```bash
curl -X GET http://localhost:8000/api/user_abc123/tasks/123 \
  -H "Authorization: Bearer eyJhbGc..."
```

### FR-2.4: Update Task

**Input:**
- user_id (extracted from JWT token, validated against URL parameter)
- task_id (integer from URL path parameter)
- Update fields: title (optional, 1-200 chars), description (optional, 0-1000 chars)

**Process:**
1. Extract authenticated user_id from JWT token
2. Validate user_id in token matches URL parameter
3. Validate task_id is a positive integer
4. Validate title if provided (1-200 chars after trim)
5. Validate description if provided (0-1000 chars)
6. Update task record in database:
   - Update title if provided (trimmed)
   - Update description if provided (or set to null)
   - Update updated_at = current UTC timestamp
   - Preserve completed status and created_at
7. Return updated task object

**Output:**
Updated task object with all fields

**Error Cases:**
- Invalid JWT token → 401 "Authentication required"
- user_id mismatch → 403 "Unauthorized to access this resource"
- Task not found → 404 "Task not found"
- Invalid task_id → 400 "Invalid task ID"
- Title > 200 chars → 400 "Title must be 200 characters or less"
- Description > 1000 chars → 400 "Description must be 1000 characters or less"
- Database connection failed → 500 "Failed to update task. Please try again."

**Database Schema:**
```sql
UPDATE tasks
SET title = COALESCE($1, title),
    description = COALESCE($2, description),
    updated_at = CURRENT_TIMESTAMP
WHERE id = $3 AND user_id = $4
RETURNING *;
```

**API Example:**
```bash
curl -X PUT http://localhost:8000/api/user_abc123/tasks/123 \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated task title","description":"Updated description"}'
```

### FR-2.5: Delete Task

**Input:**
- user_id (extracted from JWT token, validated against URL parameter)
- task_id (integer from URL path parameter)

**Process:**
1. Extract authenticated user_id from JWT token
2. Validate user_id in token matches URL parameter
3. Validate task_id is a positive integer
4. Verify task belongs to authenticated user
5. Delete task record from database
6. Return success confirmation

**Output:**
Success confirmation message

**Error Cases:**
- Invalid JWT token → 401 "Authentication required"
- user_id mismatch → 403 "Unauthorized to access this resource"
- Task not found → 404 "Task not found"
- Invalid task_id → 400 "Invalid task ID"
- Database connection failed → 500 "Failed to delete task. Please try again."

**Database Schema:**
```sql
DELETE FROM tasks
WHERE id = $1 AND user_id = $2;
```

**API Example:**
```bash
curl -X DELETE http://localhost:8000/api/user_abc123/tasks/123 \
  -H "Authorization: Bearer eyJhbGc..."
```

### FR-2.6: Toggle Completion

**Input:**
- user_id (extracted from JWT token, validated against URL parameter)
- task_id (integer from URL path parameter)
- completion_status (boolean, optional - if not provided, toggle current status)

**Process:**
1. Extract authenticated user_id from JWT token
2. Validate user_id in token matches URL parameter
3. Validate task_id is a positive integer
4. If completion_status provided, use that value
5. If completion_status not provided, toggle current completion status
6. Update task record with new completion status
7. Update updated_at timestamp
8. Return updated task object

**Output:**
Updated task object with all fields

**Error Cases:**
- Invalid JWT token → 401 "Authentication required"
- user_id mismatch → 403 "Unauthorized to access this resource"
- Task not found → 404 "Task not found"
- Invalid task_id → 400 "Invalid task ID"
- Invalid completion_status → 400 "Invalid completion status"
- Database connection failed → 500 "Failed to update task. Please try again."

**Database Schema:**
```sql
UPDATE tasks
SET completed = CASE
                  WHEN $1 IS NULL THEN NOT completed
                  ELSE $1
                END,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $2 AND user_id = $3
RETURNING *;
```

**API Example:**
```bash
curl -X PATCH http://localhost:8000/api/user_abc123/tasks/123/complete \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

## Data Model (SQLModel Schema)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: int = Field(primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None

class TaskComplete(SQLModel):
    completed: bool
```

## API Endpoint Specifications

### Create Task: POST /api/{user_id}/tasks
- **Method**: POST
- **Path Parameter**: user_id (string)
- **Request Body**: TaskCreate object
- **Response**: TaskRead object
- **Authentication**: Required JWT token

### List Tasks: GET /api/{user_id}/tasks
- **Method**: GET
- **Path Parameter**: user_id (string)
- **Query Parameters**: limit, offset (for pagination)
- **Response**: Array of TaskRead objects
- **Authentication**: Required JWT token

### Get Task: GET /api/{user_id}/tasks/{id}
- **Method**: GET
- **Path Parameters**: user_id (string), id (integer)
- **Response**: TaskRead object
- **Authentication**: Required JWT token

### Update Task: PUT /api/{user_id}/tasks/{id}
- **Method**: PUT
- **Path Parameters**: user_id (string), id (integer)
- **Request Body**: TaskUpdate object
- **Response**: TaskRead object
- **Authentication**: Required JWT token

### Delete Task: DELETE /api/{user_id}/tasks/{id}
- **Method**: DELETE
- **Path Parameters**: user_id (string), id (integer)
- **Response**: Success confirmation
- **Authentication**: Required JWT token

### Toggle Task Completion: PATCH /api/{user_id}/tasks/{id}/complete
- **Method**: PATCH
- **Path Parameters**: user_id (string), id (integer)
- **Request Body**: TaskComplete object
- **Response**: TaskRead object
- **Authentication**: Required JWT token

## MCP Tool Specifications

### MCP Tool 1: Create Task Tool
- **Name**: `create_task`
- **Description**: Creates a new task for the authenticated user
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "Authenticated user ID from JWT token"},
      "title": {"type": "string", "minLength": 1, "maxLength": 200, "description": "Task title (1-200 chars)"},
      "description": {"type": "string", "maxLength": 1000, "description": "Optional task description (0-1000 chars)"},
      "completed": {"type": "boolean", "default": false, "description": "Initial completion status"}
    },
    "required": ["user_id", "title"]
  }
  ```
- **Process**:
  1. Validate user_id from input matches user_id in JWT token
  2. Validate title length (1-200 chars after trim)
  3. Validate description length (0-1000 chars if provided)
  4. Create task record in database with user_id association
  5. Set completed status (false by default, or as specified)
  6. Set created_at and updated_at to current timestamp
  7. Return created task object with auto-generated ID
- **Output**: Created task object with all fields including auto-generated ID
- **Error Cases**:
  - User ID mismatch → 403 "Unauthorized to access this resource"
  - Invalid title → 400 "Title is required and must be 1-200 characters"
  - Invalid description → 400 "Description must be 1000 characters or less"
  - Database connection failed → 500 "Failed to create task. Please try again."

### MCP Tool 2: Get User Tasks Tool
- **Name**: `get_user_tasks`
- **Description**: Retrieves all tasks for the specified user with optional filtering and pagination
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "User ID whose tasks to retrieve"},
      "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20, "description": "Number of tasks per page"},
      "offset": {"type": "integer", "minimum": 0, "default": 0, "description": "Offset for pagination"},
      "completed": {"type": "boolean", "description": "Filter by completion status (true/false) - omit for all tasks"}
    },
    "required": ["user_id"]
  }
  ```
- **Process**:
  1. Validate user_id in input matches user_id in JWT token
  2. Query tasks table filtered by user_id
  3. Apply completion filter if specified
  4. Apply pagination with limit and offset
  5. Order results by created_at DESC (most recent first)
  6. Return array of task objects with pagination metadata
- **Output**: Object containing tasks array and pagination metadata
- **Error Cases**:
  - User ID mismatch → 403 "Unauthorized to access this resource"
  - Invalid parameters → 400 "Invalid query parameters"
  - Database connection failed → 500 "Failed to retrieve tasks. Please try again."

### MCP Tool 3: Get Single Task Tool
- **Name**: `get_task`
- **Description**: Retrieves a specific task by ID for the authenticated user
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "User ID associated with the task"},
      "task_id": {"type": "integer", "minimum": 1, "description": "ID of the task to retrieve"}
    },
    "required": ["user_id", "task_id"]
  }
  ```
- **Process**:
  1. Validate user_id in input matches user_id in JWT token
  2. Validate task_id is a positive integer
  3. Query tasks table for specific task_id and user_id combination
  4. Return single task object if found
- **Output**: Single task object with all fields
- **Error Cases**:
  - User ID mismatch → 403 "Unauthorized to access this resource"
  - Invalid task_id → 400 "Invalid task ID"
  - Task not found → 404 "Task not found"
  - Database connection failed → 500 "Failed to retrieve task. Please try again."

### MCP Tool 4: Update Task Tool
- **Name**: `update_task`
- **Description**: Updates an existing task for the authenticated user
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "Authenticated user ID"},
      "task_id": {"type": "integer", "minimum": 1, "description": "ID of task to update"},
      "title": {"type": "string", "minLength": 1, "maxLength": 200, "description": "New task title"},
      "description": {"type": "string", "maxLength": 1000, "description": "New task description"},
      "completed": {"type": "boolean", "description": "New completion status"}
    },
    "required": ["user_id", "task_id"]
  }
  ```
- **Process**:
  1. Validate user_id in input matches user_id in JWT token
  2. Validate task_id is a positive integer
  3. Validate title if provided (1-200 chars after trim)
  4. Validate description if provided (0-1000 chars)
  5. Update task record in database with provided fields
  6. Update updated_at timestamp to current time
  7. Return updated task object
- **Output**: Updated task object with all fields
- **Error Cases**:
  - User ID mismatch → 403 "Unauthorized to access this resource"
  - Invalid task_id → 400 "Invalid task ID"
  - Invalid input → 400 "Invalid task data provided"
  - Task not found → 404 "Task not found"
  - Database connection failed → 500 "Failed to update task. Please try again."

### MCP Tool 5: Delete Task Tool
- **Name**: `delete_task`
- **Description**: Deletes a specific task for the authenticated user
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "Authenticated user ID"},
      "task_id": {"type": "integer", "minimum": 1, "description": "ID of task to delete"}
    },
    "required": ["user_id", "task_id"]
  }
  ```
- **Process**:
  1. Validate user_id in input matches user_id in JWT token
  2. Validate task_id is a positive integer
  3. Verify task exists and belongs to authenticated user
  4. Delete task record from database
  5. Return success confirmation
- **Output**: Success confirmation object
- **Error Cases**:
  - User ID mismatch → 403 "Unauthorized to access this resource"
  - Invalid task_id → 400 "Invalid task ID"
  - Task not found → 404 "Task not found"
  - Database connection failed → 500 "Failed to delete task. Please try again."

### MCP Tool 6: Toggle Task Completion Tool
- **Name**: `toggle_task_completion`
- **Description**: Toggles or sets the completion status of a task
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "Authenticated user ID"},
      "task_id": {"type": "integer", "minimum": 1, "description": "ID of task to update"},
      "completed": {"type": "boolean", "description": "Desired completion status (optional - if omitted, toggle current status)"}
    },
    "required": ["user_id", "task_id"]
  }
  ```
- **Process**:
  1. Validate user_id in input matches user_id in JWT token
  2. Validate task_id is a positive integer
  3. If completed parameter provided, set to that value
  4. If completed parameter not provided, toggle current completion status
  5. Update task's completion status and updated_at timestamp
  6. Return updated task object
- **Output**: Updated task object with new completion status
- **Error Cases**:
  - User ID mismatch → 403 "Unauthorized to access this resource"
  - Invalid task_id → 400 "Invalid task ID"
  - Task not found → 404 "Task not found"
  - Invalid completion status → 400 "Completion status must be boolean"
  - Database connection failed → 500 "Failed to update task. Please try again."

## MCP Architecture Principles

### Statelessness (Constitutional Requirement)
- All MCP tools must read/write from/to database, not memory (per Constitution 489-490)
- No session state stored in server memory
- All user state stored in PostgreSQL database
- JWT tokens used for authentication without server-side sessions

### Clear Contract Design (Constitutional Requirement)
- All MCP tools have well-defined input/output schemas (per Constitution 491)
- Input validation implemented for all parameters
- Consistent response formats across all tools
- Explicit error codes and messages for all failure scenarios

### Error Handling (Constitutional Requirement)
- All MCP tools return structured error objects, not exceptions (per Constitution 492)
- Proper HTTP status codes for different error types
- Human-readable error messages that don't expose system internals
- Comprehensive error logging for debugging while protecting user privacy

### Composability (Constitutional Requirement)
- MCP tools can be chained by agents for complex operations (per Constitution 493)
- Each tool performs a single, well-defined operation
- Tools can be combined to perform multi-step operations
- Consistent authentication and authorization across all tools

## UI Component Specifications

### TaskList Component
- **Responsibility**: Display all tasks for the authenticated user
- **Props**: tasks (array of TaskRead objects), onTaskUpdate (function), onTaskDelete (function)
- **Features**: Sort tasks by creation date (newest first), show completion status, provide edit/delete buttons
- **Error Handling**: Show appropriate messages when no tasks exist
- **Loading States**: Display loading indicator during API calls

### TaskItem Component
- **Responsibility**: Represent a single task with all interactive features
- **Props**: task (TaskRead object), onToggleComplete (function), onUpdate (function), onDelete (function)
- **Features**: Display task title and description, completion checkbox, edit/delete buttons
- **Visual States**: Different styling for completed vs pending tasks
- **Event Handling**: Click handlers for completion toggle, edit, and delete

### TaskForm Component
- **Responsibility**: Provide form interface for creating and updating tasks
- **Props**: initialData (TaskUpdate object, optional), onSubmit (function), onCancel (function)
- **Fields**: Title input (required), description textarea (optional), submit/cancel buttons
- **Validation**: Real-time validation for title length and required status
- **Feedback**: Error messages for invalid input

### DeleteConfirmDialog Component
- **Responsibility**: Confirm deletion before permanently removing a task
- **Props**: isOpen (boolean), onConfirm (function), onCancel (function), taskTitle (string)
- **Features**: Warning message with task title, confirmation buttons
- **Accessibility**: Proper focus management and keyboard navigation
- **Visual Design**: Clear warning styling with distinct confirm/cancel buttons

## Business Rules

### Core Business Rules
- **Title Required**: Every task must have a title between 1-200 characters after trimming whitespace
- **Description Limits**: Description, if provided, must be 0-1000 characters
- **Completion Defaults**: New tasks are created with completed status as false by default
- **User Isolation**: Users can only create, read, update, and delete their own tasks
- **Immutable Ownership**: Once a task is created, its user association cannot be changed
- **Timestamp Management**: System automatically manages created_at and updated_at timestamps

### Validation Rules
- **Title Validation**: Title must not be empty after trimming whitespace, and must not exceed 200 characters
- **Description Validation**: Description, if provided, must not exceed 1000 characters
- **ID Validation**: Task IDs must be positive integers
- **User ID Validation**: User IDs in API calls must match the authenticated user from JWT token
- **Format Validation**: All input must conform to expected data types (string, boolean, integer)

### Behavioral Rules
- **Ordering**: Tasks are displayed in descending order by creation date (most recent first)
- **Deletion Impact**: Deleting a task removes it permanently from the system
- **Completion Tracking**: Completed tasks remain accessible but are visually distinguished
- **Concurrent Access**: Multiple tabs/sessions can safely access the same user's tasks
- **Atomic Operations**: Each CRUD operation is atomic - either succeeds completely or fails without changes

## Edge Cases and Error Handling

### Client-Side Edge Cases
- **Network Timeout**: Handle API requests that take too long with timeout messages
- **Offline Scenario**: Display appropriate messaging when user loses internet connection
- **Form Validation**: Prevent submission of invalid forms with clear error messages
- **Browser Refresh**: Preserve form data during accidental browser refreshes where appropriate
- **Concurrent Modifications**: Handle scenarios where task is modified in another session

### Server-Side Edge Cases
- **Concurrent Updates**: Handle multiple simultaneous update requests for the same task
- **Database Locking**: Manage database locks during heavy concurrent usage
- **Invalid JWT Tokens**: Properly reject requests with expired, malformed, or invalid tokens
- **Malformed Requests**: Respond appropriately to requests with incorrect content types or invalid JSON
- **Rate Limiting**: Implement appropriate rate limiting to prevent abuse

### Error Recovery
- **Partial Failures**: Ensure that partial failures don't leave the system in inconsistent states
- **Database Connection Issues**: Implement retry mechanisms with exponential backoff for transient failures
- **Service Unavailability**: Provide graceful degradation when backend services are unavailable
- **Data Corruption**: Include validation to detect and handle potential data corruption issues
- **Security Violations**: Log and monitor potential security-related errors without exposing system details

## Constraints

### Technical Constraints
- **Character Limits**: Task titles must be 1-200 characters after trimming whitespace; descriptions must be 0-1000 characters if provided
- **Data Types**: All input fields must conform to specified data types (string, boolean, integer) with proper type validation
- **Validation Requirements**: All inputs must be validated server-side using Pydantic models regardless of client-side validation
- **API Compliance**: All endpoints must follow RESTful conventions with appropriate HTTP status codes
- **Database Constraints**: All database operations must use SQLModel ORM without raw SQL queries
- **Field Requirements**: Task title is required (1-200 chars after trim), description is optional (0-1000 chars), completion defaults to false
- **Timestamp Management**: System must automatically manage created_at and updated_at timestamps without user input
- **URL Parameter Validation**: All user_id and task_id parameters must be validated against JWT token and proper format

### Performance Constraints
- **Response Times**: 95% of task API operations must complete within 2 seconds
- **Concurrent Users**: System must support 100 concurrent users during peak usage
- **Database Performance**: All queries must utilize appropriate indexes for optimal performance
- **Page Load Times**: Task list pages must load within 3 seconds with up to 100 tasks
- **API Throughput**: System must handle 10 requests per second sustained load
- **Pagination**: Task lists must implement pagination with default 20 items per page (max 100)

### Security Constraints
- **User Isolation**: Users can only access and modify their own tasks (strict user_id validation required)
- **Input Sanitization**: All user inputs must be sanitized to prevent injection attacks using parameterized queries
- **Authentication**: All task endpoints require valid JWT authentication tokens from authorization header
- **Data Validation**: All data must be validated before storage to prevent corruption and ensure integrity
- **Token Validation**: JWT tokens must be validated for signature, expiration, and user_id matching against URL parameters
- **Authorization Checks**: Every request must verify that user_id in JWT token matches user_id in URL parameter
- **Error Message Consistency**: Same error messages for unauthorized access attempts to prevent information disclosure
- **Rate Limiting**: Task endpoints should implement rate limiting to prevent abuse (100 requests per minute per user)

### Environmental Constraints
- **Database**: Must use PostgreSQL with Neon Serverless as specified in Constitution
- **Framework**: Must use FastAPI with SQLModel as specified in Constitution
- **Authentication**: Must use JWT tokens with BETTER_AUTH_SECRET as specified in Constitution
- **Infrastructure**: Frontend on Vercel, Backend on Railway/Render, Database on Neon as specified in Constitution

### Operational Constraints
- **Data Consistency**: All task operations must maintain data consistency with proper transaction handling
- **Atomic Operations**: Each task CRUD operation must be atomic (all-or-nothing)
- **User Ownership**: Once created, tasks cannot change ownership (user association immutable)
- **Deletion Impact**: Task deletion must be permanent with no recovery option in Phase II
- **Concurrent Access**: Multiple sessions per user must be supported without conflicts
- **Session Independence**: No server-side session state (fully stateless using JWT tokens)

## Non-Goals

### Out-of-Scope Features
❌ **Advanced Task Features**:
- Recurring tasks (Phase II+)
- Task sharing between users
- File attachments or rich media
- Collaborative features
- Task categorization or tagging

❌ **Advanced UI Features**:
- Drag-and-drop task reordering
- Bulk task operations
- Task import/export functionality
- Advanced filtering and search capabilities

❌ **Integration Features**:
- Calendar integration
- Email notifications
- Third-party service integrations
- Task synchronization across devices

❌ **Administrative Features**:
- Superuser access to other users' tasks
- Bulk user management
- System-wide task analytics
- Task archival or soft-delete

## Testing Requirements

### Unit Tests
- **Model Validation**: Test all SQLModel validators for Task, TaskCreate, TaskUpdate, etc.
- **Business Logic**: Test all business rule implementations separately
- **Helper Functions**: Test any utility functions for input processing or validation
- **Error Cases**: Test all possible error scenarios with appropriate error handling

### Integration Tests
- **Database Operations**: Test all CRUD operations against actual database
- **API Endpoints**: Test all API endpoints with various input combinations
- **Authentication Flow**: Test JWT validation and user_id verification across all endpoints
- **Edge Cases**: Test boundary conditions and unexpected input scenarios

### End-to-End Tests
- **User Flows**: Test complete user journeys from authentication through task management
- **Data Isolation**: Verify that users cannot access or modify other users' tasks
- **Performance**: Test response times under various load conditions
- **Cross-Session**: Test multiple browser sessions for proper isolation and synchronization

### Security Tests
- **Authorization**: Test that unauthorized users cannot access protected endpoints
- **User Impersonation**: Verify that users cannot access other users' data
- **Input Sanitization**: Test for injection vulnerabilities and other security flaws
- **JWT Validation**: Test token expiration, invalidation, and manipulation scenarios

This comprehensive specification ensures that the task CRUD functionality is implemented with proper security, validation, error handling, and user experience considerations while maintaining the required multi-user data isolation.