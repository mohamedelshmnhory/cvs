from django.db import models


# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True, default='')
