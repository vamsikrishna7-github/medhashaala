from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class SubscriptionPlan(models.Model):
    """Model for managing subscription plans"""
    
    PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    ]
    
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    features = models.JSONField(default=list, help_text="List of enabled features for this plan")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Price in currency units"
    )
    is_active = models.BooleanField(default=True, help_text="Whether this plan is available for subscription")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['price']
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    @property
    def feature_count(self):
        """Return the number of features in this plan"""
        return len(self.features) if self.features else 0


class UserSubscription(models.Model):
    """Model for tracking user subscriptions"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='user_subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True, help_text="Leave blank for unlimited subscription")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Subscription"
        verbose_name_plural = "User Subscriptions"
        # Ensure one active subscription per user
        unique_together = ['user', 'status']
    
    def __str__(self):
        return f"{self.user.name or self.user.email} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self):
        """Check if subscription is currently active"""
        if self.status != 'active':
            return False
        if self.end_date is None:
            return True
        from django.utils import timezone
        return timezone.now() <= self.end_date
    
    def get_remaining_days(self):
        """Get remaining days for subscription (None if unlimited)"""
        if self.end_date is None:
            return None
        from django.utils import timezone
        remaining = self.end_date - timezone.now()
        return max(0, remaining.days)
