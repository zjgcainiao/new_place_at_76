from django import forms
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model, RepairOrdersNewSQL02Model, AddressesNewSQL02Model
from homepageapp.models import RepairOrderLineItemSquencesNewSQL02Model, PartItemModel, LaborItemModel, LineItemsNewSQL02Model
from django.forms import formset_factory
from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div


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
        # `__` double undestore..more researched are needed.
        # queryset = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_phase')).filter(repair_order_id=self.kwargs['pk'])
        # qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_customer__addresses'))
        # qs = qs.filter(repair_order_id=self.kwargs['pk']).get()
        # qs = qs.prefetch()

# class WIPModelForm(forms.ModelForm):
#     class Meta:
#         model = RepairOrdersNewSQL02Model
#         fields = ['repair_order_id',
#                   'repair_order_customer',
#                   'repair_order_phase',
#                   'repair_order_created_as_estimate',
#                   'repair_order_is_printed',
#                   'repair_order_aggr_notes',
#                   'repair_order_snapshot_order_total_amount',
#                   ]
#         widgets = {
#             'repair_order_customer': forms.TextInput(attrs={}),
#             'repair_order_phase': forms.TextInput(attrs={}),
#         }
#     def get_queryset(self):
#         ## `__` double undestore..more researched are needed.
#         qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_phase')).filter(repair_order_id=self.kwargs['pk'])
#         # qs = RepairOrdersNewSQL02Model.objects.prefetch_related(Prefetch('repair_order_customer__addresses'))
#         # qs = qs.filter(repair_order_id=self.kwargs['pk']).get()
#         # qs = qs.prefetch()
#         return qs


RepairOrderFormSet = formset_factory(RepairOrderModelForm, extra=0)


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

    class Meta:
        model = RepairOrderLineItemSquencesNewSQL02Model
        exclude = ['line_item_last_updated_date',
                   'line_item_parent_line_item_id',]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['line_item'].queryset = LineItem.objects.all()


class PartItemModelForm(forms.ModelForm):
    part_item_quantity = forms.IntegerField(min_value=0, max_value=100)
    part_item_is_confirmed = forms.BooleanField()
    part_item_is_quantity_confirmed = forms.BooleanField()

    class Meta:
        model = PartItemModel
        fields = [
            'line_item',
            'part_item_part_no',
            'part_discount_description',
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
            'part_item_quantity': forms.NumberInput(attrs={'type': 'text', 'class': 'form-control', }),
            'part_item_unit_price': forms.NumberInput(attrs={'type': 'text', 'class': 'form-control', }),
            'part_item_unit_list': forms.NumberInput(attrs={'type': 'text', 'class': 'form-control', }),
            'part_item_unit_sale': forms.NumberInput(attrs={'type': 'text', 'class': 'form-control', }),
            'part_item_unit_cost': forms.NumberInput(attrs={'type': 'text', 'class': 'form-control', }),
            'part_item_unit_price': forms.NumberInput(attrs={'type': 'text', 'class': 'form-control', }),
            'part_item_unit_price': forms.NumberInput(attrs={'type': 'text', 'class': 'form-control', }),
            'part_item_is_confirmed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'part_item_shipping_description': forms.TextInput(attrs={}),
        }

        labels = {
            'part_item_is_confirmed': 'Is this part has been confirmed? ',

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


class LaborItemModelForm(forms.ModelForm):
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
            'labor_item_hours_charged': forms.NumberInput(attrs={'class': 'form-control', }),
            'labor_item_symptom': forms.TextInput(attrs={'class': 'form-control', }),
            'labor_item_parts_estimate': forms.NumberInput(attrs={'class': 'form-control', }),

            'labor_item_is_user_entered_labor_rate': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
                                        widgets={'part_item_quantity': forms.NumberInput(attrs={'class': 'form-control', 'type': 'text'}),
                                                 'part_item_unit_price': forms.NumberInput(attrs={'class': 'form-control', 'type': 'text'}),
                                                 'part_item_unit_list': forms.NumberInput(attrs={'class': 'form-control', 'type': 'text'}),
                                                 'part_item_unit_sale': forms.NumberInput(attrs={'class': 'form-control', 'type': 'text'}),
                                                 'part_item_unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'type': 'text'}),
                                                 'part_item_unit_plist': forms.NumberInput(attrs={'class': 'form-control', 'type': 'text'}),
                                                 'part_item_unit_price': forms.NumberInput(attrs={'class': 'form-control', }),
                                                 'part_item_is_confirmed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                                 'part_item_is_user_entered_unit_sale': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                                                                                   'readonly': True}),
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
                                         widgets={'labor_item_hours_charged': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', }),
                                                  'labor_item_symptom': forms.TextInput(attrs={'class': 'form-control', }),
                                                  'labor_item_parts_estimate': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', }),

                                                  'labor_item_is_user_entered_labor_rate': forms.CheckboxInput(attrs={'readonly': 'readonly'}),
                                                  # 'line_item': forms.TextInput(attrs={'class': 'form-control',
                                                  #                                     'readonly': 'readonly'}),
                                                  'labor_item_symptom': forms.Textarea(attrs={'class': 'form-control', }), },
                                         extra=0,
                                         )

