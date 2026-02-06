# User Entity

## Entity Overview
The User entity represents individuals who interact with the todo application. Each user has a unique identity and owns their personal todo tasks.

## Attributes

### Required Attributes
- **id** (UUID/string): Unique identifier for the user; auto-generated
- **email** (string): User's email address for authentication; unique across system
- **password_hash** (string): Securely hashed password using bcrypt with cost factor 12

### Optional Attributes
- **created_at** (timestamp): Timestamp when user account was created; auto-generated
- **updated_at** (timestamp): Timestamp when user account was last updated; auto-generated

## Relationships
- **One-to-Many**: A user can have many tasks (user has many tasks)
- **Tasks**: Associated task records owned by the user

## Business Rules
1. **Uniqueness**: Email addresses must be unique across all users
2. **Authentication**: Email and password combination required for authentication
3. **Password Security**: Passwords must be hashed using bcrypt with cost factor 12 before storage
4. **Email Validation**: Email addresses must follow RFC 5322 format standards
5. **Password Requirements**: Minimum 8 characters with uppercase, lowercase, numbers, and special characters

## Access Control
- **Ownership**: Users can only access their own tasks and user data
- **JWT Claims**: User ID included in JWT tokens for authorization validation
- **Isolation**: Strict enforcement of user data boundaries via user_id validation

## Lifecycle
- **Creation**: Occurs during user registration process
- **Authentication**: Verified during login with bcrypt password comparison
- **Data Association**: All tasks are linked to user via user_id foreign key

## Security Considerations
- **No Plain Text Storage**: Passwords never stored in plain text
- **Token Association**: User identity maintained in JWT tokens for session management
- **Rate Limiting**: Login attempts limited to prevent brute force attacks