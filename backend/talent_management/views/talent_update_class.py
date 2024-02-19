from .base import render, redirect, messages, InternalUserRequiredMixin, \
            UpdateView, TalentsModel, TalentUpdateForm, TalentAudit, timezone, \
            reverse, reverse_lazy

class TalentUpdateView(UpdateView):
    model = TalentsModel
    form_class = TalentUpdateForm
    template_name = 'talent_management/50_talent_update.html'

    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_success_url(self):
        return reverse('talent_management:talent_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.talent_last_updated_date = timezone.now()
        self.object.save()
        # After saving, compare the old and new state and log changes
        for field in TalentsModel.fields_to_track():
            old_value = self.object._initial_state[field]
            new_value = getattr(self.object, field)
            if old_value != new_value:
                TalentAudit.objects.create(
                    talent=self.object,
                    created_by=self.request.user,
                    created_at=timezone.now(),
                    field_changed=field,
                    old_value=old_value,
                    new_value=new_value
                )

        messages.success(self.request, 'Update success.')
        return redirect('talent_management:talent_detail', pk=self.kwargs['pk'])

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))