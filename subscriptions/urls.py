from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, UserSubscriptionViewSet

# Create router for ViewSets
router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='plan')
router.register(r'user-subscriptions', UserSubscriptionViewSet, basename='user-subscription')

# Admin-specific router
admin_router = DefaultRouter()
admin_router.register(r'subscriptions', UserSubscriptionViewSet, basename='admin-subscription')

app_name = 'subscriptions'

urlpatterns = [
    # Public API endpoints (for all authenticated users)
    path('api/', include(router.urls)),
    
    # Admin-only endpoints
    path('api/admin/', include(admin_router.urls)),
]
