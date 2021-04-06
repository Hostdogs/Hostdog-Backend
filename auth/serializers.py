from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register serializer
    """
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, data):
        username = data["username"]
        firstname = data["first_name"]
        lastname = data["last_name"]
        email = data["email"]
        password = data["password"]

        user = User.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            password=password,
        )
        return user