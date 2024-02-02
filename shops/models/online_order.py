from .base import models, settings, InternalUser, CustomerUser

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