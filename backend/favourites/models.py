from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    profiles = models.ManyToManyField(User, related_name='profile')

    def __str__(self):
        return f"{self.user.username}'s Favorites"
