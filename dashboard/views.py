
# 2023-04-02 created to display the index page of the main workstation page.
# representing a modern version of old mitchell1 dashboard
# WIP, search, etc.
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView,  DeleteView
from django.db.models import Q, Prefetch
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from homepageapp.models import RepairOrdersNewSQL02Model, CustomerAddressesNewSQL02Model, CustomersNewSQL02Model, AddressesNewSQL02Model, CustomerEmailsNewSQL02Model, RepairOrderLineItemSquencesNewSQL02Model, PartItemModel, LineItemsNewSQL02Model
from homepageapp.models import VehiclesNewSQL02Model, EmailsNewSQL02Model, CustomerPhonesNewSQL02Model, PhonesNewSQL02Model, VehicleNotesModel, LicensePlateSnapShotsPlate2Vin
# from homepageapp.forms import RepairOrderModelForm, CustomerModelForm, AddressModelForm, RepairOrderLineItemModelForm, PartItemModelForm, LaborItemModelForm
from dashboard.forms import PartItemInlineFormSet, LaborItemInlineFormSet
from django.forms.models import inlineformset_factory, modelformset_factory
from datetime import datetime, timedelta
from django.contrib import messages
from homepageapp.models import TextMessagesModel, VinNhtsaApiSnapshots
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from internal_users.models import InternalUser
from appointments.models import AppointmentRequest
from dashboard.forms import SearchForm, CustomerUpdateForm, RepairOrderUpdateForm, VehicleUpdateForm, AddressUpdateForm, LineItemUpdateForm, PartItemUpdateForm, LaborItemUpdateForm, VehicleCreateForm
from dashboard.forms import LiteEmailUpdateForm, CustomerCreateForm, CustomerEmailForm, CustomerAddressForm, VINSearchForm, LicensePlateSearchForm
# from dashboard.forms import LiteCustomerVehicleUpdateFormset
from django.core.paginator import Paginator
from django.db.models import Max
from django.views.generic import TemplateView
from core_operations.constants import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, LIST_OF_STATES_IN_US
# You can do the same sort of thing manually by testing on request.user.is_authenticated, but the decorator is much more convenient!
from internal_users.mixins import InternalUserRequiredMixin
from django.core.serializers import serialize
from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api, fetch_single_plate_data_via_plate2vin_api
from django.db import models
from asgiref.sync import sync_to_async
from dashboard.async_functions import fetch_latest_vin_data_from_snapshots, database_sync_to_async
from apis.api_vendor_urls import NHTSA_API_URL, PLATE2VIN_API_URL
import logging
import requests
import json
from decouple import config, UndefinedValueError, Csv
from django.db.models.query import QuerySet


LiteVehicleUpdateFormset = inlineformset_factory(
    CustomersNewSQL02Model, VehiclesNewSQL02Model, edit_only=True,
    fields=('vehicle_id', 'VIN_number', 'vehicle_license_plate_nbr', 'vehicle_license_state'), fk_name='vehicle_cust')

# 2023-09-17 list all dashboards available


def get_main_dashboard(request):
    # Create the context with the current time.
    context = {
        'current_time': CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE,
    }

    if request.user.is_authenticated:
        if isinstance(request.user, InternalUser):
            return render(request, 'dashboard/10_main_dashboard.html', context)
        else:
            # Handle what happens if the user is of type InternalUser
            return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        # Handle what happens if the user is of type InternalUser
        return HttpResponseForbidden("you don't have permission to access to this page.")

# dashboard listview via function. Version 1
def get_repair_order_dash(request):
    repair_orders = RepairOrdersNewSQL02Model.objects.filter(
        repair_order_phase__gte=1, repair_order_phase__lte=5).prefetch_related('repair_order_customer')
    # repair_orders_v2 = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer_id', 'repair_order_customer_id__addresses').filter(repair_order_phase_id__in=[1,2,3,4,5])
    customer_addresses = AddressesNewSQL02Model.objects.prefetch_related(
        'addresses')
    # the alternative way to grab repair orders, as well as the address information
    # __gte means great than or equal; __lte means less than equal
    all_in_one_set = RepairOrdersNewSQL02Model.objects.filter(
        repair_order_phase__gte=1, repair_order_phase__lte=5).prefetch_related('repair_order_customer__addresses')
    context = {
        'repair_orders': repair_orders,
        'customer_addresses': customer_addresses,
        'all_in_one_set': all_in_one_set,
        'current_time': CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE,
    }
    return render(request, 'dashboard/11_repair_order_dash.html', context)

# using listview to display the dashboarrd. version 2, dashboard list view.


class WIPDashboardView(InternalUserRequiredMixin, ListView):
    model = RepairOrdersNewSQL02Model
    context_object_name = 'repair_orders'
    template_name = 'dashboard/12_repair_order_dash_v2.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not isinstance(request.user, InternalUser):
                messages.error("you are not permitted to view this page.")
                return redirect('homepageapp:homepage')
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            messages.error("you have to login first.")
            return redirect('internal_users:internal_user_login')

    def get_queryset(self):
        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.
        # qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE
        return context

# dashboard detail view. version 1
# modified to prefetch emails, phones, taxes to each repair_order_customer object


@login_required(login_url='internal_users:internal_user_login')
def dashboard_detail_v1(request, pk):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__addresses'),
        'repair_order_customer__phones',
        'repair_order_customer__emails',
        'repair_order_customer__taxes',
        'lineitems__lineitem_noteitem',
        'repair_order_vehicle',
    ).get(pk=pk)
    # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    repair_order_id = repair_order.repair_order_id
    customer_id = repair_order.repair_order_customer.customer_id
    vehicle = repair_order.repair_order_vehicle

    line_items = repair_order.lineitems.all()

    text_messages = TextMessagesModel.objects.filter(
        text_customer=customer_id).order_by('-text_message_id')[:10]

    # send out a repair_order_id stored in the request.session.
    request.session['repair_order_id'] = repair_order_id
    # request.session['customer_id'] = customer_id

    if request.method == 'POST':
        # Process form data and save the changes
        form = RepairOrderUpdateForm(request.POST, instance=repair_order)
        if form.is_valid():
            form.save()
            messages.success('redirecting...')
            return redirect('dashboard:repair-order-dash')
    else:
        # Display the form for updating the record
        form = RepairOrderUpdateForm(instance=repair_order)

    context = {
        'repair_order': repair_order,
        'form': form,
        'repair_order_id': repair_order_id,
        'customer_id': customer_id,
        'line_items': line_items,
        'vehicle': vehicle,
        'current_time': CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE,
        'text_messages': text_messages,

    }
    return render(request, 'dashboard/21_dashboard_detail.html', context)

# dashboard detail view. Version 2


@login_required(login_url='internal_users:internal_user_login')
def dashboard_detail_v2(request, pk):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        'repair_order_customer__addresses',
        'repair_order_customer__phones',
        'repair_order_customer__emails',
        'repair_order_customer__taxes',
        # 'repair_order_customer__vehicle_customers',
    ).get(pk=pk)
    # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    repair_order_customer = repair_order.repair_order_customer
    customer_address = repair_order_customer.addresses.first()

    repair_order_form = RepairOrderUpdateForm(instance=repair_order)
    customer_form = CustomerUpdateForm(instance=repair_order_customer)
    address_form = AddressUpdateForm(instance=customer_address)

    #  'dashboard/22_dashboard_detail_v2.html'
    return render(request, 'dashboard/24_dashboard_update_as_whole_via_inlineform.html', {
        'repair_order': repair_order,
        'repair_order_form': repair_order_form,
        'customer_form': customer_form,
        'address_form': address_form,
    })


# dashboard detail view. based on the DetailView model. version 3
class DashboardDetailView(DetailView, LoginRequiredMixin):
    template_name = 'dashboard/23_dashboard_detail_v3.html'
    login_url = reverse_lazy('internal_users:internal_user_login')
    # making sure the context_object_name is repair_order so that repair_order can be used in the template html.
    context_object_name = 'repair_order'
    # slug_field = 'isbn'
    # slug_url_kwarg = 'isbn'
    # model = RepairOrdersNewSQL02Model

    # whenever visiting a repair order, update the `repair_order_last_updated_at``
    # def get_object(self):
    #         obj = super().get_object()
    #         # Record the last accessed date
    #         obj.repair_order_last_updated_at = timezone.now()
    #         obj.save()
    #         return obj
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not isinstance(request.user, InternalUser):
                return self.handle_no_permission()
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch(
            'repair_order_customer__addresses')).filter(repair_order_id=self.kwargs['pk'])
        # qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_customer__addresses'))
        # qs = qs.filter(repair_order_id=self.kwargs['pk']).get()
        # qs = qs.prefetch()
        return qs

# version 1. Updating the repair order view
# 2023-04-08. generated by ChatGPT 4.0.
# for the updating view. separate update views based on the model types
# one for repair order; one for customer and one for address
# future: one update view with


class RepairOrderUpdateView(UpdateView, LoginRequiredMixin):
    template_name = 'dashboard/52_repairorder_updateview.html'
    model = RepairOrdersNewSQL02Model
    # fields = '__all__'
    form_class = RepairOrderUpdateForm
    # success_url = reverse_lazy(
    #     'dashboard:repair_order_detail', pk=self.kwargs['object.repair_order_id'])
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_success_url(self):
        return reverse('dashboard:repair_order_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            RepairOrdersNewSQL02Model, pk=self.kwargs['pk'])
        form = RepairOrderUpdateForm(request.POST, instance=self.object)
        if form.is_valid():
            # self.object.repair_order_last_updated_at = timezone.now()
            form.save()
            # return HttpResponseRedirect(self.get_success_url())
            return redirect(reverse_lazy('dashboard:repair_order_detail', pk=self.kwargs['pk']))
        else:
            # return self.form_invalid(form)
            return self.render_to_response(self.get_context_data(form=form))

# 2023-04-08 repair order update version 2.
# generated by ChatGPT 4.0


def repair_order_update(request, pk):
    repair_order = get_object_or_404(RepairOrdersNewSQL02Model, pk=pk)
    AddressFormSet = inlineformset_factory(CustomersNewSQL02Model, AddressesNewSQL02Model,
                                           fields=('address_type', 'address_line_01', '',
                                                   'address_city', 'address_state', 'address_zip_code'), extra=1)
    if request.method == 'POST':
        repair_order_form = RepairOrderUpdateForm(
            request.POST, instance=repair_order)
        customer_address_formset = AddressFormSet(
            request.POST, instance=repair_order.repair_order_customer)
        if repair_order_form.is_valid() and customer_address_formset.is_valid():
            repair_order_form.save()
            customer_address_formset.save()
            return redirect('repair_order_detail', pk=repair_order.pk)
    else:
        repair_order_form = RepairOrderUpdateForm(instance=repair_order)
        customer_address_formset = AddressFormSet(
            instance=repair_order.repair_order_customer)
    context = {
        'repair_order': repair_order,
        'repair_order_form': repair_order_form,
        'formset': customer_address_formset,
    }
    return render(request, 'dashboard/53_repair_order_updateview_v2.html', context)


def repair_order_and_line_items_detail(request, repair_order_id):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__addresses')).prefetch_related(
        'repair_order_customer__phones',
        'repair_order_customer__emails',
        'repair_order_customer__taxes',
        'lineitems__lineitem_noteitem',
        'lineitems__parts_lineitems',
        'lineitems__lineitem_laboritem',
        'lineitems__lineitem_laboritem').get(pk=repair_order_id)
    line_items = repair_order.lineitems.all()
    part_items = {lineitem.parts_lineitems.all(
    ): lineitem.line_item_id for lineitem in line_items}
    labor_items = {lineitem.lineitem_laboritem.all(
    ): lineitem.line_item_id for lineitem in line_items}
    formset_dict = {}
    formsets = []
    for line_item in line_items:
        formset = PartItemInlineFormSet(instance=line_item)
        if formset.total_form_count() == 0:
            formset = LaborItemInlineFormSet(instance=line_item)
        formsets.append(formset)
        formset_dict.append({formset: line_item.line_item_id})
    context = {
        'repair_order': repair_order,
        'formsets': formsets,
        'formset_dict': formset_dict,
        'line_items': line_items,
        'part_items': part_items,
        'labor_items': labor_items,
    }
    return render(request, 'dashboard/51_repair_order_line_items.html', context)


class RepairOrderLineItemListView(ListView):
    template_name = 'dashboard/51_repair_order_line_items.html'
    model = RepairOrderLineItemSquencesNewSQL02Model
    context_object_name = 'repair_order'

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related(
            'repair_order_customer__addresses',
            'repair_order_customer__phones',
            'repair_order_customer__emails',
            'repair_order_customer__taxes',
            'lineitems__parts_lineitems',
            'lineitems__lineitem_laboritem',
        )

        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.

        qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(
            repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
        return qs

    # ro_single --object consite of only repair order data
    # ro_simple = RepairOrdersNewSQL02Model.objects.get(pk=self.kwargs['pk'])

    # # one query with repair order, custoemr and addresses
    # repair_order = ro_simple.prefetch_related(Prefetch('repair_order_customer__addresses'))
    # # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    # repair_order_customer = repair_order.repair_order_customer
    # address = repair_order_customer.addresses.first()

    # repair_order_form = RepairOrderModelForm(instance=ro_simple)
    # customer_form = CustomerModelForm(instance=repair_order_customer)
    # address_form = AddressModelForm(instance=address)
    # form_class = repair_order_form


class PartItemUpdateView(UpdateView, LoginRequiredMixin):
    # template_name = 'dashboard/90_part_item_list_view.html'
    template_name = 'dashboard/92_part_labor_item_update_view.html'
    form_class = PartItemUpdateForm
    context_object_name = 'part_item'

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        # qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        # qs = qs.prefetch_related('repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
        #        ).prefetch_related('repair_order_customer__taxes').prefetch_related('lineitems__parts_lineitems').prefetch_related('lineitems__lineitem_laboritem')
        qs = LineItemsNewSQL02Model.objects.prefetch_related(
            'partitems_lineitems').prefetch_related('lineitem_laboritem')
        # repair order phase defines the WIP (work-in-progress) category. 6 means invoice.  7 counter sale. 8 deleted. 9 scheduled.
        # qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        line_item = get_object_or_404(
            LineItemsNewSQL02Model, pk=self.kwargs['line_item_id'])
        if line_item is not None:
            part_item_formset = PartItemInlineFormSet(instance=line_item)
            labor_item_formset = LaborItemInlineFormSet(instance=line_item)
            if labor_item_formset.empty_form:
                selected_formset = part_item_formset
            else:
                selected_formset = labor_item_formset
        context['selected_formset'] = selected_formset
        context['part_item_formset'] = part_item_formset
        context['labor_item_formset'] = labor_item_formset
        # try:
        #     part_item = line_item.parts_lineitems.first()
        #     form = PartItemModelForm(instance=part_item)
        #     # part_item = get_object_or_404(PartItemModel,pk=self.kwargs['line_item_id'])
        # except ObjectDoesNotExist:
        #     # return redirect(reverse('dashboard:labor-item-update-view', kwargs=self.kwargs))
        #     labor_item = line_item.lineitem_laboritem.first()
        #     form = LaborItemModelForm(instance=labor_item)

        context['page_title'] = 'Update a Line Item'
        # context['form'] = form
        context['fields'] = self.get_form().fields.items()
        # the line_item_id in the url pattern is passed on to the Updateview .
        context['line_item_id'] = self.kwargs['line_item_id']
        # the pk in the url pattern is passed on to the UpdateView .
        context['repair_order_id'] = self.kwargs['pk']
        context['line_item'] = line_item
        return context

    # def form_valid(self,form):
    #     response = super().form_valid(form)
    #     return redirect(reverse('dashboard:dashboard_detail',args=self.kwargs['line_item_id']))


def line_item_labor_and_part_item_update_view(request, pk, line_item_id):
    repair_order_id = pk  # pk is repair_order_id in repairorder model.
    line_item = LineItemsNewSQL02Model.objects.prefetch_related(
        'partitems_lineitems',
        'lineitem_laboritem',
        'lineitem_noteitem'
        ).filter(line_item_id=line_item_id).first()  # to handle not found error by returning None

    # use .all() instead of .exists() to reduce the queries into DB.
    if line_item.partitems_lineitems.all():
        Formset = PartItemInlineFormSet
    elif line_item.lineitem_laboritem.all():
        Formset = LaborItemInlineFormSet
    else:
        Formset = None
        messages.error(request,
                       f'error fetching information for line item {line_item_id}. data not found or corrupted.')
        return redirect('dashboard:repair_order_detail', pk=pk)

    # in one single line item, some data is from lineitem table, some is either from partitem or laboritem table.
    if request.method == 'POST':

        form = LineItemUpdateForm(request.POST, instance=line_item)
        formset = Formset(request.POST, instance=line_item)

        if formset.is_valid() and form.is_valid():
            formset.save()
            form.save()
            messages.success(
                request, 'Line items have been updated successfully!')
            return redirect('repair_order_detail', pk=pk)
    else:
        formset = Formset(instance=line_item)
        form = LineItemUpdateForm(instance=line_item)

    context = {
        'formset': formset,
        'form': form,
        'repair_order_id': repair_order_id,
        'line_item_id': line_item_id,
        'line_item': line_item,
    }
    return render(request, 'dashboard/93_part_labor_item_update_view_v2.html', context)


class LaborItemUpdateView(UpdateView):
    template_name = 'dashboard/91_labor_item_list_view.html'
    form_class = LaborItemUpdateForm
    context_object_name = 'labor_item'

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        # qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        # qs = qs.prefetch_related('repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
        #        ).prefetch_related('repair_order_customer__taxes').prefetch_related('lineitems__parts_lineitems').prefetch_related('lineitems__lineitem_laboritem')
        qs = LineItemsNewSQL02Model.objects.prefetch_related(
            'parts_lineitems').prefetch_related('lineitem_laboritem')
        # repair order phase defines the WIP (work-in-progress) category. 6 means invoice.  7 counter sale. 8 delet

    # class AppointmentOfNext7DaysListView(ListView):
    #     template_name = 'dashboard/40-appointment_last_7_day_display.html'
    #     model = Appt
    #     context_object_name = 'appointments'


def chat_sidebar_view(request, customer_id):
    text_messages = TextMessagesModel.objects.filter(
        text_customer=customer_id).order_by('-text_message_id')[:10]
    context = {
        'text_messages': text_messages,
        # 2023-04-18: in dashboard_detail_v1() function, there stores a `customer_id` in the request.session ensures persistence in data.
        # hence i am planning to not include this variable in the context
        'customer_id': customer_id,
    }
    return render(request, 'dashboard/50_text_message_side_bar.html', context)


# added on 2023-06-03. ChatGPT generated.
# search form page --- the first step before creating an repair order.
class SearchView(View, InternalUserRequiredMixin):

    # login_url = reverse_lazy('internal_users:internal_user_login')

    async def get(self, request):
        form = SearchForm()
        context = {'appointments': None,
                   'repair_orders': None,
                   'form': form,  # re-render the form with its data.
                   }
        return render(request, 'dashboard/30_search.html', {'form': form})

    async def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():

            search_query = form.cleaned_data['search_query']

            # using sync_to_async to wrap around a search query processing in both appointments and repairorders models.
            appointments = await sync_to_async(self._get_appointments, thread_sensitive=True)(search_query)
            repair_orders = await sync_to_async(self._get_repair_orders, thread_sensitive=True)(search_query)
            # Perform the search query in the appointments or other relevant models
            # appointments = AppointmentRequest.objects.filter(Q(appointment_phone_number__icontains=search_query) |
            #                                                  Q(appointment_email__icontains=search_query)).order_by('appointment_id')

            # repair_orders = RepairOrdersNewSQL02Model.objects.prefetch_related(
            #     Prefetch('repair_order_customer__addresses')).prefetch_related(
            #     'repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
            #                                                       )

            # repair_orders = repair_orders.filter(
            #     repair_order_customer__emails__email_address__icontains=search_query
            # ).filter(repair_order_customer__phones__phone_number__icontains=search_query)

            context = {'appointments': appointments,
                       'repair_orders': repair_orders,
                       'form': form,  # re-render the form with its data.
                       }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

                return render(request, 'dashboard/31_search_results.html', context)
            else:
                print('using 30_search.html')
                return render(request, 'dashboard/30_search.html', context)
            # if appointments.exists():
            #     return render(request, 'dashboard/20_search.html', {'appointments': appointments})
            # else:
            #     return render(request, 'dashboard/20_search.html', {'no_match': True})
        else:
            return render(request, 'dashboard/30_search.html', {'form': form})

    def _get_appointments(self, search_query):
        return list(AppointmentRequest.objects.filter(
            Q(appointment_phone_number__icontains=search_query) |
            Q(appointment_email__icontains=search_query)
        ).order_by('appointment_id'))

    def _get_repair_orders(self, search_query):
        print('search any matched repair order records before creating one...')
        queryset = RepairOrdersNewSQL02Model.objects.prefetch_related(
            'repair_order_customer__addresses',
            'repair_order_customer__phones',
            'repair_order_customer__emails'
            # filtering out only active repair orders
        ).filter(
            repair_order_phase__gte=1,
            repair_order_phase__lte=5
        ).filter(
            Q(repair_order_customer__emails__email_address__icontains=search_query) |
            Q(repair_order_customer__phones__phone_number__icontains=search_query)
        )

        # .filter() calls in Django ORM does not get executed unless the queryset is evaluated.
        # when calling list() on the queset, the sql server executes the script
        return list(queryset)


def get_customer_dash(request):
    # customer_is_activate=False means that a customer is not deactivated. the name of this field is confusing. will
    # need to revise it before PROD launch.
    active_customers = CustomersNewSQL02Model.objects.filter(
        customer_is_deleted=False).prefetch_related(
        'vehicle_customers',
        'addresses',
        'phones',
        'emails',
    )

    current_time = CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE
    paginator = Paginator(active_customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/40_customer_dash_view.html', {'page_obj': page_obj,
                                                                    'current_time': current_time,
                                                                    })

# Customer Create  View


class CustomerCreateView(CreateView, LoginRequiredMixin):
    model = CustomersNewSQL02Model
    form_class = CustomerUpdateForm
    template_name = 'dashboard/42_customer_create.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

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

        self.object = form.save(commit=False)
        self.object.customer_last_updated_at = timezone.now()
        self.object.modified_by = self.request.user  # assuming the user is logged in
        self.object.save()
        messages.success(self.request, 'Update success.')
        return redirect('dashboard:customer-detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse('dashboard:customer-detail', kwargs={'pk': self.object.pk})


class CustomerDetailView(DetailView, LoginRequiredMixin):
    model = CustomersNewSQL02Model
    success_url = reverse_lazy('customer-dash')
    context_object_name = 'customer'
    template_name = 'dashboard/41_customer_detail.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CustomerUpdateForm(
                self.request.POST, instance=self.object)
        else:
            customer = get_object_or_404(
                CustomersNewSQL02Model, pk=self.kwargs['pk'])
            context['email_forms'] = [LiteEmailUpdateForm(
                instance=email) for email in customer.emails.all()]

            context['form'] = CustomerUpdateForm(instance=self.object)
        return context

    def get_queryset(self):

        qs = CustomersNewSQL02Model.objects.prefetch_related(
            'addresses',
            'phones',
            'emails',
            'vehicle_customers').filter(pk=self.kwargs['pk'])
        # qs = qs.filter(repair_order_id=self.kwargs['pk']).get()
        return qs

    def get_success_url(self):
        return reverse('dashboard:customer-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomerUpdateForm(request.POST, instance=self.object)

        if form.is_valid():
            self.object.customer_last_updated_at = timezone.now()
            form.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
        # ret911urn self.render_to_response(self.get_context_data(form=form))


class CustomerDetail2View(CustomerDetailView):
    template_name = 'dashboard/41_customer_detail_v2.html'


def update_customer_email(request, email_id):
    # email_id = request.POST.get('email_id')
    email = get_object_or_404(EmailsNewSQL02Model, pk=email_id)

    customer_email_relation = CustomerEmailsNewSQL02Model.objects.filter(
        email=email).first()

    if not customer_email_relation:
        messages.error(request, "No customer associated with this email.")
        # Redirect to some default page or handle this error appropriately
        return redirect('default_page')

    customer_id = customer_email_relation.customer.pk

    if request.method == "POST":
        form = LiteEmailUpdateForm(request.POST, instance=email)
        if form.is_valid():
            form.save()
            messages.success(request, "Email has been updated successfully.")
            return redirect('dashboard:customer-detail', pk=customer_id)
            # return JsonResponse({'status': 'success'})
        else:
            messages.error(
                request, "Error updating the email. Please try again.")
            # error_json = JsonResponse(
            #     {'status': 'error', 'errors': form.errors})
            # context = {"pk": customer_id, 'error_json_response': error_json}
            return redirect('dashboard:customer-detail', pk=customer_id,
                            )


AddressesFormset = inlineformset_factory(
    CustomersNewSQL02Model, CustomerAddressesNewSQL02Model, fields=('address',))  # extra=1


EmailsFormset = inlineformset_factory(
    CustomersNewSQL02Model, CustomerEmailsNewSQL02Model, form=CustomerEmailForm, fields=('email',), extra=1)

PhonesFormset = inlineformset_factory(
    CustomersNewSQL02Model, CustomerPhonesNewSQL02Model, fields=('customer', 'phone'), fk_name='customer')


class CustomerUpdateView(UpdateView, LoginRequiredMixin):
    model = CustomersNewSQL02Model
    form_class = CustomerUpdateForm
    template_name = 'dashboard/43_customer_update.html'
    success_url = reverse_lazy('dashboard:customer-detail')
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            customer = self.get_object()
            context['addresses_formset'] = AddressesFormset(
                self.request.POST, instance=self.object)
            context['emails_formset'] = EmailsFormset(
                self.request.POST, instance=self.object)
            context['phones_formset'] = PhonesFormset(
                self.request.POST, instance=self.object)
        else:
            context['addresses_formset'] = AddressesFormset(
                instance=self.object)
            context['emails_formset'] = EmailsFormset(instance=self.object)
            context['phones_formset'] = PhonesFormset(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer_last_updated_at = timezone.now()
        self.object.modified_by = self.request.user  # assuming the user is logged in
        self.object.save()
        messages.success(self.request, 'Update success.')
        return redirect('dashboard:customer-detail', pk=self.object.customer_id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CustomerDeleteView(DeleteView, LoginRequiredMixin):
    model = CustomersNewSQL02Model
    template_name = 'dashboard/44_customer_delete.html'
    # Redirect to customer list after "deletion"
    success_url = reverse_lazy('dashboard:customer-dash')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.customer_is_deleted = True  # Soft delete: mark as inactive
        self.object.customer_is_active = False  # Soft delete: mark as inactive
        self.object.save()
        messages.success(request, 'Customer deactivated successfully.')
        return redirect(self.get_success_url())


def get_vehicle_dash(request):
    vehciles = VehiclesNewSQL02Model.objects.select_related(
        'vehicle_cust',
        'vehicle_brake',
        'vehicle_body_style',
        'vehicle_sub_model',
        'vehicle_make',
        'vehicle_gvw',
        'vehicle_engine',
        'vehicle_brake',
        'vehicle_drive_type',
        'vehicle_transmission',
    ).order_by('-vehicle_id')
    current_time = timezone.now()
    paginator = Paginator(vehciles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/60_vehicle_dash_view.html', {'page_obj': page_obj,
                                                                   'current_time': current_time,
                                                                   })


class VehicleCreateView(CreateView, InternalUserRequiredMixin):
    model = VehiclesNewSQL02Model
    form_class = VehicleCreateForm
    template_name = 'dashboard/62_vehicle_create.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.vehicle_last_updated_at = timezone.now()
        self.object.created_by = self.request.user  # assuming the user is logged in
        self.object.save()
        messages.success(self.request, 'Update success.')
        return redirect('dashboard:vehicle-detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse('dashboard:vehicle-detail', kwargs={'pk': self.object.pk})


class VehicleDetailView(DetailView, LoginRequiredMixin):
    model = VehiclesNewSQL02Model
    success_url = reverse_lazy('dashboard:vehicle-dash')
    context_object_name = 'vehicle'
    template_name = 'dashboard/61_vehicle_detail.html'

    def get_queryset(self):
        notes = VehicleNotesModel.objects.filter(vehicle_note_is_active=True)
        return VehiclesNewSQL02Model.objects.prefetch_related(Prefetch('vehiclenotes_vehicle', queryset=notes))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = VehicleUpdateForm(
                self.request.POST, instance=self.object)
        else:
            context['form'] = VehicleUpdateForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = VehicleUpdateForm(request.POST, instance=self.object)
        if form.is_valid():
            self.object.vehicle_last_updated_at = timezone.now()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
            # return self.render_to_response(self.get_context_data(form=form))


class VehicleUpdateView(UpdateView, LoginRequiredMixin):
    model = VehiclesNewSQL02Model
    form_class = VehicleUpdateForm
    template_name = 'dashboard/63_vehicle_update.html'
    context_object_name = 'vehicle'
    success_url = reverse_lazy('dashboard:vehicle-detail')
    login_url = reverse_lazy('internal_users:internal_user_login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.vehicle_last_updated_at = timezone.now()
        self.object.modified_by = self.request.user  # assuming the user is logged in
        self.object.save()
        messages.success(
            self.request, f'Vehicle ID: {self.object.pk} update success.')
        return redirect('dashboard:vehicle-detail', pk=self.object.pk)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class VehicleDeleteView(DeleteView, LoginRequiredMixin):

    model = VehiclesNewSQL02Model
    template_name = 'dashboard/64_vehicle_delete.html'
    success_url = reverse_lazy('dashboard:vehicle-dash')
    login_url = reverse_lazy('internal_users:internal_user_login')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.vehicle_record_is_active = False  # Soft delete: mark as inactive
        self.object.save()
        messages.success(request, 'vehicle deactivated successfully.')
        return redirect(self.get_success_url())

# this is used in Vehicle Update Form to return new customer record by a phone number search.


def search_customer_by_phone(request):
    phone_number = request.GET.get('phone_number_entered', None)
    customers = CustomersNewSQL02Model.objects.filter(
        phones__phone_number_digits_only__contains=phone_number)

    # Create a list to hold the customer data
    customer_data = []

    for customer in customers:
        # Fetch related phone numbers for each customer
        phone_numbers = [p.phone_number for p in customer.phones.all()]

        # Create a dictionary holding the customer data and their related phone numbers
        data = {
            'customer_id': customer.customer_id,
            'get_customer_full_name': customer.get_customer_full_name,
            'phone_numbers': phone_numbers,
        }

        customer_data.append(data)

    return JsonResponse(customer_data, safe=False)


def update_customer_assignment(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicleId')
        selected_customer = request.POST.get('selectedCustomer')

        try:
            vehicle = VehiclesNewSQL02Model.objects.get(id=vehicle_id)
            vehicle.vehicle_cust = selected_customer
            vehicle.vehicle_last_updated_at = timezone.now()
            vehicle.modified_by = request.user  # assuming the user is logged in
            vehicle.save()
            return JsonResponse({'status': 'success', 'message': 'Customer assignment updated successfully.'})
        except VehiclesNewSQL02Model.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Vehicle not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


class RepairOrderListView(ListView, LoginRequiredMixin):
    model = RepairOrdersNewSQL02Model
    login_url = reverse_lazy('internal_users:internal_user_login')
    context_object_name = 'repairorders'
    paginate_by = 4  # if pagination is desired
    template_name = 'dashboard/50_repair_order_view_list.html'

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

# class EmailDataView(APIView):
#     def post(self, request):

#         module_dir = os.path.dirname(__file__)
#         file_path = os.path.join(module_dir, 'fixtures/Email_20230115.json')
#         with open(file_path, 'r') as f:
#             data = json.load(f)
#             serializer = EmailDataSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#         return Response({'status': 'success'})


def technician_dash_view(request, technician_id):
    line_items = LineItemsNewSQL02Model.objects.filter(LineItemTech__id=technician_id).prefetch_related(
        'lineitems__lineitem_noteitem',
        'lineitems__lineitem_laboritem',
        'lineitems__partitems_lineitems',
    )
    return render(request, 'dashboard/technician_workstation.html', {'line_items': line_items})

# this function searchs a vin number entered on the search form. save the most recent snapshot of vehicle info from NHTSA gov website
# to VinNhtsaApiSnapshots model.


async def search_single_vin_via_nhtsa(request):
    vin_data_list = []
    count = 0
    logger = logging.getLogger('django')
    if request.method == 'POST':
        form = VINSearchForm(request.POST)
        if form.is_valid():
            vin = form.cleaned_data['vin']
            year = form.cleaned_data['year']

            logger.info(
                f'performing a manual single vin search on webpage for vin {vin} and model year {year}...')

            vin_data_list, number_of_downgraded_records, created = await fetch_and_save_single_vin_from_nhtsa_api(vin, year)
    else:
        form = VINSearchForm()

    if vin_data_list:
        count = vin_data_list[0].results_count
    else:
        count = None

    context = {
        'form': form,
        'vin_data_list': vin_data_list,
        'count': count
    }
    return render(request, 'dashboard/65_vehicle_vin_search.html', context)


async def search_single_plate_via_plate2vin(request):
    form = LicensePlateSearchForm(request.POST or None)
    plate_data = []
    success = False

    if request.method == 'POST':
        if form.is_valid():
            license_plate = form.cleaned_data['license_plate']
            state = form.cleaned_data['state'].upper()

            try:
                plate_data, success = await fetch_single_plate_data_via_plate2vin_api(license_plate, state)
                if not success:
                    form.add_error(
                        None, 'Failed to fetch VIN for the given License Plate.')
            except Exception as e:
                form.add_error(
                    None, f'Error fetching plate data for plate: {license_plate} state:{state} {str(e)}')

    return render(request, 'dashboard/66_vehicle_license_plate_search.html', {'form': form, 'plate_data': plate_data, 'api_success': success})


async def fetch_or_save_latest_vin_snapshot_async(request):
    vin = request.GET.get('vin', None)
    if not vin:
        return JsonResponse({'error': 'No VIN provided'}, status=400)
    elif len(vin) < 13:
        return JsonResponse({'error': 'Incomplete VIN provided. At least 13 digits.'}, status=400)

    # Fetch the details based on VIN (you can modify this as per your logic)
    latest_vin_data = await fetch_latest_vin_data_from_snapshots(vin)
    if not latest_vin_data:
        print(
            f'no vin {vin} in the database..searching against our vendor apis..')
        await fetch_and_save_single_vin_from_nhtsa_api(vin)

    # Convert to list of dictionaries if it's a QuerySet
    if isinstance(latest_vin_data, QuerySet):
        latest_vin_data = await database_sync_to_async(list)(latest_vin_data.values())

    if not latest_vin_data:
        return JsonResponse({'error': 'No vehicle found for this VIN'}, status=404)

    # Format for presentation
    formatted_content = ""
    for entry in latest_vin_data:
        formatted_content += f"""
        {entry['variable_name']}: {entry['value']}; 
        """
    if not formatted_content:
        formatted_content = "No snapshots found for this VIN."
    print(f'the content of the popover is {formatted_content}.')
    # Return the data you want to show in popover
    # return JsonResponse(formatted_content, safe=False)  #
    return JsonResponse({'data': formatted_content})
