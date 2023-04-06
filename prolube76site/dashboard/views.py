
# 2023-04-02 created to display the index page of the main workstation page.
# representing a modern version of old mitchell1 dashboard
# WIP, search, etc.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepageapp.models import RepairOrdersNewSQL02Model,CustomerAddressesNewSQL02Model,CustomersNewSQL02Model,AddressesNewSQL02Model
from django.views.generic import ListView
from django.db.models import Q
from django.db.models import Prefetch

@login_required
def IndexPage(request):
    return render(request, 'dashboard/index.html')

# You can do the same sort of thing manually by testing on request.user.is_authenticated, but the decorator is much more convenient!

def dashboard(request):
    repair_orders = RepairOrdersNewSQL02Model.objects.filter(repair_order_phase__gte=1, repair_order_phase__lte=5).prefetch_related('repair_order_customer_id__customers')
    # repair_orders_v2 = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer_id', 'repair_order_customer_id__addresses').filter(repair_order_phase_id__in=[1,2,3,4,5])
    customer_addresses = AddressesNewSQL02Model.objects.prefetch_related('addresses')

    ## the alternative way to grab repair orders, as well as the address information

    all_in_one_set = RepairOrdersNewSQL02Model.objects.filter(repair_order_phase__gte=1, repair_order_phase__lte=5).prefetch_related(Prefetch('repair_order_customer__addresses',queryset=customer_addresses))
    context = {
        'repair_orders': repair_orders,
        'customer_addresses': customer_addresses,
        'all_in_one_set': all_in_one_set,
    }    
    return render(request, 'dashboard/01-dashboard.html', context)


class DashboardView(ListView):
    template_name = 'dashboard/01-dashboard_v2.html'
    model = RepairOrdersNewSQL02Model
    context_object_name = 'repair_orders'

    def get_queryset(self):
        ## `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
        return qs