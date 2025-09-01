from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'phone', 'name', 'role', 'subscription_plan', 'is_active', 'date_joined')
    list_filter = ('role', 'subscription_plan', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'phone', 'name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Personal info', {'fields': ('name', 'role', 'subscription_plan', 'enabled_features')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'name', 'password1', 'password2', 'role', 'subscription_plan'),
        }),
    )
