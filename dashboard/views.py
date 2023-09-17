
# 2023-04-02 created to display the index page of the main workstation page.
# representing a modern version of old mitchell1 dashboard
# WIP, search, etc.
from django.urls import reverse
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DetailView  # ,UpdateView
from django.views.generic.edit import CreateView, UpdateView,  DeleteView
from django.db.models import Q
from django.db.models import Prefetch
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponseForbidden
from homepageapp.models import RepairOrdersNewSQL02Model, CustomerAddressesNewSQL02Model, CustomersNewSQL02Model, AddressesNewSQL02Model
from homepageapp.models import RepairOrderLineItemSquencesNewSQL02Model, PartItemModel, LineItemsNewSQL02Model, VehiclesNewSQL02Model
# from homepageapp.forms import RepairOrderModelForm, CustomerModelForm, AddressModelForm, RepairOrderLineItemModelForm, PartItemModelForm, LaborItemModelForm
from dashboard.forms import PartItemFormSet, LaborItemFormSet
from django.forms.models import inlineformset_factory, modelformset_factory
from datetime import datetime, timedelta
from django.contrib import messages
from homepageapp.models import TextMessagesModel
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from internal_users.models import InternalUser
from appointments.models import AppointmentRequest
from dashboard.forms import SearchForm, CustomerUpdateForm, RepairOrderUpdateForm, VehicleUpdateForm, AddressUpdateForm, LineItemUpdateForm, PartItemUpdateForm, LaborItemUpdateForm
from django.core.paginator import Paginator
from django.db.models import Max
from django.views.generic import TemplateView
from core_operations.models import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE
# You can do the same sort of thing manually by testing on request.user.is_authenticated, but the decorator is much more convenient!

# 2023-09-17 list all dashboards available


def get_main_dashboard(request):
    # Create the context with the current time.
    context = {
        'current_time': timezone.now().replace(microsecond=0),
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
    return HttpResponseForbidden("you don't have permission to access to this page.")

# dashboard listview via function. Version 1


def wip_dashboard(request):
    repair_orders = RepairOrdersNewSQL02Model.objects.filter(
        repair_order_phase__gte=1, repair_order_phase__lte=5).prefetch_related('repair_order_customer')
    # repair_orders_v2 = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer_id', 'repair_order_customer_id__addresses').filter(repair_order_phase_id__in=[1,2,3,4,5])
    customer_addresses = AddressesNewSQL02Model.objects.prefetch_related(
        'addresses')
    # the alternative way to grab repair orders, as well as the address information
    # __gte means great than or equal; __lte means less than equal
    all_in_one_set = RepairOrdersNewSQL02Model.objects.filter(
        repair_order_phase__gte=1, repair_order_phase__lte=5).prefetch_related(Prefetch('repair_order_customer__addresses'))
    context = {
        'repair_orders': repair_orders,
        'customer_addresses': customer_addresses,
        'all_in_one_set': all_in_one_set,
    }
    return render(request, 'dashboard/11_WIP_dashboard.html', context)

# using listview to display the dashboarrd. version 2, dashboard list view.


class WIPDashboardView(LoginRequiredMixin, ListView):
    model = RepairOrdersNewSQL02Model
    context_object_name = 'repair_orders'
    template_name = 'dashboard/12_WIP_dashboard_v2.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not isinstance(request.user, InternalUser):
                return self.handle_no_permission()
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def get_queryset(self):
        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.
        # qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
        qs = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_phase__gte=1, repair_order_phase__lte=5)
        qs = qs.select_related('repair_order_customer'
                               ).prefetch_related('repair_order_customer__addresses',
                                                  'repair_order_customer__phones',
                                                  'repair_order_customer__emails',
                                                  'repair_order_customer__taxes'
                                                  )
        qs = qs.prefetch_related('payment_repairorders',
                                 'repair_order_customer__payment_customers')

        return qs


# dashboard detail view. version 1
# modified to prefetch emails, phones, taxes to each repair_order_customer object


def dashboard_detail_v1(request, pk):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__addresses'),
        'repair_order_customer__customer_phones',
        'repair_order_customer__customer_emails',
        'repair_order_customer__customer_taxes',
        'lineitems__lineitem_noteitem',
        'repair_order_vehicle'
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
            messages.success('redirecting')
            return redirect('dashboard:dashboard')
    else:
        # Display the form for updating the record
        form = RepairOrderUpdateForm(instance=repair_order)

    context = {
        'repair_order': repair_order,
        'form': form,
        'repair_order_id': repair_order_id,
        'customer_id': customer_id,
        'line_items': line_items,
        'current_time': timezone.now().replace(microsecond=0),
        'text_messages': text_messages,

    }
    return render(request, 'dashboard/20_dashboard_detail.html', context)

# dashboard detail view. Version 2


def dashboard_detail_v2(request, pk):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__customer_addresses'),
        'repair_order_customer__customer_phones',
        'repair_order_customer__customer_emails',
    ).prefetch_related(
    ).prefetch_related(
    ).prefetch_related('repair_order_customer__customer_taxes').get(pk=pk)
    # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    repair_order_customer = repair_order.repair_order_customer
    customer_address = repair_order_customer.addresses.first()

    repair_order_form = RepairOrderUpdateForm(instance=repair_order)
    customer_form = CustomerUpdateForm(instance=repair_order_customer)
    address_form = AddressUpdateForm(instance=customer_address)

    return render(request, 'dashboard/22_dashboard_detail_v2.html', {
        'repair_order': repair_order,
        'repair_order_form': repair_order_form,
        'customer_form': customer_form,
        'address_form': address_form,
    })

# dashboard detail view. based on the DetailView model. version 3


class DashboardDetailView(DetailView):
    template_name = 'dashboard/23_dashboard_detail_v3.html'

    # making sure the context_object_name is repair_order so that repair_order can be used in the template html.
    context_object_name = 'repair_order'
    # slug_field = 'isbn'
    # slug_url_kwarg = 'isbn'
    # model = RepairOrdersNewSQL02Model

    # whenever visiting a repair order, update the `repair_order_last_updated_date``
    # def get_object(self):
    #         obj = super().get_object()
    #         # Record the last accessed date
    #         obj.repair_order_last_updated_date = timezone.now()
    #         obj.save()
    #         return obj
    #
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

class RepairOrderUpdateView(UpdateView):
    template_name = 'dashboard/52_repairorder_updateview.html'
    model = RepairOrdersNewSQL02Model
    # fields = '__all__'
    form_class = RepairOrderUpdateForm
    # success_url = reverse_lazy('dashboard:dashboard-detail',pk=self.kwargs['repair_order.repair_order_id'])

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            RepairOrdersNewSQL02Model, pk=self.kwargs['pk'])
        form = RepairOrderUpdateForm(request.POST, instance=self.object)
        if form.is_valid():
            # self.object.repair_order_last_updated_date = timezone.now()
            form.save()
            # return HttpResponseRedirect(self.get_success_url())
            return redirect(reverse_lazy('dashboard:dashboard-detail', pk=self.kwargs['pk']))
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
        'repair_order_customer__phones').prefetch_related('repair_order_customer__customer_emails'
                                                          ).prefetch_related('repair_order_customer__customer_taxes'
                                                                             ).prefetch_related('lineitems__lineitem_noteitem').prefetch_related('lineitems__parts_lineitems'
                                                                                                                                                 ).prefetch_related('lineitems__lineitem_laboritem').get(pk=repair_order_id)
    line_items = repair_order.lineitems.all()
    part_items = {lineitem.parts_lineitems.all(
    ): lineitem.line_item_id for lineitem in line_items}
    labor_items = {lineitem.lineitem_laboritem.all(
    ): lineitem.line_item_id for lineitem in line_items}
    formset_dict = {}
    formsets = []
    for line_item in line_items:
        formset = PartItemFormSet(instance=line_item)
        if formset.total_form_count() == 0:
            formset = LaborItemFormSet(instance=line_item)
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
    template_name = 'dashboard/02-repair_order_line_items.html'
    model = RepairOrderLineItemSquencesNewSQL02Model
    context_object_name = 'repair_order'

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related(
            'repair_order_customer__customer_addresses',
            'repair_order_customer__customer_phones',
            'repair_order_customer__customer_emails',
            'repair_order_customer__customer_taxes',
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


class PartItemUpdateView(UpdateView):
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
            'parts_lineitems').prefetch_related('lineitem_laboritem')
        # repair order phase defines the WIP (work-in-progress) category. 6 means invoice.  7 counter sale. 8 deleted. 9 scheduled.
        # qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        line_item = get_object_or_404(
            LineItemsNewSQL02Model, pk=self.kwargs['line_item_id'])
        if line_item is not None:
            part_item_formset = PartItemFormSet(instance=line_item)
            labor_item_formset = LaborItemFormSet(instance=line_item)
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
    repair_order_id = pk
    line_item = LineItemsNewSQL02Model.objects.prefetch_related(
        'parts_lineitems',
        'lineitem_laboritem').filter(line_item_id=line_item_id).get()

    # in one single line item, some data is from lineitem table, some is either from partitem or laboritem table.
    if request.method == 'POST':
        form = LineItemUpdateForm(request.POST, instance=line_item)
        formset = PartItemFormSet(
            request.POST, instance=line_item, prefix='partitems')
        if formset.total_form_count() == 0:
            formset = LaborItemFormSet(
                request.POST, instance=line_item, prefix='laboritems')

        if form.is_valid() and formset.is_valid():
            formset.save()
            form.save()
            messages.success(
                request, 'Line items have been updated successfully!')
            return redirect('repair_order_detail', pk=pk)
    else:
        if line_item:
            part_item_formset = PartItemFormSet(instance=line_item)
            labor_item_formset = LaborItemFormSet(instance=line_item)
            form = LineItemUpdateForm(instance=line_item)
            if labor_item_formset.total_form_count() == 0:
                selected_formset = part_item_formset
                is_labor_item = 0
            elif part_item_formset.total_form_count() == 0:
                selected_formset = labor_item_formset
                is_labor_item = 1
            else:
                selected_formset = None
                form = None

        context = {
            'selected_formset': selected_formset,
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
class SearchView(LoginRequiredMixin, View):

    login_url = reverse_lazy('internal_users:internal_user_login')

    def get(self, request):
        form = SearchForm()
        return render(request, 'dashboard/30_search.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # Perform the search query in the appointments or other relevant models
            appointments = AppointmentRequest.objects.filter(Q(appointment_phone_number__icontains=search_query) |
                                                             Q(appointment_email__icontains=search_query)).order_by('appointment_id')

            repair_orders = RepairOrdersNewSQL02Model.objects.prefetch_related(
                Prefetch('repair_order_customer__addresses')).prefetch_related(
                'repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
                                                                  )

            repair_orders = repair_orders.filter(
                repair_order_customer__emails__email_address__icontains=search_query
            ).filter(repair_order_customer__phones__phone_number__icontains=search_query)

            context = {'appointments': appointments,
                       'repair_orders': repair_orders,
                       }
            return render(request, 'dashboard/30_search.html', context)
            # if appointments.exists():
            #     return render(request, 'dashboard/20_search.html', {'appointments': appointments})
            # else:
            #     return render(request, 'dashboard/20_search.html', {'no_match': True})
        else:
            return render(request, 'dashboard/30_search.html', {'form': form})


# def dashboard_search(request):
#     form = SearchForm(request.GET)
#     if form.is_valid():
#         query = form.cleaned_data['searchquery']
#         # Search in AppointmentRequest
#         appointment_requests_phone = AppointmentRequest.objects.filter(phone_number__icontains=query)
#         appointment_requests_email = AppointmentRequest.objects.filter(email_address__icontains=query)

#         # Search in RepairOrder
#         repair_orders_phone = RepairOrdersNewSQL02Model.objects.filter(phone_number__icontains=query)
#         repair_orders_email = RepairOrdersNewSQL02Model.objects.filter(email__icontains=query)

#         return render(request, 'search_results.html', {
#             'form': form,
#             'appointment_requests_phone': appointment_requests_phone,
#             'appointment_requests_email': appointment_requests_email,
#             'repair_orders_phone': repair_orders_phone,
#             'repair_orders_email': repair_orders_email,
#         })
#     else:
#         return render(request, '80_search.html', {'form': form})


def get_customer_dash(request):
    # customer_is_activate=False means that a customer is not deactivated. the name of this field is confusing. will
    # need to revise it before PROD launch.
    active_customers = CustomersNewSQL02Model.objects.filter(
        customer_is_deleted=False).prefetch_related(
        'vehicle_customers',
    )
    current_time = CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE
    paginator = Paginator(active_customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/40_customer_dash_view.html', {'page_obj': page_obj,
                                                                    'current_time': current_time,
                                                                    })

# Customer Create  View


class CustomerCreateView(CreateView):
    model = CustomersNewSQL02Model
    fields = ['customer_first_name', 'customer_last_name', 'customer_middle_name',
              'customer_does_allow_SMS',]
    template_name = 'dashboard/42_customer_creation.html'
    success_url = reverse_lazy('customers-dash')

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
    success_url = reverse_lazy('customer-dash')
    context_object_name = 'customer'
    template_name = 'dashboard/41_customer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CustomerUpdateForm(
                self.request.POST, instance=self.object)
        else:
            context['form'] = CustomerUpdateForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomerUpdateForm(request.POST, instance=self.object)
        if form.is_valid():
            self.object.customer_last_updated_date = timezone.now()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
            # return self.render_to_response(self.get_context_data(form=form))


class CustomerUpdateView(UpdateView):
    model = CustomersNewSQL02Model
    form_class = CustomerUpdateForm
    template_name = 'dashboard/43_customer_update.html'
    success_url = reverse_lazy('dashboard:customer-detail')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer_last_updated_date = timezone.now()
        self.object.modified_by = self.request.user  # assuming the user is logged in
        self.object.save()
        messages.success(self.request, 'Update success.')
        return redirect('dashboard:customer-detail', pk=self.object.customer_id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CustomerDeleteView(DeleteView):
    model = CustomersNewSQL02Model
    template_name = 'dashboard/44_customer_delete.html'
    # Redirect to customer list after "deletion"
    success_url = reverse_lazy('dashboard:customer-dash')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.customer_is_deleted = True  # Soft delete: mark as inactive
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
        'vehicle_GVW',
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


class VehicleDetailView(DetailView):
    model = VehiclesNewSQL02Model
    success_url = reverse_lazy('vehicle-dash')
    context_object_name = 'vehicle'
    template_name = 'dashboard/61_vehicle_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CustomerUpdateForm(
                self.request.POST, instance=self.object)
        else:
            context['form'] = CustomerUpdateForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomerUpdateForm(request.POST, instance=self.object)
        if form.is_valid():
            self.object.vehicle_last_updated_date = timezone.now()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
            # return self.render_to_response(self.get_context_data(form=form))


class RepairOrderListView(ListView):
    # model = RepairOrdersNewSQL02Model

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
        'lineitems__parts_lineitems',
    )
    return render(request, 'dashboard/technician_workstation.html', {'line_items': line_items})
