from accounts.views import (
    AuthToken,
    CustomerProfileViewSet,
    HostAvailableDateViewSet,
    HostHouseImageViewSet,
    HostProfileViewSet,
    AccountsViewSet,
    DogProfileViewSet,
    DogFeedingTimeViewSet,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from service.views import HostServiceViewSet
from rest_framework_nested import routers

app_name = "accounts"


"""
/api/.../
"""
router = DefaultRouter()
router.register(r"accounts", AccountsViewSet)
router.register(r"dogs", DogProfileViewSet)
router.register(r"available-date", HostAvailableDateViewSet)

"""
/api/profilehost/.../

"""
profilehost_router = DefaultRouter()
profilehost_router.register(r"profilehost", HostProfileViewSet, basename="profilehost")

host_service_router = routers.NestedDefaultRouter(
    profilehost_router, r"profilehost", lookup="host"
)

host_service_router.register(
    r"host-service", HostServiceViewSet, basename="profilehost-host-service"
)

host_service_router.register(
    r"available-date", HostAvailableDateViewSet, basename="profilehost-availabledate"
)

host_service_router.register(
    r"house-image", HostHouseImageViewSet, basename="profilehost-house-image"
)

"""
/api/profilecustomer/.../
"""
profile_customer_router = DefaultRouter()
profile_customer_router.register(
    r"profilecustomer", CustomerProfileViewSet, basename="profilecustomer"
)

dogs_router = routers.NestedDefaultRouter(
    profile_customer_router, r"profilecustomer", lookup="customer"
)
dogs_router.register(r"dogs", DogProfileViewSet, basename="profilecustomer-dogs")

feeding_time_router = routers.NestedDefaultRouter(dogs_router, r"dogs", lookup="dog")
feeding_time_router.register(
    r"feeding-time", DogFeedingTimeViewSet, basename="feeding-time"
)


urlpatterns = [path("token/", AuthToken.as_view(), name="token")]
urlpatterns += router.urls
urlpatterns += profilehost_router.urls
urlpatterns += profile_customer_router.urls
urlpatterns += host_service_router.urls
urlpatterns += dogs_router.urls
urlpatterns += feeding_time_router.urls
print(f"URL Pattern size : {len(urlpatterns)}")