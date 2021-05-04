from celery.utils.log import get_task_logger
from celery.decorators import task
from notifications.email import (
    send_email_host_service,
    send_email_customer_service_reach,
    send_email_customer_host_response,
    send_email_host_service_cancelled,
    send_email_host_service_review,
    send_email_customer_near_end_time,
    send_email_to_host_paid,
)

logger = get_task_logger(__name__)


@task(name="send_email_to_host_service")
def send_email_host_service_task(
    email, customer_first_name, customer_last_name, host_first_name, host_last_name
):
    logger.info("Sent service request email to host")
    return send_email_host_service(
        email, customer_first_name, customer_last_name, host_first_name, host_last_name
    )


@task(name="send_email_to_customer_on_service_reach")
def send_email_customer_service_reach_task(
    email,
    customer_first_name,
    customer_last_name,
    host_first_name,
    host_last_name,
    start_date,
    end_date,
    price,
):
    logger.info("Sent service notification email to customer")
    return send_email_customer_service_reach(
        email,
        customer_first_name,
        customer_last_name,
        host_first_name,
        host_last_name,
        start_date,
        end_date,
        price
    )

@task(name="send_email_to_customer_on_host_accept")
def send_email_customer_host_response_task(email, customer_first_name, customer_last_name, host_first_name, host_last_name, accept):
    logger.info("Send host response to customer")
    return send_email_customer_host_response(email, customer_first_name, customer_last_name, host_first_name, host_last_name, accept)

@task(name="send_email_host_service_cancelled")
def send_email_host_service_cancelled_task(email, customer_first_name, customer_last_name, host_first_name, host_last_name):
    logger.info("Send host about service cancelled")
    return send_email_host_service_cancelled(email, customer_first_name, customer_last_name, host_first_name, host_last_name)

@task(name="send_email_host_service_review")
def send_email_host_service_review_task(email, customer_first_name, customer_last_name, host_first_name, host_last_name, review):
    logger.info("Send host about service review score")
    return send_email_host_service_review(email, customer_first_name, customer_last_name, host_first_name, host_last_name, review)

@task(name="send_email_customer_near_end_time")
def send_email_customer_near_end_time_task(email, customer_first_name, customer_last_name, host_first_name, host_last_name, endtime):
    logger.info("Send customer about service near end time")
    return send_email_customer_near_end_time(email, customer_first_name, customer_last_name, host_first_name, host_last_name, endtime)

@task(name="send_email_customer_paid_host")
def send_email_customer_paid_host_task(email, customer_first_name, customer_last_name, host_first_name, host_last_name,price):
    logger.info("Send host about customer paid")
    return send_email_to_host_paid(email, customer_first_name, customer_last_name, host_first_name, host_last_name, price)
