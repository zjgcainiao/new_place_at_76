from django import forms

class AddressForm(forms.Form):
    address_line_1 = forms.CharField(max_length=100)
    address_line_2 = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=10)
    country_code = forms.CharField(max_length=10, default='United States')

    def clean(self):
        cleaned_data = super().clean()
        address = f"{cleaned_data['address_line_1']} {cleaned_data['address_line_2']}".strip()
        city = cleaned_data['city'].strip()
        state = cleaned_data['state'].strip()
        zip_code = cleaned_data['zip_code'].strip()
        country_code = cleaned_data['country_code'].strip()

        if not address or not city or not state or not zip_code:
            raise forms.ValidationError("All address fields are required.")

        return cleaned_data
