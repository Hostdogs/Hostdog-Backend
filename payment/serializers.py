from rest_framework import serializers
from service.models import Services
from payment.models import Payments

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payments
        fields=['id','service','pay_date','pay_total','type_payments']
        read_only_fields =['service','pay_date','pay_total','type_payments']

class PaymentAcceptSerializer(serializers.Serializer):
    model=Payments
    accept_payment=serializers.BooleanField(required=True)

        

