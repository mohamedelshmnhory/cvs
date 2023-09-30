from rest_framework import serializers

from .models import Job
# from .validators import validate_name
# from rest_framework.validators import UniqueValidator


class JobSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(
    #     max_length=255,
    #     # validators=[UniqueValidator(queryset=Job.objects.all())],
    #     # error_messages={"unique": "This name is already taken. Please choose another one."},
    # )
    # description = serializers.CharField(max_length=255, required=False, default=name)
    # description = serializers.CharField(validators=[validate_name])

    # email = serializers.CharField(source=used.email, read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'name', 'description']

    # def validate_description(self, value):
    #     request = self. context.get ('request')
    #     user = request. user
    #     qs = Job.objects.filter(user=user, description__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a job description.")
    #     return value
