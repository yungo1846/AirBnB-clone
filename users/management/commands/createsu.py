from django.core.management.base import BaseCommand
from django_seed import Seed  # fake user create
from users.models import User


class Command(BaseCommand):
    help = "This command creates superuser"

    def handle(self, *args, **options):
        try:
            admin = User.objects.get(username="edadmin")
        except User.DoesNotExist:
            admin = None
        User.objects.create_superuser("ebadmin", "yungo1846@gmail.com", "1234")
        self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
