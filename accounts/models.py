from django.db import models
import datetime
from django.urls.conf import path
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser,
)
from django.db.models import F
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from uuid import uuid4

# Create your models here.
class Accounts(AbstractUser):
    """
    Authenticaton user model
        - Authen with username & password
    """

    is_host = models.BooleanField(default=False)
    account_number=models.CharField(max_length=20,blank=True)
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


class NearestHost(models.QuerySet):
    """
    QuerySet for query nearest host within x kilometer
    """

    def nearest_host_within_x_km(self, current_lat, current_long, x_km):
        """
        Greatest circle distance formula
        """
        dlat = Radians(F("latitude") - current_lat)
        dlong = Radians(F("longitude") - current_long)
        a = Power(Sin(dlat / 2), 2) + Cos(Radians(current_lat)) * Cos(
            Radians(F("latitude"))
        ) * Power(Sin(dlong / 2), 2)
        c = 2 * ATan2(Sqrt(a), Sqrt(1 - a))
        d = 6371 * c
        return self.annotate(distance=d).order_by("distance").filter(distance__lt=x_km)


class Host(models.Model):
    """
    Host profile model
        -store host info about hostdog
    """

    def path_and_rename(instance, filename):
        extension = filename.split(".")[-1]
        return f"hosts/{uuid4().hex}.{extension}"

    GENDER_OPTIONS = (("male", "Male"), ("female", "Female"), ("none", "None"))
    account = models.OneToOneField(
        Accounts,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="host_account",
    )
    picture = models.ImageField(
        verbose_name=_("Host's image"), upload_to=path_and_rename, blank=True
    )
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    gender = models.CharField(
        max_length=10, blank=False, default="Male", choices=GENDER_OPTIONS
    )
    host_bio = models.TextField(max_length=100, blank=True)
    host_rating = models.FloatField(default=0.0)
    host_hosted_count = models.IntegerField(default=0)
    host_max = models.IntegerField(default=0)
    host_avaliable = models.IntegerField(default=0)
    host_area = models.FloatField(default=0.0)
    address = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    dob = models.DateField(default=datetime.date.today)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    objects = models.Manager()
    nearest_host = NearestHost.as_manager()

    def __str__(self):
        return str(self.account)


class Customer(models.Model):
    """
    Customer profile model
        -store customer info about hostdog
    """

    def path_and_rename(instance, filename):
        extension = filename.split(".")[-1]
        return f"customers/{uuid4().hex}.{extension}"

    GENDER_OPTIONS = (("male", "Male"), ("female", "Female"), ("none", "None"))
    account = models.OneToOneField(
        Accounts,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="customer_account",
    )
    picture = models.ImageField(
        verbose_name=_("Customer's image"), upload_to=path_and_rename, blank=True
    )
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    gender = models.CharField(
        max_length=10, blank=False, default="Male", choices=GENDER_OPTIONS
    )
    customer_bio = models.TextField(max_length=100, blank=True)
    customer_dog_count = models.IntegerField(default=0)
    customer_hosted_count = models.IntegerField(default=0)
    address = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    dob = models.DateField(default=datetime.date.today)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    def __str__(self):
        return str(self.account)


class Dog(models.Model):
    """
    Dog profile model
        -store dog info
    """

    def path_and_rename(instance, filename):
        extension = filename.split(".")[-1]
        return f"dogs/{uuid4().hex}.{extension}"

    GENDER_OPTIONS = (("male", "Male"), ("female", "Female"))
    customer = models.ForeignKey(
        Customer, related_name="dog_customer", on_delete=models.CASCADE
    )
    picture = models.ImageField(
        verbose_name=_("Dog's image"), upload_to=path_and_rename, blank=True
    )
    dog_name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=10, blank=False, default="Male", choices=GENDER_OPTIONS
    )
    dog_bio = models.TextField(max_length=100, blank=True)
    dog_status = models.CharField(max_length=20)
    dog_create_date = models.DateField(auto_now_add=True)
    dog_dob = models.DateField(default=datetime.date.today)
    dog_breed = models.CharField(max_length=20)
    dog_weight = models.FloatField(default=0.0)

    def __str__(self):
        return self.dog_name


class HostAvailableDate(models.Model):
    """
    Host available date model
    """

    host = models.ForeignKey(
        Host, on_delete=models.CASCADE, related_name="host_available_date"
    )
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.date)


class DogFeedingTime(models.Model):
    """
    Dog feeding time model
    """

    dog = models.ForeignKey(
        Dog, on_delete=models.CASCADE, related_name="dog_feeding_time"
    )
    time = models.TimeField()

    def __str__(self):
        return str(self.time)


class HouseImages(models.Model):
    """
    House image model
    """

    def path_and_rename(instance, filename):
        extension = filename.split(".")[-1]
        return f"houses/{uuid4().hex}.{extension}"

    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="house_image")
    picture = models.ImageField(
        verbose_name=_("House picture"), upload_to=path_and_rename, blank=True
    )
