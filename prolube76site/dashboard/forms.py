
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div
from django.utils.translation import gettext_lazy as _
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.db.models import Prefetch
from homepageapp.models import RepairOrderLineItemSquencesNewSQL02Model, PartItemModel, LineItemsNewSQL02Model, LaborItemModel
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model , RepairOrdersNewSQL02Model,AddressesNewSQL02Model, CustomerAddressesNewSQL02Model,PhonesNewSQL02Model
# using crispy_forms to control the search form.
class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search',widget=forms.TextInput(attrs={'class': 'form-control','placeholer':'enter phone number, license plate'}))
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'id-SearchForm'
    #     self.helper.form_class = 'blueForms'
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = 'submit_survey'
    #     self.helper.add_input(Submit('submit', 'Submit'))


class CustomerUpdateForm(forms.ModelForm):
    # customer_first_name = forms.CharField(required=True, label="first name")
    customer_resale_permit_nbr = forms.CharField(required=False, label='Resale permit number')
    customer_memebership_nbr = forms.CharField(required=False,label='Membership nbr' )
    customer_spouse_name = forms.CharField(required=False, label='Spouse Name', widget=forms.TextInput(attrs={'class':'form-control','type':'text', 'placeholder':'enter your spouse name or another trusted person who we can contact.'}))
    customer_dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}), label='Date of birth (dob)', help_text='dob is used for customer verification.')
    class Meta:
        model = CustomersNewSQL02Model
        fields = ['customer_first_name','customer_last_name', 'customer_middle_name','customer_spouse_name',
                  'customer_dob','customer_memebership_nbr', 'customer_resale_permit_nbr','customer_is_tax_exempt',
                  'customer_memo_1',
                  ]
        widgets = {
            'customer_first_name':forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'customer_last_name':forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'customer_middle_name':forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'customer_resale_permit_nbr':forms.TextInput(attrs={'class':'form-control','type':'text', 'placeholder':'usually a tax-exempt resale permit granted usually by state authorities.'}),
            'customer_memo_1':forms.Textarea(attrs={'class':'form-control','type':'text'}),
            'customer_memebership_nbr':forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'customer_does_allow_SMS':forms.CheckboxInput(attrs={'class':'form-check'}),
            'customer_is_tax_exempt':forms.CheckboxInput(attrs={'class':'form-check'}),
        }
        labels={'customer_first_name':'First name',
                'customer_last_name':'Last name',
                'customer_middle_name':'Middle name',
                'customer_memebership_nbr':'Membership nbr',
                'customer_memo_1':'Customer memo (comments from shop)',
                'customer_is_tax_exempt':'Is tax exempt?',
                }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
         ## add a "form-control" class to each form input
         ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
        })
            
        # self.fields['appointment_vehicle_make'].choices = [(make.pk, make.make_name) for make in MakesNewSQL02Model.objects.all()]
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = "post"
        self.helper.label_class = 'col-3'
        self.helper.field_class = 'col-9'
        self.helper.layout = Layout(
            Fieldset(_('customer_info'),
                Row(Column(Field('customer_first_name', css_class='form-control'),
                        css_class='col-4 ',),
                    Column(Field('customer_last_name',css_class='form-control', ), #style="background-color: #333"
                        css_class='col-4 ',),
                    Column(Field('customer_middle_name', css_class='form-control'),
                        css_class='col-4',),
                    Column(Field('customer_spouse_name',css_class='form-control',),
                        css_class='col-4',),
                    Column(Field('customer_dob', css_class='form-control'),
                        css_class='col-4',),
                    Column(Field('customer_memebership_nbr',css_class='form-control',), #style="background-color: #f333"
                        css_class='col-4',),
                    Row(HTML("<hr>"),
                        css_class='m-1 p-1'),
                    Column(Field('customer_memo_1', css_class='form-control'),
                        css_class='col-12',),
                    css_class='pt-1 mb-3'), 
            css_class='p-1 m-1'),

            Row(HTML("<hr>"),
                css_class='m-1 p-1'),

            Fieldset(_('special information: tax exempt or fleet customer.'),
                Row(Column(Field('customer_is_tax_exempt',css_class='form-check'),
                        css_class='col-4'),
                    Column(Field('customer_resale_permit_nbr',css_class='form-control'),
                        css_class='col-8'),
                css_class='p-1 m-1'),
            
            ),
            ButtonHolder(
                Row(
                Column(Submit('submit', 'Update', css_class='btn btn-primary', css_id='submit-button', style="float: left;"),
                        css_class='col col-6'),
                Column(Reset('reset', 'Reset', css_class='btn btn-secondary', css_id='reset-button', style="float: right;"),
                        css_class='col col-6'),
                css_class='p-1 m-1'),
            ),
            
        )
        # end of self.helper.Layout 

class RepairOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = RepairOrdersNewSQL02Model
        fields = [
                  'repair_order_customer',
                  'repair_order_phase',
                  'repair_order_created_as_estimate',
                  'repair_order_is_printed',
                  'repair_order_aggr_notes',
                  'repair_order_snapshot_order_total_amount',
                  ]
  
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # add a "form-control" class to each form input
        # for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
        })



class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = AddressesNewSQL02Model
        fields = ['address_line_01','address_city','address_state','address_zip_code']
 
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # add a "form-control" class to each form input
        # for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
        })
      

class VehicleUpdateForm(forms.ModelForm):
    class Meta:
        model = VehiclesNewSQL02Model
        fields = ['vehicle_id','vehicle_cust','VIN_number','vehicle_memo_01','vehicle_odometer_1']
        # exclude = ('created_at', 'updated_at',)
        # widgets = {
        #     'vehicle_cust': forms.TextInput(attrs={'class':'form-control',}),
        #     'repair_order_phase': forms.TextInput(attrs={'class':'form-control',}),
        # }
 
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # add a "form-control" class to each form input
        # for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
        })
     
class PartItemUpdateForm(forms.ModelForm):
    part_item_quantity = forms.IntegerField(min_value=0,max_value=100)
    part_item_is_confirmed = forms.BooleanField()
    part_item_is_quantity_confirmed = forms.BooleanField()
    class Meta:
        model = PartItemModel
        fields = [
            'line_item',
            'part_item_part_no',
            'part_discount_description_id',
            'part_item_is_user_entered_unit_sale',
            'part_item_is_user_entered_unit_cost',
            'part_item_quantity',
            'part_item_unit_cost',
            'part_item_unit_price',
            'part_item_unit_list',
            'part_item_unit_sale',

            # 'part_item_part_id',
            'part_item_is_confirmed',
            'part_item_is_committed',
            # 'part_item_vendor_code',
            # 'part_item_vendor_id',
            # 'part_item_manufacture_id',
            # 'part_item_invoice_number',
            # 'part_item_commission_amount',
  
            # 'part_item_is_quantity_confirmed',
            # 'part_item_confirmed_quantity',
            # 'part_item_is_part_ordered',
            # 'part_item_is_core',
            # 'part_item_is_bundled_kit',
            # 'part_item_is_MPlg_item',
            # 'part_item_is_changed_MPlg_item',
            # 'part_item_part_type',
            # 'part_item_size',
            # 'part_item_is_tire',
            # 'part_item_vendor_id',
            # 'part_item_meta',
            # 'part_item_added_from_supplier',
            # 'part_item_purchased_from_vendor',
            # 'part_item_purchased_from_supplier',
            # 'part_item_shipping_description',
            # 'part_item_shipping_cost'
        ]
        widgets = {
            'part_item_quantity': forms.NumberInput(attrs={'type': 'text', 'class':'form-control',}),
            'part_item_unit_price': forms.NumberInput(attrs={'type': 'text','class': 'form-control',}),
            'part_item_unit_list': forms.NumberInput(attrs={'type': 'text','class': 'form-control',}),
            'part_item_unit_sale': forms.NumberInput(attrs={'type': 'text','class': 'form-control',}),
            'part_item_unit_cost': forms.NumberInput(attrs={'type': 'text','class': 'form-control',}),
            'part_item_unit_price': forms.NumberInput(attrs={'type': 'text','class': 'form-control',}),
            'part_item_unit_price': forms.NumberInput(attrs={'type': 'text','class': 'form-control',}),
            'part_item_is_confirmed': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'part_item_shipping_description': forms.TextInput(attrs={}),
        }

        labels = {
            'part_item_is_confirmed': 'Is this part has been confirmed? ',

        }

    def clean_unit_price(self):
        unit_price = self.cleaned_data['part_item_unit_price']
        if unit_price < 0:
            raise forms.ValidationError("unit price must be greater than zero.")
        return unit_price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['part_item_unit_price'].validators.append(self.clean_unit_price)

class RepairOrderLineItemUpdateForm(forms.ModelForm):

    class Meta:
        model = RepairOrderLineItemSquencesNewSQL02Model
        exclude = ['line_item_last_updated_date', 'line_item_parent_line_item_id',]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['line_item'].queryset = LineItem.objects.all()


class LaborItemUpdateForm(forms.ModelForm):
    # part_item_quantity = forms.IntegerField(min_value=0,max_value=100)
    # labor_item_work_performed = forms.CharField(max_length=500, null=True)
    labor_item_is_user_entered_labor_rate = forms.BooleanField()

    class Meta:
        model = LaborItemModel
        fields = [
            'labor_item_id',
            'line_item',
            'labor_rate_description_id',
            'labor_item_is_user_entered_labor_rate',
            'labor_item_work_performed',
            'labor_item_hours_charged',
            'labor_item_symptom',
            'labor_item_is_come_back_invoice',
            'labor_item_parts_estimate',
            # 'labor_item_is_MPlg_item',
            # 'labor_item_is_Changed_MPlg_item',
        ]
        widgets = {
            'labor_item_hours_charged': forms.NumberInput(attrs={'class': 'form-control',}),
            'labor_item_symptom': forms.TextInput(attrs={'class': 'form-control',}),
            'labor_item_parts_estimate': forms.NumberInput(attrs={'class': 'form-control',}),

            'labor_item_is_user_entered_labor_rate': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'line_item': forms.TextInput(attrs={'class': 'form-control',
                                                'readonly': 'readonly'}),
            'labor_item_symptom': forms.Textarea(attrs={}),
        }

        labels = {
            # 'labor_item_is_user_entered_labor_rate': 'Is this part has been confirmed? '

        }


PartItemFormSet = inlineformset_factory(LineItemsNewSQL02Model, PartItemModel,
    fields=(
        'part_item_part_no',
        'part_discount_description_id',
        'part_item_quantity',
        'part_item_unit_cost',
        'part_item_unit_price',
        'part_item_unit_list',
        'part_item_unit_sale',
        'part_item_is_user_entered_unit_sale',
        'part_item_is_user_entered_unit_cost',),
    extra=0,

    widgets={'part_item_quantity': forms.NumberInput(attrs={'class':'form-control', 'type':'text'}),
        'part_item_unit_price': forms.NumberInput(attrs={'class': 'form-control','type':'text'}),
        'part_item_unit_list': forms.NumberInput(attrs={'class': 'form-control','type':'text'}),
        'part_item_unit_sale': forms.NumberInput(attrs={'class': 'form-control','type':'text'}),
        'part_item_unit_cost': forms.NumberInput(attrs={'class': 'form-control','type':'text'}),
        'part_item_unit_plist': forms.NumberInput(attrs={'class': 'form-control','type':'text'}),
        'part_item_unit_price': forms.NumberInput(attrs={'class': 'form-control',}),
        'part_item_is_confirmed': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        'part_item_is_user_entered_unit_sale':forms.CheckboxInput(attrs={'class':'form-check-input',
                                                            'readonly':True}),
        # 'line_item': forms.TextInput(attrs={'class': 'form-control',
        #                                     'readonly': 'readonly'}),
        'part_item_shipping_description': forms.TextInput(attrs={}),

        },
    )
LaborItemFormSet = inlineformset_factory(LineItemsNewSQL02Model, LaborItemModel, 
    fields=('labor_item_id',
        'labor_item_hours_charged',
        'labor_item_work_performed',
        'labor_rate_description_id',
        'labor_item_is_user_entered_labor_rate',
        'labor_item_is_come_back_invoice',
        'labor_item_parts_estimate',),
    widgets={'labor_item_hours_charged': forms.NumberInput(attrs={'step': '0.01','class': 'form-control',}),
        'labor_item_symptom': forms.TextInput(attrs={'class': 'form-control',}),
        'labor_item_parts_estimate': forms.NumberInput(attrs={'step': '0.01','class': 'form-control',}),

        'labor_item_is_user_entered_labor_rate': forms.CheckboxInput(attrs={'readonly':'readonly'}),
        # 'line_item': forms.TextInput(attrs={'class': 'form-control',
        #                                     'readonly': 'readonly'}),
        'labor_item_symptom': forms.Textarea(attrs={'class': 'form-control',}),},
    extra=0,
    )        

RepairOrderFormSet = formset_factory(RepairOrderUpdateForm, extra=0)
CustomerFormSet = formset_factory(CustomerUpdateForm, extra=0)
AddressFormSet = formset_factory(AddressUpdateForm, extra=0)