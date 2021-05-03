from django.db import models
from accounts.models import Host, Customer, Dog, HostAvailableDate, DogFeedingTime
from payment.models import Payments
from django.utils.timezone import localtime, make_aware, timedelta, datetime
from django.db.models import Sum
from notifications.tasks import (
    send_email_customer_host_response_task,
    send_email_host_service_cancelled_task,
    send_email_host_service_review_task,
)


class Meal(models.Model):
    """
    Meal model
        - food for dog to eat
        - can add later in production
        - can adjust the price in production
    """

    meal_type = models.CharField(max_length=50)
    meal_price_per_gram = models.FloatField()

    def __str__(self):
        return f"Meals : {self.meal_type}\nPrice : {self.meal_price_per_gram} Baht"


class HostService(models.Model):
    """
    Additional service model eg. Dog walk, Dog bath
        - Host can enable/disable the additional service in their profile or something
        - Host can adjust the additional service price

    """

    host = models.OneToOneField(
        Host,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="hostservice_host",
    )
    price_dog_walk = models.FloatField(default=0.0)
    price_get_dog = models.FloatField(default=0.0)
    price_deliver_dog = models.FloatField(default=0.0)
    price_bath_dog = models.FloatField(default=0.0)

    enable_dog_walk = models.BooleanField(default=False)
    enable_get_dog = models.BooleanField(default=False)
    enable_delivery_dog = models.BooleanField(default=False)
    enable_bath_dog = models.BooleanField(default=False)

    available_meals = models.ManyToManyField(Meal, related_name="available_meals")
    deposit_price = models.IntegerField(default=300)

    def __str__(self):
        return (
            f" Additional service of {self.host}\n"
            + f"1.) Walk the dog : {self.price_dog_walk} {'ENABLE' if self.enable_dog_walk else 'DISABLE'}\n"
            + f"2.) Get the dog : {self.price_get_dog} {'ENABLE' if self.enable_get_dog else 'DISABLE'}\n"
            + f"3.) Deliver the dog : {self.price_deliver_dog} {'ENABLE' if self.enable_delivery_dog else 'DISABLE'}\n"
            + f"4.) Bath the dog : {self.price_bath_dog} {'ENABLE' if self.enable_bath_dog else 'DISABLE'}"
        )


class Services(models.Model):
    """
    Service model
        - store pending, end, in_progress service
        - !!! IMPORTANT !!! This model store all of service in hostdog system (Pending service, Payment, End service and In progress service)
    """

    MAIN_STATUS = (
        ("pending", "Pending"),
        ("payment", "Payment"),
        ("end", "End"),
        ("wait_for_progress", "Wait for progress"),
        ("in_progress", "In progress"),
        ("late", "Late"),
        ("cancelled", "Cancelled"),
    )
    STATUS = (
        ("time_of_service", "Time of service"),
        ("้host_is_waiting_to_receive_your_dog", "Host is waiting to receive your dog"),
        ("caring_for_your_dog", "Caring for your dog"),
        ("come_and_get_your_dog", "Come and get your dog"),
        ("service_success", "Service success"),
        ("you_cancel_this_service", "You cancel this service"),
    )
    host = models.ForeignKey(
        Host, on_delete=models.CASCADE, related_name="service_host"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="service_customer"
    )
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name="service_dog")
    service_status = models.CharField(max_length=40, choices=STATUS)
    service_create_time = models.DateTimeField(auto_now_add=True)
    service_reply_time = models.DateTimeField(blank=True, null=True)
    service_start_time = models.DateTimeField()
    service_end_time = models.DateTimeField()
    service_send_time = models.DateTimeField(blank=True, null=True)
    service_get_time = models.DateTimeField(blank=True, null=True)
    service_meal_type = models.ForeignKey(
        Meal, on_delete=models.PROTECT, related_name="service_meal_type"
    )
    service_meal_weight = models.IntegerField()
    is_dog_walk = models.BooleanField(default=False)
    is_get_dog = models.BooleanField(default=False)
    is_delivery_dog = models.BooleanField(default=False)
    is_bath_dog = models.BooleanField(default=False)
    additional_service = models.ForeignKey(
        HostService, on_delete=models.CASCADE, related_name="additional_service"
    )
    service_bio = models.TextField(max_length=255, default="", blank=True)
    created_deposit_payment = models.BooleanField(default=False)
    created_late_payment = models.BooleanField(default=False)
    days_late = models.IntegerField(default=0)
    is_review = models.BooleanField(default=False)
    is_customer_receive_dog = models.BooleanField(default=False)
    rating = models.IntegerField(null=True)
    main_status = models.CharField(
        max_length=20, choices=MAIN_STATUS, default="pending"
    )
    total_price = models.IntegerField(null=True)

    def calculate_price(self):
        host_service_instance = self.additional_service
        dog_feeding_time_object = DogFeedingTime.objects.filter(dog=self.dog)
        service_delta = (
            localtime(self.service_end_time).date()
            - localtime(self.service_start_time).date()
        )
        meal_weight = self.service_meal_weight
        meal_price_per_gram = self.service_meal_type.meal_price_per_gram
        all_date_within_interval = [
            localtime(self.service_start_time).date() + timedelta(days=i)
            for i in range(service_delta.days + 1)
        ]
        meal_per_service = 0
        for date in all_date_within_interval:
            for feedingtime in dog_feeding_time_object:
                date_feeding = datetime.combine(date, feedingtime.time)
                if (
                    localtime(self.service_start_time)
                    < make_aware(date_feeding)
                    < localtime(self.service_end_time)
                ):
                    meal_per_service += 1

        total_meal_price = meal_per_service * meal_price_per_gram * meal_weight
        days_for_deposit = len(all_date_within_interval)

        total_price = (
            host_service_instance.deposit_price * days_for_deposit
        ) + total_meal_price

        host_service_price = [
            host_service_instance.price_dog_walk,
            host_service_instance.price_get_dog,
            host_service_instance.price_deliver_dog,
            host_service_instance.price_bath_dog,
        ]

        enable_service = [
            host_service_instance.enable_dog_walk,
            host_service_instance.enable_get_dog,
            host_service_instance.enable_delivery_dog,
            host_service_instance.enable_bath_dog,
        ]
        for i in range(len(enable_service)):
            if enable_service[i]:
                total_price += host_service_price[i]
        return total_price

    def accept(self):
        """
        If host accept the service
            - service main_status change to wait_for_progress [x]
            - delete range of date that cutomer register from host's available date [x]
            - create post_save signal to notification application [x]
        """
        # Host accept customer request
        if self.main_status == "pending":
            email = self.customer.account.email
            send_email_customer_host_response_task(
                email,
                self.customer.first_name,
                self.customer.last_name,
                self.host.first_name,
                self.host.last_name,
                True,
            )
            self.main_status = "wait_for_progress"
            self.service_reply_time = localtime()
            date_range = (
                localtime(self.service_start_time).date(),
                localtime(self.service_end_time).date(),
            )
            print("self.service_start_time:", self.service_start_time)
            print("self.service_end_time:", self.service_end_time)
            print("date_range:", date_range)
            HostAvailableDate.objects.filter(
                host=self.host, date__range=date_range
            ).delete()
            self.save()
            return True
        return False

    def decline(self):
        """
        If host decline the service
            - service main_status change to cancelled
        """
        if self.main_status == "pending":
            email = self.customer.account.email
            send_email_customer_host_response_task(
                email,
                self.customer.first_name,
                self.customer.last_name,
                self.host.first_name,
                self.host.last_name,
                False,
            )
            self.main_status = "cancelled"
            self.service_reply_time = localtime()
            self.save()
            return True
        return False

    def host_receive_dog(self):
        """
        Host สามารถรับหมาได้
        """
        # รับหมาได้เมื่อ Customer จ่าย Payment แล้ว
        payment = Payments.objects.get(service=self, type_payments="deposit")
        if payment.is_paid:
            self.service_status = "caring_for_your_dog"
            self.dog.dog_status = "hosting"
            self.service_send_time = localtime()
            self.save()
            self.dog.save()
            return True
        return False

    def customer_receive_dog(self):
        """
        Customer สามารถรับหมาคืนได้
        """
        # TODO กดรับหมาได้เมื่อ ...
        if self.main_status == "in_progress":
            self.is_customer_receive_dog = True
            self.save()
            return True
        return False

    def return_dog(self):
        """
        Host สามารถคืนหมาได้
        """
        # คืนหมาไม่ได้ถ้า Customer ยังไม่จ่ายค่าเลท
        # คืนหมาได้เมื่อ Customer กดรับหมาแล้ว
        if self.main_status == "in_progress" and self.is_customer_receive_dog:
            self.service_status = "service_success"
            self.main_status = "end"
            self.service_get_time = localtime()
            self.host.host_hosted_count += 1
            self.customer.customer_hosted_count += 1
            self.dog.dog_status = "idle"
            self.customer.save()
            self.host.save()
            self.dog.save()
            self.save()
            return True
        elif self.main_status == "late":
            late_payment = Payments.objects.get(service=self, type_payments="late")
            if late_payment.is_paid:
                self.main_status = "end"
                self.service_status = "service_success"
                self.service_get_time = localtime()
                self.host.host_hosted_count += 1
                self.customer.customer_hosted_count += 1
                self.dog.dog_status = "idle"
                self.customer.save()
                self.host.save()
                self.dog.save()
                self.save()
        return False

    def cancel(self):
        """
        Customer สามารถยกเลิกบริการได้
        """
        # ส่ง Email Notification ให้ Host
        # ลบ Payment ที่ไม่ได้จ่ายทิ้ง
        if self.main_status != "late":
            email = self.host.account.email
            send_email_host_service_cancelled_task(
                email,
                self.customer.first_name,
                self.customer.last_name,
                self.host.first_name,
                self.host.last_name,
            )
            self.main_status = "cancelled"
            self.service_status = "you_cancel_this_service"
            self.dog.dog_status = "idle"
            Payments.objects.filter(service=self, is_paid=False).delete()
            self.save()
            self.dog.save()
            return True
        return False

    def review(self, review_score):
        """
        Customer สามารถรีวิวบริการได้
        """
        # แจ้งเตือน Host ถึงคะแนน Review
        if self.main_status == "end":
            email = self.host.account.email
            send_email_host_service_review_task(
                email,
                self.customer.first_name,
                self.customer.last_name,
                self.host.first_name,
                self.host.last_name,
                review_score,
            )
            self.is_review = True
            if self.rating is None:
                self.rating = 0
            self.rating += review_score
            service_that_rate = Services.objects.filter(
                host=self.host, is_review=True, rating__isnull=False
            )
            other_rating = 0
            if service_that_rate.count() > 0:
                other_rating = service_that_rate.aggregate(Sum("rating"))["rating__sum"]

            self.host.host_rating = (other_rating + self.rating) / (
                service_that_rate.count() + 1
            )
            self.save()
            self.host.save()
            return True
        return False

    def __str__(self):
        return (
            f"Service by {self.host}\n"
            + f"Customer : {self.customer}\n"
            + f"Dog : {self.dog}\n"
            + f"Status : {self.service_status}\n"
            + f"Main status : {self.main_status}\n"
            + f"Additional service : {self.additional_service}"
        )
