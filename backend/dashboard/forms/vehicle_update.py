from django.forms import ValidationError
from .base import forms, FormHelper, Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden
from core_operations.constants import LIST_OF_STATES_IN_US
from homepageapp.models import VehiclesNewSQL02Model, GVWsModel, CustomersNewSQL02Model, BodyStylesModel
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

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