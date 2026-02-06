# Task Entity

## Entity Overview
The Task entity represents individual todo items that users can create, manage, and complete. Each task is owned by a single user.

## Attributes

### Required Attributes
- **id** (integer): Auto-incrementing unique identifier for the task
- **user_id** (UUID/string): Foreign key linking to the owning user; required
- **title** (string): Task title; 1-200 characters after trimming whitespace

### Optional Attributes
- **description** (string): Optional task description; 0-1000 characters
- **completed** (boolean): Completion status; defaults to false
- **created_at** (timestamp): Timestamp when task was created; auto-generated
- **updated_at** (timestamp): Timestamp when task was last updated; auto-generated

## Relationships
- **Many-to-One**: Many tasks belong to one user (many tasks -> one user)
- **User**: The user who owns this task

## Business Rules
1. **Ownership**: Each task must be associated with a valid user_id
2. **Title Requirements**: Title must be 1-200 characters after trimming whitespace
3. **Description Limits**: Description can be 0-1000 characters
4. **Completion Status**: Default value is false; can be toggled to true
5. **User Isolation**: Users can only access tasks they own

## State Transitions
- **Created**: Task is initially created with completed = false
- **Updated**: Task details can be modified while maintaining ownership
- **Completed**: Task completion status can be toggled
- **Deleted**: Task can be permanently removed by owner

## Validation Rules
- **Title Length**: 1-200 characters (after trimming)
- **Description Length**: 0-1000 characters
- **User Ownership**: user_id must match authenticated user during operations
- **Required Fields**: Only title is required for creation

## Access Control
- **Owner Only**: Users can only access, modify, or delete their own tasks
- **JWT Validation**: user_id in JWT token validated against task user_id
- **Authorization**: All operations require valid authentication and user_id matching

## Lifecycle
- **Creation**: New task with user_id association and default completion status
- **Modification**: Title/description updates with preservation of ownership
- **Completion**: Toggle completion status with timestamp update
- **Deletion**: Permanent removal by authorized owner