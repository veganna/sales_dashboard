from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help: str = 'Create a superuser'

    def handle(self, *args, **options):
        email: str = input('Email: ')
        first_name: str = input('First name: ')
        last_name: str = input('Last name: ')
        phone: str = input('Phone: ')
        password: str = input('Password: ')
        password2: str = input('Password (again): ')
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

        user: User = User.objects.create_superuser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
        )
        user.save(using='sales')
        self.stdout.write(
            self.style.SUCCESS(
                'Superuser created successfully'
            )
        )