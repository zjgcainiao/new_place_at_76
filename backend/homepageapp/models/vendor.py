# 2023-10-16 added new model Vendors (for vehicles)
from .base import models, InternalUser,FormattedPhoneNumberField

class Vendors(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    vendor_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Business Name')
    vendor_contact_persons = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Contact Person (i.e. Kenny)')
    vendor_contact_phone_number = FormattedPhoneNumberField(null=True, blank=True)
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
    vendor_type = models.IntegerField(null=True, blank=True)
    vendor_catalog_link = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True, 
        null=True,blank=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='vendors_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='vendors_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'vendors_new_03'
        ordering = ["-vendor_id"]
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

