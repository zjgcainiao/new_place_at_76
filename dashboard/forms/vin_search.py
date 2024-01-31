from django.forms import ValidationError
from .base import forms

# this form was created on 2023-10-09. used in `vehicles/fetch-single-vin-search-nhtsa-api`.
# takes a vin and model year and returns an json response with detailed vehicle info from NHTSA gov.
# the form validates the vin to be 17-digit long and model year to be equal or less than this year plus 1.
class VINSearchForm(forms.Form):
    vin = forms.CharField(required=True,
                          label='Vehicle Identification Number(VIN)',
                          help_text='required. Enter full 17 digits',
                          widget=forms.TextInput(
                              attrs={'class': 'form-control', 'placeholer': 'example: 5YJSX********'}))
    year = forms.IntegerField(required=False,
                              label='Model Year',
                              help_text="optional",
                              widget=forms.NumberInput(
                                  attrs={'class': 'form-control', 'placeholder': 'vehicle year'}))

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

    def clean_year(self):
        year = self.cleaned_data['year']
        if not year:
            return None

        current_year = datetime.now().year

        # Check if year is valid
        if year > current_year + 1 or year < 1900:  # Assuming no vehicle will be from before 1900
            raise forms.ValidationError(
                f'Model year must be between 1900 and {current_year + 1}')
        return year

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # exclude the line item id
