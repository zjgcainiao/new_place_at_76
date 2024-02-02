
from .base import render, login_required, CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE
from homepageapp.models import RepairOrdersNewSQL02Model, AddressesNewSQL02Model

# dashboard listview via function. Version 1
def get_wip_dash(request):
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
    return render(request, 'dashboard/11_wip_dash.html', context)

# using listview to display the dashboarrd. version 2, dashboard list view.