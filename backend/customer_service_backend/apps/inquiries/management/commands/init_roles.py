from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates default user roles (groups)'

    def handle(self, *args, **options):
        # Create Roles
        roles = ['Admin', 'Support']
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created group "{role}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{role}" already exists'))

        # Create Default Superuser
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user, created = User.objects.get_or_create(username='aelgueta')
        if created:
            user.set_password('Teoshim123')
            user.email = 'ashimelguetasalinas@gmail.com'
            self.stdout.write(self.style.SUCCESS('Successfully created superuser "aelgueta"'))
        else:
            self.stdout.write(self.style.WARNING('User "aelgueta" already exists, ensuring superuser status'))
        
        user.is_staff = True
        user.is_superuser = True
        user.save()
            
        self.stdout.write(self.style.SUCCESS('Role and user initialization complete.'))
