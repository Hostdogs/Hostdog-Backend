from rest_framework import serializers
from .models import Service, Meal, HostService


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for account model
    """

    class Meta:
        model = Service
        fields = (
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
            "additional_service"
        )
        read_only_fields = ("service_status", "service_create_time")


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = (
            "meal_type",
            "meal_price",
        )


class HostServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostService
        fields = (
            "host",
            "price_dog_walk",
            "price_get_dog",
            "price_deliver_dog",
            "price_bath_dog",
            "enable_dog_walk",
            "enable_get_dog",
            "enable_delivery_dog",
            "enable_bath_dog"
        )
