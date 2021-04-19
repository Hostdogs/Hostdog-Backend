from .serializers import (
    ServiceSerializer,
    MealSerializer,
    HostServiceSerializer,
    ChatSerializer,
)
from .models import Service, Meal, HostService, Chat
from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["host"]


class HostServiceViewSet(viewsets.ModelViewSet):
    queryset = HostService.objects.all()
    serializer_class = HostServiceSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()  # .order_by('chat_date_time')
    serializer_class = ChatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["customer", "host"]
