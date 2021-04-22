from django.db.models.signals import post_save
from accounts.models import Host
from service.models import HostService
from django.dispatch import receiver

@receiver(post_save, sender=Host)
def create_host_service(sender, instance, created, **kwargs):
    """
    Callback function for create host service after Host profile was create
        - This callback function activate after receive post_save signal from Host model
        - After Host profile was create --> create host service for that profile
        - *host service (see Model HostService in service/models.py)
    """
    if created:
        print(sender, instance, created)
        HostService.objects.create(host=instance)
