from rest_framework import status, viewsets
from .models import Level
from .serializers import LevelSerializer


# Create your views here.


class LevelsViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
