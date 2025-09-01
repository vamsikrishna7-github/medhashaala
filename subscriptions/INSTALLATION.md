# Subscriptions App Installation Guide

## Quick Setup

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

Ensure your REST framework settings include session authentication:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Add this
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
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
    path('', include('subscriptions.urls')),  # Add this line
]
```

### 4. Run Migrations

```bash
python manage.py makemigrations subscriptions
python manage.py migrate
```

### 5. Create Sample Data

```bash
python manage.py setup_subscriptions
```

### 6. Create Superuser (if not exists)

```bash
python manage.py createsuperuser
```

## Testing the Installation

### Run Tests

```bash
python manage.py test subscriptions
```

### Test API Endpoints

1. **List Plans** (requires authentication):
```bash
curl -X GET http://127.0.0.1:8000/api/plans/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

2. **Get User Subscription** (requires authentication):
```bash
curl -X GET http://127.0.0.1:8000/api/user-subscriptions/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

3. **Admin: List All Subscriptions** (requires admin authentication):
```bash
curl -X GET http://127.0.0.1:8000/api/admin/subscriptions/ \
  -H "Authorization: Token ADMIN_TOKEN" \
  -H "Content-Type: application/json"
```

## Features Available

- ✅ Subscription plan management (Basic, Standard, Premium)
- ✅ User subscription tracking
- ✅ Feature access control
- ✅ Admin interface
- ✅ REST API with proper permissions
- ✅ Comprehensive test suite
- ✅ Management commands for setup
- ✅ Utility functions for feature checking

## Next Steps

1. **Customize Features**: Modify the features list in the management command
2. **Add Payment Integration**: Integrate with payment gateways
3. **Add Notifications**: Set up email/SMS notifications for subscription events
4. **Add Analytics**: Track subscription metrics and usage
5. **Add Webhooks**: Implement webhooks for subscription events

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'subscriptions'**
   - Make sure the app is added to INSTALLED_APPS
   - Check that the app directory is in your Python path

2. **Authentication errors**
   - Ensure session authentication is enabled in REST_FRAMEWORK settings
   - Check that users are properly authenticated

3. **Permission errors**
   - Verify user has appropriate permissions (admin for admin endpoints)
   - Check that the custom user model is properly configured

4. **Migration errors**
   - Delete existing migrations and recreate them
   - Ensure the custom user model is properly referenced

### Getting Help

- Check the test suite for usage examples
- Review the API documentation in `api_docs.md`
- Check the README.md for comprehensive documentation
