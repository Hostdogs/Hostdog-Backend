from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.timezone import localtime


def send_email_host_service(
    email, customer_first_name, customer_last_name, host_first_name, host_last_name
):
    """
    1.) ส่งหา Host เมื่อ Customer ส่ง request มาหา
    """
    context = {
        "customer_first_name": customer_first_name,
        "customer_last_name": customer_last_name,
        "host_first_name": host_first_name,
        "host_last_name": host_last_name,
        "email": email,
    }
    email_subject = "มีผู้ใช้บริการต้องการให้คุณเลี้ยงหมา"
    email_body = render_to_string("email_host_service.txt", context)

    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
    )
    return email.send(fail_silently=False)


def send_email_customer_service_reach(
    email, customer_first_name, customer_last_name, host_first_name, host_last_name, start_date, end_date,price
):
    """
    2.) ส่งหา Customer เมื่อถึงเวลาการให้บริการแล้ว
    """
    context = {
        "customer_first_name": customer_first_name,
        "customer_last_name": customer_last_name,
        "host_first_name": host_first_name,
        "host_last_name": host_last_name,
        "start_date": start_date,
        "end_date": end_date,
        "email": email,
        "price":price
    }
    email_subject = "ถึงวันใช้บริการของคุณแล้ว"
    email_body = render_to_string("email_customer_service_reach.txt", context)
    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
    )
    return email.send(fail_silently=False)


def send_email_customer_host_response(
    email, customer_first_name, customer_last_name, host_first_name, host_last_name, accept
):
    """
    3.) ส่งหา Customer เมื่อ Host ตอบรับการบริการ
    """
    context = {
        "accept" : accept,
        "customer_first_name": customer_first_name,
        "customer_last_name": customer_last_name,
        "host_first_name": host_first_name,
        "host_last_name": host_last_name,
        "email": email
    }
    email_subject = f"Host ได้{'ยืนยัน' if accept else 'ปฏิเสธ'}การบริการของคุณแล้ว"
    email_body = render_to_string("email_customer_host_accept.txt", context)
    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
    )
    return email.send(fail_silently=False)

def send_email_host_service_cancelled(email, customer_first_name, customer_last_name, host_first_name, host_last_name):
    """
    4.) ส่งหา Host เมื่อ Customer ยกเลิก Service
    """
    context = {
        "customer_first_name": customer_first_name,
        "customer_last_name": customer_last_name,
        "host_first_name": host_first_name,
        "host_last_name": host_last_name,
        "email": email,
    }
    email_subject = "Customer ได้ยกเลิกบริการของคุณแล้ว"
    email_body = render_to_string("email_customer_host_accept.txt", context)
    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
    )
    return email.send(fail_silently=False)

def send_email_host_service_review(email, customer_first_name, customer_last_name, host_first_name, host_last_name, review):
    """
    5.) ส่งหา Host เมื่อได้รับ Review จาก Customer
    """
    context = {
        "score": review,
        "customer_first_name": customer_first_name,
        "customer_last_name": customer_last_name,
        "host_first_name": host_first_name,
        "host_last_name": host_last_name,
        "email": email,
    }
    email_subject = "Customer ได้ให้คะแนนการให้บริการของคุณ"
    email_body = render_to_string("email_host_service_review.txt", context)
    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
    )
    return email.send(fail_silently=False)

def send_email_customer_near_end_time(email, customer_first_name, customer_last_name, host_first_name, host_last_name, endtime):
    """
    6.) ส่งหา Customer เมื่อใกล้ถึงเวลา service_end_time
    """
    context = {
        "starttime": localtime(),
        "endtime": endtime,
        "customer_first_name": customer_first_name,
        "customer_last_name": customer_last_name,
        "host_first_name": host_first_name,
        "host_last_name": host_last_name,
        "email": email,
    }
    email_subject = "ใกล้ถึงเวลาสิ้นสุดบริการของคุณแล้ว"
    email_body = render_to_string("email_customer_near_end_time.txt", context)
    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
    )
    return email.send(fail_silently=False)
def send_email_to_host_paid(
    email, customer_first_name, customer_last_name, host_first_name, host_last_name,price
):
    """
    7.) ส่งว่า Customer จ่ายเงินแล้วให้ Host
    """
    context = {
        "customer_first_name": customer_first_name,
        "customer_last_name": customer_last_name,
        "host_first_name": host_first_name,
        "host_last_name": host_last_name,
        "email": email,
        "price":price
    }
    email_subject = f"Customer ได้จ่ายเงินแล้ว"
    email_body = render_to_string("send_email_to_host_paid.txt", context)
    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
    )
    return email.send(fail_silently=False)
