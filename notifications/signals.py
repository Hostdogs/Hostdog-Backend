from django.db.models.signals import post_save
from service.models import Services
from django.dispatch import receiver

@receiver(post_save, sender=Services)
def create_notification(sender, instance, created, **kwargs):
    """
    Callback function for create notification after service is created as pending service
        - This Callback function activate after receive post_save(After save object to database) signal from Service model 
        - After customer select the service and choose everything their want and accept --> Send notification to host
    """
    #if service object is created and main_status field is pending then notification must be send to Host
    pass
