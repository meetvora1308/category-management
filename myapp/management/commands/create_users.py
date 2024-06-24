from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create 100 users"

    def handle(self, *args, **kwargs):
        users = []
        for i in range(1, 101):
            username = f"user{i}"
            if not User.objects.filter(username=username).exists():
                users.append(User(username=username, password="password123"))

        # Use bulk_create for better performance
        User.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS("Successfully created 100 users"))
