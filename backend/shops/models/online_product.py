
from .base import models, settings, InternalUser, CustomerUser

class OnlineProducts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Product Name")
    delivery_method = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True,verbose_name="Product Description")
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    created_by = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING, null=True, blank=True,related_name="online_product_created_by")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="online_product_updated_by")

    
    class Meta:
        db_table = 'onlineproducts_new_03'
        ordering = ["-id", 'name']

    
