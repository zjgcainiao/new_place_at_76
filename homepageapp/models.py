from django.db import models
from django.urls import reverse
# from computedfields.models import ComputedFieldsModel, computed, compute
from django.db.models import Count
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# added on 2022-10-29 so the load_env
import os
from dotenv import load_dotenv

# documentation for py-mssql is https://pymssql.readthedocs.io/en/stable/pymssql_examples.html#basic-features-strict-db-api-compliance
# import pymssql

# ---------------------------------------  2023-03-29 stop using the new uid -------------------
# uid takes too much space and storage.
# revert back to the existing old id, such as customer_id, vehicle_id, repair_order_id, phone_id.
# add majority of data tables for testing
class CategoryModel(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_description = models.CharField(max_length=200, blank=True)
    category_display = models.IntegerField(blank=True, null=True)
    category_created_at = models.DateTimeField(auto_now_add=True)
    category_last_updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'categories_new_03'
        ordering = ['-category_id']

class AccountClassModel(models.Model):
    account_class_id = models.AutoField(primary_key=True)
    account_type = models.CharField(max_length=30, null=True)
    account_last_updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'accountclasses_new_03'
        ordering = ["-account_class_id"]
        verbose_name = 'accountclass'
        verbose_name_plural = 'accountclasses'

class InvoiceStatusModel(models.Model):
    invoice_status_id = models.AutoField(primary_key=True)
    invoice_status_description = models.CharField(max_length=30, null=True)
    invoice_status_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'invoicestatuess_new_03'
        ordering = ["invoice_status_id"]
        verbose_name = 'invoicestatus'
        verbose_name_plural = 'invoicestatuses'

class AddressesNewSQL02Model(models.Model):
    address_id = models.AutoField(primary_key=True)
    address_type_id = models.IntegerField()
    address_company_or_ATTN = models.CharField(max_length=50,blank=True)
    address_line_01 = models.CharField(max_length=80, blank=True)
    address_city = models.CharField(max_length=50,  blank=True)
    address_state = models.CharField(max_length=50, blank=True)
    address_zip_code = models.CharField(max_length=30, blank=True)
    address_created_at = models.DateTimeField(auto_now_add=True)
    address_last_updated_date = models.DateTimeField(auto_now=True, null=True)

    @property
    def get_full_address(self):
        addr_fields = [self.address_line_01, self.address_city, self.address_state.upper(),
                       self.address_zip_code]

        full_address = " ".join([field for field in addr_fields if field is not None]).strip()

        return full_address

    @property
    def get_full_address_with_ATTN(self):
        addr_fields = [self.address_company_or_ATTN, self.address_line_01, self.address_city, self.address_state.upper(),
                       self.address_zip_code]

        full_address = " ".join([field for field in addr_fields if field is not None]).strip()

        return full_address


    class Meta:
        db_table = 'addresses_new_03'
        ordering = ["-address_id"]
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

class EmailsNewSQL02Model(models.Model):
    email_id = models.IntegerField(primary_key=True)
    email_type_id = models.IntegerField()
    email_address = models.EmailField()
    email_description = models.CharField(max_length=255)
    # record_version = models.IntegerField()
    email_created_at = models.DateTimeField(auto_now_add=True)
    email_last_updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'emails_new_03'
        ordering = ["-email_id"]
        # verbose_name = 'email'
        # verbose_name_plural = 'emails'

class PhoneDescModel(models.Model):
    phone_desc_id = models.IntegerField(primary_key=True)
    phone_desc = models.CharField(max_length=50, null=True)
    phone_order = models.IntegerField()
    phone_desc_default_type = models.CharField(max_length=5, null=True)
    phone_desc_created_at = models.DateTimeField(auto_now_add=True)
    phone_desc_last_updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'phonedescs_new_03' 
        ordering = ["-phone_desc_id"]
        verbose_name='phonedesc'
        verbose_name_plural='phonedescs'


class PhonesNewSQL02Model(models.Model):
    phone_id = models.AutoField(primary_key=True)
    phone_desc = models.ForeignKey(PhoneDescModel, on_delete=models.SET_NULL, null=True,related_name='phone_descs')
    phone_number = models.CharField(max_length=20)
    phone_number_digits_only = models.CharField(max_length=20, null=True, blank=True)
    phone_number_ext = models.CharField(max_length=10, blank=True, null=True)
    phone_displayed_name = models.CharField(max_length=100)
    phone_memo_01 = models.TextField(blank=True, null=True)
    phone_created_at = models.DateTimeField(auto_now_add=True)
    phone_last_updated_date = models.DateTimeField(auto_now=True)
    # custom the corresponding data table name for this model
    class Meta:
        db_table = 'phones_new_03' 
        ordering = ["-phone_id"]
        verbose_name='phone'
        verbose_name_plural='phones'



class TaxesModel(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_description = models.CharField(max_length=30, null=True)
    tax_applied_gl_code = models.IntegerField()
    tax_item_created_at = models.DateTimeField(auto_now_add=True)
    tax_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'taxes_new_03' 
        ordering = ["-tax_id"]
        verbose_name = 'tax'
        verbose_name_plural='taxes'

class CustomersNewSQL02Model(models.Model):
    # customer_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
    # primary key = True
    customer_id = models.AutoField(primary_key=True)
    customer_title_id = models.CharField(max_length=20, null=True)
    customer_first_name = models.CharField(max_length=50, null=True)
    customer_last_name = models.CharField(max_length=50, null=True)
    customer_middle_name = models.CharField(max_length=50, null=True, blank=True)
    customer_dob = models.DateTimeField(null=True, blank=True)
    customer_spouse_name = models.CharField(max_length=50, null=True)
    # customer_primary_phone_uid = models.CharField(max_length=36, null=True)
    # customer_primary_email_uid = models.CharField(max_length=36, null=True)
    customer_is_okay_to_charge = models.BooleanField(default=True)
    customer_memo_1 = models.CharField(max_length=4000, null=True)
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
    customer_fleet_vendor_id = models.CharField(max_length=100, null=True)
    customer_created_at = models.DateTimeField(auto_now_add=True)
    # add a new many-to-many-relationship field
    addresses = models.ManyToManyField(AddressesNewSQL02Model, through='CustomerAddressesNewSQL02Model',related_name='addresses')
    # add a new many-to-many-relationship field for emails
    emails = models.ManyToManyField(EmailsNewSQL02Model, through='CustomerEmailsNewSQL02Model',related_name='emails')
    # many to many field to phones
    phones = models.ManyToManyField(PhonesNewSQL02Model, through='CustomerPhonesNewSQL02Model',related_name='phones')
    # many to many fields to Taxes
    taxes = models.ManyToManyField(TaxesModel, through='CustomerTaxesModel', related_name='taxes')

    @property
    def customer_full_name(self):
        first_name = self.customer_first_name.capitalize()  if self.customer_first_name else None
        middle_name = self.customer_middle_name.capitalize() if self.customer_middle_name else None
        last_name = self.customer_last_name.capitalize() if self.customer_last_name else None
        name_fields = [first_name, middle_name, last_name]
        full_name = ' '.join([field for field in name_fields if field is not None])
        return f"{full_name}" if full_name.strip() else "No Data"


    class Meta:
        db_table = 'customers_new_03'   # prolube76DBSTG01.dbo.customers_new_01
        ordering = ["-customer_id"]
        verbose_name = 'customer'
        verbose_name_plural = 'customers'




class CustomerAddressesNewSQL02Model(models.Model):
    address = models.ForeignKey(AddressesNewSQL02Model, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.CASCADE)
    customeraddress_address_created_at = models.DateTimeField(auto_now_add=True)
    customeraddress_last_updated_date = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = 'customeraddresses_new_03' 
        ordering = ["-address", '-customer']
        # verbose_name = 'customeraddress'
        # verbose_name_plural = 'customeraddresses'

class CustomerEmailsNewSQL02Model(models.Model):
    customeremail_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.CASCADE)
    email = models.ForeignKey(EmailsNewSQL02Model, on_delete=models.CASCADE)
    customeremail_is_selected = models.BooleanField(default=True)
    customeremail_created_at = models.DateTimeField(auto_now_add=True)
    customeremail_last_updated_date = models.DateTimeField(auto_now=True)

   
    class Meta:
        db_table = 'customeremails_new_03' 
        ordering = ["-customeremail_id", '-email']
        # verbose_name = 'customeremail'
        # verbose_name_plural = 'customeremails'

class CustomerPhonesNewSQL02Model(models.Model):
    phone = models.ForeignKey(PhonesNewSQL02Model, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.CASCADE)
    customerphone_created_at = models.DateTimeField(auto_now_add=True)
    customerphone_last_updated_date = models.DateTimeField(auto_now=True)

   
    class Meta:
        db_table = 'customerphones_new_03' 
        ordering = ["-customer", '-phone']
        # verbose_name = 'customeremail'
        # verbose_name_plural = 'customeremails'


# ---- 2023-04-03 repairorderphase model is added ----
class RepairOrderPhasesNewSQL02Model(models.Model):
    repair_order_phase_id = models.AutoField(primary_key=True)
    repair_order_phase_description = models.CharField(max_length=50)
    repair_order_phase_created_at = models.DateTimeField(auto_now_add=True)
    repair_order_phase_last_updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'repairorderphases_new_03'
        ordering = ["repair_order_phase_id"]
        verbose_name = 'repairorderphase'
        verbose_name_plural = 'repairorderphases'



class MakesNewSQL02Model(models.Model):
    make_id = models.AutoField(primary_key=True)
    make_name = models.CharField(max_length=30, null=True)
    make_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'makes_new_03'
        ordering = ["-make_id"]
        verbose_name = 'make'
        verbose_name_plural = 'makes'

class ModelsNewSQL02Model(models.Model):
    model_id = models.AutoField(primary_key=True)
    make = models.ForeignKey(MakesNewSQL02Model, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=30, null=True)
    model_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'models_new_03'
        ordering = ["-model_id", 'make']
        verbose_name = 'model'
        verbose_name_plural = 'models'

class EnginesModel(models.Model):
    engine_id = models.AutoField(primary_key=True)
    engine_displacement_CID = models.DecimalField(max_digits=10,decimal_places=1, null=True)
    engine_displacement_liter = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    engine_number_of_cylinder = models.IntegerField(null=True)
    engine_valve_per_cyclinder = models.IntegerField(null=True)
    engine_head_configuration_type = models.CharField(max_length=100,blank=True, null=True)
    engine_boost_type = models.CharField(max_length=100,blank=True, null=True)
    engine_ignition_system = models.CharField(max_length=100,blank=True, null=True)
    engine_vin_code = models.CharField(max_length=20,blank=True, null=True)
    engine_fuel_system = models.CharField(max_length=100,blank=True, null=True)
    engine_fuel_delivery_method_type = models.CharField(max_length=100,blank=True, null=True)
    engine_fuel_type = models.CharField(max_length=100,blank=True, null=True)
    engine_fuel_control_type = models.CharField(max_length=100,blank=True, null=True)
    engine_block_configuration = models.CharField(max_length=100,blank=True, null=True)
    engine_fuel_system_configuration = models.CharField(max_length=100,blank=True, null=True)
    engine_created_at = models.DateTimeField(auto_now_add=True)
    engine_last_updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'engines_new_03'
        ordering = ["-engine_id"]
        verbose_name = 'engine'
        verbose_name_plural = 'engines'

class TransmissionsModel(models.Model):
    transmission_id = models.AutoField(primary_key=True)
    transmission_type = models.CharField(max_length=100,blank=True, null=True)
    tranmission_manufacturer_code = models.CharField(max_length=100,blank=True, null=True)
    transmission_control_type = models.CharField(max_length=100,blank=True, null=True)
    tranmission_is_electronic_controlled = models.BooleanField(default=False)
    transmission_number_of_speed = models.IntegerField(null=True)
    transmission_created_at  = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'transmissions_new_03'
        ordering = ["-transmission_id"]
        verbose_name = 'transmission'
        verbose_name_plural = 'transmissions'

class BrakesModel(models.Model):
    brake_id = models.AutoField(primary_key=True)
    brake_system_type = models.CharField(max_length=150, null=True)
    brake_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'brakes_new_03'
        ordering = ["-brake_id"]
        verbose_name = 'brake'
        verbose_name_plural = 'brakes'

class GVWsModel(models.Model):
    gvw_id = models.AutoField(primary_key=True)
    gvw_text = models.CharField(max_length=150, null=True)
    gvw_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'gvws_new_03'
        ordering = ["-gvw_id"]
        verbose_name = 'gvw'
        verbose_name_plural = 'gvws'

class SubmodelsModel(models.Model):
    submodel_id = models.AutoField(primary_key=True)
    submodel_model = models.ForeignKey(ModelsNewSQL02Model, on_delete=models.CASCADE)
    submodel_name = models.CharField(max_length=150, null=True)
    submodel_DMV_id = models.IntegerField(null=True)
    submodel_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'submodels_new_03'
        ordering = ["-submodel_id"]
        verbose_name = 'submodel'
        verbose_name_plural = 'submodels'

class DrivesModel(models.Model):
    drive_id = models.AutoField(primary_key=True)
    drive_type = models.CharField(max_length=150, null=True)
    drive_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'drives_new_03'
        ordering = ["-drive_id"]
        verbose_name = 'drive'
        verbose_name_plural = 'drives'

class BodyStylesModel(models.Model):
    body_style_id = models.AutoField(primary_key=True)
    body_style_name = models.CharField(max_length=150, null=True)
    body_style_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'bodystyles_new_03'
        ordering = ["-body_style_id"]
        verbose_name = 'bodystyle'
        verbose_name_plural = 'bodystyles'
    
class MyShopVehicleConfigsModel(models.Model):
    myshop_vehicle_config_id = models.AutoField(primary_key=True)
    myshop_year_id = models.IntegerField(null=True)
    myshop_make = models.ForeignKey(MakesNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='myshop_makes')
    myshop_model = models.ForeignKey(ModelsNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='myshop_models')
    myshop_submodel = models.ForeignKey(SubmodelsModel, on_delete=models.SET_NULL, null=True, related_name='myshop_submodels')
    myshop_bodystyle = models.ForeignKey(BodyStylesModel, on_delete=models.SET_NULL, null=True, related_name='myshop_bodystyles')
    myshop_engine  = models.ForeignKey(EnginesModel, on_delete=models.SET_NULL, null=True, related_name='myshop_engines')
    myshop_brake = models.ForeignKey(BrakesModel, on_delete=models.SET_NULL, null=True, related_name='myshop_brakes')
    myshop_transmission  = models.ForeignKey(TransmissionsModel, on_delete=models.SET_NULL, null=True, related_name='myshop_transmissions')
    myshop_GVW = models.ForeignKey(GVWsModel, on_delete=models.SET_NULL, null=True, related_name='myshop_gvws')
    myshop_drive = models.ForeignKey(DrivesModel, on_delete=models.SET_NULL, null=True, name='myshop_drives')
    myshop_vehicle_config_created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'myshopvehicleconfigs_new_03'
        ordering = ["-myshop_vehicle_config_id"]
        verbose_name = 'myshopvehicleconfig'
        verbose_name_plural = 'myshopvehicleconfigs'

class VehicleConfigMyShopConfigsModel(models.Model):
   vehicle_config_id = models.AutoField(primary_key=True)
   myshop_vehicle_config = models.ForeignKey(MyShopVehicleConfigsModel,
                            on_delete=models.SET_NULL, null=True, related_name='vehicleconfigmyshopconfigs')
   vehicle_config_myshop_config_created_at = models.DateTimeField(auto_now_add=True, null=True)
   class Meta:
        db_table = 'vehicleconfigmyshopconfigs_new_03'
        ordering = ["-vehicle_config_id"]
        verbose_name = 'vehicleconfigmyshopconfig'
        verbose_name_plural = 'vehicleconfigmyshopconfigs'


class VehiclesNewSQL02Model(models.Model):
    # vehicle_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)  # default = uuid.uuid4
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_cust = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='vehicle_customers')
    vehicle_year = models.CharField(max_length=20, null=True)
    vehicle_make = models.ForeignKey(MakesNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='vehicle_makes')
    vehicle_sub_model = models.ForeignKey(SubmodelsModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_submodels')
    vehicle_body_style = models.ForeignKey(BodyStylesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_bodystyles')
    vehicle_engine = models.ForeignKey(EnginesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_engines')
    vehicle_transmission = models.ForeignKey(TransmissionsModel, on_delete=models.SET_NULL, null=True, related_name ='vehicle_transmissions')
    vehicle_brake = models.ForeignKey(BrakesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_brakes')
    vehicle_drive_type = models.ForeignKey(DrivesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_drives')
    vehicle_GVW = models.ForeignKey(GVWsModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_gvws')
    vehicle_odometer_1 = models.BigIntegerField(null=True)
    vehicle_odometer_2 = models.BigIntegerField(null=True)
    VIN_number = models.CharField(max_length=50, null=True)
    vehicle_inspection_datetime = models.DateTimeField(null=True)
    vehicle_last_in_date = models.DateTimeField(null=True)
    vehicle_license_plate_nbr = models.CharField(max_length=20, null=True)
    vehicle_license_state = models.CharField(max_length=20, null=True)
    vehicle_part_level = models.CharField(max_length=20, null=True)
    vehicle_labor_level = models.CharField(max_length=20, null=True)
    vehicle_used_level = models.CharField(max_length=20, null=True)
    vehicle_memo_01 = models.CharField(max_length=4000, null=True)
    vehicle_memo_does_print_on_order = models.BooleanField(default=False)
    vehicle_is_included_in_CRM_compaign = models.BooleanField(default=True)
    vehicle_color = models.CharField(max_length=20, null=True)
    vehicle_record_is_activate = models.BooleanField(default=True)
    vehicle_class_id = models.CharField(max_length=20, null=True)
    vehicle_engine_hour_in = models.DecimalField(max_digits=7, decimal_places=1)
    vehicle_engine_hour_out = models.DecimalField(max_digits=7, decimal_places=1)
    vehicle_active_recall_counts = models.IntegerField(null=True)
    vehicle_recall_last_checked_datetime = models.DateTimeField(null=True)
    vehicle_phone = models.ForeignKey(PhonesNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='vehicle_phones')
    vehicle_contact_phone_main_new_uid  = models.CharField(max_length=36, null=True) 
    vehicle_created_at  = models.DateTimeField(auto_now_add=True)
    vehicle_last_updated_datetime = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'vehicles_new_03'
        ordering = ["-vehicle_id"]
        verbose_name = 'vehicle'
        verbose_name_plural = 'vehicles'


class TextMessagesModel(models.Model):
    text_message_id = models.AutoField(primary_key=True)
    text_customer = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='text_customers')
    text_body = models.CharField(max_length=4000, blank=True, null=True)
    text_external_id = models.BigIntegerField(null=True)
    text_type = models.IntegerField()
    text_to_phonenumber = models.CharField(max_length=15)
    text_direction = models.BooleanField(default=False)
    text_status = models.IntegerField()
    text_error_message = models.CharField(max_length=255, null=True)
    text_error_code = models.CharField(max_length=255, null=True)
    text_datetime = models.DateTimeField()
    text_body_size = models.IntegerField()
    text_created_at = models.DateTimeField(auto_now_add=True, null=True)
    text_last_updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'textmessages_new_03'
        ordering = ['-text_message_id']
        verbose_name = 'textmessage'
        verbose_name_plural = 'textmessages'

class CannedJobsNewSQL02Model(models.Model):
    canned_job_id = models.AutoField(primary_key=True)
    canned_job_title = models.CharField(max_length=50, null=True)
    canned_job_description = models.CharField(max_length=200, null=True)
    canned_job_is_in_quick_menu = models.BooleanField(default=False)
    canned_job_category_id = models.IntegerField(blank=True, null=True)
    canned_job_applied_year = models.IntegerField(blank=True, null=True)
    canned_job_applied_make_id = models.IntegerField(blank=True, null=True)
    canned_job_applied_submodel_id = models.IntegerField(blank=True, null=True)
    canned_job_vehicle_class = models.CharField(max_length=50, null=True)
    canned_job_last_updated_date = models.DateTimeField(auto_now=True, null=True)
    canned_job_created_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'cannedjobs_new_03'
        ordering = ["-canned_job_id"]

class LineItemsNewSQL02Model(models.Model):
    line_item_id = models.AutoField(primary_key=True)
    line_item_account_class = models.ForeignKey(AccountClassModel, on_delete=models.SET_NULL, null=True,related_name='lineitem_accountclasses')
    line_item_category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True)
    line_item_description = models.CharField(max_length=2000)
    line_item_cost = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_sale = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_is_tax_exempt = models.BooleanField(default=False)
    line_item_has_no_commission = models.BooleanField(default=True)
    line_item_has_fixed_commission = models.BooleanField(default=False)
    line_item_order_revision_id = models.IntegerField(null=True)
    # line_item_order_revision_id = models.ForeignKey(OrderRevisionNewSQL02Model, models.SET_NULL, blank=True, null=True)
    # any foreignKey field will add '_id' automatically when creating a sql data table. In the sql 
    line_item_canned_job = models.ForeignKey(CannedJobsNewSQL02Model, models.SET_NULL, blank=True, null=True)
    line_item_labor_sale = models.DecimalField(max_digits=12, decimal_places=2)
    line_item_part_sale = models.DecimalField(max_digits=12, decimal_places=2)
    line_item_part_only_sale = models.DecimalField(max_digits=12, decimal_places=2)
    line_item_labor_only_sale = models.DecimalField(max_digits=12, decimal_places=2)
    line_item_sublet_sale = models.DecimalField(max_digits=12, decimal_places=2)
    line_item_package_sale = models.DecimalField(max_digits=12,decimal_places=2)
    line_item_tire_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    line_item_parent_line_item_id = models.IntegerField(null=True)
    line_item_created_at = models.DateTimeField(auto_now_add=True)
    line_item_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'lineitems_new_03' 
        ordering = ["-line_item_id"]


class NoteItemsNewSQL02Model(models.Model):
    note_item_id = models.AutoField(primary_key=True)
    line_item = models.ForeignKey(LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='lineitem_noteitem') # when it is a foreign key,"_id" is added at the end of the field name 
    note_item_text = models.TextField(null=True)
    note_item_is_printed_on_order = models.BooleanField(default=True)
    note_item_tech_observation = models.TextField(null=True)
    note_item_created_at = models.DateTimeField(auto_now_add=True)
    note_item_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'noteitems_new_03'
        ordering = ["-note_item_id"]
        verbose_name = 'noteitem'
        verbose_name_plural = 'noteitems'

class CustomerTaxesModel(models.Model):
    tax_id = models.ForeignKey(TaxesModel, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.CASCADE)
    customertaxes_last_updated_date = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'customertaxes_new_03' 
        ordering = ["-tax_id",'-customer_id']
        verbose_name = 'customertax'
        verbose_name_plural='customertaxes'

class lineItemTaxesNewSQL02Model(models.Model):
    line_item_id = models.ForeignKey(LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='taxes')
    line_item_tax_id = models.IntegerField(null=True)
    line_item_tax_charged = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_tax_rate = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_tax_created_at = models.DateTimeField(auto_now_add=True)
    line_item_tax_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'lineitemtaxes_new_03' 
        ordering = ["-line_item_id"]

class LaborItemModel(models.Model):
    labor_item_id = models.AutoField(primary_key=True)
    line_item = models.ForeignKey(LineItemsNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='lineitem_laboritem')
    labor_rate_description_id = models.IntegerField()
    labor_item_is_user_entered_labor_rate = models.BooleanField()
    labor_item_work_performed = models.TextField( blank=True, null=True)
    labor_item_hours_charged = models.DecimalField(max_digits=10, decimal_places=2)
    labor_item_symptom = models.CharField(max_length=4000, null=True)
    labor_item_is_come_back_invoice = models.BooleanField(default=False, null=True)
    labor_item_parts_estimate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    labor_item_is_MPlg_item = models.IntegerField(default=False)
    labor_item_is_Changed_MPlg_item = models.BooleanField(default=False)
    labor_item_created_at = models.DateTimeField(auto_now_add=True)
    labor_item_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'laboritems_new_03' 
        ordering = ["-labor_item_id"]


class PartsModel(models.Model):
    part_id = models.AutoField(primary_key=True)
    part_description = models.CharField(max_length=500, null=True, blank=True)
    part_cost = models.DecimalField(max_digits=12, decimal_places=2)
    part_price = models.DecimalField(max_digits=12, decimal_places=2)
    part_is_tax_exempt = models.BooleanField(default=False)
    part_category_id = models.IntegerField(null=True)
    part_account_class = models.ForeignKey(AccountClassModel, on_delete=models.SET_NULL, null=True,related_name='parts_accountclasses')
    part_comments = models.CharField(max_length=4000, null=True, blank=True)
    part_manufacturer_id = models.IntegerField(null=True)
    part_list_price = models.DecimalField(max_digits=12, decimal_places=2)
    part_is_user_entered_price = models.DecimalField(max_digits=12, decimal_places=2)
    part_kit_id = models.IntegerField(null=True)
    part_is_MPLG_item = models.BooleanField(default=False)
    part_is_changed_MPLG_item = models.BooleanField(default=False)
    part_is_core = models.BooleanField(default=False)
    part_core_cost = models.DecimalField(max_digits=12, decimal_places=2)
    part_core_list_price = models.DecimalField(max_digits=12, decimal_places=2)
    part_fee_id = models.IntegerField(null=True)
    part_is_deleted = models.BooleanField(default=False)
    part_size = models.CharField(max_length=20, null=True, blank=True)
    part_is_tire = models.BooleanField(default=False)
    part_created_at = models.DateTimeField(auto_now_add=True)
    part_last_updated_date = models.DateTimeField(auto_now=True, null=True,)
    class Meta:
        db_table = 'parts_new_03'
        ordering = ["-part_id"]

class PartItemModel(models.Model):
    part_item_id = models.AutoField(primary_key=True)
    line_item = models.ForeignKey(LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='parts_lineitems')
    part_discount_description_id = models.IntegerField(null=True)
    part_item_is_user_entered_unit_sale = models.BooleanField(default=False)
    part_item_is_user_entered_unit_cost = models.BooleanField(default=False)
    part_item_quantity = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    part_item_unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    part_item_unit_list = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    part_item_unit_sale = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    part_item_unit_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    part_item_part_no = models.CharField(max_length=100, null=True, blank=True)
    part_item_part = models.ForeignKey(PartsModel, on_delete=models.SET_NULL, null=True, related_name='parts_parts')
    part_item_is_confirmed = models.BooleanField(default=False)
    part_item_vendor_code = models.CharField(max_length=25, null=True, blank=True)
    part_item_vendor_id = models.IntegerField(null=True)
    part_item_manufacture_id = models.IntegerField(null=True)
    part_item_invoice_number = models.CharField(max_length=50, null=True, blank=True)
    part_item_commission_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    part_item_is_committed = models.BooleanField(default=False)
    part_item_is_quantity_confirmed = models.BooleanField(default=False)
    part_item_confirmed_quantity = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    part_item_is_part_ordered = models.BooleanField(default=False)
    part_item_is_core = models.BooleanField(default=False)
    part_item_is_bundled_kit = models.BooleanField(default=False)
    part_item_is_MPlg_item = models.BooleanField(default=False)
    part_item_is_changed_MPlg_item = models.BooleanField(default=False)
    part_item_part_type = models.CharField(max_length=10, null=True, blank=True)
    part_item_size = models.CharField(max_length=20, null=True, blank =True)
    part_item_is_tire = models.BooleanField(default=False)
    part_item_vendor_id = models.IntegerField(null=True)
    part_item_meta = models.CharField(max_length=4000, null=True, blank =True)
    part_item_added_from_supplier = models.CharField(max_length=50, null=True, blank =True)
    part_item_purchased_from_vendor = models.CharField(max_length=50, null=True, blank =True)
    part_item_purchased_from_supplier = models.CharField(max_length=50, null=True, blank =True)
    part_item_shipping_description = models.CharField(max_length=50, null=True, blank =True)
    part_item_shipping_cost = models.CharField(max_length=50, null=True, blank =True)
    part_item_last_updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'partitems_new_03'
        ordering = ["-part_item_id"]
        verbose_name = 'partitem'
        verbose_name_plural = 'partitems'

# class AppointmentModel(models.Model):
#     service_appointment_request_uid = models.BigAutoField(primary_key=True)
#     service_appointment_requested_datetime = models.DateTimeField(blank=True)
#     service_appointment_type = models.IntegerField()
#     service_appointment_first_name = models.CharField(max_length=60,blank=True, null=True)
#     service_appointment_last_name  = models.CharField(max_length=60,blank=True, null=True)
#     service_appointment_middle_name = models.CharField(max_length=60,blank=True, null=True)
#     service_appointment_contact_phone_main = models.CharField(max_length=60,blank=True, null=True)
#     service_appointment_contact_email_address = models.EmailField(blank=True)
#     service_appointment_preferred_contact_method = models.CharField(max_length=100, blank=True)

#     service_appointment_shop_comments = models.TextField(blank=True)
#     service_appointment_customer_id = models.IntegerField(blank=True)
#     service_appointment_vehicle_id = models.IntegerField(blank=True)
#     service_appointment_customer_details = models.CharField(max_length=2000, blank=True, null=True)
#     service_appointment_vehicle_details = models.CharField(max_length=2000, blank=True, null=True)
#     service_appointment_fleet_details = models.CharField(max_length=2000, blank=True, null=True)
#     service_appointment_waiting_options = models.CharField(max_length=100,blank=True)
#     service_appointment_sub_categories = models.CharField(max_length=300, blank=True)
#     service_appointment_status = models.IntegerField() # should be disabled
#     service_appointment_customer_comments = models.TextField()
#     service_appointment_final_estimated_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

#     service_appointment_confirmed_UTC_datetime = models.DateTimeField(blank=True)
#     service_appointment_submitted_UTC_datetime = models.DateTimeField(blank=True)
#     service_appointment_confirmed_by_employee_id = models.IntegerField(blank=True)
#     service_appointment_repair_order_id = models.IntegerField(blank=True)
#     service_appointment_is_converted_to_repair_order = models.BooleanField(default=False)
#     service_appointment_is_inactive = models.BooleanField(default=False, null=True)
#     service_appointment_created_at = models.DateTimeField(auto_now_add=True)
#     service_appointment_last_udpated_date = models.DateTimeField(null=True, auto_now=True)
#     class Meta:
#         db_table = 'appointmentrequests_new_03' 
#         ordering = ["-service_appointment_request_uid"]

class RepairOrdersNewSQL02Model(models.Model):
    # repair_order_new_uid_v01 = models.UUIDField(primary_key=True)  # models.UUIDField(primary_key=True)  # models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
    repair_order_id = models.AutoField(primary_key=True)
    repair_order_phase = models.ForeignKey(RepairOrderPhasesNewSQL02Model, on_delete=models.SET_NULL, blank=True, null=True)
    # remove the `_id` from the field name. due to recent adding a foreign key.. by adding a foreign key field, Django will add '_id' for the field in the SQL data table.
    repair_order_customer = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True) 
    # repair_order_customer_new_uid = models.CharField(max_length=20, null=True)
    # models.ForeignKey(CustomersNewSQL01Model, on_delete=models.CASCADE, null=True,db_column='customer_new_uid_v01')
    repair_order_vehicle = models.ForeignKey(VehiclesNewSQL02Model, on_delete=models.SET_NULL,null=True)
    # repair_order_serviced_vehicle_new_uid = models.CharField(max_length=36, null=True, primary_key=False) 
    repair_order_serviced_vehicle_location = models.CharField(max_length=36, null=True) 
    repair_order_service_status = models.CharField(max_length=36, null=True) 
    repair_order_scheduled_start_datetime = models.DateTimeField(null=True)
    repair_order_billed_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)  # blank = False so this is a required field on form (pending testing)
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
    repair_order_snapshot_margin_pct = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    repair_order_snapshot_haz_waste_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_labor_sale_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_parts_sale_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_supply_from_shop_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_tax_haz_material_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_tax_supply_from_shop_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_total_tax_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_balance_due_adjusted = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_discounted_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_part_discounted_desc_id = models.IntegerField(null=True, blank=True)
    repair_order_snapshot_labor_discounted_desc_id = models.IntegerField(null=True, blank=True)
    repair_order_snapshot_order_total_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_calc_haz_waste_cost = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    repair_order_snapshot_calc_shop_supply_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    repair_order_serviced_vehicle_engine_hours_in = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    repair_order_serviced_vehicle_engine_hours_out = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    repair_order_appointment_request_uid = models.CharField(max_length=50, null=True)
    repair_order_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    repair_order_created_at = models.DateTimeField(auto_now_add=True)

    # added many-to-many relationship fields managers.
    lineitems = models.ManyToManyField(LineItemsNewSQL02Model, through='RepairOrderLineItemSquencesNewSQL02Model',
                related_name='lineitems')
    class Meta:
        db_table = 'repairorders_new_03'
        ordering = ["-repair_order_id"]
        verbose_name = 'repairorder'
        verbose_name_plural = 'repairorders'

    def get_absolute_url(self):
        return reverse('dashboard-detail', kwargs={'pk': self.pk})

class OrderRevisionNewSQL02Model(models.Model):
    order_revision_id = models.AutoField(primary_key=True)
    order_revision_repair_order = models.ForeignKey(RepairOrdersNewSQL02Model, models.SET_NULL, blank=True, null=True, related_name='orderrevisions')
    order_revision_sub_estimate_number = models.IntegerField(blank=True, null=True)
    order_revision_date = models.DateTimeField(null=True)
    time_of_call = models.DateTimeField(null=True)
    order_revision_initiated_by = models.CharField(max_length=20, null=True)
    order_revision_by_service_writer_id = models.IntegerField(null=True)
    order_revision_authorizaton_by_name = models.CharField(max_length=50, null=True, blank=True)
    order_revision_number_called = models.CharField(max_length=50, null=True)
    order_revision_reason = models.CharField(max_length=200, null=True)
    order_revision_current_estimate = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_revision_amount = models.DecimalField(max_digits=15, decimal_places=2)
    order_revision_vehicle_id = models.ForeignKey(VehiclesNewSQL02Model, models.SET_NULL, blank=True, null=True)
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
        db_table = 'orderrevisions_new_03'
        ordering = ["-order_revision_id"]


class RepairOrderLineItemSquencesNewSQL02Model(models.Model):
    ro_line_item_sequence_id = models.AutoField(primary_key=True)
    repair_order = models.ForeignKey(RepairOrdersNewSQL02Model, models.CASCADE, blank=True, null=True)
    line_item = models.ForeignKey(LineItemsNewSQL02Model, models.CASCADE, blank=True, null=True)
    sequence = models.IntegerField(null=True)
    ro_line_item_sequence_created_at = models.DateTimeField(auto_now_add=True)
    ro_line_item_sequence_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'repairorderlineitemsequences_new_03'
        ordering = ["-ro_line_item_sequence_id", 'repair_order', 'line_item']
 
class PaymentTransactionsModel(models.Model):
    payment_transaction_id = models.AutoField(primary_key=True)
    payment_last_updated_date = models.DateTimeField(null=True, auto_now=True)
    class Meta:
        db_table = 'paymenttransactions_new_03'
        ordering = ["-payment_transaction_id",]

class PaymentsModel(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_repair_order = models.ForeignKey(RepairOrdersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='payment_repairorders')
    payment_record_number = models.IntegerField(null=True)
    payment_customer = models.ForeignKey(CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='payment_customers')
    payment_date = models.DateTimeField(null=True)
    payment_check_data = models.CharField(max_length=100, null=True, blank=True)
    payment_auth_data = models.CharField(max_length=100, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_invoice_status = models.ForeignKey(InvoiceStatusModel,on_delete=models.SET_NULL, null=True, related_name='payment_invoicestatuses')
    payment_is_NSF = models.BooleanField(default=False)
    payment_is_NSF_reversal = models.BooleanField(default=False)
    payment_is_fee_payment = models.BooleanField(default=False)
    payment_total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    payment_deletion_date = models.DateTimeField(null=True)
    payment_transcation = models.ForeignKey(PaymentTransactionsModel, on_delete=models.SET_NULL, null=True,related_name='payment_transactions')
    payment_account_class = models.ForeignKey(AccountClassModel, on_delete=models.SET_NULL, null=True,related_name='payment_accountclasses')
    payment_verification_data = models.CharField(max_length=200, null=True, blank=True)
    payment_receipt_one = models.CharField(max_length=200, null=True, blank=True)
    payment_receipt_two = models.CharField(max_length=200, null=True, blank=True)
    payment_receipt_three = models.CharField(max_length=200, null=True, blank=True)
    payment_last_updated_date = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        db_table = 'payments_new_03'
        ordering = ["-payment_id",]
        verbose_name = 'payment'
        verbose_name_plural = 'payments'

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
