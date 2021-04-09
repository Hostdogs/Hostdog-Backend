from django.db import models
import datetime
from django.utils.translation import gettext_lazy 
from django.contrib.auth.models import (
    AbstractUser,
)
# Create your models here.



class Accounts(AbstractUser):
    """
    Authenticaton user model
        - Authen with username & password
    """
    options = (
        ("customer", "Customer"),
        ("host", "Host"),
    )
    role = models.CharField(max_length=10, choices=options, blank=True)
    address = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    dob = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.username

    
    
class Host(models.Model):
    """
    Host profile model
        -store host info about hostdog
    """
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    host_bio = models.TextField(max_length=100)
    host_rating = models.FloatField(max_length=3)
    host_hosted_count = models.IntegerField(max_length=4)
    host_max = models.IntegerField(max_length=2)
    host_avaliable = models.IntegerField(max_length=2)
    host_area = models.FloatField(max_length=4)
    host_schedule = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return str(self.account_id)


class Customer(models.Model):
    """
    Customer profile model
        -store customer info about hostdog
    """
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    customer_bio = models.TextField(max_length=100)
    customer_dog_count = models.IntegerField(max_length=3)
    customer_hosted_count = models.IntegerField(max_length=3)

    def __str__(self):
        return str(self.account_id)

class Dog(models.Model):
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    dog_name = models.CharField(max_length=50)
    dog_bio = models.TextField(max_length=100)
    dog_status = models.CharField(max_length=20)
    dog_create_date = models.DateField(auto_now_add=True)
    dog_dob = models.DateField(default=datetime.date.today())
    dog_breed = models.CharField(max_length=20)
    dog_weight = models.FloatField(max_length=6)

    def __str__(self):
        return self.dog_name

