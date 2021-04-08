from accounts.views import AccountsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('account/', AccountsViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
]
