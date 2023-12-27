from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_migrate)
def create_initial_user(sender, **kwargs):
    if sender.name == 'chat':
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user('admin', 'admin@example.com', '1234')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            print('Usuario administrador creado exitosamente')

