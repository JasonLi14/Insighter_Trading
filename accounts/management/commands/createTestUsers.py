from django.core.management.base import BaseCommand, CommandError
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Creates a lot (100) of test users"

    def handle(self, *args, **options):
        for i in range(100):
            user = CustomUser.objects.create_user(f"test_{i}", f"test_{i}@test.com", "testpassword1010")
            user.save()
        print(CustomUser.objects.all().values())

