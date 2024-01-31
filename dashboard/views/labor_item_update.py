from .base import UpdateView
from homepageapp.models import LineItemsNewSQL02Model
from dashboard.forms import LaborItemUpdateForm

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
