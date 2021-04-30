from celery.decorators import task
from datetime import datetime, date
from payment.models import Payments
from service.models import HostService
from accounts.models import DogFeedingTime

@task(name="add_late_payment")
def add_late_payment():
    payment_that_late = Payments.objects.filter(type_payments="late",is_paid=False)
    for payment in payment_that_late:
        deposit_price=payment.service.additional_service.deposit_price
        late_price=float(1.5*(deposit_price))
        payment.pay_total+=late_price
        payment.save()
    return f"Late Payment: {payment_that_late.count()}"
