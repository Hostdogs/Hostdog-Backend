from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, MealViewSet, HostServiceViewSet

app_name = "service"

router = DefaultRouter()
router.register("services", ServiceViewSet)
router.register("meals", MealViewSet)
router.register("hostservices", HostServiceViewSet)


urlpatterns = router.urls
