# Conversation Entity

## Entity Overview
The Conversation entity represents AI-powered chat interactions between users and the todo application. This entity is prepared for Phase III implementation of AI chatbot functionality.

## Attributes

### Required Attributes
- **id** (UUID/string): Unique identifier for the conversation; auto-generated
- **user_id** (UUID/string): Foreign key linking to the user who initiated the conversation; required
- **created_at** (timestamp): Timestamp when conversation was started; auto-generated

### Optional Attributes
- **title** (string): Conversation title or summary; 0-200 characters
- **updated_at** (timestamp): Timestamp when conversation was last updated; auto-generated
- **status** (string): Current status of conversation (active, archived, pending); defaults to 'active'

## Relationships
- **Many-to-One**: Many conversations belong to one user (many conversations -> one user)
- **Messages**: Associated message records within this conversation
- **User**: The user who owns this conversation

## Business Rules
1. **Ownership**: Each conversation must be associated with a valid user_id
2. **User Isolation**: Users can only access conversations they own
3. **Status Management**: Conversations can be active, archived, or pending
4. **Title Requirements**: Title can be 0-200 characters

## State Transitions
- **Active**: Currently ongoing conversation
- **Archived**: Completed conversation moved to archive
- **Pending**: Conversation awaiting response

## Validation Rules
- **User Ownership**: user_id must match authenticated user during operations
- **Title Length**: 0-200 characters if provided
- **Required Fields**: user_id and created_at are required

## Access Control
- **Owner Only**: Users can only access, modify, or delete their own conversations
- **JWT Validation**: user_id in JWT token validated against conversation user_id
- **Authorization**: All operations require valid authentication and user_id matching

## Lifecycle
- **Creation**: New conversation with user_id association
- **Activity**: Messages added to conversation
- **Archival**: Conversation moved to archived state
- **Deletion**: Permanent removal by authorized owner

## Future Considerations (Phase III+)
- Integration with AI chatbot functionality
- Message threading within conversations
- Conversation analytics and insights
- Export capabilities for conversation history