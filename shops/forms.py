from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from crispy_forms.helper import FormHelper
from core_operations.constants import LIST_OF_STATES_IN_US
from crispy_forms.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden
# from crispy_forms_foundation.layout import Layout, Field, Fieldset, SplitDateTimeField, Row, Column, ButtonHolder, Submit, Hidden, Div, Button,FakeField, ButtonGroup
from crispy_forms.bootstrap import FormActions, InlineCheckboxes, InlineField
from django.urls import reverse
from django_recaptcha.fields import ReCaptchaField
from  django_recaptcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox, ReCaptchaV3

class VINSearchForm(forms.Form):
    # added this hiddent input for both VINSearchForm and LicensePlateSearchForm

    vin = forms.CharField(required=True,
                          label='VIN', widget=forms.TextInput(
                              attrs={'class': 'form-control', 'placeholder': 'enter the full vin number. Example. 1HGCM82633A004352'}))
    year = forms.CharField(required=False,
                           label='Year of Vehicle (Optional)', widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'enter model year'}), help_text="Optional. Enter only if you cannot get the result with vin only.")
    action = forms.CharField(widget=forms.HiddenInput(),
                             initial='action_vin_search')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), 
                             label='please check the box below to verify you are not a robot.')

    def clean_vin(self):
        vin = self.cleaned_data['vin']

        # Strip spaces
        vin = vin.replace(" ", "")

        # Check if it has 17 digits
        if len(vin) != 17:
            raise ValidationError(
                'VIN must have 17 non-empty digits')

        # Capitalize the VIN
        return vin.upper()

    # year is optional. clean it only when its entered
    def clean_year(self):
        year = self.cleaned_data['year']
        current_year = datetime.now().year

        # If year is not provided (or empty), return as is
        if not year:
            return year

        # Ensure year is an integer
        try:
            year = int(year)
        except ValueError:
            raise forms.ValidationError('Model year must be a valid number.')

        # Check if year is within valid range
        if year > current_year + 1 or year < 1900:  # Assuming no vehicle will be from before 1900
            raise forms.ValidationError(
                f'Model year must be between 1900 and {current_year + 1}')

        return year

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'VinSearchForm'
        # 'form-inline'  # 'form-horizontal'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = True
        self.helper.form_method = "post"
        self.helper.form_action = reverse(
            'shops:search_by_vin_or_plate')  # Use your URL name here
        self.helper.layout = Layout(
                            # Adjust the column sizes as needed
                Hidden('action', 'action_vin_search'),
            Row(

                Field('vin',wrapper_class='col-md-6  m-1'),
                Field('year',wrapper_class='col-md-6  m-1'),
                css_class='form-row m-1'
            ),
            Field('captcha', wrapper_class='col-md-12 p-1 m-1'),
            FormActions(
                Submit('vin search', 'Search', css_class='btn btn-outline-dark',
                       css_id='vin-search-button'),
                css_class='d-grid gap-2')

        )
class LicensePlateSearchForm(forms.Form):

    action = forms.CharField(
        widget=forms.HiddenInput(), initial='action_plate_search')

    license_plate = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter license plate number.'}))
    state = forms.ChoiceField(choices=[('', '--- None ---')] + list(LIST_OF_STATES_IN_US), widget=forms.Select(
        attrs={'class': 'form-select'}))
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), 
                             label='please check the box below to verify you are not a robot.')
    
    def clean_license_plate(self):
        license_plate = self.cleaned_data['license_plate']
        if len(license_plate) > 10:
            raise ValidationError(
                'License plate number must not be more than 10 characters long.')
        return license_plate.strip().upper()

    def clean_state(self):
        state = self.cleaned_data['state']
        if state and state not in dict(LIST_OF_STATES_IN_US):
            raise ValidationError('Invalid US state abbreviation.')
        return state

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'PlateSearchForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = True
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('shops:search_by_vin_or_plate')
        self.helper.layout = Layout(
            # Use Div to create a Bootstrap grid structure for responsiveness
            Hidden('action', 'action_plate_search'),
            Row(
                Field('license_plate', css_class='col-md-6 p-1 mb-3'),
                Field('state', css_class='col-md-6 p-1 mb-3'),
                css_class='form-row m-1'
            ),
            Row(Column(Field('captcha', css_class=''),
                   css_class='col-md-12 m-1'),
                   css_class='form-row  '),
            # You can add FormActions for better control over the submit button's placement and styling
            FormActions(
                Button('plate_search', 'Search',
                       css_class='btn btn-outline-dark',
                       css_id='plate-search-button'),
                css_class='d-grid gap-2')
        )

