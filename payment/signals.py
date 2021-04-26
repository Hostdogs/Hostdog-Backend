from django.db.models.signals import post_save
from django.dispatch import receiver
from service.models import Service,Payments,HostService

@receiver(post_save,sender=Service)
def create_payment_post_save(sender,instance,created,**kwargs):

    print('post_save working')

    if instance.main_status=="payment":
        print('if payment in post_save working')
        host_service_instance=instance.additional_service
        total_price=0
        host_service_price=[host_service_instance.price_dog_walk,
                        host_service_instance.price_get_dog,
                        host_service_instance.price_deliver_dog,
                        host_service_instance.price_bath_dog ]

        enable_service=[host_service_instance.enable_dog_walk:,
                        host_service_instance.enable_get_dog,
                        host_service_instance.enable_delivery_dog,
                        host_service_instance..enable_bath_dog
                        ]

        for i in range(len(enable_service)):
            if enable_service[i]:
                total_price+=host_service_price[i]

        Payments.objects.create(service=instance,pay_total=total_price,type_payments='deposit')
        
    else if instance.main_status=='late':
        pass


        

    # service=models.ForeignKey(
    #     Service,on_delete=models.CASCADE, related_name="service-payments"
    # )

    # is_paid=models.BooleanField(default=false)

    # pay_date=models.TimeField()
    
    # pay_total=models.FloatField()

    # type_payments=models.CharField(choices=TYPE_PAYMENT)

