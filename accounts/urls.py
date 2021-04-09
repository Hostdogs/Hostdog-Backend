from accounts.views import AccountsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import DogViewSet,CustomerViewSet, HostViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register('account', AccountsViewSet)
router.register('dog',DogViewSet)
router.register('host',HostViewSet)
router.register('customer',CustomerViewSet)

urlpatterns = router.urls

