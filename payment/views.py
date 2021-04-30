from django.shortcuts import render
from payment.models import Payments
from payment.serializers import PaymentSerializer, PaymentAcceptSerializer
from rest_framework.response import Response
from django.utils.timezone import localtime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework_extensions.mixins import NestedViewSetMixin
from notifications.tasks import send_email_customer_paid_host_task

# Create your views here.
class PaymentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ["post", "get", "head", "options"]

    @action(methods=["post"], detail=True, url_path="paydeposit", url_name="paydeposit")
    def pay_deposit(self, request, pk=None, service_pk=None):
        # TO-DO: notification payment

        serializer = PaymentAcceptSerializer(data=request.data)
        if serializer.is_valid():
            payment = self.get_object()
            payment.is_paid = True
            payment.pay_date = localtime()
            payment.save()

            service = payment.service
            host = service.host
            customer = service.customer
            email = host.account.email
            customer_first_name = customer.first_name
            host_first_name = host.first_name
            customer_last_name = customer.last_name
            host_last_name = host.last_name
            price = payment.pay_total
            send_email_customer_paid_host_task(
                email,
                customer_first_name,
                customer_last_name,
                host_first_name,
                host_last_name,
                price,
            )
            return Response(
                {"status": "success", "message": "Pay Deposit Accept Completed"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=True, url_path="paylate", url_name="paylate")
    def pay_late(self, request, pk=None):
        serializer = PaymentAcceptSerializer(data=request.data)
        if serializer.is_valid():
            payment = self.get_object()
            payment.is_paid = True
            payment.pay_date = localtime()
            payment.save()
            return Response(
                {"status": "success", "message": "Pay Deposit Accept Completed"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
