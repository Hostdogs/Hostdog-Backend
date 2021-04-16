from accounts.views import (
    AuthToken,
    CustomerProfileViewSet,
    HostAvailableDateViewSet,
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
router.register(r"accounts", AccountsViewSet)
router.register(r"dogs", DogProfileViewSet)
router.register(r"profilehost", HostProfileViewSet).register(
    r"available-date",
    HostAvailableDateViewSet,
    basename="profilehost",
    parents_query_lookups=["host"]
)
router.register(r"profilecustomer", CustomerProfileViewSet).register(
    r"dogs",
    DogProfileViewSet,
    basename="profilecustomer-dogs",
    parents_query_lookups=["customer"]
)
urlpatterns = [
    path("token/", AuthToken.as_view())
]
urlpatterns += router.urls
