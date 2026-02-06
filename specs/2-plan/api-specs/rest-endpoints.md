# REST API Endpoints Specification

## Base URLs

### Development Environment
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Base Path**: http://localhost:8000/api

### Production Environment
- **Frontend**: https://your-app.vercel.app (or custom domain)
- **Backend API**: https://your-backend.onrender.com (or railway.app)
- **API Base Path**: https://your-backend.onrender.com/api (or .railway.app)

## Authentication Header Format

All authenticated endpoints require the following header:

```
Authorization: Bearer <jwt_token_here>
```

Where `<jwt_token_here>` is a valid JWT token obtained from the authentication endpoints.

## Response Format Standards

### Success Response Format
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional success message"
}
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Optional detailed information"
  }
}
```

## Status Code Reference Table

| Status Code | Meaning | Usage |
|-------------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH requests |
| 201 | Created | Successful POST request |
| 204 | No Content | Successful DELETE request |
| 400 | Bad Request | Invalid request parameters or malformed JSON |
| 401 | Unauthorized | Invalid or missing authentication token |
| 403 | Forbidden | Valid token but insufficient permissions |
| 404 | Not Found | Requested resource does not exist |
| 409 | Conflict | Resource conflict (e.g., email already registered) |
| 422 | Unprocessable Entity | Validation errors in request data |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side processing error |

## Authentication Endpoints

### POST /api/auth/signup

**Description**: Register a new user account with email and password.

**Authentication Required**: No

**Request Parameters**: None

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Field Validation**:
- `email`: Required, valid email format, max 255 characters
- `password`: Required, minimum 8 characters with uppercase, lowercase, numbers, and special characters

**Successful Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_abc123xyz",
      "email": "user@example.com",
      "created_at": "2023-01-01T10:00:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "User registered successfully"
}
```

**Error Responses**:
- **400 Bad Request**: Invalid email format or weak password
- **409 Conflict**: Email already exists
- **500 Internal Server Error**: Registration failed due to server error

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "SecurePassword123!"
  }'
```

### POST /api/auth/signin

**Description**: Authenticate user with email and password to obtain JWT token.

**Authentication Required**: No

**Request Parameters**: None

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Field Validation**:
- `email`: Required, valid email format
- `password`: Required

**Successful Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_abc123xyz",
      "email": "user@example.com",
      "created_at": "2023-01-01T10:00:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "User authenticated successfully"
}
```

**Error Responses**:
- **400 Bad Request**: Invalid email format
- **401 Unauthorized**: Invalid email or password
- **500 Internal Server Error**: Login failed due to server error

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "existinguser@example.com",
    "password": "SecurePassword123!"
  }'
```

### GET /api/auth/me

**Description**: Retrieve current authenticated user information.

**Authentication Required**: Yes (Bearer token)

**Request Parameters**: None

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Successful Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": "user_abc123xyz",
    "email": "user@example.com",
    "created_at": "2023-01-01T10:00:00Z"
  },
  "message": "User information retrieved successfully"
}
```

**Error Responses**:
- **401 Unauthorized**: Invalid or expired token
- **500 Internal Server Error**: Failed to retrieve user information

**cURL Example**:
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### POST /api/auth/signout

**Description**: Invalidate the current user session (logout).

**Authentication Required**: Yes (Bearer token)

**Request Parameters**: None

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body**: Empty or `{}`

**Successful Response (200 OK)**:
```json
{
  "success": true,
  "message": "User logged out successfully"
}
```

**Error Responses**:
- **401 Unauthorized**: Invalid or expired token
- **500 Internal Server Error**: Logout failed due to server error

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/auth/signout \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Task Endpoints

### GET /api/{user_id}/tasks

**Description**: Retrieve all tasks for the specified user, filtered by the authenticated user's identity.

**Authentication Required**: Yes (Bearer token)

**Path Parameters**:
- `user_id` (string): The ID of the user whose tasks to retrieve

**Query Parameters**:
- `limit` (integer, optional): Number of tasks to return per page (default: 20, max: 100)
- `offset` (integer, optional): Number of tasks to skip (for pagination, default: 0)
- `completed` (boolean, optional): Filter by completion status (true/false/all)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Successful Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 123,
        "user_id": "user_abc123xyz",
        "title": "Complete project proposal",
        "description": "Finish the project proposal document",
        "completed": false,
        "created_at": "2023-01-01T10:00:00Z",
        "updated_at": "2023-01-01T10:00:00Z"
      },
      {
        "id": 124,
        "user_id": "user_abc123xyz",
        "title": "Review quarterly reports",
        "description": "",
        "completed": true,
        "created_at": "2023-01-02T15:30:00Z",
        "updated_at": "2023-01-02T16:45:00Z"
      }
    ],
    "pagination": {
      "total": 25,
      "limit": 20,
      "offset": 0,
      "has_more": true
    }
  },
  "message": "Tasks retrieved successfully"
}
```

**Error Responses**:
- **400 Bad Request**: Invalid query parameters
- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: User ID in token doesn't match the requested user ID
- **500 Internal Server Error**: Failed to retrieve tasks due to server error

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/user_abc123xyz/tasks?limit=10&offset=0" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### GET /api/{user_id}/tasks/{id}

**Description**: Retrieve a specific task by ID for the specified user.

**Authentication Required**: Yes (Bearer token)

**Path Parameters**:
- `user_id` (string): The ID of the user who owns the task
- `id` (integer): The ID of the task to retrieve

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Successful Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": "user_abc123xyz",
    "title": "Complete project proposal",
    "description": "Finish the project proposal document",
    "completed": false,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  },
  "message": "Task retrieved successfully"
}
```

**Error Responses**:
- **400 Bad Request**: Invalid task ID format
- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: User ID in token doesn't match the requested user ID
- **404 Not Found**: Task with the specified ID doesn't exist
- **500 Internal Server Error**: Failed to retrieve task due to server error

**cURL Example**:
```bash
curl -X GET http://localhost:8000/api/user_abc123xyz/tasks/123 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### POST /api/{user_id}/tasks

**Description**: Create a new task for the specified user.

**Authentication Required**: Yes (Bearer token)

**Path Parameters**:
- `user_id` (string): The ID of the user creating the task

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional task description"
}
```

**Field Validation**:
- `title`: Required, 1-200 characters after trimming whitespace
- `description`: Optional, 0-1000 characters

**Successful Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": 125,
    "user_id": "user_abc123xyz",
    "title": "New task title",
    "description": "Optional task description",
    "completed": false,
    "created_at": "2023-01-03T12:00:00Z",
    "updated_at": "2023-01-03T12:00:00Z"
  },
  "message": "Task created successfully"
}
```

**Error Responses**:
- **400 Bad Request**: Invalid input data or missing required fields
- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: User ID in token doesn't match the requested user ID
- **500 Internal Server Error**: Failed to create task due to server error

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/user_abc123xyz/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Prepare presentation slides",
    "description": "Create slides for the upcoming meeting"
  }'
```

### PUT /api/{user_id}/tasks/{id}

**Description**: Update an existing task for the specified user.

**Authentication Required**: Yes (Bearer token)

**Path Parameters**:
- `user_id` (string): The ID of the user who owns the task
- `id` (integer): The ID of the task to update

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": false
}
```

**Field Validation**:
- `title`: Optional, if provided must be 1-200 characters after trimming
- `description`: Optional, if provided must be 0-1000 characters
- `completed`: Optional, boolean value

**Successful Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": "user_abc123xyz",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": false,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-03T14:30:00Z"
  },
  "message": "Task updated successfully"
}
```

**Error Responses**:
- **400 Bad Request**: Invalid input data or ID format
- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: User ID in token doesn't match the requested user ID
- **404 Not Found**: Task with the specified ID doesn't exist
- **500 Internal Server Error**: Failed to update task due to server error

**cURL Example**:
```bash
curl -X PUT http://localhost:8000/api/user_abc123xyz/tasks/123 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true
  }'
```

### DELETE /api/{user_id}/tasks/{id}

**Description**: Delete a specific task for the specified user.

**Authentication Required**: Yes (Bearer token)

**Path Parameters**:
- `user_id` (string): The ID of the user who owns the task
- `id` (integer): The ID of the task to delete

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Successful Response (200 OK)**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- **400 Bad Request**: Invalid task ID format
- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: User ID in token doesn't match the requested user ID
- **404 Not Found**: Task with the specified ID doesn't exist
- **500 Internal Server Error**: Failed to delete task due to server error

**cURL Example**:
```bash
curl -X DELETE http://localhost:8000/api/user_abc123xyz/tasks/123 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### PATCH /api/{user_id}/tasks/{id}/complete

**Description**: Toggle or set the completion status of a specific task for the specified user.

**Authentication Required**: Yes (Bearer token)

**Path Parameters**:
- `user_id` (string): The ID of the user who owns the task
- `id` (integer): The ID of the task to update

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body**:
```json
{
  "completed": true
}
```

**Field Validation**:
- `completed`: Required, boolean value (true/false)

**Successful Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": "user_abc123xyz",
    "title": "Complete project proposal",
    "description": "Finish the project proposal document",
    "completed": true,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-03T15:45:00Z"
  },
  "message": "Task completion status updated successfully"
}
```

**Error Responses**:
- **400 Bad Request**: Invalid task ID format or invalid completed value
- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: User ID in token doesn't match the requested user ID
- **404 Not Found**: Task with the specified ID doesn't exist
- **500 Internal Server Error**: Failed to update task completion status due to server error

**cURL Example**:
```bash
curl -X PATCH http://localhost:8000/api/user_abc123xyz/tasks/123/complete \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## CORS Configuration Details

### Allowed Origins
- **Development**: http://localhost:3000 (Next.js dev server)
- **Production**: Your production domain (e.g., https://your-app.vercel.app)

### Allowed Methods
- GET, POST, PUT, PATCH, DELETE

### Allowed Headers
- Content-Type
- Authorization
- X-Requested-With
- Accept
- Origin

### Credentials
- Credentials allowed in development and production environments
- Cookie/session support enabled

## Error Handling Best Practices

### Client-Side Error Handling
1. Always check the `success` field in API responses
2. Display user-friendly messages from the `error.message` field
3. Log technical details (like error codes) for debugging only
4. Implement retry logic for 5xx errors with exponential backoff
5. Redirect to login page for 401 errors

### Server-Side Error Handling
1. Return appropriate HTTP status codes for different error types
2. Include descriptive error messages without exposing system details
3. Log server-side errors with correlation IDs for debugging
4. Implement rate limiting to prevent abuse
5. Sanitize and validate all inputs before processing

## Constraints

### Technical Constraints
- **Payload Size Limits**: Request payloads must not exceed 10KB per request to prevent resource exhaustion
- **Rate Limiting**: Maximum 100 requests per minute per IP address to prevent abuse and brute force attacks
- **Authentication Headers**: All authenticated endpoints require `Authorization: Bearer <token>` header with valid JWT
- **Content Type**: All POST/PUT/PATCH requests must use `application/json` content type with proper validation
- **URL Length**: GET request URLs must not exceed 2048 characters to ensure compatibility across clients
- **API Versioning**: No versioning in Phase II (all endpoints use current version structure)
- **Parameter Validation**: All URL and query parameters must be validated for type and format
- **JSON Schema Compliance**: All requests must conform to specified JSON schemas with proper validation
- **Character Encoding**: All requests/responses use UTF-8 encoding exclusively
- **HTTP Method Compliance**: Strict adherence to HTTP method semantics (GET for retrieval, POST for creation, etc.)

### Performance Constraints
- **Response Times**: 95% of API requests must respond within 2 seconds for optimal user experience
- **Concurrent Connections**: System must support 1000 concurrent connections for scalability
- **Database Query Time**: Individual database queries must complete within 500ms for performance
- **Token Validation**: JWT validation must complete within 100ms to maintain responsiveness
- **Page Load Performance**: API calls should not exceed 2-second response time for frontend rendering
- **Throughput Requirements**: System must handle 10 requests per second sustained load during peak usage
- **Cold Start Mitigation**: Serverless functions should minimize cold start impact on response times

### Data Constraints
- **Pagination Limits**: Maximum 100 items per page for GET requests (default 20) to prevent resource overload
- **Field Lengths**: Task titles 1-200 characters after trimming, descriptions 0-1000 characters as specified
- **Identifier Formats**: User IDs must be valid UUID format, task IDs must be positive integers
- **Request Frequency**: No more than 10 identical requests per 30-second window per user to prevent spam
- **Data Integrity**: All database operations must maintain referential integrity and constraints
- **Input Validation**: All inputs must be validated server-side regardless of client-side validation
- **Special Characters**: All text fields must sanitize or properly encode special characters to prevent injection
- **Timestamp Format**: All timestamps must use ISO 8601 format in UTC timezone

### Security Constraints
- **Token Validation**: All JWT tokens must be validated for signature, expiration, and issuer before processing requests
- **User Isolation**: Strict validation that user_id in JWT matches user_id in URL parameter for all operations
- **Injection Prevention**: All inputs must be parameterized to prevent SQL injection and other attacks
- **Information Disclosure**: Error messages must not reveal system internals or sensitive information
- **Authentication Enforcement**: All protected endpoints must validate JWT token presence and validity
- **Rate Limiting Implementation**: Proper implementation to prevent brute force and DoS attacks
- **CORS Policy**: Proper configuration to allow only authorized origins and prevent cross-site attacks
- **Data Privacy**: No sensitive information should be logged or exposed in API responses

### Environmental Constraints
- **HTTPS Requirement**: All production API communication must use HTTPS (no HTTP allowed)
- **Domain Restrictions**: API endpoints must only accept requests from authorized frontend domains
- **Infrastructure Limits**: Must operate within free tier limits of Vercel, Railway/Render, and Neon
- **Deployment Constraints**: Frontend on Vercel, Backend on Railway/Render, Database on Neon Serverless
- **Secret Management**: BETTER_AUTH_SECRET must be stored as environment variable, not in code

### Operational Constraints
- **Backward Compatibility**: API endpoints must maintain backward compatibility within Phase II
- **Error Consistency**: All endpoints must return consistent error response formats as specified
- **Logging Requirements**: All API requests must be logged for monitoring and debugging purposes
- **Monitoring**: Basic performance and error monitoring must be implemented for production
- **Session Management**: Stateless operation with JWT tokens (no server-side session storage)
- **Data Consistency**: All CRUD operations must be atomic (all-or-nothing) with proper transaction handling

## Non-Goals

### Out-of-Scope API Features
❌ **Advanced API Features**:
- GraphQL endpoint support
- WebSocket real-time updates
- Server-Sent Events (SSE) streaming
- Batch operations API
- File upload/download endpoints

❌ **Advanced Authentication**:
- API key authentication
- OAuth 2.0 flows
- Third-party authentication tokens
- Session-based authentication
- Certificate-based authentication

❌ **Complex Querying**:
- Advanced filtering beyond basic parameters
- Full-text search capabilities
- Complex join operations across entities
- Analytics aggregation endpoints
- Reporting endpoints

❌ **External Integrations**:
- Third-party webhook systems
- External service callbacks
- Payment processing APIs
- Email/SMS notification APIs
- Social media integration

## Testing with cURL

### Complete Registration and Task Management Flow Example

1. **Register a new user**:
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"SecurePassword123!"}' | \
  jq -r '.data.token')

echo "Registered token: $TOKEN"
```

2. **Create a task**:
```bash
TASK_ID=$(curl -s -X POST http://localhost:8000/api/user_abc123/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"This is a test task"}' | \
  jq -r '.data.id')

echo "Created task with ID: $TASK_ID"
```

3. **Retrieve all tasks**:
```bash
curl -X GET http://localhost:8000/api/user_abc123/tasks \
  -H "Authorization: Bearer $TOKEN"
```

4. **Update a task**:
```bash
curl -X PUT http://localhost:8000/api/user_abc123/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated test task","completed":true}'
```

5. **Mark task as complete**:
```bash
curl -X PATCH http://localhost:8000/api/user_abc123/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

6. **Delete a task**:
```bash
curl -X DELETE http://localhost:8000/api/user_abc123/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN"
```

7. **Logout**:
```bash
curl -X POST http://localhost:8000/api/auth/signout \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## MCP Tool Endpoints

### MCP Tool Base Path
All MCP tools are accessible via the `/mcp/tools/` endpoint prefix.

### Authentication MCP Tools

#### POST /mcp/tools/register_user
**Description**: MCP tool for registering a new user account.

**Authentication Required**: No

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_abc123xyz",
      "email": "user@example.com",
      "created_at": "2023-01-01T10:00:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "metadata": {
    "tool_name": "register_user",
    "timestamp": "2023-01-01T10:00:00Z",
    "execution_time_ms": 150
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": {
    "type": "VALIDATION_ERROR",
    "message": "Invalid email format. Please provide a valid email address.",
    "code": "INVALID_EMAIL_FORMAT",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  },
  "metadata": {
    "tool_name": "register_user",
    "timestamp": "2023-01-01T10:00:00Z"
  }
}
```

### POST /mcp/tools/authenticate_user

**Description**: MCP tool for authenticating user credentials.

**Authentication Required**: No

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_abc123xyz",
      "email": "user@example.com",
      "created_at": "2023-01-01T10:00:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "metadata": {
    "tool_name": "authenticate_user",
    "timestamp": "2023-01-01T10:00:00Z",
    "execution_time_ms": 120
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": {
    "type": "AUTHENTICATION_ERROR",
    "message": "Invalid credentials. Please check your email and password.",
    "code": "INVALID_CREDENTIALS",
    "details": null
  },
  "metadata": {
    "tool_name": "authenticate_user",
    "timestamp": "2023-01-01T10:00:00Z"
  }
}
```

### POST /mcp/tools/get_current_user

**Description**: MCP tool for retrieving current authenticated user information.

**Authentication Required**: Yes (Bearer token in request body)

**Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": "user_abc123xyz",
    "email": "user@example.com",
    "created_at": "2023-01-01T10:00:00Z"
  },
  "metadata": {
    "tool_name": "get_current_user",
    "timestamp": "2023-01-01T10:00:00Z",
    "execution_time_ms": 80
  }
}
```

### Task Management MCP Tools

#### POST /mcp/tools/create_task

**Description**: MCP tool for creating a new task for the authenticated user.

**Authentication Required**: Yes (JWT token in request body)

**Request Body**:
```json
{
  "user_id": "user_abc123xyz",
  "title": "New task title",
  "description": "Optional task description"
}
```

**Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": 125,
    "user_id": "user_abc123xyz",
    "title": "New task title",
    "description": "Optional task description",
    "completed": false,
    "created_at": "2023-01-03T12:00:00Z",
    "updated_at": "2023-01-03T12:00:00Z"
  },
  "metadata": {
    "tool_name": "create_task",
    "timestamp": "2023-01-03T12:00:00Z",
    "execution_time_ms": 90
  }
}
```

#### POST /mcp/tools/get_user_tasks

**Description**: MCP tool for retrieving all tasks for the specified user.

**Authentication Required**: Yes (JWT token in request body)

**Request Body**:
```json
{
  "user_id": "user_abc123xyz",
  "limit": 20,
  "offset": 0,
  "completed": null
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 123,
        "user_id": "user_abc123xyz",
        "title": "Complete project proposal",
        "description": "Finish the project proposal document",
        "completed": false,
        "created_at": "2023-01-01T10:00:00Z",
        "updated_at": "2023-01-01T10:00:00Z"
      }
    ],
    "pagination": {
      "total": 25,
      "limit": 20,
      "offset": 0,
      "has_more": true
    }
  },
  "metadata": {
    "tool_name": "get_user_tasks",
    "timestamp": "2023-01-03T12:00:00Z",
    "execution_time_ms": 110
  }
}
```

#### POST /mcp/tools/update_task

**Description**: MCP tool for updating an existing task for the authenticated user.

**Authentication Required**: Yes (JWT token in request body)

**Request Body**:
```json
{
  "user_id": "user_abc123xyz",
  "task_id": 123,
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

#### POST /mcp/tools/delete_task

**Description**: MCP tool for deleting a specific task for the authenticated user.

**Authentication Required**: Yes (JWT token in request body)

**Request Body**:
```json
{
  "user_id": "user_abc123xyz",
  "task_id": 123
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  },
  "metadata": {
    "tool_name": "delete_task",
    "timestamp": "2023-01-03T12:00:00Z",
    "execution_time_ms": 75
  }
}
```

#### POST /mcp/tools/toggle_task_completion

**Description**: MCP tool for toggling or setting the completion status of a task.

**Authentication Required**: Yes (JWT token in request body)

**Request Body**:
```json
{
  "user_id": "user_abc123xyz",
  "task_id": 123,
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": "user_abc123xyz",
    "title": "Complete project proposal",
    "description": "Finish the project proposal document",
    "completed": true,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-03T15:45:00Z"
  },
  "metadata": {
    "tool_name": "toggle_task_completion",
    "timestamp": "2023-01-03T15:45:00Z",
    "execution_time_ms": 85
  }
}
```

## MCP Architecture Compliance

### Statelessness
All MCP tools comply with constitutional requirement for stateless services:
- No session data stored in memory (per Constitution 407)
- All state stored in PostgreSQL database
- JWT tokens used for authentication without server-side sessions
- Tools read/write to database, not memory (per Constitution 489)

### Clear Contracts
All MCP tools follow constitutional requirements for clear contracts:
- Well-defined JSON schemas for all inputs and outputs (per Constitution 491)
- Consistent response formats across all tools
- Proper validation of all inputs before processing
- Machine-readable specifications for AI agent consumption

### Error Handling
All MCP tools implement constitutional requirements for error handling:
- Structured error objects returned instead of exceptions (per Constitution 492)
- Appropriate HTTP status code mappings
- User-friendly messages that don't expose system internals
- Comprehensive error logging for debugging while protecting user privacy

### Composability
All MCP tools support constitutional requirements for composability:
- Designed to be chained by AI agents (per Constitution 493)
- Each tool performs a single, well-defined operation
- Consistent authentication and authorization patterns across all tools
- Inputs and outputs designed for easy composition in complex workflows

### MCP Tool Usage Examples

#### Complete MCP Registration and Task Management Flow

1. **Register a user via MCP tool**:
```bash
MCP_RESPONSE=$(curl -s -X POST http://localhost:8000/mcp/tools/register_user \
  -H "Content-Type: application/json" \
  -d '{"email":"mcpuser@example.com","password":"SecurePassword123!"}')

TOKEN=$(echo $MCP_RESPONSE | jq -r '.data.token')
USER_ID=$(echo $MCP_RESPONSE | jq -r '.data.user.id')

echo "MCP registration response: $MCP_RESPONSE"
```

2. **Create a task via MCP tool**:
```bash
TASK_RESPONSE=$(curl -s -X POST http://localhost:8000/mcp/tools/create_task \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"$USER_ID\",\"title\":\"MCP-created task\",\"description\":\"Created via MCP tool\"}")

TASK_ID=$(echo $TASK_RESPONSE | jq -r '.data.id')

echo "Created task via MCP: $TASK_RESPONSE"
```

3. **Get user tasks via MCP tool**:
```bash
curl -X POST http://localhost:8000/mcp/tools/get_user_tasks \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"$USER_ID\",\"limit\":10,\"offset\":0}"
```

This comprehensive API specification provides clear guidelines for implementing and consuming both traditional REST API endpoints and MCP tools for the todo application with proper authentication and error handling. The MCP tools enable AI agents to interact with the application using standardized protocols as mandated by the Constitution.