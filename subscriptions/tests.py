from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import SubscriptionPlan, UserSubscription
from .utils import (
    has_feature_access, get_user_subscription, get_user_plan,
    get_user_features, is_subscription_expired, get_subscription_remaining_days
)

User = get_user_model()


class SubscriptionPlanModelTest(TestCase):
    """Test cases for SubscriptionPlan model"""
    
    def setUp(self):
        """Set up test data"""
        self.basic_plan = SubscriptionPlan.objects.create(
            name='Basic',
            features=['feature1', 'feature2'],
            price=Decimal('9.99'),
            is_active=True
        )
        
        self.premium_plan = SubscriptionPlan.objects.create(
            name='Premium',
            features=['feature1', 'feature2', 'feature3', 'feature4'],
            price=Decimal('29.99'),
            is_active=True
        )
    
    def test_subscription_plan_creation(self):
        """Test subscription plan creation"""
        self.assertEqual(self.basic_plan.name, 'Basic')
        self.assertEqual(self.basic_plan.price, Decimal('9.99'))
        self.assertTrue(self.basic_plan.is_active)
        self.assertEqual(self.basic_plan.features, ['feature1', 'feature2'])
    
    def test_feature_count_property(self):
        """Test feature_count property"""
        self.assertEqual(self.basic_plan.feature_count, 2)
        self.assertEqual(self.premium_plan.feature_count, 4)
    
    def test_string_representation(self):
        """Test string representation of subscription plan"""
        expected = "Basic - $9.99"
        self.assertEqual(str(self.basic_plan), expected)
    
    def test_plan_choices(self):
        """Test plan name choices"""
        choices = [choice[0] for choice in SubscriptionPlan.PLAN_CHOICES]
        self.assertIn('Basic', choices)
        self.assertIn('Standard', choices)
        self.assertIn('Premium', choices)


class UserSubscriptionModelTest(TestCase):
    """Test cases for UserSubscription model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        
        self.plan = SubscriptionPlan.objects.create(
            name='Basic',
            features=['feature1', 'feature2'],
            price=Decimal('9.99'),
            is_active=True
        )
        
        self.subscription = UserSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            status='active'
        )
    
    def test_user_subscription_creation(self):
        """Test user subscription creation"""
        self.assertEqual(self.subscription.user, self.user)
        self.assertEqual(self.subscription.plan, self.plan)
        self.assertEqual(self.subscription.status, 'active')
        self.assertIsNotNone(self.subscription.start_date)
    
    def test_is_active_property(self):
        """Test is_active property"""
        # Test active subscription
        self.assertTrue(self.subscription.is_active)
        
        # Test expired subscription
        self.subscription.status = 'expired'
        self.subscription.save()
        self.assertFalse(self.subscription.is_active)
        
        # Test cancelled subscription
        self.subscription.status = 'cancelled'
        self.subscription.save()
        self.assertFalse(self.subscription.is_active)
    
    def test_get_remaining_days(self):
        """Test get_remaining_days method"""
        # Test unlimited subscription (no end_date)
        self.assertIsNone(self.subscription.get_remaining_days())
        
        # Test subscription with end_date
        future_date = timezone.now() + timedelta(days=30)
        self.subscription.end_date = future_date
        self.subscription.save()
        
        remaining_days = self.subscription.get_remaining_days()
        self.assertIsNotNone(remaining_days)
        self.assertGreater(remaining_days, 0)
        self.assertLessEqual(remaining_days, 30)
    
    def test_string_representation(self):
        """Test string representation of user subscription"""
        expected = f"Test User - Basic (active)"
        self.assertEqual(str(self.subscription), expected)


class SubscriptionUtilsTest(TestCase):
    """Test cases for subscription utility functions"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        
        self.plan = SubscriptionPlan.objects.create(
            name='Basic',
            features=['feature1', 'feature2', 'feature3'],
            price=Decimal('9.99'),
            is_active=True
        )
        
        self.subscription = UserSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            status='active'
        )
    
    def test_has_feature_access(self):
        """Test has_feature_access function"""
        # Test user with access to feature
        self.assertTrue(has_feature_access(self.user, 'feature1'))
        self.assertTrue(has_feature_access(self.user, 'feature2'))
        
        # Test user without access to feature
        self.assertFalse(has_feature_access(self.user, 'feature4'))
        
        # Test anonymous user
        self.assertFalse(has_feature_access(None, 'feature1'))
    
    def test_get_user_subscription(self):
        """Test get_user_subscription function"""
        subscription = get_user_subscription(self.user)
        self.assertEqual(subscription, self.subscription)
        
        # Test user without subscription
        new_user = User.objects.create_user(
            email='new@example.com',
            name='New User',
            password='testpass123'
        )
        self.assertIsNone(get_user_subscription(new_user))
    
    def test_get_user_plan(self):
        """Test get_user_plan function"""
        plan = get_user_plan(self.user)
        self.assertEqual(plan, self.plan)
        
        # Test user without plan
        new_user = User.objects.create_user(
            email='new@example.com',
            name='New User',
            password='testpass123'
        )
        self.assertIsNone(get_user_plan(new_user))
    
    def test_get_user_features(self):
        """Test get_user_features function"""
        features = get_user_features(self.user)
        self.assertEqual(features, ['feature1', 'feature2', 'feature3'])
        
        # Test user without features
        new_user = User.objects.create_user(
            email='new@example.com',
            name='New User',
            password='testpass123'
        )
        self.assertEqual(get_user_features(new_user), [])
    
    def test_is_subscription_expired(self):
        """Test is_subscription_expired function"""
        # Test active subscription
        self.assertFalse(is_subscription_expired(self.user))
        
        # Test expired subscription
        self.subscription.status = 'expired'
        self.subscription.save()
        self.assertTrue(is_subscription_expired(self.user))
        
        # Test user without subscription
        new_user = User.objects.create_user(
            email='new@example.com',
            name='New User',
            password='testpass123'
        )
        self.assertTrue(is_subscription_expired(new_user))
    
    def test_get_subscription_remaining_days(self):
        """Test get_subscription_remaining_days function"""
        # Test unlimited subscription
        self.assertIsNone(get_subscription_remaining_days(self.user))
        
        # Test subscription with end_date
        future_date = timezone.now() + timedelta(days=15)
        self.subscription.end_date = future_date
        self.subscription.save()
        
        remaining_days = get_subscription_remaining_days(self.user)
        self.assertIsNotNone(remaining_days)
        self.assertGreater(remaining_days, 0)
        self.assertLessEqual(remaining_days, 15)


class SubscriptionAPITest(TestCase):
    """Test cases for subscription API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            name='Admin User',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        self.plan = SubscriptionPlan.objects.create(
            name='Basic',
            features=['feature1', 'feature2'],
            price=Decimal('9.99'),
            is_active=True
        )
    
    def test_subscription_plan_list_view(self):
        """Test subscription plan list view"""
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Test unauthenticated access
        response = client.get('/api/plans/')
        self.assertEqual(response.status_code, 401)
        
        # Test authenticated access
        client.force_login(self.user)
        response = client.get('/api/plans/')
        self.assertEqual(response.status_code, 200)
        
        # Check response data
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['name'], 'Basic')
    
    def test_user_subscription_view(self):
        """Test user subscription view"""
        from django.test import Client
        
        client = Client()
        client.force_login(self.user)
        
        # Test user without subscription
        response = client.get('/api/user-subscriptions/')
        self.assertEqual(response.status_code, 404)
        
        # Create subscription and test again
        UserSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            status='active'
        )
        
        response = client.get('/api/user-subscriptions/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['plan']['name'], 'Basic')
        self.assertEqual(data['status'], 'active')
