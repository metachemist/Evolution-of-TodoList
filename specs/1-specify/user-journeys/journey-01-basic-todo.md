# Journey 01: Basic Todo Management

## User Story
As a registered user, I want to manage my personal todo tasks so that I can organize and track my responsibilities.

## Actor
Registered user with authenticated account access

## Goal
Complete end-to-end task management including creation, viewing, updating, completing, and deleting tasks

## Prerequisites
- User has a registered account with valid email and password
- User is authenticated and has a valid JWT token
- User has access to the web application interface

## Trigger
User navigates to the todo application to manage their tasks

## Main Flow

### Step 1: Access Task Dashboard
- User visits the application URL
- System detects valid JWT token in localStorage
- System loads user's task dashboard
- User sees their existing tasks or empty state if no tasks exist

### Step 2: Create New Task
- User clicks "Create Task" or "+" button
- System displays task creation form
- User enters task title (1-200 characters)
- User optionally enters task description (0-1000 characters)
- User submits the form
- System validates input and user authentication
- System creates new task associated with user_id
- System displays success notification
- System adds task to the task list view

### Step 3: View Task List
- System retrieves user's tasks from database using user_id from JWT
- System displays tasks in chronological order (newest first)
- User sees all their tasks with titles, descriptions, and completion status
- System shows completion checkboxes for each task

### Step 4: Update Task
- User selects a task to edit
- System displays task editing interface
- User modifies the task title or description
- User saves the changes
- System validates user ownership and input
- System updates the task in the database
- System refreshes the task display

### Step 5: Complete Task
- User clicks the completion checkbox for a task
- System sends completion status update to backend
- System validates user ownership
- System updates the task completion status in database
- System updates the task's completion timestamp
- System reflects the change in the UI

### Step 6: Delete Task
- User selects a task for deletion
- System shows confirmation dialog
- User confirms deletion
- System validates user ownership
- System deletes the task from the database
- System removes the task from the UI

## Alternative Flows

### AF1: Empty Task List
- If user has no tasks, system displays "No tasks yet" message
- System offers "Create your first task" button or prominent creation option

### AF2: Invalid Input During Creation
- If user enters invalid title (too short or too long)
- System shows real-time validation feedback
- Form remains open with error highlighting
- User corrects input and resubmits

### AF3: Session Expiration
- If JWT token expires during activity
- System redirects user to login page with "Session expired" message
- User re-authenticates and returns to previous location

## Postconditions
- User's tasks are persisted in the database
- User can access their tasks across sessions
- Task ownership is maintained through user_id association
- Task completion status is preserved

## Success Criteria
- User can create tasks with proper validation
- User can view all their tasks in one place
- User can update task details as needed
- User can mark tasks as complete
- User can delete unwanted tasks
- All operations complete within 2 seconds
- User data remains isolated from other users

## Error Conditions
- Invalid input shows appropriate error messages
- Unauthorized access attempts are blocked
- Network failures show appropriate user feedback
- Database errors are handled gracefully

## Quality Attributes
- **Performance**: All operations complete within 2 seconds
- **Security**: User data isolation maintained at all times
- **Usability**: Intuitive interface with clear feedback
- **Reliability**: Data persists across sessions and device changes