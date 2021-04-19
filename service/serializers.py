from rest_framework import serializers
from .models import Service, Meal, HostService, Chat


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
            "service_is_walk",
            "service_is_get_dog",
            "service_is_deliver_dog",
            "service_is_dog_bath",
            "service_bio",
        )


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = (
            "host",
            "meal_type",
            "meal_price",
        )


class HostServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostService
        fields = (
            "host",
            "is_dog_walk",
            "price_dog_walk",
            "is_get_dog",
            "price_get_dog",
            "is_deliver_dog",
            "price_deliver_dog",
            "is_bath_dog",
            "price_bath_dog",
        )


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            "id",
            "customer",
            "host",
            "chat_date_time",
            "chat_data",
            "chat_send_by_host",
        )
