from .base import forms 
from homepageapp.models import AddressesNewSQL02Model

class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = AddressesNewSQL02Model
        fields = [
            'address_company_or_ATTN',
            'address_line_01',
            'address_city',
            'address_state', 'address_zip_code',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control text-input'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control textarea-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'custom-select'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'datetime-input'})
            # You can continue for other field types
