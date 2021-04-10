from accounts.views import CustomerAccountViewSet,HostAccountViewSet,AccountViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import DogProfileViewSet,CustomerProfileViewSet, HostProfileViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register('account', AccountViewSet)
router.register('account-customer', CustomerAccountViewSet)
router.register('account-host', HostAccountViewSet)
router.register('dog',DogProfileViewSet)
router.register('profile-host',HostProfileViewSet)
router.register('profile-customer',CustomerProfileViewSet)

urlpatterns = router.urls

