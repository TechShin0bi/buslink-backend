from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from agencies.models import Country

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed initial data for the application'

    def handle(self, *args, **options):
        # Create a sample country
        country, created = Country.objects.get_or_create(
            name="United States",
            code="US",
            defaults={'name': 'United States', 'code': 'US'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created sample country'))
        
        # Create superuser if not exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                password='admin123'  # Change this in production!
            )
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))