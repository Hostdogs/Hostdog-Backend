from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, MealViewSet, HostServiceViewSet

app_name = "service"

router = DefaultRouter()
router.register("service", ServiceViewSet)
router.register("meal", MealViewSet)
router.register("hostservice", HostServiceViewSet)


urlpatterns = router.urls
