
from .base import forms, FormHelper, Layout, Fieldset, Row, Column, Field, Submit,date_format
from we_handle_money_stuff.models import GLAccount,GLAccountType

class GLAccountCreateForm(forms.ModelForm):
    class Meta:
        model = GLAccount
        fields = ['name', 'description', 'account_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'account_type': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'name': 'Name',
            'description': 'Description',
            'account_type': 'Account Type'
        }
        help_texts = {
            'name': 'Enter the name of the account',
            'description': 'Enter the description of the account',
            'account_type': 'Select the account type'
        }
        error_messages = {
            'name': {
                'required': 'This field is required'
            }
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the queryset
        # self.fields['account_type'].queryset = GLAccountType.objects.all()
        fieldset_name = 'Create GL Account'
        instance = kwargs.get('instance', None)

        # Formulate the HTML strings with actual values if the instance exists
        id_html = '' if not instance else '<p><strong>ID:</strong> {}</p>'.format(instance.id)
        created_at_html = ''
        updated_at_html = ''

        if instance and instance.created_at:
            # Format the datetime object to a string as per the specified format
            created_at_str = date_format(instance.created_at, "Y-m-d P")
            created_at_html = f'<p><strong>Created At:</strong> {created_at_str}</p>'

        if instance and instance.updated_at:
            updated_at_str = date_format(instance.updated_at, "Y-m-d P")
            updated_at_html = f'<p><strong>Last Updated At:</strong> {updated_at_str}</p>'
        self.helper = FormHelper()
        self.helper.form_id = 'id-gl-account-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-3'
        # self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Fieldset(
                fieldset_name,
                Row(
                    Column(Field('name',css_class='form-control'), css_class='col-md-6 mb-0'),
                    Column(Field('account_type',css_class='form-select'), css_class='col-md-6 mb-0'),
                    css_class='form-group p-1 m-1'
                ),
                Field('description'),

            ),
            Submit('submit', 'Save')
        )

        