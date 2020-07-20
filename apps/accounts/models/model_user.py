from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    nick_name = models.CharField(_('nick_name'), max_length=30, blank=True)
    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ['id', ]
        verbose_name = _('base_model_user')
        verbose_name_plural = verbose_name
        db_table = 'auth_user'
        permissions = ()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_username()
