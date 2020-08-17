from django.core.management.base import BaseCommand
from django_seed import Seed  # fake user create
from users.models import User
import os


class Command(BaseCommand):
    help = "This command creates superuser"

    def handle(self, *args, **options):
        try:
            admin = User.objects.get(username="edadmin")
        except User.DoesNotExist:
            admin = None
        User.objects.create_superuser(
            os.environ.get("su_id"),
            "yungo1846@gmail.com",
            os.environ.get("su_password"),
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
