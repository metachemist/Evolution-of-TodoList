# Feature Specification: Next.js Todo Frontend

**Feature Branch**: `006-nextjs-todo-frontend`
**Created**: 2026-02-13
**Status**: Draft
**Input**: User description: "Build a responsive, secure, and user-friendly Todo frontend that interacts with the existing REST backend. The application must support authenticated users managing their personal tasks."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Login (Priority: P1)

A new user visits the application and creates an account by providing their email and password. After registration, they are automatically authenticated and redirected to their personal dashboard. Returning users can log in with their existing credentials and access their tasks immediately.

**Why this priority**: Authentication is the foundation of the entire application. Without the ability to register and log in, no other feature can function. This is the gateway to all task management capabilities.

**Independent Test**: Can be fully tested by registering a new account, logging out, and logging back in. Delivers value by proving the authentication flow works end-to-end with the backend.

**Acceptance Scenarios**:

1. **Given** an unauthenticated user on the registration page, **When** they submit a valid email and password (8+ characters), **Then** they receive a JWT token and are redirected to the dashboard.
2. **Given** an unauthenticated user on the login page, **When** they submit valid credentials, **Then** they receive a JWT token and are redirected to the dashboard.
3. **Given** an unauthenticated user, **When** they attempt to access the dashboard directly, **Then** they are redirected to the login page.
4. **Given** an authenticated user, **When** they click logout, **Then** their token is cleared, state is reset, and they are redirected to the login page.
5. **Given** a user on the registration page, **When** they submit an email that already exists, **Then** they see the message: "An account with this email already exists. Please log in instead."
6. **Given** a user on the login page, **When** they submit invalid credentials, **Then** they see the message: "Invalid email or password. Please try again."

---

### User Story 2 - Viewing and Managing Tasks (Priority: P1)

An authenticated user lands on their dashboard and sees all their existing tasks displayed in a list ordered newest-first (most recently created at the top). Each task shows its title, description (truncated to 2 lines with ellipsis if longer), and completion status. Completed tasks are visually distinguished with a strikethrough on the title and reduced opacity. When no tasks exist, the user sees an empty state with an illustration or icon and the message "No tasks yet. Create your first task to get started."

**Why this priority**: Viewing tasks is the core value proposition of the application. Without task display, there is nothing for users to interact with. This is co-priority with authentication as both are needed for a minimal viable product.

**Independent Test**: Can be fully tested by logging in and verifying that tasks from the backend are displayed correctly, including empty state when no tasks exist.

**Acceptance Scenarios**:

1. **Given** an authenticated user with existing tasks, **When** they navigate to the dashboard, **Then** all their tasks are displayed newest-first showing title, description (truncated to 2 lines with "..." if longer), and completion status.
2. **Given** an authenticated user with no tasks, **When** they navigate to the dashboard, **Then** they see an empty state with an icon and the message "No tasks yet. Create your first task to get started."
3. **Given** an authenticated user with completed tasks, **When** they view the task list, **Then** completed tasks display with a strikethrough on the title and reduced opacity compared to incomplete tasks.
4. **Given** a task list is loading, **When** the user is waiting, **Then** they see a loading indicator until tasks are fetched.
5. **Given** the backend is unreachable, **When** tasks fail to load, **Then** the user sees the message "Unable to load tasks. Please check your connection and try again." with a retry button.

---

### User Story 3 - Creating New Tasks (Priority: P2)

An authenticated user wants to add a new task to their list. They fill in a task title (required) and optionally a description, then submit the form. The new task appears at the top of their task list immediately.

**Why this priority**: Task creation is essential for the application to be useful beyond viewing pre-existing data. It enables users to actively manage their work.

**Independent Test**: Can be fully tested by logging in, creating a task with title and description, and verifying it appears at the top of the task list.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the dashboard, **When** they click the "Create Task" button, **Then** a modal dialog opens with an empty title field and an empty description field.
2. **Given** the create task modal is open, **When** the user fills in a title and submits, **Then** the modal closes, the new task appears at the top of the task list, focus returns to the "Create Task" button, and a success toast "Task created" appears for 3 seconds.
3. **Given** the create task modal is open, **When** the user submits without a title, **Then** they see a validation error inside the modal: "Title is required."
4. **Given** the create task modal is open, **When** the user submits a title exceeding 255 characters, **Then** they see a validation error: "Title must be 255 characters or less."
5. **Given** the create task modal is open, **When** the user submits a description exceeding 5000 characters, **Then** they see a validation error: "Description must be 5000 characters or less."
6. **Given** the task creation request fails, **When** the backend returns an error, **Then** the user sees the message inside the modal: "Failed to create task. Please try again." The modal remains open.

---

### User Story 4 - Editing Existing Tasks (Priority: P2)

An authenticated user wants to update the title or description of an existing task. They click an edit action on a task, modify the fields in a form, and save the changes. The updated task is reflected in the list immediately.

**Why this priority**: Editing tasks allows users to correct mistakes and refine their task descriptions, which is critical for ongoing task management.

**Independent Test**: Can be fully tested by logging in, selecting a task to edit, changing its title or description, and verifying the changes persist.

**Acceptance Scenarios**:

1. **Given** an authenticated user viewing their tasks, **When** they click edit on a task, **Then** a modal dialog opens with the form pre-filled with the task's current title and description.
2. **Given** the edit task modal is open, **When** the user updates the title and saves, **Then** the modal closes, the task list reflects the updated title, focus returns to the edit button of that task, and a success toast "Task updated" appears for 3 seconds.
3. **Given** the edit task modal is open, **When** the user clears the title and tries to save, **Then** they see a validation error inside the modal: "Title is required."
4. **Given** the edit task modal is open, **When** the backend returns a 404, **Then** the user sees the message inside the modal: "This task no longer exists. It may have been deleted." The modal remains open with a close button.

---

### User Story 5 - Completing and Deleting Tasks (Priority: P2)

An authenticated user wants to mark a task as complete by toggling a checkbox. They can also permanently delete tasks they no longer need. Deletion requires confirmation via a modal dialog that states the action is permanent.

**Why this priority**: Completion toggling and deletion are the natural conclusion of the task lifecycle. Without them, the task list would grow indefinitely.

**Independent Test**: Can be fully tested by logging in, toggling a task's completion status, verifying the visual change, then deleting a task and verifying it disappears.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an incomplete task, **When** they toggle the completion checkbox, **Then** the task is marked as completed with strikethrough title and reduced opacity.
2. **Given** an authenticated user with a completed task, **When** they toggle the completion checkbox again, **Then** the task is marked as incomplete with normal title and full opacity.
3. **Given** an authenticated user, **When** they click delete on a task, **Then** a modal dialog appears with the message "Are you sure you want to delete this task? This action cannot be undone." and two buttons: "Cancel" and "Delete".
4. **Given** the user clicks "Delete" in the confirmation modal, **Then** the task is removed from the list optimistically, the modal closes, focus returns to the nearest remaining task's delete button (or the "Create Task" button if no tasks remain), and a success toast "Task deleted" appears for 3 seconds.
5. **Given** the user clicks "Cancel" in the confirmation modal, **Then** the modal closes and the task remains unchanged.

---

### User Story 6 - Dark/Light Mode and Responsive Layout (Priority: P3)

A user can switch between dark and light themes for comfortable viewing in different environments. The chosen theme persists permanently in the browser so it survives page refreshes and browser restarts. The application layout adapts to mobile, tablet, and desktop screen sizes.

**Why this priority**: While important for user experience and accessibility, theme support and responsiveness are polish features that enhance but do not enable core functionality.

**Independent Test**: Can be fully tested by toggling the theme switch and verifying visual changes persist after refresh, and by resizing the browser window to verify layout adaptation at mobile, tablet, and desktop breakpoints.

**Acceptance Scenarios**:

1. **Given** a user on any page, **When** they toggle the theme switch, **Then** the entire application switches between dark and light modes.
2. **Given** a user who selected dark mode, **When** they close and reopen the browser, **Then** the application loads in dark mode.
3. **Given** a user on a mobile device (viewport < 768px), **When** they view the dashboard, **Then** the layout is single-column and touch-friendly.
4. **Given** a user on a desktop (viewport > 1024px), **When** they view the dashboard, **Then** the layout uses appropriate spacing and width constraints.

---

### Edge Cases

- What happens when the JWT token expires mid-session? The user should be redirected to the login page with the message: "Your session has expired. Please log in again."
- What happens when the user submits a form while already processing a previous request? The submit button should be disabled during processing to prevent duplicate submissions.
- What happens when the user has a slow network connection? Loading indicators must be visible, and requests that take longer than 15 seconds should display: "The request is taking longer than expected. Please check your connection."
- What happens when the backend returns a 403 Forbidden? The frontend should display: "You don't have permission to perform this action." and redirect to the dashboard.
- What happens when the user navigates directly to /dashboard without a valid token? The route guard should redirect them to /login.
- What happens when the user's browser does not support JavaScript? The application should display a noscript fallback message.
- What happens when the backend returns a 500 Internal Server Error? The frontend should display: "Something went wrong on our end. Please try again later."
- What happens when an optimistic update fails (backend rejects after UI already updated)? The UI MUST roll back to the previous state and show a non-blocking error toast at the bottom of the screen for 5 seconds with the relevant error message. The toast MUST be dismissible by clicking a close button.

## Clarifications

### Session 2026-02-13

- Q: How should the JWT token be stored — in-memory, httpOnly cookie (frontend-set), httpOnly cookie (backend-set), or sessionStorage? → A: HttpOnly cookie set by the backend (Option C). Backend sets Set-Cookie header on login/register responses. Frontend never handles raw tokens. Requires new backend endpoints: `GET /api/auth/me` (session check) and `POST /api/auth/logout` (cookie clearing).
- Q: What UX pattern should task create and edit forms use — inline, modal, slide-out panel, or separate page? → A: Modal dialog (Option B). Both create and edit open a centered modal overlay. Consistent with the delete confirmation modal pattern. Modal closes on success, stays open on validation/backend errors.
- Q: Should UI updates be optimistic (update before backend confirms) or pessimistic (wait for confirmation)? → A: Optimistic for all mutations (Option A). UI updates immediately on user action; rolls back with a non-blocking error toast (5 seconds, dismissible) if the backend rejects the request.
- Q: How should long task descriptions be displayed in the list view? → A: Truncate to 2 lines with ellipsis (Option B). Consistent card heights. Full description accessible only in the edit modal.
- Q: What happens to focus and user feedback after a modal closes on success? → A: Toast notification (Option B). Focus returns to trigger element. Non-blocking success toast for 3 seconds ("Task created" / "Task updated" / "Task deleted"). No toast for toggle completion.
- Q: How should task endpoints authenticate requests — httpOnly cookie or Bearer header? → A: Cookie auth for all endpoints (Option A). Backend reads JWT from the httpOnly cookie for task endpoints too. Frontend uses `credentials: 'include'` on all fetch calls. No Authorization header is needed. The `{user_id}` path parameter is validated server-side against the cookie's JWT `sub` claim.

## Non-Goals

The following are explicitly out of scope for this feature and MUST NOT be implemented:

- **No task filtering, sorting, or search**: The dashboard displays all tasks in newest-first order only. Advanced list manipulation is deferred to a future feature.
- **No task priorities or due dates**: Tasks have title, description, and completion status only. Priority levels, deadlines, and reminders are out of scope.
- **No multi-user collaboration**: Users cannot share tasks, assign tasks to others, or view other users' tasks.
- **No offline support or PWA**: The application requires an active network connection. Service workers, caching strategies, and installable app behavior are not included.
- **No password reset or recovery**: Users who forget their password have no self-service recovery flow in this iteration.
- **No user profile management**: Users cannot change their email, password, or view account details after registration.
- **No task pagination controls**: The frontend fetches tasks using backend defaults. Infinite scroll, page numbers, or "load more" interactions are not included.
- **No real-time updates**: Task changes from other sessions or devices are not pushed to the client. The user must refresh to see external changes.
- **No internationalization (i18n)**: The application is English-only. Translation infrastructure, locale detection, and RTL support are out of scope. (Constitution notes Urdu as a bonus feature for a future phase.)
- **No analytics or telemetry**: No usage tracking, event logging, performance monitoring, or third-party analytics scripts are included.
- **No email verification**: Registration accepts email and password without verifying the email address is real or owned by the user.

## Constraints

### Accessibility

- All pages MUST conform to WCAG 2.1 Level AA, as required by the constitution.
- All form inputs MUST have associated visible labels and aria-labels.
- All interactive elements MUST be reachable and operable via keyboard alone (Tab, Enter, Escape).
- Focus MUST be managed when modals open (trapped inside) and close (returned to trigger element).
- Color contrast MUST meet a minimum ratio of 4.5:1 for normal text and 3:1 for large text in both themes.
- The delete confirmation modal MUST be announced to screen readers when it opens.

### Performance

- Initial page load (first contentful paint) MUST occur within 1.5 seconds on a standard broadband connection (10 Mbps).
- The production JavaScript bundle MUST NOT exceed 250 KB gzipped (excluding vendor chunks loaded on demand).
- All API-triggered UI updates (task create, edit, delete, toggle) MUST complete within 2 seconds when the backend responds within its SLA (< 300ms).
- The application MUST support 50 concurrent authenticated users without degradation, per constitution Phase II targets.

### Browser Support

The application MUST function correctly (all FRs pass) on the following browsers:

- Chrome (latest 2 major versions)
- Firefox (latest 2 major versions)
- Safari (latest 2 major versions, macOS and iOS)
- Edge (latest 2 major versions)

The application is NOT required to support Internet Explorer or any browser version older than the above.

### Session and Token Behavior

- The backend issues JWT tokens with a 15-minute expiration. The frontend MUST NOT implement token refresh. When a token expires, the backend returns 401 and the frontend redirects to the login page.
- Token refresh is explicitly out of scope for this iteration.

### Testing

- Automated test coverage MUST reach 60% of frontend business logic (state management, validation, API integration), per constitution Phase II targets.
- All 6 user stories MUST have corresponding acceptance tests that can be executed as part of a test suite.

## Routing Table

| Path | Behavior | Auth Required |
|------|----------|---------------|
| `/` | Redirect to `/dashboard` if authenticated, otherwise redirect to `/login` | No |
| `/login` | Render login form. Redirect to `/dashboard` if already authenticated. | No (redirects if auth) |
| `/register` | Render registration form. Redirect to `/dashboard` if already authenticated. | No (redirects if auth) |
| `/dashboard` | Render task management interface. Redirect to `/login` if not authenticated. | Yes |

All other paths MUST return a 404 page with the message: "Page not found." and a link back to the dashboard.

## Backend API Contract

The frontend integrates with the existing FastAPI backend. The following endpoints are the complete contract. The frontend MUST NOT call endpoints not listed here.

### Authentication Endpoints

**Register**:
- Method: `POST`
- Path: `/api/auth/register`
- Request body: `{ "email": "<valid email>", "password": "<string>" }`
- Success response (201): `{ "access_token": "<jwt>", "token_type": "bearer" }` — Backend also sets an httpOnly, Secure, SameSite=Lax cookie containing the JWT.
- Error responses:
  - 409: `{ "success": false, "data": null, "error": { "code": "EMAIL_ALREADY_EXISTS", "message": "A user with this email already exists" } }`

**Login**:
- Method: `POST`
- Path: `/api/auth/login`
- Request body: `{ "email": "<valid email>", "password": "<string>" }`
- Success response (200): `{ "access_token": "<jwt>", "token_type": "bearer" }` — Backend also sets an httpOnly, Secure, SameSite=Lax cookie containing the JWT.
- Error responses:
  - 401: `{ "success": false, "data": null, "error": { "code": "INVALID_CREDENTIALS", "message": "Invalid email or password" } }`

**Get Current User (Session Check)**:
- Method: `GET`
- Path: `/api/auth/me`
- Authentication: httpOnly cookie (attached automatically by browser)
- Success response (200): `{ "id": "<uuid>", "email": "<string>" }`
- Error responses:
  - 401: No valid cookie / expired token (frontend redirects to login)

**Logout**:
- Method: `POST`
- Path: `/api/auth/logout`
- Authentication: httpOnly cookie (attached automatically by browser)
- Success response (200): Backend clears the httpOnly cookie via Set-Cookie with expired date.
- Error responses: None (always succeeds; invalid/missing cookie still returns 200)

### Task Endpoints

All task endpoints require authentication via the httpOnly cookie (attached automatically by the browser when the frontend uses `credentials: 'include'`). No `Authorization` header is needed. The `{user_id}` path parameter MUST match the authenticated user's ID (extracted from the JWT `sub` claim in the cookie).

**List Tasks**:
- Method: `GET`
- Path: `/api/{user_id}/tasks?skip=0&limit=20`
- Query params: `skip` (int, default 0), `limit` (int, default 20, max 100)
- Success response (200): Array of TaskResponse objects

**Create Task**:
- Method: `POST`
- Path: `/api/{user_id}/tasks`
- Request body: `{ "title": "<string, required>", "description": "<string, optional>" }`
- Success response (201): TaskResponse object

**Get Task**:
- Method: `GET`
- Path: `/api/{user_id}/tasks/{task_id}`
- Success response (200): TaskResponse object

**Update Task**:
- Method: `PUT`
- Path: `/api/{user_id}/tasks/{task_id}`
- Request body: `{ "title": "<string, optional>", "description": "<string, optional>" }`
- Success response (200): TaskResponse object

**Delete Task**:
- Method: `DELETE`
- Path: `/api/{user_id}/tasks/{task_id}`
- Success response (204): Empty body

**Toggle Completion**:
- Method: `PATCH`
- Path: `/api/{user_id}/tasks/{task_id}/complete`
- Request body: Empty
- Success response (200): TaskResponse object

### Shared Response Shapes

**TaskResponse**:
```
{
  "id": "<uuid>",
  "title": "<string>",
  "description": "<string | null>",
  "is_completed": <boolean>,
  "created_at": "<ISO 8601 datetime>",
  "updated_at": "<ISO 8601 datetime>",
  "owner_id": "<uuid>"
}
```

**Error Response** (all 4xx/5xx):
```
{
  "success": false,
  "data": null,
  "error": {
    "code": "<ERROR_CODE>",
    "message": "<Human-readable message>"
  }
}
```

### Common Error Codes

| HTTP Status | Error Code | Frontend Message |
|-------------|------------|------------------|
| 401 | INVALID_CREDENTIALS | "Invalid email or password. Please try again." |
| 401 | (token expired/invalid) | "Your session has expired. Please log in again." |
| 403 | UNAUTHORIZED_ACCESS | "You don't have permission to perform this action." |
| 404 | USER_NOT_FOUND | "Account not found. Please register first." |
| 404 | TASK_NOT_FOUND | "This task no longer exists. It may have been deleted." |
| 409 | EMAIL_ALREADY_EXISTS | "An account with this email already exists. Please log in instead." |
| 500 | (any) | "Something went wrong on our end. Please try again later." |
| Network failure | (none) | "Unable to connect to the server. Please check your connection and try again." |

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a registration page that accepts email and password and sends credentials to the backend registration endpoint.
- **FR-002**: System MUST provide a login page that accepts email and password and sends credentials to the backend login endpoint.
- **FR-003**: The backend MUST set the JWT access token as an httpOnly, Secure, SameSite=Lax cookie on successful login and registration responses. The frontend MUST NOT handle or store the raw token. The browser automatically attaches the cookie to all same-origin API requests.
- **FR-004**: System MUST redirect unauthenticated users to the login page when they attempt to access protected routes (dashboard).
- **FR-005**: System MUST redirect authenticated users away from login and registration pages to the dashboard.
- **FR-006**: System MUST provide a logout action that calls the backend to clear the httpOnly cookie, resets all frontend application state, and redirects to the login page.
- **FR-007**: System MUST fetch and display all tasks belonging to the authenticated user, ordered newest-first, when the dashboard loads.
- **FR-008**: System MUST provide a task creation form in a modal dialog with a required title field (max 255 characters) and an optional description field (max 5000 characters). The modal is triggered by a "Create Task" button visible on the dashboard.
- **FR-009**: System MUST allow users to create a new task. The modal MUST close immediately and the new task MUST appear at the top of the task list optimistically. If the backend rejects the request, the task MUST be removed from the list and an error toast MUST be displayed.
- **FR-010**: System MUST provide an edit action for each task that opens a modal dialog with the form pre-filled with the task's current title and description. The modal MUST close immediately on save and the task list MUST reflect the changes optimistically. If the backend rejects the update, the task MUST revert to its previous state and an error toast MUST be displayed.
- **FR-011**: System MUST provide a completion toggle for each task. The visual state MUST update optimistically on click. If the backend rejects the toggle, the task MUST revert to its previous state and an error toast MUST be displayed.
- **FR-012**: System MUST provide a delete action for each task that opens a modal confirmation dialog. On confirmation, the task MUST be removed from the list optimistically and the modal MUST close. If the backend rejects the deletion, the task MUST reappear in its original position and an error toast MUST be displayed.
- **FR-013**: System MUST validate all form inputs on the client side before submitting to the backend, with the following rules:
  - Email: MUST be a valid email format (contains `@` and a domain).
  - Password: MUST be at least 8 characters.
  - Task title: MUST NOT be empty. MUST NOT exceed 255 characters.
  - Task description: MUST NOT exceed 5000 characters.
- **FR-014**: System MUST display the specific user-friendly error messages defined in the Error Message Catalog (see Backend API Contract section) for all backend error responses.
- **FR-015**: System MUST show loading indicators during all asynchronous operations (login, registration, task fetching, task mutations).
- **FR-016**: System MUST provide dark/light mode theme switching that persists permanently in the browser across page refreshes and browser restarts.
- **FR-017**: System MUST be responsive and usable on mobile (< 768px), tablet (768px-1024px), and desktop (> 1024px) viewports.
- **FR-018**: All backend communication MUST go through a single integration layer that handles authentication, error normalization, and base URL configuration consistently.
- **FR-019**: System MUST display an empty state UI with an icon and the message "No tasks yet. Create your first task to get started." when the user has no tasks.
- **FR-020**: System MUST identify the authenticated user (via a backend endpoint or cookie-based session check) and use their identity when communicating with the backend for all user-scoped operations. Since the frontend cannot read the httpOnly cookie directly, the backend MUST provide a session/identity endpoint that returns the current user's ID and email.
- **FR-021**: Completed tasks MUST be visually distinguished from incomplete tasks using a strikethrough on the title and reduced opacity.
- **FR-024**: Task descriptions in the list view MUST be truncated to a maximum of 2 lines with an ellipsis ("...") when the content exceeds the available space. The full description is accessible only in the edit modal.
- **FR-022**: All interactive elements MUST be operable via keyboard. Modals MUST trap focus when open and return focus to the trigger element when closed (the edit/delete button that opened the modal, or the "Create Task" button for create).
- **FR-023**: All pages MUST meet WCAG 2.1 Level AA color contrast requirements in both dark and light themes.
- **FR-025**: After successful task creation, update, or deletion, the system MUST display a non-blocking success toast for 3 seconds with the message "Task created", "Task updated", or "Task deleted" respectively. No success toast is shown for completion toggle (the visual state change is sufficient confirmation). Success toasts MUST be auto-dismissible and not block user interaction.

### Key Entities

- **User Session**: Represents the authenticated user's session state, including the user ID and email (retrieved from a backend session endpoint). The JWT token is managed entirely by the browser as an httpOnly cookie and is never accessible to frontend code. Session state exists in frontend memory and is populated on app load by calling the backend identity endpoint.
- **Task**: Represents a to-do item belonging to a user, with attributes: unique identifier (UUID), title (string, required, max 255), optional description (string, max 5000), completion status (boolean), creation timestamp, and last-updated timestamp. Owned by exactly one user.
- **API Error**: Represents a structured error response from the backend, with attributes: success flag (always false), error code (string constant), and human-readable message.

## Deliverables

The following artifacts MUST be produced as part of this feature:

- All frontend application code (pages, components, state management, API integration, validation)
- `frontend/CLAUDE.md` containing frontend-specific patterns and conventions, as required by the constitution for Phase II+
- Automated tests meeting the 60% coverage target for business logic
- Every code file MUST include a comment referencing the task ID from `specs/3-tasks/` that it implements, per constitution traceability requirements
- A `.env.example` file documenting all required environment variables

## Assumptions

- The backend API is running and accessible at a configurable base URL (environment variable).
- JWT tokens use the HS256 algorithm and contain a `sub` claim with the user's UUID.
- The backend sets the JWT as an httpOnly, Secure, SameSite=Lax cookie on login and registration. The JSON response body also contains the token for backward compatibility, but the frontend MUST NOT read or store it. All endpoints (including task endpoints) accept the cookie for authentication; no Authorization header is required.
- The backend provides `GET /api/auth/me` to return the authenticated user's ID and email based on the cookie. This endpoint is required for the frontend to identify the user without reading the token.
- The backend provides `POST /api/auth/logout` to clear the httpOnly cookie.
- Task list endpoints return an array of task objects directly (not wrapped in a pagination envelope).
- The backend CORS configuration allows requests from the frontend's origin with `credentials: include` support.
- Token expiration is 15 minutes, handled by the backend returning 401. The frontend does not refresh tokens.
- The backend does not enforce password complexity beyond accepting any string. The frontend enforces a minimum of 8 characters as a usability measure.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new user can register and land on the dashboard within 3 user actions (navigate to register, fill form, submit). Verified by manual walkthrough during acceptance testing.
- **SC-002**: A returning user can log in and land on the dashboard within 2 user actions (fill form, submit). Verified by manual walkthrough during acceptance testing.
- **SC-003**: The dashboard displays all tasks within 2 seconds of page load when the backend responds within its SLA (< 300ms). Verified by measuring time from navigation to visible task list with browser dev tools.
- **SC-004**: After submitting the create task form, the new task appears at the top of the list within 2 seconds. Verified by observing the UI update after form submission.
- **SC-005**: After toggling a task's completion checkbox, the visual state (strikethrough + reduced opacity, or normal) updates within 500ms. Verified by observing the UI response to a click.
- **SC-006**: Form validation errors appear within 200ms of the user leaving an invalid field (blur) or submitting. Verified by entering invalid data and timing the error display.
- **SC-007**: All pages render without horizontal scrollbar at viewport widths of 320px, 768px, and 1024px. Verified by resizing the browser and checking for overflow.
- **SC-008**: Theme toggle switches all visible UI elements between dark and light palettes without a page reload, and the choice persists after browser restart. Verified by toggling, closing the browser, reopening, and confirming the theme.
- **SC-009**: Every error state maps to the exact user-friendly message defined in the Error Message Catalog. No raw error codes, JSON, or stack traces are visible to users. Verified by triggering each error condition in the catalog and comparing displayed text.
- **SC-010**: All 25 functional requirements (FR-001 through FR-025) pass their corresponding acceptance scenarios in a single test run. Verified by executing the full acceptance test suite before release.
- **SC-011**: Initial page load (first contentful paint) occurs within 1.5 seconds on a 10 Mbps connection. Verified by Lighthouse audit or browser dev tools throttled to "Fast 3G" equivalent.
- **SC-012**: Automated test coverage of frontend business logic reaches 60% or higher. Verified by running the test suite with coverage reporting.
- **SC-013**: All pages pass an automated accessibility audit (axe-core or equivalent) with zero critical or serious violations. Verified by running the audit tool against each route.
