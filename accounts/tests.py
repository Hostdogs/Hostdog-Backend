from django.test import TestCase,Client
from django.urls import reverse

from accounts.models import Accounts , Customer , Host , Dog , NearestHost , HostAvailableDate
from accounts.views import AccountsViewSet,AuthToken
from rest_framework.test import APITestCase,APIClient

from django.utils import timezone
import pytz
import datetime
#py manage.py makemigrations
#py manage.py migrate
#coverage run --omit="*/hostdog/*" manage.py test
#coverage html
class TestModel(TestCase):
    """
    TODO:
        - AccountViewSet
            * User create account ใส่ข้อมูลถูกต้อง (SUCCESS)
            * User create account (FAIL)
                @ ใส่ username ซ้ำ
                @ role ซ้ำกับ email เดิม
                @ ใช้ email เกิน 2 ครั้ง
            * เปลี่ยนรหัสผ่าน account (SUCCESS)
        - AuthToken
            * login ด้วย account ที่สร้างมา (SUCCESS)
        - CustomerProfileViewSet
            * เข้าถึง Customer profile หลังจาก create account (SUCCESS)
            * แก้ไข
        - HostProfileViewSet
            * เข้าถึง Host profile หลังจาก create account (SUCCESS)
            * แก้ไข
        - DogViewSet
            * เข้าถึง dog profile ผ่าน customer profile (SUCCESS)
            * สร้างหมาผ่าน customer profile (SUCCESS)
            * แก้ไขข้อมูลหมาผ่าน customer profile (SUCCESS)
            * ลบหมาผ่าน customer profile (SUCCESS)
        - HostAvailableDateViewSet
            * host กำหนดวันผ่าน host profile (SUCCESS)
            * กำหนดวันซ้ำ, วันในอดีต (FAIL)
    """
    @classmethod
    def setUpTestData(cls):
        
        acc_001 = Accounts.objects.create(
            is_superuser=False,
            password='123123123',
            last_login='2021-04-13 14:37:50.965870+00:00',
            username='test_User001',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-13 14:37:50.965870+00:00',
            is_host=True
        )
        acc_002 = Accounts(
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
        acc_003 = Accounts(
            is_superuser=False,
            password='123123123',
            last_login='2021-04-13 14:37:50.965870+00:00',
            username='test_User003',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-13 14:37:50.965870+00:00',
            is_host=True
        )
        acc_002.save()
        acc_003.save()
        acc_004 = Accounts.objects.create(
            is_superuser=False,
            password='123123123',
            last_login='2021-04-13 14:37:50.965870+00:00',
            username='test_User004',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-13 14:37:50.965870+00:00',
            is_host=True
        )
        cus_001 = Customer.objects.create(
            first_name='first',
            last_name='last',
            account_id=acc_001.id,
            gender='Male',
            address='address',
            mobile='0812345678',
            dob='2021-04-13',
            customer_bio='customer_bio',
            customer_dog_count=3,
            customer_hosted_count=4
        )
        cus_001.path_and_rename('filename')

        host_001 = Host.objects.create(
            first_name='first',
            last_name='last',
            account_id=acc_002.id,
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
        host_001.path_and_rename('filename')
        
        dog_001 = Dog.objects.create(
            gender='Male',
            customer_id=cus_001.account_id,
            dog_name='dog_name',
            dog_bio='dog_bio',
            dog_status='dog_status',
            dog_create_date='2021-04-13',
            dog_dob='2021-04-13',
            dog_breed='dog_breed',
            dog_weight=251.32
        )
        dog_001.path_and_rename('filename')

        avaDate_001 = HostAvailableDate.objects.create(
            date='2021-04-20',
            host_id=host_001.account_id
        )
        
        #near = NearestHost()
        #near.nearest_host_within_x_km(10,10,2)
        

    def test_account(self):
        acc = Accounts.objects.get(id = 1)
        
        is_superuser = acc.is_superuser
        password = f'{acc.password}'
        last_login = f'{acc.last_login}'
        username = acc.username
        email = f'{acc.email}'
        is_active = acc.is_active
        is_staff = acc.is_staff
        date_joined = f'{acc.date_joined}'
        is_host = acc.is_host
        
        word = str(acc)
        self.assertEqual(word,username)
        self.assertFalse(is_superuser)
        self.assertEqual(password,'123123123')
        self.assertEqual(last_login,'2021-04-13 14:37:50.965870+00:00')
        self.assertEqual(username,'test_User001')
        self.assertEqual(email,'account@email.com')
        self.assertTrue(is_active)
        self.assertFalse(is_staff)
        self.assertEqual(date_joined,'2021-04-13 14:37:50.965870+00:00')
        self.assertTrue(is_host)

    def test_customer(self):
        cus = Customer.objects.get(account_id = 1)

        first_name = f'{cus.first_name}'
        last_name = f'{cus.last_name}'
        account_id = cus.account_id
        gender = f'{cus.gender}'
        address = f'{cus.address}'
        mobile = f'{cus.mobile}'
        dob = f'{cus.dob}'
        customer_bio = f'{cus.customer_bio}'
        customer_dog_count = cus.customer_dog_count
        customer_hosted_count = cus.customer_hosted_count

        word = str(cus)
        self.assertEqual(word,str(cus))
        self.assertEqual(first_name,'first')
        self.assertEqual(last_name,'last')
        self.assertEqual(account_id,1)
        self.assertEqual(gender,'Male')
        self.assertEqual(address,'address')
        self.assertEqual(mobile,'0812345678')
        self.assertEqual(dob,'2021-04-13')
        self.assertEqual(customer_bio,'customer_bio')
        self.assertEqual(customer_dog_count,3)
        self.assertEqual(customer_hosted_count,4)

    def test_host(self):
        host = Host.objects.get(account_id=2)

        first_name = f'{host.first_name}'
        last_name = f'{host.last_name}'
        account_id = host.account_id
        gender = f'{host.gender}'
        host_bio = f'{host.host_bio}'
        host_rating = host.host_rating
        host_hosted_count = host.host_hosted_count
        host_max = host.host_max
        host_avaliable = host.host_avaliable
        host_area = host.host_area
        address = f'{host.address}'
        mobile = f'{host.mobile}'
        dob = f'{host.dob}'
        latitude = host.latitude
        longitude = host.longitude

        word = str(host)
        self.assertEqual(word,str(host))
        self.assertEqual(first_name,'first')
        self.assertEqual(last_name,'last')
        self.assertEqual(account_id,2)
        self.assertEqual(gender,'Female')
        self.assertEqual(host_bio,'host_bio')
        self.assertEqual(host_rating,4.5)
        self.assertEqual(host_hosted_count,10)
        self.assertEqual(host_max,3)
        self.assertEqual(host_avaliable,1)
        self.assertEqual(host_area,100)
        self.assertEqual(address,'address')
        self.assertEqual(mobile,'0812345678')
        self.assertEqual(dob,'2021-04-13')
        self.assertEqual(latitude,10)
        self.assertEqual(longitude,10)
    
    def test_dog(self):
        dog = Dog.objects.get(customer_id = 1)

        gender = f'{dog.gender}'
        customer_id = dog.customer_id
        dog_name = f'{dog.dog_name}'
        dog_bio = f'{dog.dog_bio}'
        dog_status = f'{dog.dog_status}'
        dog_create_date = f'{dog.dog_create_date}'
        dog_dob = f'{dog.dog_dob}'
        dog_breed = f'{dog.dog_breed}'
        dog_weight = dog.dog_weight

        word = str(dog)
        self.assertEqual(word,str(dog))
        self.assertEqual(gender,'Male')
        self.assertEqual(customer_id,1)
        self.assertEqual(dog_name,'dog_name')
        self.assertEqual(dog_bio,'dog_bio')
        self.assertEqual(dog_status,'dog_status')
        #self.assertEqual(dog_create_date,'2021-04-13')
        self.assertEqual(dog_dob,'2021-04-13')
        self.assertEqual(dog_breed,'dog_breed')
        self.assertEqual(dog_weight,251.32)

    def test_host_available_date(self):
        ava = HostAvailableDate.objects.get(host_id = 2)

        word = str(ava)
        self.assertEqual(word,str(ava))


'''
class TestView(APITestCase):

    @classmethod
    def setUp(self):
        

    def test_view_GET(self):
'''        


        