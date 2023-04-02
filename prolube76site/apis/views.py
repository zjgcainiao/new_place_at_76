from django.shortcuts import render
# from apis.models import CustomersNewSQL01Moxwxdel, VehiclesNewSQL01Model, RepairOrdersNewSQL01Model
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, FormView
from django.views.generic.edit import ModelFormMixin
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from homepageapp.models import CustomersNewSQL01Model, VehiclesNewSQL01Model, RepairOrdersNewSQL01Model
from .serializers import CustomerSerializer, RepairOrderSerializer
from django.core.paginator import Paginator
from django.http import JsonResponse


@api_view(['GET'])
def customer_api(request):
    # try:
        customers = CustomersNewSQL01Model.objects.all()
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


# def index(request):
#     render(request, 'index.html')


# # using the Django formview
# class CustomerCreateView(CreateView):
#     model = CustomersNewSQL01Model
#     fields = ['ustomer_id','customer_first_name','customer_last_name', 'customer_middle_name'
#               'customer_does_allow_SMS',]


# class CustomerDeleteView(DeleteView):
#     model = CustomersNewSQL01Model
#     success_url = reverse_lazy('/')

# class CustomerUpdateView(UpdateView):
#     model = CustomersNewSQL01Model
#     fields = ['ustomer_id','customer_first_name','customer_last_name', 'customer_middle_name'
#               'customer_does_allow_SMS',]
#     template_name_suffix = '_updated_form'


@api_view(['GET'])
def repairorders_api(request):
    if request.method == 'GET':
        repairorders = RepairOrdersNewSQL01Model.objects.all()

        serializer = RepairOrderSerializer(repairorders, context={'request': request}, many=True)

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