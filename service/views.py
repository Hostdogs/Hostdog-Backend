from .serializers import ServiceSerializer,MealSerializer,HostServiceSerializer
from .models import Service,Meal,HostService
from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend



class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['host']

class HostServiceViewSet(viewsets.ModelViewSet):
    queryset = HostService.objects.all()
    serializer_class = HostServiceSerializer



   
    



    


