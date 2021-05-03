from accounts.models import Customer, HostAvailableDate
from accounts.serializers import CustomerProfileSerializer, DogProfileSerializer, HostProfileSerializer
from rest_framework import serializers
from service.models import Services, Meal, HostService
from payment.serializers import PaymentSerializer
from django.utils.timezone import localtime, timedelta


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            "id",
            "meal_type",
            "meal_price_per_gram",
        ]
        read_only_fields = ["meal_type", "meal_price_per_gram"]


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for service model
        - use for create service by customer only because host, customer, dog field and some other field cant change
    """

    class Meta:
        model = Services
        fields = [
            "id",
            "host",
            "dog",
            "service_start_time",
            "service_end_time",
            "service_meal_type",
            "service_meal_weight",
            "is_dog_walk",
            "is_get_dog",
            "is_delivery_dog",
            "is_bath_dog",
            "service_bio",
        ]
        extra_kwargs = {
            "service_start_time": {"required": True},
            "service_end_time": {"required": True},
            "dog": {"required": True},
            "host": {"required": True},
        }

    def create(self, validated_data):
        customer = Customer.objects.get(account=self.context["request"].user)
        additional_service = HostService.objects.get(host=validated_data["host"])
        service = Services.objects.create(
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
            - เช็คว่าเคยลงทะเบียนกับ Host คนนี้เวลานี้ไปแล้ว
        """
        user = self.context["request"].user
        customer = Customer.objects.get(account=user)
        is_dog_walk = attrs["is_dog_walk"]
        is_get_dog = attrs["is_get_dog"]
        is_delivery_dog = attrs["is_delivery_dog"]
        is_bath_dog = attrs["is_bath_dog"]
        host = attrs["host"]
        service_meal_type = attrs["service_meal_type"]
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
            raise serializers.ValidationError(
                {"service_start_time": ["start time is greater than end time"]}
            )

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

        service_that_customer_register = Services.objects.filter(
            host=host, customer=customer
        ).exclude(main_status="cancelled")
        for service in service_that_customer_register:
            start_time = localtime(service.service_start_time)
            end_time = localtime(service.service_end_time)
            if (
                start_time <= service_start_time <= end_time
                or service_start_time <= start_time <= service_end_time
            ):
                raise serializers.ValidationError(
                    {
                        "service_start_time": ["Bad value : You already register to this service"],
                        "service_end_time": ["Bad value : You already register to this service"],
                    }
                )

        meal_that_host_have = host_service.available_meals.all()
        if service_meal_type not in meal_that_host_have:
            raise serializers.ValidationError(
                {"service_meal_type": ["Bad value : Host doesn't have this meal"]}
            )
        return super().validate(attrs)


class ServiceDetailSerializer(ServiceSerializer):
    """
    Serializer for service model(Extend from Service serializer)
        - use for managing detail of service
    """

    service_meal_type = MealSerializer(many=False, read_only=True)
    dog = DogProfileSerializer(many=False, read_only=True)
    servicepayments = PaymentSerializer(many=True, read_only=True)
    host = HostProfileSerializer(many=False, read_only=True)
    customer = CustomerProfileSerializer(many=False, read_only=True)
    class Meta(ServiceSerializer.Meta):
        fields = ServiceSerializer.Meta.fields + [
            "customer",
            "service_status",
            "service_create_time",
            "service_send_time",
            "service_get_time",
            "main_status",
            "servicepayments",
            "total_price",
        ]
        read_only_fields = [
            "host",
            "customer",
            "dog",
            "service_status",
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
            "days_late",
            "is_review",
            "is_customer_receive_dog",
            "created_deposit_payment",
            "created_late_payment",
            "total_price",
            "main_status",
        ]


class ServiceResponseSerializer(serializers.Serializer):
    """
    Serializer for host to response back to customer
        - accept service or decline service
    """

    accept = serializers.BooleanField(required=False)
    cancel = serializers.BooleanField(required=False)
    review = serializers.IntegerField(required=False)
    receive_dog = serializers.BooleanField(required=False)
    return_dog = serializers.BooleanField(required=False)

    def validate_review(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("review range is 0 - 5")
        return value

class AddMealSerializer(serializers.Serializer):
    """
    Serializer สำหรับส่ง meal id
    """

    meal = serializers.IntegerField(required=False)

    def validate_meal(self, value):
        add_meal = Meal.objects.filter(id=value)
        if not add_meal.exists():
            raise serializers.ValidationError("Invalid meal")
        return value

class HostServiceSerializer(serializers.ModelSerializer):
    available_meals = MealSerializer(many=True, read_only=True)

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
            "available_meals",
            "deposit_price",
        ]
        read_only_fields = ["host"]
