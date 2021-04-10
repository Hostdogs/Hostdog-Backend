from accounts.serializers import AccountSerializer,CustomerAccountSerializer, HostAccountSerializer, HostProfileSerializer,CustomerProfileSerializer,DogProfileSerializer
from accounts.models import Accounts, Customer, Host,Dog
from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query account
    """
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer 

class CustomerAccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query account
    """
    queryset = Accounts.objects.filter(is_customer=True)
    serializer_class = CustomerAccountSerializer

class HostAccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query account
    """
    queryset = Accounts.objects.filter(is_host=True)
    serializer_class = HostAccountSerializer



class CustomerProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer
    
    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get("pk")
    #     return generics.get_object_or_404(Customer, id=item)


class HostProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query host
    """
    queryset = Host.objects.all()
    serializer_class = HostProfileSerializer

    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get("pk")
    #     return generics.get_object_or_404(Host, id=item)


class DogProfileViewSet(viewsets.ModelViewSet):
    queryset = Dog.objects.all()
    serializer_class = DogProfileSerializer
