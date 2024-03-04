
from .base import forms, reverse, ValidationError, datetime, FormHelper, \
    Layout, Hidden, Row, Column, Field, FormActions, Submit, ReCaptchaField, \
    ReCaptchaV2Checkbox


class VINSearchForm(forms.Form):
    # added this hiddent input for both VINSearchForm and LicensePlateSearchForm

    vin = forms.CharField(required=True,
                          label='Vehicle Identification Number(VIN)', widget=forms.TextInput(
                              attrs={'class': 'form-control',
                                     'placeholder': 'Example: 1HGCM82633A004352.'}),
                          help_text="VIN must have at least 14-digit non-empty digits. 17 digits is the standard.")
    year = forms.CharField(required=False,
                           label='Year of Vehicle (Optional)',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'enter model year'}),
                           help_text="Optional. Enter only if you cannot get the result with vin only.")
    action = forms.CharField(widget=forms.HiddenInput(),
                             initial='action_vin_search')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(),
                             label='please check the box below to verify you are not a robot.')

    def clean_vin(self):
        vin = self.cleaned_data['vin']

        # Strip spaces
        vin = vin.replace(" ", "")

        # Check if it has 14 digits
        if len(vin) < 14:
            raise ValidationError(
                'VIN must have at least 14 digits')

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
                Field('vin', wrapper_class='col-md-6 m-1'),
                Field('year', wrapper_class='col-md-6 m-1'),

                css_class=' m-1'
            ),
            Field('captcha', wrapper_class='col-md-12 p-1 '),
            FormActions(
                Submit('vin search', 'Search', css_class='btn btn-outline-dark',
                       css_id='vin-search-button'),
                css_class='d-grid gap-2')

        )
