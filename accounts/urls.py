
from accounts.views import CustomerProfileViewSet, HostProfileViewSet, AccountsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import DogProfileViewSet,CustomerProfileViewSet, HostProfileViewSet

app_name = "accounts"

router = DefaultRouter()
router.register('account', AccountsViewSet)
router.register('dog',DogProfileViewSet)
router.register('profile-host',HostProfileViewSet)
router.register('profile-customer',CustomerProfileViewSet)

urlpatterns = router.urls
