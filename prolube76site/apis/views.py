from django.shortcuts import render
from apis.models import CustomersNewSQL01Model, VehiclesNewSQL01Model, RepairOrdersNewSQL01Model
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, FormView
from django.views.generic.edit import ModelFormMixin
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *

def index(request):
    render(request, 'index.html')

class CustomerListView(ListView):
    model = CustomersNewSQL01Model
    context_object_name = '76prolube-customer-list-view'
    paginate_by = 20  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add a current time into the context.
        context['now'] = timezone.now()
        number_of_actives = CustomersNewSQL01Model.objects.annotate(Count('customer_is_activate'))
        context['number_of_actives'] = number_of_actives
        return context

# using the Django formview
class CustomerCreateView(CreateView):
    model = CustomersNewSQL01Model
    fields = ['ustomer_id','customer_first_name','customer_last_name', 'customer_middle_name'
              'customer_does_allow_SMS',]


class CustomerDeleteView(DeleteView):
    model = CustomersNewSQL01Model
    success_url = reverse_lazy('/')

class CustomerUpdateView(UpdateView):
    model = CustomersNewSQL01Model
    fields = ['ustomer_id','customer_first_name','customer_last_name', 'customer_middle_name'
              'customer_does_allow_SMS',]
    template_name_suffix = '_updated_form'


# @api_view(['GET', 'POST'])
# def repairorders_list(request):
#     if request.method == 'GET':
#         data = RepairOrdersNewSQL01Model.objects.all()

#         serializer = StudentSerializer(data, context={'request': request}, many=True)

#         return Response(serializer.data)

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