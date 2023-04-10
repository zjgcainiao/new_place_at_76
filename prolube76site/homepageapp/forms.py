from django import forms
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model , RepairOrdersNewSQL02Model,AddressesNewSQL02Model
from homepageapp.models import RepairOrderLineItemSquencesNewSQL02Model
from django.forms import formset_factory
from django.db.models import Prefetch
class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = CustomersNewSQL02Model
        fields = ['customer_id', 'customer_first_name','customer_last_name', 'customer_dob',
                  'customer_does_allow_SMS','customer_memo_1',
                  'customer_is_okay_to_charge','customer_is_in_social_crm',
                  ]

class AddressModelForm(forms.ModelForm):
    class Meta:
        model = AddressesNewSQL02Model
        fields = ['address_line_01','address_city','address_state','address_zip_code']

class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = VehiclesNewSQL02Model
        fields = ['vehicle_id','vehicle_cust_id','VIN_number','vehicle_memo_01','vehicle_odometer_1']
        # exclude = ('created_at', 'updated_at',)

# Create your views here.
class RepairOrderModelForm(forms.ModelForm):
    class Meta:
        model = RepairOrdersNewSQL02Model
        fields = ['repair_order_id',
                  'repair_order_customer',
                  'repair_order_phase',
                  'repair_order_created_as_estimate',
                  'repair_order_is_printed',
                  'repair_order_aggr_notes',
                  'repair_order_snapshot_order_total_amount',
                  ]
        widgets = {
            'repair_order_customer': forms.TextInput(attrs={}),
            'repair_order_phase': forms.TextInput(attrs={}),
        }
    def get_queryset(self):
        ## `__` double undestore..more researched are needed.
        qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_phase')).filter(repair_order_id=self.kwargs['pk'])
        # qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_customer__addresses'))
        # qs = qs.filter(repair_order_id=self.kwargs['pk']).get()
        # qs = qs.prefetch()
        return qs


        
# RepairOrderFormSet = formset_factory(RepairOrderModelForm, extra=0)
# CustomerFormSet = formset_factory(CustomerModelForm, extra=0)
# AddressFormSet = formset_factory(AddressModelForm, extra=0)

# class DashboardForm(forms.ModelForm):
#     customer = forms.ModelChoiceField(queryset=CustomersNewSQL02Model.objects.all())
#     address = forms.ModelChoiceField(queryset=AddressesNewSQL02Model.objects.all())
#     class Meta:
#         model = RepairOrdersNewSQL02Model
#         fields = ['repair_order_id', 'repair_order_created_as_estimate', 'repair_order_customer',  'repair_order_snapshot_order_total_amount','customer', 'address',]
        # example of error messages
        # class Meta:
            # error_messages = {
            #     NON_FIELD_ERRORS: {
            #         'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            #     }
            # }
            #     field_classes = {
            #     'slug': MySlugFormField,
            #     }
            #     fields = ['title', 'author', 'published_date']
            #     widgets = {
            #     'published_date': DateInput(attrs={'type': 'date'})
            #     }
            #     labels = {
            #         'title': 'Book Title',
            #         'published_date': 'Publication Date'
            #     }


class RepairOrderLineItemModelForm(forms.ModelForm):
    model = RepairOrderLineItemSquencesNewSQL02Model

    class Meta:
        excluded = ['line_item_last_updated_date', 'line_Item_parent_line_item_id',]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['line_item'].queryset = LineItem.objects.all()