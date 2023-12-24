from django.db import models
# from computedfields.models import ComputedFieldsModel, computed, compute

# # the lookup table for NHTSA APIs. already exists in homepageapp.models 
# class NhtsaVariableLookup(models.Model):
#     id = models.AutoField(primary_key=True)
#     nhtsa_variable_id = models.CharField(max_length=20, null=True)
#     nhtsa_variable_name = models.CharField(max_length=100, null=True)
#     nhtsa_variable_data_type = models.CharField(max_length=50, null=True)
#     nhtsa_variable_description = models.CharField(max_length=4000, null=True)
#     nhtsa_variable_group_name = models.CharField(max_length=100, null=True)
#     last_updated_at = models.DateTimeField(null=True, auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)





# class VehiclesNewSQL01Model(models.Model):
#     vehicle_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)  # default = uuid.uuid4
#     vehicle_id        = models.CharField(max_length=20, null=True)
#     vehicle_cust_id   = models.CharField(max_length=20, null=True)
#     vehicle_year     = models.CharField(max_length=20, null=True)
#     vehicle_make_id  = models.CharField(max_length=20, null=True)
#     vehicle_sub_model_id = models.CharField(max_length=20, null=True)
#     vehicle_body_style_id = models.CharField(max_length=20, null=True)
#     vehicle_engine_id  = models.CharField(max_length=20, null=True)
#     vehicle_transmission_id = models.CharField(max_length=20, null=True)
#     vehicle_brake_id  = models.CharField(max_length=20, null=True)
#     vehicle_drive_type_id  = models.CharField(max_length=20, null=True)
#     vehicle_GVW_id     = models.CharField(max_length=20, null=True)
#     vehicle_odometer_1   = models.BigIntegerField(null=True)
#     vehicle_odometer_2   = models.BigIntegerField(null=True)
#     VIN_number   = models.CharField(max_length=50, null=True)
#     vehicle_inspection_datetime = models.DateTimeField(null=True)
#     vehicle_last_in_date    = models.DateTimeField(null=True)
#     vehicle_license_plate_nbr = models.CharField(max_length=20, null=True)
#     vehicle_license_state  = models.CharField(max_length=20, null=True)
#     vehicle_part_level     = models.CharField(max_length=20, null=True)
#     vehicle_labor_level    = models.CharField(max_length=20, null=True)
#     vechicle_used_level      = models.CharField(max_length=20, null=True)
#     vehicle_memo_01        = models.CharField(max_length=4000, null=True)
#     vehicle_memo_does_print_on_order = models.BooleanField(default=False)
#     vehicle_is_included_in_CRM_compaign = models.BooleanField(default=True)
#     vehicle_color          = models.CharField(max_length=20, null=True)
#     vehicle_record_is_activate  = models.BooleanField(default=True)
#     vehicle_class_id     = models.CharField(max_length=20, null=True)
#     vehicle_engine_hour_in   = models.DecimalField(max_digits=7, decimal_places=1, localize=True)
#     vehicle_engine_hour_out = models.DecimalField(max_digits=7, decimal_places=1, localize=True)
#     vehicle_active_recall_counts =models.IntegerField(null=True)
#     vehicle_recall_last_checked_datetime = models.DateTimeField(null=True)
#     vehicle_last_updated_datetime       = models.DateTimeField(auto_now=True, null=True)
#     vehicle_phone_id      = models.CharField(max_length=20, null=True)
#     vehicle_customer_new_uid   = models.CharField(max_length=36, null=True, primary_key=False)
#     vehicle_contact_phone_main_new_uid  = models.CharField(max_length=36, null=True, primary_key=False)
#     vehicle_created_at  = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         db_table = 'vehicles_new_01'


# class RepairOrdersNewSQL01Model:
#     repair_order_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)  # default = uuid.uuid4
#     repair_order_id = models.CharField(max_length=20, null=True)
#     repair_order_phase_id = models.CharField(max_length=20, null=True)
#     repair_order_cust_id = models.CharField(max_length=20, null=True)
#     repair_order_customer_new_uid = models.CharField(max_length=36, null=True)
#     repair_order_vehicle_id = models.CharField(max_length=20, null=True)
#     repair_order_serviced_vehicle_new_uid = models.CharField(max_length=36, null=True, primary_key=False)
#     repair_order_serviced_vehicle_location = models.CharField(max_length=36, null=True, primary_key=False)
#     repair_order_service_status = models.CharField(max_length=36, null=True)
#     repair_order_scheduled_start_datetime = models.DateTimeField(null=True)
#     repair_order_billed_hours=models.DurationField(null=True, blank=False)  # blank = False so this is a required field on form (pending testing)
#     repair_order_promise_datetime = models.DateTimeField(null=True)
#     repair_order_is_printed = models.BooleanField(default=False)
#     repair_order_invoice_is_printed = models.BooleanField(default=False)
#     repair_order_serviced_vehicle_in_datetime = models.DateTimeField(null=True)
#     repair_order_serviced_vehicle_out_datetime = models.DateTimeField(null=True)
#     repair_order_serviced_vehicle_hat = models.CharField(max_length=20, null=True)
#     repair_order_posted_datetime = models.DateTimeField(null=True)
#     repair_order_serviced_vehicle_odometer_in = models.BigIntegerField(null=True)
#     repair_order_odometer_out = models.BigIntegerField(null=True)
#     repair_order_reference_number = models.CharField(max_length=30, null=True)
#     repair_order_receipt_printed_datetime = models.DateTimeField(null=True)
#     repair_order_snapshot_is_tax_exempt = models.BooleanField(default=False)
#     repair_order_aggr_notes = models.CharField(max_length=4000, null=True)
#     repair_order_observation_text_area = models.CharField(max_length=4000, null=True)
#     repair_order_created_as_estimate = models.BooleanField(default=False)  # connecting to the estimates
#     repair_order_snapshot_margin_pct = models.DecimalField(max_digits=5, decimal_places=2, localize=True)
#     repair_order_snapshot_haz_waste_amount = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_labor_sale_amount = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_parts_sale_amount = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_supply_from_shop_amount = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_tax_haz_material_amount = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_tax_supply_from_shop_amount = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_total_tax_amount = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_balance_due_adjusted = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_discounted_amount = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_part_discounted_desc_id = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_labor_discounted_desc_id = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_order_total_amount = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_calc_haz_waste_cost = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_snapshot_calc_shop_supply_cost = models.DecimalField(max_digits=15, decimal_places=2, localize=True)
#     repair_order_serviced_vehcle_engine_hours_in = models.DecimalField(max_digits=7, decimal_places=1, localize=True)
#     repair_order_serviced_vehcle_engine_hours_out = models.DecimalField(max_digits=7, decimal_places=1, localize=True)
#     repair_order_last_updated_datetime = models.DateTimeField(null=True, auto_now=True)
#     repair_order_appointment_request_uid = models.CharField(max_length=50, null=True)
#     repair_order_created_at = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         db_table = 'repairorders_new_01'
