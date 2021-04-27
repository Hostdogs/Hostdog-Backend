from accounts.models import Customer, HostAvailableDate
from rest_framework import serializers
from service.models import Service, Meal, HostService
from django.utils.timezone import localtime, timedelta


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for service model
        - use for create service by customer only because host, customer, dog field and some other field cant change
    """

    class Meta:
        model = Service
        fields = [
            "id",
            "host",
            "dog",
            "service_is_over_night",
            "service_start_time",
            "service_end_time",
            "service_meal_type",
            "service_meal_per_day",
            "service_meal_weight",
            "is_dog_walk",
            "is_get_dog",
            "is_delivery_dog",
            "is_bath_dog",
            "service_bio",
        ]

    def create(self, validated_data):
        customer = Customer.objects.get(account=self.context["request"].user)
        additional_service = HostService.objects.get(host=validated_data["host"])
        service = Service.objects.create(
            customer=customer, additional_service=additional_service, **validated_data
        )
        return service
    
    def validate_service_start_time(self, value):
        if value < localtime():
            raise serializers.ValidationError("Do you have a time machine?")
        return value

    def validate_service_end_time(self, value):
        if value < localtime():
            raise serializers.ValidationError("Do you have a time machine?")
        return value

    def validate(self, attrs):
        """
        validate is_dog_walk, is_get_dog, is_delivery_dog, is_bath_dog field, service_start_time, service_end_time
            - check if HostService is enable that field too
            - check if service_start_time, service_end_time is valid for host
            - Customer cant choose day in the past
        """
        is_dog_walk = attrs["is_dog_walk"]
        is_get_dog = attrs["is_get_dog"]
        is_delivery_dog = attrs["is_delivery_dog"]
        is_bath_dog = attrs["is_bath_dog"]
        host = attrs["host"]
        service_start_time = attrs["service_start_time"]
        service_end_time = attrs["service_end_time"]
        service_delta = service_end_time.date() - service_start_time.date()
        host_service = HostService.objects.get(host=host)

        if is_dog_walk and not host_service.enable_dog_walk:
            raise serializers.ValidationError(
                {"is_dog_walk": [f"Bad value : is_dog_walk is DISABLE"]}
            )

        if is_get_dog and not host_service.enable_get_dog:
            raise serializers.ValidationError(
                {"is_get_dog": [f"Bad value : is_get_dog is DISABLE"]}
            )

        if is_delivery_dog and not host_service.enable_delivery_dog:
            raise serializers.ValidationError(
                {"is_delivery_dog": [f"Bad value : is_delivery_dog is DISABLE"]}
            )

        if is_bath_dog and not host_service.enable_bath_dog:
            raise serializers.ValidationError(
                {"is_bath_dog": [f"Bad value : is_bath_dog is DISABLE"]}
            )

        if service_start_time > service_end_time:
            raise serializers.ValidationError({"service_start_time": ["start time is greater than end time"]})

        all_date_within_interval = [
            service_start_time.date() + timedelta(days=i)
            for i in range(service_delta.days + 1)
        ]
        for choose_date in all_date_within_interval:
            if not HostAvailableDate.objects.filter(
                host=host, date=choose_date
            ).exists():
                raise serializers.ValidationError(
                    {
                        "service_start_time": ["Bad value : Date range error"],
                        "service_end_time": ["Bad value : Date range error"],
                    }
                )
        return super().validate(attrs)


class ServiceDetailSerializer(ServiceSerializer):
    """
    Serializer for service model(Extend from Service serializer)
        - use for managing detail of service
    """

    class Meta(ServiceSerializer.Meta):
        fields = ServiceSerializer.Meta.fields + [
            "customer",
            "service_status",
            "service_create_time",
            "service_send_time",
            "service_get_time",
            "main_status",
        ]
        read_only_fields = [
            "host",
            "customer",
            "dog",
            "service_status",
            "service_is_over_night",
            "service_create_time",
            "service_start_time",
            "service_end_time",
            "service_meal_type",
            "service_meal_per_day",
            "service_meal_weight",
            "is_dog_walk",
            "is_get_dog",
            "is_delivery_dog",
            "is_bath_dog",
            "main_status",
        ]


class ServiceResponseSerializer(serializers.Serializer):
    """
    Serializer for host to response back to customer
        - accept service or decline service
    """
    accept = serializers.BooleanField()
    cancel = serializers.BooleanField()
    review = serializers.IntegerField()
    receive_dog = serializers.BooleanField()
    return_dog = serializers.BooleanField()


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            "meal_type",
            "meal_price",
        ]


class HostServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostService
        fields = [
            "host",
            "price_dog_walk",
            "price_get_dog",
            "price_deliver_dog",
            "price_bath_dog",
            "enable_dog_walk",
            "enable_get_dog",
            "enable_delivery_dog",
            "enable_bath_dog",
        ]
