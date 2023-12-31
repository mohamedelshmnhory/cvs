from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import LevelsViewSet

router = routers.DefaultRouter()
router.register('', LevelsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
