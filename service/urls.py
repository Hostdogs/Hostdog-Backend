from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, MealViewSet, HostServiceViewSet
from payment.views import PaymentViewSet
from rest_framework_nested import routers

app_name = "service"

service_router = DefaultRouter()
"""
/api/service/.../
"""
service_router.register(r"services", ServiceViewSet,basename="services")

service_router.register("meals", MealViewSet)
"""
/api/service/services/payment
"""
payment_router=routers.NestedDefaultRouter(service_router,r"services",lookup="service")
payment_router.register(r"payment",PaymentViewSet,basename="payment")




urlpatterns = service_router.urls
urlpatterns+=payment_router.urls

print(f"URL patterns size at service : {len(urlpatterns)}")