
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the Reviewly admin account"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME")
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not all([username, email, password]):
            self.stdout.write(
                self.style.ERROR("Admin environment variables missing.")
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)

        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS("Admin account created.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Admin account updated.")
            )
