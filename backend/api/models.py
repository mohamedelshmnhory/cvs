from django.db import models
from django.contrib.auth.models import AbstractUser
from jobs.models import Job


# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    jobs = models.ManyToManyField(Job)

