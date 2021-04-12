from django.test import TestCase
from django.contrib.auth.models import (
    AbstractUser,
)
from accounts.models import Accounts, Customer, Host, Dog

class testCreateAccount(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        test_Accounts = Accounts.objects.create(
            password='123123123',
            last_login='2021-4-11',
            username='test_User001',
            email='account@email.com',
            first_name='first',
            last_name='last',
            date_joined='2021-3-26',
            is_customer=True,
            address='address',
            mobile='0812345678',
            dob='2000-11-8'
        )
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

            password = f'{acc.password}'
            last_login = f'{acc.last_login}'
            username = f'{acc.username}'
            email = f'{acc.email}'
            first_name = f'{acc.first_name}'
            last_name = f'{acc.last_name}'
            date_joined = f'{acc.date_joined}'
            is_customer = f'{acc.is_customer}'
            address = f'{acc.address}'
            mobile = f'{acc.mobile}'
            dob = f'{acc.dob}'
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
    
        customer = Dog.objects.create(customer='customer')
        dog_name = Dog.objects.create(dod_name='dog_name')
        dog_bio = Dog.objects.create(dog_bio='dog_bio')
        dog_status = Dog.objects.create(dog_status='dog_status')
        dog_create_date = Dog.objects.create(dog_create_date='dog_create_date')
        dog_dob = Dog.objects.create(dog_dob='dog_dob')
        dog_breed = Dog.objects.create(dog_breed='dog_breed')
        dog_weight = Dog.objects.create(dog_weight='dog_weight')

        def test_dog(self):
            dog = Dog.objects.get(id = 1)
            customer = f'{dog.account}'
            dog_name = f'{dog.dog_name}'
            dog_bio = f'{dog.dog_bio}'
            dog_status = f'{dog.dog_status}'
            dog_create_date = f'{dog.dog_create_date}'
            dog_dob = f'{dog.dog_dob}'
            dog_breed = f'{dog.dog_breed}'
            dog_weight = f'{dog.dog_weight}'

            self.assertEqual(customer,'customer')
            self.assertEqual(str(dog_name),'dog_name')
            self.assertEqual(dog_bio,'dog_bio')
            self.assertEqual(dog_status,'dog_status')
            self.assertEqual(dog_create_date,'dog_create_date')
            self.assertEqual(dog_dob,'dog_dob')
            self.assertEqual(dog_breed,'dog_breed')
            self.assertEqual(dog_weight,'dog_weight')
            
    def test_dog_model(self):
        customer = Dog.objects.create(customer='customer')
        dog_name = Dog.objects.create(dod_name='dog_name')
        dog_bio = Dog.objects.create(dog_bio='dog_bio')
        dog_status = Dog.objects.create(dog_status='dog_status')
        dog_create_date = Dog.objects.create(dog_create_date='dog_create_date')
        dog_dob = Dog.objects.create(dog_dob='dog_dob')
        dog_breed = Dog.objects.create(dog_breed='dog_breed')
        dog_weight = Dog.objects.create(dog_weight='dog_weight')
        self.assertEqual(customer,'customer')
        self.assertEqual(str(dog_name),'dog_name')
        self.assertEqual(dog_bio,'dog_bio')
        self.assertEqual(dog_status,'dog_status')
        self.assertEqual(dog_create_date,'dog_create_date')
        self.assertEqual(dog_dob,'dog_dob')
        self.assertEqual(dog_breed,'dog_breed')
        self.assertEqual(dog_weight,'dog_weight')
