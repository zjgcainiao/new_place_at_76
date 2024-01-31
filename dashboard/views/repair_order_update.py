
from .base import LoginRequiredMixin, UpdateView, reverse_lazy, get_object_or_404, redirect,reverse
from homepageapp.models import RepairOrdersNewSQL02Model
from dashboard.forms import RepairOrderUpdateForm

class RepairOrderUpdateView(UpdateView, LoginRequiredMixin):
    template_name = 'dashboard/52_repairorder_updateview.html'
    model = RepairOrdersNewSQL02Model
    # fields = '__all__'
    form_class = RepairOrderUpdateForm
    # success_url = reverse_lazy(
    #     'dashboard:wip_detail_v1', pk=self.kwargs['object.repair_order_id'])
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_success_url(self):
        return reverse('dashboard:wip_detail_v1', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            RepairOrdersNewSQL02Model, pk=self.kwargs['pk'])
        form = RepairOrderUpdateForm(request.POST, instance=self.object)
        if form.is_valid():
            # self.object.repair_order_last_updated_at = timezone.now()
            form.save()
            # return HttpResponseRedirect(self.get_success_url())
            return redirect(reverse_lazy('dashboard:wip_detail_v1', pk=self.kwargs['pk']))
        else:
            # return self.form_invalid(form)
            return self.render_to_response(self.get_context_data(form=form))