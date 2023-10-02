from django.db import models
from django.contrib.auth.models import AbstractUser
from jobs.models import Job
from levels.models import Level
from favourites.models import Favorite
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import django_filters


# from urllib.parse import urlparse, unquote

# Create your models here.


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='profile_images/', blank=True)
    fullname = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    jobs = models.ManyToManyField(Job, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)

    def is_favourite(self, request):
        try:
            if request.user.is_authenticated:
                return Favorite.objects.filter(user=request.user, profiles=self).exists()
            return False
        except AttributeError:
            return False

    def save(self, *args, **kwargs):
        if self.avatar:
            name = f"{self.username}_{self.avatar.name}"
            # Generate a unique filename for the avatar
            filename = f"profile_images/{name}"

            # Save the avatar to the default storage
            default_storage.save(filename, ContentFile(self.avatar.read()))

            # Update the avatar field with the base URL and filename
            self.avatar = f"{filename}"  # https://example.com/media/{filename}

        super().save(*args, **kwargs)


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    fullname = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['username', 'fullname']
