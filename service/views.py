from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from service.serializers import (
    AddMealSerializer,
    ServiceDetailSerializer,
    ServiceResponseSerializer,
    ServiceSerializer,
    MealSerializer,
    HostServiceSerializer,
)
from service.models import Services, Meal, HostService
from rest_framework import generics, serializers, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import action
from rest_framework_extensions.mixins import NestedViewSetMixin

class IsOwnerAndHost(BasePermission):
    """
    - Allow only Host and Owner to access
    """

    def has_permission(self, request, view):
        return request.user.is_host

    def has_object_permission(self, request, view, obj):
        return obj.host.account == request.user


class IsAssociatedTo(BasePermission):
    """
    - Only user who associated to the service can view that service
    - Host who hosted the service can view that service
    - Customer who use the service can view that service
    - User who are not associated to the service cant view that service
    - Admin can access every service
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        host_who_own_service = obj.host.account
        customer_who_use_service = obj.customer.account
        return (
            user.is_staff
            or host_who_own_service == user
            or customer_who_use_service == user
        )


class ServiceViewSet(NestedViewSetMixin,viewsets.ModelViewSet):
    """
    API endpoint for managing service
        - Customer request service to Host (POST) --> notification to host
    """

    permission_classes = [IsAssociatedTo & IsAuthenticated]
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["main_status"]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "response":
            serializer_class = ServiceResponseSerializer 
        elif self.action == "create":
            serializer_class = ServiceSerializer
        else:
            serializer_class = ServiceDetailSerializer
        return serializer_class

    @action(methods=["post"], detail=True, url_path="response", url_name="response")
    def response(self, request, pk=None):
        """
        Accept or Decline something at request
        """
        service = self.get_object()
        user = self.request.user
        serializer = ServiceResponseSerializer(data=request.data)
        if serializer.is_valid():
            accept = serializer.data.get("accept")
            cancel = serializer.data.get("cancel")
            review = serializer.data.get("review")
            return_dog = serializer.data.get("return_dog")
            receive_dog = serializer.data.get("receive_dog")
            print("receive_dog",receive_dog)
            if user.is_host: # Host
                if service.main_status == "pending": # Accept/Decline
                    if accept:
                        service.accept()
                        return Response(
                            {"success": "Service accepted"}, status=status.HTTP_200_OK
                        )
                    else:
                        service.decline()
                        return Response(
                            {"success": "Service decline"}, status=status.HTTP_200_OK
                        )
                elif service.main_status == "in_progress": 
                    if receive_dog: # Host ยืนยันการรับหมา
                        host_receive_dog_success = service.host_receive_dog()
                        response_data = {"success": "Host receive dog success"} if host_receive_dog_success else {"fail": "Can't receive dog"}
                        status_code = status.HTTP_200_OK if host_receive_dog_success else status.HTTP_400_BAD_REQUEST
                        return Response(response_data, status=status_code)
                    elif return_dog: # Host ยืนยันการคืนหมา
                        return_dog_success = service.return_dog()
                        response_data = {"success": "Host return dog success"} if return_dog_success else {"fail": "Can't return dog"}
                        status_code = status.HTTP_200_OK if return_dog_success else status.HTTP_400_BAD_REQUEST
                        return Response(response_data, status=status_code)
            else: # Customer
                if service.main_status != "late" and cancel: #ยกเลิกบริการ
                    cancel_success = service.cancel()
                    response_data = {"success": "Service cancelled"} if cancel_success else {"fail": "Can't cancel service"}
                    status_code = status.HTTP_200_OK if cancel_success else status.HTTP_400_BAD_REQUEST
                    return Response(response_data, status=status_code)
                elif service.main_status == "in_progress":  # กดรับหมา
                    if receive_dog:
                        print("kuy pat")
                        customer_receive_dog_success = service.customer_receive_dog()
                        response_data = {"success": "Customer receive dog success"} if customer_receive_dog_success else {"fail": "Customer fail to receive dog"}
                        status_code = status.HTTP_200_OK if customer_receive_dog_success else status.HTTP_400_BAD_REQUEST
                        return Response(response_data, status=status_code)
                elif service.main_status == "end" and not service.is_review: # รีวิวบริการ
                    if review:
                        review_success = service.review(review)
                        response_data = {"success": "Review service success"} if review_success else {"fail": "Can't review service"}
                        status_code = status.HTTP_200_OK if review_success else status.HTTP_400_BAD_REQUEST
                        return Response(response_data, status=status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for managing meal of service
    """

    permission_classes = [IsAuthenticated]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["meal_type", "meal_price_per_gram"]

    def create(self, request, *args, **kwargs):
        host_service_pk = self.kwargs.get("host_service_pk")
        host_service = HostService.objects.get(host=host_service_pk)
        serializer = AddMealSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        meal_id = serializer.data.get("meal")
        host_service.available_meals.add(Meal.objects.get(id=meal_id))
        host_service.save()
        return Response({"success": "Add meal success"}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        host_service_pk = self.kwargs.get("host_service_pk")
        meal_pk = self.kwargs.get("pk")
        host_service = HostService.objects.get(host=host_service_pk)
        host_service.available_meals.remove(Meal.objects.get(id=meal_pk))
        host_service.save()
        return Response({"success": "Remove meal success"}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        host_service_pk = self.kwargs.get("host_service_pk")
        queryset = Meal.objects.all()
        if host_service_pk:
            queryset = Meal.objects.filter(available_meals=host_service_pk)
        return queryset


class HostServiceViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint for managing host service
        - Only Host can access this viewset
        - Only Owner can access their own
    """

    permission_classes = [IsOwnerAndHost & IsAuthenticated]
    queryset = HostService.objects.all()
    serializer_class = HostServiceSerializer

    http_method_names = ["get", "put", "patch", "head", "options"]
    
    # def get_serializer_class(self):
    #     serializer_class=self.serializer_class
    #     parent_lookup=self.kwargs.get("add_meal")
    #     if parent_lookup:
    #         serializer_class=MealSerializer
    #     else:
    #         serializer_class=HostServiceSerializer
    #     return serializer_class

    # def get_serializer_class(self):
    #     serializer_class = self.serializer_class
    #     parent_lookup = self.kwargs.get("host_pk")
    #     if parent_lookup:
    #         serializer_class = HostAvailableDateWithNestedSerializer
    #     else:
    #         serializer_class = HostAvailableDateSerializer
    #     return serializer_class

    # @action(methods=["put"],detail=True ,url_path="addmeal",url_name="add_meal")
    # def add_meal(self,request,pk=None):
    #     pass
        # serializer=MealSerializer(data=request.data)

        # if serializer.is_valid():

        #     service_meal_id=serializer.data.get("id")

        #     meal=Meal.objects.get(id=service_meal_type)

        #     host_service=self.get_object()
        #     host_service.available_meals.clear()
        #     host_service.available_meals.add(meal)
        #     host_service.save()
                
        #     return Response(
        #             {"status": "success", "message": "add Meal Completed"},
        #             status=status.HTTP_200_OK,)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    

