from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import UserSubscription

User = get_user_model()


def has_feature_access(user, feature_name):
    """
    Check if user has access to a specific feature based on their subscription.
    
    Args:
        user: Django User instance
        feature_name: String name of the feature to check
        
    Returns:
        bool: True if user has access, False otherwise
    """
    if not user or not user.is_authenticated:
        return False
    
    try:
        subscription = UserSubscription.objects.get(
            user=user, 
            status='active'
        )
        
        # Check if subscription is still valid
        if not subscription.is_active:
            return False
            
        return feature_name in subscription.plan.features
    except UserSubscription.DoesNotExist:
        return False


def get_user_subscription(user):
    """
    Get user's current active subscription.
    
    Args:
        user: Django User instance
        
    Returns:
        UserSubscription instance or None if no active subscription
    """
    if not user or not user.is_authenticated:
        return None
    
    try:
        return UserSubscription.objects.get(
            user=user, 
            status='active'
        )
    except UserSubscription.DoesNotExist:
        return None


def get_user_plan(user):
    """
    Get user's current subscription plan.
    
    Args:
        user: Django User instance
        
    Returns:
        SubscriptionPlan instance or None if no active subscription
    """
    subscription = get_user_subscription(user)
    return subscription.plan if subscription else None


def get_user_features(user):
    """
    Get list of features available to the user.
    
    Args:
        user: Django User instance
        
    Returns:
        list: List of feature names available to the user
    """
    plan = get_user_plan(user)
    return plan.features if plan else []


def is_subscription_expired(user):
    """
    Check if user's subscription has expired.
    
    Args:
        user: Django User instance
        
    Returns:
        bool: True if subscription is expired, False otherwise
    """
    subscription = get_user_subscription(user)
    if not subscription:
        return True
    
    return not subscription.is_active


def get_subscription_remaining_days(user):
    """
    Get remaining days for user's subscription.
    
    Args:
        user: Django User instance
        
    Returns:
        int or None: Number of remaining days, None if unlimited
    """
    subscription = get_user_subscription(user)
    if not subscription:
        return None
    
    return subscription.get_remaining_days()


def can_upgrade_subscription(user, target_plan):
    """
    Check if user can upgrade to a target plan.
    
    Args:
        user: Django User instance
        target_plan: SubscriptionPlan instance
        
    Returns:
        bool: True if user can upgrade, False otherwise
    """
    current_plan = get_user_plan(user)
    if not current_plan:
        return True  # No current plan, can subscribe to any plan
    
    # Check if target plan has more features
    current_features = set(current_plan.features)
    target_features = set(target_plan.features)
    
    return len(target_features) > len(current_features)


def get_available_plans_for_user(user):
    """
    Get list of plans available for user to subscribe to.
    
    Args:
        user: Django User instance
        
    Returns:
        QuerySet: Available subscription plans
    """
    from .models import SubscriptionPlan
    
    # Get all active plans
    available_plans = SubscriptionPlan.objects.filter(is_active=True)
    
    # If user has no subscription, all plans are available
    current_subscription = get_user_subscription(user)
    if not current_subscription:
        return available_plans
    
    # Filter out plans with fewer features than current plan
    current_features_count = len(current_subscription.plan.features)
    return available_plans.filter(
        features__len__gt=current_features_count
    )


def create_user_subscription(user, plan, end_date=None, status='active'):
    """
    Create a new subscription for a user.
    
    Args:
        user: Django User instance
        plan: SubscriptionPlan instance
        end_date: Optional end date for subscription
        status: Subscription status (default: 'active')
        
    Returns:
        UserSubscription: Created subscription instance
    """
    # Cancel any existing active subscription
    UserSubscription.objects.filter(
        user=user, 
        status='active'
    ).update(status='cancelled')
    
    # Create new subscription
    return UserSubscription.objects.create(
        user=user,
        plan=plan,
        end_date=end_date,
        status=status
    )


def cancel_user_subscription(user):
    """
    Cancel user's active subscription.
    
    Args:
        user: Django User instance
        
    Returns:
        bool: True if subscription was cancelled, False if no active subscription
    """
    try:
        subscription = UserSubscription.objects.get(
            user=user, 
            status='active'
        )
        subscription.status = 'cancelled'
        subscription.save()
        return True
    except UserSubscription.DoesNotExist:
        return False


def renew_user_subscription(user, end_date=None):
    """
    Renew user's subscription.
    
    Args:
        user: Django User instance
        end_date: Optional new end date
        
    Returns:
        bool: True if subscription was renewed, False if no active subscription
    """
    try:
        subscription = UserSubscription.objects.get(
            user=user, 
            status='active'
        )
        subscription.status = 'active'
        if end_date:
            subscription.end_date = end_date
        subscription.save()
        return True
    except UserSubscription.DoesNotExist:
        return False
