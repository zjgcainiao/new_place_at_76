from .base import Layout, Fieldset, Row, Column, Field, Submit, forms,FormHelper
from we_handle_money_stuff.models import GLSubAccount
from .gl_sub_account_create import GLSubAccountCreateForm

class GLSubAccountUpdateForm(GLSubAccountCreateForm):
   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fieldset_name = 'Update GL Sub Account'
        instance = kwargs.get('instance', None)
        self.helper = FormHelper()
        self.helper.form_id = 'id-gl-sub-account-update-form'
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
