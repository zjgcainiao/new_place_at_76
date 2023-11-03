from django.db import models
# from computedfields.models import ComputedFieldsModel, computed, compute


# class NhtsaVariableLookup(models.Model):
#     variable_data_type: "string",
#     variable_description: "<p>This field stores any other battery information that does not belong to any of the other battery related fields.</p>",
#     variable_group_name: "Mechanical / Battery",
#       "ID": 1,
#       "Name": "Other Battery Info"


# class CustomerAPI01(models.Model):
#     customer_new_uid_v01 = models.CharField(editable=False, auto_created = True, primary_key=True, max_length=36)
#     # primary key = True
#     customer_id  = models.CharField(max_length=20, null=True)
#     customer_title_id    = models.CharField(max_length=20, null=True)
#     customer_first_name  = models.CharField(max_length=50, null=True)
#     customer_last_name   = models.CharField(max_length=50, null=True)
#     customer_middle_name = models.CharField(max_length=50, null=True)
#     customer_dob    = models.DateTimeField(null=True)
#     customer_spouse_name  = models.CharField(max_length=50, null=True)
#     customer_contact_phone_uid = models.CharField(max_length=36, null=True, primary_key=False)
#     customer_contact_email_uid = models.CharField(max_length=36, null=True, primary_key=False)
#     customer_is_okay_to_charge  = models.BooleanField(default=True)
#     customers_memo_1  = models.CharField(max_length=4000, null=True)
#     customer_is_tax_exempt = models.BooleanField(default=False)
#     customer_resale_permit_nbr = models.CharField(max_length=20, null=True)
#     customer_is_in_social_crm  = models.BooleanField(default=True)
#     customer_hear_from_us_type = models.CharField(max_length=20, null=True)
#     customer_last_visit_date   = models.DateTimeField(null=True)
#     customer_first_visit_date  = models.DateTimeField(null=True)
#     customer_is_activate       = models.BooleanField(default=True)
#     customer_memebership_nbr   = models.CharField(max_length=20, null=True)
#     customer_does_allow_SMS  = models.BooleanField(default=True)
#     customer_email_address_in_json = models.CharField(max_length=200, null=True)
#     customer_last_updated_datetime  = models.DateTimeField(null=True, auto_now=True)
#     customer_created_at   = models.DateTimeField(auto_now_add=True)
#     customer_is_created_from_appointments = models.BooleanField(default=False)
#     customer_fleet_vendor_id = models.CharField(max_length=20, null=True)
#     # custom the corresponding data table name for this model
#     class Meta:
#         db_table = 'customers_new_01'  #'AERODROMES'

# def get_absolute_url(self):
#     return reverse('customer-detail', kwargs={'pk': self.pk})

# class PhonesNewSQL01Model(models.Model):
#     phone_new_uid_v01= models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
#     phone_id = models.CharField(max_length=20, null=True)
#     phone_desc_id= models.CharField(max_length=20, null=True)
#     phone_number= models.CharField(max_length=20, null=True)
#     phone_number_ext= models.CharField(max_length=20, null=True)
#     phone_displayed_name= models.CharField(max_length=20, null=True)
#     phone_memo_01 = models.CharField(max_length=100, null=True)
#     phone_created_at = models.DateTimeField(null=True,add_now_add=True)
#     phone_last_updated_date = models.DateTimeField(null=True,auto_now=True)
#     # custom the corresponding data table name for this model
#     class Meta:
#         db_table = 'phones_news_01'  #'AERODROMES'


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
