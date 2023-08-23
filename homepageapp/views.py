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
# from .serializers import *
# , RepairOrderModelForm
from homepageapp.forms import CustomerModelForm, VehicleModelForm, RepairOrderLineItemModelForm
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
    number_of_actives = CustomersNewSQL02Model.objects.annotate(
        Count('customer_is_deleted'))
    return render(request, 'homepageapp/01-customer-view-list-v2.html', {'customers': customers,
                                                                         'number_of_actives': number_of_actives,
                                                                         'current_time': current_time, })

# -------------------------------
# ------2023-03-26---------------
# GPT 4.0 generated
# display data on 01-customer-view-list-v3.html


def active_customer_list(request):
    # customer_is_activate=False means that a customer is not deactivated. the name of this field is confusing. will
    # need to revise it before PROD launch.
    active_customers = CustomersNewSQL02Model.objects.filter(
        customer_is_deleted=False)
    paginator = Paginator(active_customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'homepageapp/01-customer-view-list-v3.html', {'page_obj': page_obj})


# createView
class CustomerCreateView(CreateView):
    model = CustomersNewSQL02Model
    fields = ['customer_first_name', 'customer_last_name', 'customer_middle_name',
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
        max_customer_id = CustomersNewSQL02Model.objects.aggregate(Max('customer_id'))[
            'customer_id__max']
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
            context['form'] = CustomerModelForm(
                self.request.POST, instance=self.object)
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


# try to list all repair ordes 2022-11-05
# model repairOrder
def all_repair_orders(request):
    # load the environment
    try:
        server = config("DB_SERVER")
    except KeyError as e:
        raise RuntimeError(
            "Erro. Could not find any database server information. Make sure server info is available in the environemnt") from e

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    databaseName = os.getenv("DB_HOST")
    # how to use pymssql, visit https://pymssql.readthedocs.io/en/stable/ref/pymssql.html#module-level-symbols
    # pymssql.connect(server='.', user=None, password=None, database='', timeout=0, login_timeout=60, charset='UTF-8', as_dict=False, host='', appname=None, port='1433', conn_properties=None, autocommit=False, tds_version=None)
    conn = pyodbc.connect(server, user, password, databaseName)
    c1 = conn.cursor()
    c1.execute("""
        SELECT TOP (50) 
       a.[RepairOrderId]
      -- ,a.[RepairOrderPhaseId]
      ,f.[Phase] as ' Repair Order Phase'
      ,concat(b.[FirstName], ' ', b.[LastName]) as 'Customer Name'
      ,b.[LastVisited]
      ,b.[FirstVisited]
      ,b.[NewCustFollowUpDate]
      ,[TimeIn] as 'Repair Order TimeIn'
      ,[TimeOut] as 'Repair Order TimeOut'
      ,[DatePosted] as 'Repair Order Posted Date'
      ,[OdometerIn]
      ,[OdometerOut]
      ,[StatusDescription]
      ,[ScheduleDate]
      ,[ScheduledHours]
      ,[PromiseDate]
      ,[ReasonForVisitId]    
      ,[Location]
      ,a.[CustId]
      ,a.[VehicleId]
      ,c.year 'manuf year'
      ,c.[Vin]
      ,c.[License]
      ,c.[LicenseState]
      ,c.EngineId
      ,d.[NumberOfCylinders]
      ,d.[ValvesPerCylinder]
      ,d.[FuelDeliveryMethodType]
      ,c.[MakeId]
      ,c.[SubModelId]
      ,e.[Name] as 'model Name'
      ,[CategoryId]
      ,[RoPrinted]
      ,[InvoicePrinted]
      ,a.[LastChangeDate]
      ,a.[AppointmentRequestUid]
      ,a.[Notes]
      ,a.[OrderTotal]
      ,a.[ShopSuppliesAmt]
      ,a.[TotalTaxAmt]
      ,a.[LaborSale]
      ,a.[PartsSale]
      ,a.[DiscountAmt]
      ,a.[Observations]
      ,a.[CreatedAsEstimate]
      ,[TaxAmtHazMat]
      ,[TaxAmtShopSupplies]
      ,[PrintedDate]
      ,[PartDiscountDescriptionId]
      ,a.[TaxExempt]
      ,[LaborRateDescriptionId]
      ,[RateVersionDate]
      ,[FromQuickEst]
      ,[HazWasteAmt]
      ,[BalanceDueAdjustment]
      ,a.[timestamp]
      ,[MarginPct]
      ,[TireFeeSale]
      ,a.[EngineHoursIn]
      ,a.[EngineHoursOut]
      ,a.[RecordVersion]
  FROM [ShopMgt].[SM].[RepairOrder] as a
  left join [ShopMgt].[SM].[Customers] as b  on a.[CustId]=b.[custID]
  left join  [ShopMgt].[SM].[Vehicle] as c on c.[VehicleId]=a.[vehicleID]
  left join [ShopMgt].[DMV].[Engine] as d on d.EngineId=c.[engineid]
  left join  [ShopMgt].[SM].[RepairOrderPhase] as f on f.[RepairOrderPhaseId]=a.[RepairOrderPhaseId]
  left join [ShopMgt].[DMV].[Make] as e on e.MakeId=c.MakeId
  where f.[Phase] not in ('DELETED')
  order by [TimeIn] desc
    """)
    all_repair_orders = []
    data = c1.fetchall()

    for row in data:
        repair_id = row[0]    # repair ID
        # getting the customer name. column number may change due to the sql script
        customer_name = row[2]
        # get the status of the repair order; EST/RO/INV/DELETED/SCHEDULED
        repair_status = row[1]
        vin = row[20]         # vin number
        make = row[29]         # make of the vehicle
        time_out = row[7]      # repair_order_time_out
        last_visit_date = row[2]  # last date visted
        vehicle_year = row[19]    # vehicle year
        repair_total_amount = row[36]  # total repair amount
        RO = {'repair_id': repair_id, 'repair_status': repair_status, 'time_out': time_out, 'repair_total_amount': repair_total_amount,
              'customer_name': customer_name, 'make': make, 'vehicle_year': vehicle_year, 'vin': vin, 'last_visit_date': last_visit_date}

        all_repair_orders.append(RO)
    return render(request, 'polls/repair_order_dashboard.html', {'all_repair_orders': all_repair_orders})
