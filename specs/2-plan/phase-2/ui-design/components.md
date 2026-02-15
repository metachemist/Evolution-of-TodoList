# Component Architecture: Next.js Todo Frontend

**Feature**: 006-nextjs-todo-frontend | **Date**: 2026-02-13
**Spec**: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md
**Plan**: @specs/2-plan/phase-2/phase-2-nextjs-todo-frontend.md

## Component Inventory

### Primitive UI Components (`src/components/ui/`)

#### Button
- **Type**: Client Component
- **Props**: `variant` (primary | destructive | ghost), `size` (sm | md), `disabled`, `loading`, `children`, standard button attrs
- **Behavior**: Renders a styled `<button>`. Shows spinner when `loading=true`. Disables click when `disabled` or `loading`.
- **Accessibility**: Native `<button>` element, `aria-disabled` when loading
- **Styling**: Tailwind classes, 4.5:1 contrast ratio in both themes

#### Input
- **Type**: Client Component
- **Props**: `label`, `error`, `id`, standard input attrs
- **Behavior**: Renders `<label>` + `<input>` pair. Shows error message below when `error` is provided.
- **Accessibility**: `<label htmlFor={id}>`, `aria-describedby` pointing to error element, `aria-invalid` when error present
- **Integration**: Works with react-hook-form `register()` via spread

#### Modal
- **Type**: Client Component (wrapper around Radix UI Dialog)
- **Props**: `open`, `onOpenChange`, `title`, `description?`, `children`
- **Behavior**: Renders Radix `Dialog.Root` → `Dialog.Portal` → `Dialog.Overlay` + `Dialog.Content`. Overlay is semi-transparent backdrop. Content is centered.
- **Accessibility**:
  - Focus trapped inside when open (Radix built-in)
  - Escape key closes (Radix built-in)
  - Focus returns to trigger element on close (Radix built-in)
  - `Dialog.Title` announced by screen readers
  - `role="dialog"`, `aria-modal="true"` (Radix built-in)
  - Body scroll locked when open
- **Styling**: Tailwind. Overlay: `bg-black/50`. Content: centered with max-width, rounded corners, padding.

#### Toast (Sonner Configuration)
- **Type**: Client Component
- **Props**: None (configured once in root layout)
- **Behavior**: Renders `<Toaster position="bottom-right" />` from Sonner. Toast calls (`toast.success()`, `toast.error()`) happen imperatively from hooks/API client.
- **Configuration**:
  - Success: 3 second duration, auto-dismiss
  - Error: 5 second duration, close button visible, dismissible
  - Position: bottom-right (does not block main content)

#### ThemeToggle
- **Type**: Client Component
- **Props**: None
- **Behavior**: Reads current theme from `useTheme()` (next-themes). Toggles between `'light'` and `'dark'` on click. Persists to `localStorage` automatically via next-themes.
- **Accessibility**: `<button>` with `aria-label="Toggle theme"`. Visual icon indicates current state.
- **Placement**: Navigation bar (desktop), hamburger menu (mobile)

---

### Auth Components (`src/components/auth/`)

#### LoginForm
- **Type**: Client Component (`'use client'`)
- **Props**: None
- **State**: react-hook-form with zodResolver(loginSchema)
- **Behavior**:
  1. Renders email + password inputs with validation
  2. On submit: calls `POST /api/auth/login` via `useAuth().login()`
  3. On success: `router.push('/dashboard')`
  4. On error: displays error message from API client error catalog
  5. Submit button disabled during `isSubmitting`
- **Validation**: Email format, password ≥8 chars. Errors shown on blur and submit.
- **Accessibility**: All inputs have visible labels, `aria-describedby` for errors, `role="alert"` on error messages
- **Session expiry message**: Reads `?reason=session_expired` from URL params, shows "Your session has expired. Please log in again." above the form.

#### RegisterForm
- **Type**: Client Component (`'use client'`)
- **Props**: None
- **State**: react-hook-form with zodResolver(registerSchema)
- **Behavior**:
  1. Renders email + password inputs with validation
  2. On submit: calls `POST /api/auth/register` via `useAuth().register()`
  3. On success: `router.push('/dashboard')`
  4. On error: displays error message (e.g., "An account with this email already exists")
  5. Submit button disabled during `isSubmitting`
- **Validation**: Same as LoginForm (email format, password ≥8 chars)
- **Link**: "Already have an account? Log in" link to `/login`

---

### Task Components (`src/components/tasks/`)

#### TaskList
- **Type**: Client Component (`'use client'`)
- **Props**: None (reads userId from UserContext)
- **State**: `useTasks()` hook (TanStack Query) providing `{ tasks, isLoading, isError, error }`
- **Behavior**:
  - **Loading**: Renders loading skeleton (pulsing placeholder cards)
  - **Error**: Renders "Unable to load tasks. Please check your connection and try again." + retry button
  - **Empty**: Renders `<EmptyState />`
  - **Has tasks**: Renders list of `<TaskItem />` components, newest-first
  - **Create button**: "Create Task" button at top, opens `<TaskCreateModal />`
- **Accessibility**: `<ul role="list">` container, each task is `<li>`

#### TaskItem
- **Type**: Client Component (`'use client'`)
- **Props**: `task: Task`
- **Behavior**:
  - Renders: checkbox (completion toggle) + title + truncated description (2 lines, CSS `line-clamp-2`) + edit button + delete button
  - **Completed state**: Title has `line-through`, card has `opacity-60`
  - **Toggle**: Calls `useToggleTask()` mutation on checkbox click. Optimistic UI update.
  - **Edit**: Opens `<TaskEditModal />` for this task
  - **Delete**: Opens `<TaskDeleteModal />` for this task
- **Accessibility**:
  - Checkbox: `<input type="checkbox" aria-label="Mark {title} as {complete/incomplete}">`
  - Edit button: `aria-label="Edit {title}"`
  - Delete button: `aria-label="Delete {title}"`

#### EmptyState
- **Type**: Server or Client Component (no interactivity needed)
- **Props**: None
- **Behavior**: Renders an icon (clipboard or checkmark illustration) + "No tasks yet. Create your first task to get started."
- **Styling**: Centered, muted text, appropriate icon size

#### TaskCreateModal
- **Type**: Client Component (`'use client'`)
- **Props**: `open: boolean`, `onOpenChange: (open: boolean) => void`
- **State**: react-hook-form with zodResolver(taskCreateSchema)
- **Behavior**:
  1. Modal opens with empty title + description fields
  2. Client-side validation: title required (1-255 chars), description optional (0-5000 chars)
  3. On submit: calls `useCreateTask()` mutation
  4. On success: modal closes, toast "Task created" 3s, focus returns to "Create Task" button
  5. On validation error: error shown inside modal, modal stays open
  6. On backend error: "Failed to create task. Please try again." shown inside modal, modal stays open
  7. Submit button disabled during submission
- **Accessibility**: Inherits Modal accessibility (focus trap, escape, screen reader)

#### TaskEditModal
- **Type**: Client Component (`'use client'`)
- **Props**: `task: Task`, `open: boolean`, `onOpenChange: (open: boolean) => void`
- **State**: react-hook-form pre-filled with `task.title` and `task.description`
- **Behavior**:
  1. Modal opens with fields pre-filled from current task
  2. Same validation as create
  3. On submit: calls `useUpdateTask()` mutation
  4. On success: modal closes, toast "Task updated" 3s, focus returns to edit button of that task
  5. On validation error: error shown inside modal, modal stays open
  6. On 404: "This task no longer exists. It may have been deleted." shown in modal with close button
  7. Submit button disabled during submission
- **Accessibility**: Same as TaskCreateModal

#### TaskDeleteModal
- **Type**: Client Component (`'use client'`)
- **Props**: `task: Task`, `open: boolean`, `onOpenChange: (open: boolean) => void`
- **Behavior**:
  1. Modal shows: "Are you sure you want to delete this task? This action cannot be undone."
  2. Two buttons: "Cancel" and "Delete"
  3. Cancel: closes modal, task unchanged
  4. Delete: calls `useDeleteTask()` mutation, optimistic removal
  5. On success: modal closes, toast "Task deleted" 3s, focus returns to nearest remaining task's delete button (or "Create Task" button if none remain)
  6. On error: task reappears, error toast 5s
- **Accessibility**:
  - `Dialog.Title`: "Delete Task"
  - `Dialog.Description`: The confirmation message (announced by screen readers)
  - Delete button styled as destructive (red)

---

### Hooks (`src/hooks/`)

#### useAuth
- **Returns**: `{ login, register, logout, isLoading }`
- `login(email, password)`: POST /api/auth/login → router.push('/dashboard')
- `register(email, password)`: POST /api/auth/register → router.push('/dashboard')
- `logout()`: POST /api/auth/logout → clear context → router.push('/login')

#### useTasks
- **Returns**: `{ tasks, isLoading, isError, error, refetch }`
- Wraps `useQuery({ queryKey: ['tasks', userId], queryFn: ... })`
- Reads `userId` from UserContext

#### useCreateTask
- **Returns**: TanStack `useMutation` result
- `onMutate`: Optimistic insert at index 0 with temp ID
- `onError`: Remove optimistic task, show error toast
- `onSettled`: Invalidate `['tasks', userId]`

#### useUpdateTask
- **Returns**: TanStack `useMutation` result
- `onMutate`: Snapshot + optimistic field update
- `onError`: Revert to snapshot, show error toast
- `onSettled`: Invalidate `['tasks', userId]`

#### useDeleteTask
- **Returns**: TanStack `useMutation` result
- `onMutate`: Snapshot + optimistic removal
- `onError`: Reinsert task at original index, show error toast
- `onSettled`: Invalidate `['tasks', userId]`

#### useToggleTask
- **Returns**: TanStack `useMutation` result
- `onMutate`: Snapshot + optimistic `is_completed` flip
- `onError`: Revert toggle, show error toast
- `onSettled`: Invalidate `['tasks', userId]`

---

### Providers (`src/providers/`)

#### QueryProvider
- **Type**: Client Component (`'use client'`)
- **Behavior**: Wraps children in `<QueryClientProvider client={queryClient}>`. Creates query client with global 401 error handler.

#### UserProvider
- **Type**: Client Component (`'use client'`)
- **Props**: `user: { id: string, email: string }`
- **Behavior**: Provides user object via React Context. Children access via `useUser()` hook.

## Component Rendering Modes

| Component | Server Component | Client Component | Reason |
|---|:---:|:---:|---|
| Root Layout | x | | Static HTML shell, providers wrapper |
| (auth) Layout | x | | Static minimal layout |
| (dashboard) Layout | x | | Fetches /api/auth/me server-side |
| Dashboard Page | x | | Shell that renders TaskList |
| not-found | x | | Static 404 page |
| LoginForm | | x | useState, event handlers, router |
| RegisterForm | | x | useState, event handlers, router |
| TaskList | | x | TanStack Query hook, interactivity |
| TaskItem | | x | onClick handlers, state |
| EmptyState | x | | Pure presentation |
| TaskCreateModal | | x | Form state, modal interaction |
| TaskEditModal | | x | Form state, modal interaction |
| TaskDeleteModal | | x | Modal interaction, mutation |
| ThemeToggle | | x | useTheme hook, onClick |
| Button | | x | onClick handler |
| Input | | x | Form registration, onChange |
| Modal | | x | Radix Dialog (portal, focus trap) |
