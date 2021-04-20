from django.db import models
from accounts.models import Host, Customer, Dog, Accounts
from django.utils import timezone


class Meal(models.Model):
    """
    Meal model
        - food for dog to eat
        - can add later in production
        - can adjust the price in production
    """

    meal_type = models.CharField(max_length=50)
    meal_price = models.FloatField()

    def __str__(self):
        return f"""Meals : {self.meal_type}\n
                Price : {self.meal_price} Baht
                """


class HostService(models.Model):
    """
    Additional service model eg. Dog walk, Dog bath
        - Host can enable/disable the additional service in their profile or something
        - Host can adjust the additional service price

    """

    host = models.OneToOneField(Host, on_delete=models.CASCADE, primary_key=True)
    price_dog_walk = models.FloatField(default=0.0)
    price_get_dog = models.FloatField(default=0.0)
    price_deliver_dog = models.FloatField(default=0.0)
    price_bath_dog = models.FloatField(default=0.0)
    enable_dog_walk = models.BooleanField(default=True)
    enable_get_dog = models.BooleanField(default=True)
    enable_delivery_dog = models.BooleanField(default=True)
    enable_bath_dog = models.BooleanField(default=True)

    def __str__(self):
        return f""" Additional service of {self.host}\n
                    1.) Walk the dog : {self.price_dog_walk} {'ENABLE' if self.enable_dog_walk else 'DISABLE'}\n
                    2.) Get the dog : {self.price_get_dog} {'ENABLE' if self.enable_get_dog else 'DISABLE'}\n
                    3.) Deliver the dog : {self.price_deliver_dog} {'ENABLE' if self.enable_delivery_dog else 'DISABLE'}\n
                    4.) Bath the dog : {self.price_bath_dog} {'ENABLE' if self.enable_bath_dog else 'DISABLE'}"""


class Service(models.Model):
    """
    Service model
        - store pending, end, in_progress service
        - !!! IMPORTANT !!! This model store all of service in hostdog system (Pending service, End service and In progress service)
    """

    MAIN_STATUS = (
        ("pending", "Pending"),
        ("end", "End"),
        ("in_progress", "In progress"),
    )
    STATUS = (
        ("time_of_service", "Time of service"),
        ("้host_is_waiting_to_receive_your_dog", "Host is waiting to receive your dog"),
        ("caring_for_your_dog", "Caring for your dog"),
        ("come_and_get_your_dog", "Come and get your dog"),
        ("service_success", "Service success"),
    )
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    service_status = models.CharField(max_length=10, choices=STATUS)
    service_is_over_night = models.BooleanField(default=False)
    service_create_time = models.DateTimeField(auto_now_add=True)
    service_start_time = models.DateField()
    service_end_time = models.DateField(blank=True, null=True)
    service_send_time = models.DateTimeField(blank=True, null=True)
    service_get_time = models.DateTimeField(blank=True, null=True)
    service_meal_type = models.ForeignKey(Meal, on_delete=models.CASCADE)
    service_meal_per_day = models.IntegerField()
    service_meal_weight = models.IntegerField()
    is_dog_walk = models.BooleanField(default=False)
    is_get_dog = models.BooleanField(default=False)
    is_delivery_dog = models.BooleanField(default=False)
    is_bath_dog = models.BooleanField(default=False)
    service_bio = models.TextField(max_length=255, default="")
    main_status = models.CharField(max_length=20, choices=MAIN_STATUS)

    def __str__(self):
        return f"""Service by {self.host}\n
                Customer : {self.customer}\n
                Dog : {self.dog}\n
                Status : {self.service_status}\n
                Main status : {self.main_status}
                """