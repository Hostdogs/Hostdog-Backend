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

# class CustomAccountManager(BaseUserManager):
#     """
#     Account manager
#     """
#     def create_superuser(self, email, username, password, firstname, lastname, **other_fields):
#         """
#         Create super user
#         """
#         other_fields.setdefault("is_staff", True)
#         other_fields.setdefault("is_superuser", True)
#         other_fields.setdefault("is_active", True)

#         if other_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must be assigned to is_staff=True.")
#         if other_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must be assigned to is_superuser=True.")
#         return self.create_user(email, username, password, firstname, lastname, **other_fields)


#     def create_user(self,email, username, password, firstname, lastname, **other_fields):
#         """
#         Create user
#         """
#         if not email:
#             raise ValueError(gettext_lazy("You must provide an email address"))
#         email = self.normalize_email(email)
#         user = self.model(
#             email=email, username=username, firstname=firstname, lastname=lastname, **other_fields
#         )
#         user.set_password(password)
#         user.save()
#         return user


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