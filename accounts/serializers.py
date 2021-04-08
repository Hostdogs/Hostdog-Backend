from rest_framework import serializers
from accounts.models import Accounts


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for account
    """

    class Meta:
        model = Accounts
        fields = ("username", "email", "password", "first_name", "last_name", "mobile", "address", "role")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        account = Accounts.objects.create_user(**validated_data)
        return account