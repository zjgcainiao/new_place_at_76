import os
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
# repairOrder model was added on 11/5/2022. Deleted on 11/18/2022
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json

from appointments.forms import AppointmentRequestForm
from appointments.models import AppointmentRequest
from django.views.generic import CreateView, FormView, TemplateView
from formtools.wizard.views import WizardView
from django.urls import reverse_lazy
import calendar

def fetch_master_calendar_view(request):
    return render(request, 'appointments/index.html')
    
# 2023-04-10 created by ChatGPT4.0 
def appointment_create_view(request):
    form = AppointmentRequestForm(request.POST or None)
    # form = AppointmentRequestForm(request.POST)
    if form.is_valid():
        appointment_data = form.cleaned_data
        appointment_data = json.dumps(appointment_data, default=str)
        request.session['appointment_data'] = appointment_data
        # request.session['submitted_form'] = json.dumps(form, default=dict)[0]
        # json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)
        # appointment = form.save(commit=False)
        # appointment.appointment_requested_datetime = timezone.now()
        # appointment.save()
        # kwargs = {'appointment': appointment}
        # TODO: Send email to customer about service request status

        return redirect('appointments:appointment-preview-view')
        # return redirect('appointment_preview', args=[appointment.appointment_id])
    context = {'form': form}

    return render(request, 'appointments/01-appointment-create.html', context)

def appointment_preview_view(request):
    # appointment = kwargs.get('appointment', None)
    appointment_data = request.session.get('appointment_data')
    # submitted_form = request.session.get('submitted_form')
    if not appointment_data:
        return redirect('appointments:appointment-create')
    # 2024-04-10 using json.loads to load back the appointment_data.
    # otherwise appointment_data will be 
    appointment_data = json.loads(appointment_data)
# if request.method == 'GET':
    form = AppointmentRequestForm(appointment_data)
    appointment = AppointmentRequest(**appointment_data)
    context = {'form': form,
               'appointment': appointment,
               }
    if request.method == 'POST':
        appointment.appointment_status ='C'
        appointment.save()
        messages.success(request, 'Appointment has been submitted successfuly.')
        request.session.pop('appointment_data')
        return redirect('appointments:appointment-success-view')
    return render(request, 'appointments/02-appointment-preview.html', context)
    # #     form = AppointmentRequestForm(request.POST)
    # #     if form.is_valid():
    # #         appointment = form.save(commit=False)
    # #         appointment.appointment_status = 'C'
    # #         appointment.save()
        # form = AppointmentRequestForm(request.POST)
        # if form.is_valid():
        #     appointment = AppointmentRequest(form.fields)
        #     appointment.save()
        #     messages.success(request, 'Appointment has been submitted successfuly.')
        #     request.session.pop('appointment_data')
        # # send_appointment_confirmation_email(appointment)
        #     return redirect('appointments:appointment-success')
        # return redirect('appointment_success')
        # form = AppointmentRequestForm(initial=kwargs)
        # return render(request, 'appointments/02-appointment-preview.html', {'form': form})
        # elif 'confirm' in request.POST:
        #     form = AppointmentRequestForm(request.POST)
        #     if form.is_valid():
        #         appointment = form.save(commit=False)
        #         appointment.appointment_status = 'C'
        #         appointment.save()
        #         # Send confirmation email -- pending
        #         # 2023-04-10
        #         # subject = 'Appointment Confirmed'
        #         # html_message = render_to_string('appointment_confirmation_email.html', {'appointment': appointment})
        #         # plain_message = strip_tags(html_message)
        #         # from_email = 'Your Company <noreply@yourcompany.com>'
        #         # to_email = appointment.appointment_email
        #         # send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        # # else:
        # #     return redirect('appointment-create-view')
        # # form = AppointmentRequestForm()
    
    # context = {'form': form}
    # return render(request, 'appointments/02-appointment-preview.html', context)
    # return redirect('appointment-create-view')

def appointment_success(request):
    return render(request, 'appointments/03-appointment-creation-success.html')


class AppointmentCreateView(CreateView):
    model = AppointmentRequest
    form_class = AppointmentRequestForm
    template_name = 'appointments/01-appointment-create.html'
    success_url = reverse_lazy('appointments:appointment-preview-view')

class AppointmentPreviewView(FormView):
    template_name = 'appointments/02-appointment-preview.html'
    form_class = AppointmentRequestForm
    success_url = reverse_lazy('appointments:appointment-success-view')

    def form_valid(self, form):
        self.request.session['appointment_data'] = self.request.POST
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.session.get('appointment_data', {})
        return kwargs

class AppointmentSuccessView(TemplateView):
    template_name = 'appointments/03-appointment-creation-success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment_data = self.request.session.get('appointment_data', {})
        if appointment_data:
            appointment = AppointmentRequest(**appointment_data)
            appointment.save()
            self.request.session['appointment_data'] = None
            context['appointment'] = appointment
        return context