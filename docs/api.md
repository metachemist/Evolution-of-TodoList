# API Documentation

## Overview
This is a Multi-User Todo REST API built with FastAPI, SQLModel, and Neon PostgreSQL. The API provides full CRUD operations for tasks with proper user isolation and authentication middleware.

## Authentication
All endpoints require JWT token authentication. Include the token in the Authorization header as follows:
```
Authorization: Bearer <your-jwt-token>
```

## Base URL
```
https://api.yourdomain.com/api/{user_id}/
```

## Endpoints

### GET /api/{user_id}/tasks
Retrieve all tasks for the specified user.

**Response**: `200 OK`
```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "is_completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "owner_id": "uuid-string"
  }
]
```

### POST /api/{user_id}/tasks
Create a new task for the specified user.

**Request Body**:
```json
{
  "title": "New task title",
  "description": "New task description"
}
```

**Response**: `201 Created`
```json
{
  "id": "uuid-string",
  "title": "New task title",
  "description": "New task description",
  "is_completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "owner_id": "uuid-string"
}
```

### GET /api/{user_id}/tasks/{task_id}
Retrieve a specific task for the specified user.

**Response**: `200 OK`
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "is_completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "owner_id": "uuid-string"
}
```

### PUT /api/{user_id}/tasks/{task_id}
Update a specific task for the specified user.

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

**Response**: `200 OK`
```json
{
  "id": "uuid-string",
  "title": "Updated task title",
  "description": "Updated task description",
  "is_completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "owner_id": "uuid-string"
}
```

### DELETE /api/{user_id}/tasks/{task_id}
Delete a specific task for the specified user.

**Response**: `204 No Content`

### PATCH /api/{user_id}/tasks/{task_id}/complete
Toggle the completion status of a specific task for the specified user.

**Response**: `200 OK`
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "is_completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "owner_id": "uuid-string"
}
```

## Error Handling
All error responses follow the same structure:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {} // Optional additional details
  }
}
```

## Rate Limiting
The API implements rate limiting to prevent abuse. Users are limited to 1000 requests per hour per user.

## Security
- All user data is isolated - users can only access their own tasks
- JWT tokens are validated on every request
- User ID in URL path is verified against JWT claims