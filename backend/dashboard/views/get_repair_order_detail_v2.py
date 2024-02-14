
from .base import render, login_required
from homepageapp.models import RepairOrdersNewSQL02Model
from dashboard.forms import RepairOrderUpdateForm, CustomerUpdateForm, AddressUpdateForm

@login_required(login_url='internal_users:internal_user_login')
def get_repair_order_detail_v2(request, pk):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        'repair_order_customer__addresses',
        'repair_order_customer__phones',
        'repair_order_customer__emails',
        'repair_order_customer__taxes',
        # 'repair_order_customer__vehicle',
    ).get(pk=pk)
    # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    repair_order_customer = repair_order.repair_order_customer
    customer_address = repair_order_customer.addresses.first()

    repair_order_form = RepairOrderUpdateForm(instance=repair_order)
    customer_form = CustomerUpdateForm(instance=repair_order_customer)
    address_form = AddressUpdateForm(instance=customer_address)

    #  'dashboard/22_repair_order_detail_v1.html'
    return render(request, 'dashboard/24_wip_detail_update_as_whole_via_inlineform.html', {
        'repair_order': repair_order,
        'repair_order_form': repair_order_form,
        'customer_form': customer_form,
        'address_form': address_form,
    })