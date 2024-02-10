from .base import models, InternalUser,FormattedPhoneNumberField

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

