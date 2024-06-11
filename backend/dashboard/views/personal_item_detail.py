from .base import DetailView, LoginRequiredMixin, Prefetch, reverse_lazy, HttpResponseRedirect, timezone, \
    reverse
from homepageapp.models import PersonalItem, PersonalItemImage
from dashboard.forms import PersonalItemUpdateForm


class PersonalItemDetailView(DetailView, LoginRequiredMixin):
    model = PersonalItem
    # success_url = reverse_lazy('dashboard:personal_item_dash')
    context_object_name = 'item'
    template_name = 'dashboard/101_personal_item_detail.html'

    def get_success_url(self):
        return reverse('dashboard:personal_item_dash', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        items = PersonalItem.objects.filter(
            is_active=True)
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()

        # Fetch images related to this specific PersonalItem instance
        context['item_images'] = PersonalItemImage.objects.filter(
            personal_item=item)

        # Optionally, include the update form for convenience
        if self.request.POST:
            context['form'] = PersonalItemUpdateForm(
                self.request.POST, instance=item)
        else:
            context['form'] = PersonalItemUpdateForm(instance=item)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PersonalItemUpdateForm(request.POST, instance=self.object)
        if form.is_valid():
            # Update the updated_at field using the save() method
            form.instance.updated_at = timezone.now()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
            # return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
