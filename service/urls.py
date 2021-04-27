from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, MealViewSet, HostServiceViewSet
from payment.views import PaymentViewSet
from rest_framework_nested import routers

app_name = "service"

router = DefaultRouter()
"""
/api/service/.../
"""
router.register("services", ServiceViewSet)


host_service_router=DefaultRouter()


router.register("meals", MealViewSet)




urlpatterns = router.urls
print(f"URL patterns size at service : {len(urlpatterns)}")