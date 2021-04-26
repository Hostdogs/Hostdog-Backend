from celery.decorators import task
from datetime import datetime, date
from payment import Payments
from service.models import HostService

@task(name="add_late_payment")
def add_late_payment():
    payment_that_late = Payments.objects.filter(type_payments="late")
    for payment in payment_that_late:
        payment.total_price+=payment.service.additional_service.late_price
        payment.save()
    return f"Late Payment: {payment_that_late.count()}"
