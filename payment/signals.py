from django.db.models.signals import post_save
from django.dispatch import receiver
from service.models import Service,Payments,HostService

@receiver(post_save,sender=Service)
def create_payment_post_save(sender,instance,created,**kwargs):

    print('post_save working')

    if instance.main_status=="payment":

        HostService.objects.get()
        
        Payments.objects.create(service=instance)

        print('if in post_save')

    # service=models.ForeignKey(
    #     Service,on_delete=models.CASCADE, related_name="service-payments"
    # )

    # is_paid=models.BooleanField(default=false)

    # pay_date=models.TimeField()
    
    # pay_total=models.FloatField()

    # type_payments=models.CharField(choices=TYPE_PAYMENT)

