from accounts.models import Customer, HostAvailableDate
from rest_framework import serializers
from service.models import Service, Meal, HostService


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

    def validate(self, attrs):
        """
        validate is_dog_walk, is_get_dog, is_delivery_dog, is_bath_dog field, service_start_time, service_end_time
            - check if HostService is enable that field too
            - check if service_start_time, service_end_time is valid for host
        """
        print(attrs)
        is_dog_walk = attrs["is_dog_walk"]
        is_get_dog = attrs["is_get_dog"]
        is_delivery_dog = attrs["is_delivery_dog"]
        is_bath_dog = attrs["is_bath_dog"]
        host = attrs["host"]
        service_start_time = attrs["service_start_time"]
        service_end_time = attrs["service_end_time"]
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
        if HostAvailableDate.objects.filter(
            host=host, date=service_start_time
        ).exists():
            raise serializers.ValidationError(
                {
                    "service_start_time": [
                        "Bad value : this service start time is not available for host"
                    ]
                }
            )
        if HostAvailableDate.objects.filter(host=host, date=service_end_time).exists():
            raise serializers.ValidationError(
                {
                    "service_end_time": [
                        "Bad value : this service end time is not available for host"
                    ]
                }
            )
        return super().validate(attrs)


class ServiceDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for service model
        - use for managing detail of service
    """

    class Meta:
        model = Service
        fields = [
            "id",
            "host",
            "customer",
            "dog",
            "service_status",
            "service_is_over_night",
            "service_create_time",
            "service_start_time",
            "service_end_time",
            "service_send_time",
            "service_get_time",
            "service_meal_type",
            "service_meal_per_day",
            "service_meal_weight",
            "is_dog_walk",
            "is_get_dog",
            "is_delivery_dog",
            "is_bath_dog",
            "service_bio",
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
