from accounts.serializers import (
    AccountSerializer,
    CustomerSerializer,
    HostSerializer,
    DogSerializer,
    ChangePasswordSerializer,
)
from accounts.models import Accounts, Customer, Host
from rest_framework import generics, viewsets, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import Dog
from rest_framework.decorators import action
from rest_framework.response import Response


class AccountsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query account
    """

    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer

    @action(
        methods=["post"],
        detail=True,
        url_path="change-password",
        url_name="change_password",
    )  # can set permission class at this decorator
    def set_password(self, request, pk=None):
        """
        Change password endpoint
        """
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"status": "success", "message": "Password updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query dog
    """

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
