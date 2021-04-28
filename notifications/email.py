from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


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
    email, customer_first_name, customer_last_name, host_first_name, host_last_name, start_date, end_date
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
        "email": email,
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