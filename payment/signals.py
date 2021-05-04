from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from service.models import Services, HostService
from payment.models import Payments
from accounts.models import DogFeedingTime
from django.utils.timezone import datetime, timedelta, make_aware, localtime


@receiver(post_save, sender=Services)
def create_payment_post_save(sender, created, instance, update_fields, **kwargs):

    print("post_save working")

    if instance.main_status == "payment" and not instance.created_deposit_payment:
        total_price = instance.calculate_price()
        Payments.objects.create(
            service=instance, pay_total=total_price, type_payments="deposit"
        )

    elif instance.main_status == "late" and not instance.created_late_payment:
        Payments.objects.create(service=instance, pay_total=0, type_payments="late")
