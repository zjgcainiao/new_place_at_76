from .base import forms
from core_operations.constants import EMAIL_TYPES
from homepageapp.models import EmailsNewSQL02Model
class LiteEmailUpdateForm(forms.ModelForm):
    email_id = forms.IntegerField(required=False)
    email_type_id = forms.ChoiceField(choices=EMAIL_TYPES, label='type')
    email_address = forms.EmailField(label='address', required=True)
    email_description = forms.CharField(
        max_length=200, label='notes:')
    email_can_send_notification = forms.BooleanField(
        required=False, label='allow notifcations')

    class Meta:
        model = EmailsNewSQL02Model
        fields = ['email_type_id',
                  'email_address', 'email_description', 'email_can_send_notification']

        widgets = {
            # 'email_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email_type_id': forms.Select(attrs={"type": "text", "class": "form-control form-select"}),
            'email_address': forms.EmailInput(attrs={"type": "text", "class": "form-control"}),
            'email_description': forms.Textarea(attrs={"type": "text", "class": "form-control editable-field"}),
            'email_can_send_notification': forms.CheckboxInput(attrs={'class': 'form-check form-control'}),
        }
        labels = {
            'email_can_send_notification': 'allow notifications?',
            'email_type_id': 'email type',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
