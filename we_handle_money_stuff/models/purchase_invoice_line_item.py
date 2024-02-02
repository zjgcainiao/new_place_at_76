from .base import models,InternalUser
from .purchase_invoice import PurchaseInvoice


class PurchaseInvoiceLineItem(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_line_type = models.CharField(choices=[('product', 'Product'), ('service', 'Service'),('tax',"Tax"),("discount","Discount"),('undefined','Undefined')], max_length=50, default='undefined')
    name = models.CharField(max_length=255, null=True, blank=True)
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(InternalUser, related_name='purchase_invoice_line_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='purchase_invoice_line_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    
    class Meta:
        db_table = 'purchase_invoice_line_items'
        ordering = ["-id"]
        verbose_name = 'Purchase Invoice Line Item'
        verbose_name_plural = 'Purchase Invoice Line Items'
        permissions = [
            ('view_purchase_invoice_line_item', 'Can view Purchase Invoice Line Item'),
            ('create_purchase_invoice_line_item', 'Can create Purchase Invoice Line Item'),
            ('edit_purchase_invoice_line_item', 'Can edit Purchase Invoice Line Item'),
            ('delete_purchase_invoice_line_item', 'Can delete Purchase Invoice Line Item'),
        ]
