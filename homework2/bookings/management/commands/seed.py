from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bookings.models import Movie
from datetime import date
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        admin_user = os.environ.get("ADMIN_USER", "admin")
        admin_pass = os.environ.get("ADMIN_PASS", "admin12345")

        if not User.objects.filter(username=admin_user).exists():
            User.objects.create_superuser(admin_user, "", admin_pass)
            self.stdout.write(self.style.SUCCESS("Created superuser"))

        if Movie.objects.count() == 0:
            Movie.objects.create(
                title="Inception",
                description="A skilled thief enters people's dreams to steal secrets but is tasked with planting an idea instead.",
                release_date=date(2010, 7, 16),
                duration=148,
            )
            self.stdout.write(self.style.SUCCESS("Created sample movie"))
