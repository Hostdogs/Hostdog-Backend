from rest_framework import serializers
from accounts.models import Accounts, Customer, Host


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for account
    """

    class Meta:
        model = Accounts
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "mobile",
            "address",
            "role",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        account = Accounts.objects.create_user(**validated_data)
        return account


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for customer
    """

    class Meta:
        model = Customer
        fields = (
            "id",
            "account_id",
            "customer_bio",
            "customer_dog_count",
            "customer_hosted_count",
        )


class HostSerializer(serializers.ModelSerializer):
    """
    Serializer for host
    """

    class Meta:
        model = Host
        fields = (
            "id",
            "account_id",
            "host_bio",
            "host_rating",
            "host_hosted_count",
            "host_max",
            "host_avaliable",
            "host_area",
            "host_schedule",
        )
