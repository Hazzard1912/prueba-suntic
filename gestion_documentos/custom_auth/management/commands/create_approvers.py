from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from custom_auth.models import User

class Command(BaseCommand):
    help = 'Create the Approvers group and example users'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Approvers')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created the Approvers group'))
        else:
            self.stdout.write(self.style.WARNING('Approvers group already exists'))

        users_data = [
            {'email': 'approver1@example.com', 'password': 'password123'},
            {'email': 'approver2@example.com', 'password': 'password123'},
            {'email': 'approver3@example.com', 'password': 'password123'},
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(email=user_data['email'])
            if created:
                user.set_password(user_data['password'])
                user.is_staff = True
                user.save()
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.email}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {user.email} already exists'))