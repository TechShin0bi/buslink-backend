from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AgencyEmployee

@receiver(post_save, sender=AgencyEmployee)
def assign_permissions_to_employee(sender, instance, created, **kwargs):
    if created and instance.role:
        # Add all permissions from the role to the user
        instance.user.user_permissions.add(*instance.role.permissions.all())