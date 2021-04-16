from rest_framework import serializers
from rest_framework.authtoken.models import Token
from accounts.models import Accounts, Customer, Host, Dog, HostAvailableDate


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for account model
    """
    token = serializers.SerializerMethodField()
    class Meta:
        model = Accounts
        fields = (
            "id",
            "is_host",
            "username",
            "email",
            "password",
            "token"
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def get_token(self, validated_data):
        user = Accounts.objects.get(username=validated_data.username)
        token = Token.objects.get(user=user)
        return token.key

    def create(self, validated_data):
        account = Accounts.objects.create_user(**validated_data)
        token = Token.objects.create(user=account)
        return account


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint
    """

    model = Accounts
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class DogProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for dog model
    """

    class Meta:
        model = Dog
        fields = (
            "id",
            "customer",
            "picture",
            "dog_name",
            "dog_dob",
            "dog_breed",
            "dog_weight",
            "dog_bio",
            "dog_create_date"
        )

        extra_kwargs = {
            "dog_name": {"required": True},
        }


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer model
    """

    dogs = DogProfileSerializer(read_only=True, many=True)

    class Meta:
        model = Customer
        fields = (
            "account",
            "picture",
            "first_name",
            "last_name",
            "customer_bio",
            "customer_dog_count",
            "customer_hosted_count",
            "address",
            "mobile",
            "dob",
            "latitude",
            "longitude",
            "dogs",
        )

class HostAvailableDateSerializer(serializers.ModelSerializer):
    """
    Serializer for host available date for service
    """
    class Meta:
        model = HostAvailableDate
        fields = ("id", "host", "date")

class HostProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for host model
    """
    available_dates = HostAvailableDateSerializer(read_only=True, many=True)
    class Meta:
        model = Host
        fields = (
            "account",
            "picture",
            "first_name",
            "last_name",
            "host_bio",
            "host_rating",
            "host_hosted_count",
            "host_max",
            "available_dates",
            "host_area",
            "host_schedule",
            "address",
            "mobile",
            "dob",
            "latitude",
            "longitude",
        )
