from celery.decorators import task
from datetime import datetime, date
from payment.models import Payments
from service.models import HostService
from accounts.models import DogFeedingTime

@task(name="add_late_payment")
def add_late_payment():
    payment_that_late = Payments.objects.filter(type_payments="late",is_paid=False)
    for payment in payment_that_late:
        dog_feeding_time_object=DogFeedingTime.objects.filter(dog=payment.service.dog)
        meal_per_day=dog_feeding_time_object.count()
        meal_price=payment.service.service_meal_type.meal_price
        meal_weight=payment.service.service_meal_weight
        deposit_price=payment.service.additional_service.deposit_price
        late_price=deposit_price+(meal_per_day*meal_price*meal_weight)
        payment.total_price+=late_price
        payment.save()
    return f"Late Payment: {payment_that_late.count()}"
