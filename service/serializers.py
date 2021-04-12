from rest_framework import serializers
from .models import Service,Meal,HostService


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
            "service_is_deliver_dog",
            "service_is_dog_bath",
            "service_bio",
        )

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class HostServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostService
        fields = '__all__'

