from rest_framework import serializers

from .models import Job
from rest_framework.validators import UniqueValidator
from datetime import timezone


class JobSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(
    #     max_length=255,
    #     # validators=[UniqueValidator(queryset=Job.objects.all())],
    #     # error_messages={"unique": "This name is already taken. Please choose another one."},
    # )
    # description = serializers.CharField(max_length=255, required=False, default=name)

    class Meta:
        model = Job
        fields = ['id', 'name', 'description']
