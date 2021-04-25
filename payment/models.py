from django.db import models
from service.models import Service
# Create your models here.
class Payments(models.Model):
    service=models.ForeignKey(
        Service,on_delete=models.CASCADE, related_name="service-payments"
    )
    
    pay_date=models.TimeField()
    pay_total=models.FloatField()
    pay_bank_name=models.CharField()
    pay_status=models.CharField()
    type_payments=models.CharField()

    def __str__(self):
        return str(pay_bank_name)+' '+str(pay_total)
