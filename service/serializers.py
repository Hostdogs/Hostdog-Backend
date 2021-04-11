from rest_framework import serializers
from .models import Service


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
            "service_reg_time",
            "service_end_time",
            "service_meal_type",
            "service_meal_per_day",
            "service_meal_weight",
            "service_is_walk",
            "service_is_get_dog",
            "service_is_ride_dog",
            "service_is_dog_bath",
            "service_bio",
        )
