from .base import forms

class AutomanBaseModelForm(forms.ModelForm):  # Change to forms.ModelForm if you're working with model forms
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