from .base import DetailView, LoginRequiredMixin, Prefetch, reverse_lazy, \
    HttpResponseRedirect, timezone, \
    reverse, render
from homepageapp.models import MovingItem, MovingRequest
from dashboard.forms import PersonalItemUpdateForm
from django.shortcuts import get_object_or_404

# class MovingRequestDetailView(DetailView, LoginRequiredMixin):
#     model = MovingRequest
#     # success_url = reverse_lazy('dashboard:personal_item_dash')
#     context_object_name = 'moving_request'
#     template_name = 'dashboard/111_moving_request_detail.html'

#     def get_success_url(self):
#         return reverse('dashboard:moving_request_dash',
#                        kwargs={'pk': self.object.pk})

#     def get_queryset(self):
#         items = MovingRequest.objects.select_related(
#         ).filter(
#             is_active=True)
#         return items

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['form'] = PersonalItemUpdateForm(
#                 self.request.POST, instance=self.object)
#         else:
#             context['form'] = PersonalItemUpdateForm(instance=self.object)
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = PersonalItemUpdateForm(request.POST, instance=self.object)
#         if form.is_valid():
#             # Update the updated_at field using the save() method
#             form.instance.updated_at = timezone.now()
#             form.save()
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return self.form_invalid(form)
#             # return self.render_to_response(self.get_context_data(form=form))

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))


def moving_request_detail(request, pk):
    # Retrieve the moving request and its associated containers
    moving_request = get_object_or_404(MovingRequest, pk=pk)
    moving_items = moving_request.moving_items.select_related(
        'moving_item', 'container').all()

    # Create a mapping of containers to their items
    container_items = {}
    for item in moving_items:
        if item.container:
            if item.container not in container_items:
                container_items[item.container] = []
            container_items[item.container].append(item)

    context = {
        'moving_request': moving_request,
        'container_items': container_items,
    }

    return render(request, 'moving_request_detail.html', context)
