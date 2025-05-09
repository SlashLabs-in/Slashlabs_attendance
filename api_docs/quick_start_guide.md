# SlashLabs Attendance System API Quick Start Guide

This quick start guide will help you get started with the SlashLabs Attendance System API quickly.

## Authentication

### 1. Obtain an API Token

Before you can use any of the protected API endpoints, you need to authenticate and get a token:

```
POST /api/login
```

Example with cURL:

```bash
curl -X POST 'https://your-domain.com/api/login' \
-H 'Content-Type: application/json' \
-d '{
    "username": "your_username",
    "password": "your_password"
}'
```

The response will include a JWT token:

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your.email@example.com",
    "full_name": "Your Name",
    "role": "employee"
  }
}
```

### 2. Using the Token

Include the token in the Authorization header for all subsequent requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Common API Tasks

### 1. Recording Attendance (Check-In)

To record a user's check-in:

```
POST /api/attendance/check-in
```

Example with cURL:

```bash
curl -X POST 'https://your-domain.com/api/attendance/check-in' \
-H 'Authorization: Bearer YOUR_TOKEN_HERE' \
-F 'location=Office Building, Floor 3' \
-F 'status=present'
```

### 2. Recording Attendance (Check-Out)

To record a user's check-out:

```
POST /api/attendance/check-out
```

Example with cURL:

```bash
curl -X POST 'https://your-domain.com/api/attendance/check-out' \
-H 'Authorization: Bearer YOUR_TOKEN_HERE' \
-F 'notes=Completed all tasks for the day'
```

### 3. Viewing Attendance History

To view a user's attendance history:

```
GET /api/attendance/history
```

Example with cURL:

```bash
curl -X GET 'https://your-domain.com/api/attendance/history' \
-H 'Authorization: Bearer YOUR_TOKEN_HERE'
```

### 4. Getting User Profile Information

To get the current user's profile information:

```
GET /api/users/profile
```

Example with cURL:

```bash
curl -X GET 'https://your-domain.com/api/users/profile' \
-H 'Authorization: Bearer YOUR_TOKEN_HERE'
```

### 5. Updating User Profile

To update the current user's profile:

```
PUT /api/users/profile
```

Example with cURL:

```bash
curl -X PUT 'https://your-domain.com/api/users/profile' \
-H 'Authorization: Bearer YOUR_TOKEN_HERE' \
-H 'Content-Type: application/json' \
-d '{
    "full_name": "Updated Name"
}'
```

## Error Handling

All API endpoints return standard HTTP status codes:

- 200/201: Success
- 400: Bad Request - Check your request parameters
- 401: Unauthorized - Invalid or missing token
- 404: Not Found - Resource not found
- 500: Server Error - Contact support

Error responses include a message explaining the error:

```json
{
  "message": "Error description here"
}
```

## Rate Limiting

API requests are limited to 100 requests per minute per user. If you exceed this limit, you will receive a 429 Too Many Requests response.

## Need Help?

For additional help or support:

1. Check the full API documentation
2. Review code examples in the `code_examples.md` file
3. Import the Postman collection for testing
4. Refer to the OpenAPI specification for detailed endpoint information

For technical assistance, contact the support team at support@attendance-system.com.
