from payment.models import Payments
from django.db.models.signals import post_save
from accounts.models import Host
from service.models import HostService, Services
from django.dispatch import receiver
from notifications.tasks import send_email_host_service_task


@receiver(post_save, sender=Host)
def create_host_service(sender, instance, created, **kwargs):
    """
    Callback function for create host service after Host profile was create
        - This callback function activate after receive post_save signal from Host model
        - After Host profile was create --> create host service for that profile
        - *host service (see Model HostService in service/models.py)
    """
    if created:
        HostService.objects.create(host=instance)


@receiver(post_save, sender=Services)
def send_email_when_service_create(sender, instance, created, **kwargs):
    """
    ส่งอีเมลล์ไปหา Host เมื่อ Service ถูกสร้างจาก Customer
    """
    if created:
        host = instance.host
        customer = instance.customer
        email = host.account.email
        send_email_host_service_task(
            email,
            customer.first_name,
            customer.last_name,
            host.first_name,
            host.last_name,
        )


@receiver(post_save, sender=Payments)
def update_create_payment_field(sender, instance, created, **kwargs):
    """
    เมื่อ Payment ชนิด deposit ถูกสร้าง Field created_deposit_payment จะเป็น True
    เมื่อ Payment ชนิด late ถูกสร้าง Field created_late_payment จะเป็น True
    เมื่อ Payment ชนิด deposit ถูกจ่าย service_status จะเป็น Host รอรับหมา main_status เป็น In progress
    เมื่อ Payment ชนิด late ถูกจ่าย service_status จะเป็น Service จบแล้ว main_status จะเป็น end
    """
    service = instance.service
    type_payments = instance.type_payments
    if created:  # ถ้ามีการสร้าง Payment
        if type_payments == "deposit":
            service.created_deposit_payment = True
            service.save()
        elif type_payments == "late":
            service.created_late_payment = True
            service.save()
    else:
        if instance.is_paid:  # ถ้ามีการจ่ายเงินเกิดขึ้น
            if type_payments == "deposit" and service.main_status == "payment":
                service.main_status = "in_progress"
                service.service_status = "host_is_waiting_to_receive_your_dog"
                service.save()
            elif type_payments == "late" and service.main_status == "late":
                service.main_status = "end"
                service.service_status = "service_success"
                service.save()
