from accounts.serializers import (
    AccountSerializer,
    CustomerProfileSerializer,
    HostProfileSerializer,
    DogProfileSerializer,
    ChangePasswordSerializer,
)
from accounts.models import Accounts, Customer, Host, Dog
from rest_framework import generics, viewsets, status, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class AccountsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query account
    """

    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ("get", "post", "delete", "head", "options")

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


class AuthToken(ObtainAuthToken):
    """
    API endpoint for Token authentication
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "username": user.username,
            "email": user.email
        })

class DogProfileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for query dog
    """

    queryset = Dog.objects.all()
    serializer_class = DogProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [r"^dog_name", r"^dog_breed"]

    def get_queryset(self):
        """
        Can query only your dog
        """
        user = self.request.user
        #print(user, self.request.auth)
        queryset = Dog.objects.filter(customer=user.id)
        return queryset

class CustomerProfileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for query customer
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer
    http_method_names = ("get", "put", "patch", "head", "options")

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return generics.get_object_or_404(Customer, account=item)



class HostProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query host
    """

    queryset = Host.objects.all()
    serializer_class = HostProfileSerializer
    http_method_names = ("get", "put", "patch", "head", "options")
    filter_backends = [filters.SearchFilter]
    search_fields = [r"^first_name", r"^last_name"]

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return generics.get_object_or_404(Host, account=item)

    def get_queryset(self):
        """
        TODO:
            - choose filtering field
            - endpoint for profile querying
        """
        pass
