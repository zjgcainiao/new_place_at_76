from .base import models, InternalUser
from .vendor import Vendors
from .address import AddressesNewSQL02Model

class VendorAdddresses(models.Model):

    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(
        AddressesNewSQL02Model, on_delete=models.CASCADE,null=True, blank=True)
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
