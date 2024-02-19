from .base import render, get_object_or_404,SessionWizardView,settings,reverse_lazy,FileSystemStorage, json,redirect, os
from appointments.forms import  AppointmentImageFormset,AppointmentCreationForm


# version 2 of appointment creation.
class AppointmentCreateView(SessionWizardView):
    # def get_template_names(self):
    #     return ['appointments/12_appointment_create_v2_step_1.html', 'appointments/13_appointment_create_v2_step_2.html']
    template_name = 'appointments/10_appointment_create_v2.html'

    file_storage = FileSystemStorage(location=os.path.join(
        settings.DEFAULT_FILE_STORAGE, 'appointment_images'))
    form_list = [
        ('upload images', AppointmentImageFormset),
        ('new_appointment', AppointmentCreationForm),
    ]

    success_url = reverse_lazy('appointments:appointment-preview-view')

    def done(self, form_list, **kwargs):
        image_formset, appointment_form = form_list
        appointment_form.save(commit=False)
        appointment_data = appointment_form.cleaned_data
        images = image_formset.save(commit=False)
        appointment_data = json.dumps(appointment_data, default=str)
        images = json.dumps(images, default=str)
        self.request.session['appointment_data'] = appointment_data
        self.request.session['images'] = images
        # talent_data = {}
        #     talent_data.update(form.cleaned_data)
        # # # Create the talent record
        # # talent = TalentsModel.objects.create(**talent_data)
        # talent = TalentsModel(**talent_data)
        # Get the current user
        # Add a success message
        # messages.success(self.request, "Talent created successfully.")
        # return redirect("talent_management:talent_list", {'talent': talent})
        return redirect('appointments:appointment_preview_view')
