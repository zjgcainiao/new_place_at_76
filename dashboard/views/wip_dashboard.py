from .base import render, login_required, CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, messages, redirect, reverse_lazy, ListView,Prefetch

from homepageapp.models import RepairOrdersNewSQL02Model
from internal_users.models import InternalUser
from internal_users.mixins import InternalUserRequiredMixin

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