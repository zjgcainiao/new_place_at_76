from django.shortcuts import render
from django.urls import reverse_lazy
from homepageapp.models import CustomersNewSQL01Model, VehiclesNewSQL01Model, RepairOrdersNewSQL01Model
#, RepairOrdersNewSQL01Model
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, FormView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# from .serializers import *
from .forms import CustomerModelForm, VehicleModelForm #, RepairOrderModelForm
from django.db.models import Count
from django.core.paginator import Paginator
from uuid import UUID
import uuid
from django.db.models import Max
from django.http import HttpResponseRedirect


def GetHomepageView(request):
    return render(request, 'homepageapp/homepageapp-home.html')

# this is the class-based list view 
class CustomerListView(ListView):
    model = CustomersNewSQL01Model

    context_object_name = 'customers'
    paginate_by = 4  # if pagination is desired
    template_name = 'homepageapp/01-customer-view-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add a current time into the context.
        context['current_time'] = timezone.now()
        number_of_actives = CustomersNewSQL01Model.objects.annotate(Count('customer_is_deleted'))
        context['number_of_actives'] = number_of_actives
        # console.log(f'the context transftered here is {context}' )
        context['form'] = CustomerModelForm()
        # Create any data and add it to the context
        context['addl'] = 'This is just some data'
        return context

    def get_queryset(self):
        return CustomersNewSQL01Model.objects.order_by('-customer_id')

# -------------2023-03-15--------
# GPT 3.5 generated
# display data on 01-customer-view-list-v2.html
def customer_list(request):
    customers = CustomersNewSQL01Model.objects.all()
    current_time = timezone.now()
    number_of_actives = CustomersNewSQL01Model.objects.annotate(Count('customer_is_activate'))
    return render(request, 'homepageapp/01-customer-view-list-v2.html', {'customers': customers,
                                                                         'number_of_actives':number_of_actives,
                                                                         'current_time':current_time,})

# -------------------------------
# ------2023-03-26---------------
# GPT 4.0 generated
# display data on 01-customer-view-list-v3.html

def active_customer_list(request):
    # customer_is_activate=False means that a customer is not deactivated. the name of this field is confusing. will 
    # need to revise it before PROD launch.
    active_customers = CustomersNewSQL01Model.objects.filter(customer_is_deleted = False)
    paginator = Paginator(active_customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'homepageapp/01-customer-view-list-v3.html', {'page_obj': page_obj})


# createView
class CustomerCreateView(CreateView):
    model = CustomersNewSQL01Model
    fields = ['customer_first_name','customer_last_name', 'customer_middle_name',
              'customer_does_allow_SMS',]
    success_url = reverse_lazy('customers-list-v3')
    template_name = 'homepageapp/02-customer-creation.html'
    
    # ---- 2023-03-27-------
    # encounter Conversion failed when converting from a character string to uniqueidentifier.
    # ChatGPT 4.0
    # ----------------------
    def form_valid(self, form):

        # Generate a new UUID for the customer_id field. customer_new_uid_v01 -- newly added uuid
        form.instance.customer_new_uid_v01 = uuid.uuid4()
        # Get the current maximum value of the customer_id field. customer_id is the legacy id used in old DB.
        max_customer_id = CustomersNewSQL01Model.objects.aggregate(Max('customer_id'))['customer_id__max']
        # Increment the max value by 1 to get the new customer_id value
        new_customer_id = max_customer_id + 1 if max_customer_id is not None else 1
        # Set the customer_id value for the new record and save it
        form.instance.customer_id = new_customer_id
        return super().form_valid(form)    
 
class CustomerDetailView(DetailView):
    model = CustomersNewSQL01Model
    success_url = reverse_lazy('customer-detail')
    template_name = 'homepageapp/03-customer-detail-update.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CustomerModelForm(self.request.POST, instance = self.object)
        else:
            context['form'] = CustomerModelForm(instance=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomerModelForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CustomerUpdateView(UpdateView):
    model = CustomersNewSQL01Model
    fields = ['customer_first_name','customer_last_name', 'customer_middle_name',
              'customer_does_allow_SMS',]
    success_url = reverse_lazy('customers-list-v3')
    template_name = 'homepageapp/03-customer-details-update.html'

class CustomerDeleteView(DeleteView):
    model = CustomersNewSQL01Model
    # success_url = reverse_lazy('/')


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

# 
class RepairOrderListView(ListView):
    model = RepairOrdersNewSQL01Model

    context_object_name = 'repairorders'
    paginate_by = 4  # if pagination is desired
    template_name = 'homepageapp/51-repair-order-view-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add a current time into the context.
        context['current_time'] = timezone.now()
        # number_of_actives = CustomersNewSQL01Model.objects.annotate(Count('customer_is_deleted'))
        # context['number_of_actives'] = number_of_actives
        # console.log(f'the context transftered here is {context}' )
        # context['form'] = CustomerModelForm()
        # Create any data and add it to the context
        context['addl'] = 'comments about repairordersNewSQL01Model'
        return context

    def get_queryset(self):
        return RepairOrdersNewSQL01Model.objects.order_by('-repair_order_id')