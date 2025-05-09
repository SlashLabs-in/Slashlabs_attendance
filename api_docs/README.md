# SlashLabs Attendance System API Documentation

## Overview

This document provides information about the SlashLabs Attendance System's API endpoints. The API allows mobile applications and other systems to interact with the SlashLabs Attendance, enabling check-ins, check-outs, and data retrieval.

## Base URL

```
https://your-domain.com/api
```

## Authentication

The API uses JSON Web Tokens (JWT) for authentication. To access protected endpoints, you must include the JWT token in the Authorization header of your request.

### Token Format

```
Authorization: Bearer YOUR_TOKEN_HERE
```

### Getting a Token

To get a token, make a POST request to the `/api/login` endpoint with valid credentials.

---

## Endpoints

### Authentication

#### Login

Authenticate a user and retrieve a JWT token.

- **URL**: `/login`
- **Method**: `POST`
- **Authentication**: None
- **Content-Type**: `application/json`

**Request Body**:

```json
{
  "username": "string",
  "password": "string"
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "token": "string",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "full_name": "string",
    "role": "string"
  }
}
```

**Error Response**:

- **Code**: 401 Unauthorized
- **Content**:

```json
{
  "message": "Authentication failed. Invalid credentials."
}
```

---

### Attendance

#### Check-In

Record a user's check-in to work.

- **URL**: `/attendance/check-in`
- **Method**: `POST`
- **Authentication**: Required
- **Content-Type**: `multipart/form-data`

**Request Parameters**:

| Parameter | Type   | Required | Description                            |
| --------- | ------ | -------- | -------------------------------------- |
| image     | File   | No       | Image file to capture during check-in  |
| location  | String | No       | Location description or coordinates    |
| status    | String | No       | Attendance status (default: 'present') |
| notes     | String | No       | Additional notes about the check-in    |

**Success Response**:

- **Code**: 201 Created
- **Content**:

```json
{
  "message": "Check-in successful",
  "attendance": {
    "id": "integer",
    "check_in_time": "datetime",
    "status": "string"
  }
}
```

**Error Response**:

- **Code**: 400 Bad Request
- **Content**:

```json
{
  "message": "You are already checked in today."
}
```

#### Check-Out

Record a user's check-out from work.

- **URL**: `/attendance/check-out`
- **Method**: `POST`
- **Authentication**: Required
- **Content-Type**: `multipart/form-data`

**Request Parameters**:

| Parameter | Type   | Required | Description                            |
| --------- | ------ | -------- | -------------------------------------- |
| image     | File   | No       | Image file to capture during check-out |
| notes     | String | No       | Additional notes about the check-out   |

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Check-out successful",
  "attendance": {
    "id": "integer",
    "check_in_time": "datetime",
    "check_out_time": "datetime",
    "status": "string"
  }
}
```

**Error Response**:

- **Code**: 404 Not Found
- **Content**:

```json
{
  "message": "No active check-in found for today."
}
```

#### Get Attendance History

Retrieve a user's attendance history.

- **URL**: `/attendance/history`
- **Method**: `GET`
- **Authentication**: Required

**Query Parameters**:

| Parameter  | Type    | Required | Description                                 |
| ---------- | ------- | -------- | ------------------------------------------- |
| page       | Integer | No       | Page number for pagination (default: 1)     |
| per_page   | Integer | No       | Records per page (default: 10)              |
| start_date | String  | No       | Filter records from this date (YYYY-MM-DD)  |
| end_date   | String  | No       | Filter records until this date (YYYY-MM-DD) |

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "attendances": [
    {
      "id": "integer",
      "check_in_time": "datetime",
      "check_out_time": "datetime",
      "status": "string",
      "image_path": "string",
      "location": "string",
      "notes": "string"
    }
  ],
  "total": "integer",
  "pages": "integer",
  "current_page": "integer"
}
```

---

### User Profile

#### Get Profile

Retrieve the current user's profile information.

- **URL**: `/users/profile`
- **Method**: `GET`
- **Authentication**: Required

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "string",
  "department": "string",
  "position": "string"
}
```

#### Update Profile

Update the current user's profile information.

- **URL**: `/users/profile`
- **Method**: `PUT`
- **Authentication**: Required
- **Content-Type**: `application/json`

**Request Body**:

```json
{
  "email": "string",
  "full_name": "string",
  "password": "string"
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "full_name": "string"
  }
}
```

**Error Response**:

- **Code**: 400 Bad Request
- **Content**:

```json
{
  "message": "Email already in use."
}
```

---

## Status Codes

| Status Code | Description                                       |
| ----------- | ------------------------------------------------- |
| 200         | OK - The request has succeeded                    |
| 201         | Created - The request has been fulfilled          |
| 400         | Bad Request - The request could not be understood |
| 401         | Unauthorized - Authentication is required         |
| 404         | Not Found - The requested resource was not found  |
| 500         | Server Error - An error occurred on the server    |

---

## Data Models

### User

| Field      | Type    | Description                     |
| ---------- | ------- | ------------------------------- |
| id         | Integer | Unique identifier               |
| username   | String  | Unique username                 |
| email      | String  | User's email address            |
| full_name  | String  | User's full name                |
| role       | String  | User's role (admin or employee) |
| department | String  | User's department               |
| position   | String  | User's job position             |

### Attendance

| Field          | Type     | Description                               |
| -------------- | -------- | ----------------------------------------- |
| id             | Integer  | Unique identifier                         |
| user_id        | Integer  | ID of the user                            |
| check_in_time  | Datetime | Time of check-in                          |
| check_out_time | Datetime | Time of check-out (can be null)           |
| status         | String   | Attendance status (present, late, absent) |
| image_path     | String   | Path to the uploaded image                |
| location       | String   | Location information                      |
| notes          | String   | Additional notes                          |

---

## Error Handling

All error responses will contain a JSON object with a `message` field explaining the error.

Example:

```json
{
  "message": "Authentication failed. Invalid credentials."
}
```

---

## Rate Limiting

API requests are limited to 100 requests per minute per user. If you exceed this limit, you will receive a 429 Too Many Requests response.

---

## Security Guidelines

- Always use HTTPS to ensure secure data transmission
- Protect your API tokens and never expose them in client-side code
- Tokens expire after 24 hours and will need to be renewed
- Implement proper error handling in your client applications

---

For more information or technical support, please contact our development team.
