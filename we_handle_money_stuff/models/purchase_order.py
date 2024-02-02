from .base import models, InternalUser
from .purchase_vendor import PurchaseVendor


class PurchaseOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    
    order_date = models.DateTimeField()
    purchase_vendor = models.ForeignKey(PurchaseVendor, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    expected_delivery_at = models.DateTimeField(null=True, blank=True)
    status= models.CharField(choices=[('ordered', 'Ordered'), ('delivered', 'Delivered'),('cancelled',"Cancelled"),('returning','Returning'),('refunded','Refunded')], max_length=50, default='ordered')
    total_amount= models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(InternalUser, related_name='purchase_order_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='purchase_order_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'purchase_order'
        managed = True
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-id']
        permissions = [
            ('view_purchase_order', 'Can view Purchase Order'),
            ('create_purchase_order', 'Can create Purchase Order'),
            ('edit_purchase_order', 'Can edit Purchase Order'),
            ('delete_purchase_order', 'Can delete Purchase Order'),
        ]