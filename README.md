# MedhaShaala - Authentication System

A Django-based authentication system using Djoser + SimpleJWT with support for email or phone-based login.

## Features

- **Custom User Model**: UUID-based user model with email/phone authentication
- **JWT Authentication**: Secure token-based authentication using SimpleJWT
- **Flexible Login**: Login with either email or phone number
- **Role-based Access**: User roles (super_admin, admin, user)
- **Subscription Plans**: Different subscription tiers (base, standard, premium)
- **API Documentation**: Auto-generated API docs using drf-spectacular

## Tech Stack

- Django 5.2.5
- Django REST Framework 3.16.1
- Djoser 2.2.1 (Authentication endpoints)
- SimpleJWT 5.5.1 (JWT tokens)
- drf-spectacular 0.28.0 (API documentation)

## Project Setup

### 1. Clone and Install Dependencies

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser
```

### 3. Run the Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/users/` | POST | Register a new user |
| `/api/auth/jwt/create/` | POST | Login (get JWT tokens) |
| `/api/auth/jwt/refresh/` | POST | Refresh JWT token |
| `/api/auth/jwt/verify/` | POST | Verify JWT token |
| `/api/auth/users/me/` | GET | Get current user profile |
| `/api/auth/users/me/` | PUT/PATCH | Update current user profile |
| `/api/auth/users/reset_password/` | POST | Request password reset |
| `/api/auth/users/reset_password_confirm/` | POST | Confirm password reset |

### Documentation Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/schema/` | OpenAPI schema |
| `/api/docs/` | Swagger UI documentation |
| `/api/redoc/` | ReDoc documentation |

## User Model Fields

- `id`: UUID primary key
- `email`: Email address (unique, optional)
- `phone`: Phone number (unique, optional)
- `name`: Full name (required)
- `role`: User role (super_admin, admin, user)
- `subscription_plan`: Subscription tier (base, standard, premium)
- `enabled_features`: JSON field for feature flags
- `is_active`: Account status
- `date_joined`: Registration date

## API Usage Examples

### 1. Register a New User

```bash
curl -X POST http://127.0.0.1:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "password": "securepassword123",
    "re_password": "securepassword123",
    "role": "user",
    "subscription_plan": "base"
  }'
```

### 2. Login with Email

```bash
curl -X POST http://127.0.0.1:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### 3. Login with Phone

```bash
curl -X POST http://127.0.0.1:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1234567890",
    "password": "securepassword123"
  }'
```

### 4. Get User Profile

```bash
curl -X GET http://127.0.0.1:8000/api/auth/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Refresh Token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/jwt/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```

## JWT Token Configuration

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 1 day
- **Algorithm**: HS256
- **Token Type**: Bearer

## Custom Features

### Email or Phone Login
The system supports login with either email or phone number. Users can register with either field, and both can be used for authentication.

### Role-based Access
Users have different roles with varying permissions:
- `super_admin`: Full system access
- `admin`: Administrative access
- `user`: Standard user access

### Subscription Plans
Users can have different subscription tiers:
- `base`: Basic features
- `standard`: Enhanced features
- `premium`: Full feature access

## Development

### Creating a Superuser

```bash
python manage.py createsuperuser
```

### Running Tests

```bash
python manage.py test
```

### Database Reset

```bash
# Remove existing database
rm db.sqlite3

# Recreate migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Production Considerations

1. **Security**: Change `SECRET_KEY` in production
2. **Database**: Use PostgreSQL or MySQL in production
3. **HTTPS**: Always use HTTPS in production
4. **Token Expiry**: Adjust JWT token lifetimes as needed
5. **CORS**: Configure CORS settings for frontend integration
6. **Environment Variables**: Use environment variables for sensitive settings

## License

This project is licensed under the MIT License.
