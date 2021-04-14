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
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission,
    IsAdminUser,
    SAFE_METHODS,
)


class IsOwner(BasePermission):
    """
    Object-level permission to only owner of an object or admin to edit it.
    """

    message = "you are not owner of this account!"

    def has_object_permission(self, request, view, obj):
        """
        Requirements:
            - authenticated
            - staff
            - owner
        """
        user = request.user
        return user and user.is_authenticated and (user.is_staff or obj == user)


class IsDogOwner(BasePermission):
    """
    Only dog owner can create their dog on their profile
    """

    message = "you can't create dog profile on other profile!"

    def has_permission(self, request, view):
        """
        Allow GET method for read only but user must authenticated themself
        """
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        if view.action == "create":
            parent_lookup_customer = int(view.kwargs.get("parent_lookup_customer"))
            if (
                parent_lookup_customer is not None
                and parent_lookup_customer != request.user.id
            ):
                return False
            return int(request.data.get("customer")) == request.user.id
        return super().has_permission(request, view)


class AccountsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query account
    """

    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

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

    def get_permissions(self):
        if self.action in {"list", "update", "partial_update"}:
            self.permission_classes = [IsAdminUser]
        elif self.action in {"retrieve", "destroy", "set_password"}:
            self.permission_classes = [IsOwner]
        return super().get_permissions()


class AuthToken(ObtainAuthToken):
    """
    API endpoint for Token authentication
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "email": user.email,
            }
        )


class DogProfileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for query dog
    """

    permission_classes = [IsDogOwner]
    queryset = Dog.objects.all()
    serializer_class = DogProfileSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [r"^dog_name", r"^dog_breed"]
    filterset_fields = ["dog_status", "dog_breed", "dog_weight", "dog_status", "gender"]

class CustomerProfileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for query customer
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer
    http_method_names = ["get", "put", "patch", "head", "options"]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [r"^first_name", r"^last_name"]
    filterset_fields = ["customer_dog_count"]

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
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = (r"^first_name", r"^last_name")
    filterset_fields = ("host_rating", "host_area", "host_schedule")

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return generics.get_object_or_404(Host, account=item)
