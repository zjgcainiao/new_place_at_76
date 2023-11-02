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
from appointments.forms import AppointmentCreationForm, AppointmentImagesForm
from appointments.forms import AppointmentImageFormSet
from appointments.models import AppointmentRequest, AppointmentImages
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import DetailView
from django.views.generic import ListView
from formtools.wizard.views import WizardView
from django.urls import reverse_lazy
import calendar
from formtools.wizard.views import SessionWizardView
from appointments.models import APPT_STATUS_CANCELLED, APPT_STATUS_NOT_SUBMITTED
from internal_users.models import InternalUser
from customer_users.models import CustomerUser

# 2023-11-01 revised this appointment_create_view_for_customer (request)


def appointment_create_view_for_customer(request):
    # form = AppointmentCreationForm(request.POST or None)
    if request.method == 'POST':
        # form = AppointmentCreationForm(request.POST)
        if not request.FILES:
            form = AppointmentCreationForm(request.POST)
        else:
            form = AppointmentCreationForm(request.POST, request.FILES)
        if form.is_valid():

            appointment = form.save(commit=False)
            if request.user.is_authenticated():
                user = request.user
                if isinstance(user, CustomerUser):
                    appointment.appointment_customer_user = user

                elif isinstance(user, InternalUser):
                    appointment.created_by = user
            else:
                appointment.appointment_customer_user = None

            images = request.FILES.getlist('appointment_images')

            for image in images:
                # Here we save the image temporarily or mark it as not confirmed
                temp_image = AppointmentImages(
                    appointment=appointment, image=image)
                temp_image.save()

            # Instead of saving the entire form data in the session, just save the ID
            request.session['appointment_id'] = appointment.pk
            return redirect('appointments:appointment-preview-view')
        else:
            print(form.errors)  # print out the form errors

            # return redirect('appointment_preview', args=[appointment.appointment_id])
    else:
        form = AppointmentCreationForm()

    context = {'form': form, }

    return render(request, 'appointments/10_appointment_create.html', context)


def appointment_preview_view(request):
    appointment_id = request.session.get('appointment_id')
    if appointment_id:
        appointment = AppointmentRequest.objects.get(pk=appointment_id)
        images = AppointmentImages.objects.filter(appointment=appointment)
        context = {'appointment': appointment, 'images': images}
        return render(request, 'appointments/21_appointment_preview.html', context)
    else:
        # Handle the case where there is no appointment_id in the session
        return redirect('appointments:create_appointment')


def appointment_success(request):
    return render(request, 'appointments/22_appointment_creation_success.html')


# version 2 of appointment creation.
class AppointmentCreateView(SessionWizardView):
    # def get_template_names(self):
    #     return ['appointments/12_appointment_create_v2_step_1.html', 'appointments/13_appointment_create_v2_step_2.html']
    template_name = 'appointments/10_appointment_create_v2.html'

    file_storage = FileSystemStorage(location=os.path.join(
        settings.DEFAULT_FILE_STORAGE, 'appointment_images'))
    form_list = [
        ('upload images', AppointmentImageFormSet),
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
        return redirect('appointments:appointment-preview-view')


class AppointmentPreviewView(FormView):
    template_name = 'appointments/21_appointment_preview.html'
    # form_class = AppointmentCreationForm
    success_url = reverse_lazy('appointments:appointment-success-view')

    def form_valid(self, form):
        self.request.session['appointment_data'] = self.request.POST
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.session.get('appointment_data', {})
        return kwargs


class AppointmentSuccessView(TemplateView):
    template_name = 'appointments/22_appointment_creation_success.html'

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
    template_name = 'appointments/20_appointment_list.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        qs = AppointmentRequest.objects.prefetch_related(
            'appointment_repair_order').exclude(appointment_status=APPT_STATUS_CANCELLED).all()
        # qs=qs.filter(appointment_status=APPT_STATUS_CANCELLED)
        # select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.

        return qs


class AppointmentDetailView(DetailView):
    model = AppointmentRequest
    context_object_name = 'appointment'
    template_name = 'appointments/30_appointment_detail.html'
    # login_url = '/users/login'

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


class AppointmentDetailByConfirmationIdView(AppointmentDetailView):
    def get_queryset(self):
        queryset = AppointmentRequest.objects.filter(
            appointment_confirmation_id=self.args['appointment_confirmation_id'])
        return queryset


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
    return render(request, 'appointments/21_appointment_image_list.html', {'images': images, 'appointment': appointment})


def appointment_image_soft_delete(request, image_id):
    image = get_object_or_404(AppointmentImages, image_id=image_id)
    image.image_is_active = False
    image.save()
    messages.add_message(request, messages.INFO,
                         "Image selected has been deleted.")
    return redirect('appointment:appointment_image_list')
