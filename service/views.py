from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from service.serializers import (
    ServiceDetailSerializer,
    ServiceResponseSerializer,
    ServiceSerializer,
    MealSerializer,
    HostServiceSerializer,
)
from service.models import Service, Meal, HostService
from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import action


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

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create":
            serializer_class = ServiceSerializer
        elif self.action == "response":
            serializer_class = ServiceResponseSerializer
        else:
            serializer_class = ServiceDetailSerializer
        return serializer_class

    @action(methods=["post"], detail=True, url_path="response", url_name="response")
    def response(self, request, pk=None):
        """
        Accept or Decline customer request
        """
        service = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = serializer.data["response"]
            if response:
                service.accept()
                return Response({"success": "Service accepted"}, status=status.HTTP_200_OK)
            else:
                service.decline()
                return Response({"success": "Service decline"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class MealViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing meal of service
    """

    permission_classes = [IsAuthenticated]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["meal_type", "meal_price"]


class HostServiceViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for managing host service
        - Only Host can access this viewset
        - Only Owner can access their own
    """

    permission_classes = [IsOwnerAndHost & IsAuthenticated]
    queryset = HostService.objects.all()
    serializer_class = HostServiceSerializer
    http_method_names = ["get", "put", "patch", "head", "options"]
