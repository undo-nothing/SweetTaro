from django.db import models


class BingWapper(models.Model):
    filename = models.CharField(max_length=200, null=False, blank=False)
    title = models.CharField(max_length=400, null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    keyword = models.CharField(max_length=400, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'bing_wapper'
        verbose_name = 'BingWapper'
        verbose_name_plural = verbose_name
