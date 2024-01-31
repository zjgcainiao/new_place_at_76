
from .base import render, get_object_or_404, redirect
from homepageapp.models import RepairOrdersNewSQL02Model, CustomersNewSQL02Model, AddressesNewSQL02Model
from dashboard.forms import RepairOrderUpdateForm
from django.forms import inlineformset_factory


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
            return redirect('wip_detail_v1', pk=repair_order.pk)
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