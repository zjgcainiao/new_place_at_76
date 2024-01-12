from django.db import models
from internal_users.models import InternalUser
from customer_users.models import CustomerUser

from django.db import models
from django.conf import settings

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

    class OnlineOrders(models.Model):
        id = models.AutoField(primary_key=True)
        order_number = models.CharField(max_length=100, null=True, blank=True)
        order_total = models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
        order_status = models.CharField(max_length=100, null=True, blank=True)
        order_date = models.DateTimeField(auto_now_add=True)
        order_created_by = models.ForeignKey(
            InternalUser, on_delete=models.DO_NOTHING, null=True, blank=True)
        order_updated_at = models.DateTimeField(auto_now=True)
        order_updated_by = models.ForeignKey(
            InternalUser, on_delete=models.CASCADE, null=True, blank=True, related_name="online_order_updated_by")
        order_customer_id = models.ForeignKey(
            CustomerUser, on_delete=models.CASCADE, null=True, blank=True, related_name="online_order_customer")

        class Meta:
            db_table = 'onlineorders_new_03'
            ordering = ["-id", 'order_number']




class UserSearchCount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.search_count}"
