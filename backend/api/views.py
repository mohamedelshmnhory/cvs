from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .response import CustomResponse
from rest_framework.parsers import MultiPartParser, JSONParser
from jobs.models import Job
from jobs.serializers import JobSerializer
from .models import UserFilter
from .mixins import StaffEditorPermissionMixin

User = get_user_model()


# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]  # Allow any user to register


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow any user to register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        token, created = Token.objects.get_or_create(user=serializer.instance)
        user_data = UserSerializer(user).data
        response_data = {
            "user": user_data,
            "token": token.key,
        }
        message = "User registered successfully."
        return CustomResponse(status=True, data=response_data, message=message,
                              status_code=status.HTTP_200_OK)

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        fullname = serializer.validated_data.get('fullname') or None
        if fullname is None:
            fullname = username
        serializer.save(fullname=fullname)


class UserLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data
        response_data = {
            "user": user_data,
            "token": token.key,
            # "access": serializer.validated_data["access"],
            # "refresh": serializer.validated_data["refresh"],
        }
        message = "User logged in successfully."
        return CustomResponse(status=True, data=response_data, message=message,
                              status_code=status.HTTP_200_OK)


class UserListView(StaffEditorPermissionMixin, generics.ListAPIView):
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def get_queryset(self):
        job_id = self.request.query_params.get('job_id')
        level_id = self.request.query_params.get('level_id')

        if job_id and level_id:
            return User.objects.filter(jobs__id=job_id, level__id=level_id)
        elif job_id:
            return User.objects.filter(jobs__id=job_id)
        elif level_id:
            return User.objects.filter(level__id=level_id)
        else:
            return User.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user_data = UserSerializer(self.get_object()).data
        return CustomResponse(status=True, data=user_data, message='',
                              status_code=status.HTTP_200_OK)


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # print(request.FILES)

        # handle password change
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if old_password and new_password:
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                user_data['password'] = new_password
            else:
                return CustomResponse(status=False, data=None, message='Wrong old password.',
                                      status_code=status.HTTP_400_BAD_REQUEST)

        return CustomResponse(status=True,
                              data=user_data,
                              message='User profile updated successfully.',
                              status_code=status.HTTP_200_OK)


class UserActionsAPIView(
    StaffEditorPermissionMixin,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
    generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data)


# class ChangePasswordView(generics.UpdateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user
#
#     def post(self, request):
#         serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Password updated successfully."},
#                             status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """

    serializer = JobSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        # instance = form.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response({"invalid": "not good data"}, status=400)
