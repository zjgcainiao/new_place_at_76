from django.conf import settings
from django.views.decorators.http import require_http_methods
import logging
import requests
import json
import os
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import status
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model, RepairOrdersNewSQL02Model, LineItemsNewSQL02Model, TextMessagesModel, VinNhtsaApiSnapshots, LicensePlateSnapShotsPlate2Vin
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from internal_users.models import InternalUser
from internal_users.internal_user_auth_backend import InternalUserBackend
from apis.serializers import CustomerSerializer,LineItemsSerializer, TextMessagesSerializer,AddressSerializer, PhoneSerializer, EmailSerializer, CustomerSerializer, RepairOrderSerializer, PaymentSerializer, LastestVinDataSerializer, PlateAndVinDataSerializer
from homepageapp.models import VinNhtsaApiSnapshots
from core_operations.models import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE
from django.core.exceptions import ObjectDoesNotExist
from core_operations.constants import POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apis.user_permissions import IsInternalUser
from rest_framework.permissions import IsAuthenticated


# added on 2023-11-06
class WIPDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsInternalUser]
    serializer_class = RepairOrderSerializer

    def get_queryset(self):
        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.

        qs = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_phase__gte=1,
            repair_order_phase__lte=5
        ).select_related(
            'repair_order_customer', 'repair_order_vehicle',
        ).prefetch_related('repair_order_customer__addresses',
                           'repair_order_customer__phones',
                           'repair_order_customer__emails',
                           'repair_order_customer__taxes',
                           'payment_repairorders',
                           'repair_order_customer__payment_customers',
                           )

        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use pagination if it's set up in the settings
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If pagination is not set or not needed, serialize the queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def current_time(self, request):
        return Response({'current_time': CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE})


class LastestVinDataViewSet(viewsets.ModelViewSet):
    serializer_class = LastestVinDataSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]

    def get_queryset(self):
        # Your queryset logic here...
        return VinNhtsaApiSnapshots.objects.all().select_related('variable')

## this one returns api data based on POPULAR_NHTSA_VARIABLE_IDS
class VinNhtsaApiSnapshotViewSet(viewsets.ModelViewSet):
    serializer_class = LastestVinDataSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]

    def get_queryset(self):
        # List of variable IDs to filter. imported from core_operations.constants
        variable_ids_list = POPULAR_NHTSA_VARIABLE_IDS
        # vin = self.kwargs.get('vin')
        vin = self.request.query_params.get('vin')
        # print(f'fetched vin number is {vin}')

        if vin:
            qs = VinNhtsaApiSnapshots.objects.filter(
                vin=vin,
                version=5,
                variable__in=variable_ids_list,
            ).order_by('-created_at', 'variable')

            # Sort based on the order of variable_ids_list
            sorted_qs = sorted(
                qs, key=lambda x: variable_ids_list.index(x.variable))
            return sorted_qs
        else:
            return VinNhtsaApiSnapshots.objects.none()

    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return Response({"Error": "VIN not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


class PlateAndVinDataViewSet(viewsets.ModelViewSet):
    queryset = LicensePlateSnapShotsPlate2Vin.objects.all()
    serializer_class = PlateAndVinDataSerializer
    # permission_classes = [IsAuthenticated, IsInternalUser]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = super().get_queryset()
        vin = self.request.query_params.get('vin', None)
        if vin:
            queryset = queryset.filter(vin=vin)
        return queryset

    def create(self, request, *args, **kwargs):
        # Custom logic for creating a new instance
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # Custom logic for updating an existing instance
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Custom logic for deleting an instance
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Add any other methods you need (e.g., partial_update, retrieve, etc.)

    # Optionally override perform_create, perform_update, perform_destroy if needed


class ActiveRepairOrderViewSet(viewsets.ModelViewSet):
    serializer_class = RepairOrderSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]

    def get_queryset(self):
        qs = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_phase__gte=1, repair_order_phase__lte=5)
        qs = qs.prefetch_related('repair_order_customer',
                                 'repair_order_customer__addresses',
                                 'repair_order_customer__addresses',
                                 'repair_order_customer__phones',
                                 'repair_order_customer__emails',
                                 'repair_order_customer__taxes',
                                 'payment_repairorders',
                                 'repair_order_customer__payment_customers'
                                 )
        return qs


class LineItemsViewSet(viewsets.ModelViewSet):

    serializer_class = LineItemsSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]

    def get_queryset(self):
        return LineItemsNewSQL02Model.objects.prefetch_related(
            'lineitems__lineitem_noteitem',
            'lineitems__lineitem_laboritem',
            'lineitems__parts_lineitems')

# get the most recent 10 text messages


class TextMessagesViewSet(viewsets.ModelViewSet):

    serializer_class = TextMessagesSerializer

    def get_queryset(self):
        return TextMessagesModel.objects.filter(text_customer=self.kwargs['customer_id']).order_by('-text_message_id')[:10]


@api_view(['GET'])
def get_active_customers_api(request):
    # try:
    customers = CustomersNewSQL02Model.objects.filter(
        customer_is_deleted=False)
    # page = request.GET.get('page', 1)
    # paginator = Paginator(customers, 20)
    serializer = CustomerSerializer(customers, many=True)
    return JsonResponse({'customers': serializer.data})
    # return Response(serialized_customers.data)

    # formatted_data = {
    #     'data': serializer.data
    # }
    # return Response(formatted_data)

    # except PageNotAnInteger:
    #     return Response({'error': 'Invalid page number.'}, status=status.HTTP_400_BAD_REQUEST)
    # except EmptyPage:
    #     return Response({'error': 'Page out of range.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_active_repairorders_api(request):
    if request.method == 'GET':
        # repairorders = RepairOrdersNewSQL02Model.objects.all()
        repairorders = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_phase__gte=1, repair_order_phase__lte=5)
        repairorders = repairorders.select_related('repair_order_customer'
                                                   ).prefetch_related('repair_order_customer__addresses',
                                                                      'repair_order_customer__addresses',
                                                                      'repair_order_customer__phones',
                                                                      'repair_order_customer__emails',
                                                                      'repair_order_customer__taxes'
                                                                      )
        repairorders = repairorders.prefetch_related('payment_repairorders',
                                                     'repair_order_customer__payment_customers')
        serializer = RepairOrderSerializer(
            repairorders, context={'request': request}, many=True)

        return JsonResponse({'repairorders': serializer.data})

#     elif request.method == 'POST':
#         serializer = RepairOrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT', 'DELETE'])
# def repairorders_detail(request, pk):
#     try:
#         student = Student.objects.get(pk=pk)
#     except Student.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = RepairOrderSerializer(student, data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         student.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# 2023-08-04 this is the Login API that was created to respond to react app dashboard_react
# dashboard_react is designed to


@csrf_exempt
@require_POST
def api_internal_user_login(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')

    user = InternalUserBackend().authenticate(
        request, email=email, password=password)

    if user is not None:
        login(request, user,
              backend='internal_users.internal_user_auth_backend.InternalUserBackend')

        return JsonResponse({
            'email': user.email,
            # 'user': user,
            # user.groups.filter(name='Technicians').exists(),
            'is_technician': False,  # True,
            'is_authenticated_user': user.is_authenticated,
            'is_internal_user': isinstance(user, InternalUser),
        })
    else:
        # Unauthorized sattus code.
        return JsonResponse({'error': 'Invalid login details.'}, status=401)


@csrf_exempt  # Disable CSRF token for this view
@require_http_methods(["POST"])  # Only allow POST requests to this endpoint
def openai_proxy(request):
    # Extract the data from the incoming POST request
    data = request.POST or request.data
    headers = {
        'Authorization': f'Bearer {settings.OPENAI_API_KEY2}',
        'Content-Type': 'application/json',
    }

    try:
        # Forward the request to OpenAI API
        response = requests.post(
            'https://api.openai.com/v1/engines/davinci-codex/completions',
            json=data,
            headers=headers
        )
        response.raise_for_status()
        # Return the response from OpenAI API
        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request to OpenAI API
        return JsonResponse({'error': str(e)}, status=502)  # Proxy Error
