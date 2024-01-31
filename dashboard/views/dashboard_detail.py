from .base import LoginRequiredMixin, DetailView, reverse_lazy, Prefetch,InternalUserRequiredMixin
from homepageapp.models import RepairOrdersNewSQL02Model
from internal_users.models import InternalUser



# dashboard detail view. based on the DetailView model. version 3
class DashboardDetailView(DetailView, InternalUserRequiredMixin):
    template_name = 'dashboard/23_dashboard_detail_v3.html'
    # login_url = reverse_lazy('internal_users:internal_user_login')
    # making sure the context_object_name is repair_order so that repair_order can be used in the template html.
    context_object_name = 'repair_order'
    # slug_field = 'isbn'
    # slug_url_kwarg = 'isbn'
    # model = RepairOrdersNewSQL02Model

    # whenever visiting a repair order, update the `repair_order_last_updated_at``
    # def get_object(self):
    #         obj = super().get_object()
    #         # Record the last accessed date
    #         obj.repair_order_last_updated_at = timezone.now()
    #         obj.save()
    #         return obj
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not isinstance(request.user, InternalUser):
                return self.handle_no_permission()
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch(
            'repair_order_customer__addresses')).filter(repair_order_id=self.kwargs['pk'])
        # qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_customer__addresses'))
        # qs = qs.filter(repair_order_id=self.kwargs['pk']).get()
        # qs = qs.prefetch()
        return qs