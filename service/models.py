from django.db import models
from accounts.models import Host,Customer,Dog
import datetime

class Meal(models.Model):
    host = models.ForeignKey(Host,on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=50)
    meal_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.meal_type



class Service(models.Model):

    host = models.ForeignKey(Host,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    dog = models.OneToOneField(Dog,on_delete=models.CASCADE)
    service_status = models.CharField(max_length=10)
    service_is_over_night = models.BooleanField(default=False)
    service_reg_time = models.DateTimeField(default=datetime.date.today)
    service_end_time = models.DateTimeField(default=datetime.date.today)
    service_meal_type = models.ForeignKey(Meal,on_delete=models.CASCADE)
    service_meal_per_day = models.IntegerField()
    service_meal_weight = models.IntegerField(default=20)
    service_is_walk = models.BooleanField(default=False)
    service_is_get_dog = models.BooleanField(default=False)
    service_is_ride_dog = models.BooleanField(default=False)
    service_is_dog_bath = models.BooleanField(default=False)
    service_bio = models.TextField(max_length=255,default="")


# class HostService(models.Model):










