from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, MealViewSet, HostServiceViewSet

app_name = "service"

router = DefaultRouter()
"""
/api/service/.../
"""
router.register("services", ServiceViewSet)
router.register("meals", MealViewSet)


urlpatterns = router.urls
print(f"URL patterns size at service : {len(urlpatterns)}")