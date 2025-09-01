# Subscriptions API Documentation

## Overview

The Subscriptions API provides endpoints for managing subscription plans and user subscriptions in a school management system. All endpoints require authentication.

## Authentication

The API supports both session authentication and token authentication:

- **Session Authentication**: Use Django's session-based authentication
- **Token Authentication**: Include `Authorization: Token YOUR_TOKEN` header

## Base URL

```
http://127.0.0.1:8000/api/
```

## Endpoints

### Subscription Plans

#### List All Plans
**GET** `/plans/`

Returns a paginated list of subscription plans. Regular users see only active plans, while admin users see all plans.

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Basic",
      "features": ["feature1", "feature2"],
      "price": "9.99",
      "is_active": true,
      "feature_count": 2,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Get Single Plan
**GET** `/plans/{id}/`

Returns details of a specific subscription plan.

**Response:**
```json
{
  "id": 1,
  "name": "Basic",
  "features": ["feature1", "feature2"],
  "price": "9.99",
  "is_active": true,
  "feature_count": 2,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Create Plan (Admin Only)
**POST** `/plans/`

Creates a new subscription plan.

**Request Body:**
```json
{
  "name": "Basic",
  "features": ["feature1", "feature2"],
  "price": "9.99",
  "is_active": true
}
```

**Response:** Returns the created plan object.

#### Update Plan (Admin Only)
**PUT** `/plans/{id}/`

Updates an existing subscription plan.

**Request Body:**
```json
{
  "name": "Basic",
  "features": ["feature1", "feature2", "feature3"],
  "price": "12.99",
  "is_active": true
}
```

**Response:** Returns the updated plan object.

#### Delete Plan (Admin Only)
**DELETE** `/plans/{id}/`

Deletes a subscription plan.

**Response:** 204 No Content

#### Enable/Disable Plan (Admin Only)
**POST** `/plans/{id}/enable_disable/`

Enables or disables a subscription plan.

**Request Body:**
```json
{
  "is_active": false
}
```

**Response:** Returns the updated plan object.

### User Subscriptions

#### Get Current User Subscription
**GET** `/user-subscriptions/`

Returns the current user's active subscription. Returns 404 if no active subscription exists.

**Response:**
```json
{
  "id": 1,
  "plan": {
    "id": 1,
    "name": "Basic",
    "features": ["feature1", "feature2"],
    "price": "9.99",
    "is_active": true,
    "feature_count": 2,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-12-31T23:59:59Z",
  "status": "active",
  "is_active": true,
  "remaining_days": 365,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Get My Subscription Details
**GET** `/user-subscriptions/my_subscription/`

Alternative endpoint to get current user's subscription details.

**Response:** Same as above.

### Admin Endpoints (Admin Only)

#### List All Subscriptions
**GET** `/admin/subscriptions/`

Returns a paginated list of all user subscriptions.

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "plan": {
        "id": 1,
        "name": "Basic",
        "features": ["feature1", "feature2"],
        "price": "9.99",
        "is_active": true,
        "feature_count": 2,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      },
      "plan_id": 1,
      "start_date": "2024-01-01T00:00:00Z",
      "end_date": "2024-12-31T23:59:59Z",
      "status": "active",
      "is_active": true,
      "remaining_days": 365,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Create User Subscription
**POST** `/admin/subscriptions/`

Creates a new subscription for a user.

**Request Body:**
```json
{
  "user": 1,
  "plan_id": 1,
  "end_date": "2024-12-31T23:59:59Z",
  "status": "active"
}
```

**Response:** Returns the created subscription object.

#### Update User Subscription
**PUT** `/admin/subscriptions/{id}/`

Updates an existing user subscription.

**Request Body:**
```json
{
  "user": 1,
  "plan_id": 2,
  "end_date": "2024-12-31T23:59:59Z",
  "status": "active"
}
```

**Response:** Returns the updated subscription object.

#### Delete User Subscription
**DELETE** `/admin/subscriptions/{id}/`

Deletes a user subscription.

**Response:** 204 No Content

#### Cancel Subscription
**POST** `/admin/subscriptions/{id}/cancel/`

Cancels a user subscription by setting status to 'cancelled'.

**Response:** Returns the updated subscription object.

#### Renew Subscription
**POST** `/admin/subscriptions/{id}/renew/`

Renews a user subscription and optionally updates the end date.

**Request Body (optional):**
```json
{
  "end_date": "2025-12-31T23:59:59Z"
}
```

**Response:** Returns the updated subscription object.

## Error Responses

### 400 Bad Request
```json
{
  "error": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **204 No Content**: Request successful, no content returned
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Pagination

List endpoints return paginated results with the following structure:

```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/plans/?page=2",
  "previous": null,
  "results": [...]
}
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## Examples

### cURL Examples

#### List Plans
```bash
curl -X GET http://127.0.0.1:8000/api/plans/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

#### Create Plan
```bash
curl -X POST http://127.0.0.1:8000/api/plans/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Basic",
    "features": ["feature1", "feature2"],
    "price": "9.99",
    "is_active": true
  }'
```

#### Get User Subscription
```bash
curl -X GET http://127.0.0.1:8000/api/user-subscriptions/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

#### Create User Subscription (Admin)
```bash
curl -X POST http://127.0.0.1:8000/api/admin/subscriptions/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "plan_id": 1,
    "end_date": "2024-12-31T23:59:59Z",
    "status": "active"
  }'
```

### Python Examples

#### Using requests library
```python
import requests

# List plans
response = requests.get(
    'http://127.0.0.1:8000/api/plans/',
    headers={'Authorization': 'Token YOUR_TOKEN'}
)
plans = response.json()

# Create plan
response = requests.post(
    'http://127.0.0.1:8000/api/plans/',
    headers={'Authorization': 'Token YOUR_TOKEN'},
    json={
        'name': 'Basic',
        'features': ['feature1', 'feature2'],
        'price': '9.99',
        'is_active': True
    }
)
new_plan = response.json()
```

## Notes

- All timestamps are in ISO 8601 format (UTC)
- Decimal fields are returned as strings to preserve precision
- The `features` field is a JSON array of feature names
- The `is_active` property on UserSubscription is computed based on status and end_date
- Admin users have access to all endpoints, regular users have read-only access to plans and their own subscriptions
