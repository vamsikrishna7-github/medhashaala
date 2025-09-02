from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer for subscription plan details"""
    
    class Meta:
        model = None  # Will be set dynamically
        fields = ('id', 'name', 'features', 'price', 'is_active')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports
        from subscriptions.models import SubscriptionPlan
        self.Meta.model = SubscriptionPlan


class CustomUserCreateSerializer(UserCreateSerializer):
    """Custom serializer for user registration that accepts email OR phone"""
    
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'phone', 'name', 'password', 'role', 'subscription_plan')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
            'phone': {'required': False},
        }

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')
        
        if not email and not phone:
            raise serializers.ValidationError(
                "Either email or phone must be provided"
            )
        
        # Check if user with email already exists
        if email and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "A user with this email already exists"
            )
        
        # Check if user with phone already exists
        if phone and CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists"
            )
        
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            name=validated_data.get('name'),
            password=validated_data.get('password'),
            role=validated_data.get('role', 'user'),
            subscription_plan=validated_data.get('subscription_plan'),
        )
        return user


class CustomUserSerializer(UserSerializer):
    """Custom serializer for user profile"""
    
    subscription_plan = SubscriptionPlanSerializer(read_only=True)
    subscription_plan_name = serializers.CharField(read_only=True)
    current_subscription = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'phone', 'name', 'role', 'subscription_plan', 
                 'subscription_plan_name', 'current_subscription', 'enabled_features', 'date_joined')
    
    def get_current_subscription(self, obj):
        """Get current active subscription details"""
        subscription = obj.current_subscription
        if subscription:
            return {
                'id': subscription.id,
                'plan_name': subscription.plan.name,
                'status': subscription.status,
                'start_date': subscription.start_date,
                'end_date': subscription.end_date,
                'is_active': subscription.is_active,
                'remaining_days': subscription.get_remaining_days(),
            }
        return None


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer that accepts email OR phone for login"""
    
    username_field = 'login_field'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login_field'] = serializers.CharField()
        self.fields['password'] = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        login_field = attrs.get('login_field')
        password = attrs.get('password')
        
        if not login_field or not password:
            raise serializers.ValidationError(
                "Must include 'login_field' and 'password'"
            )
        
        # Try to find user by email or phone
        user = None
        if '@' in login_field:
            # Assume it's an email
            try:
                user = CustomUser.objects.get(email=login_field)
            except CustomUser.DoesNotExist:
                pass
        else:
            # Assume it's a phone number
            try:
                user = CustomUser.objects.get(phone=login_field)
            except CustomUser.DoesNotExist:
                pass
        
        if not user:
            raise serializers.ValidationError(
                "No user found with the provided email or phone number"
            )
        
        if not user.check_password(password):
            raise serializers.ValidationError(
                "Invalid password"
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                "User account is disabled"
            )
        
        # Set the user for the parent serializer
        self.user = user
        
        # Call parent validate method to get tokens
        data = super().validate(attrs)
        
        # Add user info to response
        data['user'] = CustomUserSerializer(user).data
        
        return data
