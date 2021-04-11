from accounts.views import (
    CustomerProfileViewSet,
    HostProfileViewSet,
    AccountsViewSet,
    DogProfileViewSet,
)
from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin

app_name = "accounts"


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()
router.register(r"account", AccountsViewSet)
router.register(r"dog", DogProfileViewSet)
router.register(r"profile-host", HostProfileViewSet)
router.register(r"profile-customer", CustomerProfileViewSet)

urlpatterns = router.urls
