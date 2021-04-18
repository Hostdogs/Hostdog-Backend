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
        fields = ("id", "is_host", "username", "email", "password", "token")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def get_token(self, validated_data):
        user = Accounts.objects.get(username=validated_data.username)
        token = Token.objects.get(user=user)
        return token.key

    def validate(self, attrs):
        """
        validate the email and is_host field
            - username is unique
            - one email can apply for 2 times
            - in two email cant apply for the same role
        """
        is_host = attrs["is_host"]
        email = attrs["email"]
        account_email = Accounts.objects.filter(email=email)
        if account_email.count() >= 2:
            raise serializers.ValidationError(
                {"email": ["This email has already been used."]}
            )
        elif account_email.filter(is_host=is_host).exists():
            raise serializers.ValidationError(
                {
                    "is_host": [
                        f"This email has already been used for {'Host' if is_host else 'Customer'}"
                    ]
                }
            )
        return super().validate(attrs)

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
            "dog_create_date",
        )

        extra_kwargs = {
            "dog_name": {"required": True},
        }

    def validate_customer(self, value):
        """
        validate the customer field
            - user cant change customer of dog
        """
        if value.account != self.context["request"].user:
            raise serializers.ValidationError("Bad value.")
        return value


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

    def validate_host(self, value):
        """
        validate the host field
            - user cant change host of date
        """
        if value.account != self.context["request"].user:
            raise serializers.ValidationError("Bad value.")
        return value
    
    def validate_date(self, value):
        """
        validate the date field
            - the date must not have the duplicate for one host
        """
        host = Host.objects.get(account=self.context["request"].user)
        if HostAvailableDate.objects.filter(date=value, host=host).exists():
            raise serializers.ValidationError("This date has already been assigned for this host")
        return value


class HostProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for host model
    """

    available_dates = HostAvailableDateSerializer(read_only=True, many=True)
    distance = serializers.SerializerMethodField()
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
            "address",
            "mobile",
            "dob",
            "latitude",
            "longitude",
            "distance"
        )

    def get_distance(self, validated_data):
        try:
            distance = validated_data.distance
        except AttributeError as e:
            print(e)
            return "-"
        return distance
