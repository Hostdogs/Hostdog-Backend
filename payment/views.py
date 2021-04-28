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

    @action(methods=["post"],detail=True, url_path="paydeposit", url_name="paydeposit")
    def pay_deposit(self,request,pk=None):
    #TO-DO: notification payment

        serializer=PaymentAcceptSerializer(data=request.data)
        if serializer.is_valid():
            payment=self.get_object()
            payment.is_paid=True
            payment.pay_date=timezone.now()
            payment.save()
            return Response(
                {"status": "success", "message": "Pay Deposit Accept Completed"},
                status=status.HTTP_200_OK,)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(methods=["post"],detail=True, url_path="paylate", url_name="paylate")
    def pay_late(self,request,pk=None):
        serializer=PaymentAcceptSerializer(data=request.data)
        if serializer.is_valid():
            payment=self.get_object()
            payment.is_paid=True
            payment.pay_date=timezone.now()
            payment.save()
            return Response(
                {"status": "success", "message": "Pay Deposit Accept Completed"},
                status=status.HTTP_200_OK,)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


