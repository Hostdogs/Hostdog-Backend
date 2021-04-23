from django.test import TestCase,Client
from django.contrib.auth.models import (
    AbstractUser,
)
from accounts.models import Host,Customer,Dog,Accounts
from service.models import Service,Meal
from rest_framework.test import APIClient, APITestCase

#py manage.py makemigrations
#py manage.py migrate
#coverage run --omit="*/hostdog/*" manage.py test
#coverage html
class API_Testing(APITestCase):
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
            * host ปรับ enable/disable additional service ได้
            * host ปรับราคา additional service ได้
            * host เพิ่ม/ลบ อาหารจาก Meal ได้
    """
    @classmethod
    def setUpTestData(self):
        """
        #Model testing
        acc_005 = Accounts.objects.create(
            is_superuser=False,
            password='123123123',
            last_login='2021-04-13 14:37:50.965870+00:00',
            username='test_User002',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-13 14:37:50.965870+00:00',
            is_host=False
        )
        host_002 = Host.objects.create(
            first_name='first',
            last_name='last',
            account_id=acc_005.id,
            gender='Female',
            host_bio='host_bio',
            host_rating=4.5,
            host_hosted_count=10,
            host_max=3,
            host_avaliable=1,
            host_area=100,
            address='address',
            mobile='0812345678',
            dob='2021-04-13',
            latitude=10,
            longitude=10
        )
        """
        meal_001 = Meal.objects.create(
            meal_type='meal_type',
            meal_price=24.132
            #host_id=host_002.account_id
            
        )

        #create account for API testing
        acc_api_001 = Accounts.objects.create_user(
            username="Account_001",
            email="acc_001@api.com",
            password="123",
            is_host=False
        )
        acc_api_002 = Accounts.objects.create_user(
            username="Account_002",
            email="acc_002@api.com",
            password="123",
            is_host=True
        )


    def test_meal(self):
        meal = Meal.objects.get(id = 1)

        #host_id = meal.host_id
        meal_type = f'{meal.meal_type}'
        meal_price = meal.meal_price

        word = str(meal)
        self.assertEqual(word,str(meal))
        self.assertEqual(meal_type,'meal_type')
        self.assertEqual(meal_price,24.132)

