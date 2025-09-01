from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import SubscriptionPlan, UserSubscription
from .serializers import (
    SubscriptionPlanSerializer, 
    UserSubscriptionSerializer, 
    UserSubscriptionReadSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow admin users full access,
    but only read access for regular users.
    """
    
    def has_permission(self, request, view):
        # Allow read access for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Allow full access for admin users
        return request.user.is_staff


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing subscription plans.
    
    - GET /api/plans/ - List all active plans (all users)
    - GET /api/plans/{id}/ - Retrieve specific plan (all users)
    - POST /api/plans/ - Create new plan (admin only)
    - PUT/PATCH /api/plans/{id}/ - Update plan (admin only)
    - DELETE /api/plans/{id}/ - Delete plan (admin only)
    """
    
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_queryset(self):
        """Filter plans based on user permissions"""
        if self.request.user.is_staff:
            # Admin users can see all plans
            return SubscriptionPlan.objects.all()
        else:
            # Regular users can only see active plans
            return SubscriptionPlan.objects.filter(is_active=True)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def enable_disable(self, request, pk=None):
        """
        Enable or disable a subscription plan.
        
        POST /api/plans/{id}/enable_disable/
        Body: {"is_active": true/false}
        """
        plan = self.get_object()
        is_active = request.data.get('is_active')
        
        if is_active is None:
            return Response(
                {'error': 'is_active field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plan.is_active = bool(is_active)
        plan.save()
        
        serializer = self.get_serializer(plan)
        return Response(serializer.data)


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user subscriptions.
    
    - GET /api/user-subscriptions/ - Get current user's subscription (all users)
    - GET /api/admin/subscriptions/ - List all subscriptions (admin only)
    - POST /api/admin/subscriptions/ - Create subscription (admin only)
    - PUT/PATCH /api/admin/subscriptions/{id}/ - Update subscription (admin only)
    - DELETE /api/admin/subscriptions/{id}/ - Delete subscription (admin only)
    """
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter subscriptions based on user permissions"""
        if self.request.user.is_staff:
            # Admin users can see all subscriptions
            return UserSubscription.objects.all()
        else:
            # Regular users can only see their own subscription
            return UserSubscription.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializers based on user permissions"""
        if self.request.user.is_staff:
            return UserSubscriptionSerializer
        else:
            return UserSubscriptionReadSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Admin actions require admin permissions
            return [IsAdminUser()]
        else:
            # Read actions require authentication
            return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        """Override list to handle user's own subscription"""
        if not request.user.is_staff:
            # For regular users, return their current subscription
            subscription = UserSubscription.objects.filter(
                user=request.user, 
                status='active'
            ).first()
            
            if subscription:
                serializer = self.get_serializer(subscription)
                return Response(serializer.data)
            else:
                return Response(
                    {'message': 'No active subscription found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # For admin users, return all subscriptions
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_subscription(self, request):
        """
        Get current user's subscription details.
        
        GET /api/user-subscriptions/my_subscription/
        """
        subscription = UserSubscription.objects.filter(
            user=request.user, 
            status='active'
        ).first()
        
        if subscription:
            serializer = UserSubscriptionReadSerializer(subscription)
            return Response(serializer.data)
        else:
            return Response(
                {'message': 'No active subscription found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def cancel(self, request, pk=None):
        """
        Cancel a user subscription.
        
        POST /api/admin/subscriptions/{id}/cancel/
        """
        subscription = self.get_object()
        subscription.status = 'cancelled'
        subscription.save()
        
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def renew(self, request, pk=None):
        """
        Renew a user subscription.
        
        POST /api/admin/subscriptions/{id}/renew/
        Body: {"end_date": "YYYY-MM-DD"} (optional)
        """
        subscription = self.get_object()
        subscription.status = 'active'
        
        # Update end_date if provided
        end_date = request.data.get('end_date')
        if end_date:
            subscription.end_date = end_date
        
        subscription.save()
        
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)
