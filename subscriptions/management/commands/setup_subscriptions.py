from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionPlan


class Command(BaseCommand):
    help = 'Set up sample subscription plans for the school management system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample subscription plans...')
        
        # Sample features for different plans
        basic_features = [
            'student_management',
            'basic_reports',
            'email_notifications',
            'attendance_tracking'
        ]
        
        standard_features = basic_features + [
            'advanced_reports',
            'grade_management',
            'parent_portal',
            'sms_notifications',
            'timetable_management'
        ]
        
        premium_features = standard_features + [
            'advanced_analytics',
            'custom_reports',
            'api_access',
            'priority_support',
            'data_export',
            'multi_branch_support',
            'advanced_security'
        ]
        
        # Create or update plans
        plans_data = [
            {
                'name': 'Basic',
                'features': basic_features,
                'price': 9.99,
                'description': 'Essential features for small schools'
            },
            {
                'name': 'Standard',
                'features': standard_features,
                'price': 19.99,
                'description': 'Comprehensive features for growing schools'
            },
            {
                'name': 'Premium',
                'features': premium_features,
                'price': 39.99,
                'description': 'Advanced features for large institutions'
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for plan_data in plans_data:
            plan, created = SubscriptionPlan.objects.update_or_create(
                name=plan_data['name'],
                defaults={
                    'features': plan_data['features'],
                    'price': plan_data['price'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created {plan.name} plan with {len(plan.features)} features')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated {plan.name} plan with {len(plan.features)} features')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully set up subscription plans: {created_count} created, {updated_count} updated'
            )
        )
        
        # Display summary
        self.stdout.write('\nSubscription Plans Summary:')
        self.stdout.write('=' * 50)
        
        for plan in SubscriptionPlan.objects.all():
            self.stdout.write(
                f'{plan.name:10} | ${plan.price:6.2f} | {len(plan.features):2d} features | '
                f'{"Active" if plan.is_active else "Inactive"}'
            )
