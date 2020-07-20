from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    name = 'apps.accounts'

    def ready(self):
        from .utils import create_default_user
        post_migrate.connect(create_default_user, sender=self)
