from .base import models,InternalUser

class PurchaseVendor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    address_formatted = models.TextField(null=True, blank=True) # reserved for formatted address via google map api verification
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    comment_json = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, related_name='purchase_vendor_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='purchase_vendor_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'purchase_vendor'
        verbose_name = 'Purchase Vendor'
        verbose_name_plural = 'Purchase Vendors'
        ordering = ['name']
        unique_together = ('name', 'is_active')
        permissions = [
            ('view_purchase_vendor', 'Can view Purchase Vendor'),
            ('create_purchase_vendor', 'Can create Purchase Vendor'),
            ('edit_purchase_vendor', 'Can edit Purchase Vendor'),
            ('delete_purchase_vendor', 'Can delete Purchase Vendor'),
        ]

