from celery.utils.log import get_task_logger
from celery.decorators import task
from notifications.email import (
    send_email_host_service,
    send_email_customer_service_reach,
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
    )
