from django.db import models
from accounts.models import Customer, Host
from service.models import Service

# Create your models here.


class Notifications(models.Model):
    """
    Notifications model
        - Customer send request to host for service
        - Host can accept or decline the service
        - If Host accept/decline notification will warn the customer about that
        - Cant send duplicate of Notification to the same host (New service request = New notification(Old notification will be delete))
        - May be 2 type of notification : message only and message&Interact(Accept, Decline)
    """

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer"
    )
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="host")
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service"
    )
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    received_date = models.DateTimeField(auto_now_add=True)

    