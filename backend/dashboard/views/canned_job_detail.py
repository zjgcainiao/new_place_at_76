from .base import DetailView, Prefetch, reverse_lazy, timezone, InternalUserRequiredMixin
from homepageapp.models import CannedJobLineItemSequence,CannedJobsNewSQL02Model
from dashboard.forms import CannedJobUpdateForm


class CannedJobDetailView(DetailView, InternalUserRequiredMixin):
    model = CannedJobsNewSQL02Model
    success_url = reverse_lazy('dashboard:canned_job_dash')
    context_object_name = 'canned_job'
    template_name = 'dashboard/51_canned_job_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current canned job instance using the object attribute (provided by DetailView)
        canned_job_instance = self.object
        
        # Query the related line items through the CannedJobLineItemSequence intermediate model
        # Note: Adjust the query according to your actual model relationships if needed
        related_line_items = CannedJobLineItemSequence.objects.filter(
            canned_job=canned_job_instance
        ).select_related('line_item').order_by('sequence')
        
        # Extract line_item objects from the sequences, ensuring they are not None
        context['related_line_items'] = [{'line_item': sequence.line_item,
                                          'sequence':sequence.sequence} for sequence in related_line_items if sequence.line_item is not None]

        # Include any additional forms or context data as needed
        if self.request.POST:
            context['form'] = CannedJobUpdateForm(self.request.POST, instance=canned_job_instance)
        else:
            context['form'] = CannedJobUpdateForm(instance=canned_job_instance)

        return context


    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = VehicleUpdateForm(request.POST, instance=self.object)
    #     if form.is_valid():
    #         self.object.vehicle_last_updated_at = timezone.now()
    #         form.save()
    #         return HttpResponseRedirect(self.get_success_url())
    #     else:
    #         return self.form_invalid(form)
            # return self.render_to_response(self.get_context_data(form=form))
