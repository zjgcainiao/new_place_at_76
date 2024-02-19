from .gl_account_create import GLAccountCreateForm
from .base import Layout, Fieldset, Row, Column, Field, Submit, HTML
from we_handle_money_stuff.models import GLAccountType
class GLAccountUpdateForm(GLAccountCreateForm):
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # Set the queryset
        # self.fields['account_type'].queryset = GLAccountType.objects.all()
        fieldset_name = 'Update GL Account'

        # 2024-02-14 to display the ID in a read-only manner
        # Use the `HTML` layout object to insert the ID display
        # Check if there's an instance and it has an ID
        if self.instance and self.instance.pk:
            id_display = f'<p class="text-muted">Account ID: {self.instance.pk}</p>'
        else:
            id_display = ''

        self.helper.layout = Layout(
            Fieldset(
                fieldset_name,
                HTML(id_display),
                Row(
                    Column(Field('name',css_class='form-control'), css_class='col-md-6 mb-0'),
                    Column(Field('account_type',css_class='form-select'), css_class='col-md-6 mb-0'),
                    css_class='form-group p-1 m-1'
                ),
                Field('description'),

            ),
            Submit('submit', 'Save')
        )