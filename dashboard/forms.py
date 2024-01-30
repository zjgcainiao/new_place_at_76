
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button
from django.utils.translation import gettext_lazy as _
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.db.models import Prefetch
from homepageapp.models import RepairOrderLineItemSquencesNewSQL02Model, PartItemModel, LineItemsNewSQL02Model, LaborItemModel, EmailsNewSQL02Model
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model, RepairOrdersNewSQL02Model, AddressesNewSQL02Model, CustomerAddressesNewSQL02Model, PhonesNewSQL02Model, CustomerEmailsNewSQL02Model, CustomerPhonesNewSQL02Model
from datetime import datetime
from homepageapp.models import GVWsModel, SubmodelsModel, BrakesModel, EnginesModel, TransmissionsModel, BodyStylesModel, CategoryModel, NoteItemsNewSQL02Model
from django.urls import reverse, reverse_lazy
# using crispy_forms to control the search form.
from core_operations.constants import EMAIL_TYPES, LIST_OF_STATES_IN_US
from django.core.exceptions import ValidationError
from crispy_forms.bootstrap import PrependedText
from django.utils.safestring import mark_safe

class AutomanBaseForm(forms.Form):  # Change to forms.ModelForm if you're working with model forms
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control text-input'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control textarea-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'custom-select'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'datetime-input'})

class AutomanBaseModelForm(forms.ModelForm):  # Change to forms.ModelForm if you're working with model forms
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control text-input'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control textarea-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'custom-select'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'datetime-input'})
class SearchForm(AutomanBaseForm):
    search_query = forms.CharField(label='Search', widget=forms.TextInput(
        attrs={'placeholder': 'enter a phone number, license plate to search.','type':'search'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize FormHelper
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        # Form layout
        self.helper.layout = Layout(
            Div(
                # PrependedText is used to add the search icon as a prepended element to your input field
                PrependedText('search_query', mark_safe('<span class="mdi mdi-magnify search-icon"></span>'), active=True,_class='form-control dropdown-toggle'),
                Submit('submit', 'Search', css_class='btn btn-primary input-group-text'),
                css_class='form-group  p-1 m-1',
            ),
            
        )
        
class CustomerEmailForm(AutomanBaseModelForm):
    email_type_id = forms.ChoiceField(choices=EMAIL_TYPES, label='type')
    email_address = forms.EmailField()

    class Meta:
        model = CustomerEmailsNewSQL02Model
        fields = ('email_type_id',)

    def save(self, commit=True):
        # Save the primary object (CustomerEmailsNewSQL02Model instance)
        instance = super().save(commit=False)

        # Save the related object (EmailsNewSQL02Model instance)
        email = EmailsNewSQL02Model.objects.create(
            email_type_id=self.cleaned_data['email_type_id'],
            email_address=self.cleaned_data['email_address']
        )
        instance.email = email

        if commit:
            instance.save()

        return instance

class CustomerAddressForm(forms.ModelForm):
    address_type_id = forms.ChoiceField(choices=EMAIL_TYPES, label='type')
    email_address = forms.EmailField()
    address_company_or_ATTN = forms.CharField(
        max_length=20, label='Attention To or Company')
    address_line_01 = forms.CharField(
        max_length=20, label='Attention To or Company')
    address_city = forms.CharField(max_length=20, label='city')
    address_state = forms.CharField(max_length=2, label='state')
    address_zip_code = forms.CharField(max_length=10, label='zip code')

    def save(self, commit=True):
        # Save the primary object (CustomerEmailsNewSQL02Model instance)
        instance = super().save(commit=False)

        # Save the related object (EmailsNewSQL02Model instance)
        email = EmailsNewSQL02Model.objects.create(
            email_type_id=self.cleaned_data['email_type_id'],
            email_address=self.cleaned_data['email_address']
        )
        instance.email = email

        if commit:
            instance.save()

        return instance


class CustomerPhoneForm(forms.ModelForm):
    customer = forms.CharField(label='customer_id')
    phone_desc_id = forms.ChoiceField(choices=EMAIL_TYPES, label='type')

    phone_number = forms.CharField(
        max_length=20, label='phone number (10-digit)')
    phone_number_ext = forms.CharField(max_length=20, label='ext')

    def save(self, commit=True):
        # Save the primary object (CustomerEmailsNewSQL02Model instance)
        instance = super().save(commit=False)

        # Save the related object (EmailsNewSQL02Model instance)
        phone = PhonesNewSQL02Model.objects.create(
            phone_desc_id=self.cleaned_data['phone_desc_id'],
            phone_number=self.cleaned_data['phone_number'],
            phone_number_ext=self.cleaned_data['phone_number_ext'],
        )
        instance.phone = phone

        if commit:
            instance.save()

        return instance

    class Meta:
        model = CustomerPhonesNewSQL02Model
        fields = ['customer', 'phone']


class CustomerUpdateForm(forms.ModelForm):
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
        # add a "form-control" class to each form input
        # for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

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


class CustomerCreateForm(CustomerUpdateForm):
    class Meta(CustomerUpdateForm.Meta):
        fields = CustomerUpdateForm.Meta.fields  # + ['any_additional_field']

    # Add any additional fields or methods specific to the create form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # child form specific code


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
        fields = [
            'address_company_or_ATTN',
            'address_line_01',
            'address_city',
            'address_state', 'address_zip_code',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control text-input'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control textarea-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'custom-select'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'datetime-input'})
            # You can continue for other field types

class VehicleUpdateForm(forms.ModelForm):
    vehicle_id = forms.CharField(required=False)

    # Override the default vehicle_license_state field
    vehicle_license_state = forms.ChoiceField(
        choices=LIST_OF_STATES_IN_US, required=False, label='state')

    class Meta:
        model = VehiclesNewSQL02Model
        fields = ['vehicle_id',
                  'vehicle_cust', 'VIN_number',
                  'vehicle_license_plate_nbr', 'vehicle_license_state',
                  'vehicle_make', 'vehicle_year', 'vehicle_sub_model',
                  'vehicle_drive_type', 'vehicle_engine',
                  'vehicle_body_style', 'vehicle_brake',
                  'vehicle_transmission',
                  'vehicle_inspection_datetime',
                  'vehicle_gvw', 'vehicle_color',
                  'vehicle_recall_last_checked_datetime',
                  'vehicle_active_recall_counts',
                  'vehicle_is_included_in_crm_compaign',
                  'vehicle_memo_01', "vehicle_memo_does_print_on_order",
                  'vehicle_odometer_1', 'vehicle_odometer_2',
                  'vehicle_record_is_active',

                  ]
        # exclude = ('created_at', 'updated_at',)
        widgets = {
            'vehicle_cust': forms.Select(attrs={'class': ' form-select', 'disabled': 'True'}),
            'vehicle_memo_01': forms.TextInput(attrs={'class': 'form-control', }),
            'vehicle_recall_last_checked_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', "disabled": "True"}),
            'vehicle_is_included_in_crm_compaign': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            "vehicle_memo_does_print_on_order": forms.CheckboxInput(attrs={'type': 'checkbox'})
        }
        # forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        labels = {
            'vehicle_cust': 'customer',
            'vehicle_drive_type': 'drive type',
            'vehicle_sub_model': 'sub model',
            'vehicle_year': 'year',
            'vehicle_make': 'make',
            'vehicle_gvw': 'gross weight (lbs)',
            'vehicle_transmission': 'transmission',
            'vehicle_body_style': "body style",
            'vehicle_license_plate_nbr': 'license plate',
            'vehicle_memo_01': 'memo',
            'vehicle_memo_does_print_on_order': 'does print on order?',
            'vehicle_active_recall_counts': 'active recall counts',
            'vehicle_recall_last_checked_datetime': 'recall last checked',

        }

    def clean_VIN_number(self):
        vin = self.cleaned_data['VIN_number']

        # Strip spaces
        vin = vin.replace(" ", "")

        # Check if it has 17 digits
        if len(vin) != 17:
            raise ValidationError(
                'VIN must have 17 non-empty digits')

        # Capitalize the VIN
        return vin.upper()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control text-input'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control textarea-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'custom-select'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'datetime-input'})
            # You can continue for other field types

        # dynamically update the choices for the vhicle_license_state_field

        formatted_state_choices = [
            (abbr, f"{abbr} - {full}") for abbr, full in LIST_OF_STATES_IN_US]
        # license state can be only chosen from a list. Display custom data when there is no match.

        self.fields['vehicle_license_state'].choices = formatted_state_choices

        # Get a list of state abbreviations
        state_abbrs = [abbr for abbr, _ in LIST_OF_STATES_IN_US]

        # Check if current instance has a state value not in the list and append it
        if self.instance.vehicle_license_state and self.instance.vehicle_license_state not in state_abbrs:
            extra_choice = (self.instance.vehicle_license_state,
                            self.instance.vehicle_license_state)
            self.fields['vehicle_license_state'].choices.append(extra_choice)
        # Make vehicle_id read-only
        self.fields['vehicle_id'].widget.attrs['disabled'] = True

        # Modify choices for 'vehicle_gvw' field
        self.fields['vehicle_gvw'].choices = [
            (gvw.pk, gvw.gvw_text) for gvw in GVWsModel.objects.all()]

        # Customize the vehicle_cust field to display customer names
        self.fields['vehicle_cust'].choices = [
            (customer.pk, customer.get_customer_full_name) for customer in CustomersNewSQL02Model.objects.all()]

        # Customize the vehicle_cust field to display customer names
        self.fields['vehicle_body_style'].choices = [
            (body_style.pk, body_style.get_body_style_feature) for body_style in BodyStylesModel.objects.all()]

        # pass on the actual url that handles 'search_customer_by_phone' view function in the views.py to the vehicle_id field.
        # javascript in the vehicle_update.html will pick it up.
        search_customer_by_phone_url = reverse(
            'dashboard:search_customer_by_phone')
        self.fields['vehicle_id'].widget.attrs.update(
            {'data-url': search_customer_by_phone_url})

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = "post"
        self.helper.label_class = 'col-3'
        self.helper.field_class = 'col-9'
        # self.helper.error_text_inline = True
        # self.helper.use_custom_control = True  # for Bootstrap custom controls

        # Custom popover button
        # updated with jQuery popover udpate
        popover_html = """
        <button type="button" class="btn btn-danger" id='latest-vin-snapshot-button' data-bs-trigger="focus" data-bs-toggle="popover" data-bs-title="VIN Online" data-bs-content="some content">
            Fetch latest Vin info (Source:NHTSA)
        </button>
        <script>
        $(function(){
        
            // id=latest-vin-snapshot-button
            $("#latest-vin-snapshot-button").popover();

            $("#latest-vin-snapshot-button").on('click', function() {
                var vin = $('[name="VIN_number"]').val();
                $.ajax({
                    url: "{% url 'dashboard:fetch_or_save_latest_vin_snapshot' %}",  
                    data: {
                        'vin': vin,
                    },
                    method: 'GET',
                    dataType: 'json',
                    success: function(response) {
                        // console.log(response);
                        console.log(response.data);
                        // console.log(response.status);
                        $("#latest-vin-snapshot-button").popover('dispose'); // Destroy the current popover 
                        $("#latest-vin-snapshot-button").attr('data-bs-content', response.data);
                        $("#latest-vin-snapshot-button").popover('update');
                        $("#latest-vin-snapshot-button").popover(); // Reinitialize the popover
                        // $("#latest-vin-snapshot-button").popover('hide');
                        $("#latest-vin-snapshot-button").popover('show');
                        

                        //$("#latest-vin-snapshot-button").prop('data-bs-content', response);
                        // Update the popover content
                        //$("#latest-vin-snapshot-button").popover('update');

                    },
                    error: function(error) {
                        console.error("Error fetching VIN data:", error);
                    }
                });
            });
        });
        </script>
        """

        self.helper.layout = Layout(
            Fieldset(_('Linked Customer'),
                     #          Row(
                     #     Column('vehicle_id', css_class='col-6'),

                     # ),
                     Row(Column('vehicle_cust', css_class='col-6'),
                         Column(Button('reassign new customer',
                                       'reassign customer', css_class='btn btn-primary'),
                                css_class='col-6'),
                         ),
                     Row(css_id='vehicle_customer_search_container'),
                     ),
            Row(HTML("<hr>"), css_class='m-1 p-1'),
            Fieldset(
                _('Vehicle Info'),
                Row(
                    Column('VIN_number', css_class='col-6'),
                    # Adding the popover button
                    Column(HTML(popover_html), css_class='col-6'),
                ),

                Row(
                    Column('vehicle_license_plate_nbr', css_class='col-6'),
                    Column('vehicle_license_state', css_class='col-6'),
                ),
                Row(
                    Column('vehicle_year', css_class='col-6'),
                    Column('vehicle_make', css_class='col-6'),
                    Column('vehicle_sub_model', css_class='col-6'),
                    Column('vehicle_body_style', css_class='col-6'),
                    Column('vehicle_drive_type', css_class='col-6'),
                    Column('vehicle_engine', css_class='col-6'),
                    Column('vehicle_transmission', css_class='col-6'),
                    Column('vehicle_brake', css_class='col-6'),
                    Column('vehicle_gvw', css_class='col-6'),
                    Column('vehicle_color', css_class='col-6'),

                ),
                Row(
                    Column('vehicle_active_recall_counts', css_class='col-6'),
                    Column('vehicle_recall_last_checked_datetime',
                           css_class='col-5'),
                ),

            ),
            Row(HTML("<hr>"), css_class='m-1 p-1'),
            Fieldset(
                _('Additional info'),
                Row(
                    Column('vehicle_memo_01',
                           css_class='col-9'),
                    Column('vehicle_memo_does_print_on_order',
                           css_class='col-3'),
                    Column(Field('vehicle_is_included_in_crm_compaign', css_class=""),
                           css_class='col-6'),

                ),
            ),
            Row(HTML("<hr>"), css_class='m-1 p-1'),
            Fieldset(
                Row(
                    Field('vehicle_record_is_active'),
                )
            ),
            ButtonHolder(
                Row(
                    Column(Submit('submit', 'Apply', css_class='btn btn-primary', css_id='submit-button', style="float: left;"),
                           css_class='col col-6'),
                    Column(Reset('delete', 'Delete', css_class='btn btn-danger', css_id='danger-button', style="float: right;"),
                           css_class='col col-6'),
                    css_class='p-1 m-1'),
            ),
        )

# Vehicle Create From inherited from Vehicle Update Form


class VehicleCreateForm(VehicleUpdateForm):
    class Meta(VehicleUpdateForm.Meta):
        fields = VehicleUpdateForm.Meta.fields  # + ['any_additional_field']

    # Add any additional fields or methods specific to the create form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # child form specific code


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
            'line_item',
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

class LaborItemUpdateForm(forms.ModelForm):
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

class NoteItemUpdateForm(forms.ModelForm):

    class Meta:
        model = NoteItemsNewSQL02Model
        fields =['note_item_id','note_item_text', 
                 'note_item_tech_observation', ]
        readonly_fields = ['note_item_id','note_item_created_at', 'note_item_last_updated_at']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control text-input'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control textarea-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'custom-select'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'datetime-input'})
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.form_method = "post"

            # You can continue for other field types


RepairOrderFormSet = formset_factory(RepairOrderUpdateForm, extra=0)
CustomerFormSet = formset_factory(CustomerUpdateForm, extra=0)
AddressFormSet = formset_factory(AddressUpdateForm, extra=0)

PartItemInlineFormSet = inlineformset_factory(LineItemsNewSQL02Model, PartItemModel,
                                              form=PartItemUpdateForm, extra=0,
                                              can_delete=True,
                                              )
LaborItemInlineFormSet = inlineformset_factory(LineItemsNewSQL02Model, LaborItemModel,
                                               form=LaborItemUpdateForm,
                                               extra=0,
                                               can_delete=True,
                                               )


NoteItemInlineFormSet = inlineformset_factory(LineItemsNewSQL02Model, NoteItemsNewSQL02Model,
                                               form=NoteItemUpdateForm,
                                               extra=0,
                                               can_delete=True,
                                               )
# LineItem  UpdateForm. Parent formto PartItemUpdateForm and LaborItemUpdateForm.


class LineItemUpdateForm(AutomanBaseModelForm):
    line_item_description = forms.CharField(widget=forms.Textarea(
        attrs={"type": "text", "class": "editable-field"}), 
        label='Item Description:'),
    
    line_item_category = forms.ModelChoiceField(
        queryset=CategoryModel.objects.all(),
        required=False,
        label='category',
        to_field_name="category_description",
    )
    line_item_description = forms.CharField(widget=forms.Textarea(
        attrs={"type": "text", "class": "editable-field"}), label='Item Description:'),

    class Meta:
        model = LineItemsNewSQL02Model
        fields = [
            'line_item_id',
            'line_item_description',
            'line_item_category',
            'line_item_parent_line_item',
        ]
        readonly_fields = ['line_item_id','line_item_parent_line_item','line_item_last_updated_at','line_item_created_at' ]
        # exclude = [
        #     'line_item_parent_line_item_id',]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # add a "form-control" class to certain input types
        for name, field in self.fields.items():
            # check widget type
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select)):
                field.widget.attrs.update({'class': 'form-control'})
        # Set the queryset
        # self.fields['line_item_category'].queryset = CategoryModel.objects.all()

        # Modify the widget to display `category_desc`
        self.fields['line_item_category'].widget = forms.Select(
            choices=[(cat.pk, cat.category_description)
                     for cat in CategoryModel.objects.all()]
        )

        for name, field in self.fields.items():
            # check widget type
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select)):
                field.widget.attrs.update({'class': 'form-control'})

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.form_method = "post"


class LineItemCreateForm(LineItemUpdateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # exclude the line item id
        del self.fields['line_item_id']

# This liteEmailUpdateForm is used on the customer detail page. It allows users to edit


class LiteEmailUpdateForm(forms.ModelForm):
    email_id = forms.IntegerField(required=False)
    email_type_id = forms.ChoiceField(choices=EMAIL_TYPES, label='type')
    email_address = forms.EmailField(label='address', required=True)
    email_description = forms.CharField(
        max_length=200, label='notes:')
    email_can_send_notification = forms.BooleanField(
        required=False, label='allow notifcations')

    class Meta:
        model = EmailsNewSQL02Model
        fields = ['email_type_id',
                  'email_address', 'email_description', 'email_can_send_notification']

        widgets = {
            # 'email_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email_type_id': forms.Select(attrs={"type": "text", "class": "form-control form-select"}),
            'email_address': forms.EmailInput(attrs={"type": "text", "class": "form-control"}),
            'email_description': forms.Textarea(attrs={"type": "text", "class": "form-control editable-field"}),
            'email_can_send_notification': forms.CheckboxInput(attrs={'class': 'form-check form-control'}),
        }
        labels = {
            'email_can_send_notification': 'allow notifications?',
            'email_type_id': 'email type',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


LiteCustomerVehicleUpdateFormset = inlineformset_factory(
    CustomersNewSQL02Model, VehiclesNewSQL02Model, edit_only=True,
    fields=('vehicle_id', 'VIN_number', 'vehicle_license_plate_nbr'), fk_name='vehicle_cust')


# this form was created on 2023-10-09. used in `vehicles/fetch-single-vin-search-nhtsa-api`.
# takes a vin and model year and returns an json response with detailed vehicle info from NHTSA gov.
# the form validates the vin to be 17-digit long and model year to be equal or less than this year plus 1.
class VINSearchForm(forms.Form):
    vin = forms.CharField(required=True,
                          label='Vehicle Identification Number(VIN)',
                          help_text='required. Enter full 17 digits',
                          widget=forms.TextInput(
                              attrs={'class': 'form-control', 'placeholer': 'example: 5YJSX********'}))
    year = forms.IntegerField(required=False,
                              label='Model Year',
                              help_text="optional",
                              widget=forms.NumberInput(
                                  attrs={'class': 'form-control', 'placeholder': 'vehicle year'}))

    def clean_vin(self):
        vin = self.cleaned_data['vin']

        # Strip spaces
        vin = vin.replace(" ", "")

        # Check if it has 17 digits
        if len(vin) != 17:
            raise ValidationError(
                'VIN must have 17 non-empty digits')

        # Capitalize the VIN
        return vin.upper()

    def clean_year(self):
        year = self.cleaned_data['year']
        if not year:
            return None

        current_year = datetime.now().year

        # Check if year is valid
        if year > current_year + 1 or year < 1900:  # Assuming no vehicle will be from before 1900
            raise forms.ValidationError(
                f'Model year must be between 1900 and {current_year + 1}')
        return year

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # exclude the line item id


class LicensePlateSearchForm(forms.Form):
    license_plate = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter license plate number.'}))
    state = forms.ChoiceField(choices=[('', '--- None ---')] + list(LIST_OF_STATES_IN_US), widget=forms.Select(
        attrs={'class': 'form-select'}))

    def clean_license_plate(self):
        license_plate = self.cleaned_data['license_plate']
        if len(license_plate) > 10:
            raise ValidationError(
                'License plate number must not be more than 10 characters long.')
        return license_plate.strip().upper()

    def clean_state(self):
        state = self.cleaned_data['state']
        if state and state not in dict(LIST_OF_STATES_IN_US):
            raise ValidationError('Invalid US state abbreviation.')
        return state

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # exclude the line item id
