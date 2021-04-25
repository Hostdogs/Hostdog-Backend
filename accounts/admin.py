from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Accounts, Customer, Host, Dog
from rest_framework.authtoken.admin import TokenAdmin


class CustomUserAdmin(UserAdmin):

    model = Accounts
    list_display = (
        "email",
        "username",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "username",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)

class DogAdmin(admin.ModelAdmin):
    list_filter = ('customer')


TokenAdmin.raw_id_fields = ["user"]

admin.site.register(Accounts, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Host)
admin.site.register(Dog)

