from django.test import TestCase,Client
from django.contrib.auth.models import (
    AbstractUser,
)
from accounts.models import Host,Customer,Dog,Meal
#py manage.py makemigrations
#py manage.py migrate
#coverage run --omit="*/hostdog/*" manage.py test
#coverage html
class TestModel(TestCase):

    @classmethod
    def setUpTestData(self):
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

        host_001 = Host.objects.create(
            first_name='first',
            last_name='last',
            account_id=acc_002.id,
            gender='Female',
            host_bio='host_bio',
            host_rating=4.5,
            host_schedule='host_schedule'
        )

        meal_001 = Meal.objects.create(
            host_id=host_001.id,
            meal_type='meal_type',
            meal_price=24.132
        )
        
    def test_meal(self):
        meal = Meal.objects.get(host_id=1)

        host_id = meal.host_id
        meal_type = f'{meal.meal_type}'
        meal_price = meal.meal_price

        word = str(meal)
        self.assertEqual(word,str(meal))
        self.assertEqual(meal_type,'meal_type')
        self.assertEqual(meal_price,24.132)

