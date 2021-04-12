from django.test import TestCase
from django.contrib.auth.models import (
    AbstractUser,
)
from accounts.models import Accounts, Customer, Host, Dog
from rest_framework.test import APITestCase
import datetime

class TestModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        acc_001 = Accounts.objects.create(
            is_superuser=False,
            password='123123123',
            last_login='2021-04-12 00:00:00+00:00',
            username='test_User001',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-12 00:00:00+00:00',
            is_host=True
        )
        acc_002 = Accounts.objects.create(
            is_superuser=False,
            password='123123123',
            last_login='2021-04-12',
            username='test_User002',
            email='account@email.com',
            is_active=True,
            is_staff=False,
            date_joined='2021-04-12',
            is_host=False
        )
        acc_001.save()
        acc_002.save()

        cus_001 = Customer.objects.create(
            first_name='first',
            last_name='last',
            account=Accounts.objects.get(id = 1),
            gender='Male',
            address='address',
            mobile='0812345678',
            dob='2021-04-12',
            customer_bio='customer_bio',
            customer_dog_count=3,
            customer_hosted_count=4
        )
    
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
        self.assertEqual(last_login,'2021-04-12 00:00:00+00:00')
        self.assertEqual(username,'test_User001')
        self.assertEqual(email,'account@email.com')
        self.assertTrue(is_active)
        self.assertFalse(is_staff)
        self.assertEqual(date_joined,'2021-04-12 00:00:00+00:00')
        self.assertTrue(is_host)

    def test_customer(self):
        cus = Customer.objects.get(id = 1)

        first_name = f'{cus.first_name}'
        last_name = f'{cus.last_name}'
        account = Accounts.objects.get(account_id)
        gender = f'{cus.gender}'
        address = f'{cus.address}'
        mobile = f'{cus.mobile}'
        dob = f'{cus.dob}'
        customer_bio = f'{cus.customer_bio}'
        customer_dog_count = cus.customer_dog_count
        customer_hosted_count = cus.customer_hosted_count

        word = str(cus)
        self.assertEqual(word,cus)
        self.assertEqual(first_name,'first')
        self.assertEqual(last_name,'last')
        self.assertEqual(account,1)
        self.assertEqual(gender,'Male')
        self.assertEqual(address,'address')
        self.assertEqual(mobile,'0812345678')
        self.assertEqual(dob,'2021-04-12')
        self.assertEqual(customer_bio,'customer_bio')
        self.assertEqual(customer_dog_count,3)
        self.assertEqual(customer_hosted_count,4)

        """
        test_Customer = Customer.objects.create(
            account=123,
            customer_bio='customer_bio',
            customer_dog_count=3,
            customer_hosted_count=4
        )
        test_Host = Host.objects.create(
            account=123,
            host_bio='host_bio',
            host_rating=4.5,
            host_hosted_count=7,
            host_max=2,
            host_avaliable=1,
            host_area=5.32,
            host_schedule='host_schedule'
        )
        test_Dog = Dog.objects.create(
            customer=123,
            dog_name='dog_name',
            dog_bio='dog_bio',
            dog_status='dog_status',
            dog_create_date='2021-3-26',
            dog_dob='2021-2-14',
            dog_breed='dog_breed',
            dog_weight=251.32
        )

        def test_Account_Content(self):
            acc = Accounts.objects.get(id = 1)
            cus = Customer.objects.get(id = 1)
            host = Host.objects.get(id = 1)
            dog = Dog.objects.get(id = 1)

            test_Accounts = f'{acc.password}'
            test_Accounts = f'{acc.last_login}'
            test_Accounts = f'{acc.username}'
            test_Accounts = f'{acc.email}'
            test_Accounts = f'{acc.first_name}'
            test_Accounts = f'{acc.last_name}'
            test_Accounts = f'{acc.date_joined}'
            test_Accounts = f'{acc.is_customer}'
            test_Accounts = f'{acc.address}'
            test_Accounts = f'{acc.mobile}'
            test_Accounts = f'{acc.dob}'
            self.assertEqual(password,'123123123')
            self.assertEqual(last_login,'2021-4-11')
            self.assertEqual(str(username),'test_User001')
            self.assertEqual(email,'account@email.com')
            self.assertEqual(first_name,'first')
            self.assertEqual(last_name,'last')
            self.assertEqual(date_joined,'2021-3-26')
            self.assertEqual(is_customer,True)
            self.assertEqual(address,'address')
            self.assertEqual(mobile,'0812345678')
            self.assertEqual(dob,'2000-11-8')

            account = f'{cus.account}'
            customer_bio = f'{cus.customer_bio}'
            customer_dog_count = f'{cus.customer_dog_count}'
            customer_hosted_count = f'{cus.customer_hosted_count}'
            self.assertEqual(account,123)
            self.assertEqual(customer_bio,'customer_bio')
            self.assertEqual(customer_dog_count,3)
            self.assertEqual(customer_hosted_count,4)

            account = f'{host.account}'
            host_bio = f'{host.host_bio}'
            host_rating = f'{host.host_rating}'
            host_hosted_count = f'{host.host_hosted_count}'
            host_max = f'{host.host_max}'
            host_avaliable = f'{host.host_avaliable}'
            host_area = f'{host.host_area}'
            host_schedule = f'{host.host_schedule}'
            self.assertEqual(account,123)
            self.assertEqual(host_bio,'host_bio')
            self.assertEqual(host_rating,4.5)
            self.assertEqual(host_hosted_count,7)
            self.assertEqual(host_max,2)
            self.assertEqual(host_avaliable,1)
            self.assertEqual(host_area,5.32)
            self.assertEqual(host_schedule,'host_schedule')

            customer = f'{dog.account}'
            dog_name = f'{dog.dog_name}'
            dog_bio = f'{dog.dog_bio}'
            dog_status = f'{dog.dog_status}'
            dog_create_date = f'{dog.dog_create_date}'
            dog_dob = f'{dog.dog_dob}'
            dog_breed = f'{dog.dog_breed}'
            dog_weight = f'{dog.dog_weight}'
            self.assertEqual(customer,123)
            self.assertEqual(str(dog_name),'dog_name')
            self.assertEqual(dog_bio,'dog_bio')
            self.assertEqual(dog_status,'dog_status')
            self.assertEqual(dog_create_date,'2021-3-26')
            self.assertEqual(dog_dob,'2021-2-14')
            self.assertEqual(dog_breed,'dog_breed')
            self.assertEqual(dog_weight,251.32)
            """
            
    
        

    
