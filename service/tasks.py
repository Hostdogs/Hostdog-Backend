from celery.decorators import task
from service.models import Services
from payment.models import Payments
from django.utils.timezone import localtime, timedelta
from notifications.tasks import (
    send_email_customer_service_reach_task,
    send_email_customer_near_end_time_task,
)


@task(name="add")
def add(x, y):
    """
    Test LOL 55555
    """
    return x + y


@task(name="check_incoming_service")
def check_wait_for_progress_service():
    """
    Task นี้มีไว้เช็คว่าถึงเวลาบริการของ service นั้นหรือยัง (เฉพาะ Service ที่ wait_for_progress)
    ถ้าถึงแล้วก็ปรับ main_status เป็น in_progress แล้วสร้าง Notification แจ้งเตือนcustomer กับ host ด้วย

    schedule : ทำการรัน Task นี้ทุกๆ 1 นาที
    """

    all_service_wait_for_progress_today = Services.objects.filter(
        main_status="wait_for_progress", service_start_time__lte=localtime()
    )
    for (
        service
    ) in (
        all_service_wait_for_progress_today
    ):  # ทำการส่งอีเมลล์แจ้งเตือน และ แก้ไขค่าใน service
        customer = service.customer
        host = service.host
        email = customer.account.email
        customer_first_name = customer.first_name
        customer_last_name = customer.last_name
        host_fist_name = host.first_name
        host_last_name = host.last_name
        start_date = service.service_start_time
        end_date = service.service_end_time
        service.main_status = "payment"
        service.service_status = "time_of_service"
        # service.save(update_fields=["main_status","service_status"])
        service.save()

        price=Payments.objects.get(service=service).pay_total
        send_email_customer_service_reach_task(
            email,
            customer_first_name,
            customer_last_name,
            host_fist_name,
            host_last_name,
            start_date,
            end_date,
            price,
        )
    # ตรงนี้คือหลังจาก ปรับ service ที่ wait_for_progress เป็น in_progress [x]
    # ส่งเมลล์เตือน Customer [x]

    # - ทำการแก้ field ของ Service ว่าได้สร้าง Payment มัดจำเรียบร้อยแล้ว created_deposit_payment = True [x]
    #   ระบบ Payment ต้อง Listening ที่ post_save signal เช็คว่า field นี้ถูกเปลี่ยนก็สร้าง Payment เลย

    return f"New service in progress : {all_service_wait_for_progress_today.count()}"


@task(name="check_late_service")
def check_in_progress_service_that_late():
    """
    Task นี้มีไว้เช็คว่า service ไหน in_progress อยู่แล้ว Late โดยเช็คจาก service end time
    ก็จะทำการปรับ field created_late_payment = True แล้วสร้าง Payment โดยคิดราคาจากที่ Host ตั้งไว้
    ถ้ามี Late payment อยู่แล้ว(แสดงว่าเลทมาแล้วหลายวัน) ก็บวกราคาเพิ่มเข้าไปที่ Payment นั้นโดยดูจากราคาที่ Host ตั้งไว้

    schedule : ทำการรัน Task นี้ทุก 1 นาที
    """
    in_progress_service_that_late = Services.objects.filter(
        main_status="in_progress", service_end_time__lt=localtime()-timedelta(days=1)
    )
    for service in in_progress_service_that_late:
        service.main_status = "late"
        service.days_late = (localtime() - service.service_end_time).days
        service.save()
    #   - Payment ต้อง Listening ที่ post_save signal ว่ามีการเปลี่ยนแปลงที่ field created_late_payment
    #   - สร้าง Notification แจ้งเตือนให้
    #   - ส่งเมลล์แจ้งเตือน

    return f"Service that late : {in_progress_service_that_late.count()}"


@task(name="notify_near_end_service")
def notify_near_end_service(before_hour):
    """
    Task นี้มีไว้แจ้งเตือน Customer เมื่อ Service ใกล้จะจบลงโดยจะแจ้งเตือนก่อนจบ x ชั่วโมง

    schedule : ทำการรัน Task นี้ทุกๆ 1 ชั่วโมง
    """
    service_that_near_end = Services.objects.filter(
        main_status="in_progress",
        service_end_time__hour=(localtime() + timedelta(hours=before_hour)).hour,
    )
    for service in service_that_near_end:
        email = service.customer.account.email
        customer = service.customer
        host = service.host
        send_email_customer_near_end_time_task(
            email,
            customer.first_name,
            customer.last_name,
            host.first_name,
            host.last_name,
            service.service_end_time
        )
    return f"Service that near end : {service_that_near_end.count()}"

@task(name="service_not_pay_in_service_time")
def cancel_that_service():
    service_objects=Services.objects.filter(main_status="payment")
    
    for service in service_objects:
        payment=Payments.objects.get(service=service,type_payment="deposit")
        if not payment.is_paid and localtime()-service.service_start_time > timedelta(hours=1)  :
            service.main_status="cancelled"
            service.service_status="you_cancel_this_service"
            service.save()
    return f"payment service: {service_objects}"
