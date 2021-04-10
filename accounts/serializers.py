
from rest_framework import serializers
from accounts.models import Accounts, Customer, Host, Dog
from rest_framework.response import Response
from rest_framework import status

class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for account model
    """
    class Meta:
        model = Accounts
        fields = (
            "id",
            "is_customer",
            "is_host",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "dob",
            "mobile",
            "address",
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


class CustomerAccountSerializer(serializers.ModelSerializer):
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
            "dob",
            "mobile",
            "address",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            }

    def create(self, validated_data):
        validated_data['is_customer'] = True
        account = Accounts.objects.create_user(**validated_data)
        Customer.objects.create(account=account)
        return account

class HostAccountSerializer(serializers.ModelSerializer):
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
            "dob",
            "mobile",
            "address",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        
            }

    def create(self, validated_data):
        validated_data['is_host'] = True
        account = Accounts.objects.create_user(**validated_data)
        Host.objects.create(account=account)
        return account
        



class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer model
    """

    class Meta:
        model = Customer
        fields = (
            "account",
            "customer_bio",
            "customer_dog_count",
            "customer_hosted_count",
        )

    # def create(self, validated_data):
    #     return 

    


class HostProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for host model
    """

    class Meta:
        model = Host
        fields = (
            "account",
            "host_bio",
            "host_rating",
            "host_hosted_count",
            "host_max",
            "host_avaliable",
            "host_area",
            "host_schedule",
        )

    # def create(self, validated_data):
    #     return Response(status=status.HTTP_400_BAD_REQUEST)


class DogProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dog
        fields = ("id","customer_id","dog_name","dog_dob","dog_breed","dog_weight","dog_bio")
        
        extra_kwargs = {
            "dog_name":{"required":True},
        
        }
