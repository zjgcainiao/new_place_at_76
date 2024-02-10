from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
# from homepageapp.models import CustomersNewSQL01Model, VehiclesNewSQL01Model, RepairOrdersNewSQL01Model
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model, RepairOrdersNewSQL02Model, RepairOrderLineItemSquencesNewSQL02Model
from homepageapp.models import CustomerAddressesNewSQL02Model, CustomerEmailsNewSQL02Model, CustomerPhonesNewSQL02Model
from homepageapp.models import lineItemTaxesNewSQL02Model, LineItemsNewSQL02Model, RepairOrderLineItemSquencesNewSQL02Model
from homepageapp.models import NoteItemsNewSQL02Model
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import ListView, FormView, DetailView, TemplateView
from django.views.generic.edit import ModelFormMixin
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from dotenv import load_dotenv
import pyodbc
# from .serializers import EmailDataSerializer
import json
import os
from dashboard.forms import CustomerUpdateForm
import requests
from django.http import HttpResponse
# from .serializers import *

from django.db.models import Count
from django.core.paginator import Paginator
# from uuid import UUID
from django.utils import timezone
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.contrib import messages
from decouple import config, Csv


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

# dashboard-react app entrypoint html 2023-08-06


class GetReactAppView(TemplateView):
    template_name = 'homepageapp/13_react_app_portal.html'
    login_url = reverse_lazy('internal_users:internal_user_login')


class CustomerListView(ListView):
    model = CustomersNewSQL02Model

    context_object_name = 'customers'
    paginate_by = 4  # if pagination is desired
    template_name = 'homepageapp/01-customer-view-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add a current time into the context.
        context['current_time'] = timezone.now()
        number_of_actives = CustomersNewSQL02Model.objects.annotate(
            Count('customer_is_deleted'))
        context['number_of_actives'] = number_of_actives
        # console.log(f'the context transftered here is {context}' )
        context['form'] = CustomerUpdateForm()
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
    number_of_actives = CustomersNewSQL02Model.objects.annotate(
        Count('customer_is_deleted'))
    return render(request, 'homepageapp/01-customer-view-list-v2.html', {'customers': customers,
                                                                         'number_of_actives': number_of_actives,
                                                                         'current_time': current_time, })
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




def verify_stripe_applepay(request):
    cloud_url = 'https://storage.googleapis.com/vin-doctor.appspot.com/stripe/apple-developer-merchantid-domain-association'

    try:
        response = requests.get(cloud_url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        # Handle any exceptions that occur during the HTTP request
        return HttpResponse(str(e), status=500)

    return HttpResponse(response.content, content_type='text/plain')