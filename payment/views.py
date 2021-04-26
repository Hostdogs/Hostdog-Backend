from django.shortcuts import render
from payment.models import Payments
from payment.serializers import PaymentSerializer
from rest_framework.response import Response
from django.utils import timezone
# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    queryset=Payments.objects.all()
    serializer_class=PaymentSerializer
    http_method_names = ["get","head","options"]

    @action(method=["post"],detail=True)
    def pay(self,request,pk=None):
        payment=self.get_object()
        payment.is_paid=True
        payment.pay_date=timezone.now()
        payment.save()


