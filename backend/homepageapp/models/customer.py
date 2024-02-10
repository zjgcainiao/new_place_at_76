from .base import models, InternalUser, FormattedPhoneNumberField
from .address import AddressesNewSQL02Model
from .email import EmailsNewSQL02Model
from .phone import PhonesNewSQL02Model
from .tax import TaxesModel

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
