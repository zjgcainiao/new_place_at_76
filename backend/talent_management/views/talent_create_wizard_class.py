
from .base import TalentsModel, TalentAudit,InternalUserRequiredMixin, reverse_lazy, ListView, Q, re, \
                    messages, render, InternalUser, SessionWizardView,TALENT_CREATE_FORMS, \
                    redirect, HttpResponse, CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, timezone

class TalentCreateWizardView(SessionWizardView):

    # form_list = [
    #     ('personal_and_contact_info', PersonalContactInfoForm),
    #     ('employment_info', EmploymentInfoForm),
    #     ('remarks_and_comments', RemarkAndCommentsForm),
    # ]
    form_list = TALENT_CREATE_FORMS
    template_name = 'talent_management/42_talent_creation_v2.html'
    preview_template = 'talent_management/41_talent_creation_preview.html'

    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)

    def done(self, form_list, **kwargs):
        print(form_list)
        talent_data = {}
        for form in form_list:
            if not form.is_valid():
                # This is just a basic error handling.
                # You might want to redirect or show an error message instead.
                return HttpResponse("Error: Invalid form data.", status=400)

            talent_data.update(form.cleaned_data)

        # # Create the talent record
        # talent = TalentsModel.objects.create(**talent_data)
        # Create the talent instance but don't save it to the database yet
        talent = TalentsModel(**talent_data)
        talent.save()

        # Get the current user
        user = self.request.user

        if user.is_authenticated and isinstance(user, InternalUser):
            field = 'talent_id'
            old_value = ''
            TalentAudit.objects.create(
                talent=talent,
                # Assuming you have a method or field on Talents that holds the current user making the change
                created_by=user,
                created_at=timezone.now(),
                field_changed=field,
                old_value=old_value,
                new_value=getattr(talent, field),
            )

        # Add a success message
        messages.success(self.request, "Talent created successfully.")
        # redirect('talent_management:talent_detail', pk=self.kwargs['pk'])
        return redirect('talent_management:talent_detail', pk=talent.pk)
        # return render(self.request, 'talent_management/40_talent_creation.html', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context.update({'current_time': CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE})

        # if self.steps.current == self.steps.current:
        #     context.update({'another_var': True})
        return context

# This one uses shared_task