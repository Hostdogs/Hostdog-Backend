from django.db import models
from django.utils import timezone
import datetime
from django.utils.translation import gettext_lazy 
from django.contrib.auth.models import (
    AbstractUser,
    PermissionsMixin,
    BaseUserManager,
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