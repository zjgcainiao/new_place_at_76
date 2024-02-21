
import attr
import attrs
from .base import forms, LIST_OF_STATES_IN_US, \
Hidden, Row, Field, FormActions, Button, ReCaptchaField, ReCaptchaV2Checkbox, \
Layout, Column, FormHelper, ValidationError, reverse

class LicensePlateSearchForm(forms.Form):

    action = forms.CharField(
        widget=forms.HiddenInput(), initial='action_plate_search')

    license_plate = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter license plate number.'}))
    state = forms.ChoiceField(choices=[('', '--- None ---')] + list(LIST_OF_STATES_IN_US), widget=forms.Select(
        attrs={'class': 'form-select'}))
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={}), 
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

