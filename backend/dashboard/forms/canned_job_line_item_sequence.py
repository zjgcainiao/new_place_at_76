from .base import forms, FormHelper, Layout, Field, Fieldset, Submit, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden
from homepageapp.models import CannedJobLineItemSequence, LineItemsNewSQL02Model
from .automan_base_model import AutomanBaseModelForm
from appointments.custom_validators import validate_numeric

class CannedJobLineItemSequenceForm(AutomanBaseModelForm):
    # Dynamically add fields for the LineItem details you want to be editable
    line_item_id = forms.CharField(required=False,
                                   disabled=True,
                                   label='id')  # Example for demonstration
    line_item_description = forms.CharField(required=False)  # Example for demonstration
    
    line_item_cost = forms.DecimalField(
        required=False,
        widget=forms.TextInput(attrs={}),  # Keep the free-form text input style
        validators=[validate_numeric],  # Apply the custom numeric validator
        label='Total cost'
    )
    
    line_item_sale = forms.DecimalField(
        required=False,
        widget=forms.TextInput(attrs={}),  # Similarly for line_item_sale
        validators=[validate_numeric],  # Apply the custom numeric validator
        label='Total sale'
    )

    line_item_has_fixed_commission = forms.BooleanField(required=False,
                                                        widget=forms.CheckboxInput(attrs={'class': 'toggle-switch'}), 
                                                        label='Fixed Commission?')  # Example for demonstration
    line_item_is_tax_exempt = forms.BooleanField(required=False,widget=forms.CheckboxInput,label='is Tax Exempt?')  # Example for demonstration

    sequence = forms.IntegerField(required=False, disabled=True, 
                                  widget=forms.HiddenInput(attrs={'readonly': 'readonly'}),
                                  label='Sequence')  # Example for demonstration
    # line_item = forms.ModelChoiceField(queryset=LineItemsNewSQL02Model.objects.none(),
    #                             widget = forms.HiddenInput(),
    #                             required=False,
    #                             label='Line Item')  # Example for demonstration
    class Meta:
        model = CannedJobLineItemSequence
        fields = ['id', 'sequence', ] #'line_item'
        readonly_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def save(self, commit=True):
        # Custom save method to also save changes made to the LineItem details
        instance = super().save(commit=False)
        if commit:
            line_item = instance.line_item
            line_item.line_item_id = self.cleaned_data.get('line_item_id')
            line_item.line_item_description = self.cleaned_data.get('line_item_description')
            line_item.line_item_cost = self.cleaned_data.get('line_item_cost')
            line_item.line_item_sale = self.cleaned_data.get('line_item_sale')
            line_item.line_item_has_fixed_commission = self.cleaned_data.get('line_item_has_fixed_commission')
            line_item.line_item_is_tax_exempt= self.cleaned_data.get('line_item_is_tax_exempt')
            line_item.save()  # Save the LineItem with the updated details
            instance.save()  # Save the CannedJobLineItemSequence instance
        return instance
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable the sequence field to make it read-only in the U
        self.fields['sequence'].disabled = True
        self.fields['sequence'].hidden = True
        instance = self.instance
        canned_job = instance.canned_job if instance else None
        line_item = instance.line_item if instance else None
        if instance and canned_job and line_item:

            # Prepopulate the form fields with LineItem details
            self.fields['line_item_id'].initial = self.instance.line_item.line_item_id
            self.fields['line_item_description'].initial = self.instance.line_item.line_item_description
            self.fields['line_item_cost'].initial = self.instance.line_item.line_item_cost
            self.fields['line_item_sale'].initial = self.instance.line_item.line_item_sale
            self.fields['line_item_has_fixed_commission'].initial = self.instance.line_item.line_item_has_fixed_commission
            self.fields['line_item_is_tax_exempt'].initial = self.instance.line_item.line_item_is_tax_exempt
        
        self.fields['line_item_id'].disabled = True
        # self.fields['line_item'].disabled = True
        # Initialize FormHelper
        self.helper = FormHelper()
        self.helper.form_tag = False  # Don't render form tag, using table structure instead
        self.helper.form_class = 'form-inline'  # Bootstrap 5 row with gutters
        self.helper.label_class = 'sr-only'

        self.helper.layout = Layout(
            Row(
                Hidden('sequence', '{{ form.sequence.value }}'),  # Correctly handle hidden fields
                # Hidden('line_item', '{{ form.line_item.value }}'),  # Correctly handle hidden fields
                Field('line_item_id',  wrapper_class='form-group col-md-2'),
                Field('line_item_description', wrapper_class='form-group col-md-4'),
                Field('line_item_cost', wrapper_class='form-group col-md-2'),
                Field('line_item_sale',  wrapper_class='form-group col-md-2'),
                Field('line_item_has_fixed_commission', wrapper_class='form-switch col-md-1'),
                Field('line_item_is_tax_exempt', wrapper_class='form-switch col-md-1'),
                css_class='form-inline justify-content-center align-items-center'
            ),
        )