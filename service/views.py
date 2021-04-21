from .serializers import (
    ServiceSerializer,
    MealSerializer,
    HostServiceSerializer
)
from .models import Service, Meal, HostService
from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing service
        - Customer request service to Host (POST) --> notification to host
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class MealViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing meal of service
    """
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [DjangoFilterBackend]


class HostServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing host service
    """
    queryset = HostService.objects.all()
    serializer_class = HostServiceSerializer
