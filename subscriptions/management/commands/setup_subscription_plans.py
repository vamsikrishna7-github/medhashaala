from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from subscriptions.models import SubscriptionPlan

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up default subscription plans and migrate existing users'

    def handle(self, *args, **options):
        self.stdout.write('Setting up subscription plans...')
        
        # Create default subscription plans
        plans_data = [
            {
                'name': 'Basic',
                'features': ['basic_access', 'limited_queries'],
                'price': 0.00,
                'is_active': True,
            },
            {
                'name': 'Standard',
                'features': ['basic_access', 'standard_queries', 'priority_support'],
                'price': 9.99,
                'is_active': True,
            },
            {
                'name': 'Premium',
                'features': ['basic_access', 'unlimited_queries', 'priority_support', 'advanced_features'],
                'price': 19.99,
                'is_active': True,
            },
        ]
        
        created_plans = []
        for plan_data in plans_data:
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f'Created plan: {plan.name}')
            else:
                self.stdout.write(f'Plan already exists: {plan.name}')
            created_plans.append(plan)
        
        # Map old subscription plan values to new plans
        plan_mapping = {
            'base': 'Basic',
            'standard': 'Standard',
            'premium': 'Premium',
        }
        
        # Update users who don't have a subscription plan set
        users_without_plan = User.objects.filter(subscription_plan__isnull=True)
        self.stdout.write(f'Found {users_without_plan.count()} users without subscription plans')
        
        for user in users_without_plan:
            # Try to find a plan based on the old field value if it exists
            # For now, assign Basic plan as default
            basic_plan = SubscriptionPlan.objects.filter(name='Basic').first()
            if basic_plan:
                user.subscription_plan = basic_plan
                user.save(update_fields=['subscription_plan'])
                self.stdout.write(f'Assigned Basic plan to user: {user.email or user.phone}')
        
        self.stdout.write(self.style.SUCCESS('Successfully set up subscription plans!'))
