from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser,
)

# Create your models here.


class Accounts(AbstractUser):
    """
    Authenticaton user model
        - Authen with username & password
    """

    is_host = models.BooleanField(default=False)
    first_name = None
    last_name = None

    def save(self, *args, **kwargs):
        """
        Create Host or customer profile on save of account to database
        """
        created = not self.pk
        super(Accounts, self).save(*args, **kwargs)
        if created:
            if self.is_host:
                Host.objects.create(account=self)
            else:
                Customer.objects.create(account=self)

    def __str__(self):
        return self.username


class Host(models.Model):
    """
    Host profile model
        -store host info about hostdog
    """
    account = models.OneToOneField(Accounts, on_delete=models.CASCADE,primary_key=True)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    host_bio = models.TextField(max_length=100, blank=True)
    host_rating = models.FloatField(default=0.0)
    host_hosted_count = models.IntegerField(default=0)
    host_max = models.IntegerField(default=0)
    host_avaliable = models.IntegerField(default=0)
    host_area = models.FloatField(default=0.0)
    host_schedule = models.TextField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    dob = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.account_id)


class Customer(models.Model):
    """
    Customer profile model
        -store customer info about hostdog
    """
    account = models.OneToOneField(Accounts, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    customer_bio = models.TextField(max_length=100, blank=True)
    customer_dog_count = models.IntegerField(default=0)
    customer_hosted_count = models.IntegerField(default=0)
    address = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    dob = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.account_id)

class Dog(models.Model):
    """
    Dog profile model
        -store dog info 
    """
    customer = models.ForeignKey(Customer, to_field="account" , on_delete=models.CASCADE)
    dog_name = models.CharField(max_length=50)
    dog_bio = models.TextField(max_length=100)
    dog_status = models.CharField(max_length=20)
    dog_create_date = models.DateField(auto_now_add=True)
    dog_dob = models.DateField(default=datetime.date.today)
    dog_breed = models.CharField(max_length=20)
    dog_weight = models.FloatField(default=0.0)

    def __str__(self):
        return self.dog_name
