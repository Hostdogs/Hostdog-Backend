from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractUser,
)
from accounts.serializers import (
    AccountSerializer,
    CustomerProfileSerializer,
    DogProfileWithNestedSerializer,
    HostAvailableDateSerializer,
    HostAvailableDateWithNestedSerializer,
    HostProfileSerializer,
    DogProfileSerializer,
    ChangePasswordSerializer,
)
from accounts.models import Accounts , Customer , Host , Dog , NearestHost , HostAvailableDate
from accounts.views import AccountsViewSet,AuthToken
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
import pytz
import datetime
#py manage.py makemigrations
#py manage.py migrate
#coverage run --omit="*/hostdog/*" manage.py test
#coverage html
'''
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
        
        #near_001 = NearestHost()
        #near_001.nearest_host_within_x_km(5,5,2)

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
        ava = HostAvailableDate.objects.get(host = self.host_001)

        word = str(ava)
        self.assertEqual(word,str(ava))
'''

class TestAPI(APITestCase):

    @classmethod
    def setUp(self):
        self.client = APIClient()
        self.acc_001 = Accounts.objects.create(
            is_host = True,
            username = 'host001',
            #password = 'password',
            email = 'host001@email.com'
        )
        self.acc_001.set_password('password')
        self.acc_001.save()
        t_acc001=Token.objects.create(user=self.acc_001)
        self.acc_002 = Accounts.objects.create(
            is_host = False,
            username = 'cus001',
            #password = 'password',
            email = 'cus001@email.com'
        )
        self.acc_002.set_password('password')
        self.acc_002.save()
        self.host001 = Host.objects.get(account=self.acc_001)
        self.cus001 = Customer.objects.get(account=self.acc_002)
        self.dog_001 = Dog.objects.create(
            customer=self.cus001,
            dog_name='dog_name',
            dog_breed='dog_breed',
            gender='Female'
        )
        self.client.force_authenticate(user=self.acc_001)
        self.client.force_authenticate(user=self.cus001)
    def test_acc_view_set(self):

        url = reverse('accounts:accounts-list')
        #create
        data1 = {
            'is_host' : True,
            'username' : 'username',
            'password' : 'password',
            'email' : 'account001@email.com'
        }
        response1 = self.client.post(url,data1,format = 'json')#201
        #same username
        data2 = {
            'is_host' : True,
            'username' : 'username',
            'password' : 'password',
            'email' : 'account002@email.com'
        }
        response2 = self.client.post(url,data2,format = 'json')#400
        #same email
        data3 = {
            'is_host' : True,
            'username' : 'username2',
            'password' : 'password',
            'email' : 'account002@email.com'
        }
        response3 = self.client.post(url,data3,format = 'json')#201
        data4 = {
            'is_host' : True,
            'username' : 'username3',
            'password' : 'password',
            'email' : 'account002@email.com'
        }
        response4 = self.client.post(url,data4,format = 'json')#400
        data5 = {
            'is_host' : False,
            'username' : 'username3',
            'password' : 'password',
            'email' : 'account002@email.com'
        }
        response5 = self.client.post(url,data5,format = 'json')#201
        data6 = {
            'is_host' : False,
            'username' : 'username4',
            'password' : 'password',
            'email' : 'account002@email.com'
        }
        response6 = self.client.post(url,data6,format = 'json')#400

        self.assertEqual(response1.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response4.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response5.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response6.status_code,status.HTTP_400_BAD_REQUEST) 

    def test_change_pass(self):
        token = Token.objects.get(user=self.acc_001)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = reverse('accounts:accounts-change_password',kwargs={'pk':self.acc_001.id})   
        data1={    
            'old_password':'password',
            'new_password':'new_password'
        }
        response1 = self.client.post(url,data1,format = 'json')
        data2={
            'old_password':'wrong_password',
            'new_password':'new_password'
        }
        response2 = self.client.post(url,data2,format = 'json')
        self.assertEqual(response1.status_code,status.HTTP_200_OK) 
        self.assertEqual(response2.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_cus_profile(self):

        url = reverse('accounts:customer-list',kwargs={'pk':self.acc_002.id})
        data1{
            'first_name':'first_name',
            'last_name':'last_name'
        }
