from .base import ListView, LoginRequiredMixin, reverse_lazy,timezone
from homepageapp.models import RepairOrdersNewSQL02Model





class RepairOrderListView(ListView, LoginRequiredMixin):
    model = RepairOrdersNewSQL02Model
    login_url = reverse_lazy('internal_users:internal_user_login')
    context_object_name = 'repairorders'
    paginate_by = 4  # if pagination is desired
    template_name = 'dashboard/50_repair_order_view_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add a current time into the context.
        context['current_time'] = timezone.now()
        # number_of_actives = CustomersNewSQL01Model.objects.annotate(Count('customer_is_deleted'))
        # context['number_of_actives'] = number_of_actives
        # console.log(f'the context transftered here is {context}' )
        # context['form'] = CustomerModelForm()
        # Create any data and add it to the context
        context['addl'] = 'comments about repairorders list view'
        return context

    def get_queryset(self):
        return RepairOrdersNewSQL02Model.objects.order_by('-repair_order_id')