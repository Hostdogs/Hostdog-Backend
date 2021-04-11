from rest_framework import serializers
from accounts.models import Accounts, Customer, Host, Dog


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for account model
    """

    class Meta:
        model = Accounts
        fields = (
            "id",
            "is_host",
            "username",
            "email",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        account = Accounts.objects.create_user(**validated_data)
        return account


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint
    """

    model = Accounts
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer model
    """

    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "customer_bio",
            "customer_dog_count",
            "customer_hosted_count",
            "address",
            "mobile",
            "dob"
        )


class HostProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for host model
    """

    class Meta:
        model = Host
        fields = (
            "first_name",
            "last_name",
            "host_bio",
            "host_rating",
            "host_hosted_count",
            "host_max",
            "host_avaliable",
            "host_area",
            "host_schedule",
            "address",
            "mobile",
            "dob"
        )


class DogProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for dog model
    """
    class Meta:
        model = Dog
        fields = (
            "customer_id",
            "dog_name",
            "dog_dob",
            "dog_breed",
            "dog_weight",
            "dog_bio",
        )

        extra_kwargs = {
            "dog_name": {"required": True},
        }


class UpdateAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for update account detail
    """
    class Meta:
        model = Accounts
        fields = (
            "id",
            "first_name",
            "last_name",
            "mobile",
            "address",
        )