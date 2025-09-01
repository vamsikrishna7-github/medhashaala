from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription
from django.contrib.auth import get_user_model

User = get_user_model()


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer for SubscriptionPlan model"""
    
    feature_count = serializers.ReadOnlyField()
    
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'features', 'price', 'is_active', 
            'feature_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_features(self, value):
        """Validate that features is a list"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Features must be a list")
        return value
    
    def validate_price(self, value):
        """Validate that price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for UserSubscription model"""
    
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    plan = SubscriptionPlanSerializer(read_only=True)
    plan_id = serializers.IntegerField(write_only=True)
    is_active = serializers.ReadOnlyField()
    remaining_days = serializers.ReadOnlyField()
    
    class Meta:
        model = UserSubscription
        fields = [
            'id', 'user', 'plan', 'plan_id', 'start_date', 'end_date', 
            'status', 'is_active', 'remaining_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'start_date', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Custom validation for user subscription"""
        # Check if plan exists and is active
        plan_id = data.get('plan_id')
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
            if not plan.is_active:
                raise serializers.ValidationError("Cannot subscribe to inactive plan")
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Invalid plan ID")
        
        # Check for existing active subscription
        user = data.get('user')
        if UserSubscription.objects.filter(user=user, status='active').exists():
            raise serializers.ValidationError("User already has an active subscription")
        
        return data
    
    def create(self, validated_data):
        """Create user subscription with plan"""
        plan_id = validated_data.pop('plan_id')
        plan = SubscriptionPlan.objects.get(id=plan_id)
        validated_data['plan'] = plan
        return super().create(validated_data)


class UserSubscriptionReadSerializer(serializers.ModelSerializer):
    """Read-only serializer for user's own subscription"""
    
    plan = SubscriptionPlanSerializer(read_only=True)
    is_active = serializers.ReadOnlyField()
    remaining_days = serializers.ReadOnlyField()
    
    class Meta:
        model = UserSubscription
        fields = [
            'id', 'plan', 'start_date', 'end_date', 'status', 
            'is_active', 'remaining_days', 'created_at'
        ]
        read_only_fields = fields
