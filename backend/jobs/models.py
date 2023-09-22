from django.db import models
import django_filters


# Create your models here.
class Job(models.Model):
    # pk
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True, default='')


class JobFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Job
        fields = ['name', 'description']
