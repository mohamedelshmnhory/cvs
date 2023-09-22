from django.urls import path
from . import views
from .views import UserRegistrationView, UserLoginView, UserProfileView, UpdateProfileView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register', UserRegistrationView.as_view(), name='user-register'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('profile', UserProfileView.as_view(), name='user-profile'),
    path('profile/update', UpdateProfileView.as_view(), name='update-profile'),
    # path('change-password/', ChangePasswordView.as_view({'post': 'change_password'}), name='change_password'),
    path('', views.api_home),  # localhost:8000/api/
    # path('products/', include('products.urls'))
]
