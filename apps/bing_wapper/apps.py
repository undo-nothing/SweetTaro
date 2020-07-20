from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BingWapperConfig(AppConfig):
    name = 'apps.bing_wapper'

    def ready(self):
        pass
