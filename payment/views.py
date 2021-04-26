from django.shortcuts import render
from payment.models import Payments
from payment.serializers import PaymentSerializer
# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    queryset=Payments.objects.all()
    serializer_class=PaymentSerializer
    http_method_names = ["get"]