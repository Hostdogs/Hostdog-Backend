
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet,MealViewSet


router = DefaultRouter()
router.register('service', ServiceViewSet)
router.register('meal',MealViewSet)



urlpatterns = router.urls
