import logging
import aiohttp
import asyncio
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import status
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model, RepairOrdersNewSQL02Model, LineItemsNewSQL02Model, TextMessagesModel, VinNhtsaApiSnapshots
from apis.serializers import CustomerSerializer, RepairOrderSerializer
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
import json
from apis.serializers import LineItemsSerializer, TextMessagesSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from internal_users.models import InternalUser
from internal_users.internal_user_auth_backend import InternalUserBackend
from apis.serializers import AddressSerializer, PhoneSerializer, EmailSerializer, CustomerSerializer, RepairOrderSerializer, PaymentSerializer, LastestVinDataSerializer
from homepageapp.models import VinNhtsaApiSnapshots


from django.core.exceptions import ObjectDoesNotExist
from core_operations.constants import POPULAR_NHTSA_VARIABLE_IDS


class LastestVinDataViewSet(viewsets.ModelViewSet):
    serializer_class = LastestVinDataSerializer

    def get_queryset(self):
        # Your queryset logic here...
        return VinNhtsaApiSnapshots.objects.all().prefetch_related('nhtsa_variable_ids')


class VinNhtsaApiSnapshotViewSet(viewsets.ModelViewSet):
    serializer_class = LastestVinDataSerializer

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


class ActiveRepairOrderViewSet(viewsets.ModelViewSet):
    serializer_class = RepairOrderSerializer

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


# async def fetch_single_vin_from_nhtsa_api(vin, vehicle_year=None):
#     # url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json&modelyear={vehicle_year}"
#     if vehicle_year:
#         url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json&modelyear={vehicle_year}"
#     else:
#         url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.json()
