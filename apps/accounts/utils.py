from django.contrib.auth import get_user_model


def create_default_user(sender, **kwargs):
    class_user = get_user_model()
    if not class_user.objects.filter(username='admin'):
        class_user.objects.create_superuser(username='admin', password='admin')
        print('create default user: admin admin')
