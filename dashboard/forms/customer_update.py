from .base import forms, FormHelper, Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden
from .automan_base_model import AutomanBaseModelForm
from homepageapp.models import CustomersNewSQL02Model

class CustomerUpdateForm(AutomanBaseModelForm):
    # customer_first_name = forms.CharField(required=True, label="first name")
    customer_resale_permit_nbr = forms.CharField(
        required=False, label='Resale permit number')
    customer_memebership_nbr = forms.CharField(
        required=False, label='Membership nbr')
    customer_spouse_name = forms.CharField(required=False, label='Spouse Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'enter your spouse name or another trusted person who we can contact.'}))
    customer_dob = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}), label='Date of birth (dob)', help_text='dob is only used to verififcation purpose, such as picking up the car after service.')

    class Meta:
        model = CustomersNewSQL02Model
        fields = ['customer_first_name', 'customer_last_name', 'customer_middle_name', 'customer_spouse_name',
                  'customer_dob', 'customer_memebership_nbr', 'customer_resale_permit_nbr', 'customer_is_tax_exempt',
                  'customer_memo_1',
                  ]
        widgets = {
            'customer_first_name': forms.TextInput(attrs={'type': 'text'}),
            'customer_last_name': forms.TextInput(attrs={'type': 'text'}),
            'customer_middle_name': forms.TextInput(attrs={'type': 'text'}),
            'customer_resale_permit_nbr': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'usually a tax-exempt resale permit granted usually by state authorities.'}),
            'customer_memo_1': forms.Textarea(attrs={'type': 'text'}),
            'customer_memebership_nbr': forms.TextInput(attrs={'type': 'text'}),
            'customer_does_allow_SMS': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'customer_is_tax_exempt': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }
        labels = {'customer_first_name': 'First name',
                  'customer_last_name': 'Last name',
                  'customer_middle_name': 'Middle name',
                  'customer_memebership_nbr': 'Membership nbr',
                  'customer_memo_1': 'Customer memo (comments from shop)',
                  'customer_is_tax_exempt': 'Is tax exempt?',
                  }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        # self.fields['appointment_vehicle_make'].choices = [(make.pk, make.make_name) for make in MakesNewSQL02Model.objects.all()]

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = "post"
        # self.helper.label_class = 'col-3'
        # self.helper.field_class = 'col-9'
        self.helper.layout = Layout(
            Fieldset(_('customer_info'),
                     Row(Column(Field('customer_first_name', css_class='form-control'),
                                css_class='col-4',),
                         Column(Field('customer_last_name', css_class='form-control'),  # style="background-color: #333"
                                css_class='col-4',),
                         Column(Field('customer_middle_name', css_class='form-control'),
                                css_class='col-4',),
                         Column(Field('customer_spouse_name', css_class='form-control'),
                                css_class='col-4',),
                         Column(Field('customer_dob', css_class='form-control'),
                                css_class='col-4',),
                         Row(HTML("<hr>"),
                             css_class='m-1 p-1'),
                         Column(Field('customer_memo_1', css_class='form-control'),
                                css_class='col-12',),
                         css_class='pt-1 mb-0'),
                     css_class='p-1 m-1'),

            Row(HTML("<hr>"),
                css_class='m-1 p-1'),

            Fieldset(_('Special Information: tax exempt or fleet customer.'),
                     Row(Column(Field('customer_is_tax_exempt', css_class='form-check'),
                                css_class='col-4'),
                         Column(Field('customer_resale_permit_nbr', css_class='form-control'),
                                css_class='col-8'),
                         css_class='p-1 m-1'),

                     ),
            ButtonHolder(
                Row(
                    Column(Submit('submit', 'Apply', css_class='btn btn-primary', css_id='submit-button', style="float: left;"),
                           css_class='col col-6'),
                    Column(Reset('reset', 'Reset', css_class='btn btn-secondary', css_id='reset-button', style="float: right;"),
                           css_class='col col-6'),
                    css_class='p-1 m-1'),
            ),

        )
        # end of self.helper.Layout
