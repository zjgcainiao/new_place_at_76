from django.forms import ValidationError
from traitlets import default
from core_operations.constants import LIST_OF_STATES_IN_US
from homepageapp.models import PersonalItem, PersonalItemImage
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core_operations.utilities import generate_code128_barcode_lite

from .base import forms, FormHelper, Layout, Fieldset, Submit, Field, \
    ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden, logger

from appointments.custom_validators import validate_vehicle_year, validate_file_size
from django.core.validators import FileExtensionValidator


class PersonalItemUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True)

    # Add the image field from AppointmentImages
    item_images = forms.ImageField(
        required=False,
        label=_("Item Images"),
        widget=forms.ClearableFileInput(),
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']),
                    validate_file_size],
        help_text="Up to 5 images(png, jpg, jpeg, etc). 8MB each",

    )

    class Meta:
        model = PersonalItem
        fields = ['id',
                  'item_original_barcode',
                  'name',
                  'item_category',
                  'is_storage_container',
                  'description',
                  'dimensional_size',
                  'location',

                  #   'is_active',
                  ]
        # exclude = ('created_at', 'updated_at',)
        widgets = {
            'item_category': forms.Select(attrs={'class': ' form-select', }),
            'item_original_barcode': forms.TextInput(attrs={'placeholder': 'the original barcode created by the manufacturer'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter item name'}),
            'description': forms.TextInput(attrs={'placeholder': 'describe the item, e.g. color, size, etc.'}),
            'dimensional_size': forms.TextInput(attrs={'placeholder': 'e.g. 10x10x10 inches'}),
            'location': forms.TextInput(attrs={'placeholder': 'Follow the naming format: <branch-id or address>-<aisle>-<rack>-<level>-<slot>. Default to 3301 West Warner'}),
            # "is_active": forms.CheckboxInput(attrs={'type': 'checkbox', 'disabled': 'False'}),
        }
        labels = {
            'item_category': _('Item Category'),
            'item_original_barcode': _('Original (Manufacturer) Barcode'),
            'name': _('Name'),
            'description': _('Description'),
            'dimensional_size': _('Dimensional Size'),
            'location': _('Location'),
            # 'is_active': _('Is Active'),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control text-input'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {'class': 'form-control textarea-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'datetime-input'})
            # You can continue for other field types

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = "post"
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        # self.helper.error_text_inline = True
        # self.helper.use_custom_control = True  # for Bootstrap custom controls

        # Custom popover button
        # updated with jQuery popover udpate
        popover_html = """

        """

        self.helper.layout = Layout(
            Fieldset(
                _('Personal Item Information'),
                Row(
                    Column('name', css_class='col-md-6'),
                    # Adding the popover button
                    # Column(HTML(popover_html), css_class='col-md-6'),
                    Column('item_category', css_class='col-md-6'),
                    Hidden('is_storage_container', value=''),
                ),
                Row(
                    Column('item_original_barcode', css_class=' col-md-6'),
                    Column('dimensional_size', css_class=' col-md-6'),
                ),
                Row(
                    Column('description', css_class='col-md-12'),

                ),

                Row(
                    Column('location',
                           css_class='col-md-12'),
                ),
                # personal-item-image upload section.
                Row(
                    Column(
                        Field('item_images', css_class='form-control'),
                        css_class='col-md-6'
                    ),
                    css_class='p-1 m-1'),
                # no longer needs this "upload" button
                # Row(Column(Button('upload', 'Upload', css_class='btn-outline-dark', css_id='appt-img-upload-btn'), css_class='col'),
                #     css_class='m-1 p-1'),


            ),

            ButtonHolder(
                Row(
                    Column(Submit('submit', 'Apply',
                                  css_class='btn btn-primary',
                                  css_id='submit-button', style="float: left;"),
                           css_class='col-md-6'),
                    Column(Button('cancel', 'Cancel', css_class='btn btn-secondary',
                                  css_id='cancel-button', style="float: right;"),
                           css_class='col-md-6'),
                    css_class='p-1 m-1'),
            ),
        )

    def clean_item_images(self):
        images = self.files.getlist('item_images')
        print(f'images captured during form cleaning function: {images}')
        if len(images) > 5:
            raise ValidationError("You can only upload a maximum of 5 images.")

    def save(self, commit=True):

        # First, call the parent's save method with `commit=False` to avoid saving too early
        instance = super().save(commit=False)
        print(f'instance to be saved: {instance}')
        # Check if the instance has a primary key (existing object) or not (new object)
        if instance.pk:
            try:
                # Retrieve the original instance from the database to compare item_category
                original_instance = PersonalItem.objects.get(pk=instance.pk)
                original_item_category = original_instance.item_category
            except PersonalItem.DoesNotExist:
                original_item_category = None
        else:
            # If it's a new instance, there's no original item category
            original_item_category = None
        # Setting container status based on category

        if instance.item_category == 'storage_containers':
            instance.is_storage_container = True

        # Setting the default location
        if not instance.location:
            instance.location = '3301 West Warner Ave, Santa Ana, CA 92704 - 0 - 0 - 0 - 0'

        # Generate barcode using the updated function, passing in the relevant product/category ID. in this case, item_category
        # Determine if the barcode should be regenerated:
        # - If the original barcode is empty
        # - If the item_category has changed
        if not instance.barcode_full_code or \
                (original_item_category and
                 instance.item_category != original_item_category
                 ):

            # Generate the barcode
            barcode_full_code, barcode_content_file = \
                generate_code128_barcode_lite(
                    instance.item_category
                )

            # Attach the barcode information to the instance
            instance.barcode_full_code = barcode_full_code
            instance.barcode_image.save(
                barcode_content_file.name, barcode_content_file, save=False)

        if commit:

            instance.save()
            # Retrieve the list of uploaded images
            images = self.files.getlist('item_images')
            logger.info(
                f'images captured during form saving function: {images}')
            if images:
                for image in images:
                    PersonalItemImage.objects.create(
                        personal_item=instance,
                        image=image,
                    )

        return instance
