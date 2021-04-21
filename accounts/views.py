from accounts.serializers import (
    AccountSerializer,
    CustomerProfileSerializer,
    HostAvailableDateSerializer,
    HostProfileSerializer,
    DogProfileSerializer,
    ChangePasswordSerializer,
)
from accounts.models import Accounts, Customer, Host, Dog, HostAvailableDate
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
from datetime import date, timedelta, datetime


class IsOwnerOrAdmin(BasePermission):
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


class DogOwnerPermission(BasePermission):
    """
    - Allow only dog owner to update or partial-update their dog
    - Only dog owner can create their dog on their profile
    - Anonymous user not allow
    - Allow to  read-only if not owner of the dog
    """

    def has_permission(self, request, view):
        if view.action == "create":
            parent_lookup_customer = view.kwargs.get("parent_lookup_customer")
            if (
                parent_lookup_customer is not None
                and Accounts.objects.get(id=parent_lookup_customer) != request.user
            ):
                return False
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.customer.account == request.user


class OwnProfilePermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    - Anyone who authenticated can see other profile
    - Only profile owner can update, partial-update their profile
    - Profile cant create (Created when account was create)
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.account == request.user


class AvailableDateOwnPermission(BasePermission):
    """
    Allow only profile owner to edit their own available date
    - Anyone who authenticated can see this available date
    """

    def has_permission(self, request, view):
        if view.action == "create":
            parent_lookup_host = view.kwargs.get("parent_lookup_host")
            if (
                parent_lookup_host is not None
                and Accounts.objects.get(id=parent_lookup_host) != request.user
            ):
                return False
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.host.account == request.user


class AccountsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for query account
    """

    authentication_classes = [TokenAuthentication]
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
            self.permission_classes = [IsOwnerOrAdmin]
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
        print(user)
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

    permission_classes = [DogOwnerPermission & IsAuthenticated]
    queryset = Dog.objects.all()
    serializer_class = DogProfileSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [r"^dog_name", r"^dog_breed"]
    filterset_fields = ["dog_status", "dog_breed", "dog_weight", "dog_status", "gender"]


class CustomerProfileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for query customer
    """

    permission_classes = [OwnProfilePermission & IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer
    http_method_names = ["get", "put", "patch", "head", "options"]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [r"^first_name", r"^last_name"]
    filterset_fields = ["customer_dog_count"]


class HostProfileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for query host
    """

    permission_classes = [OwnProfilePermission & IsAuthenticated]
    queryset = Host.nearest_host.all()
    serializer_class = HostProfileSerializer
    http_method_names = ["get", "put", "patch", "head", "options"]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [r"^first_name", r"^last_name"]
    filterset_fields = ["host_rating", "host_area"]

    def get_queryset(self):
        dist = self.request.query_params.get("distance")
        weekday = self.request.query_params.getlist("weekday")
        exact_date = self.request.query_params.getlist("date")
        date_range = self.request.query_params.getlist("date_range")
        date_full_range = self.request.query_params.getlist("date_full_range")
        area_range = self.request.query_params.getlist("area_range")
        queryset = Host.nearest_host.filter(
            available_dates__date__isnull=False
        ).distinct()
        print(dist, weekday, exact_date, date_range, area_range)
        print(queryset)
        if dist:
            customer = Customer.objects.get(account=self.request.user)
            lat = customer.latitude
            long = customer.longitude
            queryset = queryset.nearest_host_within_x_km(
                current_lat=lat, current_long=long, x_km=dist
            )
        if weekday:
            queryset = queryset.filter(available_dates__date__iso_week_day__in=weekday)
        if exact_date:
            queryset = queryset.filter(available_dates__date__in=date)
        if len(date_full_range) >= 2:
            start_date_string, end_date_string = date_full_range[:2]
            start_date = datetime.strptime(start_date_string, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_string, "%Y-%m-%d").date()
            delta = end_date - start_date
            all_date_within_interval = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
            for wanted_date in all_date_within_interval:
                queryset = queryset.filter(available_dates__date=wanted_date)
        if len(date_range) >= 2:
            date_range_interval = date_range[:2]
            queryset = queryset.filter(available_dates__date__range=date_range_interval)
        if len(area_range) >= 2:
            area_range_interval = area_range[:2]
            queryset = queryset.filter(host_area__range=area_range_interval)
        return queryset


class HostAvailableDateViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for manage host avalilable date
    """

    permission_classes = [AvailableDateOwnPermission & IsAuthenticated]
    queryset = HostAvailableDate.objects.all()
    serializer_class = HostAvailableDateSerializer
    http_method_names = ["get", "post", "put", "patch", "delete", "head", "options"]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [r"^date"]
    filterset_fields = ["date"]