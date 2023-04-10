
# 2023-04-02 created to display the index page of the main workstation page.
# representing a modern version of old mitchell1 dashboard
# WIP, search, etc.

from django.shortcuts import render, get_list_or_404, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView, DetailView
from django.db.models import Q
from django.db.models import Prefetch
from django.utils import timezone
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from homepageapp.models import RepairOrdersNewSQL02Model,CustomerAddressesNewSQL02Model,CustomersNewSQL02Model,AddressesNewSQL02Model
from homepageapp.forms import RepairOrderModelForm,CustomerModelForm,AddressModelForm
from django.forms.models import inlineformset_factory

@login_required
def IndexPage(request):
    return render(request, 'dashboard/index.html')

# You can do the same sort of thing manually by testing on request.user.is_authenticated, but the decorator is much more convenient!

# dashboard listview via function. Version 1
def dashboard(request):
    repair_orders = RepairOrdersNewSQL02Model.objects.filter(repair_order_phase__gte=1, repair_order_phase__lte=5).prefetch_related('repair_order_customer__customers')
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
    return render(request, 'dashboard/01-dashboard.html', context)

# using listview to display the dashbaord. version 2, dashboard list view.
class DashboardView(ListView):
    template_name = 'dashboard/01-dashboard_v2.html'
    model = RepairOrdersNewSQL02Model
    context_object_name = 'repair_orders'

    def get_queryset(self):
        ## `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
        return qs
    
# version 1 dashborad detail view
def dashboard_detail(request, pk):

    # repair_order = get_object_or_404(request.GET,pk=pk)
    repair_order = get_object_or_404(RepairOrdersNewSQL02Model, pk=pk)

    if request.method == 'POST':
        # Process form data and save the changes
        form = RepairOrderModelForm(request.POST, instance=repair_order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Display the form for updating the record
        form = RepairOrderModelForm(instance=repair_order)

    context = {
        'repair_order': repair_order,
        'form': form,
    }
    return render(request, 'dashboard/02-dashboard_detail.html', context)

# dashboard detail view. Version 2
def dashboard_detail_view(request, pk):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_customer__addresses')).get(pk=pk)
    # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    repair_order_customer = repair_order.repair_order_customer
    address = repair_order_customer.addresses.first()

    repair_order_form = RepairOrderModelForm(instance=repair_order)
    customer_form = CustomerModelForm(instance=repair_order_customer)
    address_form = AddressModelForm(instance=address)

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
    success_url = reverse_lazy('dashboard-detail')

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

