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

### Frontend Components (12+ components)

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

13. **LoadingSpinner Component** - Visual indicator for loading states
    - Responsibility: Shows loading states during API operations

### Backend Components

1. **Authentication Service** - User registration, login, JWT handling
   - Responsibility: Password hashing, token generation, user validation

2. **Task Service** - Business logic for task operations
   - Responsibility: CRUD operations, user isolation, data validation

3. **Database Models** - SQLModel definitions for data structures
   - Responsibility: Define schema, relationships, constraints

4. **API Routes** - Endpoint definitions for all operations
   - Responsibility: Handle HTTP requests, return appropriate responses

5. **MCP Tools** - Standardized interfaces for AI agents
   - Responsibility: Provide standardized access to application functionality for AI agents

6. **Middleware** - Authentication, logging, error handling
   - Responsibility: Cross-cutting concerns, request processing pipeline

7. **Configuration** - Environment variables, settings management
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

### Day 1: Project Setup and Environment Configuration
- Initialize Next.js project with TypeScript and Tailwind CSS
- Set up FastAPI backend with SQLModel and database connection
- Configure shared BETTER_AUTH_SECRET
- Set up basic project structure and development environment
- **Environment Setup Clarity**:
  - Install Node.js 18+ and Python 3.11+ with proper version management
  - Set up virtual environment for Python dependencies (using uv or pipenv)
  - Install required packages: Next.js, TypeScript, Tailwind CSS, FastAPI, SQLModel, PostgreSQL drivers
  - Configure development environment with proper .env files for both frontend and backend
  - Set up shared BETTER_AUTH_SECRET across both services
  - Establish consistent code formatting with ESLint, Prettier, and Black
- **API Contract Definition**:
  - Define initial API specification document outlining authentication and task endpoints
  - Create shared TypeScript interfaces for API responses (to be used by frontend)
  - Document expected request/response formats for all endpoints
- **Initial Testing Setup**:
  - Configure testing frameworks (Jest for frontend, pytest for backend)
  - Set up basic unit test structure for both services
  - Create initial smoke tests for API endpoints
- Time estimate: 6 hours

### Day 2: Database Models and Authentication Setup
- Implement SQLModel definitions for User and Task models
- Set up database connection and migration system
- Implement JWT authentication with Better Auth
- Create password hashing utilities using bcrypt
- **Integrated Testing**:
  - Write unit tests for password hashing utilities
  - Create model validation tests for User and Task entities
  - Test database connection and migration setup
- Time estimate: 4 hours

### Day 3: Backend API Implementation (Part 1)
- Implement user registration endpoint
- Implement user login endpoint
- Implement JWT token generation and validation
- Add authentication middleware for protected routes
- **API Contract Emphasis**:
  - Finalize authentication API contracts with exact request/response schemas
  - Document error response formats consistently
  - Create API documentation for frontend team to reference
- **Integrated Testing**:
  - Write unit tests for authentication functions
  - Create integration tests for registration and login endpoints
  - Test JWT token generation and validation
- **Parallel Development Preparation**:
  - Provide frontend team with API contract documentation
  - Mock endpoints if needed for frontend development to proceed in parallel
- Time estimate: 5 hours

### Day 4: Backend API Implementation (Part 2)
- Implement task CRUD endpoints (GET, POST, PUT, DELETE)
- Implement task completion toggle endpoint
- Add user authorization checks for all task operations
- Add comprehensive input validation and error handling
- **API Contract Emphasis**:
  - Finalize task management API contracts with exact request/response schemas
  - Document all possible error scenarios and responses
  - Ensure consistent response formats across all endpoints
- **Integrated Testing**:
  - Write unit tests for all CRUD operations
  - Create integration tests for task endpoints
  - Test user authorization and data isolation
- **Parallel Development Preparation**:
  - Provide updated API documentation to frontend team
  - Ensure endpoints are fully functional for frontend integration
- Time estimate: 5 hours

### Day 5: Frontend Authentication Components
- Create SignUpForm component with validation
- Create SignInForm component with authentication
- Implement AuthGuard for protected routes
- Set up authentication state management
- **API Contract Implementation**:
  - Implement frontend API clients based on defined contracts
  - Create authentication service to handle API interactions
  - Implement proper error handling based on API specifications
- **Integrated Testing**:
  - Write component tests for authentication forms
  - Test authentication state management
  - Create integration tests for API interactions
- **Parallel Development Coordination**:
  - Coordinate with backend team for any API adjustments
  - Ensure API contracts are being properly implemented
- Time estimate: 6 hours

### Day 6: Frontend Task Components
- Create TaskList component to display user tasks
- Create TaskItem component with interactive features
- Create TaskForm component for task creation/editing
- Implement task completion toggle functionality
- **API Contract Implementation**:
  - Implement task management API clients based on defined contracts
  - Create task service to handle API interactions
  - Ensure all API calls follow established contracts
- **Integrated Testing**:
  - Write component tests for all task components
  - Test API interactions and error handling
  - Create integration tests for complete user flows
- **Parallel Development Coordination**:
  - Verify all API endpoints are working as expected
  - Address any discrepancies between contract and implementation
- Time estimate: 6 hours

### Day 7: UI Polish and Integrated Testing
- Style components with Tailwind CSS
- Implement loading states and error handling
- Create confirmation dialogs for deletions
- Add success/error notifications
- **Comprehensive Testing**:
  - Perform end-to-end testing of authentication flows
  - Test complete task management workflows
  - Conduct security testing for user isolation
  - Run all unit and integration tests
- **API Contract Verification**:
  - Verify all API interactions follow established contracts
  - Ensure consistent error handling across frontend and backend
- Time estimate: 5 hours

### Day 8: MCP Tools and Deployment
- Implement MCP tool infrastructure and middleware
- Create MCP tool wrappers for all authentication endpoints
- Create MCP tool wrappers for all task management endpoints
- Integrate frontend and backend components
- Perform end-to-end testing
- Set up deployment configurations
- Deploy to Vercel (frontend) and Railway/Render (backend)
- **Final Testing and Verification**:
  - Test MCP tools functionality with AI agent interactions
  - Verify all API contracts work correctly in deployed environment
  - Conduct final security and performance testing
- **Documentation and Handoff**:
  - Complete API documentation for future development
  - Document deployment process and environment configurations
  - Ensure all team members understand the API contracts
- Time estimate: 4 hours

**Total estimated time: 35 hours**

## Parallel Development Strategy

### Frontend and Backend Coordination
- **Day 1**: Both teams work on environment setup and initial configuration
- **Days 2-4**: Backend team focuses on API development while frontend team can begin with authentication components using mock data
- **Days 5-6**: Frontend team integrates with backend APIs as they become available
- **Throughout**: Regular synchronization meetings to ensure API contracts are properly implemented

### API Contract Management
- **Definition Phase**: Clear specification of request/response formats before implementation
- **Documentation**: Living documentation updated as APIs evolve
- **Validation**: Both frontend and backend validate against contracts
- **Testing**: Contract testing to ensure compatibility between services

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
- **Security Headers**: Implementation of proper security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Strict-Transport-Security)
- **CORS Policy**: Proper configuration to allow only authorized origins and prevent cross-site attacks
- **CSRF Protection**: Secure token storage using double-submit cookie pattern or proper origin validation when using localStorage
- **Input Sanitization**: Implementation of input sanitization using DOMPurify and output encoding with framework built-ins
- **CSP Headers**: Implementation of Content Security Policy headers with 'strict-dynamic' directive

### Performance Considerations
- **Database Indexing**: Strategic indexes on user_id, completion status, and timestamps
- **API Efficiency**: Optimized queries with proper filtering and pagination
- **Caching Strategy**: Potential for Redis caching of frequently accessed data
- **Bundle Optimization**: Next.js automatic code splitting and optimization
- **Token Validation Performance**: JWT validation must complete within 100ms to maintain responsiveness
- **Database Query Performance**: Individual database queries must complete within 500ms for performance
- **Response Time Targets**: 95% of API requests must respond within 2 seconds for optimal user experience
- **Concurrent Connection Handling**: System must support 1000 concurrent connections for scalability

### API Contract Details
- **Endpoint Structure**: RESTful endpoints following the pattern `/api/{user_id}/{resource}` for user-specific resources
- **Request/Response Format**: Standardized JSON format with consistent success/error patterns
- **Authentication Headers**: All authenticated endpoints require `Authorization: Bearer <token>` header with valid JWT
- **Content Type**: All POST/PUT/PATCH requests must use `application/json` content type with proper validation
- **Error Response Format**: Consistent error response structure with type, message, code, and optional details
- **Success Response Format**: Consistent success response structure with data and optional metadata
- **HTTP Status Codes**: Proper use of standard HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- **Rate Limiting Headers**: Implementation of rate limiting headers to inform clients of remaining requests

## Constraints

### Technical Constraints
- **Stateless Architecture**: No session data stored in memory
- **Database Persistence**: All user state stored in PostgreSQL
- **JWT Tokens**: Authentication without server-side sessions
- **Monorepo Structure**: All code in single repository following spec structure
- **Constitutional Compliance**: Adherence to technology stack requirements (Next.js 16+, FastAPI, SQLModel, PostgreSQL, Better Auth)
- **Password Complexity**: Minimum 8 characters, maximum 20 characters, with at least one special character (!@#$%^&*)
- **Hashing Algorithm**: Passwords must be hashed using bcrypt with cost factor 12 and automatic salt generation
- **Token Duration**: JWT tokens must expire after exactly 1 hour (3600 seconds) from issue time
- **Rate Limiting**: Authentication endpoints must implement rate limiting (max 5 attempts per IP per 15 minutes) to prevent brute force attacks; implemented using in-memory storage with IP-based tracking
- **Input Validation**: All inputs must be validated server-side using Pydantic models regardless of client-side validation
- **Algorithm Requirement**: JWT tokens must be signed using HS256 algorithm
- **Token Claims**: JWT must include user_id, email, exp, iat, and iss claims as specified
- **Database Security**: User credentials must be stored in PostgreSQL with appropriate access controls
- **Token Storage**: JWT tokens will be stored in localStorage for accessibility in SPA functionality with appropriate XSS protections
- **User Data Isolation**: Database queries must include user_id in WHERE clauses to enforce user data boundaries at the application level
- **Error Response Format**: All API endpoints must return standardized error responses in a consistent JSON format

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
- **Login Speed**: Authentication operations must complete within 2 seconds for 95% of requests
- **Token Validation**: JWT validation must complete within 100ms
- **Database Operations**: User lookup and creation must complete within 500ms
- **Concurrent Sessions**: System must support 100 concurrent authentication operations
- **Response Times**: 95% of authentication API endpoints respond within 2 seconds
- **Token Generation**: JWT creation and signing must complete within 50ms

### Security Constraints (Constitutional Requirements)
- **Password Hashing**: All passwords must be stored with bcrypt hashing (cost factor 12) with automatic salt generation; no other hashing algorithms permitted; password validation must include minimum 8 characters, maximum 20 characters, with at least one special character; per Constitution 403 (security hashing requirements)
- **Token Security**: JWT tokens must be properly signed with BETTER_AUTH_SECRET using HS256 algorithm and validated on each request; tokens must include exactly user_id (string), email (string), exp (timestamp), iat (timestamp), and iss (string: "todo-app-auth-service") claims as specified; token expiration strictly enforced at exactly 3600 seconds from issue with no tolerance; all token validation must complete within 100ms; token validation must reject any tokens with missing or invalid claims; per Constitution 404-405 (token security requirements)
- **Input Validation**: All user inputs must be validated server-side using Pydantic models with strict type checking regardless of client-side validation; no raw SQL queries permitted, only ORM-based database access; validation must include bounds checking, type validation, and format verification; per Constitution 491 (validation requirements)
- **Input Sanitization**: All user inputs must be sanitized using DOMPurify for HTML content and proper output encoding for display; prevent XSS by encoding special characters in user-generated content; per Constitution 408 (input sanitization requirements)
- **CORS Policy**: Frontend domain must be properly whitelisted in backend CORS settings for secure cross-origin communication; only HTTPS origins permitted in production environment; wildcard origins prohibited in any environment; strict validation prevents unauthorized cross-origin access
- **User Isolation**: Strict validation of user_id in JWT token vs URL parameter with application-level WHERE clause enforcement; database queries must include user_id in WHERE clauses to enforce data boundaries at application level; no user can access another user's data regardless of URL manipulation attempts; user_id validation must occur before any database operations; per Constitution 406 (user isolation requirements)
- **Rate Limiting**: Implementation using in-memory storage with IP-based tracking (max 5 attempts per IP per 15-minute sliding window) to prevent brute force attacks; rate limiting must use sliding window counter algorithm with exact 15-minute windows; blocked IPs must be automatically unblocked after 15 minutes; implement rate limiting headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset) to inform clients of remaining requests; per Constitution 402 (rate limiting requirements)
- **Token Storage**: JWT tokens stored in localStorage with specific XSS protection measures: input sanitization using DOMPurify, output encoding with framework built-ins, CSP headers with 'strict-dynamic' directive; no other storage mechanisms permitted in Phase II; additional CSRF protection through token validation patterns; per Constitution 408 (security storage requirements)
- **Error Handling**: Consistent error responses with generic messages to prevent user enumeration (same "Invalid credentials" for both invalid email and wrong password); error messages must not expose internal system details; all error responses must follow standardized format with success/error flags and appropriate HTTP status codes; per Constitution 492 (error handling requirements)
- **Shared Secrets**: BETTER_AUTH_SECRET must be identical value across frontend and backend services for JWT validation to work properly; secret must be at least 32 characters and randomly generated; secrets must be stored in environment variables, never in code; per Constitution 404 (secret sharing requirements)
- **CSRF Protection**: Secure token storage using double-submit cookie pattern or proper origin validation when using localStorage; implement proper referer and origin header validation for all authentication requests; per Constitution 408 (CSRF protection requirements)
- **Transport Security**: All communications must use HTTPS with HSTS headers set to 31536000 seconds (1 year) in production environment; HTTP connections must be redirected to HTTPS; certificate pinning recommended for mobile access; per Constitution 409 (transport security requirements)
- **Session Management**: No server-side session storage; all authentication state in JWT tokens only (stateless approach); client-side token storage must be cleared on logout; no persistent session storage mechanisms permitted; per Constitution 407 (stateless requirements)
- **Data Encryption**: All sensitive data encrypted in transit using TLS 1.3 and at rest in the database; database connections must use SSL encryption; per Constitution 410 (encryption requirements)
- **Audit Logging**: All authentication and authorization attempts must be logged for security monitoring; log sensitive information must be sanitized to protect user privacy; access logs must be retained per regulatory requirements; per Constitution 411 (audit requirements)
- **Security Headers**: Proper security headers including X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, and Strict-Transport-Security must be implemented; implement Content Security Policy (CSP) headers with 'strict-dynamic' directive; per Constitution 408 (security header requirements)

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
The MCP tools are implemented as a standardized interface layer that sits between AI agents and the core application API. Each MCP tool maps to specific existing API endpoints but provides a consistent, well-documented interface optimized for AI consumption following Model Context Protocol standards.

### Tool-to-API Mapping

**Authentication Tools:**
- `register_user` MCP tool → POST /api/auth/signup endpoint (creates new user account with email/password)
- `authenticate_user` MCP tool → POST /api/auth/signin endpoint (validates credentials and returns JWT token)
- `get_current_user` MCP tool → GET /api/auth/me endpoint (retrieves authenticated user information)
- `logout_user` MCP tool → POST /api/auth/signout endpoint (handles client-side session termination)

**Task Management Tools:**
- `create_task` MCP tool → POST /api/{user_id}/tasks endpoint (creates new task for authenticated user)
- `get_user_tasks` MCP tool → GET /api/{user_id}/tasks endpoint (retrieves all tasks for user)
- `get_task` MCP tool → GET /api/{user_id}/tasks/{id} endpoint (retrieves specific task by ID)
- `update_task` MCP tool → PUT /api/{user_id}/tasks/{id} endpoint (updates existing task details)
- `delete_task` MCP tool → DELETE /api/{user_id}/tasks/{id} endpoint (deletes specified task)
- `toggle_task_completion` MCP tool → PATCH /api/{user_id}/tasks/{id}/complete endpoint (toggles completion status)

### API Endpoint Data Flows

The following detailed data flows correspond to the API endpoints defined in the feature specification:

**Authentication Flows:**
- **GET /api/auth/me**: Extract JWT token from Authorization header → Validate token signature against BETTER_AUTH_SECRET → Verify token hasn't expired → Decode user_id from token claims → Query user record from database by user_id → Return user information excluding sensitive fields (password, internal data) with proper authorization checks

**Session Management Flows:**
- **POST /api/auth/signout**: Validate JWT token format and signature → Perform client-side token clearing (no server-side sessions due to stateless architecture) → Return success confirmation → Update client-side authentication state to logged-out

**Task Management Flows:**
- **GET /api/{user_id}/tasks**: Validate JWT token and extract authenticated user_id → Compare authenticated user_id with requested user_id from URL → Validate user_ids match (enforce user isolation) → Query tasks from database filtered by user_id → Apply pagination and ordering → Return tasks array with metadata
- **POST /api/{user_id}/tasks**: Validate JWT token and extract authenticated user_id → Compare with requested user_id → Validate user_ids match → Validate task input parameters (title length, description length) → Insert new task record with user_id association → Return created task with auto-generated ID and timestamps
- **PUT /api/{user_id}/tasks/{id}**: Validate JWT token and extract user_id → Verify user_id matches both JWT and URL parameter → Verify task exists and belongs to authenticated user → Validate updated input parameters → Update task record in database → Return updated task object with new timestamps
- **DELETE /api/{user_id}/tasks/{id}**: Validate JWT token and extract user_id → Verify user_id matches both JWT and URL parameter → Confirm task belongs to authenticated user → Delete task record from database → Return success confirmation

### MCP Tool Middleware
Each MCP tool incorporates standardized middleware that enforces constitutional requirements:
1. **Input Validation**: Validates JSON schema against tool specification using Pydantic models
2. **Authentication**: Extracts and validates JWT token from input with proper signature and expiration checks
3. **Authorization**: Verifies user_id in token matches requested user_id parameter with strict validation
4. **Error Wrapping**: Converts API errors to standardized MCP error format per constitutional requirements
5. **Logging**: Records tool usage for monitoring and debugging while respecting privacy requirements
6. **Rate Limiting**: Implements rate limiting to prevent abuse per security constraints
7. **Constitutional Compliance**: Ensures adherence to statelessness, clear contracts, error handling, and composability requirements

### MCP Tool Response Format
All MCP tools follow a standardized response format that adheres to constitutional requirements:
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

For errors (conforming to constitutional error handling requirements):
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
    "timestamp": "ISO 8601 timestamp"
  }
}
```

## MCP Architecture Principles Implementation (Constitutional Requirements)

### Statelessness (Constitutional Requirement 489-490)
- **Database-persisted operations**: All MCP tools read/write to database rather than in-memory storage (per Constitution 489-490)
- **No session maintenance**: No session state maintained between tool calls (per Constitution 407)
- **JWT-only authentication**: Authentication state managed exclusively through JWT tokens without server-side session storage (per Constitution 407)
- **Persistent user data**: All user data stored in PostgreSQL database with proper relationships and constraints
- **Horizontal scalability support**: Stateless design enables horizontal scaling without shared session state

### Clear Contract Design (Constitutional Requirement 491)
- **Well-defined schemas**: All MCP tools have well-defined JSON input/output schemas (per Constitution 491)
- **Machine-readable specifications**: Input/output specifications are machine-readable with clear validation rules
- **Pre-processing validation**: Validation occurs before processing with Pydantic models (per Constitution 491)
- **Consistent responses**: Consistent response formats across all tools with proper field standardization (per Constitution 491)
- **API specification compliance**: All contracts follow RESTful conventions and OpenAPI standards

### Error Handling (Constitutional Requirement 492)
- **Structured objects**: All MCP tools return structured error objects, not exceptions (per Constitution 492)
- **HTTP status mapping**: Errors include appropriate HTTP status code mappings for different error types
- **Privacy-preserving logs**: Technical details logged server-side while user-friendly messages returned to protect user privacy
- **Consistent categorization**: Error types categorized consistently across all tools (per Constitution 492)
- **Comprehensive logging**: Proper error logging for security monitoring while maintaining user privacy
- **Graceful degradation**: Systems provide fallback behaviors when components fail
- **Specific Error Responses**: 
  - Authentication errors return 401 with message "Invalid authentication token"
  - Authorization errors return 403 with message "Not authorized to access this resource"
  - Validation errors return 400 with detailed field-specific error messages
  - Resource not found errors return 404 with message "Requested resource not found"
  - Server errors return 500 with generic message "An unexpected error occurred"
  - Rate limiting errors return 429 with message "Too many requests, please try again later"
- **Error Response Format**: All errors follow the standardized format with success=false, error object containing type, message, code, and optional details
- **User-Friendly Messages**: Error messages are appropriate for end users without exposing system internals
- **Generic Error Messages**: Use generic messages like "Invalid credentials" for both invalid email and wrong password to prevent user enumeration

### Composability (Constitutional Requirement 493)
- **Chaining support**: MCP tools designed for chaining by agents for complex authentication workflows (per Constitution 493)
- **Single-operation design**: Each tool performs a single, well-defined operation following single responsibility principle
- **Combination capability**: Tools can be combined to perform complex multi-step processes
- **Consistent interface**: Consistent authentication and authorization patterns across all tools (per Constitution 493)
- **Workflow composition**: AI agents can compose complex operations by chaining multiple simple tools
- **Modular functionality**: Each tool operates independently while supporting integration with others

## Integration with Domain and User Journey Specifications

### Alignment with Domain Entities
This architectural plan directly implements the domain entities specified in the domain directory:
- **User Entity**: Implementation follows the specification in @specs/1-specify/domain/user-entity.md with proper authentication, authorization, and security measures
- **Task Entity**: Implementation follows the specification in @specs/1-specify/domain/task-entity.md with proper associations to user_id and validation rules
- **Conversation Entity**: Implementation follows the specification in @specs/1-specify/domain/conversation-entity.md for AI chat functionality (Phase III)

### Alignment with User Journeys
This architectural plan supports all user journeys defined in the user-journeys directory:
- **Basic Todo Journey**: All functionality for @specs/1-specify/user-journeys/journey-01-basic-todo.md is implemented through the frontend components and backend API
- **AI Chat Journey**: Architecture provides foundation for @specs/1-specify/user-journeys/journey-02-ai-chat.md through MCP tools and API design
- **Advanced Features Journey**: Implementation supports requirements in @specs/1-specify/user-journeys/journey-03-advanced-features.md through extensible architecture patterns

### Alignment with Feature Requirements
This architectural plan implements the core requirements from the feature specification @specs/1-specify/features/feature-02-fullstack-todo.md:
- **Authentication Requirements**: All authentication flows (registration, login, logout) align with the detailed user stories and functional requirements
- **Task Management**: All CRUD operations and user authorization requirements map to the architectural components and data flows outlined in this plan
- **Security Requirements**: Implementation follows the detailed security requirements including JWT token management, password hashing, rate limiting, and user isolation
- **API Endpoints**: All endpoints specified in the feature spec are implemented according to the architectural patterns described here
- **MCP Tools**: The 7 MCP tools specified in the feature spec are implemented using the architectural patterns and middleware described in this plan
- **Domain Entities**: Implementation respects the domain entity definitions in @specs/1-specify/domain/user-entity.md, @specs/1-specify/domain/task-entity.md, and @specs/1-specify/domain/conversation-entity.md
- **Token Management**: Specifically aligned with feature spec constraints - no token refresh mechanism in Phase II; users must re-authenticate after 1-hour expiration; refresh functionality reserved for future phases
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

### Integrated Testing Approach
Rather than concentrating testing in a single phase, testing is integrated throughout the development process:

- **Day 1**: Initial testing setup and smoke tests
- **Days 2-4**: Unit and integration tests developed alongside backend functionality
- **Days 5-6**: Component and integration tests developed alongside frontend functionality
- **Day 7**: Comprehensive end-to-end and security testing
- **Day 8**: Final verification and deployment testing

### Backend Testing
- **Unit Tests**: Test individual functions, authentication logic, and validation as each component is developed
- **MCP Tool Tests**: Test all MCP tools with various input combinations during Day 8
- **Integration Tests**: Test API endpoints with real database connections throughout Days 2-4
- **Security Tests**: Verify authentication, authorization, and data isolation throughout development
- **Performance Tests**: Benchmark API endpoints under load during Day 8
- **Password Validation Tests**: Test all password complexity requirements with valid/invalid inputs during Day 2
- **Token Generation Tests**: Test JWT creation, signing, and validation functions during Day 3
- **Authorization Logic Tests**: Test user ID comparison and permission verification during Days 3-4
- **Input Validation Tests**: Test all input validation functions with boundary conditions throughout Days 3-4

### Frontend Testing
- **Component Tests**: Test UI components with Jest and React Testing Library as each component is developed (Days 5-6)
- **Integration Tests**: Test component interactions and state management throughout Days 5-7
- **End-to-End Tests**: Simulate user flows using Playwright or Cypress during Days 7-8
- **MCP Integration Tests**: Test MCP tool accessibility for AI agents during Day 8
- **Accessibility Tests**: Verify accessibility compliance throughout Days 6-7
- **Authentication Flow Tests**: Complete registration, login, and token validation cycle throughout Days 5-7
- **Database Integration Tests**: Test user creation, lookup, and password verification against real database during Days 2-4
- **API Endpoint Tests**: Test all authentication endpoints with various inputs throughout Days 5-7
- **Authorization Middleware Tests**: Test protected routes with valid/invalid tokens throughout Days 5-7

### Security Testing
- **Password Strength Tests**: Verify that weak passwords are properly rejected during Day 2
- **Injection Attack Tests**: Test for SQL injection and other attack vectors throughout Days 3-4
- **Token Manipulation Tests**: Test response to tampered JWT tokens during Day 3
- **Rate Limiting Tests**: Test brute force protection mechanisms during Day 3
- **Session Hijacking Tests**: Verify token security and storage practices throughout Days 5-7

### API Contract Testing
- **Contract Verification**: Test that frontend and backend implementations match defined API contracts throughout Days 5-7
- **Schema Validation**: Verify request/response schemas match contract definitions
- **Error Handling Tests**: Ensure error responses match contract specifications

### Test Coverage Goals
- **Backend**: Minimum 80% coverage for business logic
- **MCP Tools**: 100% coverage for all tool inputs and error cases
- **Frontend**: Minimum 70% coverage for components
- **Critical Paths**: 100% coverage for authentication and authorization
- **API Tests**: Automated testing of all endpoints with various inputs
- **Contract Tests**: 100% verification that implementations match API contracts

### Specific Test Types and Targets
- **Unit Tests**: Target 85%+ coverage for pure functions and business logic
- **Integration Tests**: Test all API endpoints with real database connections (100% endpoint coverage)
- **Component Tests**: Test all UI components with Jest and React Testing Library (70%+ component coverage)
- **End-to-End Tests**: Test complete user flows using Playwright or Cypress (all major user journeys)
- **Security Tests**: Test authentication, authorization, and data isolation (100% security-critical paths)
- **API Contract Tests**: Verify all request/response schemas match contract definitions (100% compliance)
- **Error Handling Tests**: Test all error scenarios and responses (100% error path coverage)
- **Performance Tests**: Benchmark API endpoints under load (meet response time targets)
- **Accessibility Tests**: Verify accessibility compliance (WCAG 2.1 AA standards)
- **Rate Limiting Tests**: Verify brute force protection mechanisms (proper rate limiting)

This updated architectural plan provides a comprehensive roadmap for implementing a secure, scalable, and maintainable full-stack todo application with proper authentication, user data isolation, and MCP tools for AI agent integration as mandated by the Constitution. The plan incorporates all requirements from the constitution, feature specifications, domain entities, user journeys, and API specifications for Phase 2 of the Todo Evolution project.