
from .base import forms, FormHelper, Layout, Column, Field, inlineformset_factory, ValidationError, FileExtensionValidator, validate_file_size
from appointments.models import AppointmentImages, AppointmentRequest
from django.utils.translation import gettext_lazy as _

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


AppointmentImageFormset = inlineformset_factory(
    AppointmentRequest, AppointmentImages,
    form=AppointmentImagesForm, fk_name='appointment',
    can_order=True, can_delete=True,

    extra=1, max_num=5)
