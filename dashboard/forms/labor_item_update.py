from .base import forms, FormHelper, Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden
from django.utils.translation import gettext_lazy as _
from homepageapp.models import LaborItemModel
from .automan_base_model import AutomanBaseModelForm
class LaborItemUpdateForm(AutomanBaseModelForm):
    labor_item_symptom = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": 'include the noise, the incident that customer mentions'}), label='Symtoms')
    labor_item_is_user_entered_labor_rate = forms.BooleanField(widget=forms.CheckboxInput(
       attrs={'class': 'form-check-input', 'role': 'switch'}), label='is manual labor rate?')
    labor_item_is_come_back_invoice = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'role': 'switch'}), label='is come-back invoice')
    
    labor_item_hours_charged = forms.FloatField(widget=forms.NumberInput())
    labor_item_work_performed = forms.CharField(
        widget=forms.Textarea(), label='work performed (labor)')

    class Meta:
        model = LaborItemModel
        fields = [
            'labor_item_id',
            # 'line_item',
            'labor_item_symptom',
            'labor_item_work_performed',
            'labor_item_hours_charged',
            'labor_item_is_come_back_invoice',
            'labor_item_parts_estimate',
            'labor_rate_description',
            'labor_item_is_user_entered_labor_rate',
            # 'labor_item_is_MPlg_item',
            # 'labor_item_is_Changed_MPlg_item',
        ]
        widgets = {

            # 'line_item': forms.TextInput(attrs={'class': 'form-control',
            #                                     'readonly': 'readonly'}),
            'labor_item_hours_charged': forms.NumberInput(attrs={'class': 'form-control'}),
            'labor_item_symptom': forms.TextInput(attrs={'class': 'form-control', 
                                                         'placeholder': 'Include the noise, the incident that customer mentions'}),
            'labor_item_parts_estimate': forms.NumberInput(attrs={'class': 'form-control'}),
            'labor_item_is_come_back_invoice': forms.CheckboxInput(),
            'labor_item_is_user_entered_labor_rate': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # add a "form-control" class to each form input
        # for enabling bootstrap
        # for name, field in self.fields.items():
        #     # check widget type
        #     if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select)):
        #         field.widget.attrs.update({'class': 'form-control'})

        # self.fields['appointment_vehicle_make'].choices = [(make.pk, make.make_name) for make in MakesNewSQL02Model.objects.all()]

        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_tag = False
        self.helper.form_method = "post"
        # self.helper.label_class = 'col-3'
        # self.helper.field_class = 'col-9'
        self.helper.layout = Layout(
            Row(Column(Field('labor_item_symptom', css_class='form-control'),
                    css_class='col-12'),
                   
                Column (Field('labor_item_work_performed', rows="3", css_class='form-control mb-2'),
                        css_class='col-12'),
                css_class='form-group p-1 m-1'),

            Row(Column(Field('labor_item_hours_charged', css_class='form-control mb-2'),
                   css_class='col-6'),
                Column(
                    Field('labor_item_is_user_entered_labor_rate', style='margin: 5px;',wrapper_class='form-check form-switch p-1 m-1'),
                    css_class='col-6'
                    ),
            css_class='form-group p-1 m-1'),

            
            Row(
                Column(Field('labor_item_parts_estimate', css_class='form-control mb-2'),
                   css_class='col-6'),
                Column(Field('labor_item_is_come_back_invoice', style='margin-left: 0;',wrapper_class='form-check form-switch p-1 m-1'),
                    css_class='col-6'),
                css_class='form-group m-1 p-1'),


        )
