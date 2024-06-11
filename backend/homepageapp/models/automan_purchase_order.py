from django.db import models
from decimal import Decimal


PURCHASE_SOURCE_CHOICES = [
    ('online_amazon', 'Online Purchase - Amazon'),
    ('online_ebay', 'Online Purchase - Ebay'),
    ('online_oreilly', 'Online Purchase - OReilly'),
    ('online_autozone', 'Online Purchase - Autozone'),
    ('physical_order', 'Purcased at Physical Locations (Stores, Dealerships etc)'),
]


class AutomanPurchaseOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_date = models.DateTimeField()
    source = models.CharField(
        max_length=100, choices=PURCHASE_SOURCE_CHOICES)
    source_order_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Original Purchase Order Id')
    scanned_image = models.ImageField(
        '/scanned_purchase_orders', null=True, blank=True)
    supplier = models.CharField(max_length=255, null=True, blank=True)
    expected_delivery_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    order_status = models.CharField(
        max_length=200,
        choices=[  # Define choices
            ('Pending', 'Pending'), ('Approved', 'Approved'), 
            ('Shipped', 'Shipped'), ('Delayed', 'Delayed'),
            ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'),
            ('Converted_to_Inventory_Item', 'Converted to Inventory Item')
        ]
    )
    purchase_reason = models.CharField(max_length=50,
                                       choices=[('inventory', 'Inventory'),
                                                ('repair_order', 'Repair Order'),])

    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True)
    shippinng_address = models.CharField(
        max_length=4000, null=True, blank=True)
    billing_address = models.CharField(max_length=4000, null=True, blank=True)

    updated_at = models.DateTimeField(
        auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "automan_purchase_order"
        ordering = ['-created_at']
