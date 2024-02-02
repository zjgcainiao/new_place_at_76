from .base import models, InternalUser
from .purchase_vendor import PurchaseVendor
from .purchase_order import PurchaseOrder

class PurchaseInvoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    invoice_number = models.CharField(max_length=100,blank=True,null=True)
    invoice_date = models.DateField(blank=True,null=True)
    description = models.TextField(null=True, blank=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.DO_NOTHING, null=True, blank=True)
    invoice_due_at = models.DateTimeField(null=True, blank=True)
    invoice_status = models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid'),('partial',"Partial")], max_length=50, default='unpaid')
    invoice_amount = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)
    scanned_image = models.ImageField(upload_to='invoices/', null=True, blank=True)
    comment_json = models.JSONField(null=True, blank=True)
    manual_review_at = models.DateTimeField(null=True, blank=True)
    manual_review_by = models.ForeignKey(InternalUser, related_name='scanned_invoice_manual_review_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(InternalUser, related_name='scanned_invoice_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='scanned_invoice_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'purchase_invoice'
        managed = True
        verbose_name = 'Purchase Invoice'
        verbose_name_plural = 'Purchase Invoices'
        ordering = ['-id']
        unique_together = ('invoice_number', 'invoice_date')
        permissions = [
            ('view_purchase_invoice', 'Can view Purchase Invoice'),
            ('create_purchase_invoice', 'Can create Purchase Invoice'),
            ('edit_purchase_invoice', 'Can edit Purchase Invoice'),
            ('delete_purchase_invoice', 'Can delete Purchase Invoice'),
        ]