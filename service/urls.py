
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet,MealViewSet,HostServiceViewSet


router = DefaultRouter()
router.register('service', ServiceViewSet)
router.register('meal',MealViewSet)
router.register('host-service',HostServiceViewSet)



urlpatterns = router.urls
