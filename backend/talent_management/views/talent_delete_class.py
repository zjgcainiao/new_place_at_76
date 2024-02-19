from .base import render, redirect, messages, LoginRequiredMixin, DeleteView, \
                TalentsModel, reverse_lazy, CURRENT_TIME_SHOW_PRECISE_TIME_WITH_TIMEZONE

class TalentDeleteView(DeleteView, LoginRequiredMixin):
    model = TalentsModel
    template_name = 'talent_management/60_talent_delete.html'
    # Redirect to customer list after "deletion"
    success_url = reverse_lazy('talent_management:talent_list')

    def form_valid(self, form):
        self.object = form.instance
        # Soft delete: mark as inactive
        self.object.talent_is_active = False
        if self.object.talent_incident_record_json:
            self.object.talent_incident_record_json.append(
                {CURRENT_TIME_SHOW_PRECISE_TIME_WITH_TIMEZONE: f'this talent record {self.object.pk} is requested for a deletion. Deactivation.'})
        else:
            self.object.talent_incident_record_json = [
                {CURRENT_TIME_SHOW_PRECISE_TIME_WITH_TIMEZONE:
                    f'this talent record {self.object.pk} is requested for a deletion. Deactivation.'}
            ]

        self.object.save()
        messages.success(
            self.request, 'Talent record has been deleted successfully.')
        return redirect(self.get_success_url())
