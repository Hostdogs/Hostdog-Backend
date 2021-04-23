from django.db.models import base
from accounts.views import (
    AuthToken,
    CustomerProfileViewSet,
    HostAvailableDateViewSet,
    HostHouseImageViewSet,
    HostProfileViewSet,
    AccountsViewSet,
    DogProfileViewSet,
)
from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from service.views import HostServiceViewSet

app_name = "accounts"

#combination of NestedRouter and DefaultRouter So goooooddd
class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()
"""
/api/.../
"""
router.register(r"accounts", AccountsViewSet)
router.register(r"dogs", DogProfileViewSet)
router.register(r"available-date", HostAvailableDateViewSet)

"""
/api/profilehost/.../
"""
profilehost_route = router.register(r"profilehost", HostProfileViewSet)
profilehost_route.register(
    r"host-service",
    HostServiceViewSet,
    basename="profilehost-host-service",
    parents_query_lookups=["host"],
)
profilehost_route.register(
    r"available-date",
    HostAvailableDateViewSet,
    basename="profilehost-availabledate",
    parents_query_lookups=["host"],
)
profilehost_route.register(
    r"house-image",
    HostHouseImageViewSet,
    basename="profilehost-house-image",
    parents_query_lookups=["host"]
)

"""
/api/profilecustomer/.../
"""
router.register(r"profilecustomer", CustomerProfileViewSet).register(
    r"dogs",
    DogProfileViewSet,
    basename="profilecustomer-dogs",
    parents_query_lookups=["customer"],
)

urlpatterns = [path("token/", AuthToken.as_view(), name="token")]
urlpatterns += router.urls
