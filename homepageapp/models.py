from django.db import models
from django.urls import reverse
# from computedfields.models import ComputedFieldsModel, computed, compute
from django.db.models import Count
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# added on 2022-10-29 so the load_env
import os
from dotenv import load_dotenv
from internal_users.models import InternalUser
import re
from apis.api_vendor_urls import NHTSA_API_URL
from core_operations.models import FormattedPhoneNumberField
# documentation for py-mssql is https://pymssql.readthedocs.io/en/stable/pymssql_examples.html#basic-features-strict-db-api-compliance
# import pymssql

# ---------------------------------------  2023-03-29 stop using the new uid -------------------
# uid takes too much space and storage.
# revert back to the existing old id, such as customer_id, vehicle_id, repair_order_id, phone_id.
# add majority of data tables for testing


class AddressesNewSQL02Model(models.Model):
    address_id = models.AutoField(primary_key=True)
    address_type_id = models.IntegerField()
    address_company_or_ATTN = models.CharField(
        max_length=50, null=True, blank=True)
    address_line_01 = models.CharField(max_length=80, null=True, blank=True)
    address_city = models.CharField(max_length=50,  null=True, blank=True)
    address_state = models.CharField(max_length=50, null=True, blank=True)
    address_zip_code = models.CharField(max_length=30, null=True, blank=True)
    address_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='address_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='address_modified', on_delete=models.SET_NULL, null=True, blank=True)
    address_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def get_full_address(self):
        addr_fields = [self.address_line_01, self.address_city, self.address_state.upper(),
                       self.address_zip_code]

        full_address = " ".join(
            [field for field in addr_fields if field is not None]).strip()

        return full_address

    @property
    def get_full_address_with_ATTN(self):
        addr_fields = [self.address_company_or_ATTN, self.address_line_01, self.address_city, self.address_state.upper(),
                       self.address_zip_code]

        full_address = " ".join(
            [field for field in addr_fields if field is not None]).strip()

        return full_address

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'addresses_new_03'
        ordering = ["-address_id"]
        verbose_name = 'address'
        verbose_name_plural = 'addresses'


class Alerts(models.Model):
    id = models.AutoField(primary_key=True)
    alert_connected_vehicle_provider_id = models.IntegerField(null=True)
    alert_schedule_id = models.IntegerField(null=True)
    alert_quick_close_id = models.IntegerField(null=True)
    alert_longtitude = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True)

    alert_latitude = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True)
    alert_dtc = models.CharField(max_length=4000, null=True)
    altert_status = models.IntegerField(null=True, blank=True)
    alert_mileage = models.IntegerField(null=True, blank=True)
    alert_mileage_units = models.IntegerField(null=True, blank=True)
    alert_resolved_at = models.DateTimeField(null=True, blank=True)
    alert_submitted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    created_by = models.ForeignKey(
        InternalUser, related_name='alerts_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='alerts_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'alerts_new_03'
        ordering = ["-id", '-created_at']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)


class AccountClassModel(models.Model):
    account_class_id = models.AutoField(primary_key=True)
    account_type = models.CharField(max_length=30, null=True)
    account_last_updated_at = models.DateTimeField(auto_now=True, null=True)
    account_created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='accountclass_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='accountclass_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'accountclasses_new_03'
        ordering = ["-account_class_id"]
        verbose_name = 'accountclass'
        verbose_name_plural = 'accountclasses'


class CategoryModel(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_description = models.CharField(
        max_length=200, blank=True, null=True)
    category_display = models.IntegerField(blank=True, null=True)
    category_created_at = models.DateTimeField(auto_now_add=True)
    # tracking fields
    created_by = models.ForeignKey(
        InternalUser, related_name='category_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='category_modified', on_delete=models.SET_NULL, null=True, blank=True)
    category_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'categories_new_03'
        ordering = ['-category_id']

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

# this model stores specs data related to vendors which provide catelog links. VendorLink stores the actual format of the link used.
# could be outdated for future use.


class CatalogLinks(models.Model):
    catalog_link_id = models.AutoField(primary_key=True)
    catalog_link_file_used = models.CharField(
        max_length=50, blank=True, null=True)
    catalog_link_display_name = models.CharField(
        max_length=50, blank=True, null=True)
    catalog_link_interface_version = models.CharField(
        max_length=10, blank=True, null=True)
    catalog_link_auth_code = models.CharField(
        max_length=50, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='catelog_links_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='catelog_links_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'catalog_links_new_03'
        ordering = ['-catalog_link_id']
        verbose_name = '(Vendor) Catalog Link'
        verbose_name_plural = '(Vendor) Catalog Links'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)

# 2023-10-16 added new model VendorType. It defines types of vehicle related whole sale vendors: tire shop, repair shop, dealerhip


class VendorTypes(models.Model):
    vendor_type_id = models.AutoField(primary_key=True)
    vendor_type_name = models.CharField(
        max_length=100, null=True, verbose_name='Vendor Type Name')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='vendor_types_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, null=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='vendor_types_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'vendor_types_new_03'
        ordering = ["-vendor_type_id"]
        verbose_name = 'Vendor Type'
        verbose_name_plural = 'Vendor Types'

# 2023-10-16 added new model Vendors (for vehicles)


class Vendors(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    vendor_name = models.CharField(
        max_length=50, null=True, verbose_name='Business Name')
    vendor_contact_persons = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Contact Person (i.e. Kenny)')
    vendor_contact_phone_number = FormattedPhoneNumberField(null=True)
    vendor_comment = models.CharField(max_length=200, null=True, blank=True)
    vendor_contact_email_address = models.CharField(
        max_length=50, null=True, blank=True)
    vendor_is_active = models.BooleanField(
        default=True, null=True, blank=True)
    vendor_email_verified = models.BooleanField(
        default=False, null=True, blank=True)
    vendor_last_email_verified_at = models.DateTimeField(blank=True, null=True)
    vendor_email_verified_type = models.CharField(
        max_length=100, null=True, blank=True)
    vendor_code = models.CharField(max_length=15, null=True, blank=True)
    vendor_limit = models.CharField(max_length=15, null=True, blank=True)
    vendor_terms = models.CharField(max_length=50, null=True, blank=True)
    vendor_account_class = models.CharField(
        max_length=15, null=True, blank=True)
    vendor_type = models.IntegerField(blank=True, null=True)
    vendor_catalog_link = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='vendors_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='vendors_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'vendors_new_03'
        ordering = ["-vendor_id"]
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

# addded VendorLinks model that specified the link spec in 'vendor_link_value' field.


class VendorLinks(models.Model):
    vendor_link_id = models.AutoField(primary_key=True)
    vendor_id = models.IntegerField(null=True, blank=True)
    vendor_link_property = models.CharField(
        max_length=200, null=True, blank=True)
    vendor_link_value = models.CharField(
        max_length=4000, null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='vendor_links_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='vendor_links_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'vendor_links_new_03'
        ordering = ["-vendor_link_id"]
        verbose_name = 'vendor link'
        verbose_name_plural = 'vendor links'


class VendorAdddresses(models.Model):

    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
    address = models.ForeignKey(
        AddressesNewSQL02Model, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(
        auto_now=True, null=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='vendor_addresses_updated_by', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='vendor_addresses_created_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'vendor_addresses_new_03'
        ordering = ["-id", '-created_at']
        verbose_name = 'Vendor Address'
        verbose_name_plural = 'Vendor Addresses'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)


class InvoiceStatusModel(models.Model):
    invoice_status_id = models.AutoField(primary_key=True)
    invoice_status_description = models.CharField(max_length=30, null=True)
    invoice_status_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='invoice_status_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='invoice_status_modified', on_delete=models.SET_NULL, null=True, blank=True)
    invoice_status_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'invoicestatuses_new_03'
        ordering = ["invoice_status_id"]
        verbose_name = 'invoicestatus'
        verbose_name_plural = 'invoicestatuses'


class EmailsNewSQL02Model(models.Model):
    email_id = models.IntegerField(primary_key=True)
    email_type_id = models.IntegerField()
    email_address = models.EmailField()
    email_description = models.CharField(max_length=255, null=True, blank=True)
    email_can_send_notification = models.BooleanField(default=True)
    email_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='email_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='email_modified', on_delete=models.SET_NULL, null=True, blank=True)
    email_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'emails_new_03'
        ordering = ["-email_id"]
        verbose_name = 'email'
        verbose_name_plural = 'emails'


class PhoneDescModel(models.Model):
    phone_desc_id = models.IntegerField(primary_key=True)
    phone_desc = models.CharField(max_length=50, null=True)
    phone_order = models.IntegerField()
    phone_desc_default_type = models.CharField(max_length=5, null=True)
    phone_desc_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='phonedesc_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='phonedesc_modified', on_delete=models.SET_NULL, null=True, blank=True)
    phone_desc_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'phonedescs_new_03'
        ordering = ["-phone_desc_id"]
        verbose_name = 'phonedesc'
        verbose_name_plural = 'phonedescs'


class PhonesNewSQL02Model(models.Model):
    phone_id = models.AutoField(primary_key=True)
    phone_desc = models.ForeignKey(
        PhoneDescModel, on_delete=models.SET_NULL, null=True, related_name='phone_descs')
    phone_number = models.CharField(max_length=20)
    phone_number_digits_only = models.CharField(
        max_length=20, null=True, blank=True)
    phone_number_ext = models.CharField(max_length=10, blank=True, null=True)
    phone_displayed_name = models.CharField(max_length=100)
    phone_memo_01 = models.TextField(blank=True, null=True)
    phone_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='phone_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='phone_modified', on_delete=models.SET_NULL, null=True, blank=True)
    phone_last_updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_phone_number_digit_only(self):
        phone_number_digits = re.sub(r'\D', '', self.phone_number)

    # custom the corresponding data table name for this model
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'phones_new_03'
        ordering = ["-phone_id"]
        verbose_name = 'phone'
        verbose_name_plural = 'phones'


class TaxesModel(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_description = models.CharField(max_length=30, null=True)
    tax_applied_gl_code = models.IntegerField()
    tax_item_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='tax_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='tax_modified', on_delete=models.SET_NULL, null=True, blank=True)
    tax_last_updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'taxes_new_03'
        ordering = ["-tax_id"]
        verbose_name = 'tax'
        verbose_name_plural = 'taxes'


class CustomersNewSQL02Model(models.Model):
    # customer_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
    # primary key = True
    customer_id = models.AutoField(primary_key=True)
    customer_title_id = models.CharField(max_length=20, null=True, blank=True)
    customer_first_name = models.CharField(
        max_length=50, null=True, blank=True)
    customer_last_name = models.CharField(max_length=50, null=True, blank=True)
    customer_middle_name = models.CharField(
        max_length=50, null=True, blank=True)
    customer_dob = models.DateTimeField(null=True, blank=True)
    customer_spouse_name = models.CharField(
        max_length=50, null=True, blank=True)
    # customer_primary_phone_uid = models.CharField(max_length=36, null=True)
    # customer_primary_email_uid = models.CharField(max_length=36, null=True)
    customer_is_okay_to_charge = models.BooleanField(default=True)
    customer_memo_1 = models.CharField(max_length=4000, null=True, blank=True)
    customer_is_tax_exempt = models.BooleanField(default=False)
    customer_resale_permit_nbr = models.CharField(
        max_length=20, null=True, blank=True)
    customer_is_in_social_crm = models.BooleanField(default=True)
    customer_hear_from_us_type = models.CharField(
        max_length=20, null=True, blank=True)
    customer_last_visit_date = models.DateTimeField(null=True, blank=True)
    customer_first_visit_date = models.DateTimeField(null=True, blank=True)
    customer_is_deleted = models.BooleanField(
        default=False, null=True, blank=True)
    customer_is_active = models.BooleanField(
        default=True, null=True, blank=True)  # flip the original 'deleted' field in the old database.
    customer_memebership_nbr = models.CharField(
        max_length=20, null=True, blank=True)
    customer_does_allow_SMS = models.BooleanField(default=True)
    customer_email_address_in_json = models.CharField(
        max_length=200, null=True, blank=True)

    customer_last_updated_at = models.DateTimeField(auto_now=True)
    customer_is_created_from_appointments = models.BooleanField(default=False)
    customer_fleet_vendor_id = models.CharField(
        max_length=100, null=True, blank=True)
    customer_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='customer_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='customer_modified', on_delete=models.SET_NULL, null=True, blank=True)

    # add a new many-to-many-relationship field
    addresses = models.ManyToManyField(
        AddressesNewSQL02Model, through='CustomerAddressesNewSQL02Model', related_name='customer_addresses')
    # add a new many-to-many-relationship field for emails
    emails = models.ManyToManyField(
        EmailsNewSQL02Model, through='CustomerEmailsNewSQL02Model', related_name='customer_emails')
    # many to many field to phones
    phones = models.ManyToManyField(
        PhonesNewSQL02Model, through='CustomerPhonesNewSQL02Model', related_name='customer_phones')
    # many to many fields to Taxes
    taxes = models.ManyToManyField(
        TaxesModel, through='CustomerTaxesModel', related_name='customer_taxes')

    @property
    def get_customer_full_name(self):
        first_name = self.customer_first_name.capitalize(
        ) if self.customer_first_name else None
        middle_name = self.customer_middle_name.capitalize(
        ) if self.customer_middle_name else None
        last_name = self.customer_last_name.capitalize() if self.customer_last_name else None
        name_fields = [first_name, middle_name, last_name]
        full_name = ' '.join(
            [field for field in name_fields if field is not None])
        return full_name.strip() if full_name.strip() else "No available name."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'customers_new_03'   # prolube76DBSTG01.dbo.customers_new_01
        ordering = ["-customer_id"]
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.get_customer_full_name


class CustomerAddressesNewSQL02Model(models.Model):
    address = models.ForeignKey(
        AddressesNewSQL02Model, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.CASCADE)

    customeraddress_created_at = models.DateTimeField(
        auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='customeraddress_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='customeraddress_modified', on_delete=models.SET_NULL, null=True, blank=True)
    customeraddress_last_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'customeraddresses_new_03'
        ordering = ["-address", '-customer']
        # verbose_name = 'customeraddress'
        # verbose_name_plural = 'customeraddresses'


class CustomerEmailsNewSQL02Model(models.Model):
    customeremail_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.CASCADE)
    email = models.ForeignKey(EmailsNewSQL02Model, on_delete=models.CASCADE)
    customeremail_is_selected = models.BooleanField(default=True)

    customeremail_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='customeremail_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='customeremail_modified', on_delete=models.SET_NULL, null=True, blank=True)
    customeremail_last_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'customeremails_new_03'
        ordering = ["-customeremail_id", '-email']
        # verbose_name = 'customeremail'
        # verbose_name_plural = 'customeremails'


class CustomerPhonesNewSQL02Model(models.Model):
    phone = models.ForeignKey(PhonesNewSQL02Model, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.CASCADE)
    customerphone_created_at = models.DateTimeField(auto_now_add=True)
    customerphone_last_updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='customerphone_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='customerphone_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

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
    repair_order_phase_last_updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='repair_order_phase_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='repair_order_phase_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'repairorderphases_new_03'
        ordering = ["repair_order_phase_id"]
        verbose_name = 'repairorderphase'
        verbose_name_plural = 'repairorderphases'


class MakesNewSQL02Model(models.Model):
    make_id = models.AutoField(primary_key=True)
    make_name = models.CharField(max_length=30, null=True)
    make_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='make_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='make_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'makes_new_03'
        ordering = ["-make_id"]
        verbose_name = 'make'
        verbose_name_plural = 'makes'

    def __str__(self):
        return self.make_name.strip()


class ModelsNewSQL02Model(models.Model):
    model_id = models.AutoField(primary_key=True)
    make = models.ForeignKey(MakesNewSQL02Model, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=30, null=True)
    model_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='model_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='model_modified', on_delete=models.SET_NULL, null=True, blank=True)
    make_last_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'models_new_03'
        ordering = ["-model_id", 'make']
        verbose_name = 'model'
        verbose_name_plural = 'models'

    def __str__(self):
        return self.model_name.strip()


class EnginesModel(models.Model):
    engine_id = models.AutoField(primary_key=True)
    engine_displacement_CID = models.DecimalField(
        max_digits=10, decimal_places=1, null=True)
    engine_displacement_liter = models.DecimalField(
        max_digits=10, decimal_places=1, null=True)
    engine_number_of_cylinder = models.IntegerField(null=True)
    engine_valve_per_cyclinder = models.IntegerField(null=True)
    engine_head_configuration_type = models.CharField(
        max_length=100, blank=True, null=True)
    engine_boost_type = models.CharField(max_length=100, blank=True, null=True)
    engine_ignition_system = models.CharField(
        max_length=100, blank=True, null=True)
    engine_vin_code = models.CharField(max_length=20, blank=True, null=True)
    engine_fuel_system = models.CharField(
        max_length=100, blank=True, null=True)
    engine_fuel_delivery_method_type = models.CharField(
        max_length=100, blank=True, null=True)
    engine_fuel_type = models.CharField(max_length=100, blank=True, null=True)
    engine_fuel_control_type = models.CharField(
        max_length=100, blank=True, null=True)
    engine_block_configuration = models.CharField(
        max_length=100, blank=True, null=True)
    engine_fuel_system_configuration = models.CharField(
        max_length=100, blank=True, null=True)
    engine_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='engine_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='engine_modified', on_delete=models.SET_NULL, null=True, blank=True)
    engine_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def get_engine_feature(self):
        fields = [str(self.engine_id), ": ",
                  str(self.engine_number_of_cylinder).strip(
        ) if self.engine_number_of_cylinder is not None else '',
            str(self.engine_valve_per_cyclinder).strip(
        ) if self.engine_valve_per_cyclinder is not None else '',
            "-", self.engine_vin_code if self.engine_vin_code is not None else '',
            "-", self.engine_fuel_type.strip() if self.engine_fuel_type is not None else '',
            "-", self.engine_head_configuration_type if self.engine_head_configuration_type is not None else '',
            "-", self.engine_boost_type.strip() if self.engine_boost_type is not None else '',
            "-", self.engine_fuel_type.strip() if self.engine_fuel_type is not None else '',
            "-", self.engine_fuel_system_configuration.strip() if self.engine_fuel_system_configuration is not None else '',
        ]
        engine_feature = "".join(
            [field for field in fields if field is not None])
        return engine_feature if engine_feature else "No available engine config cound."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'engines_new_03'
        ordering = ["-engine_id"]
        verbose_name = 'engine'
        verbose_name_plural = 'engines'

    def __str__(self):
        return self.get_engine_feature


class TransmissionsModel(models.Model):
    transmission_id = models.AutoField(primary_key=True)
    transmission_type = models.CharField(max_length=100, blank=True, null=True)
    transmission_manufacturer_code = models.CharField(
        max_length=100, blank=True, null=True)
    transmission_control_type = models.CharField(
        max_length=100, blank=True, null=True)
    transmission_is_electronic_controlled = models.BooleanField(default=False)
    transmission_number_of_speed = models.IntegerField(null=True, blank=True)
    transmission_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='transmission_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='transmission_modified', on_delete=models.SET_NULL, null=True, blank=True)
    transmission_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    @property
    def get_transmission_feature(self):
        fields = [str(self.transmission_id), ": ", self.transmission_type.strip(
        ),  "-", self.transmission_control_type, "-", self.transmission_manufacturer_code.strip(),
            '-',
            "electronic controlled" if str(self.transmission_is_electronic_controlled) else "not electronic controlled"]

        transmission_feature = "".join(
            [field for field in fields if field is not None])
        return transmission_feature if transmission_feature else "No available drive type."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'transmissions_new_03'
        ordering = ["-transmission_id"]
        verbose_name = 'transmission'
        verbose_name_plural = 'transmissions'

    def __str__(self):
        return self.get_transmission_feature


class BrakesModel(models.Model):
    brake_id = models.AutoField(primary_key=True)
    brake_system_type = models.CharField(max_length=150, null=True, blank=True)
    brake_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='brake_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='brake_modified', on_delete=models.SET_NULL, null=True, blank=True)
    brake_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    @property
    def get_brake_feature(self):
        fields = [str(self.brake_id), ": ", self.brake_system_type.strip()]

        brake_feature = "".join(
            [field for field in fields if field is not None])
        return brake_feature if brake_feature else "No available brake system found."

    class Meta:
        db_table = 'brakes_new_03'
        ordering = ["-brake_id"]
        verbose_name = 'brake'
        verbose_name_plural = 'brakes'

    def __str__(self):
        return self.get_brake_feature


class GVWsModel(models.Model):
    gvw_id = models.AutoField(primary_key=True)
    gvw_text = models.CharField(max_length=150, null=True)
    gvw_created_at = models.DateTimeField(auto_now_add=True)
    gvw_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    @property
    def get_gvw_feature(self):
        fields = [str(self.gvw_id), ": ", self.gvw_text.strip()]

        gvw_feature = "".join(
            [field for field in fields if field is not None])
        return gvw_feature if gvw_feature else "No available brake system found."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'gvws_new_03'
        ordering = ["-gvw_id"]
        verbose_name = 'gvw'
        verbose_name_plural = 'gvws'

    def __str__(self):
        return self.get_gvw_feature


class SubmodelsModel(models.Model):
    submodel_id = models.AutoField(primary_key=True)
    submodel_model = models.ForeignKey(
        ModelsNewSQL02Model, on_delete=models.CASCADE)
    submodel_name = models.CharField(max_length=150, null=True)
    submodel_DMV_id = models.IntegerField(null=True)
    submodel_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='submodel_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='submodel_modified', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_sub_model_feature(self):
        fields = [str(self.submodel_id),
                  ": ", self.submodel_name.strip() if self.submodel_name is not None else ''
                  ]
        sub_model_feature = "".join(
            [field for field in fields if field is not None])
        return sub_model_feature if sub_model_feature else "No available sub model."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'submodels_new_03'
        ordering = ["-submodel_id"]
        verbose_name = 'submodel'
        verbose_name_plural = 'submodels'

    def __str__(self):
        return self.get_sub_model_feature


class DrivesModel(models.Model):
    drive_id = models.AutoField(primary_key=True)
    drive_type = models.CharField(max_length=150, null=True)
    drive_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='drive_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='drive_modified', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_drive_type_feature(self):
        fields = [str(self.drive_id), ": ", self.drive_type.strip()]
        drive_type_feature = "".join(
            [field for field in fields if field is not None])
        return drive_type_feature if drive_type_feature else "No available drive type."

    def __str__(self):
        return self.get_drive_type_feature

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'drives_new_03'
        ordering = ["-drive_id"]
        verbose_name = 'drive'
        verbose_name_plural = 'drives'


class BodyStylesModel(models.Model):
    body_style_id = models.AutoField(primary_key=True)
    body_style_name = models.CharField(max_length=150, null=True)
    body_style_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='body_style_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='body_style_modified', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_body_style_feature(self):
        fields = [str(self.body_style_id), ": ", self.body_style_name.strip()]
        body_style_feature = "".join(
            [field for field in fields if field is not None])
        return body_style_feature if body_style_feature else "No available body style found."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'bodystyles_new_03'
        ordering = ["-body_style_id"]
        verbose_name = 'bodystyle'
        verbose_name_plural = 'bodystyles'


class MyShopVehicleConfigsModel(models.Model):
    myshop_vehicle_config_id = models.AutoField(primary_key=True)
    myshop_year_id = models.IntegerField(null=True)
    myshop_make = models.ForeignKey(
        MakesNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='myshop_makes')
    myshop_model = models.ForeignKey(
        ModelsNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='myshop_models')
    myshop_submodel = models.ForeignKey(
        SubmodelsModel, on_delete=models.SET_NULL, null=True, related_name='myshop_submodels')
    myshop_bodystyle = models.ForeignKey(
        BodyStylesModel, on_delete=models.SET_NULL, null=True, related_name='myshop_bodystyles')
    myshop_engine = models.ForeignKey(
        EnginesModel, on_delete=models.SET_NULL, null=True, related_name='myshop_engines')
    myshop_brake = models.ForeignKey(
        BrakesModel, on_delete=models.SET_NULL, null=True, related_name='myshop_brakes')
    myshop_transmission = models.ForeignKey(
        TransmissionsModel, on_delete=models.SET_NULL, null=True, related_name='myshop_transmissions')
    myshop_GVW = models.ForeignKey(
        GVWsModel, on_delete=models.SET_NULL, null=True, related_name='myshop_gvws')
    myshop_drive = models.ForeignKey(
        DrivesModel, on_delete=models.SET_NULL, null=True, name='myshop_drives')
    myshop_vehicle_config_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='myshop_vehicle_config_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='myshop_vehicle_config_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'myshopvehicleconfigs_new_03'
        ordering = ["-myshop_vehicle_config_id"]
        verbose_name = 'myshop vehicle configuration'
        verbose_name_plural = 'myshop vehicle configurations'


class VehicleConfigMyShopConfigsModel(models.Model):
    vehicle_config_id = models.AutoField(primary_key=True)
    myshop_vehicle_config = models.ForeignKey(MyShopVehicleConfigsModel,
                                              on_delete=models.SET_NULL, null=True, related_name='vehicleconfigmyshopconfigs')
    vehicle_config_myshop_config_created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='vehicle_config_myshop_config_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='vehicle_config_myshop_config_modified', on_delete=models.SET_NULL, null=True, blank=True)

    # Methods
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super(MyShopVehicleConfigsModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'vehicleconfigmyshopconfigs_new_03'
        ordering = ["-vehicle_config_id"]
        verbose_name = 'vehicleconfigmyshopconfig'
        verbose_name_plural = 'vehicleconfigmyshopconfigs'


class VehiclesNewSQL02Model(models.Model):
    # vehicle_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)  # default = uuid.uuid4
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_cust = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='vehicle_customers', blank=True)
    vehicle_year = models.CharField(max_length=20, null=True, blank=True)
    vehicle_make = models.ForeignKey(
        MakesNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='vehicle_makes', blank=True)
    vehicle_sub_model = models.ForeignKey(
        SubmodelsModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_submodels', blank=True)
    vehicle_body_style = models.ForeignKey(
        BodyStylesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_bodystyles', blank=True)
    vehicle_engine = models.ForeignKey(
        EnginesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_engines', blank=True)
    vehicle_transmission = models.ForeignKey(
        TransmissionsModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_transmissions', blank=True)
    vehicle_brake = models.ForeignKey(
        BrakesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_brakes', blank=True)
    vehicle_drive_type = models.ForeignKey(
        DrivesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_drives', blank=True)
    vehicle_gvw = models.ForeignKey(
        GVWsModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_gvws', blank=True)
    vehicle_odometer_1 = models.BigIntegerField(null=True, blank=True)
    vehicle_odometer_2 = models.BigIntegerField(null=True, blank=True)
    VIN_number = models.CharField(max_length=50, null=True, blank=True)
    vehicle_inspection_datetime = models.DateTimeField(null=True, blank=True)
    vehicle_last_in_date = models.DateTimeField(null=True, blank=True)
    vehicle_license_plate_nbr = models.CharField(
        max_length=20, null=True, blank=True)
    vehicle_license_state = models.CharField(
        max_length=20, null=True, blank=True)
    vehicle_part_level = models.CharField(max_length=20, null=True, blank=True)
    vehicle_labor_level = models.CharField(
        max_length=20, null=True, blank=True)
    vehicle_used_level = models.CharField(max_length=20, null=True, blank=True)
    vehicle_memo_01 = models.CharField(max_length=4000, null=True, blank=True)
    vehicle_memo_does_print_on_order = models.BooleanField(default=False)
    vehicle_is_included_in_crm_compaign = models.BooleanField(default=True)
    vehicle_color = models.CharField(max_length=20, null=True, blank=True)

    vehicle_record_is_active = models.BooleanField(default=True)
    vehicle_class_id = models.CharField(max_length=20, null=True, blank=True)
    vehicle_engine_hour_in = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True)
    vehicle_engine_hour_out = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True)
    vehicle_active_recall_counts = models.IntegerField(null=True, blank=True)
    vehicle_recall_last_checked_datetime = models.DateTimeField(
        null=True, blank=True)
    vehicle_phone = models.ForeignKey(
        PhonesNewSQL02Model, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicle_phones',)
    vehicle_contact_phone_main_new_uid = models.CharField(
        max_length=36, null=True, blank=True)

    vehicle_authorized_customers = models.ManyToManyField(
        'CustomersNewSQL02Model', related_name='authorized_vehicles', blank=True)

    vehicle_created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        InternalUser, related_name='vehicle_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='vehicle_modified', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'vehicles_new_03'
        ordering = ["-vehicle_id"]
        verbose_name = 'vehicle'
        verbose_name_plural = 'vehicles'


class TextMessagesModel(models.Model):
    text_message_id = models.AutoField(primary_key=True)
    text_customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='text_customers')
    text_body = models.CharField(max_length=4000, blank=True, null=True)
    text_external_id = models.BigIntegerField(null=True, blank=True)
    text_type = models.IntegerField()
    text_to_phonenumber = models.CharField(max_length=15)
    text_direction = models.BooleanField(default=False)
    text_status = models.IntegerField(null=True, blank=True)
    text_error_message = models.CharField(
        max_length=255, null=True, blank=True)
    text_error_code = models.CharField(max_length=255, null=True, blank=True)
    text_datetime = models.DateTimeField(null=True, blank=True)
    text_body_size = models.IntegerField(null=True, blank=True)
    text_created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='text_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='text_modified', on_delete=models.SET_NULL, null=True, blank=True)
    text_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'textmessages_new_03'
        ordering = ['-text_message_id']
        verbose_name = 'textmessage'
        verbose_name_plural = 'textmessages'


class VehicleNotesModel(models.Model):
    vehicle_note_id = models.AutoField(primary_key=True)
    vehicle_note_type_id = models.IntegerField(null=True, blank=True)
    vehicle = models.ForeignKey(
        VehiclesNewSQL02Model, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehiclenotes_vehicle')
    vehicle_note_text = models.CharField(max_length=400, null=True, blank=True)

    vehicle_note_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)
    vehicle_note_created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    vehicle_note_is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='vehicle_note_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='vehicle_note_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'vehiclenotes_new_03'
        ordering = ['-vehicle_note_id']
        verbose_name = 'vehiclenote'
        verbose_name_plural = 'vehiclenotes'


class CannedJobsNewSQL02Model(models.Model):
    canned_job_id = models.AutoField(primary_key=True)
    canned_job_title = models.CharField(max_length=50, null=True)
    canned_job_description = models.CharField(max_length=200, null=True)
    canned_job_is_in_quick_menu = models.BooleanField(default=False)
    canned_job_category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True)
    canned_job_applied_year = models.IntegerField(blank=True, null=True)
    canned_job_applied_make_id = models.IntegerField(blank=True, null=True)
    canned_job_applied_submodel_id = models.IntegerField(blank=True, null=True)
    canned_job_vehicle_class = models.CharField(
        max_length=50, null=True, blank=True)
    canned_job_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)
    canned_job_created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='canned_job_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='canned_job_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'cannedjobs_new_03'
        ordering = ["-canned_job_id"]


LINE_ITEM_TYPES = [
    ('part', 'Part'),
    ('labor', 'Labor'),
    ('unknown', 'unknown')
]


class LineItemsNewSQL02Model(models.Model):
    line_item_id = models.AutoField(primary_key=True)
    line_item_account_class = models.ForeignKey(
        AccountClassModel, on_delete=models.SET_NULL, null=True, related_name='lineitem_accountclasses')
    line_item_category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True, related_name='lineitem_category')
    # 2023-10-01 newly added field
    line_item_type = models.CharField(
        max_length=10, choices=LINE_ITEM_TYPES, null=True)
    line_item_description = models.CharField(max_length=2000)
    line_item_cost = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_sale = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_is_tax_exempt = models.BooleanField(default=False)
    line_item_has_no_commission = models.BooleanField(default=True)
    line_item_has_fixed_commission = models.BooleanField(default=False)
    line_item_order_revision_id = models.IntegerField(null=True)
    # line_item_order_revision_id = models.ForeignKey(OrderRevisionNewSQL02Model, models.SET_NULL, blank=True, null=True)
    # any foreignKey field will add '_id' automatically when creating a sql data table. In the sql
    line_item_canned_job = models.ForeignKey(
        CannedJobsNewSQL02Model, models.SET_NULL, blank=True, null=True)
    line_item_labor_sale = models.DecimalField(max_digits=12, decimal_places=2)
    line_item_part_sale = models.DecimalField(max_digits=12, decimal_places=2)
    line_item_part_only_sale = models.DecimalField(
        max_digits=12, decimal_places=2)
    line_item_labor_only_sale = models.DecimalField(
        max_digits=12, decimal_places=2)
    line_item_sublet_sale = models.DecimalField(
        max_digits=12, decimal_places=2)
    line_item_package_sale = models.DecimalField(
        max_digits=12, decimal_places=2)
    line_item_tire_fee = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    line_item_parent_line_item = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    line_item_created_at = models.DateTimeField(auto_now_add=True)
    line_item_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='line_item_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='line_item_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'lineitems_new_03'
        ordering = ["-line_item_id"]


class NoteItemsNewSQL02Model(models.Model):
    note_item_id = models.AutoField(primary_key=True)
    # when it is a foreign key,"_id" is added at the end of the field name
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='lineitem_noteitem')
    note_item_text = models.TextField(null=True, blank=True)
    note_item_is_printed_on_order = models.BooleanField(default=True)
    note_item_tech_observation = models.TextField(null=True, blank=True)

    note_item_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='note_item_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='note_item_modified', on_delete=models.SET_NULL, null=True, blank=True)
    note_item_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'noteitems_new_03'
        ordering = ["-note_item_id"]
        verbose_name = 'noteitem'
        verbose_name_plural = 'noteitems'


class CustomerTaxesModel(models.Model):
    tax_id = models.ForeignKey(TaxesModel, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.CASCADE)
    customertaxes_created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    customertaxes_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'customertaxes_new_03'
        ordering = ["-tax_id", '-customer_id']
        verbose_name = 'customertax'
        verbose_name_plural = 'customertaxes'


class lineItemTaxesNewSQL02Model(models.Model):
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='taxes')
    line_item_tax_id = models.IntegerField(null=True)
    line_item_tax_charged = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_tax_rate = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_tax_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='line_item_tax_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='line_item_tax_modified', on_delete=models.SET_NULL, null=True, blank=True)
    line_item_tax_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'lineitemtaxes_new_03'
        ordering = ["-line_item_id"]


class LaborItemModel(models.Model):
    labor_item_id = models.AutoField(primary_key=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='lineitem_laboritem')
    labor_rate_description_id = models.IntegerField()
    labor_item_is_user_entered_labor_rate = models.BooleanField()
    labor_item_work_performed = models.TextField(blank=True, null=True)
    labor_item_hours_charged = models.DecimalField(
        max_digits=10, decimal_places=2)
    labor_item_symptom = models.CharField(
        max_length=4000, null=True, blank=True)
    labor_item_is_come_back_invoice = models.BooleanField(
        default=False, null=True)
    labor_item_parts_estimate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    labor_item_is_MPlg_item = models.IntegerField(default=False)
    labor_item_is_Changed_MPlg_item = models.BooleanField(default=False)

    labor_item_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='labor_item_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='labor_item_modified', on_delete=models.SET_NULL, null=True, blank=True)
    labor_item_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'laboritems_new_03'
        ordering = ["-labor_item_id"]


class PartsModel(models.Model):
    part_id = models.AutoField(primary_key=True)
    part_description = models.CharField(max_length=500, null=True, blank=True)
    part_cost = models.DecimalField(max_digits=12, decimal_places=2)
    part_price = models.DecimalField(max_digits=12, decimal_places=2)
    part_is_tax_exempt = models.BooleanField(default=False)
    part_category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True)
    part_account_class = models.ForeignKey(
        AccountClassModel, on_delete=models.SET_NULL, null=True, related_name='parts_accountclasses')
    part_comments = models.CharField(max_length=4000, null=True, blank=True)
    part_manufacturer_id = models.IntegerField(null=True)
    part_list_price = models.DecimalField(max_digits=12, decimal_places=2)
    part_is_user_entered_price = models.DecimalField(
        max_digits=12, decimal_places=2)
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
    created_by = models.ForeignKey(
        InternalUser, related_name='part_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='part_modified', on_delete=models.SET_NULL, null=True, blank=True)
    part_last_updated_at = models.DateTimeField(auto_now=True, null=True,)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'parts_new_03'
        ordering = ["-part_id"]


class PartItemModel(models.Model):
    part_item_id = models.AutoField(primary_key=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='partitems_lineitems')
    part_discount_description_id = models.IntegerField(null=True)
    part_item_is_user_entered_unit_sale = models.BooleanField(default=False)
    part_item_is_user_entered_unit_cost = models.BooleanField(default=False)
    part_item_quantity = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    part_item_unit_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    part_item_unit_list = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    part_item_unit_sale = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    part_item_unit_cost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    part_item_part_no = models.CharField(max_length=100, null=True, blank=True)
    part_item_part = models.ForeignKey(
        PartsModel, on_delete=models.SET_NULL, null=True, related_name='partitems_parts')
    part_item_is_confirmed = models.BooleanField(default=False)
    part_item_vendor_code = models.CharField(
        max_length=25, null=True, blank=True)
    part_item_vendor_id = models.IntegerField(null=True)
    part_item_manufacture_id = models.IntegerField(null=True)
    part_item_invoice_number = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_commission_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    part_item_is_committed = models.BooleanField(default=False)
    part_item_is_quantity_confirmed = models.BooleanField(default=False)
    part_item_confirmed_quantity = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    part_item_is_part_ordered = models.BooleanField(default=False)
    part_item_is_core = models.BooleanField(default=False)
    part_item_is_bundled_kit = models.BooleanField(default=False)
    part_item_is_MPlg_item = models.BooleanField(default=False)
    part_item_is_changed_MPlg_item = models.BooleanField(default=False)
    part_item_part_type = models.CharField(
        max_length=10, null=True, blank=True)
    part_item_size = models.CharField(max_length=20, null=True, blank=True)
    part_item_is_tire = models.BooleanField(default=False)
    part_item_vendor_id = models.IntegerField(null=True)
    part_item_meta = models.CharField(max_length=4000, null=True, blank=True)
    part_item_added_from_supplier = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_purchased_from_vendor = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_purchased_from_supplier = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_shipping_description = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_shipping_cost = models.CharField(
        max_length=50, null=True, blank=True)

    part_item_created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='part_item_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='part_item_modified', on_delete=models.SET_NULL, null=True, blank=True)
    part_item_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'partitems_new_03'
        ordering = ["-part_item_id"]
        verbose_name = 'partitem'
        verbose_name_plural = 'partitems'


class Inventories(models.Model):

    inventory_id = models.AutoField(primary_key=True)
    inventory_part = models.ForeignKey(
        PartsModel, on_delete=models.CASCADE, related_name='inventory_part')
    inventory_on_hand = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    inventory_on_order = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    inventory_location = models.CharField(max_length=80, null=True, blank=True)
    inventory_last_sold_at = models.DateTimeField(null=True, blank=True)
    inventory_available_quantity = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    inventory_committed_quantity = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    ivnentory_condition_id = models.IntegerField(null=True, blank=True)
    inventory_superceded_by = models.ForeignKey(
        PartsModel, on_delete=models.CASCADE, related_name='inventory_part_superceded_by', null=True, blank=True)
    inventory_restock_quantity = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_order_point = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_core_quantity = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_does_pay_comission = models.BooleanField(default=False)
    inventory_total_cost_amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_last_cost_amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_prior_to_last_cost_amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, null=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='inventory_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='inventory_created_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'inventories_new_03'
        ordering = ["-inventory_id", '-created_at']
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)


class RepairOrdersNewSQL02Model(models.Model):
    # repair_order_new_uid_v01 = models.UUIDField(primary_key=True)  # models.UUIDField(primary_key=True)  # models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
    repair_order_id = models.AutoField(primary_key=True)
    repair_order_phase = models.ForeignKey(
        RepairOrderPhasesNewSQL02Model, on_delete=models.SET_NULL, blank=True, null=True)
    # remove the `_id` from the field name. due to recent adding a foreign key.. by adding a foreign key field, Django will add '_id' for the field in the SQL data table.
    repair_order_customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True)

    repair_order_vehicle = models.ForeignKey(
        VehiclesNewSQL02Model, on_delete=models.SET_NULL, null=True, blank=True)

    repair_order_serviced_vehicle_location = models.CharField(
        max_length=36, null=True)
    repair_order_service_status = models.CharField(max_length=36, null=True)
    repair_order_scheduled_start_datetime = models.DateTimeField(null=True)
    # blank = False so this is a required field on form (pending testing)
    repair_order_billed_hours = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=False)
    repair_order_promise_datetime = models.DateTimeField(null=True)
    repair_order_is_printed = models.BooleanField(default=False)
    repair_order_invoice_is_printed = models.BooleanField(default=False)
    repair_order_serviced_vehicle_in_datetime = models.DateTimeField(
        null=True, blank=True)
    repair_order_serviced_vehicle_out_datetime = models.DateTimeField(
        null=True)
    repair_order_serviced_vehicle_hat = models.CharField(
        max_length=20, null=True)
    repair_order_posted_datetime = models.DateTimeField(null=True)
    repair_order_serviced_vehicle_odometer_in = models.BigIntegerField(
        null=True)
    repair_order_serviced_vehicle_odometer_out = models.BigIntegerField(
        null=True)
    repair_order_reference_number = models.CharField(
        max_length=30, null=True, blank=True)
    repair_order_receipt_printed_datetime = models.DateTimeField(null=True)
    repair_order_snapshot_is_tax_exempt = models.BooleanField(default=False)
    repair_order_aggr_notes = models.CharField(
        max_length=4000, null=True, blank=True)
    repair_order_observation_text_area = models.CharField(
        max_length=4000, null=True)
    repair_order_created_as_estimate = models.BooleanField(
        default=False)  # connecting to the estimates
    repair_order_snapshot_margin_pct = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_haz_waste_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_labor_sale_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_parts_sale_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_supply_from_shop_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_tax_haz_material_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_tax_supply_from_shop_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_total_tax_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_balance_due_adjusted = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_discounted_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_part_discounted_desc_id = models.IntegerField(
        null=True, blank=True)
    repair_order_snapshot_labor_discounted_desc_id = models.IntegerField(
        null=True, blank=True)
    repair_order_snapshot_order_total_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_calc_haz_waste_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_calc_shop_supply_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_serviced_vehicle_engine_hours_in = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True)
    repair_order_serviced_vehicle_engine_hours_out = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True)
    repair_order_appointment_request_uid = models.CharField(
        max_length=50, null=True, blank=True)

    repair_order_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)
    repair_order_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='repair_order_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='repair_order_modified', on_delete=models.SET_NULL, null=True, blank=True)

    # added many-to-many relationship fields managers.
    lineitems = models.ManyToManyField(LineItemsNewSQL02Model, through='RepairOrderLineItemSquencesNewSQL02Model',
                                       related_name='lineitems')

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'repairorders_new_03'
        ordering = ["-repair_order_id"]
        verbose_name = 'repairorder'
        verbose_name_plural = 'repairorders'

    def get_absolute_url(self):
        return reverse('repair_order_detail', kwargs={'pk': self.pk})


class OrderRevisionNewSQL02Model(models.Model):
    order_revision_id = models.AutoField(primary_key=True)
    order_revision_repair_order = models.ForeignKey(
        RepairOrdersNewSQL02Model, models.SET_NULL, blank=True, null=True, related_name='orderrevisions')
    order_revision_sub_estimate_number = models.IntegerField(
        blank=True, null=True)
    order_revision_date = models.DateTimeField(null=True)
    time_of_call = models.DateTimeField(null=True)
    order_revision_initiated_by = models.CharField(max_length=20, null=True)
    order_revision_by_service_writer_id = models.IntegerField(null=True)
    order_revision_authorizaton_by_name = models.CharField(
        max_length=50, null=True, blank=True)
    order_revision_number_called = models.CharField(max_length=50, null=True)
    order_revision_reason = models.CharField(max_length=200, null=True)
    order_revision_current_estimate = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_revision_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_vehicle_id = models.ForeignKey(
        VehiclesNewSQL02Model, models.SET_NULL, blank=True, null=True)
    order_revision_labor_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_parts_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_sublet_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_haz_waste_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_shop_supplies_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_tax_amount_haz_mat = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_tax_amount_shop_supplies = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_discounted_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_tax_charged = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_tire_fee_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_created_at = models.DateTimeField(auto_now_add=True)
    order_revision_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='order_revision_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='order_revision_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'orderrevisions_new_03'
        ordering = ["-order_revision_id"]


class RepairOrderLineItemSquencesNewSQL02Model(models.Model):
    ro_line_item_sequence_id = models.AutoField(primary_key=True)
    repair_order = models.ForeignKey(
        RepairOrdersNewSQL02Model, models.CASCADE, blank=True, null=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, models.CASCADE, blank=True, null=True)
    sequence = models.IntegerField(null=True)

    ro_line_item_sequence_created_at = models.DateTimeField(auto_now_add=True)
    ro_line_item_sequence_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='ro_line_item_sequence_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='ro_line_item_sequence_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'repairorderlineitemsequences_new_03'
        ordering = ["-ro_line_item_sequence_id", 'repair_order', 'line_item']


class LineItemAssignedTechnicanModel(models.Model):
    line_item_assigned_tech_id = models.AutoField(primary_key=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, models.CASCADE, blank=True, null=True)
    old_employee_id = models.IntegerField(null=True, blank=True)
    assigned_tech_hours_actual = models.DecimalField(
        max_digits=15, decimal_places=2)
    assigned_tech_hours_pay = models.DecimalField(
        max_digits=15, decimal_places=2)
    assigned_tech_comission = models.DecimalField(
        max_digits=15, decimal_places=2)

    created_by = models.ForeignKey(
        InternalUser, related_name='line_item_assigned_tech_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='line_item_assigned_tech_modified', on_delete=models.SET_NULL, null=True, blank=True)
    line_item_assigned_tech_created_at = models.DateTimeField(
        auto_now_add=True)
    line_item_assigned_tech_last_change_date = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        # for naming you table
        db_table = "lineitemassignedtechnicans_new_03"
        ordering = ["-line_item"]


class PaymentTransactionsModel(models.Model):
    payment_transaction_id = models.AutoField(primary_key=True)
    payment_transcation_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)
    payment_transcation_created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='payment_transaction_tech_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='payment_transaction_modified', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'paymenttransactions_new_03'
        ordering = ["-payment_transaction_id",]


class PaymentsModel(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_repair_order = models.ForeignKey(
        RepairOrdersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='payment_repairorders')
    payment_record_number = models.IntegerField(null=True)
    payment_customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='payment_customers')
    payment_date = models.DateTimeField(null=True)
    payment_check_data = models.CharField(
        max_length=100, null=True, blank=True)
    payment_auth_data = models.CharField(max_length=100, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_invoice_status = models.ForeignKey(
        InvoiceStatusModel, on_delete=models.SET_NULL, null=True, related_name='payment_invoicestatuses')
    payment_is_NSF = models.BooleanField(default=False)
    payment_is_NSF_reversal = models.BooleanField(default=False)
    payment_is_fee_payment = models.BooleanField(default=False)
    payment_total_payment = models.DecimalField(
        max_digits=10, decimal_places=2)
    payment_deletion_date = models.DateTimeField(null=True)
    payment_transcation = models.ForeignKey(
        PaymentTransactionsModel, on_delete=models.SET_NULL, null=True, related_name='payment_transactions')
    payment_account_class = models.ForeignKey(
        AccountClassModel, on_delete=models.SET_NULL, null=True, related_name='payment_accountclasses')
    payment_verification_data = models.CharField(
        max_length=200, null=True, blank=True)
    payment_receipt_one = models.CharField(
        max_length=200, null=True, blank=True)
    payment_receipt_two = models.CharField(
        max_length=200, null=True, blank=True)
    payment_receipt_three = models.CharField(
        max_length=200, null=True, blank=True)

    payment_created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    payment_last_updated_at = models.CharField(
        max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='payment_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='payment_modified', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'payments_new_03'
        ordering = ["-payment_id",]
        verbose_name = 'payment'
        verbose_name_plural = 'payments'


# created 2023-10-18. store the variable_name info and its group name. updated by management script "populate_nhtsa_variable_list".

class NhtsaVariableList(models.Model):
    id = models.AutoField(primary_key=True)
    variable_id = models.IntegerField(unique=True, default=None)
    variable_name = models.CharField(max_length=200, null=True, blank=True)
    variable_group_name = models.CharField(
        max_length=200, null=True, blank=True)
    variable_description_html = models.CharField(
        max_length=4000, null=True, blank=True)
    variable_data_type = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nhtsa_variable_list'
        ordering = ["-id", 'variable_id']


# this model stores each snapshot pulled for each vin from NHTSA gov website.
class VinNhtsaApiSnapshots(models.Model):
    # Assuming standard VIN length of 17 characters. NHTSA website
    id = models.BigAutoField(primary_key=True)
    vin = models.CharField(
        max_length=17, verbose_name="Vehicle Identification Number (VIN)")
    variable_id = models.ForeignKey(
        NhtsaVariableList, on_delete=models.SET_NULL, null=True,
        to_field='variable_id',  # specify the field of the related model is variable_id
        related_name='nhtsa_variableids')
    variable_name = models.CharField(max_length=255, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    value_id = models.IntegerField(null=True, blank=True)

    source = models.CharField(
        max_length=300, default=NHTSA_API_URL, null=True, blank=True)
    results_count = models.IntegerField(null=True, blank=True)
    results_message = models.CharField(max_length=800, null=True, blank=True)
    results_search_criteria = models.CharField(
        max_length=300, null=True, blank=True)
    # keeps 5 versions of vin info pulled from nhtsa.gov
    version = models.IntegerField(default=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vin_snapshots_nhtsa_new_03'
        ordering = ['-id', '-created_at', 'vin', 'variable_id']
        indexes = [
            # Index to speed up searches based on created at, VIN and VariableID
            models.Index(fields=['-created_at', 'vin', 'variable_id']),
        ]

    def __str__(self):
        return f"{self.vin} - {self.variable_name}: {self.value}"


# this model tracks the repair status of each line item.
class LineItemCompletionTracking(models.Model):

    LINE_ITEM_TYPE_CHOICES = (
        ('unassigned_type', 'Unassigned Line Item Type'),
        ('part', 'Part'),
        ('labor', 'Labor'),
    )
    # the intention is to have all line items with status_choice=completed
    LINE_ITEM_STATUS_CHOICES = (
        ('not started', 'Not Started'),
        ('starting', 'Starting'),
        ('in_progress', 'In Progress'),
        ('initial_completion', 'Initial Completion'),
        ('repair_verifying', 'Repair Verifyng'),
        ('completed', 'Completed'),
    )
    id = models.BigAutoField(primary_key=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='lineitem_completiontracking')

    line_item_assigned_technician = models.ForeignKey(
        InternalUser, on_delete=models.SET_NULL, null=True)
    line_item_technican_notes = models.TextField(null=True, blank=True)
    line_item_before_images = models.ImageField(
        upload_to='line_item_before_images/')
    line_item_after_images = models.ImageField(
        upload_to='line_item_after_images/')
    line_item_type = models.CharField(
        max_length=30, choices=LINE_ITEM_TYPE_CHOICES, default="unassigned_type")
    line_item_status = models.CharField(
        max_length=30, choices=LINE_ITEM_STATUS_CHOICES, default='not started')

    line_item_estimated_completion_at = models.DateTimeField(
        null=True, blank=True)

    # For tracking when this record was created.
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    udpated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'line_item_completion_tracking_new_03'
        ordering = ['-id', '-created_at']


# model stores reponses of api calls to plate2vin by entering a combo of plate and state.
# use the combo of plate and state to determine if newer information need to be pulled.
class LicensePlateSnapShotsPlate2Vin(models.Model):
    id = models.BigAutoField(primary_key=True)
    api_url = models.URLField(max_length=500, null=True, blank=True)
    api_response = models.JSONField(null=True, verbose_name="api_response")
    license_plate = models.CharField(
        max_length=10, null=True, db_index=True)
    state = models.CharField(max_length=2, null=True, db_index=True)
    vin = models.CharField(max_length=17, db_index=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    make = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=50, null=True)
    trim = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    engine = models.CharField(max_length=50, null=True)
    style = models.CharField(max_length=50, null=True)
    transmission = models.CharField(max_length=50, null=True)
    drive_type = models.CharField(max_length=20)
    fuel = models.CharField(max_length=20, null=True)
    color_name = models.CharField(max_length=50, null=True, blank=True)
    color_abbreviation = models.CharField(max_length=15, null=True)
    # keeps 5 versions of any license plates
    version = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL,
                                   null=True, related_name='license_plate_searches')
    # added to fresh anytime a new api is called for the same license plate and state
    last_checked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ''.join(self.license_plate, ' ', self.state)

    class Meta:
        db_table = 'licenseplate_snapshots_plate2vin'
        ordering = ["-id", '-created_at', "license_plate", '-version']
        indexes = [
            models.Index(fields=['-created_at', 'license_plate', 'state']),
        ]
