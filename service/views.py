from .serializers import ServiceSerializer
from .models import Service
from rest_framework import generics, viewsets, status



class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
