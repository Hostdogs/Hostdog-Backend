from accounts.views import AccountsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'accounts'

router = DefaultRouter()
router.register('account', AccountsViewSet)

urlpatterns = router.urls

