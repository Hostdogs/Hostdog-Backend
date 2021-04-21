from .serializers import ServiceSerializer, MealSerializer, HostServiceSerializer
from .models import Service, Meal, HostService
from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsOwnerAndHost(BasePermission):
    """
    - Allow only Host and Owner to access
    """

    def has_permission(self, request, view):
        return request.user.is_host

    def has_object_permission(self, request, view, obj):
        return obj.host.account == request.user


class IsAssociatedTo(BasePermission):
    """
    - Only user who associated to the service can view that service
    - Host who hosted the service can view that service
    - Customer who use the service can view that service
    - User who are not associated to the service cant view that service
    - Admin can access every service
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        host_who_own_service = obj.host.account
        customer_who_use_service = obj.customer.account
        return (
            user.is_staff
            or host_who_own_service == user
            or customer_who_use_service == user
        )


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing service
        - Customer request service to Host (POST) --> notification to host
    """

    permission_classes = [IsAssociatedTo & IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["main_status"]


class MealViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing meal of service
    """

    permission_classes = [IsAuthenticated]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["meal_type", "meal_price"]


class HostServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing host service
        - Only Host can access this viewset
        - Only Owner can access their own
    """

    permission_classes = [IsOwnerAndHost & IsAuthenticated]
    queryset = HostService.objects.all()
    serializer_class = HostServiceSerializer

    def get_queryset(self):
        user = self.request.user
        return HostService.objects.filter(host=user)