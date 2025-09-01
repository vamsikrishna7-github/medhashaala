# Django Subscriptions App

A complete Django application for managing subscription plans in a school management system. This app provides subscription plan management, user subscription tracking, and feature access control.

## Features

- **Subscription Plan Management**: Create, update, and manage subscription plans (Basic, Standard, Premium)
- **User Subscription Tracking**: Track user subscriptions with start/end dates and status
- **Feature Access Control**: Control feature access based on subscription plans
- **Admin Interface**: Full admin interface for managing plans and subscriptions
- **REST API**: Complete REST API with proper permissions and authentication
- **Permission System**: Different access levels for admin users and regular users

## Models

### SubscriptionPlan
- `name`: Plan name (Basic, Standard, Premium)
- `features`: JSON field storing enabled features list
- `price`: Decimal field for plan pricing
- `is_active`: Boolean to enable/disable plans
- `created_at`, `updated_at`: Timestamps

### UserSubscription
- `user`: ForeignKey to Django User
- `plan`: ForeignKey to SubscriptionPlan
- `start_date`, `end_date`: Subscription period
- `status`: Subscription status (active, expired, cancelled)
- `created_at`, `updated_at`: Timestamps

## Setup Instructions

### 1. Add to INSTALLED_APPS

Add the subscriptions app to your Django settings:

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'subscriptions',  # Add this line
]
```

### 2. Configure REST Framework

Add REST Framework settings to your Django settings:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### 3. Include URLs

Add the subscriptions URLs to your main URL configuration:

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('subscriptions.urls')),
]
```

### 4. Run Migrations

```bash
python manage.py makemigrations subscriptions
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Create Sample Data

You can create sample subscription plans through the Django admin interface or using Django shell:

```python
# Create sample plans
from subscriptions.models import SubscriptionPlan

# Basic Plan
basic_plan = SubscriptionPlan.objects.create(
    name='Basic',
    features=['basic_features', 'email_support'],
    price=9.99,
    is_active=True
)

# Standard Plan
standard_plan = SubscriptionPlan.objects.create(
    name='Standard',
    features=['basic_features', 'advanced_features', 'email_support', 'phone_support'],
    price=19.99,
    is_active=True
)

# Premium Plan
premium_plan = SubscriptionPlan.objects.create(
    name='Premium',
    features=['basic_features', 'advanced_features', 'premium_features', 'email_support', 'phone_support', 'priority_support'],
    price=39.99,
    is_active=True
)
```

## API Endpoints

### Authentication
All endpoints require authentication. Use session authentication or token authentication.

### Subscription Plans

#### List All Plans
```bash
curl -X GET http://127.0.0.1:8000/api/plans/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

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
      "features": ["basic_features", "email_support"],
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
```bash
curl -X GET http://127.0.0.1:8000/api/plans/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

#### Create Plan (Admin Only)
```bash
curl -X POST http://127.0.0.1:8000/api/plans/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Basic",
    "features": ["basic_features", "email_support"],
    "price": "9.99",
    "is_active": true
  }'
```

#### Update Plan (Admin Only)
```bash
curl -X PUT http://127.0.0.1:8000/api/plans/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Basic",
    "features": ["basic_features", "email_support", "new_feature"],
    "price": "12.99",
    "is_active": true
  }'
```

#### Enable/Disable Plan (Admin Only)
```bash
curl -X POST http://127.0.0.1:8000/api/plans/1/enable_disable/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

### User Subscriptions

#### Get Current User Subscription
```bash
curl -X GET http://127.0.0.1:8000/api/user-subscriptions/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "id": 1,
  "plan": {
    "id": 1,
    "name": "Basic",
    "features": ["basic_features", "email_support"],
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
```bash
curl -X GET http://127.0.0.1:8000/api/user-subscriptions/my_subscription/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### Admin Endpoints (Admin Only)

#### List All Subscriptions
```bash
curl -X GET http://127.0.0.1:8000/api/admin/subscriptions/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

#### Create User Subscription
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

#### Update User Subscription
```bash
curl -X PUT http://127.0.0.1:8000/api/admin/subscriptions/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "plan_id": 2,
    "end_date": "2024-12-31T23:59:59Z",
    "status": "active"
  }'
```

#### Cancel Subscription
```bash
curl -X POST http://127.0.0.1:8000/api/admin/subscriptions/1/cancel/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

#### Renew Subscription
```bash
curl -X POST http://127.0.0.1:8000/api/admin/subscriptions/1/renew/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"end_date": "2025-12-31T23:59:59Z"}'
```

## Permissions

### Regular Users
- View available subscription plans (active only)
- View their own subscription details
- Read-only access to subscription information

### Admin Users
- Full CRUD access to subscription plans
- Full CRUD access to user subscriptions
- Enable/disable subscription plans
- Cancel and renew user subscriptions
- View all subscriptions and plans

## Usage Examples

### Check User Feature Access

```python
from subscriptions.models import UserSubscription

def has_feature_access(user, feature_name):
    """Check if user has access to a specific feature"""
    try:
        subscription = UserSubscription.objects.get(
            user=user, 
            status='active'
        )
        return feature_name in subscription.plan.features
    except UserSubscription.DoesNotExist:
        return False

# Usage
if has_feature_access(request.user, 'premium_features'):
    # User has access to premium features
    pass
else:
    # User doesn't have access
    pass
```

### Get User's Current Plan

```python
def get_user_plan(user):
    """Get user's current subscription plan"""
    try:
        subscription = UserSubscription.objects.get(
            user=user, 
            status='active'
        )
        return subscription.plan
    except UserSubscription.DoesNotExist:
        return None

# Usage
plan = get_user_plan(request.user)
if plan:
    print(f"User is on {plan.name} plan with {plan.feature_count} features")
```

## Admin Interface

The app provides a comprehensive admin interface at `/admin/`:

- **Subscription Plans**: Create, edit, and manage subscription plans
- **User Subscriptions**: View and manage user subscriptions
- **Bulk Actions**: Activate, deactivate, or cancel multiple subscriptions
- **Filtering**: Filter by status, plan, dates, etc.
- **Search**: Search by username, email, or plan name

## Testing

Run the test suite:

```bash
python manage.py test subscriptions
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
