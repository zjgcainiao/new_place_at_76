from .base import Layout, Fieldset, Row, Column, Field, Submit, forms,FormHelper
from we_handle_money_stuff.models import GLSubAccount

class GLSubAccountCreateForm(forms.ModelForm):
    class Meta:
        model =GLSubAccount
        fields = ['name', 'description', 'parent_account','sub_account_number','sub_account_type','sub_account_detail_type']
        required = ['name', 'sub_account_number','sub_account_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'parent_account': forms.Select(attrs={'class': 'form-select'}),
            'sub_account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sub Account Number'}),
            'sub_account_type': forms.Select(attrs={'class': 'form-select'}),
            'sub_account_detail_type': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Name',
            'description': 'Description',
            'parent_account': 'parent Account',
            'sub_account_number': 'Sub Account Number',
            'sub_account_type': 'Sub Account Type',
            'sub_account_detail_type': 'Sub Account Detail Type',
        }
        help_texts = {
            'name': 'Enter the name of the account',
            'description': 'Enter the description of the account',
            'parent_account': 'Select the parent account',
            'sub_account_number': 'Enter the sub account number',
            'sub_account_type': 'Select the sub account type',
            'sub_account_detail_type': 'Select the sub account type detail',
        }
        error_messages = {
            'name': {
                'required': 'This field is required'
            },
            'sub_account_number': {
                'required': 'This field is required'
            },
            'sub_account_type': {
                'required': 'This field is required'
            },
            'sub_account_detail_type': {
                'required': 'This field is required'
            },
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fieldset_name = 'Create Sub GL Account'
        instance = kwargs.get('instance', None)
        self.helper = FormHelper()
        self.helper.form_id = 'id-gl-sub-account-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                fieldset_name,
                Row(
                    Column(Field('name',css_class='form-control'), css_class='col-md-6 mb-0'),
                    Column(Field('sub_account_number',css_class='form-select'), css_class='col-md-6 mb-0'),
                    css_class='form-group p-1 m-1'
                ),
                Row(
                    Column(Field('sub_account_type',css_class='form-select'), css_class='col-md-6 mb-0'),
                    Column(Field('sub_account_detail_type',css_class='form-select'), css_class='col-md-6 mb-0'),
                    css_class='p-1 m-1'
                ),
                Row(
                    Column(Field('description',css_class='form-control'), css_class='col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column(Submit('submit', 'Create', css_class='btn btn-primary'), css_class='col-md-12 mb-0'),
                    css_class='row'
                ),
            )
        )
