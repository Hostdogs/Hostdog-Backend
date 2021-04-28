from celery.decorators import task
from datetime import datetime, date
from payment.models import Payments
from service.models import HostService

@task(name="add_late_payment")
def add_late_payment():
    payment_that_late = Payments.objects.filter(type_payments="late",is_paid=False)
    for payment in payment_that_late:
        late_price=payment.service.additional_service.deposit_price+(payment.service.service_meal_per_day*payment.service.service_meal_type.meal_price)
        payment.total_price+=late_price
        payment.save()
    return f"Late Payment: {payment_that_late.count()}"
