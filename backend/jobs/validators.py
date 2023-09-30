from rest_framework import serializers

from .models import Job


def validate_name(value):
    qs = Job.objects.filter(name__iexact=value)
    if qs.exists():
        raise serializers.ValidationError(f"{value} is already a job name.")
    return value
