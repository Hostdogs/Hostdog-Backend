from celery.decorators import task
from accounts.models import HostAvailableDate
from django.utils.timezone import localtime
from datetime import date

@task(name="delete_past_available_date")
def delete_past_available_date_task():
    """
    Task นี้มีไว้ลบ available date ที่ Past

    schedule : ทำการรัน Task นี้ทุกๆ 1 นาที
    """
    past_available_date = HostAvailableDate.objects.filter(date__lt=date.today())
    past_available_date.delete()
    return f"Past available date : {past_available_date.count()}]"