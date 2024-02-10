
from .base import ListView,Q
from homepageapp.models import RepairOrderLineItemSquencesNewSQL02Model, RepairOrdersNewSQL02Model


class RepairOrderLineItemListView(ListView):
    template_name = 'dashboard/51_repair_order_line_items.html'
    model = RepairOrderLineItemSquencesNewSQL02Model
    context_object_name = 'repair_order'

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.select_related(
            'repair_order_customer').prefetch_related(
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
