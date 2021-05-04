from accounts.models import Accounts, Dog, Customer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import localtime

@receiver(post_save, sender=Dog)
def update_increment_customer_dog_count(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        customer.customer_dog_count += 1
        customer.save()

@receiver(post_delete, sender=Dog)
def update_decrement_customer_dog_count(sender, instance, using, **kwargs):
    customer = instance.customer
    customer.customer_dog_count -= 1
    customer.save()

@receiver(post_save, sender=Accounts)
def update_last_login(sender, instance, created, **kwargs):
    if created:
        instance.last_login = localtime()
        instance.save()