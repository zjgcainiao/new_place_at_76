
from .base import render,  messages,redirect
from homepageapp.models import RepairOrdersNewSQL02Model, TextMessagesModel, AddressesNewSQL02Model,NoteItemsNewSQL02Model
from customer_users.models import CustomerUser
from internal_users.models import InternalUser
from dashboard.forms import RepairOrderUpdateForm
from appointments.forms import AppointmentCreationForm

def appointment_create_view_for_customer(request):
    # form = AppointmentCreationForm(request.POST or None)
    if request.method == 'POST':

        form = AppointmentCreationForm(request.POST, request.FILES or None)
        if form.is_valid():
            # Save the appointment instance but do not commit to the database yet
            appointment = form.save(commit=False)
            if request.user.is_authenticated:
                user = request.user
                if isinstance(user, CustomerUser):
                    appointment.appointment_customer_user = user

                elif isinstance(user, InternalUser):
                    appointment.created_by = user
            else:
                appointment.appointment_customer_user = None
            # Now save the appointment instance to the database
            appointment.save()

            # Now that the appointment instance is saved, you can save related images
            form.save_m2m()  # Save many-to-many data for the form
            form.save(commit=True)  # Now save the images
            messages.info(request,
                          "Here is the preview of your service appointment request. \
                            Your appointment has NOT submitted yet. Please use the submit button below to proceed.")
            return redirect('appointments:appointment_preview_view', pk=appointment.pk)
        else:
            print(form.errors)  # print out the form errors

            # return redirect('appointment_preview', args=[appointment.appointment_id])
    else:
        form = AppointmentCreationForm()

    context = {'form': form, }

    return render(request, 'appointments/10_appointment_create.html', context)