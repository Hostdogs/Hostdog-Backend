from django.db import models
from service.models import Service
# Create your models here.
class Payments(models.Model):
    TYPE_PAYMENT=(('deposit','Deposit')('late','Late'))

    service=models.ForeignKey(
        Service,on_delete=models.CASCADE, related_name="service-payments"
    )

    is_paid=models.BooleanField(default=false)

    pay_date=models.TimeField()
    
    pay_total=models.FloatField()

    type_payments=models.CharField(choices=TYPE_PAYMENT)

    

    def __str__(self):
        return str(pay_bank_name)+' '+str(pay_total)
