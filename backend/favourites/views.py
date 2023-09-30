from rest_framework import generics
from rest_framework import status
from .models import Favorite
from .serializers import FavoriteSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions
from api.response import CustomResponse

User = get_user_model()


class AddToFavoriteView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        profile_id = self.kwargs.get('profile_id')
        profile = User.objects.get(id=profile_id)
        user = self.request.user

        favorite, created = Favorite.objects.get_or_create(user=user)

        favorite.profiles.add(profile)
        favorite.save()

    def create(self, request, *args, **kwargs):
        self.perform_create(self.get_serializer(data=request.data))
        return CustomResponse(status=True, message='Added to favorites',
                              status_code=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        favorite = self.get_queryset().filter(profiles__id=profile_id).first()

        if favorite:
            profile = favorite.profiles.get(id=profile_id)
            favorite.profiles.remove(profile)
            favorite.save()
            return CustomResponse(status=True, message='Removed from favorites',
                                  status_code=status.HTTP_204_NO_CONTENT)
        else:
            return CustomResponse(status=False, message='Not found',
                                  status_code=status.HTTP_404_NOT_FOUND)


class GetFavoritesView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        if serializer.data:
            data = serializer.data[0]['profiles']
        else:
            data = []
        return CustomResponse(status=True, data=data, message='',
                              status_code=status.HTTP_200_OK)

# class RemoveFromFavoritesView(generics.DestroyAPIView):
#     serializer_class = FavoriteSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         return Favorite.objects.filter(user=self.request.user)
#
#     def destroy(self, request, *args, **kwargs):
#         profile_id = self.kwargs.get('profile_id')
#         favorite = self.get_queryset().filter(profiles__id=profile_id).first()
#
#         if favorite:
#             profile = favorite.profiles.get(id=profile_id)
#             favorite.profiles.remove(profile)
#             favorite.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)
