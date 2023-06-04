
# 2023-04-02 created to display the index page of the main workstation page.
# representing a modern version of old mitchell1 dashboard
# WIP, search, etc.
from django.urls import reverse
from django.shortcuts import render, get_list_or_404, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import  DetailView #,UpdateView
from django.views.generic.edit import CreateView, UpdateView,  DeleteView
from django.db.models import Q
from django.db.models import Prefetch
from django.utils import timezone
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from homepageapp.models import RepairOrdersNewSQL02Model, CustomerAddressesNewSQL02Model,CustomersNewSQL02Model,AddressesNewSQL02Model
from homepageapp.models import RepairOrderLineItemSquencesNewSQL02Model, PartItemModel, LineItemsNewSQL02Model
from homepageapp.forms import RepairOrderModelForm, CustomerModelForm, AddressModelForm, RepairOrderLineItemModelForm, PartItemModelForm, LaborItemModelForm
from homepageapp.forms import PartItemFormSet, LaborItemFormSet
from django.forms.models import inlineformset_factory, modelformset_factory
from datetime import datetime, timedelta
from appointments.models import AppointmentRequest
from django.contrib import messages
from homepageapp.models import TextMessagesModel
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def IndexPage(request):
    return render(request, 'dashboard/index.html')

# You can do the same sort of thing manually by testing on request.user.is_authenticated, but the decorator is much more convenient!
# dashboard listview via function. Version 1
def dashboard(request):
    repair_orders = RepairOrdersNewSQL02Model.objects.filter(repair_order_phase__gte=1, repair_order_phase__lte=5).prefetch_related('repair_order_customer')
    # repair_orders_v2 = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer_id', 'repair_order_customer_id__addresses').filter(repair_order_phase_id__in=[1,2,3,4,5])
    customer_addresses = AddressesNewSQL02Model.objects.prefetch_related('addresses')
    ## the alternative way to grab repair orders, as well as the address information
    # __gte means great than or equal; __lte means less than equal
    all_in_one_set = RepairOrdersNewSQL02Model.objects.filter(repair_order_phase__gte=1, repair_order_phase__lte=5).prefetch_related(Prefetch('repair_order_customer__addresses'))
    context = {
        'repair_orders': repair_orders,
        'customer_addresses': customer_addresses,
        'all_in_one_set': all_in_one_set,
    }    
    return render(request, 'dashboard/10_dashboard.html', context)

# using listview to display the dashboarrd. version 2, dashboard list view.
class DashboardView(LoginRequiredMixin, ListView):
    model = RepairOrdersNewSQL02Model
    context_object_name = 'repair_orders'
    template_name = 'dashboard/11_dashboard_v2.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_queryset(self):
        ## `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        qs = qs.prefetch_related('repair_order_customer__phones').prefetch_related('repair_order_customer__emails').prefetch_related('repair_order_customer__taxes')
        
        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.
        
        qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
        return qs
    
# dashboard detail view. version 1 
# modified to prefetch emails, phones, taxes to each repair_order_customer object
def dashboard_detail_v1(request, pk):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__addresses')).prefetch_related(
        'repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
        ).prefetch_related('repair_order_customer__taxes').prefetch_related('lineitems__noteitems'
        ).prefetch_related('repair_order_vehicle').get(pk=pk)
    # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    repair_order_id = repair_order.repair_order_id
    customer_id = repair_order.repair_order_customer.customer_id
    vehicle = repair_order.repair_order_vehicle
    
    line_items = repair_order.lineitems.all()
    
    text_messages = TextMessagesModel.objects.filter(text_customer=customer_id).order_by('-text_message_id')[:10]

    # send out a repair_order_id stored in the request.session.
    request.session['repair_order_id'] = repair_order_id
    # request.session['customer_id'] = customer_id

    if request.method == 'POST':
        # Process form data and save the changes
        form = RepairOrderModelForm(request.POST, instance=repair_order)
        if form.is_valid():
            form.save()
            messages.success('redirecting')
            return redirect('dashboard:dashboard')
    else:
        # Display the form for updating the record
        form = RepairOrderModelForm(instance=repair_order)

    context = {
        'repair_order': repair_order,
        'form': form,
        'repair_order_id':repair_order_id,
        'customer_id':customer_id,
        'line_items': line_items,
        'current_time': timezone.now().replace(microsecond=0),
        'text_messages':text_messages,

    }
    return render(request, 'dashboard/02-dashboard_detail.html', context)

# dashboard detail view. Version 2
def dashboard_detail_v2(request, pk):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__addresses')).prefetch_related(
        'repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
        ).prefetch_related('repair_order_customer__taxes').get(pk=pk)
    # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    repair_order_customer = repair_order.repair_order_customer
    customer_address = repair_order_customer.addresses.first()

    repair_order_form = RepairOrderModelForm(instance=repair_order)
    customer_form = CustomerModelForm(instance=repair_order_customer)
    address_form = AddressModelForm(instance=customer_address)

    return render(request, 'dashboard/02-dashboard_detail_v2.html', {
        'repair_order': repair_order,
        'repair_order_form': repair_order_form,
        'customer_form': customer_form,
        'address_form': address_form,
    })

# dashboard detail view. based on the DetailView model. version 3
class DashboardDetailView(DetailView):
    template_name = 'dashboard/02-dashboard_detail_v3.html'

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
        ## `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_customer__addresses')).filter(repair_order_id=self.kwargs['pk'])
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
    template_name = 'dashboard/03-repairorder_updateview.html'
    model = RepairOrdersNewSQL02Model
    # fields = '__all__'
    form_class = RepairOrderModelForm
    # success_url = reverse_lazy('dashboard:dashboard-detail',pk=self.kwargs['repair_order.repair_order_id'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = RepairOrderModelForm(request.POST, instance=self.object)
        if form.is_valid():
            # self.object.repair_order_last_updated_date = timezone.now()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

# 2023-04-08 repair order update version 2.
# generated by ChatGPT 4.0 
def repair_order_update(request, pk):
    repair_order = get_object_or_404(RepairOrdersNewSQL02Model, pk=pk)
    AddressFormSet = inlineformset_factory(CustomersNewSQL02Model, AddressesNewSQL02Model, 
                                           fields=('address_type', 'address_line_01', '', 
                                           'address_city', 'address_state', 'address_zip_code'), extra=1)
    if request.method == 'POST':
        repair_order_form = RepairOrderModelForm(request.POST, instance=repair_order)
        customer_address_formset = AddressFormSet(request.POST, instance=repair_order.repair_order_customer)
        if repair_order_form.is_valid() and customer_address_formset.is_valid():
            repair_order_form.save()
            customer_address_formset.save()
            return redirect('repair_order_detail', pk=repair_order.pk)
    else:
        repair_order_form = RepairOrderModelForm(instance=repair_order)
        customer_address_formset = AddressFormSet(instance=repair_order.repair_order_customer)
    context = {
        'repair_order': repair_order,
        'repair_order_form': repair_order_form,
        'formset': customer_address_formset,
    }
    return render(request, 'dashboard/03-repair_order_updateview_v2.html', context)

def repair_order_and_line_items_detail(request, repair_order_id):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__addresses')).prefetch_related(
        'repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
        ).prefetch_related('repair_order_customer__taxes'
        ).prefetch_related('lineitems__noteitems').prefetch_related('lineitems__parts_lineitems'
        ).prefetch_related('lineitems__labor_lineitems').get(pk=repair_order_id)
    line_items = repair_order.lineitems.all()
    part_items = {lineitem.parts_lineitems.all():lineitem.line_item_id for lineitem in line_items}
    labor_items = {lineitem.labor_lineitems.all():lineitem.line_item_id for lineitem in line_items} 
    formset_dict = {}          
    formsets = []
    for line_item in line_items:
        formset = PartItemFormSet(instance=line_item)
        if formset.total_form_count() == 0:
            formset = LaborItemFormSet(instance=line_item)
        formsets.append(formset)
        formset_dict.append({formset:line_item.line_item_id})
    context = {
        'repair_order': repair_order,
        'formsets': formsets,
        'formset_dict':formset_dict,
        'line_items': line_items,
        'part_items': part_items,
        'labor_items': labor_items,
    }
    return render(request, 'dashboard/02-repair_order_line_items.html', context)

class RepairOrderLineItemListView(ListView):
    template_name = 'dashboard/02-repair_order_line_items.html'
    model = RepairOrderLineItemSquencesNewSQL02Model
    context_object_name = 'repair_order'

    def get_queryset(self):
        ## `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        qs = qs.prefetch_related('repair_order_customer__phones').prefetch_related('repair_order_customer__emails').prefetch_related('repair_order_customer__taxes').prefetch_related('lineitems__parts_lineitems').prefetch_related('lineitems__labor_lineitems')
        
        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.
        
        qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
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
    form_class = PartItemModelForm
    context_object_name = 'part_item'

    def get_queryset(self):
        ## `__` double undestore..more researched are needed.
        # qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        # qs = qs.prefetch_related('repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
        #        ).prefetch_related('repair_order_customer__taxes').prefetch_related('lineitems__parts_lineitems').prefetch_related('lineitems__labor_lineitems')
        qs = LineItemsNewSQL02Model.objects.prefetch_related('parts_lineitems').prefetch_related('labor_lineitems')
        # repair order phase defines the WIP (work-in-progress) category. 6 means invoice.  7 counter sale. 8 deleted. 9 scheduled.
        # qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        line_item = get_object_or_404(LineItemsNewSQL02Model, pk=self.kwargs['line_item_id'])
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
            #     labor_item = line_item.labor_lineitems.first()
            #     form = LaborItemModelForm(instance=labor_item)
        
        context['page_title'] = 'Update a Line Item'
        # context['form'] = form
        context['fields'] = self.get_form().fields.items()
        context['line_item_id']=self.kwargs['line_item_id'] # the line_item_id in the url pattern is passed on to the Updateview .
        context['repair_order_id']=self.kwargs['pk'] # the pk in the url pattern is passed on to the UpdateView .
        context['line_item']=line_item
        return context
    
    # def form_valid(self,form):
    #     response = super().form_valid(form)
    #     return redirect(reverse('dashboard:dashboard_detail',args=self.kwargs['line_item_id']))

#
def line_item_labor_and_part_item_update_view(request, pk, line_item_id):
    repair_order_id = pk
    line_item = LineItemsNewSQL02Model.objects.prefetch_related('parts_lineitems').prefetch_related('labor_lineitems').filter(line_item_id=line_item_id).get()
    if request.method == 'POST':
        lineitem_form = RepairOrderLineItemModelForm(request.POST, instance=line_item)
        formset = PartItemFormSet(request.POST, instance=line_item)
        if formset.total_form_count() == 0:
            formset = LaborItemFormSet(request.POST, instance=line_item)
        
        if formset.is_valid() and lineitem_form.is_valid():
            formset.save()
            lineitem_form.save()
            messages.success(request, 'Line items have been updated successfully!')
            return redirect('repair_order_detail', pk=pk)
    else:
        if line_item:
                part_item_formset = PartItemFormSet(instance=line_item)
                labor_item_formset = LaborItemFormSet(instance=line_item)
                if labor_item_formset.total_form_count()==0:
                    selected_formset = part_item_formset
                    is_labor_item = 0
                elif part_item_formset.total_form_count()==0:
                    selected_formset = labor_item_formset
                    is_labor_item = 1
                else:
                    selected_formset = None
        

        context = {
                'selected_formset':selected_formset,
                'repair_order_id':repair_order_id,
                'line_item_id':line_item_id,
                'line_item':line_item,
        }
        return render(request, 'dashboard/93_part_labor_item_update_view_v2.html', context)

    
class LaborItemUpdateView(UpdateView):
    template_name = 'dashboard/91_labor_item_list_view.html'
    form_class = LaborItemModelForm
    context_object_name = 'labor_item'
    def get_queryset(self):
        ## `__` double undestore..more researched are needed.
        # qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        # qs = qs.prefetch_related('repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
        #        ).prefetch_related('repair_order_customer__taxes').prefetch_related('lineitems__parts_lineitems').prefetch_related('lineitems__labor_lineitems')
        qs = LineItemsNewSQL02Model.objects.prefetch_related('parts_lineitems').prefetch_related('labor_lineitems')
        # repair order phase defines the WIP (work-in-progress) category. 6 means invoice.  7 counter sale. 8 delet

    # class AppointmentOfNext7DaysListView(ListView):
    #     template_name = 'dashboard/40-appointment_last_7_day_display.html'
    #     model = Appt
    #     context_object_name = 'appointments'


def chat_sidebar_view(request,customer_id):
    text_messages = TextMessagesModel.objects.filter(text_customer=customer_id).order_by('-text_message_id')[:10]
    context = {
        'text_messages': text_messages,
        # 2023-04-18: in dashboard_detail_v1() function, there stores a `customer_id` in the request.session ensures persistence in data.
        # hence i am planning to not include this variable in the context
        'customer_id': customer_id,
    }
    return render(request, 'dashboard/50-text-message-side-bar.html', context)