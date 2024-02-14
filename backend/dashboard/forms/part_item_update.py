
from .base import forms, Field, Column, Row, Layout, FormHelper, HTML,Fieldset
from .automan_base_model import AutomanBaseModelForm
from homepageapp.models import PartItemModel

class PartItemUpdateForm(AutomanBaseModelForm):
    part_item_quantity = forms.IntegerField(
        min_value=0, max_value=100, widget=forms.NumberInput(attrs={'type': 'text', }), label='quantity', required=False)
    
    part_item_unit_cost = forms.DecimalField(
        min_value=0, max_value=10000, widget=forms.NumberInput(attrs={'type': 'text', }), 
        label='unit cost', required=False)
    part_item_unit_price = forms.DecimalField(
        min_value=0, max_value=10000, widget=forms.NumberInput(attrs={'type': 'text', }), 
        label='unit price', required=False)
    part_item_unit_list = forms.DecimalField(
        min_value=0, max_value=10000, widget=forms.NumberInput(attrs={'type': 'text', }), 
        label='unit list', required=False)
    part_item_unit_sale = forms.DecimalField(
        min_value=0, max_value=10000, widget=forms.NumberInput(attrs={'type': 'text', }), 
        label='unit sale', required=False)
    

    part_item_part_no = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', }), label='part number', required=False)
    
    part_item_is_quantity_confirmed = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'toggle-swtich'}), label='quantity confirmed?', required=False)

    part_item_is_confirmed = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'toggle-swtich'}), label='part confirmed?', required=False)

    part_item_is_quantity_confirmed = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'toggle-switch'}), label='is quantity confirmed?', required=False)
    part_item_is_committed = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'toggle-swtich'}), label='is the part commeted yet?', required=False)

    class Meta:
        model = PartItemModel
        fields = [
            # 'line_item',
            'part_item_part_no',
            'part_discount_description_id',
            'part_item_quantity',
            'part_item_confirmed_quantity',
            'part_item_is_quantity_confirmed',
            'part_item_unit_cost',
            'part_item_is_user_entered_unit_cost',
            'part_item_unit_price',
            'part_item_unit_list',
            'part_item_unit_sale',
            'part_item_is_user_entered_unit_sale',
            # 'part_item_part_id',
            'part_item_is_part_ordered',
            'part_item_is_core',
            'part_item_is_bundled_kit',
            'part_item_is_confirmed',
            'part_item_is_committed',
            'part_item_vendor_code',
            'part_item_vendor_id',
            'part_item_manufacture_id',
            'part_item_invoice_number',
            'part_item_commission_amount',
            'part_item_is_MPlg_item',
            'part_item_is_changed_MPlg_item',
            'part_item_part_type',
            'part_item_size',
            'part_item_is_tire',
            'part_item_meta',
            'part_item_added_from_supplier',
            'part_item_purchased_from_vendor',
            'part_item_purchased_from_supplier',
            'part_item_shipping_description',
            'part_item_shipping_cost',
        ]
        widgets = {
            'part_item_quantity': forms.NumberInput(attrs={'type': 'text', }),
            'part_item_confirmed quantity': forms.NumberInput(attrs={'type': 'text', }),
            'part_item_unit_list': forms.NumberInput(attrs={'type': 'text', }),
            'part_item_unit_sale': forms.NumberInput(attrs={'type': 'text', }),
            'part_item_unit_cost': forms.NumberInput(attrs={'type': 'text', }),
            'part_item_unit_price': forms.NumberInput(attrs={'type': 'text', }),
            'part_item_shipping_description': forms.TextInput(attrs={}),
        }

        labels = {
            # 'part_item_is_confirmed': 'Is this part has been confirmed? ',

        }

    def clean_part_item_unit_price(self):
        unit_price = self.cleaned_data.get('part_item_unit_price')
        if unit_price is not None and unit_price < 0:
            raise forms.ValidationError("Unit price must be greater than zero.")
        return unit_price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.label_class = 'col-9 text-left'
        self.helper.field_class = 'col-3 text-right'
        self.helper.layout = Layout(

                    Row(Column(Field('part_item_quantity', css_class='form-control'),
                               Field('part_item_is_quantity_confirmed',wrapper_class='form-switch '),
                            css_class='col-md-12'),
                            
                        Column (Field('part_item_unit_cost', css_class='form-control'),
                                
                                css_class='col-12'),

                        css_class='form-group '),

                    Row(
                        Column(Field('part_item_unit_price', css_class='form-control'),
                        css_class='col-md-12 '),
                        Column(Field('part_item_unit_list', css_class='form-control'),
                        css_class='col-md-12'),
                        Column(Field('part_item_unit_sale', css_class='form-control'),
                        css_class='col-12'),

                    css_class='form-group'),

                    
                    Row(

                    css_class='form-group'),
                    
                        Row(
                            Column(Field('part_item_vendor_id', css_class=''),
                            css_class='col-md-12'),
                            Column(Field('part_item_manufacture_id', css_class=''),
                            css_class='col-md-12'),
                            Column(Field('part_item_invoice_number', css_class=''),
                            css_class='col-md-12'),
                            Column(Field('part_item_commission_amount', css_class=''),
                            css_class='col-md-12'),
                            Column(Field('part_item_is_tire', wrapper_class='form-switch '),
                            css_class='col-md-12'),
                            Column(Field('part_item_is_part_ordered', wrapper_class='form-switch '),
                            css_class='col-12'),
                            Column(Field('part_item_size', css_class=''),
                            css_class='col-12'),
                            Column(Field('part_item_added_from_supplier',css_class=' '),
                            css_class='col-12'),
                            Column(Field('part_item_purchased_from_vendor', css_class=' '),
                            css_class='col-12'),
                            Column(Field('part_item_shipping_description', css_class=''),
                            css_class='col-12'),
                            Column(Field('part_item_shipping_cost', css_class=' '),
                            css_class='col-12'),
                        css_class='form-group '),
                                 
                                

                )
