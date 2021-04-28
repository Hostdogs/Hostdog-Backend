from django.shortcuts import render
from payment.models import Payments
from payment.serializers import PaymentSerializer,PaymentAcceptSerializer
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    queryset=Payments.objects.all()
    serializer_class=PaymentSerializer
    http_method_names = ["get","head","options"]

    @action(method=["post"],detail=True)
    def pay(self,request,pk=None):
    #TO-DO: notification payment
        serializer=PaymentAcceptSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data.get("accept_payment"):
                payment=self.get_object()
                payment.is_paid=True
                payment.pay_date=timezone.now()
                payment.save()
                
                return Response(
                {"status": "success", "message": "Pay Accept Completed"},
                status=status.HTTP_200_OK,)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


