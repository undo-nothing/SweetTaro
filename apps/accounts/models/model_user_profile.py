import json

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.TextField(_('preferences'), default='', blank=True)

    def get_preferences(self, key=None, default=None):
        data = {}
        if self.preferences:
            data = json.loads(self.preferences)

        if key:
            data.get(key, default)

        return data

    def set_preferences(self, new_attrs):
        import json
        saved_preference = self.get_preferences()
        saved_preference.update(new_attrs)
        self.preferences = json.dumps(saved_preference)

    class Meta(object):
        verbose_name = _('user profile')
        verbose_name_plural = verbose_name
        db_table = 'auth_user_profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
