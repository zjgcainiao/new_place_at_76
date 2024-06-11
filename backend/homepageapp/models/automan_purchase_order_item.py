from django.db import models
from .automan_purchase_order import AutomanPurchaseOrder
from decimal import Decimal


class AutomanPurchaseOrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    automan_purchase_order = models.ForeignKey(
        AutomanPurchaseOrder,
        on_delete=models.DO_NOTHING,
        related_name='automan_purchase_order_items')
    quantity = models.IntegerField(default=0)
    # is_taxable = models.BooleanField(default=False)
    unit_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    line_total = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_line_total(self):
        self.line_total = Decimal(self.quantity) * \
            Decimal(self.unit_price or 0.00)
        self.save()

    class Meta:
        db_table = "automan_purchase_order_items"
        ordering = ['-created_at']
