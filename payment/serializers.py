from rest_framework import serializers
from service.models import Service
from payment.models import Payments

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payments
        fields=['id','service','pay_date','pay_total','pay_bank_name','pay_status','type_payments']
        read_only_fields =['service','pay_date','pay_total','pay_bank_name','pay_status','type_payments']
        

        

