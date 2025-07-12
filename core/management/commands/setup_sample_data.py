from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from items.models import Item
from swaps.models import Swap

class Command(BaseCommand):
    help = 'Create sample data for the ReWear platform'

    def handle(self, *args, **options):
        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@rewear.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin user created: admin/admin123'))

        # Create some regular users first
        users = []
        for i in range(3):
            username = f'user{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, f'{username}@example.com', 'password123')
                users.append(user)
                self.stdout.write(f'Created user: {username}')

        # Get existing users if they already exist
        if not users:
            users = list(User.objects.filter(username__startswith='user'))

        if users and Item.objects.count() < 5:
            # Create sample items
            sample_items = [
                {
                    'title': 'Vintage Denim Jacket', 
                    'category': 'outerwear', 
                    'size': 'M', 
                    'condition': 'excellent', 
                    'point_value': 50,
                    'description': 'Great condition vintage denim jacket ready for swap.'
                },
                {
                    'title': 'Floral Summer Dress', 
                    'category': 'dresses', 
                    'size': 'S', 
                    'condition': 'good', 
                    'point_value': 35,
                    'description': 'Beautiful floral dress perfect for summer.'
                },
                {
                    'title': 'Designer Sneakers', 
                    'category': 'shoes', 
                    'size': '9', 
                    'condition': 'new', 
                    'point_value': 80,
                    'description': 'Brand new designer sneakers in original box.'
                },
                {
                    'title': 'Cashmere Sweater', 
                    'category': 'tops', 
                    'size': 'L', 
                    'condition': 'excellent', 
                    'point_value': 60,
                    'description': 'Luxurious cashmere sweater in excellent condition.'
                },
                {
                    'title': 'Leather Handbag', 
                    'category': 'accessories', 
                    'size': 'One Size', 
                    'condition': 'good', 
                    'point_value': 45,
                    'description': 'Stylish leather handbag with minor wear.'
                },
            ]
            
            for i, item_data in enumerate(sample_items):
                Item.objects.create(
                    owner=users[i % len(users)],
                    is_approved=True,
                    **item_data
                )
            
            self.stdout.write(self.style.SUCCESS(f'Created {len(sample_items)} sample items'))

        self.stdout.write(self.style.SUCCESS('Sample data setup complete!'))
