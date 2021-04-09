from accounts.serializers import AccountSerializer, CustomerSerializer, HostSerializer,DogSerializer
from accounts.models import Accounts, Customer, Host
from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import Dog


class AccountsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query account
    """
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer


class DogViewSet(viewsets.ModelViewSet):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return generics.get_object_or_404(Customer, id=item)

    


class HostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query host
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return generics.get_object_or_404(Host, id=item)

    

