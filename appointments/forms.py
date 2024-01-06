from django import forms
import re
from appointments.models import AppointmentRequest, AppointmentImages
from datetime import date, datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from appointments.models import APPT_STATUS_PORGRESSING, APPT_STATUS_CONFIRMED, APPT_STATUS_SUBMITTED
from core_operations.common_functions import get_latest_vehicle_make_list, get_latest_vehicle_model_list
from homepageapp.models import MakesNewSQL02Model
from django.db.models import Q
from django.core.validators import FileExtensionValidator

from internal_users.models import InternalUser
from customer_users.models import CustomerUser
from django.contrib.contenttypes.models import ContentType
from core_operations.models import US_COUNTRY_CODE
from core_operations.common_functions import format_phone_number_to_shop_standard, deformat_phone_numbers
from appointments.custom_validators import validate_vehicle_year, validate_file_size, validate_phone_number


class AppointmentCreationForm(forms.ModelForm):

    appointment_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'type': 'text', 'placeholder': 'example: johnson.goku@gmail.com'}),
        label=_('Contact Email'), help_text="Required. Will send important updates to this email.")
    # Add your custom fields
    appointment_vehicle_year = forms.IntegerField(
        required=False,
        validators=[validate_vehicle_year],
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'model year, 2024, 2023 etc.', }),
        label=_('Year'),

    )

    appointment_vehicle_make = forms.ChoiceField(
        required=False,
        choices=get_latest_vehicle_make_list, label='Make')
    appointment_vehicle_model = forms.ChoiceField(
        required=False,
        choices=get_latest_vehicle_model_list, label='Model')

    appointment_phone_number = forms.CharField(required=False,
                                               validators=[
                                                   validate_phone_number],
                                               widget=forms.TextInput(attrs={
                                                                      'type': 'text', 'placeholder': 'Enter a US phone number. Ex.: (231)456-9809.'}),
                                               label=_('Contact Phone'), help_text="we send important updates & reminders to this number.")

    appointment_concern_description = forms.CharField(widget=forms.Textarea(attrs={'type': 'text', 'placeholder': 'Examples: 1. I want to do a oil change for 2020 Toyota Sienna. Full Synthetic as usual. 2. My A/C system does not cool enough during a hot day. Last week, i drove to ... 3. The engine acted weird this morning, the car suddenly lost power on a freeway ramp...'}),
                                                      label='Desribe your issue as detailed as you can.')

    # appointment_requested_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'datetime-local','class':'form-control'}))
    # appointment_requested_time = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control datetimepicker-input'}))
    # attrs={'type': 'datetime-local', }

    # Add the image field from AppointmentImages
    appointment_images = forms.ImageField(
        required=False,
        label=_("Images"),
        widget=forms.ClearableFileInput(),
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']),
            validate_file_size],
        help_text="up to 5 images(png, jpg, jpeg, etc). 8MB each"
    )

    class Meta:
        model = AppointmentRequest
        exclude = ('created_at', 'updated_at',)
        fields = [
            'appointment_reason_for_visit',
            'appointment_requested_datetime',
            'appointment_first_name',
            'appointment_last_name',
            'appointment_email',
            'appointment_phone_number',
            'appointment_vehicle_year',
            'appointment_vehicle_make',
            'appointment_vehicle_model',
            'appointment_concern_description',

            # 'appointment_vehicle_detail',
            # 'appointment_vehicle_detail_in_json',
        ]
        widgets = {
            # , 'class':'form-control
            'appointment_requested_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', }),
            # 'type': 'text','class': 'form-control'
            'appointment_first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'first name'}),
            'appointment_last_name': forms.TextInput(attrs={'type': 'text', 'placeholder': 'last name', }),
            # 'appointment_reason_for_visit': forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            # 'appointment_vehicle_detail': forms.TextInput(attrs={'type': 'text','placeholder':'for example: 2020 Toyota Tocoma SE, or 2021 Mercedez C300 AWD.'}),
            'appointment_concern_description': forms.Textarea(attrs={'type': 'text', }),
        }

        labels = {
            'appointment_reason_for_visit': _('Reason for Visit'),
            'appointment_requested_datetime': _('Appointment Time'),
            'appointment_first_name': _('First Name'),
            'appointment_last_name': _('Last Name'),
            'appointment_email': _('Email'),
            'appointment_phone_number': _('Phone Number'),
            'appointment_vehicle_detail': _('Vehicle Detail'),
            'appointment_concern_description': _('Desribe your issue as detail as you can.'),
            'appointment_vehicle_year': _('Year'),
            'appointment_vehicle_make': _('Make'),
            'appointment_vehicle_model': _('Model'),
        }

    # def save(self, commit=False):
    #     # First save the appointment instance
    #     appointment = super().save(commit)

    #     # If image data exists, save them
    #     for img_file in self.files.getlist('appointment_images'):
    #         image_instance = AppointmentImages(
    #             appointment=appointment,
    #             appointment_image=img_file,
    #         )
    #         image_instance.save()

    #     return appointment

    def save(self, commit=True):
        # Save the appointment instance
        # Make sure to save the appointment first
        appointment = super().save(commit=commit)

        if commit:  # If we are committing the save to the database
            # If image data exists, save them
            for img_file in self.files.getlist('appointment_images'):
                AppointmentImages.objects.create(
                    appointment=appointment,
                    appointment_image=img_file,
                )

        return appointment

    def clean_appointment_email(self):
        appointment_email = self.cleaned_data['appointment_email']
        if appointment_email is not None:
            appt = AppointmentRequest.objects.filter(Q(appointment_status=APPT_STATUS_SUBMITTED) | Q(appointment_status=APPT_STATUS_CONFIRMED) | Q(appointment_status=APPT_STATUS_PORGRESSING)
                                                     ).filter(appointment_email=appointment_email)
            # existing pending/in-progresss/confirmed/
            if appt.exists():
                error_message = "There is an existing appointment associated with this email. "
                error_attrs = {'class': 'alert alert-warning', 'role': "alert"}
                raise forms.ValidationError(error_message, params=error_attrs)

            return appointment_email
        else:
            raise ValueError('email cannot be empty.')

    # check
    def clean_appointment_vehicle_detail(self):

        if not self.cleaned_data['appoinment_vehicle_year'] and not self.cleaned_data['appointment_vehicle_make'] and not self.cleaned_data['appointment_vehicle_model']:
            appointment_vehicle_detail = ''.join([self.cleaned_data['appoinment_vehicle_year'], "_",
                                                 self.cleaned_data['appoinment_vehicle_make'], "_", self.cleaned_data['appoinment_vehicle_model']])
        else:
            appointment_vehicle_detail is None
        return appointment_vehicle_detail

    def clean_appointment_phone_number(self):
        phone_number = self.cleaned_data['appointment_phone_number']
        if phone_number:
            phone_number_formatted = format_phone_number_to_shop_standard(
                phone_number)
        else:
            phone_number_formatted = None

        return phone_number_formatted

    def clean(self):
        # cleaned_data = super().clean()
        images = self.files.getlist('appointment_images')
        if len(images) > 5:
            raise ValidationError("You can only upload a maximum of 5 images.")

    def __init__(self, *args, **kwargs):
        # add a request into the keyword arguments in the form

        # self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

        # self.fields['appointment_vehicle_make'].choices = [(make.pk, make.make_name) for make in MakesNewSQL02Model.objects.all()]

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        # self.helper.label_class = 'col-md-3'
        # self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Row(Fieldset(_('Time and Contact Info'),
                Row(Column(Field('appointment_email', css_class='form-control'),
                           css_class='col-md-6',),
                    Column(Field('appointment_phone_number', css_class='form-control', style="background-color: #cfe2f3"),
                           css_class='col-md-6',),
                    css_class='p-1 m-1'),
                Row(
                    Column(Field('appointment_first_name', css_class='form-control'),
                           css_class='col-md-6',),
                    Column(Field('appointment_last_name', css_class='form-control'),
                           css_class='col-md-6',),
                    css_class='p-1 m-1'),

                Row(
                    # Column(Field('appointment_requested_date', css_class='form-control'),
                    #     css_class='col-md-6',),
                    # Column(Field('appointment_requested_time', css_class='form-control'),
                    #     css_class='col-md-6',),
                    Column(Field('appointment_requested_datetime', css_class='form-control'),
                           css_class='col-md-6',),
                    Column(Field('appointment_reason_for_visit', css_class='form-select'),
                           css_class='col-md-6',),
                    css_class='p-1 m-1'),
            ),
                css_class='p-1 m-1'),

            HTML("<hr>"),

            Row(
                Fieldset(_('Describe your service requests or issues:'),
                         # Div(Column(Field('appointment_vehicle_detail',css_class='form-control'),
                         #     css_class='col col-12'),
                         #     css_class='p-1'),
                         # 'appointment_vehicle_detail_in_json',
                         Row(
                    Column(Field('appointment_vehicle_year', css_class='form-control'),
                           css_class='col-md-4',),
                    Column(Field('appointment_vehicle_make', css_class='form-select'),
                           css_class='col-md-4',),
                    Column(Field('appointment_vehicle_model', css_class='form-select'),
                           css_class='col-md-4 ',),
                    css_class='p-1'),
                ),
                css_class='p-1 m-1'),

            HTML("<hr>"),

            Row(
                Column(Field('appointment_concern_description', css_class='form-control'),
                       css_class='col-md-12'),
                css_class='p-1 m-1'),

            HTML("<hr>"),

            # appointment-image upload section.
            Row(
                Column(
                    Field('appointment_images', css_class='form-control'),
                    css_class='col-md-6'
                ),
                css_class='p-1 m-1'),
            # no longer needs this "upload" button
            # Row(Column(Button('upload', 'Upload', css_class='btn-outline-dark', css_id='appt-img-upload-btn'), css_class='col'),
            #     css_class='m-1 p-1'),
            HTML("<hr>"),

            ButtonHolder(
                Row(
                    Column(Submit('submit', 'Submit', css_class='btn-outline-primary'),
                           css_class='col'),
                    # Column(Reset('Reset This Form', 'Reset Form', css_class='btn-outline-dark'),
                    #         css_class='col col-6'),
                    css_class='p-1 m-1'),
            ),
        )
        # self.helper.add_input(Reset('Reset This Form', 'Reset Me!'))
    # appointment_requested_datetime = forms.DateTimeField()


class AppointmentRequestFormV2(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.label_class = 'col-4'
        self.helper.field_class = 'col-8'
        self.helper.layout = Layout(
            Fieldset(_('Basic Info'),
                     Field('appointment_requested_datetime',
                           css_class='form-control'),

                     Field('appointment_reason_for_visit',
                           css_class='form-control'),
                     Field('appointment_first_name', css_class='form-control'),
                     Field('appointment_last_name', css_class='form-control'),
                     'appointment_email',
                     'appointment_phone_number',
                     'appointment_concern_description',
                     ),
            Fieldset(_('Vehicle Info'),
                     'appointment_vehicle_year',
                     'appointment_vehicle_make',
                     'appointment_vehicle_model',
                     'appointment_vehicle_detail'
                     'appointment_vehicle_detail_in_json',
                     ),
            # Field('appointment_email', id="appointment_email_field", css_class= "form-control"),
            ButtonHolder(
                HTML(
                    "<span style='display: hidden;'>Appointment Request Submitted.</span>"),
                Submit('submit', 'Submit', css_class='btn btn-outline-danger')
            ),
        )
        self.helper.add_input(Reset('Reset This Form', 'Reset Me!'))

    class Meta:
        model = AppointmentRequest
        fields = [
            'appointment_reason_for_visit',
            'appointment_requested_datetime',
            'appointment_phone_number',
            'appointment_email',
            'appointment_first_name',
            'appointment_last_name',
            'appointment_vehicle_detail',
            'appointment_concern_description',
            'appointment_vehicle_detail_in_json',
        ]


class AppointmentImagesForm(forms.ModelForm):
    appointment_image = forms.ImageField(
        widget=forms.ClearableFileInput(),
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']),
                    validate_file_size],
        label=_('Images'),
        help_text=_('Upload up to 5 images ( maximum size: 8 MB each)'),
    )

    def clean_appointment_image(self):
        image = self.cleaned_data.get('appointment_image')
        if image:
            if image.size > 8*1024*1024:  # image file size limit of 8MB
                raise ValidationError(
                    "Image file too large - must be 8 MB or less.")
        return image

    class Meta:
        model = AppointmentImages
        fields = ["appointment_image",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.form_class = "form-inline"
        # self.helper.label_class = 'col-3'
        # self.helper.field_class = 'col-9'
        self.helper.layout = Layout(
            Column(Field('appointment_image', css_class='form-control'),
                   css_class='col col-md-12')

        )


AppointmentImageFormSet = inlineformset_factory(
    AppointmentRequest, AppointmentImages,
    form=AppointmentImagesForm, fk_name='appointment',
    # can_order=True, can_delete=True,

    extra=1, max_num=5)
