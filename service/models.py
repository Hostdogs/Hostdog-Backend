from django.db import models
from accounts.models import Host, Customer, Dog, HostAvailableDate
from django.db.models import Sum
from notifications.tasks import send_email_customer_host_response_task


class Meal(models.Model):
    """
    Meal model
        - food for dog to eat
        - can add later in production
        - can adjust the price in production
    """

    meal_type = models.CharField(max_length=50)
    meal_price = models.FloatField()
   

    def __str__(self):
        return f"Meals : {self.meal_type}\nPrice : {self.meal_price} Baht"


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

    enable_dog_walk = models.BooleanField(default=True)
    enable_get_dog = models.BooleanField(default=True)
    enable_delivery_dog = models.BooleanField(default=True)
    enable_bath_dog = models.BooleanField(default=True)
    
    available_meals = models.ManyToManyField(
        Meal, related_name="available_meals"
    )
    deposit_price = models.IntegerField(default=300)

    def __str__(self):
        return (
            f" Additional service of {self.host}\n"
            + "1.) Walk the dog : {self.price_dog_walk} {'ENABLE' if self.enable_dog_walk else 'DISABLE'}\n"
            + "2.) Get the dog : {self.price_get_dog} {'ENABLE' if self.enable_get_dog else 'DISABLE'}\n"
            + "3.) Deliver the dog : {self.price_deliver_dog} {'ENABLE' if self.enable_delivery_dog else 'DISABLE'}\n"
            + "4.) Bath the dog : {self.price_bath_dog} {'ENABLE' if self.enable_bath_dog else 'DISABLE'}"
        )


class Service(models.Model):
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
    service_is_over_night = models.BooleanField(default=False)
    service_create_time = models.DateTimeField(auto_now_add=True)
    service_start_time = models.DateTimeField()
    service_end_time = models.DateTimeField()
    service_send_time = models.DateTimeField(blank=True, null=True)
    service_get_time = models.DateTimeField(blank=True, null=True)
    service_meal_type = models.ForeignKey(
        Meal, on_delete=models.CASCADE, related_name="service_service_meal_type"
    )
    service_meal_per_day = models.IntegerField()
    service_meal_weight = models.IntegerField()
    is_dog_walk = models.BooleanField(default=False)
    is_get_dog = models.BooleanField(default=False)
    is_delivery_dog = models.BooleanField(default=False)
    is_bath_dog = models.BooleanField(default=False)
    additional_service = models.OneToOneField(
        HostService, on_delete=models.CASCADE, related_name="additional_service"
    )
    service_bio = models.TextField(max_length=255, default="")
    created_deposit_payment = models.BooleanField(default=False)
    created_late_payment = models.BooleanField(default=False)
    days_late = models.IntegerField(default=0)
    is_review = models.BooleanField(default=False)
    is_customer_receive_dog = models.BooleanField(default=False)
    main_status = models.CharField(
        max_length=20, choices=MAIN_STATUS, default="pending"
    )

    def accept(self, is_host):
        """
        If host accept the service
        TODO:
            - service main_status change to wait_for_progress [x]
            - delete range of date that cutomer register from host's available date [x]
            - create post_save signal to notification application [x]
            - if catch signal from payment
                - change main_status to in_progress
                - change status to time of service
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
                True
            )
            self.main_status = "wait_for_progress"
            date_range = (
                self.service_start_time.date(),
                self.service_end_time.date(),
            )
            HostAvailableDate.objects.filter(
                host=self.host, date__range=date_range
            ).delete()
            self.save()
            return True
        return False

    def decline(self, is_host):
        """
        If host decline the service
            - service main_status change to cancelled
            TODO:
            - create post_save signal to notification
        """
        if self.main_status == "pending":
            email = self.customer.account.email
            send_email_customer_host_response_task(
                email,
                self.customer.first_name,
                self.customer.last_name,
                self.host.first_name,
                self.host.last_name,
                False
            )
            self.main_status = "cancelled"
            self.save()
            return True
        return False

    def host_receive_dog(self):
        """
        Host สามารถรับหมาได้
        """
        # TODO รับหมาได้เมื่อ Customer จ่าย Payment แล้ว
        self.service_status = "caring_for_your_dog"
        self.save()

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
        # TODO คืนหมาไม่ได้ถ้า Customer ยังไม่จ่ายค่าเลท
        if self.main_status == "in_progress" and self.is_customer_receive_dog:
            self.service_status = "service_success"
            self.main_status = "end"
            self.save()
            return True
        return False


    def cancel(self):
        """
        Customer สามารถยกเลิกบริการได้
        """
        #TODO ส่ง Email Notification ให้ Host
        if self.main_status != "late":
            self.main_status = "cancelled"
            self.service_status = "you_cancel_this_service"
            self.save()
            return True
        return False

    def review(self, review_score):
        """
        Customer สามารถรีวิวบริการได้
        """
        # TODO แจ้งเตือน Host ถึงคะแนน Review
        if self.main_status == "end":
            self.is_review = True
            self.rating += review_score
            service_that_rate = Service.objects.filter(host=self.host, is_review=True)
            self.host.host_rating += (
                service_that_rate.aggregate(Sum("host_rating"))["host_rating__sum"]
                / service_that_rate.count()
            )
            self.save()
            self.host.save()
            return True
        return False

    def __str__(self):
        return (
            f"Service by {self.host}\n"
            + "Customer : {self.customer}\n"
            + "Dog : {self.dog}\n"
            + "Status : {self.service_status}\n"
            + "Main status : {self.main_status}"
        )
