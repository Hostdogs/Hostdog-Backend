from django.http import response
from django.test import TestCase
from django.urls import reverse
from accounts.models import Customer, Dog, DogFeedingTime, Host, Accounts, HostAvailableDate
from service.models import HostService, Services, Meal
from rest_framework.test import APIClient, APITestCase
from datetime import date
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils.timezone import datetime, localtime, timedelta

# py manage.py makemigrations
# py manage.py migrate
# coverage run --omit="*/hostdog/*" manage.py test
# coverage html

"""
    TODO:
        - Model testing
            * Test about create the object model (SUCCESS)
        - Host create available date (>= 3 Testcase)
            * register date in the past (FAIL) [x]
            * register date greater than or equal to today (SUCCESS) [x]
            * register date that in service (FAIL) [x]
        - ServiceViewSet
            - Customer register the host service 
                * register to the correct host available date (SUCCESS) [x]
                * register to the wrong host available date (FAIL) [x]
                * register to the date in the past (FAIL) [x]
                * register with meal that host doensn't have (FAIL) [x]
                * attribute in service object must correct (SUCCESS)
                * customer choose wrong additional service (FAIL)
                    @ Host เลือกไม่เปิด Field ตามนี้ แต่ customer กลับเลือกใช้บริการ
                    @ is_dog_walk
                    @ is_get_dog
                    @ is_delivery_dog
                    @ is_bath_dog
                * customer choose correct additional service (SUCCESS)
                    @ ตรงข้ามกับข้อก่อนหน้า
                * customer select the correct meal (SUCCESS)
                * customer select the wrong meal (FAIL)
                * after finish registration main_status is pending (SUCCESS)
            - Host response to the customer request
                * Host accept the customer request then main_status change to payment (SUCCESS)
                * Host decline the customer request then main_status change to cancelled (SUCCESS)
                * Host accept request ครั้งที่ 2 (FAIL) **ควรจะได้ครั้งเดียว
                * Host decline request ครั้งที่ 2 (FAIL) **ควรจะได้ครั้งเดียว
        - MealViewSet
            * สร้างมื้ออาหารได้ (SUCCESS)
            * ปรับราคาได้ (SUCCESS)
        - HostServiceViewSet
            * host ปรับ enable/disable additional service ได้ (SUCCESS) [x]
            * host ปรับราคา additional service ได้ (SUCCESS) [x]
            * host เพิ่ม/ลบ อาหารจาก Meal ได้ (SUCCESS) [x]
"""


class Model_Testing(TestCase):
    @classmethod
    def setUpTestData(self):
        # Model testing
        self.acc_005 = Accounts.objects.create(
            is_superuser=False,
            password="123123123",
            last_login="2021-04-13 14:37:50.965870+00:00",
            username="test_User002",
            email="account@email.com",
            is_active=True,
            is_staff=False,
            date_joined="2021-04-13 14:37:50.965870+00:00",
            is_host=False,
        )
        self.host_002 = Host.objects.create(
            first_name="first",
            last_name="last",
            account=self.acc_005,
            gender="Female",
            host_bio="host_bio",
            host_rating=4.5,
            host_hosted_count=10,
            host_area=100,
            address="address",
            mobile="0812345678",
            dob="2021-04-13",
            latitude=10,
            longitude=10,
        )

        self.meal_001 = Meal.objects.create(
            meal_type="meal_type", meal_price_per_gram=24.132
        )

    def test_meal(self):
        meal = Meal.objects.get(id=self.meal_001.id)
        meal_type = f"{meal.meal_type}"
        meal_price_per_gram = meal.meal_price_per_gram

        word = str(meal)
        self.assertEqual(word, str(meal))
        self.assertEqual(meal_type, "meal_type")
        self.assertEqual(meal_price_per_gram, 24.132)


class API_Testing(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.acc_host_001 = Accounts.objects.create_user(
            username="host001", email="host001@api.com", is_host=True
        )
        self.acc_host_001.set_password("123")
        self.acc_host_001.save()
        self.token_acc_host_001 = Token.objects.create(user=self.acc_host_001)
        self.acc_cus_001 = Accounts.objects.create_user(
            username="customer001", email="cus001@api.com", is_host=False
        )
        self.acc_cus_001.set_password("123")
        self.acc_cus_001.save()
        self.token_acc_cus_001 = Token.objects.create(user=self.acc_cus_001)
        self.host = Host.objects.get(account=self.acc_host_001)
        self.customer = Customer.objects.get(account=self.acc_cus_001)
        self.additional_service = HostService.objects.get(host=self.host)
        for day in range(2):
            self.host_001_available_date = HostAvailableDate.objects.create(
                host=self.host, date=date.today() + timedelta(days=day)
            )
        self.dog_001 = Dog.objects.create(
            customer=self.customer,
            dog_name="Doggy",
            dog_breed="USA",
            gender="male",
        )
        self.meal_001 = Meal.objects.create(
            meal_type="Chicken", meal_price_per_gram=150
        )
        self.service = Services.objects.create(
            customer=self.customer,
            host=self.host,
            dog=self.dog_001,
            service_start_time=localtime(),
            service_end_time=localtime() + timedelta(days=1),
            service_meal_type=self.meal_001,
            service_meal_weight=15,
            is_dog_walk=True,
            is_get_dog=True,
            is_delivery_dog=True,
            is_bath_dog=True,
            additional_service=self.additional_service,
            service_bio="My first service",
        )
        return super().setUp()

    def test_create_available_date(self):
        """
        1.) register date in the past (FAIL)
        2.) register date greater than or equal to today (SUCCESS)
        3.) register date that in service (FAIL)
        """
        # Reverse view -> url
        # App : accounts
        # url_name :
        self.client.force_authenticate(
            user=self.acc_host_001, token=self.token_acc_host_001
        )
        url = reverse(
            "accounts:profilehost-availabledate-list",
            kwargs={"host_pk": self.acc_host_001.id},
        )
        # url = api/profilehost/idของhostคนนี้/available-date/
        # 1
        yesterday = date.today() - timedelta(days=1)
        data1 = {"date": yesterday}
        response1 = self.client.post(url, data1, format="json")
        # 2
        future_day = date(2060, 5, 1) + timedelta(days=1)
        data2 = {"date": future_day}
        response2 = self.client.post(url, data2, format="json")
        # 3
        data3 = {"date": self.service.service_end_time.date()}
        response3 = self.client.post(url, data3, format="json")

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)


class ServiceViewSetTesting(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.acc_cus_001 = Accounts.objects.create_user(
            username="customer001", email="cus001@api.com", is_host=False
        )
        self.acc_cus_001.set_password("123")
        self.acc_cus_001.save()
        self.token_acc_cus_001 = Token.objects.create(user=self.acc_cus_001)

        self.acc_host_001 = Accounts.objects.create_user(
            username="host001", email="host001@api.com", is_host=True
        )
        self.acc_host_001.set_password("123")
        self.acc_host_001.save()
        self.token_acc_host_001 = Token.objects.create(user=self.acc_host_001)

        self.host = Host.objects.get(account=self.acc_host_001)
        self.customer = Customer.objects.get(account=self.acc_cus_001)
        self.additional_service = HostService.objects.get(host=self.host)
        self.additional_service.enable_dog_walk = True
        self.additional_service.enable_bath_dog = True
        self.additional_service.save()

        self.dog_001 = Dog.objects.create(
            customer=self.customer,
            dog_name="Doggy",
            dog_breed="USA",
            gender="male",
        )
        feeding_times = ["06:00", "18:00"]
        for feeding_time in feeding_times:
            DogFeedingTime.objects.create(dog=self.dog_001, time=feeding_time)

        self.meal_001 = Meal.objects.create(meal_type="Chicken", meal_price_per_gram=50)
        self.meal_002 = Meal.objects.create(meal_type="Pizza", meal_price_per_gram=30)

        self.additional_service.available_meals.add(self.meal_001)

        for day in range(2):
            self.host_001_available_date = HostAvailableDate.objects.create(
                host=self.host, date=date.today() + timedelta(days=day)
            )

        return super().setUp()

    def test_register_host_service(self):
        """
        1.) register to the correct host available date (SUCCESS)
        2.) register to the wrong host available date (FAIL)
        3.) register to the date in the past (FAIL)
        4.) get service that register (SUCCESS)
        """
        self.client.force_authenticate(
            user=self.acc_cus_001, token=self.token_acc_cus_001
        )
        url = reverse("service:services-list")
        # 1
        service_data = {
            "host": self.host.account.id,
            "dog": self.dog_001.id,
            "service_is_over_night": True,
            "service_start_time": localtime() + timedelta(hours=3),
            "service_end_time": localtime() + timedelta(days=1),
            "service_meal_type": self.meal_001.id,
            "service_meal_weight": 50,
            "is_dog_walk": True,
            "is_get_dog": False,
            "is_delivery_dog": False,
            "is_bath_dog": True,
            "service_bio": "My first service yayyy",
        }
        service_response = self.client.post(url, service_data, format="json")
        # 2
        service_data_2 = {
            "host": self.host.account.id,
            "dog": self.dog_001.id,
            "service_is_over_night": True,
            "service_start_time": localtime() + timedelta(hours=3),
            "service_end_time": localtime() + timedelta(days=2),
            "service_meal_type": self.meal_001.id,
            "service_meal_weight": 50,
            "is_dog_walk": True,
            "is_get_dog": False,
            "is_delivery_dog": False,
            "is_bath_dog": True,
            "service_bio": "My first service yayyy",
        }
        service_response_2 = self.client.post(url, service_data_2, format="json")
        # 3
        service_data_3 = {
            "host": self.host.account.id,
            "dog": self.dog_001.id,
            "service_is_over_night": True,
            "service_start_time": datetime(2021, 1, 2),
            "service_end_time": datetime(2021, 1, 3),
            "service_meal_type": self.meal_001.id,
            "service_meal_weight": 50,
            "is_dog_walk": True,
            "is_get_dog": False,
            "is_delivery_dog": False,
            "is_bath_dog": True,
            "service_bio": "My first service yayyy",
        }
        service_response_3 = self.client.post(url, service_data_3, format="json")
        # 4
        service_response_4 = self.client.get(url)
        self.assertEqual(service_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(service_response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(service_response_3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(service_response_4.status_code, status.HTTP_200_OK)

    def test_select_meal(self):
        """
        1.) register with meal that host doensn't have (FAIL)
        2.) register with meal that host have (SUCCESS)
        """
        self.client.force_authenticate(
            user=self.acc_cus_001, token=self.token_acc_cus_001
        )
        url = reverse("service:services-list")
        service_data_1 = {
            "host": self.host.account.id,
            "dog": self.dog_001.id,
            "service_is_over_night": True,
            "service_start_time": localtime() + timedelta(hours=3),
            "service_end_time": localtime() + timedelta(days=1),
            "service_meal_type": self.meal_002.id,
            "service_meal_weight": 50,
            "is_dog_walk": True,
            "is_get_dog": False,
            "is_delivery_dog": False,
            "is_bath_dog": True,
            "service_bio": "My first service yayyy",
        }
        service_response_1 = self.client.post(url, service_data_1, format="json")

        service_data_2 = {
            "host": self.host.account.id,
            "dog": self.dog_001.id,
            "service_is_over_night": True,
            "service_start_time": localtime() + timedelta(hours=3),
            "service_end_time": localtime() + timedelta(days=1),
            "service_meal_type": self.meal_001.id,
            "service_meal_weight": 50,
            "is_dog_walk": True,
            "is_get_dog": False,
            "is_delivery_dog": False,
            "is_bath_dog": True,
            "service_bio": "My first service yayyy",
        }
        service_response_2 = self.client.post(url, service_data_2, format="json")

        self.assertEqual(service_response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(service_response_2.status_code, status.HTTP_201_CREATED)

    def test_customer_choose_wrong_additional_service(self):
        """
        * customer choose wrong additional service (FAIL)
            @ Host เลือกไม่เปิด Field ตามนี้ แต่ customer กลับเลือกใช้บริการ
            @ is_dog_walk
            @ is_get_dog
            @ is_delivery_dog
            @ is_bath_dog
        """
        self.client.force_authenticate(
            user=self.acc_cus_001, token=self.token_acc_cus_001
        )
        url = reverse("service:services-list")
        service_data = {
            "host": self.host.account.id,
            "dog": self.dog_001.id,
            "service_is_over_night": True,
            "service_start_time": localtime() + timedelta(hours=3),
            "service_end_time": localtime() + timedelta(days=1),
            "service_meal_type": self.meal_001.id,
            "service_meal_weight": 50,
            "is_dog_walk": True,
            "is_get_dog": True,
            "is_delivery_dog": True,
            "is_bath_dog": True,
            "service_bio": "My first service yayyy",
        }
        service_response = self.client.post(url, service_data, format="json")
        self.assertEqual(service_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_hostservice(self):
        """
        1.) host ปรับ enable/disable additional service ได้ (SUCCESS)
        2.) host ปรับราคา additional service ได้ (SUCCESS)
        """
        self.client.force_authenticate(
            user=self.acc_host_001, token=self.token_acc_host_001
        )
        url = reverse(
            "accounts:profilehost-host-service-detail",
            kwargs={"host_pk": self.acc_host_001.id, "pk": self.acc_host_001.id},
        )
        update_data = {
            "enable_dog_walk": False,
            "enable_delivery_dog": True,
            "price_dog_walk": 50,
            "price_bath_dog": 100,
        }
        response_1 = self.client.patch(url, update_data, format="json")
        response_2 = self.client.get(url)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)

    def test_host_add_del_meal(self):
        """
        1.) host เพิ่ม/ลบ อาหารจาก Meal ได้ (SUCCESS)
        2.) host เพิ่ม อาหารที่ผิด (FAIL)
        """
        self.client.force_authenticate(
            user=self.acc_host_001, token=self.token_acc_host_001
        )
        url_1 = reverse(
            "accounts:host-service-meals-list",
            kwargs={
                "host_pk": self.acc_host_001.id,
                "host_service_pk": self.acc_host_001.id,
            },
        )
        select_meal_data_1 = {"meal": self.meal_001.id}
        response_1 = self.client.post(url_1, select_meal_data_1, format="json")
        select_meal_data_2 = {"meal": 9999999999}
        response_2 = self.client.post(url_1, select_meal_data_2, format="json")
        print(response_2.data)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

        url_2 = reverse(
            "accounts:host-service-meals-detail",
            kwargs={
                "host_pk": self.acc_host_001.id,
                "host_service_pk": self.acc_host_001.id,
                "pk": self.meal_001.id
            },
        )
        response_3 = self.client.delete(url_2)
        self.assertEqual(response_3.status_code, status.HTTP_204_NO_CONTENT)
