from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from service.models import Services,HostService
from payment.models import Payments
from accounts.models import DogFeedingTime
from django.utils.timezone import datetime,timedelta,make_aware,localtime
@receiver(post_save,sender=Services)
def create_payment_post_save(sender,created,instance,update_fields,**kwargs):

    print('post_save working')

    if  instance.main_status=="payment" and not instance.created_deposit_payment:
        print('if payment in post_save working')
        print("instance.additional_service:",instance.additional_service)
        
        host_service_instance=instance.additional_service
     
        dog_feeding_time_object=DogFeedingTime.objects.filter(dog=instance.dog)

        service_delta=localtime(instance.service_end_time).date()-localtime(instance.service_start_time).date()

        meal_weight=instance.service_meal_weight

        meal_price_per_gram=instance.service_meal_type.meal_price_per_gram

        all_date_within_interval = [
            localtime(instance.service_start_time).date() + timedelta(days=i)
            for i in range(service_delta.days + 1)
        ]


        meal_per_service=0

        for date in all_date_within_interval:
            for feedingtime in dog_feeding_time_object:
                date_feeding=datetime.combine(date,feedingtime.time)
                if localtime(instance.service_start_time) < make_aware(date_feeding) < localtime(instance.service_end_time):
                    meal_per_service+=1
                    
        print("meal_per_service:",meal_per_service)
        print("meal_price_per_gram",meal_price_per_gram)
        print("meal_weight",meal_weight)

        total_meal_price=meal_per_service*meal_price_per_gram*meal_weight

        days_for_deposit=len(all_date_within_interval)
        
        print("all_date_within_interval",all_date_within_interval)
        print("days_for_deposit:",days_for_deposit)
        print("host_service_instance.deposit_price",host_service_instance.deposit_price)
        print("total_meal_price",total_meal_price)
        total_price=(host_service_instance.deposit_price*days_for_deposit)+total_meal_price
        print("total_price_with_total_meal_price_before_add_additional:",total_price)

        host_service_price=[host_service_instance.price_dog_walk,
                        host_service_instance.price_get_dog,
                        host_service_instance.price_deliver_dog,
                        host_service_instance.price_bath_dog ]

        enable_service=[host_service_instance.enable_dog_walk,
                        host_service_instance.enable_get_dog,
                        host_service_instance.enable_delivery_dog,
                        host_service_instance.enable_bath_dog
                        ]
        additional_price=0
        for i in range(len(enable_service)):
            if enable_service[i]:
                total_price+=host_service_price[i]
                additional_price+=host_service_price[i]
        print("additional_price",additional_price)
        print("total_price_with_total_meal_price_after_add_additional",total_price)
        Payments.objects.create(service=instance,pay_total=total_price,type_payments='deposit')

        instance.save()

    elif instance.main_status=='late' and not instance.created_late_payment:
        Payments.objects.create(service=instance,pay_total=0,type_payments='late')
        instance.save()
    




