from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from service.models import Services,HostService
from payment.models import Payments
from datetime import datetime, date
from accounts.models import DogFeedingTime

@receiver(pre_save,sender=Services)
def create_payment_pre_save(sender,instance,**kwargs):

    print('post_save working')
    print("instance.main_status:",instance.main_status,"instance.created_deposit_payment:",instance.created_deposit_payment)
    if instance.main_status=="payment" and not instance.created_deposit_payment:
        print('if payment in post_save working')

        payment_instance=Payments.objects.get(service=instance)

        host_service_instance=instance.additional_service

        dog_feeding_time_object=DogFeedingTime.objects.filter(dog=instance.dog)

        meals_per_day=dog_feeding_time_object.count()

        days=(instance.service_end_time-instance.service_start_time).days

        total_meal_price=meals_per_day*instance.service_meal_weight*instance.service_meal_type.meal_price*days

        total_price=instance.service.additional_service.deposit_price+total_meal_price

        host_service_price=[host_service_instance.price_dog_walk,
                        host_service_instance.price_get_dog,
                        host_service_instance.price_deliver_dog,
                        host_service_instance.price_bath_dog ]

        enable_service=[host_service_instance.enable_dog_walk,
                        host_service_instance.enable_get_dog,
                        host_service_instance.enable_delivery_dog,
                        host_service_instance.enable_bath_dog
                        ]

        for i in range(len(enable_service)):
            if enable_service[i]:
                total_price+=host_service_price[i]

        Payments.objects.create(service=instance,pay_total=total_price,type_payments='deposit')
        instance.save()

    elif instance.main_status=='late' and not instance.created_late_payment:
        Payments.objects.create(service=instance,pay_total=0,type_payments='late')
        instance.save()
    




