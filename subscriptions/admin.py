from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin interface for SubscriptionPlan model"""
    
    list_display = ['name', 'price', 'feature_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'name', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'price', 'is_active')
        }),
        ('Features', {
            'fields': ('features',),
            'description': 'Enter features as a JSON array (e.g., ["feature1", "feature2"])'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def feature_count(self, obj):
        """Display feature count in admin list"""
        return obj.feature_count
    feature_count.short_description = 'Features Count'


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for UserSubscription model"""
    
    list_display = ['user', 'plan', 'status', 'is_active', 'start_date', 'end_date']
    list_filter = ['status', 'plan', 'start_date', 'created_at']
    search_fields = ['user__username', 'user__email', 'plan__name']
    readonly_fields = ['created_at', 'updated_at', 'is_active']
    
    fieldsets = (
        ('Subscription Details', {
            'fields': ('user', 'plan', 'status')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date'),
            'description': 'Leave end_date blank for unlimited subscription'
        }),
        ('Status Information', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active(self, obj):
        """Display if subscription is currently active"""
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = 'Currently Active'
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions', 'cancel_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        """Admin action to activate selected subscriptions"""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} subscription(s) activated successfully.')
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        """Admin action to deactivate selected subscriptions"""
        updated = queryset.update(status='expired')
        self.message_user(request, f'{updated} subscription(s) deactivated successfully.')
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"
    
    def cancel_subscriptions(self, request, queryset):
        """Admin action to cancel selected subscriptions"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} subscription(s) cancelled successfully.')
    cancel_subscriptions.short_description = "Cancel selected subscriptions"
