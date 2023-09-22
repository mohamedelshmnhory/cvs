from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from jobs.serializers import JobSerializer
# from django.contrib.auth import update_session_auth_hash

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'age', 'jobs', 'password', 'is_superuser',
                  'get_all_permissions']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'validators': [UniqueValidator(queryset=User.objects.all(),
                                                     message='A user with that email already exists.')]},
            'phone': {'validators': [UniqueValidator(queryset=User.objects.all(),
                                                     message='A user with that phone already exists.')]},
        }

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
#     new_password_confirmation = serializers.CharField(required=True)
#
#     def validate(self, data):
#         # Check if the old password is correct
#         user = self.context['request'].user
#         if not user.check_password(data['old_password']):
#             raise serializers.ValidationError({"old_password": ["Wrong password."]})
#
#         # Check if the new password and confirmation match
#         if data['new_password'] != data['new_password_confirmation']:
#             raise serializers.ValidationError({"new_password": ["New passwords do not match."]})
#
#         return data
#
#     def save(self):
#         # Change the user's password
#         user = self.context['request'].user
#         user.set_password(self.validated_data['new_password'])
#         user.save()
#
#         # Update the session to keep the user logged in
#         request = self.context['request']
#         update_session_auth_hash(request, user)
#         auth_login(request, user)
