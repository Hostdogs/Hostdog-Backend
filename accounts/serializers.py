from rest_framework import serializers
from rest_framework.authtoken.models import Token


from accounts.models import (
    Accounts,
    Customer,
    Host,
    Dog,
    HostAvailableDate,
    HouseImages,
    DogFeedingTime,
)
from service.models import Service
from datetime import date


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
        - use with dog view with not nested resource
    """

    class Meta:
        model = Dog
        fields = [
            "id",
            "customer",
            "picture",
            "dog_name",
            "dog_dob",
            "dog_breed",
            "dog_weight",
            "dog_bio",
            "dog_create_date",
        ]

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


class DogProfileWithNestedSerializer(DogProfileSerializer):
    """
    Serializer for dog model(Extend from DogProfileSerializer)
        - use with dog view with nested resource
    """

    class Meta(DogProfileSerializer.Meta):
        fields = DogProfileSerializer.Meta.fields
        read_only_fields = ["customer", "dog_create_date"]

    def create(self, validated_data):
        customer = Customer.objects.get(account=self.context["request"].user)
        dog = Dog.objects.create(customer=customer, **validated_data)
        return dog


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer model
        - use when create customer profile
    """

    dog_customer = DogProfileSerializer(read_only=True, many=True)

    class Meta:
        model = Customer
        fields = [
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
            "dog_customer",
        ]
        read_only_fields = ["account"]


class HostAvailableDateSerializer(serializers.ModelSerializer):
    """
    Serializer for host available date for service
    """

    class Meta:
        model = HostAvailableDate
        fields = ["id", "host", "date"]

    def validate_host(self, value):
        """
        validate the host field
            - user cant change host of date
        """
        if value.account != self.context["request"].user:
            raise serializers.ValidationError("Bad value : Not this user")
        return value

    def validate_date(self, value):
        """
        validate the date field
            - the date must not have the duplicate for one host
            - Host cant register in date that host is service
            - Host cant register date in the past
        """
        host = Host.objects.get(account=self.context["request"].user)

        if value < date.today():
            raise serializers.ValidationError("Do you have a time machine?")

        if HostAvailableDate.objects.filter(date=value, host=host).exists():
            raise serializers.ValidationError(
                "This date has already been assigned for this host"
            )

        in_progess_service = Service.objects.filter(
            host=host,
            service_start_time__lte=value,
            service_end_time__gte=value,
            main_status="in_progress",
        )
        if in_progess_service.exists():
            raise serializers.ValidationError("This date in in your service date")

        return value


class HostAvailableDateWithNestedSerializer(HostAvailableDateSerializer):
    """
    Serializer for HostAvailable date model(Extend from HostAvailableDateSerializer)
        - use with host available view with nest resource
    """

    class Meta(HostAvailableDateSerializer.Meta):
        fields = HostAvailableDateSerializer.Meta.fields
        read_only_fields = ["host"]

    def create(self, validated_data):
        host = Host.objects.get(account=self.context["request"].user)
        host_available_date = HostAvailableDate.objects.create(
            host=host, **validated_data
        )
        return host_available_date


class HouseImagesSerializer(serializers.ModelSerializer):
    """
    Serializer for house image model
    """

    class Meta:
        model = HouseImages
        fields = ["host", "picture"]
        read_only_fields = ["host"]

    def create(self, validated_data):
        host = Host.objects.get(account=self.context["request"].user)
        house_image = HouseImages.objects.create(host=host, **validated_data)
        return house_image


class HostProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for host model
    """

    host_available_date = HostAvailableDateSerializer(read_only=True, many=True)
    house_image = HouseImagesSerializer(read_only=True, many=True)
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Host
        fields = (
            "account",
            "picture",
            "house_image",
            "first_name",
            "last_name",
            "host_bio",
            "host_rating",
            "host_hosted_count",
            "host_max",
            "host_available_date",
            "host_area",
            "address",
            "mobile",
            "dob",
            "latitude",
            "longitude",
            "distance",
        )

    def get_distance(self, validated_data):
        try:
            distance = validated_data.distance
        except AttributeError as e:
            print(e)
            return "-"
        return distance


class DogFeedingTimeSerializer(serializers.ModelSerializer):
    """
    Serializer for dog feeding time model
    """
    class Meta:
        model = DogFeedingTime
        fields = ["id", "dog", "time"]
        read_only_fields = ["dog"]

    def create(self, validated_data):
        dog_id = self.context["view"].kwargs["dog_pk"]
        dog = Dog.objects.get(id=dog_id)
        feeding_time = DogFeedingTime.objects.create(dog=dog, **validated_data)
        return feeding_time
