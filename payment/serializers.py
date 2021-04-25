from rest_framework import serializers
from service.models import Service
from payment.models import Payments

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payments
        fields=['id','service','pay_date','pay_total','pay_bank_name','pay_status','type_payments']
            service=models.ForeignKey(
        Service,on_delete=models.CASCADE, related_name="service-payments"
    )

        read_only_fields =['service','pay_date']
    def create(self,validated_data):
        #ไม่แน่ใจว่าถูกไหม
        service_id=self.context["view"].kwargs["service_pk"]
        service=Service.object.get(id=service_id)
        payment =Payments.objects.create(service=service,**validated_data)
        return payment

        

