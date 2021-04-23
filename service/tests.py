from django.test import TestCase
from django.urls import reverse
from accounts.models import Customer, Dog, Host, Accounts
from service.models import HostService, Service, Meal
from rest_framework.test import APIClient, APITestCase
from datetime import date, datetime, timedelta
from rest_framework import status

# py manage.py makemigrations
# py manage.py migrate
# coverage run --omit="*/hostdog/*" manage.py test
# coverage html

"""
    TODO:
        - Model testing
            * Test about create the object model (SUCCESS)
        - Host create available date (>= 3 Testcase)
            * register date in the past (FAIL)
            * register date greater than or equal to today (SUCCESS)
            * register date that in service (FAIL)
        - ServiceViewSet
            - Customer register the host service 
                * register to the correct host available date (SUCCESS)
                * register to the wrong host available date (FAIL)
                * register to the date in the past (FAIL)
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
            * host ปรับ enable/disable additional service ได้ (SUCCESS)
            * host ปรับราคา additional service ได้ (SUCCESS)
            * host เพิ่ม/ลบ อาหารจาก Meal ได้ (SUCCESS)
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
            host_max=3,
            host_avaliable=1,
            host_area=100,
            address="address",
            mobile="0812345678",
            dob="2021-04-13",
            latitude=10,
            longitude=10,
        )

        self.meal_001 = Meal.objects.create(
            meal_type="meal_type", meal_price=24.132
        )

    def test_meal(self):
        meal = Meal.objects.get(id=self.meal_001.id)
        meal_type = f"{meal.meal_type}"
        meal_price = meal.meal_price

        word = str(meal)
        self.assertEqual(word, str(meal))
        self.assertEqual(meal_type, "meal_type")
        self.assertEqual(meal_price, 24.132)


class API_Testing(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.acc_host_001 = Accounts.objects.create_user(
            username="host001",
            email="host001@api.com",
            password="123",
            is_host=True
        )
        self.acc_cus_001 = Accounts.objects.create_user(
            username="customer001",
            email="cus001@api.com",
            password="123",
            is_host=False
        )
        self.host = Host.objects.get(account=self.acc_host_001)
        self.customer = Customer.objects.get(account=self.acc_cus_001)
        self.additional_service = HostService.objects.get(host=self.host)
        self.dog_001 = Dog.objects.create(
            customer = self.customer,
            dog_name = "Doggy",
            dog_breed = "USA",
            gender="male",
        )
        self.meal_001 = Meal.objects.create(
            meal_type = "Chicken",
            meal_price = 150
        )
        self.service = Service.objects.create(
            customer = self.customer,
            host = self.host,
            dog = self.dog_001,
            service_start_time = date.today(),
            service_end_time = date.today() + timedelta(days=1),
            service_meal_type = self.meal_001,
            service_meal_per_day = 2,
            service_meal_weight = 15,
            is_dog_walk = True,
            is_get_dog = True,
            is_delivery_dog = True,
            is_bath_dog = True,
            additional_service = self.additional_service,
            service_bio = "My first service"
        )
        self.client.force_authenticate(user=self.acc_host_001)
        return super().setUp()
    
    def test_create_available_date(self):
        """
        1.) register date in the past (FAIL)
        2.) register date greater than or equal to today (SUCCESS)
        3.) register date that in service (FAIL)
        """
        # Reverse view -> url
        #App : accounts
        #url_name : 
        
        url = reverse("accounts:profilehost-availabledate-list", kwargs={"parent_lookup_host": self.acc_host_001.id})
        # url = api/profilehost/idของhostคนนี้/available-date/
        # 1
        yesterday = date.today() - timedelta(days=1)
        data1 = {"date": yesterday}
        response1 = self.client.post(url, data1, format="json")
        # 2
        next_day = date.today() + timedelta(days=1)
        data2 = {"date": next_day}
        response2 = self.client.post(url, data2, format="json")
        # 3
        data3 = {"date": self.service.service_end_time}
        response3 = self.client.post(url, data3, format="json")

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
