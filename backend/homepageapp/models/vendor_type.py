
# 2023-10-16 added new model VendorType. It defines types of vehicle related whole sale vendors: tire shop, repair shop, dealerhip
from .base import models, InternalUser

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