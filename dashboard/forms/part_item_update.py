
from .base import forms, Field, Column, Row, Layout, FormHelper
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
        label='unit cost', required=False)
    part_item_unit_list = forms.DecimalField(
        min_value=0, max_value=10000, widget=forms.NumberInput(attrs={'type': 'text', }), 
        label='unit cost', required=False)
    part_item_unit_sale = forms.DecimalField(
        min_value=0, max_value=10000, widget=forms.NumberInput(attrs={'type': 'text', }), 
        label='unit cost', required=False)
    

    part_item_part_no = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', }), label='part no', required=False)
    
    part_item_is_quantity_confirmed = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'toggle-swtich'}), label='quantity confirmed?', required=False)

    part_item_is_confirmed = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'toggle-swtich'}), label='part confirmed?', required=False)

    part_item_is_user_entered_unit_sale = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': ''}), label='unit sale entered manually?', required=False)
    part_item_is_user_entered_unit_cost = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': ' toggle-swtich'}), label='unit cost entered manually?', required=False)

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

    def clean_unit_price(self):
        unit_price = self.cleaned_data['part_item_unit_price']
        if unit_price < 0:
            raise forms.ValidationError(
                "unit price must be greater than zero.")
        return unit_price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['part_item_unit_price'].validators.append(
            self.clean_unit_price)

        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_tag = False
        self.helper.form_method = "post"
        # self.helper.label_class = 'col-3'
        # self.helper.field_class = 'col-9'
        self.helper.layout = Layout(
                    Row(Column(Field('part_item_quantity', css_class='form-control'),
                            css_class='col-8'),
                        Column(Field('part_item_is_quantity_confirmed', style='margin-left: 0;',wrapper_class='form-check form-switch p-1 m-1'),
                            css_class='col-4'),
                        Column (Field('part_item_unit_cost', rows="3", css_class='form-control mb-2'),
                                css_class='col-8'),
                        Column (Field('part_item_is_user_entered_unit_cost', rows="3", css_class='form-control mb-2'),
                                css_class='col-4'),
                        css_class='form-group p-1 m-1'),

                    Row(Column(Field('part_item_unit_price', css_class='form-control mb-2'),
                        css_class='col-6'),
                        Column(Field('part_item_unit_list', css_class='form-control mb-2'),
                        css_class='col-6'),
                        Column(Field('part_item_unit_sale', css_class='form-control mb-2'),
                        css_class='col-6'),
                        Column(
                            Field('part_item_is_user_entered_unit_sale', style='margin: 5px;',wrapper_class='form-check form-switch p-1 m-1'),
                            css_class='col-6'
                            ),
                    css_class='form-group p-1 m-1'),

                    
                    Row(
                        Column(Field('part_item_vendor_id', css_class='form-control mb-2'),
                        css_class='col-6'),
                        Column(Field('part_item_is_tire', style='margin-left: 0;',wrapper_class='form-check form-switch p-1 m-1'),
                            css_class='col-6'),
                        css_class='form-group m-1 p-1'),


                )
