from rest_framework import serializers
from .models import Favorite
from api.serializers import UserSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    profiles = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ['profiles']
