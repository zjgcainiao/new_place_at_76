from .base import FormPreview, TalentsModel, messages, redirect

class TalentCreatePreview(FormPreview):
    # 'talent_management/40_talent_creation.html'
    form_template = 'talent_management/41_talent_creation_preview.html'
    # preview_template = 'talent_management/41_talent_creation_preview.html'

    def done(self, request, cleaned_data):
        # Save the form data or perform any necessary actions
        TalentsModel.objects.create(**cleaned_data)
        # Add a success message
        messages.success(request, "Talent created successfully.")
        return redirect('talent_management:talent_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context variables needed for preview template
        return context
