from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        email = input('Email: ')
        first_name = input('First name: ')
        last_name = input('Last name: ')
        phone = input('Phone: ')
        password = input('Password: ')
        password2 = input('Password (again): ')
        if password != password2:
            self.stdout.write(
                self.style.ERROR(
                    'Passwords did not match'
                )
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(
                    'User with this email already exists'
                )
            )
            return

        if not email or not first_name or not last_name or not phone or not password:
            self.stdout.write(
                self.style.ERROR(
                    'All fields are required'
                )
            )
            return

        user = User.objects.create_superuser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
        )
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                'Superuser created successfully'
            )
        )
        