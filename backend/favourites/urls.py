# favorites/urls.py
from django.urls import path
from .views import AddToFavoriteView, GetFavoritesView

urlpatterns = [
    path('', GetFavoritesView.as_view(), name='favorite-list'),
    path('<int:profile_id>', AddToFavoriteView.as_view(), name='favorite'),
    # path('remove-from-favorites/<int:profile_id>', RemoveFromFavoritesView.as_view(),
    #      name='remove-from-favorites'),
]
