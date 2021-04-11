from django.contrib import admin
from .models import Accounts, Customer, Host, Dog

admin.site.register(Accounts)
admin.site.register(Customer)
admin.site.register(Host)


class DogAdmin(admin.ModelAdmin):
    list_filter = ('customer')