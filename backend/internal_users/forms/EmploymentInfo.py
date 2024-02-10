
# 2023-05-30
# this form is used to display a internal_user's employment information
# this detail page displays most but not all information of the talent record that is assocaited with the user.
# the fields shall be limited and not editable.
from .base import forms, FormHelper, Layout, Div, Field
from talent_management.models import TalentsModel

class EmploymentInfoForm(forms.ModelForm):
    # create a talent_full_name to store data from the property field of TalentsModel
    talent_full_name = forms.CharField(label="Full Name", required=False)

    class Meta:
        model = TalentsModel
        fields = ['talent_employee_id', 'talent_first_name', 'talent_last_name', 'talent_middle_name',
                  'talent_date_of_birth', 'talent_phone_number_primary', 'talent_mailing_address_is_the_same_physical_address',
                  'talent_hire_date', 'talent_department', 'talent_supervisor',
                  'talent_pay_type', 'talent_pay_rate', 'talent_pay_frequency',
                  'talent_previous_department',
                  ]

    def set_readonly(self):
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True

    def get_pay_type_display(self):
        return dict(self.PAY_TYPES).get(self.talent_pay_type)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set all fields to readonly
        self.set_readonly()
        if self.instance:
            self.fields['talent_full_name'].initial = self.instance.talent_full_name

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('talent_employee_id', css_class='form-control'),
                Field('talent_first_name', css_class='form-control'),
                css_class='card'
            ),
            Div(
                Field('talent_department'),
                Field('talent_supervisor'),
                Field('talent_pay_type'),
                Field('talent_pay_rate'),
                Field('talent_pay_frequency'),
                css_class='card'
            ),
            Div(
                Field('talent_previous_department'),
                Field('talent_discharge_date'),
                css_class='card'
            ),
            # Add more sections for other groups of fields
        )