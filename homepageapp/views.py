from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
# from homepageapp.models import CustomersNewSQL01Model, VehiclesNewSQL01Model, RepairOrdersNewSQL01Model
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model, RepairOrdersNewSQL02Model,RepairOrderLineItemSquencesNewSQL02Model
from homepageapp.models import CustomerAddressesNewSQL02Model, CustomerEmailsNewSQL02Model, CustomerPhonesNewSQL02Model
from homepageapp.models import lineItemTaxesNewSQL02Model,LineItemsNewSQL02Model, RepairOrderLineItemSquencesNewSQL02Model
from homepageapp.models import NoteItemsNewSQL02Model
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import ListView, FormView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
# from .serializers import EmailDataSerializer
import json
import os
# from .serializers import *
from homepageapp.forms import CustomerModelForm, VehicleModelForm, RepairOrderLineItemModelForm #, RepairOrderModelForm
from django.db.models import Count
from django.core.paginator import Paginator
# from uuid import UUID
from django.utils import timezone
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.contrib import messages

def GetHomepageView(request):
    # the list of icons corresponding to the services provided by the shop. Reduce code redundancy
    service_icons = [
            {
                'img_src': 'homepageapp/img/svgs/car-maintenance-icon.svg',
                'alt': 'car car-maintenance-oil-change',
                'title': 'Oil Changes',
            },
            {
                'img_src': 'homepageapp/img/svgs/air-conditioning-icon.svg',
                'alt': 'a/c-system-diagnosis-and-repair',
                'title': 'Air Conditioning Not Cooling & Heating',
            },
            {
                'img_src': 'homepageapp/img/svgs/engine-icon.svg',
                'alt': 'engine',
                'title': 'Engine Repair (w/ service lights on, overheating, etc)',
            },
            {
                'img_src': 'homepageapp/img/svgs/battery-svgrepo-com-icon.svg',
                'alt': 'Family MPV',
                'title': 'Car Battery Service',
            },
            {
                'img_src': 'homepageapp/img/svgs/electrical-service-icon.svg',
                'alt': 'Compact',
                'title': 'Electric Diangosis',
            },
            {
                'img_src': 'homepageapp/img/svgs/brake-icon.svg',
                'alt': 'Convertible',
                'title': 'Brake Replacements',
            },
            {
                'img_src': 'homepageapp/img/svgs/spark-spark-plug-svgrepo-com-icon.svg',
                'alt': 'spark-plug',
                'title': 'Spark Plugs',
            },
            {
                'img_src': 'homepageapp/img/svgs/gear-shift-stick-svgrepo-com-icon.svg',
                'alt': 'transmission',
                'title': 'Transmission Service',
            },
            {
                'img_src': 'homepageapp/img/svgs/windshield-icon.svg',
                'alt': 'Windshield-Wipers',
                'title': 'Windshield Wiper',
            },
            {
                'img_src': 'homepageapp/img/svgs/suspension-icon.svg',
                'alt': 'suspension',
                'title': 'Suspension Service',
            },
        ]
    return render(request, 'homepageapp/20_homepageapp_home.html', {'service_icons': service_icons})

def GetServiceListView(request):
    return render(request, 'homepageapp/21_homepageapp_service_list.html')

def GetAboutUsView(request):
    # return render(request, 'homepageapp/20_homepageapp_home_v2.html')
    return render(request, 'homepageapp/22_homepageapp_about_us.html')

# this is the class-based list view 
class CustomerListView(ListView):
    model = CustomersNewSQL02Model

    context_object_name = 'customers'
    paginate_by = 4  # if pagination is desired
    template_name = 'homepageapp/01-customer-view-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add a current time into the context.
        context['current_time'] = timezone.now()
        number_of_actives = CustomersNewSQL02Model.objects.annotate(Count('customer_is_deleted'))
        context['number_of_actives'] = number_of_actives
        # console.log(f'the context transftered here is {context}' )
        context['form'] = CustomerModelForm()
        # Create any data and add it to the context
        context['addl'] = 'This is just some data'
        return context

    def get_queryset(self):
        return CustomersNewSQL02Model.objects.order_by('-customer_id')

# -------------2023-03-15--------
# GPT 3.5 generated
# display data on 01-customer-view-list-v2.html
# version 2
def customer_list(request):
    customers = CustomersNewSQL02Model.objects.all()
    current_time = timezone.now()
    number_of_actives = CustomersNewSQL02Model.objects.annotate(Count('customer_is_deleted'))
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
    active_customers = CustomersNewSQL02Model.objects.filter(customer_is_deleted = False)
    paginator = Paginator(active_customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'homepageapp/01-customer-view-list-v3.html', {'page_obj': page_obj})


# createView
class CustomerCreateView(CreateView):
    model = CustomersNewSQL02Model
    fields = ['customer_first_name','customer_last_name', 'customer_middle_name',
              'customer_does_allow_SMS',]
    success_url = reverse_lazy('homepageapp:customers-list-v3')
    template_name = 'homepageapp/02-customer-creation.html'
    
    # ---- 2023-03-27-------
    # encounter Conversion failed when converting from a character string to uniqueidentifier.
    # ChatGPT 4.0
    # ----------------------
    def form_valid(self, form):
        # Generate a new UUID for the customer_id field. customer_new_uid_v01 -- newly added uuid
        # form.instance.customer_new_uid_v01 = uuid.uuid4()
        # Get the current maximum value of the customer_id field. customer_id is the legacy id used in old DB.
        max_customer_id = CustomersNewSQL02Model.objects.aggregate(Max('customer_id'))['customer_id__max']
        # Increment the max value by 1 to get the new customer_id value
        new_customer_id = max_customer_id + 1 if max_customer_id is not None else 1
        # Set the customer_id value for the new record and save it
        form.instance.customer_id = new_customer_id
        return super().form_valid(form)    
 
class CustomerDetailView(DetailView):
    model = CustomersNewSQL02Model
    success_url = reverse_lazy('customers-list-v3')
    context_object_name = 'customer'
    template_name = 'homepageapp/03-customer-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CustomerModelForm(self.request.POST, instance=self.object)
        else:
            context['form'] = CustomerModelForm(instance=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomerModelForm(request.POST, instance=self.object)
        if form.is_valid():
            self.object.customer_last_updated_date = timezone.now()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CustomerUpdateView(UpdateView):
    model = CustomersNewSQL02Model
    success_url = reverse_lazy('homepageapp:customer-detail')
    form_class = CustomerModelForm
    template_name = 'homepageapp/03-customer-update.html'


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomerModelForm(request.POST, instance=self.object)
        if form.is_valid():
            self.object.customer_last_updated_date = timezone.now()
            form.save()
            messages.success(request, 'Update success.')
            return redirect('homepageapp:customer-detail', pk=self.object.customer_id)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class CustomerDeleteView(DeleteView):
    model = CustomersNewSQL02Model
    # success_url = reverse_lazy('/')



# 
class RepairOrderListView(ListView):
    # model = RepairOrdersNewSQL02Model

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
        context['addl'] = 'comments about repairorders list view'
        return context

    def get_queryset(self):
        return RepairOrdersNewSQL02Model.objects.order_by('-repair_order_id')

class EmailDataView(APIView):
    def post(self, request):

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'fixtures/Email_20230115.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
            serializer = EmailDataSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({'status': 'success'})
    

