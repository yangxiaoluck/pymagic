from __future__ import unicode_literals

from django.db import models

# Create your models here.


class FrontConfig(models.Model):
    index = models.IntegerField(default=None)
    tpl_type = models.IntegerField(default=None)
    info = models.TextField(default=None)