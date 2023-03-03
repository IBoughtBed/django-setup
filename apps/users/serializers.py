from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from .models import CustomUser


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = CustomUser
        fields = ("pk", "username", "email")
        read_only_fields = ("email",)


class CustomJWTSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user_data = CustomUserDetailsSerializer(
            obj["user"], context=self.context).data
        return user_data
