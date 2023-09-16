from homepageapp.models import ModelsNewSQL02Model
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
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
from django.contrib.auth.mixins import LoginRequiredMixin
from appointments.forms import AppointmentRequestForm, AppointmentRequestFormV2, AppointmentImagesForm
from appointments.forms import AppointmentImagesForm, AppointmentImageFormSet
from appointments.models import AppointmentRequest, AppointmentImages
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import DetailView
from django.views.generic import ListView
from formtools.wizard.views import WizardView
from django.urls import reverse_lazy
import calendar
from formtools.wizard.views import SessionWizardView
from appointments.models import APPT_STATUS_CANCELLED, APPT_STATUS_NOT_SUBMITTED


# 2023-04-10

def appointment_create_view_for_customer(request):
    # form = AppointmentRequestForm(request.POST or None)
    if request.method == 'POST':
        # form = AppointmentRequestForm(request.POST)
        form = AppointmentRequestForm(request.POST, request.FILES)
        image_formset = AppointmentImageFormSet(
            request.POST, request.FILES, user=request.user)
        image_form = AppointmentImagesForm(
            request.POST, request.FILES, user=request.user)
    # form = AppointmentRequestForm(request.POST)
        if form.is_valid():  # and image_formset.is_valid()
            # form.save()
            form.save(commit=False)
            appointment_data = form.cleaned_data
            # appointment_data.user = request.user
            appointment_data = json.dumps(appointment_data, default=str)
            request.session['appointment_data'] = appointment_data
            # request.session['images'] = [image_form.cleaned_data for image_form in image_formset]
            # request.session['submitted_form'] = json.dumps(form, default=dict)[0]
            # json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)
            # appointment = form.save(commit=False)
            # appointment.appointment_requested_datetime = timezone.now()
            # appointment.save()
            # kwargs = {'appointment': appointment}
            # TODO: Send email to customer about service request status

            return redirect('appointments:appointment-preview-view')
        else:
            print(form.errors)  # print out the form errors
            # return redirect('appointment_preview', args=[appointment.appointment_id])
    else:
        form = AppointmentRequestForm
        image_formset = AppointmentImageFormSet(
            queryset=AppointmentImages.objects.none())
        image_form = AppointmentImagesForm()
    # context = {'form': form}
    context = {'form': form, 'image_formset': image_formset,
               'image_form': image_form}

    return render(request, 'appointments/10_appointment_create.html', context)


def appointment_preview_view(request):
    # appointment = kwargs.get('appointment', None)
    appointment_data = request.session.get('appointment_data')
    images = request.session.get('images')
    # submitted_form = request.session.get('submitted_form')
    if not appointment_data:
        return redirect('appointments:appointment-create-view')
    # 2024-04-10 using json.loads to load back the appointment_data.
    # otherwise appointment_data will be
    appointment_data = json.loads(appointment_data)
    images = json.loads(images)
# if request.method == 'GET':
    form = AppointmentRequestForm(appointment_data)
    appointment = AppointmentRequest(**appointment_data)
    context = {'form': form,
               'appointment': appointment,
               }
    if request.method == 'POST':
        appointment.appointment_status = APPT_STATUS_NOT_SUBMITTED
        appointment.save()
        messages.success(
            request, 'Appointment has been submitted successfuly.')
        request.session.pop('appointment_data')
        return redirect('appointments:appointment-success-view')
    return render(request, 'appointments/20_appointment_preview.html', context)

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
    return render(request, 'appointments/30_appointment_creation_success.html')


# version 2 of appointment creation.


class AppointmentCreateView(SessionWizardView):
    # def get_template_names(self):
    #     return ['appointments/12_appointment_create_v2_step_1.html', 'appointments/13_appointment_create_v2_step_2.html']
    template_name = 'appointments/11_appointment_create_v2.html'

    file_storage = FileSystemStorage(location=os.path.join(
        settings.DEFAULT_FILE_STORAGE, 'appointment_images'))
    form_list = [
        ('upload images', AppointmentImageFormSet),
        ('new_appointment', AppointmentRequestForm),
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
        return redirect('appointments:appointment-preview-view')


class AppointmentPreviewView(FormView):
    template_name = 'appointments/20_appointment_preview.html'
    # form_class = AppointmentRequestForm
    success_url = reverse_lazy('appointments:appointment-success-view')

    def form_valid(self, form):
        self.request.session['appointment_data'] = self.request.POST
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.session.get('appointment_data', {})
        return kwargs


class AppointmentSuccessView(TemplateView):
    template_name = 'appointments/30_appointment_creation_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment_data = self.request.session.get('appointment_data', {})
        if appointment_data:
            appointment = AppointmentRequest(**appointment_data)
            appointment.save()
            self.request.session['appointment_data'] = None
            context['appointment'] = appointment
        return context


class AppointmentListView(LoginRequiredMixin, ListView):
    model = AppointmentRequest
    context_object_name = 'appointments'
    template_name = 'appointments/50_appointment_list.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        qs = AppointmentRequest.objects.prefetch_related(
            'appointment_repair_order').exclude(appointment_status=APPT_STATUS_CANCELLED).all()
        # qs=qs.filter(appointment_status=APPT_STATUS_CANCELLED)
        # select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.

        return qs


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = AppointmentRequest
    context_object_name = 'appointment'
    template_name = 'appointments/60_appointment_detail_view.html'
    login_url = '/users/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AppointmentImagesForm()
        return context

    def post(self, request, *args, **kwargs):
        appointment = self.get_object()
        form = AppointmentImagesForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.appointment = appointment
            image.save()
        return self.get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     talent = self.get_object()
    #     form = TalentDocumentsForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         document = form.save(commit=False)
    #         document.talent = talent
    #         document.save()
    #     return self.get(request, *args, **kwargs)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user=self.request.user)


def appointment_get_vehicle_models(request, make_id):
    models = ModelsNewSQL02Model.objects.filter(
        make_id=make_id).all().order_by('model_name')
    model_dict_list = list(models.values('model_id', 'model_name'))
    model_tuple_list = [(model.pk, model.model_name) for model in models]
    # return JsonResponse(model_tuple_list, safe=False)
    return JsonResponse(model_dict_list, safe=False)


def appointment_image_list(request, pk):
    appointment = AppointmentRequest.objects.get(pk=pk)
    images = AppointmentImages.objects.filter(
        image_is_active=True).filter(appointment=appointment).all()
    return render(request, 'appointments/70_appointment_image_list.html', {'images': images, 'appointment': appointment})


def appointment_image_soft_delete(request, image_id):
    image = get_object_or_404(AppointmentImages, image_id=image_id)
    image.image_is_active = False
    image.save()
    messages.add_message(request, messages.INFO,
                         "Image selected has been deleted.")
    return redirect('appointment:appointment_image_list')
