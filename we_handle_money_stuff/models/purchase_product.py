from .base import models,InternalUser

# this class tracks the product that was purchased by the shop.
# this class is NOT a list of our own products, but rather a list of products that we have purchased from a vendor. Check OnlineProduct in the shops app for our own products.
# this class should be work hand in hand with Part and Vendor modes in the homepageapp. 

class PurchaseProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(InternalUser, related_name='purchase_product_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='purchase_product_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'purchase_products'
        ordering = ["-id"]
        verbose_name = 'Purchase Product'
        verbose_name_plural = 'Purchase Products'
        indexes = [
            models.Index(fields=['name', 'price']),
        ]
        permissions = [
            ('view_purchase_product', 'Can view Purchase Product'),
            ('create_purchase_product', 'Can create Purchase Product'),
            ('edit_purchase_product', 'Can edit Purchase Product'),
            ('delete_purchase_product', 'Can delete Purchase Product'),
        ]