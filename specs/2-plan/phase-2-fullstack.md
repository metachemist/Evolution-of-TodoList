# Phase 2: Full-Stack Application Architecture Plan

## High-Level System Architecture

The Phase 2 architecture follows a modern full-stack approach with clear separation of concerns between frontend, backend, and database layers. Below is an ASCII representation of the system architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Browser/Client                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Next.js App   │  │  React UI Libs  │  │   State Mgmt   │ │
│  │   (Frontend)    │  │ (Tailwind, etc) │  │ (Context/Zustand│ │
│  └─────────────────┘  └─────────────────┘  │    , etc.)     │ │
│         │                       │            └─────────────────┘ │
│         │ HTTP Requests         │                                   │
│         ▼                       ▼                                   │
├─────────────────────────────────────────────────────────────────┤
│                    API Communication Layer                      │
│              (HTTPS, JSON, JWT Authentication)                  │
├─────────────────────────────────────────────────────────────────┤
│                         FastAPI Server                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Authentication │  │   Route/Handler │  │  Request/Resp   │ │
│  │    Service      │  │     Logic       │  │   Processing    │ │
│  │  (Better Auth)  │  │   (CRUD Ops)    │  │   (Pydantic)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│         │                       │                       │         │
│         │ Database Queries      │ Data Modeling         │         │
│         ▼                       ▼                       ▼         │
├─────────────────────────────────────────────────────────────────┤
│                       PostgreSQL Database                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   User Table    │  │   Task Table    │  │  Indexes/Contr. │ │
│  │ (Authentication │  │ (Task CRUD)     │  │  (Performance)  │ │
│  │   , Security)   │  │   , Relations   │  │    , Integrity  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend Components (11+ components)

1. **App Component** - Root application component that sets up routing and global state
   - Responsibility: Entry point, layout structure, global error boundaries

2. **AuthWrapper Component** - Handles authentication state management across the app
   - Responsibility: Checks authentication status, provides auth context

3. **SignUpForm Component** - Registration form with validation
   - Responsibility: User registration, input validation, error handling

4. **SignInForm Component** - Login form with credential validation
   - Responsibility: User authentication, credential validation, session management

5. **AuthGuard Component** - Route protection middleware
   - Responsibility: Verifies authentication before allowing access to protected routes

6. **TaskList Component** - Displays all tasks for the authenticated user
   - Responsibility: Fetches and displays user's tasks, handles filtering/sorting

7. **TaskItem Component** - Represents a single task with interactive features
   - Responsibility: Displays task details, handles completion toggle, edit/delete

8. **TaskForm Component** - Creates and updates tasks
   - Responsibility: Task creation/edit form, validation, submission handling

9. **Header Component** - Application navigation and user controls
   - Responsibility: Navigation menu, user profile, logout functionality

10. **Dashboard Component** - Main application landing page
    - Responsibility: Aggregates task lists, statistics, quick actions

11. **DeleteConfirmDialog Component** - Modal for confirming deletions
    - Responsibility: Confirmation modal with safety warnings

12. **Notification Component** - Global notification system
    - Responsibility: Displays success/error messages to user

### Backend Components

1. **Authentication Service** - User registration, login, JWT handling
   - Responsibility: Password hashing, token generation, user validation

2. **Task Service** - Business logic for task operations
   - Responsibility: CRUD operations, user isolation, data validation

3. **Database Models** - SQLModel definitions for data structures
   - Responsibility: Define schema, relationships, constraints

4. **API Routes** - Endpoint definitions for all operations
   - Responsibility: Handle HTTP requests, return appropriate responses

5. **Middleware** - Authentication, logging, error handling
   - Responsibility: Cross-cutting concerns, request processing pipeline

6. **Configuration** - Environment variables, settings management
   - Responsibility: Manage application configuration and secrets

## Data Flow Diagrams

### User Registration Flow (10+ steps)

1. User navigates to `/signup` page
2. User enters email and password in SignUpForm component
3. Frontend validates input format (email pattern, password strength)
4. Frontend sends POST request to `/api/auth/signup` with user data
5. Backend receives request and validates input parameters
6. Backend checks if email already exists in users table
7. Backend hashes password using bcrypt (cost factor 12)
8. Backend creates new user record in database
9. Backend generates JWT token with user information
10. Backend returns JWT token and user info to frontend
11. Frontend stores JWT token (localStorage/sessionStorage)
12. Frontend redirects user to dashboard/home page

### User Login Flow (9+ steps)

1. User navigates to `/login` page
2. User enters email and password in SignInForm component
3. Frontend validates input presence and format
4. Frontend sends POST request to `/api/auth/signin` with credentials
5. Backend receives request and looks up user by email
6. Backend compares provided password with stored hash using bcrypt
7. Backend generates new JWT token if credentials match
8. Backend returns JWT token and user information
9. Frontend stores JWT token and redirects to dashboard
10. Frontend updates global authentication state

### Task Creation Flow (13+ steps)

1. Authenticated user clicks "Create Task" button
2. TaskForm component opens in create mode
3. User enters task title and optional description
4. Frontend validates input on client-side (length, required fields)
5. Frontend extracts user_id from JWT token in localStorage
6. Frontend sends POST request to `/api/{user_id}/tasks` with task data
7. Backend extracts user_id from JWT token and validates against URL
8. Backend validates task input parameters (title length, description length)
9. Backend inserts new task record with user_id association
10. Backend returns created task object with auto-generated ID
11. Frontend updates local state with new task
12. Frontend shows success notification to user
13. TaskForm component closes and user sees new task in list

### Task List Loading Flow (10+ steps)

1. Authenticated user navigates to dashboard/tasks page
2. TaskList component mounts and begins loading
3. Frontend extracts user_id from JWT token
4. Frontend sends GET request to `/api/{user_id}/tasks`
5. Backend receives request and validates JWT token
6. Backend extracts user_id from token and compares with URL parameter
7. Backend queries tasks table filtered by user_id
8. Backend orders results by created_at (descending)
9. Backend returns array of user's tasks
10. Frontend updates local state with retrieved tasks
11. TaskList component renders tasks in chronological order

### Task Update Flow (13+ steps)

1. User clicks edit button on a task in TaskList
2. TaskItem component transitions to edit mode or opens TaskForm
3. User modifies task title and/or description
4. Frontend validates updated input data
5. Frontend extracts user_id from JWT token
6. Frontend sends PUT request to `/api/{user_id}/tasks/{task_id}`
7. Backend validates JWT token and extracts user_id
8. Backend compares token user_id with URL user_id parameter
9. Backend verifies task belongs to authenticated user
10. Backend updates task record in database with new values
11. Backend updates updated_at timestamp
12. Backend returns updated task object
13. Frontend updates local state and refreshes the task display

### Task Deletion Flow (10+ steps)

1. User clicks delete button on a task in TaskList
2. DeleteConfirmDialog component opens with task details
3. User confirms deletion in confirmation dialog
4. Frontend extracts user_id from JWT token
5. Frontend sends DELETE request to `/api/{user_id}/tasks/{task_id}`
6. Backend validates JWT token and extracts user_id
7. Backend compares token user_id with URL user_id parameter
8. Backend verifies task belongs to authenticated user
9. Backend deletes task record from database
10. Backend returns success confirmation
11. Frontend removes task from local state
12. DeleteConfirmDialog closes and shows success notification

### Task Completion Toggle Flow (9+ steps)

1. User clicks completion checkbox on a task in TaskList
2. TaskItem component handles the toggle event
3. Frontend extracts user_id from JWT token
4. Frontend sends PATCH request to `/api/{user_id}/tasks/{task_id}/complete`
5. Backend validates JWT token and extracts user_id
6. Backend compares token user_id with URL user_id parameter
7. Backend verifies task belongs to authenticated user
8. Backend updates task's completed status and updated_at timestamp
9. Backend returns updated task object
10. Frontend updates local state and visual representation

### Get Current User Flow (7+ steps)

1. Authenticated user requests current user information
2. Frontend extracts JWT token from storage
3. Frontend sends GET request to `/api/auth/me` with Authorization header
4. Backend receives request and validates JWT token
5. Backend extracts user_id from token claims
6. Backend queries user record from database by user_id
7. Backend returns user information (excluding sensitive fields like password)
8. Frontend updates user profile state with retrieved information

### Logout Flow (6+ steps)

1. User clicks logout button/link in the application
2. Frontend extracts JWT token from storage
3. Frontend sends POST request to `/api/auth/signout` with Authorization header
4. Backend validates JWT token and processes logout request
5. Frontend clears JWT token from localStorage/sessionStorage
6. Frontend redirects user to login page and resets authentication state

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

### Additional Indexes for Performance
```sql
-- Composite index for efficient user task queries with completion status
CREATE INDEX idx_tasks_user_completed_created ON tasks(user_id, completed, created_at DESC);

-- Index for searching tasks by title (if search functionality is added later)
CREATE INDEX idx_tasks_title_gin ON tasks USING gin(title gin_trgm_ops);
```

## Deployment Architecture

### Development Environment
- **Frontend**: Next.js development server on port 3000
- **Backend**: FastAPI development server on port 8000
- **Database**: PostgreSQL running locally or in Docker container
- **Environment**: Node.js 18+, Python 3.11+, Docker for containerization

### Production Environment
- **Frontend Hosting**: Vercel with automatic deployments from GitHub
- **Backend Hosting**: Railway or Render with environment variables
- **Database**: Neon Serverless PostgreSQL with connection pooling
- **CDN**: Vercel's built-in CDN for static assets
- **Monitoring**: Built-in platform monitoring for performance metrics

### Environment Configuration
- **Development**: `.env.local` with local database connection
- **Staging**: Platform environment variables with staging database
- **Production**: Platform environment variables with production database
- **Secrets**: BETTER_AUTH_SECRET managed through platform secret management

## Implementation Strategy (8-Day Timeline)

### Day 1: Project Setup and Configuration
- Initialize Next.js project with TypeScript and Tailwind CSS
- Set up FastAPI backend with SQLModel and database connection
- Configure shared BETTER_AUTH_SECRET
- Set up basic project structure and development environment
- Time estimate: 6 hours

### Day 2: Database Models and Authentication Setup
- Implement SQLModel definitions for User and Task models
- Set up database connection and migration system
- Implement JWT authentication with Better Auth
- Create password hashing utilities using bcrypt
- Time estimate: 4 hours

### Day 3: Backend API Implementation (Part 1)
- Implement user registration endpoint
- Implement user login endpoint
- Implement JWT token generation and validation
- Add authentication middleware for protected routes
- Time estimate: 5 hours

### Day 4: Backend API Implementation (Part 2)
- Implement task CRUD endpoints (GET, POST, PUT, DELETE)
- Implement task completion toggle endpoint
- Add user authorization checks for all task operations
- Add comprehensive input validation and error handling
- Time estimate: 5 hours

### Day 5: Frontend Authentication Components
- Create SignUpForm component with validation
- Create SignInForm component with authentication
- Implement AuthGuard for protected routes
- Set up authentication state management
- Time estimate: 6 hours

### Day 6: Frontend Task Components
- Create TaskList component to display user tasks
- Create TaskItem component with interactive features
- Create TaskForm component for task creation/editing
- Implement task completion toggle functionality
- Time estimate: 6 hours

### Day 7: UI Polish and Testing
- Style components with Tailwind CSS
- Implement loading states and error handling
- Create confirmation dialogs for deletions
- Add success/error notifications
- Time estimate: 5 hours

### Day 8: Integration and Deployment
- Integrate frontend and backend components
- Perform end-to-end testing
- Set up deployment configurations
- Deploy to Vercel (frontend) and Railway/Render (backend)
- Time estimate: 4 hours

**Total estimated time: 35 hours**

## Technical Decisions and Rationale

### Framework Choices
- **Next.js 16+ with App Router**: Provides excellent developer experience, SSR capabilities, and optimized production builds
- **FastAPI**: Offers automatic API documentation, type validation, and high performance
- **SQLModel**: Combines SQLAlchemy and Pydantic for unified data modeling
- **PostgreSQL**: Robust, scalable, ACID-compliant database with advanced features

### Authentication Approach
- **JWT Tokens**: Statelessness supports horizontal scaling and microservices architecture
- **bcrypt Hashing**: Industry standard for password security with adjustable cost factor
- **Better Auth**: Provides proven authentication patterns and security best practices

### Security Considerations
- **User Isolation**: Strict validation of user_id in JWT vs URL parameters
- **Input Validation**: Server-side validation for all inputs using Pydantic models
- **SQL Injection Prevention**: Parameterized queries through SQLModel/SQLAlchemy
- **Rate Limiting**: Implementation to prevent brute force attacks

### Performance Considerations
- **Database Indexing**: Strategic indexes on user_id, completion status, and timestamps
- **API Efficiency**: Optimized queries with proper filtering and pagination
- **Caching Strategy**: Potential for Redis caching of frequently accessed data
- **Bundle Optimization**: Next.js automatic code splitting and optimization

## Constraints

### Technical Constraints
- **Stateless Architecture**: No session data stored in memory
- **Database Persistence**: All user state stored in PostgreSQL
- **JWT Tokens**: Authentication without server-side sessions
- **Monorepo Structure**: All code in single repository following spec structure
- **Constitutional Compliance**: Adherence to technology stack requirements (Next.js 16+, FastAPI, SQLModel, PostgreSQL, Better Auth)

### Infrastructure Constraints
- **Vercel Deployment**: Frontend hosted on Vercel platform
- **Railway/Render**: Backend hosted on Railway or Render
- **Neon Serverless**: PostgreSQL database hosted on Neon
- **Shared Secrets**: BETTER_AUTH_SECRET shared between services
- **HTTPS Requirement**: All production traffic encrypted

### Performance Constraints
- **Response Times**: API endpoints should respond within 2 seconds for 95% of requests
- **Page Load Times**: Page load times should be under 3 seconds
- **Concurrent Users**: Support for 100 concurrent users during peak usage
- **Database Query Performance**: All queries must utilize appropriate indexing

### Security Constraints
- **Password Hashing**: All passwords stored with bcrypt hashing (cost factor 12) with automatic salt generation; no other hashing algorithms permitted; password validation must include minimum 8 characters with uppercase, lowercase, numbers, and special characters
- **Token Security**: JWT tokens properly signed with BETTER_AUTH_SECRET using HS256 algorithm and validated on each request; tokens must include exactly user_id (string), email (string), exp (timestamp), iat (timestamp), and iss (string: "todo-app-auth-service") claims as specified in feature spec; token expiration strictly enforced at exactly 3600 seconds from issue with no tolerance; all token validation must complete within 100ms; token validation must reject any tokens with missing or invalid claims
- **Input Validation**: All user inputs validated server-side using Pydantic models with strict type checking regardless of client-side validation; no raw SQL queries permitted, only ORM-based database access; validation must include bounds checking, type validation, and format verification
- **CORS Policy**: Frontend domain properly whitelisted in backend CORS settings for secure cross-origin communication; only HTTPS origins permitted in production environment; wildcard origins prohibited in any environment
- **User Isolation**: Strict validation of user_id in JWT token vs URL parameter with application-level WHERE clause enforcement; database queries must include user_id in WHERE clauses to enforce data boundaries at application level; no user can access another user's data regardless of URL manipulation attempts; user_id validation must occur before any database operations
- **Rate Limiting**: Implementation using in-memory storage with IP-based tracking (max 5 attempts per IP per 15-minute sliding window) to prevent brute force attacks; rate limiting must use sliding window counter algorithm with exact 15-minute windows; blocked IPs must be automatically unblocked after 15 minutes
- **Token Storage**: JWT tokens stored in localStorage with specific XSS protection measures: input sanitization using DOMPurify, output encoding with framework built-ins, CSP headers with 'strict-dynamic' directive; no other storage mechanisms permitted in Phase II
- **Error Handling**: Consistent error responses with generic messages to prevent user enumeration (same "Invalid credentials" for both invalid email and wrong password); error messages must not expose internal system details; all error responses must follow standardized format with success/error flags and appropriate HTTP status codes
- **Shared Secrets**: BETTER_AUTH_SECRET must be identical value across frontend and backend services for JWT validation to work properly; secret must be at least 32 characters and randomly generated; secrets must be stored in environment variables, never in code
- **CSRF Protection**: Secure token storage using double-submit cookie pattern as additional protection layer when using localStorage; implement proper origin validation for all authentication requests
- **Transport Security**: All communications must use HTTPS with HSTS headers set to 31536000 seconds (1 year) in production environment; HTTP connections must be redirected to HTTPS
- **Session Management**: No server-side session storage; all authentication state in JWT tokens only; client-side token storage must be cleared on logout; no persistent session storage mechanisms permitted

## Non-Goals

### Out-of-Scope Architecture
❌ **Advanced Infrastructure**:
- Kubernetes deployment (Phase IV)
- Microservices architecture
- Advanced monitoring and logging
- Scaling strategies beyond basic

❌ **Advanced Features**:
- Offline functionality
- Native mobile applications
- Desktop applications
- Advanced analytics capabilities

❌ **Additional Integrations**:
- Third-party service integrations
- Email notification systems
- Payment processing
- File storage services

❌ **Advanced Security**:
- Certificate-based authentication
- Hardware security modules
- Advanced threat detection
- Zero-trust architecture

## MCP Tool Implementation Architecture

### MCP Tool Layer Design
The MCP tools are implemented as an additional layer that sits between the traditional API endpoints and AI agents. Each MCP tool maps to one or more existing API endpoints but provides a standardized interface optimized for AI consumption.

### Tool-to-API Mapping

**Authentication Tools:**
- `register_user` MCP tool → POST /api/auth/signup endpoint
- `authenticate_user` MCP tool → POST /api/auth/signin endpoint
- `get_current_user` MCP tool → GET /api/auth/me endpoint
- `logout_user` MCP tool → POST /api/auth/signout endpoint

**Task Management Tools:**
- `create_task` MCP tool → POST /api/{user_id}/tasks endpoint
- `get_user_tasks` MCP tool → GET /api/{user_id}/tasks endpoint
- `get_task` MCP tool → GET /api/{user_id}/tasks/{id} endpoint
- `update_task` MCP tool → PUT /api/{user_id}/tasks/{id} endpoint
- `delete_task` MCP tool → DELETE /api/{user_id}/tasks/{id} endpoint
- `toggle_task_completion` MCP tool → PATCH /api/{user_id}/tasks/{id}/complete endpoint

### API Endpoint Data Flows

The following data flows correspond to the API endpoints defined in the feature specification:

**Authentication Flows:**
- **GET /api/auth/me**: Extract JWT token from Authorization header → Validate token signature and expiration → Decode user_id from token → Query user record from database → Return user information excluding sensitive fields (password, internal data)

**Session Management Flows:**
- **POST /api/auth/signout**: Extract JWT token from Authorization header → Validate token → Clear client-side token storage (no server-side session invalidation in stateless approach) → Return success confirmation

### MCP Tool Middleware
Each MCP tool includes standardized middleware that handles:
1. **Input Validation**: Validates JSON schema against tool specification
2. **Authentication**: Extracts and validates JWT token from input
3. **Authorization**: Verifies user_id in token matches requested user_id
4. **Error Wrapping**: Converts API errors to standardized MCP error format
5. **Logging**: Records tool usage for monitoring and debugging
6. **Rate Limiting**: Implements rate limiting to prevent abuse

### MCP Tool Response Format
All MCP tools follow a standardized response format:
```json
{
  "success": true,
  "data": { /* tool-specific response data */ },
  "metadata": {
    "tool_name": "tool-name",
    "timestamp": "ISO 8601 timestamp",
    "execution_time_ms": 123
  }
}
```

For errors:
```json
{
  "success": false,
  "error": {
    "type": "VALIDATION_ERROR | AUTHENTICATION_ERROR | AUTHORIZATION_ERROR | SERVER_ERROR",
    "message": "Human-readable error message",
    "code": "TOOL_ERROR_CODE",
    "details": { /* optional error details */ }
  },
  "metadata": {
    "tool_name": "tool-name",
    "timestamp": "ISO 86001 timestamp"
  }
}
```

## MCP Architecture Principles Implementation

### Statelessness
- All MCP tools follow stateless design (per Constitution 489-490)
- Tools read/write to database, not memory
- No session state maintained between tool calls
- JWT tokens used for authentication without server-side sessions

### Clear Contracts
- All MCP tools have well-defined JSON schemas (per Constitution 491)
- Input/output specifications are machine-readable
- Validation occurs before processing
- Consistent response formats across all tools

### Error Handling
- All MCP tools return structured error objects (per Constitution 492)
- Errors include appropriate HTTP status mappings
- Technical details logged server-side, user-friendly messages returned
- Error types categorized consistently across tools

### Composability
- MCP tools designed for chaining by AI agents (per Constitution 493)
- Each tool performs single, well-defined operation
- Tools can be combined for complex operations
- Consistent authentication across all tools

## Integration with Feature Specification

### Alignment with Feature Requirements
This architectural plan directly implements the requirements specified in the feature specification:
- **User Journeys**: All user journeys described in @specs/1-specify/user-journeys/journey-01-basic-todo.md, @specs/1-specify/user-journeys/journey-02-ai-chat.md, and @specs/1-specify/user-journeys/journey-03-advanced-features.md are implemented through the architectural components and data flows outlined in this plan
- **Authentication Requirements**: All authentication flows (registration, login, logout) align with the detailed user stories and functional requirements in @specs/1-specify/features/feature-02-fullstack-todo.md
- **Task Management**: All CRUD operations and user authorization requirements map to the architectural components and data flows outlined in this plan
- **Security Requirements**: Implementation follows the detailed security requirements including JWT token management, password hashing, rate limiting, and user isolation
- **API Endpoints**: All endpoints specified in the feature spec are implemented according to the architectural patterns described here
- **MCP Tools**: The 7 MCP tools specified in the feature spec are implemented using the architectural patterns and middleware described in this plan
- **Domain Entities**: Implementation respects the domain entity definitions in @specs/1-specify/domain/user-entity.md, @specs/1-specify/domain/task-entity.md, and @specs/1-specify/domain/conversation-entity.md
- **Token Management**: Specifically aligned with feature spec constraints - no token refresh mechanism in Phase II; users must re-authenticate after 1-hour expiration; refresh functionality reserved for future phases

### Error Handling Integration
- **Missing BETTER_AUTH_SECRET**: Both frontend and backend services will log configuration errors and return appropriate 500 responses as specified in feature spec
- **Database Connection Failures**: Retry logic with exponential backoff is implemented as specified in feature spec error handling section
- **JWT Validation Failures**: Consistent 401 responses for all token validation errors as specified in feature spec
- **User Account Deletion**: Existing tokens remain valid until expiration as specified in feature spec assumptions

### Component-to-Requirement Mapping
- **AuthWrapper Component** → Implements authentication state management requirements from feature spec
- **SignUpForm/SignInForm Components** → Implement user registration/login requirements from feature spec
- **AuthGuard Component** → Implements protected route requirements from feature spec
- **TaskList/TaskItem/TaskForm Components** → Implement task management requirements from feature spec
- **Authentication Service** → Implements JWT token management and user validation from feature spec
- **Task Service** → Implements user isolation and data validation requirements from feature spec

## Testing Strategy

### Backend Testing
- **Unit Tests**: Test individual functions, authentication logic, and validation
- **MCP Tool Tests**: Test all MCP tools with various input combinations
- **Integration Tests**: Test API endpoints with real database connections
- **Security Tests**: Verify authentication, authorization, and data isolation
- **Performance Tests**: Benchmark API endpoints under load

### Frontend Testing
- **Component Tests**: Test UI components with Jest and React Testing Library
- **Integration Tests**: Test component interactions and state management
- **End-to-End Tests**: Simulate user flows using Playwright or Cypress
- **MCP Integration Tests**: Test MCP tool accessibility for AI agents
- **Accessibility Tests**: Verify accessibility compliance

### Test Coverage Goals
- **Backend**: Minimum 80% coverage for business logic
- **MCP Tools**: 100% coverage for all tool inputs and error cases
- **Frontend**: Minimum 70% coverage for components
- **Critical Paths**: 100% coverage for authentication and authorization
- **API Tests**: Automated testing of all endpoints with various inputs

This architectural plan provides a comprehensive roadmap for implementing a secure, scalable, and maintainable full-stack todo application with proper authentication and user data isolation. The MCP tool layer ensures AI agents can interact with the application using standardized protocols as mandated by the Constitution.