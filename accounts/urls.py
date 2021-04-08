from accounts.views import AccountsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import DogViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register('', AccountsViewSet)
router.register('dog',DogViewSet)

urlpatterns = router.urls

