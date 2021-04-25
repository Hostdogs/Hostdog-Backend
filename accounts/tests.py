from django.test import TestCase
from django.urls import reverse
from accounts.models import Accounts , Customer , Host , Dog, HostAvailableDate
from accounts.views import AccountsViewSet,AuthToken
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
import pytz
from datetime import date, datetime, timedelta
#py manage.py makemigrations
#py manage.py migrate
#coverage run --omit="*/hostdog/*" manage.py test
#coverage html

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

class TestModel(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.acc_host_001 = Accounts.objects.create(
            is_superuser=False,
            last_login='2021-04-13 14:37:50.965870+00:00',
            username='test_User001',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-13 14:37:50.965870+00:00',
            is_host=True
        )
        cls.acc_host_001.set_password("123123123")
        cls.acc_host_001.save()

        cls.acc_cus_001 = Accounts(
            is_superuser=False,
            last_login='2021-04-13 14:37:50.965870+00:00',
            username='test_User002',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-13 14:37:50.965870+00:00',
            is_host=False
        )
        cls.acc_cus_001.set_password('123123123')
        cls.acc_cus_001.save()
        
        cls.acc_host_002 = Accounts(
            is_superuser=False,
            last_login='2021-04-13 14:37:50.965870+00:00',
            username='test_User003',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-13 14:37:50.965870+00:00',
            is_host=True
        )
        cls.acc_host_002.set_password('123123123')
        cls.acc_host_002.save()

        cls.acc_host_003 = Accounts.objects.create(
            is_superuser=False,
            last_login='2021-04-13 14:37:50.965870+00:00',
            username='test_User004',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-13 14:37:50.965870+00:00',
            is_host=True
        )
        cls.acc_host_003.set_password('123123123')
        cls.acc_host_003.save()
        
        cls.cus_001 = Customer.objects.get(account=cls.acc_cus_001)
        cls.cus_001.first_name = "first"
        cls.cus_001.last_name = "last"
        cls.cus_001.gender = "Male"
        cls.cus_001.address = "address"
        cls.cus_001.mobile = "0812345678"
        cls.cus_001.dob = "2021-04-13"
        cls.cus_001.customer_bio = "customer_bio"
        cls.cus_001.customer_dog_count = 3
        cls.cus_001.customer_hosted_count = 4

        cls.host_001 = Host.objects.get(account=cls.acc_host_001)
        cls.host_001.first_name = "first"
        cls.host_001.last_name = "last"
        cls.host_001.gender = "Female"
        cls.host_001.host_bio ="host_bio"
        cls.host_001.host_rating = 4.5
        cls.host_001.host_hosted_count = 10
        cls.host_001.host_max = 3
        cls.host_001.host_available = 1
        cls.host_001.host_area = 100
        cls.host_001.address = "address"
        cls.host_001.mobile = "0812345678"
        cls.host_001.dob = "2021-04-13"
        cls.host_001.latitude = 10
        cls.host_001.longitude = 10

        cls.dog_001 = Dog.objects.create(
            gender='Male',
            customer=cls.cus_001,
            dog_name='dog_name',
            dog_bio='dog_bio',
            dog_status='dog_status',
            dog_create_date='2021-04-13',
            dog_dob='2021-04-13',
            dog_breed='dog_breed',
            dog_weight=251.32
        )

        cls.ava_date_001 = HostAvailableDate.objects.create(
            date='2021-04-20',
            host=cls.host_001
        )

    def test_account(self):
        acc = self.acc_host_001
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
        self.assertNotEqual(password,'123123123')
        self.assertEqual(last_login,'2021-04-13 14:37:50.965870+00:00')
        self.assertEqual(username,'test_User001')
        self.assertEqual(email,'account@email.com')
        self.assertTrue(is_active)
        self.assertFalse(is_staff)
        self.assertEqual(date_joined,'2021-04-13 14:37:50.965870+00:00')
        self.assertTrue(is_host)

    def test_customer(self):
        cus = self.cus_001
        first_name = f'{cus.first_name}'
        last_name = f'{cus.last_name}'
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
        self.assertEqual(gender,'Male')
        self.assertEqual(address,'address')
        self.assertEqual(mobile,'0812345678')
        self.assertEqual(dob,'2021-04-13')
        self.assertEqual(customer_bio,'customer_bio')
        self.assertEqual(customer_dog_count,3)
        self.assertEqual(customer_hosted_count,4)

    def test_host(self):
        host = self.host_001
        first_name = f'{host.first_name}'
        last_name = f'{host.last_name}'
        gender = f'{host.gender}'
        host_bio = f'{host.host_bio}'
        host_rating = host.host_rating
        host_hosted_count = host.host_hosted_count
        host_max = host.host_max
        host_available = host.host_available
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
        self.assertEqual(gender,'Female')
        self.assertEqual(host_bio,'host_bio')
        self.assertEqual(host_rating,4.5)
        self.assertEqual(host_hosted_count,10)
        self.assertEqual(host_max,3)
        self.assertEqual(host_available,1)
        self.assertEqual(host_area,100)
        self.assertEqual(address,'address')
        self.assertEqual(mobile,'0812345678')
        self.assertEqual(dob,'2021-04-13')
        self.assertEqual(latitude,10)
        self.assertEqual(longitude,10)
    
    def test_dog(self):
        dog = self.dog_001
        gender = f'{dog.gender}'
        customer = self.cus_001
        dog_name = f'{dog.dog_name}'
        dog_bio = f'{dog.dog_bio}'
        dog_status = f'{dog.dog_status}'
        dog_dob = f'{dog.dog_dob}'
        dog_breed = f'{dog.dog_breed}'
        dog_weight = dog.dog_weight

        word = str(dog)
        self.assertEqual(word,str(dog))
        self.assertEqual(gender,'Male')
        self.assertEqual(customer,self.cus_001)
        self.assertEqual(dog_name,'dog_name')
        self.assertEqual(dog_bio,'dog_bio')
        self.assertEqual(dog_status,'dog_status')
        self.assertEqual(dog_dob,'2021-04-13')
        self.assertEqual(dog_breed,'dog_breed')
        self.assertEqual(dog_weight,251.32)

    def test_host_available_date(self):
        ava = self.ava_date_001
        word = str(ava)
        self.assertEqual(word,str(ava))


class TestAPI(APITestCase):

    @classmethod
    def setUp(self):
        self.client = APIClient()
        self.acc_001 = Accounts.objects.create(
            is_host = True,
            username = 'host001',
            email = 'host001@email.com'
        )
        self.acc_001.set_password('password')
        self.acc_001.save()
        self.t_acc001 = Token.objects.create(user=self.acc_001)
        self.acc_002 = Accounts.objects.create(
            is_host = False,
            username = 'cus001',
            email = 'cus001@email.com'
        )
        self.acc_002.set_password('password')
        self.acc_002.save()
        self.t_acc002 = Token.objects.create(user=self.acc_002)
        self.host001 = Host.objects.get(account=self.acc_001)
        self.cus001 = Customer.objects.get(account=self.acc_002)
        self.dog_001 = Dog.objects.create(
            customer=self.cus001,
            dog_name='dog_name',
            dog_breed='dog_breed',
            gender='Female'
        )

        
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
        self.client.force_authenticate(user=self.acc_001,token=self.t_acc001)

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
    
    def test_login(self):
        url = reverse("accounts:token")
        data  ={"username": self.acc_001.username, "password": "password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
    
    def test_cus_profile(self):
        self.client.force_authenticate(user=self.acc_002,token=self.t_acc002)

        url = reverse('accounts:profilecustomer-detail',kwargs={'pk':self.acc_002.id})
        
        data1={
            "first_name":'first_name',
            "last_name":'last_name',
            "gender":'male',
            "customer_bio":'customer_bio',
            "customer_dog_count":5,
            "customer_hosted_count":20,
            "address":'address',
            "mobile":'0812345678',
            "dob":'2021-04-13',
            "latitude":10,
            "longitude":10,
        }
        response1 = self.client.put(url,data1,format='json')
        data2={
            "first_name":'new_first_name',
            "last_name":'new_last_name'
        }
        response2 = self.client.patch(url,data2,format='json')
        self.assertEqual(response1.status_code,status.HTTP_200_OK)
        self.assertEqual(response2.status_code,status.HTTP_200_OK)
    
    def test_host_profile(self):
        self.client.force_authenticate(user=self.acc_001,token=self.t_acc001)

        url = reverse('accounts:profilehost-detail',kwargs={'pk':self.acc_001.id})
        url += '?all=1'
        data1={
            "first_name":'first_name',
            "last_name":'last_name',
            "gender":'Male',
            "host_bio":'host_bio',
            "host_rating":4.53,
            "host_hosted_count":10,
            "host_max":9,
            "host_available_date":'2021-04-13',
            "host_area":20.5,
            "address":'address',
            "mobile":'0812345678',
            "dob":'2021-04-12',
            "latitude":10,
            "longitude":10,
        }
        response1=self.client.put(url,data1,format='json')
        data2={
            "first_name":'new_first_name',
            "last_name":'new_last_name'
        }
        response2 = self.client.patch(url,data2,format='json')
        self.assertEqual(response1.status_code,status.HTTP_200_OK)
        self.assertEqual(response2.status_code,status.HTTP_200_OK)
    
    def test_dog_profile(self):
        self.client.force_authenticate(user=self.acc_002,token=self.t_acc002)

        url1 = reverse('accounts:profilecustomer-dogs-list',kwargs={'customer_pk':self.acc_002.id})

        data1={
            'dog_name':'dog_name',
            'dog_bio':'dog_bio',
            'dog_create_date':'2021-04-13',
            'dog_dob':'2021-04-12',
            'dog_breed':'dog_breed',
            'dog_weight':55.36
        }
        response1=self.client.post(url1,data1,format='json')
        
        url2 = reverse('accounts:profilecustomer-dogs-detail',kwargs={'customer_pk':self.acc_002.id,'pk':self.dog_001.id})

        data2={
            'dog_name':'new_dog_name',
            'dog_bio':'new_dog_bio'
        }
        response2=self.client.patch(url2,data2,format='json')
        
        data3={
            'dog_name':'dog_name',
            'dog_bio':'dog_bio',
            'dog_create_date':'2021-04-13',
            'dog_dob':'2021-04-12',
            'dog_breed':'dog_breed',
            'dog_weight':55.36
        }
        response3=self.client.post(url1,data3,format='json')
        response3=self.client.delete(url2,data3,format='json')
        

        self.assertEqual(response1.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code,status.HTTP_200_OK)
        self.assertEqual(response3.status_code,status.HTTP_204_NO_CONTENT)

    def test_host_availabledate(self):
        self.client.force_authenticate(user=self.acc_001,token=self.t_acc001)

        url = reverse('accounts:profilehost-availabledate-list',kwargs={'host_pk':self.acc_001.id}) 

        data1={
            'date': date.today() + timedelta(days=1)
        }
        response1=self.client.post(url,data1,format='json')
        
        data2={
            'date': date.today() - timedelta(days=1)
        }
        response2=self.client.post(url,data2,format='json')
        
        self.assertEqual(response1.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code,status.HTTP_400_BAD_REQUEST)

