from django.db import models
from django.urls import reverse
# from computedfields.models import ComputedFieldsModel, computed, compute
from django.db.models import Count
from django.utils import timezone
# added on 2022-10-29 so the load_env
import os
# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
from dotenv import load_dotenv
# documentation for py-mssql is https://pymssql.readthedocs.io/en/stable/pymssql_examples.html#basic-features-strict-db-api-compliance
# import pymssql

# from prolube76site.polls.views import all_repair_orders 

class CustomersNewSQL01Model(models.Model):
    customer_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
    # primary key = True
    customer_id = models.IntegerField(null=True)
    customer_title_id = models.CharField(max_length=20, null=True)
    customer_first_name = models.CharField(max_length=50, null=True)
    customer_last_name = models.CharField(max_length=50, null=True)
    customer_middle_name = models.CharField(max_length=50, null=True)
    customer_dob = models.DateTimeField(null=True)
    customer_spouse_name = models.CharField(max_length=50, null=True)
    customer_primary_phone_uid = models.CharField(max_length=36, null=True, primary_key=False)
    customer_primary_email_uid = models.CharField(max_length=36, null=True, primary_key=False)
    customer_is_okay_to_charge = models.BooleanField(default=True)
    customers_memo_1 = models.CharField(max_length=4000, null=True)
    customer_is_tax_exempt = models.BooleanField(default=False)
    customer_resale_permit_nbr = models.CharField(max_length=20, null=True)
    customer_is_in_social_crm = models.BooleanField(default=True)
    customer_hear_from_us_type = models.CharField(max_length=20, null=True)
    customer_last_visit_date = models.DateTimeField(null=True)
    customer_first_visit_date = models.DateTimeField(null=True)
    customer_is_deleted = models.BooleanField(default=False)
    customer_memebership_nbr = models.CharField(max_length=20, null=True)
    customer_does_allow_SMS = models.BooleanField(default=True)
    customer_email_address_in_json = models.CharField(max_length=200, null=True)
    customer_last_updated_datetime = models.DateTimeField(auto_now=True)
    customer_is_created_from_appointments = models.BooleanField(default=False)
    customer_fleet_vendor_id = models.CharField(max_length=20, null=True)
    customer_created_at = models.DateTimeField(auto_now_add=True)
    # custom the corresponding data table name for this model
    class Meta:
        db_table = 'customers_new_01'  #'AERODROMES' # prolube76DBSTG01.dbo.customers_new_01
        ordering = ["-customer_id"]
    
    # def get_absolute_url(self):
    #     return reverse('author-detail', kwargs={'pk': self.pk})



class PhonesNewSQL01Model(models.Model):
    phone_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)  
    phone_id = models.IntegerField(null=True)
    phone_desc_id = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    phone_number_ext = models.CharField(max_length=20, null=True)
    phone_displayed_name = models.CharField(max_length=20, null=True)
    phone_memo_01 = models.CharField(max_length=100, null=True)
    phone_created_at = models.DateTimeField(null=True)
    phone_last_updated_date = models.DateTimeField(null=True,auto_now=True)
    # custom the corresponding data table name for this model
    class Meta:
        db_table = 'phones_news_01' 
        ordering = ["-phone_id"]

class VehiclesNewSQL01Model(models.Model):
    vehicle_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)  # default = uuid.uuid4
    vehicle_id = models.CharField(max_length=20, null=True)
    vehicle_cust_id = models.CharField(max_length=20, null=True)
    vehicle_year = models.CharField(max_length=20, null=True)
    vehicle_make_id = models.CharField(max_length=20, null=True)
    vehicle_sub_model_id = models.CharField(max_length=20, null=True)
    vehicle_body_style_id = models.CharField(max_length=20, null=True)
    vehicle_engine_id = models.CharField(max_length=20, null=True)
    vehicle_transmission_id = models.CharField(max_length=20, null=True)
    vehicle_brake_id = models.CharField(max_length=20, null=True)
    vehicle_drive_type_id  = models.CharField(max_length=20, null=True)
    vehicle_GVW_id     = models.CharField(max_length=20, null=True)
    vehicle_odometer_1   = models.BigIntegerField(null=True)
    vehicle_odometer_2   = models.BigIntegerField(null=True)
    VIN_number   = models.CharField(max_length=50, null=True)
    vehicle_inspection_datetime = models.DateTimeField(null=True)
    vehicle_last_in_date    = models.DateTimeField(null=True)
    vehicle_license_plate_nbr = models.CharField(max_length=20, null=True)
    vehicle_license_state  = models.CharField(max_length=20, null=True)
    vehicle_part_level     = models.CharField(max_length=20, null=True)
    vehicle_labor_level    = models.CharField(max_length=20, null=True)
    vechicle_used_level      = models.CharField(max_length=20, null=True)
    vehicle_memo_01        = models.CharField(max_length=4000, null=True)
    vehicle_memo_does_print_on_order = models.BooleanField(default=False)
    vehicle_is_included_in_CRM_compaign = models.BooleanField(default=True)
    vehicle_color          = models.CharField(max_length=20, null=True)
    vehicle_record_is_activate  = models.BooleanField(default=True)
    vehicle_class_id     = models.CharField(max_length=20, null=True)
    vehicle_engine_hour_in   = models.DecimalField(max_digits=7, decimal_places=1)
    vehicle_engine_hour_out = models.DecimalField(max_digits=7, decimal_places=1)
    vehicle_active_recall_counts = models.IntegerField(null=True)
    vehicle_recall_last_checked_datetime = models.DateTimeField(null=True)
    vehicle_last_updated_datetime       = models.DateTimeField(auto_now=True, null=True)
    vehicle_phone_id      = models.CharField(max_length=20, null=True)
    vehicle_customer_new_uid   = models.CharField(max_length=36, null=True) 
    vehicle_contact_phone_main_new_uid  = models.CharField(max_length=36, null=True) 
    vehicle_created_at  = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'vehicles_new_01'
        ordering = ["-vehicle_id"]


class RepairOrdersNewSQL01Model(models.Model):
    repair_order_new_uid_v01 = models.UUIDField(primary_key=True)  # models.UUIDField(primary_key=True)  # models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
    repair_order_id = models.IntegerField(null=True)
    repair_order_phase_id = models.CharField(max_length=20, null=True)
    repair_order_cust_id = models.CharField(max_length=20, null=True)
    repair_order_customer_new_uid = models.CharField(max_length=20, null=True)
    # models.ForeignKey(CustomersNewSQL01Model, on_delete=models.CASCADE, null=True,db_column='customer_new_uid_v01')
    repair_order_vehicle_id = models.CharField(max_length=20, null=True)
    repair_order_serviced_vehicle_new_uid = models.CharField(max_length=36, null=True, primary_key=False) 
    repair_order_serviced_vehicle_location = models.CharField(max_length=36, null=True) 
    repair_order_service_status = models.CharField(max_length=36, null=True) 
    repair_order_scheduled_start_datetime = models.DateTimeField(null=True)
    repair_order_billed_hours = models.DurationField(null=True, blank=False)  # blank = False so this is a required field on form (pending testing)
    repair_order_promise_datetime = models.DateTimeField(null=True)
    repair_order_is_printed = models.BooleanField(default=False)
    repair_order_invoice_is_printed = models.BooleanField(default=False)
    repair_order_serviced_vehicle_in_datetime = models.DateTimeField(null=True)
    repair_order_serviced_vehicle_out_datetime = models.DateTimeField(null=True)
    repair_order_serviced_vehicle_hat = models.CharField(max_length=20, null=True)
    repair_order_posted_datetime = models.DateTimeField(null=True)
    repair_order_serviced_vehicle_odometer_in = models.BigIntegerField(null=True)
    repair_order_odometer_out = models.BigIntegerField(null=True)
    repair_order_reference_number = models.CharField(max_length=30, null=True)
    repair_order_receipt_printed_datetime = models.DateTimeField(null=True)
    repair_order_snapshot_is_tax_exempt = models.BooleanField(default=False)
    repair_order_aggr_notes = models.CharField(max_length=4000, null=True)
    repair_order_observation_text_area = models.CharField(max_length=4000, null=True)
    repair_order_created_as_estimate = models.BooleanField(default=False)  # connecting to the estimates
    repair_order_snapshot_margin_pct = models.DecimalField(max_digits=5, decimal_places=2)
    repair_order_snapshot_haz_waste_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_labor_sale_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_parts_sale_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_supply_from_shop_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_tax_haz_material_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_tax_supply_from_shop_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_total_tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_balance_due_adjusted = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_discounted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_part_discounted_desc_id = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_labor_discounted_desc_id = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_order_total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_calc_haz_waste_cost = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_calc_shop_supply_cost = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_serviced_vehcle_engine_hours_in = models.DecimalField(max_digits=7, decimal_places=1)
    repair_order_serviced_vehcle_engine_hours_out = models.DecimalField(max_digits=7, decimal_places=1)
    repair_order_appointment_request_uid = models.CharField(max_length=50, null=True)

    repair_order_created_at = models.DateTimeField(auto_now_add=True)
    repair_order_last_updated_datetime = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'repairorders_new_01'
        ordering = ["-repair_order_id"]

# -------------------  2023-03-29 stop using the new uid ----------------
# uid takes too much space and storage.
# revert back to the existing old id, such as customer_id, vehicle_id, repair_order_id, phone_id.
# add majority of data tables for testing
class AddressesNewSQL02Model(models.Model):
    address_id = models.AutoField(primary_key=True)
    address_type_id = models.IntegerField()
    address_company_or_ATTN = models.CharField(max_length=30,blank=True)
    address_line_01 = models.CharField(max_length=30,blank=True)
    address_city = models.CharField(max_length=20,blank=True)
    address_state = models.CharField(max_length=30,blank=True)
    address_zip_code = models.IntegerField()
    address_created_at = models.DateTimeField(auto_now_add=True)
    address_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'addresses_new_02'
        ordering = ["-address_id"]
        verbose_name = 'address'
        verbose_name_plural='addresses'



class CustomersNewSQL02Model(models.Model):
    # customer_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
    # primary key = True
    customer_id = models.AutoField(primary_key=True)
    customer_title_id = models.CharField(max_length=20, null=True)
    customer_first_name = models.CharField(max_length=50, null=True)
    customer_last_name = models.CharField(max_length=50, null=True)
    customer_middle_name = models.CharField(max_length=50, null=True)
    customer_dob = models.DateTimeField(null=True)
    customer_spouse_name = models.CharField(max_length=50, null=True)
    # customer_primary_phone_uid = models.CharField(max_length=36, null=True)
    # customer_primary_email_uid = models.CharField(max_length=36, null=True)
    customer_is_okay_to_charge = models.BooleanField(default=True)
    customers_memo_1 = models.CharField(max_length=4000, null=True)
    customer_is_tax_exempt = models.BooleanField(default=False)
    customer_resale_permit_nbr = models.CharField(max_length=20, null=True)
    customer_is_in_social_crm = models.BooleanField(default=True)
    customer_hear_from_us_type = models.CharField(max_length=20, null=True)
    customer_last_visit_date = models.DateTimeField(null=True)
    customer_first_visit_date = models.DateTimeField(null=True)
    customer_is_deleted = models.BooleanField(default=False)
    customer_memebership_nbr = models.CharField(max_length=20, null=True)
    customer_does_allow_SMS = models.BooleanField(default=True)
    customer_email_address_in_json = models.CharField(max_length=200, null=True)
    customer_last_updated_date = models.DateTimeField(auto_now=True)
    customer_is_created_from_appointments = models.BooleanField(default=False)
    customer_fleet_vendor_id = models.CharField(max_length=20, null=True)
    customer_created_at = models.DateTimeField(auto_now_add=True)
    # add a new many-to-many-relationship field
    addresses = models.ManyToManyField(AddressesNewSQL02Model, through='CustomerAddressesNewSQL02Model',related_name='addresses')

    class Meta:
        db_table = 'customers_new_02'   # prolube76DBSTG01.dbo.customers_new_01
        ordering = ["-customer_id"]
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

class CustomerAddressesNewSQL02Model(models.Model):
    address = models.ForeignKey(AddressesNewSQL02Model, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.CASCADE)
    customeraddress_address_created_at = models.DateTimeField(auto_now_add=True)
    customeraddress_last_updated_date = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = 'customeraddresses_new_02' 
        ordering = ["-address_id", '-customer_id']
        # verbose_name = 'customeraddress'
        # verbose_name_plural = 'customeraddresses'

# ---- 2023-04-03 repairorderphase model is added ----
class RepairOrderPhasesNewSQL02Model(models.Model):
    repair_order_phase_id = models.AutoField(primary_key=True)
    repair_order_phase_description = models.CharField(max_length=50)
    class Meta:
        db_table = 'repairorderphases_new_02'
        ordering = ["repair_order_phase_id"]
        verbose_name = 'repairorderphase'
        verbose_name_plural = 'repairorderphases'


class VehiclesNewSQL02Model(models.Model):
    # vehicle_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)  # default = uuid.uuid4
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_cust_id = models.CharField(max_length=20, null=True)
    vehicle_year = models.CharField(max_length=20, null=True)
    vehicle_make_id = models.CharField(max_length=20, null=True)
    vehicle_sub_model_id = models.CharField(max_length=20, null=True)
    vehicle_body_style_id = models.CharField(max_length=20, null=True)
    vehicle_engine_id = models.CharField(max_length=20, null=True)
    vehicle_transmission_id = models.CharField(max_length=20, null=True)
    vehicle_brake_id = models.CharField(max_length=20, null=True)
    vehicle_drive_type_id = models.CharField(max_length=20, null=True)
    vehicle_GVW_id = models.CharField(max_length=20, null=True)
    vehicle_odometer_1 = models.BigIntegerField(null=True)
    vehicle_odometer_2 = models.BigIntegerField(null=True)
    VIN_number = models.CharField(max_length=50, null=True)
    vehicle_inspection_datetime = models.DateTimeField(null=True)
    vehicle_last_in_date = models.DateTimeField(null=True)
    vehicle_license_plate_nbr = models.CharField(max_length=20, null=True)
    vehicle_license_state  = models.CharField(max_length=20, null=True)
    vehicle_part_level     = models.CharField(max_length=20, null=True)
    vehicle_labor_level    = models.CharField(max_length=20, null=True)
    vechicle_used_level      = models.CharField(max_length=20, null=True)
    vehicle_memo_01        = models.CharField(max_length=4000, null=True)
    vehicle_memo_does_print_on_order = models.BooleanField(default=False)
    vehicle_is_included_in_CRM_compaign = models.BooleanField(default=True)
    vehicle_color          = models.CharField(max_length=20, null=True)
    vehicle_record_is_activate  = models.BooleanField(default=True)
    vehicle_class_id     = models.CharField(max_length=20, null=True)
    vehicle_engine_hour_in   = models.DecimalField(max_digits=7, decimal_places=1)
    vehicle_engine_hour_out = models.DecimalField(max_digits=7, decimal_places=1)
    vehicle_active_recall_counts = models.IntegerField(null=True)
    vehicle_recall_last_checked_datetime = models.DateTimeField(null=True)
    vehicle_last_updated_datetime       = models.DateTimeField(auto_now=True, null=True)
    vehicle_phone_id      = models.CharField(max_length=20, null=True)
    vehicle_customer_new_uid   = models.CharField(max_length=36, null=True) 
    vehicle_contact_phone_main_new_uid  = models.CharField(max_length=36, null=True) 
    vehicle_created_at  = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'vehicles_new_02'
        ordering = ["-vehicle_id"]
        verbose_name = 'vehicle'
        verbose_name_plural = 'vehicles'





# remove the new_uid_v01. not pratical.
class PhonesNewSQL02Model(models.Model):   
    phone_id = models.AutoField(primary_key=True)
    phone_desc_id = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    phone_number_ext = models.CharField(max_length=10, blank=True, null=True)
    phone_displayed_name = models.CharField(max_length=100)
    phone_memo_01 = models.TextField(blank=True, null=True)
    phone_created_at = models.DateTimeField(auto_now_add=True)
    phone_last_updated_date = models.DateTimeField(auto_now=True)
    # custom the corresponding data table name for this model
    class Meta:
        db_table = 'phones_news_02' 
        ordering = ["-phone_id"]
        verbose_name='phone'
        verbose_name_plural='phones'

    




class RepairOrdersNewSQL02Model(models.Model):
    # repair_order_new_uid_v01 = models.UUIDField(primary_key=True)  # models.UUIDField(primary_key=True)  # models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
    repair_order_id = models.AutoField(primary_key=True)
    repair_order_phase = models.ForeignKey(RepairOrderPhasesNewSQL02Model, on_delete=models.SET_NULL,blank=True, null=True)
    
    # remove the `_id` from the field name. due to recent adding a foreign key.. by adding a foreign key field, Django will add '_id' for the field in the SQL data table.
    repair_order_customer = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='customers') 
    # repair_order_customer_new_uid = models.CharField(max_length=20, null=True)
    # models.ForeignKey(CustomersNewSQL01Model, on_delete=models.CASCADE, null=True,db_column='customer_new_uid_v01')
    repair_order_vehicle = models.ForeignKey(VehiclesNewSQL02Model, on_delete=models.SET_NULL,null=True)
    # repair_order_serviced_vehicle_new_uid = models.CharField(max_length=36, null=True, primary_key=False) 
    repair_order_serviced_vehicle_location = models.CharField(max_length=36, null=True) 
    repair_order_service_status = models.CharField(max_length=36, null=True) 
    repair_order_scheduled_start_datetime = models.DateTimeField(null=True)
    repair_order_billed_hours = models.DurationField(null=True, blank=False)  # blank = False so this is a required field on form (pending testing)
    repair_order_promise_datetime = models.DateTimeField(null=True)
    repair_order_is_printed = models.BooleanField(default=False)
    repair_order_invoice_is_printed = models.BooleanField(default=False)
    repair_order_serviced_vehicle_in_datetime = models.DateTimeField(null=True)
    repair_order_serviced_vehicle_out_datetime = models.DateTimeField(null=True)
    repair_order_serviced_vehicle_hat = models.CharField(max_length=20, null=True)
    repair_order_posted_datetime = models.DateTimeField(null=True)
    repair_order_serviced_vehicle_odometer_in = models.BigIntegerField(null=True)
    repair_order_serviced_vehicle_odometer_out = models.BigIntegerField(null=True)
    repair_order_reference_number = models.CharField(max_length=30, null=True)
    repair_order_receipt_printed_datetime = models.DateTimeField(null=True)
    repair_order_snapshot_is_tax_exempt = models.BooleanField(default=False)
    repair_order_aggr_notes = models.CharField(max_length=4000, null=True)
    repair_order_observation_text_area = models.CharField(max_length=4000, null=True)
    repair_order_created_as_estimate = models.BooleanField(default=False)  # connecting to the estimates
    repair_order_snapshot_margin_pct = models.DecimalField(max_digits=5, decimal_places=2)
    repair_order_snapshot_haz_waste_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_labor_sale_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_parts_sale_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_supply_from_shop_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_tax_haz_material_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_tax_supply_from_shop_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_total_tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_balance_due_adjusted = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_discounted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_part_discounted_desc_id = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_labor_discounted_desc_id = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_order_total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_calc_haz_waste_cost = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_snapshot_calc_shop_supply_cost = models.DecimalField(max_digits=15, decimal_places=2)
    repair_order_serviced_vehcle_engine_hours_in = models.DecimalField(max_digits=7, decimal_places=1)
    repair_order_serviced_vehcle_engine_hours_out = models.DecimalField(max_digits=7, decimal_places=1)
    repair_order_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    repair_order_appointment_request_uid = models.CharField(max_length=50, null=True)
    repair_order_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'repairorders_new_02'
        ordering = ["-repair_order_id"]
        verbose_name = 'repairorder'
        verbose_name_plural='repairorders'



class OrderRevisionNewSQL02Model(models.Model):
    order_revision_id = models.AutoField(primary_key=True)
    order_revision_repair_order_id = models.ForeignKey(RepairOrdersNewSQL02Model, models.SET_NULL, blank=True, null=True)
    order_revision_sub_estimate_number = models.IntegerField(blank=True, null= True)
    order_revision_date = models.DateTimeField(null=True)
    time_of_call = models.DateTimeField(null=True)
    order_revision_initiated_by = models.CharField(max_length=20,null=True)
    order_revision_by_service_writer_id = models.IntegerField(null=True)
    order_revision_authorizaton_by_name = models.CharField(max_length=50, null=True)
    order_revision_number_called = models.CharField(max_length=50, null=True)
    order_revision_reason = models.CharField(max_length=200, null=True)
    order_revision_current_estimate = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_revision_amount = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_vehicle_id = models.ForeignKey(VehiclesNewSQL02Model,models.SET_NULL, blank=True, null=True)
    order_revision_labor_amount = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_parts_amount = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_sublet_amount = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_haz_waste_amount = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_shop_supplies_amount = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_tax_amount_haz_mat = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_tax_amount_shop_supplies = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_discounted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_tax_charged = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_tire_fee_amount = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_created_at = models.DateTimeField(auto_now_add=True)
    order_revision_last_updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'orderrevisions_new_02'
        ordering = ["-order_revision_id"]

class CannedJobsNewSQL02Model(models.Model):
    canned_job_id = models.AutoField(primary_key=True)
    canned_job_title = models.CharField(max_length=50, null=True)
    canned_job_description = models.CharField(max_length=200, null=True)
    canned_job_is_in_quick_menu = models.BooleanField(default=False)
    canned_job_cateory_id = models.IntegerField(blank=True, null=True)
    canned_job_applied_year = models.IntegerField(blank=True, null=True)
    canned_job_applied_make_id = models.IntegerField(blank=True, null=True)
    canned_job_applied_submodel_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'cannedjobs_new_02'
        ordering = ["-canned_job_id"]


class LineItemsNewSQL02Model(models.Model):
    line_item_id = models.AutoField(primary_key=True)
    line_item_acct_class_id = models.IntegerField()
    line_item_category_id = models.IntegerField()
    line_item_description = models.CharField(max_length=100)
    Line_item_cost = models.DecimalField(max_digits=5,decimal_places=2)
    line_item_sale = models.DecimalField(max_digits=5,decimal_places=2)
    line_item_is_tax_exempt = models.BooleanField(default=False)
    line_item_has_no_commission = models.BooleanField(default=True)
    line_item_has_fixed_commission = models.BooleanField(default=False)
    line_item_order_revision_id = models.ForeignKey(OrderRevisionNewSQL02Model, models.SET_NULL, blank=True, null=True)
    line_item_canned_job_id = models.ForeignKey(CannedJobsNewSQL02Model, models.SET_NULL, blank=True, null=True)

    line_item_labor_sale = models.DecimalField(max_digits=5,decimal_places=2)
    line_item_part_sale = models.DecimalField(max_digits=5,decimal_places=2)
    line_item_part_only_sale = models.DecimalField(max_digits=5,decimal_places=2)
    line_item_labor_only_sale = models.DecimalField(max_digits=5, decimal_places=2)
    line_item_sublet_sale = models.DecimalField(max_digits=5,decimal_places=2)
    line_item_package_sale = models.DecimalField(max_digits=5,decimal_places=2)
    line_item_tire_fee = models.DecimalField(max_digits=5,decimal_places=2)
    line_Item_parrent_line_item_id = models.IntegerField()

    line_item_created_at = models.DateTimeField(auto_now_add=True)
    line_item_last_updated_date = models.DateTimeField(null=True, auto_now=True)
 
    class Meta:
        db_table = 'lineitems_new_02' 
        ordering = ["-line_item_id"]


class NoteItemsNewSQL02Model(models.Model):
    note_item_id = models.AutoField(primary_key=True)
    line_item_id = models.ForeignKey(LineItemsNewSQL02Model, on_delete = models.CASCADE)
    note_text = models.TextField()
    is_printed_on_order = models.BooleanField(default=True)
    tech_observation = models.TextField()
    note_item_created_at = models.DateTimeField(auto_now_add=True)
    note_item_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'noteitems_new_02' 
        ordering = ["-note_item_id"]
        verbose_name = 'noteitem'
        verbose_name_plural='noteitems'


class lineItemTaxesNewSQL02Model(models.Model):
    line_item_id = models.IntegerField()
    line_item_tax_id = models.IntegerField()
    line_item_tax_charged = models.DecimalField(max_digits=5,decimal_places=2)
    line_item_tax_rate = models.DecimalField(max_digits=5,decimal_places=2)
    line_item_tax_created_at = models.DateTimeField(auto_now_add=True)
    line_item_tax_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'lineitemtaxes_new_02' 
        ordering = ["-line_item_id"]
 

# from django.db import models

# class Customer(models.Model):
#     customer_id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_updated_at = models.DateTimeField(auto_now=True)

# class RepairOrder(models.Model):
#     repair_order_id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     repair_order_status = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_updated_at = models.DateTimeField(auto_now=True)

# class Address(models.Model):
#     address_id = models.AutoField(primary_key=True)
#     street = models.CharField(max_length=100)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     zip_code = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_updated_at = models.DateTimeField(auto_now=True)

# class CustomerAddress(models.Model):
#     customer_address_id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     address = models.ForeignKey(Address, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_updated_at = models.DateTimeField(auto_now=True)

# class Phone(models.Model):
#     phone_id = models.AutoField(primary_key=True)
#     phone_number = models.CharField(max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_updated_at = models.DateTimeField(auto_now=True)

# class CustomerPhone(models.Model):
#     customer_phone_id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_updated_at = models.DateTimeField(auto_now=True)
